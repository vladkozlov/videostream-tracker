import asyncio
import logging
import pathlib

from aiohttp import web

from routes import setup_routes
from db import setup_database
from views import Handler
from utils import load_config

ROOT_DIR = pathlib.Path(__file__).parent

async def init_app(loop):
    config = load_config(ROOT_DIR / 'config' / 'config.yml')

    app = web.Application()
    db_pool = await setup_database(app, config['redis'], loop)

    handler = Handler(loop, db_pool)

    setup_routes(app, handler, ROOT_DIR)

    host, port = config['host'], config['port']
    return app, host, port

def main():
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()

    app, host, port = loop.run_until_complete(init_app(loop))

    web.run_app(app, host=host, port=port)

if __name__ == '__main__':
    main()