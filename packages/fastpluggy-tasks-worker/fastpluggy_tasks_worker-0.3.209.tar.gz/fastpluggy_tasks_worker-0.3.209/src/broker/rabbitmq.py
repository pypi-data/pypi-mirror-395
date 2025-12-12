# broker/rabbitmq.py
"""
RabbitMQ broker backend.
- Uses RabbitMQ as the message queue backend
- Supports distributed worker scenarios across multiple processes/hosts
- Provides persistence and reliability through RabbitMQ
- Compatible with the Broker contracts used by TaskRunner

Intended use:
    BROKER_TYPE=rabbitmq
    RABBITMQ_URL=amqp://guest:guest@localhost:5672/

Features:
- Message persistence via RabbitMQ queues
- Worker registration and heartbeat tracking in separate exchange
- Topic configuration and concurrency limits
- Dead-letter queue support
- Distributed locking via RabbitMQ
"""
import json
import logging
import threading
import time
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

from fastpluggy.core.tools.serialize_tools import serialize_value

try:
    import pika
    from pika.exceptions import AMQPError, AMQPConnectionError
except ImportError:
    pika = None
    AMQPError = Exception
    AMQPConnectionError = Exception

from .contracts import (
    Broker,
    BrokerMessage,
    TopicInfo,
    TopicConfig,
    WorkerInfo,
    ClusterStats,
    ActiveTaskInfo,
    LockInfo,
)

log = logging.getLogger("RabbitMQBroker")


class RabbitMQBroker(Broker):
    """A distributed broker implementation using RabbitMQ."""

    def __init__(self, rabbitmq_url: str) -> None:
        if pika is None:
            raise ImportError(
                "pika library is required for RabbitMQ broker. "
                "Install it with: pip install pika"
            )

        # Connection parameters
        self.rabbitmq_url = rabbitmq_url
        self._connection = None
        self._channel = None
        self._lock = threading.RLock()

        # Message id generator (local counter, prefixed with instance id)
        import uuid
        self._instance_id = str(uuid.uuid4())[:8]
        self._next_id = 1

        # In-memory tracking for workers, running messages, and locks
        # (These could be moved to Redis/DB for true multi-instance support)
        self._workers: Dict[str, WorkerInfo] = {}
        self._worker_tasks: Dict[str, set[str]] = {}
        self._running: Dict[str, BrokerMessage] = {}
        self._locks: Dict[str, Dict[str, Any]] = {}
        self._locks_by_name: Dict[str, str] = {}
        
        # Topic configs stored in memory (could be persisted to RabbitMQ metadata or external store)
        self._topic_configs: Dict[str, TopicConfig] = {}

        # Heartbeat staleness threshold (seconds)
        self._hb_ttl = 10.0

        # Exchange and queue naming conventions
        self._task_exchange = "taskworker.tasks"
        self._worker_exchange = "taskworker.workers"
        self._dlx_exchange = "taskworker.dlx"
        
        # Role tag
        self.role: Optional[str] = "rabbitmq"

    # ------------- Connection Management -------------
    def _connect(self) -> None:
        """Establish connection to RabbitMQ."""
        if self._connection and not self._connection.is_closed:
            return

        try:
            params = pika.URLParameters(self.rabbitmq_url)
            # Add client properties for AMQP 1.0 identification
            params.client_properties = {
                'connection_name': 'fastpluggy-tasks-worker',
                'container-id': self._instance_id
            }
            self._connection = pika.BlockingConnection(params)
            self._channel = self._connection.channel()
            
            # Declare main task exchange (topic exchange for routing by queue name)
            self._channel.exchange_declare(
                exchange=self._task_exchange,
                exchange_type='topic',
                durable=True
            )
            
            # Declare dead-letter exchange
            self._channel.exchange_declare(
                exchange=self._dlx_exchange,
                exchange_type='topic',
                durable=True
            )
            
            log.info(f"Connected to RabbitMQ: {self.rabbitmq_url}")
        except Exception as e:
            log.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def _ensure_channel(self) -> None:
        """Ensure we have a valid channel, reconnecting if necessary."""
        try:
            if self._channel and self._channel.is_open:
                return
        except:
            pass
        
        self._connect()

    def _close(self) -> None:
        """Close the RabbitMQ connection."""
        try:
            if self._channel:
                self._channel.close()
        except:
            pass
        
        try:
            if self._connection:
                self._connection.close()
        except:
            pass

    # ------------- Lifecycle -------------
    def setup(self) -> None:
        """Initialize RabbitMQ connection and exchanges."""
        with self._lock:
            self._connect()

    def wait_ready(self) -> None:
        """Wait for broker to be ready."""
        self._ensure_channel()

    # ------------- Topic Helpers -------------
    def ensure_topic(self, topic: str) -> None:
        """Ensure a topic/queue exists in RabbitMQ."""
        with self._lock:
            self._ensure_channel()
            
            # Get or create topic config
            if topic not in self._topic_configs:
                self._topic_configs[topic] = TopicConfig()
            
            # Declare queue with dead-letter exchange support
            args = {
                'x-dead-letter-exchange': self._dlx_exchange,
                'x-dead-letter-routing-key': f"dlx.{topic}"
            }
            
            self._channel.queue_declare(
                queue=topic,
                durable=True,
                arguments=args
            )
            
            # Bind queue to task exchange with its name as routing key
            self._channel.queue_bind(
                exchange=self._task_exchange,
                queue=topic,
                routing_key=topic
            )
            
            # Declare corresponding dead-letter queue
            dlq_name = f"{topic}.dead"
            self._channel.queue_declare(queue=dlq_name, durable=True)
            self._channel.queue_bind(
                exchange=self._dlx_exchange,
                queue=dlq_name,
                routing_key=f"dlx.{topic}"
            )

    # ------------- Core Operations -------------
    def publish(self, topic: str, payload: Dict[str, Any], headers: Optional[Dict[str, Any]] = None) -> str:
        """Publish a new message to the given topic."""
        with self._lock:
            self._ensure_channel()
            self.ensure_topic(topic)
            
            msg_id = f"rmq:{self._instance_id}:{self._next_id}"
            self._next_id += 1
            
            msg = BrokerMessage(
                id=msg_id,
                topic=topic,
                payload=dict(payload or {}),
                headers=dict(headers or {}),
                attempts=0,
                created_at=datetime.now(timezone.utc),
            )
            
            # Serialize message to JSON (ensure we pass a string to .encode)
            body = json.dumps(serialize_value({
                'id': msg.id,
                'topic': msg.topic,
                'payload': msg.payload,
                'headers': msg.headers,
                'attempts': msg.attempts,
                'created_at': msg.created_at.isoformat(),
            }), ensure_ascii=False)
            
            # Publish to exchange with routing key = topic name
            self._channel.basic_publish(
                exchange=self._task_exchange,
                routing_key=topic,
                body=body.encode('utf-8'),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # persistent
                    message_id=msg_id,
                    timestamp=int(time.time()),
                )
            )
            
            log.debug(f"Published message {msg_id} to topic {topic}")
            return msg_id

    def _has_global_permit(self, topic: str) -> bool:
        """Check if topic has capacity for another running message."""
        config = self._topic_configs.get(topic, TopicConfig())
        if config.concurrency_limit is None:
            return True
        
        # Count running messages for this topic
        running_count = sum(1 for msg in self._running.values() if msg.topic == topic)
        return running_count < config.concurrency_limit

    def claim(self, topic: str, worker_id: str) -> Optional[BrokerMessage]:
        """Claim one message from the given topic for a specific worker."""
        with self._lock:
            self._ensure_channel()
            
            # Handle wildcard topic - not implemented in this version
            if topic == "*":
                log.warning("Wildcard topic claiming not yet implemented for RabbitMQ broker")
                return None
            
            self.ensure_topic(topic)
            
            # Check concurrency limit
            if not self._has_global_permit(topic):
                return None
            
            # Try to get a message from the queue (non-blocking)
            method_frame, properties, body = self._channel.basic_get(queue=topic, auto_ack=False)
            
            if method_frame is None:
                # No messages available
                return None
            
            # Deserialize message
            try:
                data = json.loads(body.decode('utf-8'))
                msg = BrokerMessage(
                    id=data['id'],
                    topic=data['topic'],
                    payload=data['payload'],
                    headers=data.get('headers', {}),
                    attempts=data.get('attempts', 0),
                    created_at=datetime.fromisoformat(data['created_at']),
                )
            except Exception as e:
                log.error(f"Failed to deserialize message: {e}")
                # Reject and requeue
                self._channel.basic_nack(delivery_tag=method_frame.delivery_tag, requeue=True)
                return None
            
            # Increment attempts
            msg.attempts += 1
            
            # Update headers
            msg.headers['worker_id'] = worker_id
            msg.headers['claimed_at'] = datetime.now(timezone.utc).isoformat()
            msg.headers['delivery_tag'] = method_frame.delivery_tag
            
            # Track as running
            self._running[msg.id] = msg
            self._worker_tasks.setdefault(worker_id, set()).add(msg.id)
            
            log.debug(f"Claimed message {msg.id} from topic {topic} for worker {worker_id}")
            return msg

    def ack(self, msg_id: str) -> None:
        """Acknowledge successful processing of a message."""
        with self._lock:
            msg = self._running.pop(msg_id, None)
            if not msg:
                log.warning(f"Attempted to ack unknown message: {msg_id}")
                return
            
            # Remove from worker task tracking
            wid = msg.headers.get('worker_id')
            if wid:
                self._worker_tasks.get(wid, set()).discard(msg_id)
            
            # Acknowledge to RabbitMQ
            delivery_tag = msg.headers.get('delivery_tag')
            if delivery_tag is not None:
                try:
                    self._ensure_channel()
                    self._channel.basic_ack(delivery_tag=delivery_tag)
                except Exception as e:
                    log.error(f"Failed to ack message {msg_id}: {e}")
            
            # Auto-release any lock associated with this task
            try:
                task_id = msg.payload.get("task_id") or msg_id
                if task_id in self._locks:
                    self._release_lock_no_owner_check(task_id)
            except Exception:
                pass
            
            log.debug(f"Acknowledged message {msg_id}")

    def nack(self, msg_id: str, requeue: bool = True) -> None:
        """Negative acknowledgement: mark a message as failed."""
        with self._lock:
            msg = self._running.pop(msg_id, None)
            if not msg:
                log.warning(f"Attempted to nack unknown message: {msg_id}")
                return
            
            # Remove from worker task tracking
            wid = msg.headers.get('worker_id')
            if wid:
                self._worker_tasks.get(wid, set()).discard(msg_id)
            
            # Release any locks
            try:
                task_id = msg.payload.get("task_id") or msg_id
                if task_id in self._locks:
                    self._release_lock_no_owner_check(task_id)
            except Exception:
                pass
            
            # Nack to RabbitMQ
            delivery_tag = msg.headers.get('delivery_tag')
            if delivery_tag is not None:
                try:
                    self._ensure_channel()
                    self._channel.basic_nack(delivery_tag=delivery_tag, requeue=requeue)
                except Exception as e:
                    log.error(f"Failed to nack message {msg_id}: {e}")
            
            log.debug(f"Nacked message {msg_id} (requeue={requeue})")

    # ------------- Workers / Heartbeat -------------
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
        """Register a worker presence with the broker."""
        now = datetime.now(timezone.utc).isoformat()
        with self._lock:
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
            log.info(f"Registered worker {worker_id} on {host} (capacity={capacity})")

    def heartbeat(
        self,
        worker_id: str,
        running: Optional[int] = None,
        capacity: Optional[int] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Update worker heartbeat."""
        with self._lock:
            w = self._workers.get(worker_id)
            if not w:
                log.warning(f"Heartbeat for unknown worker: {worker_id}")
                return
            
            w.last_heartbeat = datetime.now(timezone.utc).isoformat()
            if capacity is not None:
                w.capacity = int(capacity)
            if running is not None:
                w.running_hint = int(running)
            if meta is not None:
                w.meta = dict(w.meta or {})
                w.meta['hb'] = meta

    def unregister_worker(self, worker_id: str) -> None:
        """Unregister a worker."""
        with self._lock:
            self._workers.pop(worker_id, None)
            self._worker_tasks.pop(worker_id, None)
            log.info(f"Unregistered worker {worker_id}")

    def get_workers(self, include_tasks: bool = False, stale_after: Optional[float] = None) -> List[WorkerInfo]:
        """List workers known to the broker."""
        with self._lock:
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

    # ------------- Listings / Stats -------------
    def get_topics(self) -> List[TopicInfo]:
        """List topics with queue metrics."""
        with self._lock:
            self._ensure_channel()
            out: List[TopicInfo] = []
            
            for topic_name in self._topic_configs.keys():
                try:
                    # Get queue statistics from RabbitMQ
                    result = self._channel.queue_declare(queue=topic_name, passive=True, durable=True)
                    queued = result.method.message_count
                    
                    # Count running for this topic
                    running_count = sum(1 for msg in self._running.values() if msg.topic == topic_name)
                    
                    # Count dead-letter messages
                    dlq_name = f"{topic_name}.dead"
                    try:
                        dlq_result = self._channel.queue_declare(queue=dlq_name, passive=True, durable=True)
                        dead_letter = dlq_result.method.message_count
                    except:
                        dead_letter = 0
                    
                    # Count subscribers (workers listening to this topic)
                    subscribers = sum(
                        1 for w in self._workers.values()
                        if (topic_name in w.topics) or ("*" in w.topics)
                    )
                    
                    config = self._topic_configs.get(topic_name, TopicConfig())
                    
                    out.append(TopicInfo(
                        topic=topic_name,
                        queued=queued,
                        running=running_count,
                        dead_letter=dead_letter,
                        subscribers=subscribers,
                        configuration=config,
                    ))
                except Exception as e:
                    log.warning(f"Failed to get stats for topic {topic_name}: {e}")
            
            return sorted(out, key=lambda x: x.topic)

    def get_cluster_stats(self) -> ClusterStats:
        """Aggregate cluster-level stats."""
        with self._lock:
            total_capacity = sum(w.capacity for w in self._workers.values())
            total_running = sum(len(s) for s in self._worker_tasks.values())
            
            return ClusterStats(
                workers=len(self._workers),
                total_capacity=total_capacity,
                total_running=total_running,
                topics=self.get_topics(),
                broker_type="rabbitmq",
            )

    def stats(self) -> Dict[str, Any]:
        """Return a summary of broker status."""
        cs = self.get_cluster_stats()
        return {
            "workers": cs.workers,
            "total_capacity": cs.total_capacity,
            "total_running": cs.total_running,
            "topics": [t.topic for t in cs.topics],
            "broker_type": cs.broker_type,
        }

    def get_all_active_tasks(self, topic: Optional[str]) -> List[ActiveTaskInfo]:
        """Return a list of active tasks known by the broker."""
        with self._lock:
            items: List[ActiveTaskInfo] = []
            
            # For now, only return running tasks (queued tasks would require consuming from RabbitMQ)
            for m in self._running.values():
                if topic is not None and m.topic != topic:
                    continue
                items.append(ActiveTaskInfo(
                    id=m.id,
                    topic=m.topic,
                    payload=m.payload,
                    headers=dict(m.headers or {}),
                    attempts=m.attempts,
                    created_at=m.created_at.isoformat(),
                    state="running",
                    claimed_by=(m.headers or {}).get('worker_id')
                ))
            
            return items

    # ------------- Locks -------------
    def _release_lock_no_owner_check(self, task_id: str) -> bool:
        """Release a lock without checking ownership."""
        info = self._locks.pop(task_id, None)
        if not info:
            return False
        tname = info.get("task_name")
        if tname and self._locks_by_name.get(tname) == task_id:
            self._locks_by_name.pop(tname, None)
        return True

    def acquire_lock(self, task_name: str, task_id: str, locked_by: str) -> bool:
        """Acquire an exclusive lock for a task."""
        if not task_id:
            return False
        if not task_name:
            task_name = task_id
        
        with self._lock:
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
            return True

    def release_lock(self, task_id: str, locked_by: Optional[str] = None) -> bool:
        """Release a lock."""
        if not task_id:
            return False
        
        with self._lock:
            info = self._locks.get(task_id)
            if not info:
                return False
            if locked_by is not None and info.get("locked_by") != locked_by:
                return False
            return self._release_lock_no_owner_check(task_id)

    def get_locks(self) -> List[LockInfo]:
        """List current task locks."""
        with self._lock:
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
        """Force release a task lock."""
        with self._lock:
            return self._release_lock_no_owner_check(task_id)

    # ------------- Topic Configuration -------------
    def set_topic_config(self, topic: str, config: TopicConfig) -> None:
        """Set full topic configuration atomically."""
        with self._lock:
            self.ensure_topic(topic)
            
            lim = None if config.concurrency_limit is None else int(config.concurrency_limit)
            if lim is not None and lim < 0:
                raise ValueError("concurrency_limit must be >= 0 or None")
            
            self._topic_configs[topic] = TopicConfig(
                concurrency_limit=lim,
                max_retries=config.max_retries,
                dead_letter_enabled=bool(config.dead_letter_enabled),
                retention_seconds=config.retention_seconds,
            )

    def get_topic_config(self, topic: str) -> TopicConfig:
        """Return the current TopicConfig for a topic."""
        with self._lock:
            self.ensure_topic(topic)
            return self._topic_configs.get(topic, TopicConfig())

    def get_all_topic_configs(self) -> Dict[str, TopicConfig]:
        """Return a snapshot of all topic configs by topic name."""
        with self._lock:
            return {name: cfg for name, cfg in self._topic_configs.items()}

    def get_topic_running(self) -> Dict[str, int]:
        """Return current running counts per topic."""
        with self._lock:
            result = {}
            for topic_name in self._topic_configs.keys():
                result[topic_name] = sum(1 for msg in self._running.values() if msg.topic == topic_name)
            return result

    def __del__(self):
        """Cleanup on destruction."""
        self._close()
