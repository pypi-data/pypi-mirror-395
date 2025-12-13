import json
import time
from typing import Any, Literal

from .config import config
from .doc_store import DocStore as DocStoreMongo, TaskEntity
from .interface import Task, TaskInput
from .redis_stream import RedisStreamConsumer, RedisStreamProducer


class DocStoreRedis(DocStoreMongo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.producer = RedisStreamProducer()
        self.consumer_group = config.redis.consumer_group
        self.consumer_pool = {}

    def impersonate(self, username: str) -> "DocStoreRedis":
        """Impersonate another user for this DocStore instance."""
        # use __new__ to bypass __init__
        new_store = super().impersonate(username)
        assert isinstance(new_store, DocStoreRedis)
        new_store.producer = self.producer
        new_store.consumer_group = self.consumer_group
        new_store.consumer_pool = self.consumer_pool
        return new_store

    def _get_or_create_consumer(self, stream: str) -> RedisStreamConsumer:
        key = f"{stream}:{self.consumer_group}"
        if key not in self.consumer_pool:
            self.consumer_pool[key] = RedisStreamConsumer(None, stream, self.consumer_group, create_group=True)
        return self.consumer_pool[key]

    # TODO: priority
    def insert_task(self, target_id: str, task_input: TaskInput) -> Task:
        """Insert a new task into the database."""
        self._check_writable()
        if not target_id:
            raise ValueError("target_id must be provided.")
        if not isinstance(task_input, TaskInput):
            raise ValueError("task_input must be a TaskInput instance.")
        command = task_input.command
        if not command:
            raise ValueError("command must be a non-empty string.")
        args = task_input.args or {}
        if any(not isinstance(k, str) for k in args.keys()):
            raise ValueError("All keys in args must be strings.")

        if command.startswith("ddp."):
            # command is a handler path.
            command, args["path"] = "handler", command

        task_entity = {
            "target": target_id,
            "command": command,
            "args": json.dumps(args),
            "create_user": self.username,
        }

        result = self.producer.add(command, fields=task_entity)
        return Task(
            id=result,
            rid=0,
            status="new",
            target=task_entity["target"],
            command=task_entity["command"],
            args=args,
            create_user=task_entity["create_user"],
        )

    def grab_new_tasks(
        self,
        command: str,
        args: dict[str, Any] = {},
        create_user: str | None = None,
        num=10,
        hold_sec=3600,
        max_retries=10,
    ) -> list[Task]:
        consumer = self._get_or_create_consumer(command)
        messages = consumer.read_or_claim(num, min_idle_ms=hold_sec * 1000)

        tasks = []
        for message in messages:
            task_entity = message.fields
            task = Task(
                id=message.id,
                rid=0,
                status="new",
                target=task_entity["target"],
                command=task_entity["command"],
                args=json.loads(task_entity["args"]),
                create_user=task_entity["create_user"],
                grab_time=int(time.time() * 1000),  # 确保非 0，便于 update 校验
            )
            tasks.append(task)
        return tasks

    def update_task(
        self,
        task_id: str,
        grab_time: int,
        command: str,
        status: Literal["done", "error", "skipped"],
        error_message: str | None = None,
        task: Task | None = None,
    ):
        """Update a task after processing."""
        self._check_writable()
        if not command:
            raise ValueError("command must be provided.")
        if not task_id:
            raise ValueError("task ID must be provided.")
        if not grab_time:
            raise ValueError("grab_time must be provided.")
        if status not in ("done", "error", "skipped"):
            raise ValueError("status must be one of 'done', 'error', or 'skipped'.")
        if status == "error" and not error_message:
            raise ValueError("error_message must be provided if status is 'error'.")

        if status == "error":
            if not task:
                raise ValueError("task must be provided if status is 'error'.")
            task_entity = TaskEntity(
                target=task.target,
                command=task.command,
                args=task.args,
                status="error",
                create_user=task.create_user,
                update_user=None,
                grab_user=task.grab_user,
                grab_time=grab_time,
                error_message=error_message,
            )
            result = self._insert_elem(Task, task_entity)
            assert result is not None, "Task insertion failed, should not happen."

        consumer = self._get_or_create_consumer(command)
        consumer.ack([task_id])
