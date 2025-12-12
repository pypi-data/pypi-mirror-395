"""
startup and initialization for production inbox system.

provides lifecycle hooks for:
- redis queue connection
- worker initialization
- graceful shutdown
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from synqed.agent_email.inbox.queue import initialize_queue, shutdown_queue
from synqed.agent_email.inbox.worker import start_workers_for_all_agents, shutdown_workers


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
    redis_url: str = "redis://localhost:6379",
) -> AsyncIterator[None]:
    """
    fastapi lifespan context manager for inbox system.
    
    initializes redis queue and workers on startup,
    gracefully shuts down on exit.
    
    usage:
        from synqed.agent_email.inbox.startup import create_lifespan
        
        app = FastAPI(lifespan=create_lifespan())
    
    args:
        app: fastapi application
        redis_url: redis connection url
    """
    # startup
    logger.info("initializing inbox system...")
    
    try:
        # connect to redis
        await initialize_queue(redis_url=redis_url)
        logger.info("redis queue connected")
        
        # start workers for all registered agents
        await start_workers_for_all_agents(redis_url=redis_url)
        logger.info("workers started")
        
        logger.info("inbox system ready")
        
        yield
    
    finally:
        # shutdown
        logger.info("shutting down inbox system...")
        
        # stop workers
        await shutdown_workers()
        logger.info("workers stopped")
        
        # close redis connection
        await shutdown_queue()
        logger.info("redis queue disconnected")
        
        logger.info("inbox system shutdown complete")


def create_lifespan(redis_url: str = "redis://localhost:6379"):
    """
    create lifespan context manager with custom redis url.
    
    usage:
        app = FastAPI(lifespan=create_lifespan("redis://myhost:6379"))
    
    args:
        redis_url: redis connection url
        
    returns:
        lifespan context manager function
    """
    @asynccontextmanager
    async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
        async with lifespan(app, redis_url=redis_url):
            yield
    
    return _lifespan


async def manual_startup(redis_url: str = "redis://localhost:6379") -> None:
    """
    manually initialize inbox system (without fastapi lifespan).
    
    use this if you need to initialize the system outside of fastapi context.
    
    args:
        redis_url: redis connection url
    """
    logger.info("manually initializing inbox system...")
    await initialize_queue(redis_url=redis_url)
    await start_workers_for_all_agents(redis_url=redis_url)
    logger.info("inbox system initialized")


async def manual_shutdown() -> None:
    """
    manually shutdown inbox system (without fastapi lifespan).
    
    use this if you manually initialized the system.
    """
    logger.info("manually shutting down inbox system...")
    await shutdown_workers()
    await shutdown_queue()
    logger.info("inbox system shutdown complete")

