from taskiq import TaskiqScheduler


class MyTaskiqScheduler(TaskiqScheduler):
    async def startup(self) -> None:
        await super().startup()

    async def shutdown(self) -> None:
        await super().shutdown()
