# broker/memory.py
"""
In‑memory (single‑process) broker backend.
- Zero sockets, zero IPC, zero persistence.
- Thread‑safe for multiple worker threads inside one Python process.
- Surface is compatible with LocalBroker and the Broker contracts used by TaskRunner.

Intended use:
    BROKER_TYPE=inmem (see factory wiring below)

Limitations:
- Not visible across OS processes. Use your BaseManager/LocalBroker when you need multi‑process.
- Dead‑letter messages are kept in RAM only.
"""
from __future__ import annotations

import logging
import threading
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

from .contracts import (
    Broker,
    BrokerMessage,
    TopicState,
    TopicInfo,
    TopicConfig,
    WorkerInfo,
    ClusterStats,
    ActiveTaskInfo,
    LockInfo,
)

log = logging.getLogger("InMemoryBroker")


class InMemoryBroker(Broker):
    """A drop‑in, in‑process broker implementation."""

    def __init__(self) -> None:
        # Synchronization primitive (protects all state below)
        self._cv = threading.Condition()

        # Message id generator
        self._next_id = 1

        # Runtime state
        self._topics: Dict[str, TopicState] = {}
        self._running: Dict[str, BrokerMessage] = {}
        self._workers: Dict[str, WorkerInfo] = {}
        self._worker_tasks: Dict[str, set[str]] = {}

        # Simple exclusive locks (task_id keyed)
        self._locks: Dict[str, Dict[str, Any]] = {}
        self._locks_by_name: Dict[str, str] = {}

        # Heartbeat staleness threshold (seconds)
        self._hb_ttl = 10.0

        # Optional role tag
        self.role: Optional[str] = "inmem"

        # Round‑robin cursor for wildcard topic pick
        self._topic_rr_index = 0

    # ------------- lifecycle -------------
    def setup(self) -> None:
        # No external resources to start
        return None

    def wait_ready(self) -> None:
        # Always ready
        return None

    # ------------- topic helpers -------------
    def ensure_topic(self, topic: str) -> None:
        with self._cv:
            self._ensure_topic_locked(topic)

    def _ensure_topic_locked(self, topic: str) -> TopicState:
        ts = self._topics.get(topic)
        if ts is None:
            ts = TopicState()
            self._topics[topic] = ts
        return ts

    # ------------- core ops -------------
    def publish(self, topic: str, payload: Dict[str, Any], headers: Optional[Dict[str, Any]] = None) -> str:
        headers = dict(headers or {})
        with self._cv:
            msg_id = f"inmem:{self._next_id}"
            self._next_id += 1
            msg = BrokerMessage(
                id=msg_id,
                topic=topic,
                payload=dict(payload or {}),
                headers=headers,
                attempts=0,
                created_at=datetime.now(timezone.utc),
            )
            ts = self._ensure_topic_locked(topic)
            ts.q.append(msg)
            ts.total_count += 1
            self._cv.notify_all()
            return msg_id

    def _has_global_permit_locked(self, topic: str) -> bool:
        ts = self._topics.get(topic)
        if ts is None:
            return True
        lim = ts.config.concurrency_limit
        if lim is None:
            return True
        return ts.running < int(lim)

    def _choose_wildcard_topic_locked(self) -> Optional[str]:
        if not self._topics:
            return None
        names = sorted(self._topics.keys())
        n = len(names)
        if n == 0:
            return None
        # round‑robin scan from last index for fairness
        start = self._topic_rr_index % n
        for i in range(n):
            name = names[(start + i) % n]
            ts = self._topics[name]
            if ts.q and self._has_global_permit_locked(name):
                self._topic_rr_index = (start + i + 1) % n
                return name
        return None

    def claim(self, topic: str, worker_id: str) -> Optional[BrokerMessage]:
        with self._cv:
            if topic == "*":
                sel = self._choose_wildcard_topic_locked()
                if sel is None:
                    return None
                ts = self._topics[sel]
            else:
                sel = topic
                ts = self._ensure_topic_locked(sel)
                if not ts.q:
                    return None
                if not self._has_global_permit_locked(sel):
                    return None

            msg = ts.q.popleft()
            msg.attempts += 1
            # decorate headers best‑effort
            try:
                msg.headers["worker_id"] = worker_id
                msg.headers["claimed_at"] = datetime.now(timezone.utc).isoformat()
            except Exception:
                msg.headers = {"worker_id": worker_id, "claimed_at": datetime.now(timezone.utc).isoformat()}

            self._running[msg.id] = msg
            self._worker_tasks.setdefault(worker_id, set()).add(msg.id)
            ts.running += 1
            return msg

    def ack(self, msg_id: str) -> None:
        with self._cv:
            msg = self._running.pop(msg_id, None)
            if not msg:
                return
            wid = (msg.headers or {}).get("worker_id")
            if wid:
                self._worker_tasks.get(wid, set()).discard(msg_id)
            ts = self._topics.get(msg.topic)
            if ts:
                if ts.running > 0:
                    ts.running -= 1
                ts.completed_count += 1

            # Auto‑release any lock associated with this task
            try:
                task_id = (msg.payload or {}).get("task_id") or msg_id
                if task_id in self._locks:
                    self._release_lock_no_owner_check_locked(task_id)
            except Exception:
                pass

            self._cv.notify_all()

    def nack(self, msg_id: str, requeue: bool = True) -> None:
        with self._cv:
            msg = self._running.pop(msg_id, None)
            if not msg:
                return
            wid = (msg.headers or {}).get("worker_id")
            if wid:
                self._worker_tasks.get(wid, set()).discard(msg_id)
            ts = self._topics.get(msg.topic)
            if ts and ts.running > 0:
                ts.running -= 1

            try:
                task_id = (msg.payload or {}).get("task_id") or msg_id
                if task_id in self._locks:
                    self._release_lock_no_owner_check_locked(task_id)
            except Exception:
                pass

            if requeue:
                self._ensure_topic_locked(msg.topic).q.appendleft(msg)
                # Increment error count (task failed and will be retried)
                if ts:
                    ts.error_count += 1
            else:
                ts = self._ensure_topic_locked(msg.topic)
                if ts.config.dead_letter_enabled:
                    ts.dead.append(msg)
                # Increment skipped count (task was skipped/dead-lettered)
                ts.skipped_count += 1
            self._cv.notify_all()

    # ------------- workers / heartbeat -------------
    def register_worker(
        self,
        worker_id: str,
        *,
        pid: int,
        host: str,
        topics: List[str],
        capacity: int,
        role: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._cv:
            self._workers[worker_id] = WorkerInfo(
                worker_id=worker_id,
                host=host,
                pid=int(pid),
                capacity=int(capacity or 1),
                running=0,
                running_hint=None,
                stale=False,
                topics=list(topics or []),
                started_at=now,
                last_heartbeat=now,
                role=role or self.role,
                meta=dict(meta or {}),
                tasks=None,
            )
            self._worker_tasks.setdefault(worker_id, set())
            self._cv.notify_all()

    def heartbeat(self, worker_id: str, running: Optional[int] = None, capacity: Optional[int] = None,
                  meta: Optional[Dict[str, Any]] = None) -> None:
        with self._cv:
            w = self._workers.get(worker_id)
            if not w:
                return
            w.last_heartbeat = datetime.now(timezone.utc).isoformat()
            if capacity is not None:
                w.capacity = int(capacity)
            if running is not None:
                w.running_hint = int(running)
            if meta is not None:
                w.meta = dict(w.meta or {})
                w.meta["hb"] = meta
            self._cv.notify_all()

    def unregister_worker(self, worker_id: str) -> None:
        with self._cv:
            self._workers.pop(worker_id, None)
            self._worker_tasks.pop(worker_id, None)
            self._cv.notify_all()

    def get_workers(self, include_tasks: bool = False, stale_after: Optional[float] = None) -> List[WorkerInfo]:
        with self._cv:
            now = datetime.now(timezone.utc)
            ttl = stale_after if stale_after is not None else self._hb_ttl
            out: List[WorkerInfo] = []
            for w in self._workers.values():
                running = len(self._worker_tasks.get(w.worker_id, ()))
                hb = getattr(w, 'last_heartbeat', None)
                try:
                    hb_dt = datetime.fromisoformat(hb) if hb else None
                except Exception:
                    hb_dt = None
                stale = False
                if hb_dt is not None:
                    stale = (now - hb_dt) > timedelta(seconds=ttl)
                tasks_list = None
                if include_tasks:
                    tasks_list = sorted(list(self._worker_tasks.get(w.worker_id, ())))
                out.append(WorkerInfo(
                    worker_id=w.worker_id,
                    host=w.host,
                    pid=int(w.pid),
                    capacity=int(w.capacity),
                    running=running,
                    running_hint=w.running_hint,
                    stale=stale,
                    topics=sorted(list(w.topics)),
                    started_at=w.started_at,
                    last_heartbeat=hb or w.started_at,
                    role=w.role,
                    meta=w.meta,
                    tasks=tasks_list,
                ))
            return out

    # ------------- listings / stats -------------
    def get_topics(self) -> List[TopicInfo]:
        with self._cv:
            out: List[TopicInfo] = []
            for name, ts in self._topics.items():
                subscribers = sum(1 for w in self._workers.values() if (name in w.topics) or ("*" in w.topics))
                out.append(ts.to_info(name, subscribers))
            return sorted(out, key=lambda x: x.topic)

    def get_cluster_stats(self) -> ClusterStats:
        with self._cv:
            total_capacity = sum(w.capacity for w in self._workers.values())
            total_running = sum(len(s) for s in self._worker_tasks.values())
            return ClusterStats(
                workers=len(self._workers),
                total_capacity=total_capacity,
                total_running=total_running,
                topics=self.get_topics(),
                broker_type="memory",
            )

    def stats(self) -> Dict[str, Any]:
        cs = self.get_cluster_stats()
        return {
            "workers": cs.workers,
            "total_capacity": cs.total_capacity,
            "total_running": cs.total_running,
            "topics": [t.topic for t in cs.topics],
            "broker_type": cs.broker_type,
        }

    def get_all_active_tasks(self, topic: Optional[str]) -> List[ActiveTaskInfo]:
        with self._cv:
            items: List[ActiveTaskInfo] = []
            # queued
            if topic is None:
                it = [(name, ts.q) for name, ts in self._topics.items()]
            else:
                q = self._topics.get(topic, TopicState()).q
                it = [(topic, q)]
            for _, q in it:
                for m in list(q):
                    items.append(ActiveTaskInfo(
                        id=m.id, topic=m.topic, payload=m.payload,
                        headers=dict(m.headers or {}), attempts=m.attempts,
                        created_at=m.created_at.isoformat(), state="queued"
                    ))
            # running
            for m in self._running.values():
                if topic is not None and m.topic != topic:
                    continue
                items.append(ActiveTaskInfo(
                    id=m.id, topic=m.topic, payload=m.payload,
                    headers=dict(m.headers or {}), attempts=m.attempts,
                    created_at=m.created_at.isoformat(), state="running",
                    claimed_by=(m.headers or {}).get("worker_id")
                ))
            return items

    # ------------- locks -------------
    def _release_lock_no_owner_check_locked(self, task_id: str) -> bool:
        info = self._locks.pop(task_id, None)
        if not info:
            return False
        tname = info.get("task_name")
        if tname and self._locks_by_name.get(tname) == task_id:
            self._locks_by_name.pop(tname, None)
        return True

    def acquire_lock(self, task_name: str, task_id: str, locked_by: str) -> bool:
        if not task_id:
            return False
        if not task_name:
            task_name = task_id
        with self._cv:
            xid = self._locks_by_name.get(task_name)
            if xid and xid != task_id:
                return False
            self._locks[task_id] = {
                "task_id": task_id,
                "task_name": task_name,
                "locked_by": locked_by,
                "acquired_at": datetime.now(timezone.utc).isoformat(),
            }
            self._locks_by_name[task_name] = task_id
            self._cv.notify_all()
            return True

    def release_lock(self, task_id: str, locked_by: Optional[str] = None) -> bool:
        if not task_id:
            return False
        with self._cv:
            info = self._locks.get(task_id)
            if not info:
                return False
            if locked_by is not None and info.get("locked_by") != locked_by:
                return False
            ok = self._release_lock_no_owner_check_locked(task_id)
            self._cv.notify_all()
            return ok

    def get_locks(self) -> List[LockInfo]:
        with self._cv:
            return [
                LockInfo(
                    task_id=tid,
                    task_name=info.get("task_name"),
                    locked_by=info.get("locked_by"),
                    acquired_at=info.get("acquired_at"),
                )
                for tid, info in self._locks.items()
            ]

    def force_release_lock(self, task_id: str) -> bool:
        with self._cv:
            ok = self._release_lock_no_owner_check_locked(task_id)
            self._cv.notify_all()
            return ok

    # ------------- topic config -------------
    def set_topic_config(self, topic: str, config: TopicConfig) -> None:
        with self._cv:
            ts = self._ensure_topic_locked(topic)
            lim = None if config.concurrency_limit is None else int(config.concurrency_limit)
            if lim is not None and lim < 0:
                raise ValueError("concurrency_limit must be >= 0 or None")
            ts.config = TopicConfig(
                concurrency_limit=lim,
                max_retries=config.max_retries,
                dead_letter_enabled=bool(config.dead_letter_enabled),
                retention_seconds=config.retention_seconds,
            )
            self._cv.notify_all()

    def get_topic_config(self, topic: str) -> TopicConfig:
        with self._cv:
            return self._ensure_topic_locked(topic).config

    def get_all_topic_configs(self) -> Dict[str, TopicConfig]:
        with self._cv:
            return {name: ts.config for name, ts in self._topics.items()}

    # Legacy helpers expected by runner/manager
    def set_topic_concurrency_limit(self, topic: str, limit: Optional[int]) -> None:
        self.set_topic_config(topic, TopicConfig(concurrency_limit=limit))

    def get_topic_concurrency_limits(self) -> Dict[str, Optional[int]]:
        with self._cv:
            return {name: ts.config.concurrency_limit for name, ts in self._topics.items()}

    def get_topic_running(self) -> Dict[str, int]:
        with self._cv:
            return {name: ts.running for name, ts in self._topics.items()}
