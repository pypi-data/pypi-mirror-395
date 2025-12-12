# RabbitMQ Broker for Task Worker Plugin

This document describes how to use the RabbitMQ broker implementation for the task worker plugin.

## Overview

The RabbitMQ broker provides a distributed, persistent message queue backend for the task worker system. It's ideal for production deployments where you need:

- **Reliability**: Messages are persisted to disk by RabbitMQ
- **Scalability**: Workers can run on multiple hosts/processes
- **High Availability**: Leverage RabbitMQ clustering features
- **Dead Letter Queues**: Automatic handling of failed messages

## Installation

Install the task worker plugin with RabbitMQ support:

```bash
pip install fastpluggy-tasks-worker[rabbitmq]
```

This installs the `pika` library required for RabbitMQ connectivity.

## Configuration

### Environment Variables

Set the following environment variables to configure RabbitMQ:

```bash
export BROKER_TYPE=rabbitmq
export RABBITMQ_URL=amqp://guest:guest@localhost:5672/
```

### Configuration Settings

In your application settings:

```python
from fastpluggy_plugin.tasks_worker.config import TasksRunnerSettings

settings = TasksRunnerSettings()
settings.BROKER_TYPE = "rabbitmq"
settings.RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
```

### RabbitMQ URL Format

The `RABBITMQ_URL` should follow the AMQP URI format:

```
amqp://username:password@hostname:port/vhost
```

Examples:
- Local development: `amqp://guest:guest@localhost:5672/`
- Production with auth: `amqp://myuser:mypass@rabbitmq.example.com:5672/myvhost`
- Secure connection: `amqps://user:pass@rabbitmq.example.com:5671/`

## Features

### Core Operations

- **publish**: Publish messages to topics (queues)
- **claim**: Claim messages for processing with concurrency control
- **ack**: Acknowledge successful message processing
- **nack**: Reject messages (with requeue or dead-letter options)

### Worker Management

- Worker registration and heartbeat tracking
- Automatic stale worker detection
- Worker capacity management

### Topic Management

- Automatic topic (queue) creation
- Concurrency limits per topic
- Dead-letter queue support for failed messages
- Topic configuration (max retries, retention, etc.)

### Observability

- Real-time worker and topic statistics
- Active task tracking
- Cluster-wide metrics

### Task Locking

- Exclusive locks for tasks (stored in-memory, synced across broker instance)
- Automatic lock release on task completion/failure

## Architecture

### Exchanges and Queues

The RabbitMQ broker creates the following exchanges:

- `taskworker.tasks`: Topic exchange for routing task messages
- `taskworker.dlx`: Dead-letter exchange for failed messages

For each topic (e.g., "default"):
- Queue: `default` - Main task queue
- Queue: `default.dead` - Dead-letter queue for failed tasks

### Message Flow

1. **Publish**: Messages are published to `taskworker.tasks` exchange with routing key = topic name
2. **Queue**: RabbitMQ routes messages to the appropriate queue
3. **Claim**: Workers fetch messages using `basic_get` (non-blocking)
4. **Process**: Worker executes the task
5. **Ack/Nack**: Worker acknowledges or rejects the message
   - **Ack**: Message is removed from queue
   - **Nack (requeue=True)**: Message returns to queue for retry
   - **Nack (requeue=False)**: Message moves to dead-letter queue

## Usage Example

### Starting Workers

```python
from fastpluggy_plugin.tasks_worker import TaskRunner
from fastpluggy_plugin.tasks_worker.broker.factory import get_broker

# Get the RabbitMQ broker
broker = get_broker()  # Reads BROKER_TYPE from settings

# Initialize broker
broker.setup()

# Start worker
runner = TaskRunner(broker=broker, topics=["default"], capacity=4)
runner.run()
```

### Publishing Tasks

```python
from fastpluggy_plugin.tasks_worker.broker.factory import get_broker

broker = get_broker()
broker.setup()

# Publish a task
msg_id = broker.publish(
    topic="default",
    payload={
        "task_name": "my_task",
        "args": [1, 2, 3],
        "kwargs": {"foo": "bar"}
    },
    headers={"priority": "high"}
)

print(f"Published message: {msg_id}")
```

### Monitoring

```python
from fastpluggy_plugin.tasks_worker.broker.factory import get_broker

broker = get_broker()
broker.setup()

# Get cluster stats
stats = broker.get_cluster_stats()
print(f"Workers: {stats.workers}")
print(f"Capacity: {stats.total_capacity}")
print(f"Running: {stats.total_running}")

# Get topic info
topics = broker.get_topics()
for topic in topics:
    print(f"{topic.topic}: {topic.queued} queued, {topic.running} running")

# Get workers
workers = broker.get_workers()
for worker in workers:
    print(f"{worker.worker_id}: {worker.running}/{worker.capacity} tasks")
```

## Limitations

### Current Implementation Notes

1. **Worker State**: Worker registrations and heartbeats are stored in-memory on the broker instance. For true multi-instance broker support, these would need to be moved to a shared store (Redis, database, or RabbitMQ itself).

2. **Task Locks**: Exclusive locks are stored in-memory. For distributed locking across multiple broker instances, consider using Redis or a distributed lock manager.

3. **Wildcard Topics**: The wildcard topic (`*`) claiming is not yet implemented in the RabbitMQ broker.

4. **Active Tasks**: The `get_all_active_tasks` method currently only returns in-flight tasks, not queued tasks (to avoid consuming from RabbitMQ).

### Future Enhancements

- Distributed worker registry using RabbitMQ metadata or external store
- Consumer-based message consumption (instead of polling with basic_get)
- Priority queues support
- Message TTL (time-to-live) configuration
- Wildcard topic support
- Distributed locking with Redis or Consul

## Troubleshooting

### Connection Issues

If you see connection errors:

1. Verify RabbitMQ is running: `sudo systemctl status rabbitmq-server`
2. Check the URL is correct in `RABBITMQ_URL`
3. Verify network connectivity: `telnet rabbitmq-host 5672`
4. Check RabbitMQ logs: `/var/log/rabbitmq/`

### Import Error

If you get `ImportError: pika library is required`:

```bash
pip install pika
# or
pip install fastpluggy-tasks-worker[rabbitmq]
```

### Message Accumulation

If messages are piling up in queues:

1. Check workers are running and healthy
2. Verify concurrency limits are not too restrictive
3. Check for stuck/crashed workers
4. Review dead-letter queue for failed messages

### Performance Issues

For high-throughput scenarios:

1. Increase worker capacity
2. Use multiple worker processes/hosts
3. Tune RabbitMQ configuration (prefetch count, queue settings)
4. Consider using RabbitMQ clustering

## References

- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Pika Documentation](https://pika.readthedocs.io/)
- [AMQP 0-9-1 Protocol](https://www.rabbitmq.com/amqp-0-9-1-reference.html)
