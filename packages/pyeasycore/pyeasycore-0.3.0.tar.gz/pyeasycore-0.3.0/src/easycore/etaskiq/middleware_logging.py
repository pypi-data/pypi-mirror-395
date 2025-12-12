# -*- coding: utf-8 -*-
from typing import Any

from taskiq import TaskiqMessage, TaskiqMiddleware, TaskiqResult


class LoggingMiddlewareWorker(TaskiqMiddleware):

    async def pre_execute(self, message: TaskiqMessage) -> TaskiqMessage:
        # logger.info(
        #     f"Preparing to execute task: {message.task_name}",
        #     extra={
        #         "task_id": message.task_id,
        #         "task_args": str(message.args),
        #         "task_kwargs": str(message.kwargs),
        #     },
        # )
        return message

    async def post_execute(
        self, message: TaskiqMessage, result: TaskiqResult[Any]
    ) -> None:
        # Ghi log kết quả sau khi thực thi
        # logger.info(
        #     f"Task {message.task_name} completed with result: {result.return_value}"
        # )
        result.labels["task_name"] = message.task_name
