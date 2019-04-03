import aioredis

async def init_db(loop, config):
    pool = await aioredis.create_redis_pool(
        (config['host'], config['port']),
        minsize=config['minsize'],
        maxsize=config['maxsize'],
        loop=loop
    )
    return pool

async def setup_database(app, config, loop):
    pool = await init_db(loop, config)

    async def close_database(app):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_database)
    app['db_pool'] = pool
    return pool