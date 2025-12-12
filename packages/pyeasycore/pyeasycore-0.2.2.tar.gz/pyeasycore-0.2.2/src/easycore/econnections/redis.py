# -*- coding: utf-8 -*-
from redis.asyncio import ConnectionPool, Redis

from ..abstractions import SingletonMeta


class RedisClient(metaclass=SingletonMeta):
    def __init__(self, redis_url: str, max_conns: int = 20) -> None:
        self.client = self._new_client(redis_url, max_conns)

    def _new_client(self, redis_url: str, max_conns: int) -> Redis:
        """
        Create a new Redis client.
        redis_url example: "redis://[:password]@host:port/db_number"
                            "redis://user:password@host:port/db_number"
        Args:
            redis_url (str): Redis connection URL.
            max_conns (int): Maximum number of connections in the pool.
        Returns:
            Redis: An instance of Redis client.
        """
        pool = ConnectionPool.from_url(
            url=redis_url,
            max_connections=max_conns,
            encoding="utf-8",
            decode_responses=True,
        )
        client = Redis(connection_pool=pool)
        return client
