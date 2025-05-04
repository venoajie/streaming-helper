# -*- coding: utf-8 -*-

# built ins
import asyncio

# installed
import orjson

# user defined formula
from streaming_helper.restful_api.telegram import (
    end_point_params_template as end_point_telegram,
)
from streaming_helper.utilities import system_tools


async def telegram_messaging(
    client_redis: object,
    client_id: str,
    client_secret: str,
    redis_channels: list,

) -> None:
    """ """

    try:

        # connecting to redis pubsub
        pubsub: object = client_redis.pubsub()

        error_channel: str = "error"

        # prepare channels placeholders
        channels = [
            error_channel,
        ]

        # subscribe to channels
        [await pubsub.subscribe(o) for o in channels]


        # get redis channels
        order_rest_channel: str = redis_channels["order_rest"]
        my_trade_receiving_channel: str = redis_channels["my_trade_receiving"]
        order_update_channel: str = redis_channels["order_cache_updating"]
        portfolio_channel: str = redis_channels["portfolio"]
        sqlite_updating_channel: str = redis_channels["sqlite_record_updating"]
        sub_account_cached_channel: str = redis_channels["sub_account_cache_updating"]

        while True:

            try:

                message_byte = await pubsub.get_message()

                if message_byte and message_byte["type"] == "message":

                    message_byte_data = orjson.loads(message_byte["data"])

                    message_channel = message_byte["channel"]

                    if error_channel in message_channel:

                        data = message_byte_data["params"]["data"]
                        
                        await end_point_telegram.send_message(
                        client_id,
                            client_secret,
                            data)

                    if my_trade_receiving_channel in message_channel:

                        log.critical(message_channel)
                        log.error(data)

                        for trade in data:
                        instrument_name": trade_result["instrument_name"]})
    trade_to_db.update({"amount": trade_result["amount"]})
    trade_to_db.update({"price": trade_result["price"]})
    trade_to_db.update({"direction": trade_result["direction"]})
    trade_to_db.update({"trade_id": trade_result["trade_id"]})
    trade_to_db.update({"order_id": trade_result["order_id"]})
    trade_to_db.update({"timestamp": trade_result["timestamp"]})


            except Exception as error:

                await system_tools.parse_error_message_with_redis(
                    client_redis,
                    error,
                )

                continue

            finally:
                await asyncio.sleep(0.001)

    except Exception as error:

        await system_tools.parse_error_message_with_redis(
            client_redis,
            error,
        )
