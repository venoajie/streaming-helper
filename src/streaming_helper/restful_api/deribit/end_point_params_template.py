# -*- coding: utf-8 -*-

# user defined formula
from streaming_helper.utilities import time_modification as time_mod


def get_currencies_end_point() -> str:
    return f"public/get_currencies?"


def get_server_time_end_point() -> str:
    return f"public/get_time?"


def get_instruments_end_point(currency) -> str:
    return f"public/get_instruments?currency={currency.upper()}"


def basic_https() -> str:
    return f"https://deribit.com/api/v2/public"


def get_tickers_end_point(instrument_name: str) -> str:
    return f"{basic_https()}/ticker?instrument_name={instrument_name}"


def get_tradingview_chart_data_end_point() -> str:
    return f"{basic_https()}/get_tradingview_chart_data?"


def get_ohlc_end_point(
    endpoint_tradingview: str,
    instrument_name: str,
    resolution: int,
    qty_or_start_time_stamp: int,
    provided_end_timestamp: int = None,
    qty_as_start_time_stamp: bool = False,
) -> str:

    now_unix = time_mod.get_now_unix_time()

    # start timestamp is provided
    start_timestamp = qty_or_start_time_stamp

    # recalculate start timestamp using qty as basis point
    if qty_as_start_time_stamp:
        start_timestamp = now_unix - (60000 * resolution) * qty_as_start_time_stamp

    if provided_end_timestamp:
        end_timestamp = provided_end_timestamp
    else:
        end_timestamp = now_unix

    return f"{endpoint_tradingview}end_timestamp={end_timestamp}&instrument_name={instrument_name}&resolution={resolution}&start_timestamp={start_timestamp}"


def get_json_payload(
    endpoint: str,
    params: dict,
) -> dict:

    id = id_numbering(
        endpoint,
        endpoint,
    )

    return {
        "jsonrpc": "2.0",
        "id": id,
        "method": f"{endpoint}",
        "params": params,
    }


def get_open_orders_end_point() -> str:
    return f"private/get_open_orders"


def get_open_orders_params(
    kind: str,
    type: str,
) -> dict:
    return {
        "kind": kind,
        "type": type,
    }


def get_subaccounts_end_point() -> str:
    return f"private/get_subaccounts"


def get_subaccounts_params(
    with_portfolio: bool = True,
) -> dict:
    return {
        "with_portfolio": with_portfolio,
    }


def get_subaccounts_details_end_point() -> str:
    return f"private/get_subaccounts_details"


def get_subaccounts_details_params(
    currency: str,
    with_open_orders: bool = True,
) -> dict:
    return {
        "currency": currency,
        "with_open_orders": with_open_orders,
    }


def get_user_trades_by_currency_end_point() -> str:
    return f"private/get_user_trades_by_currency"


def get_user_trades_by_currency_params(
    currency: str,
    kind: str = "any",
    count: int = 1000,
) -> dict:
    return {
        "currency": currency,
        "kind": kind,
        "count": count,
    }


def get_user_trades_by_instrument_and_time_end_point() -> str:
    return f"private/get_user_trades_by_instrument_and_time"


def get_user_trades_by_instrument_and_time_params(
    instrument_name: str,
    start_timestamp: int,
    count: int = 1000,
) -> dict:

    now_unix = time_mod.get_now_unix_time()

    return {
        "count": count,
        "end_timestamp": end_timestamp,
        "instrument_name": instrument_name,
        "start_timestamp": start_timestamp,
    }


def get_transaction_log_end_point() -> str:
    return f"private/get_transaction_log"


def get_transaction_log_params(
    currency: str,
    start_timestamp: int,
    count: int = 1000,
    query: str = "trade",
) -> dict:

    now_unix = time_mod.get_now_unix_time()

    return {
        "count": count,
        "currency": currency,
        "end_timestamp": end_timestamp,
        "query": query,
        "start_timestamp": start_timestamp,
    }


def send_orders_end_point(side: str) -> str:

    if side == "buy" or side == "sell":
        return f"private/{side}"


def send_orders_params(
    side: str,
    instrument,
    amount,
    label: str = None,
    price: float = None,
    type: str = "limit",
    otoco_config: list = None,
    linked_order_type: str = None,
    trigger_price: float = None,
    trigger: str = "last_price",
    time_in_force: str = "fill_or_kill",
    reduce_only: bool = False,
    post_only: bool = True,
    reject_post_only: bool = False,
) -> str:

    params = {}

    params.update({"instrument_name": instrument})
    params.update({"amount": amount})
    params.update({"label": label})
    params.update({"instrument_name": instrument})
    params.update({"type": type})

    if trigger_price is not None:

        params.update({"trigger": trigger})
        params.update({"trigger_price": trigger_price})
        params.update({"reduce_only": reduce_only})

    if "market" not in type:
        params.update({"price": price})
        params.update({"post_only": post_only})
        params.update({"reject_post_only": reject_post_only})

    if otoco_config:
        params.update({"otoco_config": otoco_config})

        if linked_order_type is not None:
            params.update({"linked_order_type": linked_order_type})
        else:
            params.update({"linked_order_type": "one_triggers_other"})

        params.update({"trigger_fill_condition": "incremental"})

    return params


def send_limit_order_params(
    params: dict,
) -> str:
    """ """

    # basic params
    side = params["side"]
    instrument = params["instrument_name"]
    label_numbered = params["label"]
    size = params["size"]
    type = params["type"]
    limit_prc = params["entry_price"]

    try:
        otoco_config = params["otoco_config"]
    except:
        otoco_config = None

    try:
        linked_order_type = params["linked_order_type"]

    except:
        linked_order_type = None

    order_result = None

    if side != None:

        if type == "limit":  # limit has various state

            order_result = send_orders_params(
                side,
                instrument,
                size,
                label_numbered,
                limit_prc,
                type,
                otoco_config,
            )

        else:

            trigger_price = params["trigger_price"]
            trigger = params["trigger"]

            order_result = send_orders_params(
                side,
                instrument,
                size,
                label_numbered,
                limit_prc,
                type,
                otoco_config,
                linked_order_type,
                trigger_price,
                trigger,
            )

    return order_result


def cancel_all_orders() -> str:
    return f"cancel_all"


def cancel_order() -> str:
    return f"cancel"


def get_cancel_order_params(
    detailed: False,
) -> dict:

    now_unix = time_mod.get_now_unix_time()

    return {
        "detailed": detailed,
    }


def get_api_end_point(
    endpoint: str,
    parameters: dict = None,
) -> dict:
    """
    used in data receiver deribit

    """

    private_endpoint = f"private/{endpoint}"

    params = {}
    params.update({"jsonrpc": "2.0"})
    params.update({"method": private_endpoint})
    if endpoint == "get_subaccounts":
        params.update({"params": {"with_portfolio": True}})

    if endpoint == "get_open_orders":
        end_point_params = dict(kind=parameters["kind"], type=parameters["type"])

        params.update({"params": end_point_params})

    return params


def id_numbering(
    operation: str,
    ws_channel: str,
) -> str:
    """

    id convention

    method
    subscription    3
    get             4

    auth
    public	        1
    private	        2

    instruments
    all             0
    btc             1
    eth             2

    subscription
    --------------  method      auth    seq    inst
    portfolio	        3	    1	    01
    user_order	        3	    1	    02
    my_trade	        3	    1	    03
    order_book	        3	    2	    04
    trade	            3	    1	    05
    index	            3	    1	    06
    announcement	    3	    1	    07

    get
    --------------
    currencies	        4	    2	    01
    instruments	        4	    2	    02
    positions	        4	    1	    03

    """
    id_auth = 1
    if "user" in ws_channel:
        id_auth = 9

    id_method = 0
    if "subscribe" in operation:
        id_method = 3
    if "get" in operation:
        id_method = 4
    id_item = 0
    if "book" in ws_channel:
        id_item = 1
    if "user" in ws_channel:
        id_item = 2
    if "chart" in ws_channel:
        id_item = 3
    if "index" in ws_channel:
        id_item = 4
    if "order" in ws_channel:
        id_item = 5
    if "position" in ws_channel:
        id_item = 6
    id_instrument = 0
    if "BTC" or "btc" in ws_channel:
        id_instrument = 1
    if "ETH" or "eth" in ws_channel:
        id_instrument = 2
    return int(f"{id_auth}{id_method}{id_item}{id_instrument}")
