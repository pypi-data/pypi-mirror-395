import asyncio
import logging

from .agent import patch_aiohttp_ssl, server
from .config import config


async def run_worker() -> None:
    """Start the LiveKit agent worker."""
    config.validate()

    if config.DISABLE_SSL_VERIFY:
        patch_aiohttp_ssl()

    server.update_options(
        api_key=config.LIVEKIT_API_KEY,
        api_secret=config.LIVEKIT_API_SECRET,
        ws_url=config.LIVEKIT_URL,
    )

    await server.run()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    asyncio.run(run_worker())


__all__ = ["run_worker", "main"]
