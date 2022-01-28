SECRET_KEY = "secret"
APP_DEBUG = True
S3_ACCESS = {
    "BUCKET": "name",
    "REGION": "region",
    "ACCESS_KEY_ID": "keyid",
    "SECRET_ACCESS_KEY": "secret"
}
API_ROUTES = {
    "API": [
        {"name": "stg",
         "GET": "https://partners-stg.deliveryhero.io/v1/orders/{order_id}",
         "PUT": "https://partners-stg.deliveryhero.io/v1/orders/{order_id}",
         "GET_TEST": "https://partners-stg.deliveryhero.io/v1/test-orders/{order_id}",
         "PUT_TEST": "https://partners-stg.deliveryhero.io/v1/test-orders/{order_id}",
         "docs": "https://partners-stg.deliveryhero.io/redoc/index.html#section/Authentication"
         },
        {"name": "eu",
         "GET": "https://partners-eu.deliveryhero.io/v1/orders/{order_id}",
         "PUT": "https://partners-eu.deliveryhero.io/v1/orders/{order_id}",
         "GET_TEST": "https://partners-eu.deliveryhero.io/v1/test-orders/{order_id}",
         "PUT_TEST": "https://partners-eu.deliveryhero.io/v1/test-orders/{order_id}",
         "docs": "https://partners-eu.deliveryhero.io/redoc/index.html#section/Authentication"
         }
    ],
    "GET_ORDER": "https://partners-eu.deliveryhero.io/v1/test-orders/{order_id}",
    "PUT_ORDER": "https://partners-eu.deliveryhero.io/v1/test-orders/{order_id}",
    "PROFILE_PATH": "test/profiles.json",
    "ORDER_PATH": "test/order_list.json"
}


