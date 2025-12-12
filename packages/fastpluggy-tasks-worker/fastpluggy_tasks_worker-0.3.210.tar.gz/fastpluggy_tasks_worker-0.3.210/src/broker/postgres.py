# broker/postgres.py
"""
PostgreSQL-backed Broker implementation using SQLAlchemy (sync).

Contract: implements the synchronous Broker interface defined in broker/contracts.py
with minimal but complete functionality used by TaskRunner and the UI routes.

Design:
- messages table holds queued/running/dead messages (payload + headers JSON)
- topic_config table stores TopicConfig per topic
- topic_stats table accumulates counters (completed, errors, skipped, total)
- workers table stores worker heartbeats / capacity for observability

Concurrency:
- claim() uses SELECT ... FOR UPDATE SKIP LOCKED to safely fetch the next available
  message without blocking other workers.

IDs:
- Messages are returned as id like "pg:<int>" to make source obvious in logs/metrics.

Configuration:
- Uses fastpluggy.core.database.get_database_url() environment wiring, so you can set
  DATABASE_URL to a postgres URL (e.g., postgresql+psycopg://user:pass@host/db)

Note:
- This is a minimal viable implementation. Some optional APIs return empty/defaults
  where not critical to TaskRunner operation.
"""
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
import time

from fastpluggy.core.tools.serialize_tools import serialize_value
from sqlalchemy import (
    JSON,
    BigInteger,
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    select,
    func,
    update,
    insert,
    delete,
    case,
)
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from .contracts import (
    Broker,
    BrokerMessage,
    TopicConfig,
    TopicInfo,
    WorkerInfo,
    ClusterStats,
    ActiveTaskInfo,
    LockInfo,
)

try:
    # Prefer the shared helper so the same DB URL resolution is used across plugins
    from fastpluggy.core.database import get_database_url
except Exception:  # pragma: no cover - fallback for environments without fastpluggy installed
    import os
    def get_database_url() -> str:
        return os.getenv("DATABASE_URL", "sqlite:///./tasks_worker_pg_broker.db")


# ---------- SQLAlchemy metadata / tables ----------
metadata = MetaData()

messages = Table(
    "tw_messages",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("topic", String(255), nullable=False, index=True),
    Column("payload", JSON, nullable=False),
    Column("headers", JSON, nullable=False, default={}),
    Column(
        "state",
        String(20),
        nullable=False,
        default="created",
        index=True,
    ),
    Column("attempts", Integer, nullable=False, default=0),
    Column("claimed_by", String(255), nullable=True, index=True),
    Column("claimed_at", DateTime(timezone=True), nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)),
)

# Per-topic configuration persisted as JSON
topic_config = Table(
    "tw_topic_config",
    metadata,
    Column("topic", String(255), primary_key=True),
    Column("config", JSON, nullable=False, default={}),
)

# Per-topic cumulative counters so we don't lose stats after deletes
topic_stats = Table(
    "tw_topic_stats",
    metadata,
    Column("topic", String(255), primary_key=True),
    Column("completed_count", BigInteger, nullable=False, default=0),
    Column("error_count", BigInteger, nullable=False, default=0),
    Column("skipped_count", BigInteger, nullable=False, default=0),
    Column("total_count", BigInteger, nullable=False, default=0),
)

# Observability of workers
workers = Table(
    "tw_workers",
    metadata,
    Column("worker_id", String(255), primary_key=True),
    Column("pid", Integer, nullable=True),
    Column("host", String(255), nullable=True),
    Column("topics", Text, nullable=True),  # comma-separated list
    Column("capacity", Integer, nullable=True),
    Column("running", Integer, nullable=True),
    Column("role", String(64), nullable=True),
    Column("meta", JSON, nullable=True),
    Column("last_heartbeat", DateTime(timezone=True), nullable=True, index=True),
)

# Simple exclusive locks table
locks = Table(
    "tw_locks",
    metadata,
    Column("task_id", String(255), primary_key=True),
    Column("task_name", String(255), nullable=False, unique=True),  # ensure exclusive per task_name
    Column("locked_by", String(255), nullable=True),
    Column("acquired_at", DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)),
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _topic_list_to_str(topics: List[str]) -> str:
    return ",".join(sorted(set(topics or [])))


def _ensure_topic_stats(sess: Session, topic: str) -> None:
    exists = sess.execute(select(topic_stats.c.topic).where(topic_stats.c.topic == topic)).first()
    if not exists:
        sess.execute(insert(topic_stats).values(topic=topic, completed_count=0, error_count=0, skipped_count=0, total_count=0))


def _ensure_topic_config(sess: Session, topic: str) -> None:
    exists = sess.execute(select(topic_config.c.topic).where(topic_config.c.topic == topic)).first()
    if not exists:
        sess.execute(insert(topic_config).values(topic=topic, config={}))


class PostgresBroker(Broker):
    def __init__(self, database_url: Optional[str] = None) -> None:
        self.database_url = database_url or get_database_url()
        # Create a sync Engine; psycopg or psycopg2 are supported via URL scheme
        self.engine: Engine = create_engine(self.database_url, future=True)
        self.role: Optional[str] = "postgres"

    # ---------- lifecycle ----------
    def setup(self) -> None:
        # Create tables one by one to avoid touching unrelated metadata
        for tbl in (messages, topic_config, topic_stats, workers, locks):
            tbl.create(self.engine, checkfirst=True)

    def wait_ready(self, timeout: Optional[float] = 30.0, interval: float = 0.5) -> bool:
        """
        Block until the Postgres backend is reachable and required tables exist.
        Returns True when ready, False if the timeout elapses.
        """
        start = time.time()
        while True:
            try:
                with self.engine.connect() as conn:
                    # basic connectivity check
                    conn.exec_driver_sql("SELECT 1")
                # Ensure tables are created once connection is OK
                self.setup()
                return True
            except Exception:
                # Not ready yet
                if timeout is not None and (time.time() - start) >= float(timeout):
                    return False
                time.sleep(max(0.05, float(interval)))

    # ---------- helpers ----------
    def _pg_id(self, raw_id: int) -> str:
        return f"pg:{raw_id}"

    def _parse_id(self, msg_id: str) -> int:
        if msg_id.startswith("pg:"):
            return int(msg_id.split(":", 1)[1])
        # allow raw numeric for flexibility
        try:
            return int(msg_id)
        except Exception:
            raise ValueError(f"Invalid PostgresBroker message id: {msg_id}")

    # ---------- core ops ----------
    def publish(self, topic: str, payload: Dict[str, Any], headers: Optional[Dict[str, Any]] = None) -> str:
        headers = dict(headers or {})
        with Session(self.engine) as sess, sess.begin():
            _ensure_topic_stats(sess, topic)
            _ensure_topic_config(sess, topic)
            res = sess.execute(
                insert(messages)
                .values(
                    topic=topic,
                    payload=serialize_value(dict(payload or {}), serialize_dates=True),
                    headers=serialize_value(headers or {}, serialize_dates=True),
                    state="queued",
                    attempts=0,
                    created_at=_now(),
                )
                .returning(messages.c.id)
            )
            raw_id = res.scalar_one()
            # bump totals
            sess.execute(
                update(topic_stats)
                .where(topic_stats.c.topic == topic)
                .values(total_count=topic_stats.c.total_count + 1)
            )
            return self._pg_id(int(raw_id))

    def claim(self, topic: str, worker_id: str) -> Optional[BrokerMessage]:
        with Session(self.engine) as sess, sess.begin():
            # concurrency limit check: if set, only allow claim when running < limit
            cfg_row = sess.execute(select(topic_config.c.config).where(topic_config.c.topic == topic)).first()
            if cfg_row:
                cfg = TopicConfig(**cfg_row[0]) if cfg_row[0] else TopicConfig()
                if cfg.concurrency_limit is not None:
                    cur_running = sess.execute(
                        select(func.count()).select_from(messages).where(
                            (messages.c.topic == topic) & (messages.c.state == "running")
                        )
                    ).scalar_one()
                    if int(cur_running) >= int(cfg.concurrency_limit):
                        return None

            # Select the next queued message using SKIP LOCKED
            msg_row = sess.execute(
                select(
                    messages.c.id,
                    messages.c.payload,
                    messages.c.headers,
                    messages.c.attempts,
                    messages.c.created_at,
                )
                .where((messages.c.topic == topic) & (messages.c.state == "queued"))
                .order_by(messages.c.id.asc())
                .with_for_update(skip_locked=True)
                .limit(1)
            ).first()

            if not msg_row:
                return None

            raw_id: int = int(msg_row.id)
            # Mark as running and increment attempts
            sess.execute(
                update(messages)
                .where(messages.c.id == raw_id)
                .values(state="running", attempts=messages.c.attempts + 1, claimed_by=worker_id, claimed_at=_now())
            )

            return BrokerMessage(
                id=self._pg_id(raw_id),
                topic=topic,
                payload=dict(msg_row.payload or {}),
                headers=dict(msg_row.headers or {}),
                attempts=int(msg_row.attempts) + 1,
                created_at=msg_row.created_at or _now(),
            )

    def ack(self, msg_id: str) -> None:
        raw_id = self._parse_id(msg_id)
        with Session(self.engine) as sess, sess.begin():
            # fetch topic then delete and increment completed counter
            row = sess.execute(select(messages.c.topic).where(messages.c.id == raw_id)).first()
            if not row:
                return None
            topic = row[0]
            sess.execute(delete(messages).where(messages.c.id == raw_id))
            _ensure_topic_stats(sess, topic)
            sess.execute(
                update(topic_stats)
                .where(topic_stats.c.topic == topic)
                .values(completed_count=topic_stats.c.completed_count + 1)
            )
            return None

    def nack(self, msg_id: str, requeue: bool = True) -> None:
        raw_id = self._parse_id(msg_id)
        with Session(self.engine) as sess, sess.begin():
            row = sess.execute(select(messages.c.topic).where(messages.c.id == raw_id)).first()
            if not row:
                return None
            topic = row[0]
            if requeue:
                sess.execute(
                    update(messages)
                    .where(messages.c.id == raw_id)
                    .values(state="queued", claimed_by=None, claimed_at=None)
                )
                _ensure_topic_stats(sess, topic)
                sess.execute(
                    update(topic_stats)
                    .where(topic_stats.c.topic == topic)
                    .values(error_count=topic_stats.c.error_count + 1)
                )
            else:
                sess.execute(update(messages).where(messages.c.id == raw_id).values(state="dead"))
                _ensure_topic_stats(sess, topic)
                sess.execute(
                    update(topic_stats)
                    .where(topic_stats.c.topic == topic)
                    .values(skipped_count=topic_stats.c.skipped_count + 1)
                )
            return None

    # ---------- optional API ----------
    def ensure_topic(self, topic: str) -> None:
        with Session(self.engine) as sess, sess.begin():
            _ensure_topic_stats(sess, topic)
            _ensure_topic_config(sess, topic)

    def stats(self) -> Dict[str, Any]:
        with Session(self.engine) as sess:
            topics_count = sess.execute(select(func.count()).select_from(topic_stats)).scalar_one()
            queued = sess.execute(select(func.count()).select_from(messages).where(messages.c.state == "queued")).scalar_one()
            running_cnt = sess.execute(select(func.count()).select_from(messages).where(messages.c.state == "running")).scalar_one()
            dead = sess.execute(select(func.count()).select_from(messages).where(messages.c.state == "dead")).scalar_one()
            workers_count = sess.execute(select(func.count()).select_from(workers)).scalar_one()
            return {
                "topics": int(topics_count or 0),
                "queued": int(queued or 0),
                "running": int(running_cnt or 0),
                "dead": int(dead or 0),
                "workers": int(workers_count or 0),
                "role": self.role,
                "backend": "postgres",
            }

    def get_all_active_tasks(self, topic: Optional[str]) -> List[ActiveTaskInfo]:
        with Session(self.engine) as sess:
            where_clause = []
            if topic:
                where_clause.append(messages.c.topic == topic)
            # Include running as active; you could also include queued if desired for UI
            sel = select(
                messages.c.id,
                messages.c.topic,
                messages.c.payload,
                messages.c.headers,
                messages.c.attempts,
                messages.c.claimed_by,
                messages.c.state,
                messages.c.created_at,
            )
            if where_clause:
                sel = sel.where(*where_clause)
            sel = sel.where(messages.c.state.in_(["queued", "running"]))
            rows = sess.execute(sel.order_by(messages.c.created_at.asc()).limit(500)).all()
            out: List[ActiveTaskInfo] = []
            for r in rows:
                out.append(ActiveTaskInfo(
                    id=self._pg_id(int(r.id)),
                    topic=r.topic,
                    payload=dict(r.payload or {}),
                    headers=dict(r.headers or {}),
                    attempts=int(r.attempts or 0),
                    claimed_by=r.claimed_by,
                    created_at=r.created_at.isoformat() if r.created_at else None,
                    state=r.state,
                ))
            return out

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
        with Session(self.engine) as sess, sess.begin():
            sess.execute(
                pg_insert(workers)
                .values(
                    worker_id=worker_id,
                    pid=pid,
                    host=host,
                    topics=_topic_list_to_str(topics),
                    capacity=capacity,
                    running=0,
                    role=role or self.role,
                    meta=serialize_value(meta or {}, serialize_dates=True),
                    last_heartbeat=_now(),
                )
                .on_conflict_do_update(
                    index_elements=[workers.c.worker_id],
                    set_=dict(
                        pid=pid,
                        host=host,
                        topics=_topic_list_to_str(topics),
                        capacity=capacity,
                        role=role or self.role,
                        meta=serialize_value(meta or {}, serialize_dates=True),
                        last_heartbeat=_now(),
                    ),
                )
            )

    def heartbeat(
        self,
        worker_id: str,
        running: Optional[int] = None,
        capacity: Optional[int] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        with Session(self.engine) as sess, sess.begin():
            values = dict(last_heartbeat=_now())
            if running is not None:
                values["running"] = int(running)
            if capacity is not None:
                values["capacity"] = int(capacity)
            if meta is not None:
                values["meta"] = serialize_value(meta, serialize_dates=True)
            sess.execute(
                pg_insert(workers)
                .values(worker_id=worker_id, **values)
                .on_conflict_do_update(index_elements=[workers.c.worker_id], set_=values)
            )

    def unregister_worker(self, worker_id: str) -> None:
        with Session(self.engine) as sess, sess.begin():
            sess.execute(delete(workers).where(workers.c.worker_id == worker_id))

    def get_workers(self, include_tasks: bool = False, stale_after: Optional[float] = None) -> List[Union[WorkerInfo, Dict[str, Any]]]:
        with Session(self.engine) as sess:
            rows = sess.execute(select(
                workers.c.worker_id,
                workers.c.pid,
                workers.c.host,
                workers.c.topics,
                workers.c.capacity,
                workers.c.running,
                workers.c.role,
                workers.c.meta,
                workers.c.last_heartbeat,
            ).order_by(workers.c.worker_id.asc())).all()
            out: List[WorkerInfo] = []
            for r in rows:
                hb = r.last_heartbeat.isoformat() if r.last_heartbeat else None
                topics_list = (r.topics or "").split(",") if r.topics else []
                out.append(WorkerInfo(
                    worker_id=r.worker_id,
                    pid=r.pid or 0,
                    host=r.host or "",
                    capacity=r.capacity or 0,
                    running=r.running or 0,
                    running_hint=None,
                    stale=False,
                    topics=topics_list,
                    started_at=hb or "",
                    last_heartbeat=hb,
                    role=r.role,
                    meta=r.meta or {},
                    tasks=None,
                ))
            return out

    def get_topics(self) -> List[Union[TopicInfo, Dict[str, Any]]]:
        with Session(self.engine) as sess:
            # gather queue counters from messages
            counts = sess.execute(
                select(
                    messages.c.topic,
                    func.count().filter(messages.c.state == "queued").label("queued"),
                    func.count().filter(messages.c.state == "running").label("running"),
                    func.count().filter(messages.c.state == "dead").label("dead"),
                )
                .group_by(messages.c.topic)
            ).all()
            counts_by_topic: Dict[str, Dict[str, int]] = {}
            for r in counts:
                counts_by_topic[r.topic] = {
                    "queued": int(r.queued or 0),
                    "running": int(r.running or 0),
                    "dead": int(r.dead or 0),
                }

            # get configs
            cfg_rows = sess.execute(select(topic_config.c.topic, topic_config.c.config)).all()
            cfgs = {r.topic: TopicConfig(**(r.config or {})) for r in cfg_rows}

            # get cumulative stats
            stat_rows = sess.execute(select(
                topic_stats.c.topic,
                topic_stats.c.completed_count,
                topic_stats.c.error_count,
                topic_stats.c.skipped_count,
                topic_stats.c.total_count,
            )).all()
            s_by_topic = {r.topic: r for r in stat_rows}

            # compute subscribers from workers topics listing (best-effort)
            subs: Dict[str, int] = {}
            for r in sess.execute(select(workers.c.topics)).all():
                for t in (r.topics or "").split(","):
                    t = t.strip()
                    if not t:
                        continue
                    subs[t] = subs.get(t, 0) + 1

            # union of all topics seen
            topics = set(counts_by_topic) | set(cfgs) | set(s_by_topic) | set(subs)
            out: List[TopicInfo] = []
            for t in sorted(topics):
                c = counts_by_topic.get(t, {"queued": 0, "running": 0, "dead": 0})
                cfg = cfgs.get(t, TopicConfig())
                st = s_by_topic.get(t)
                out.append(TopicInfo(
                    topic=t,
                    queued=c["queued"],
                    running=c["running"],
                    dead_letter=c["dead"],
                    subscribers=subs.get(t, 0),
                    configuration=cfg,
                    completed_count=int(getattr(st, "completed_count", 0) or 0),
                    error_count=int(getattr(st, "error_count", 0) or 0),
                    skipped_count=int(getattr(st, "skipped_count", 0) or 0),
                    total_count=int(getattr(st, "total_count", 0) or 0),
                ))
            return out

    def get_cluster_stats(self) -> Union[ClusterStats, Dict[str, Any]]:
        # Provide something coherent based on messages and workers
        s = self.stats()
        # ClusterStats signature expects workers/capacity/running; map best-effort
        return ClusterStats(
            workers=int(s.get("workers", 0) or 0),
            total_capacity=int(s.get("capacity", 0) or 0),
            total_running=int(s.get("running", 0) or 0),
            topics=self.get_topics(),
            broker_type=self.role,
        )

    # ---------- Locks API ----------
    def acquire_lock(self, task_name: str, task_id: str, locked_by: str) -> bool:
        if not task_id:
            return False
        if not task_name:
            task_name = task_id
        with Session(self.engine) as sess, sess.begin():
            ins = pg_insert(locks).values(
                task_id=str(task_id),
                task_name=str(task_name),
                locked_by=str(locked_by) if locked_by is not None else None,
                acquired_at=_now(),
            ).on_conflict_do_nothing(index_elements=[locks.c.task_name])
            res = sess.execute(ins)
            # rowcount is 1 on success insert, 0 if conflict
            return (res.rowcount or 0) > 0

    def release_lock(self, task_id: str, locked_by: Optional[str] = None) -> bool:
        if not task_id:
            return False
        with Session(self.engine) as sess, sess.begin():
            cond = locks.c.task_id == str(task_id)
            if locked_by is not None:
                cond = cond & (locks.c.locked_by == str(locked_by))
            res = sess.execute(delete(locks).where(cond))
            return (res.rowcount or 0) > 0

    def get_locks(self) -> List[LockInfo]:
        with Session(self.engine) as sess:
            rows = sess.execute(select(locks.c.task_id, locks.c.task_name, locks.c.locked_by, locks.c.acquired_at)).all()
            out: List[LockInfo] = []
            for r in rows:
                out.append(LockInfo(
                    task_id=str(r.task_id),
                    task_name=r.task_name,
                    locked_by=r.locked_by,
                    acquired_at=r.acquired_at.isoformat() if r.acquired_at else None,
                ))
            return out

    def force_release_lock(self, task_id: str) -> bool:
        if not task_id:
            return False
        with Session(self.engine) as sess, sess.begin():
            res = sess.execute(delete(locks).where(locks.c.task_id == str(task_id)))
            return (res.rowcount or 0) > 0

    # ---------- Topic configuration API ----------
    def set_topic_config(self, topic: str, config: TopicConfig) -> None:
        with Session(self.engine) as sess, sess.begin():
            _ensure_topic_config(sess, topic)
            sess.execute(
                update(topic_config)
                .where(topic_config.c.topic == topic)
                .values(config=asdict(config))
            )

    def get_topic_config(self, topic: str) -> TopicConfig:
        with Session(self.engine) as sess:
            row = sess.execute(select(topic_config.c.config).where(topic_config.c.topic == topic)).first()
            if row and row[0]:
                try:
                    return TopicConfig(**row[0])
                except Exception:
                    return TopicConfig()
            return TopicConfig()

    def get_all_topic_configs(self) -> Dict[str, TopicConfig]:
        with Session(self.engine) as sess:
            rows = sess.execute(select(topic_config.c.topic, topic_config.c.config)).all()
            out: Dict[str, TopicConfig] = {}
            for r in rows:
                try:
                    out[r.topic] = TopicConfig(**(r.config or {}))
                except Exception:
                    out[r.topic] = TopicConfig()
            return out

    # ---------- Real-time counters ----------
    def get_topic_running(self) -> Dict[str, int]:
        with Session(self.engine) as sess:
            rows = sess.execute(
                select(messages.c.topic, func.count().label("cnt"))
                .where(messages.c.state == "running")
                .group_by(messages.c.topic)
            ).all()
            return {r.topic: int(r.cnt or 0) for r in rows}
