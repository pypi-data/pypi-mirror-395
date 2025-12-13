import asyncio
import aio_pika
import json

from cattle_grid.app import app_globals


async def publish_reporting(routing_key, data):
    connection = await aio_pika.connect_robust(app_globals.application_config.amqp_url)

    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            "reporting", aio_pika.ExchangeType.TOPIC
        )

        await exchange.publish(
            aio_pika.Message(body=json.dumps(data).encode()),
            routing_key=routing_key,
        )


def before_step(context, step):
    data = {"name": step.name, "type": step.step_type}
    asyncio.get_event_loop().run_until_complete(publish_reporting("step", data))
