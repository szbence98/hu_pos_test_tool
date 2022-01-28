import datetime
from os import path, remove
import json
import boto3
from flask import current_app as app, Response
import requests


def auth_header(req):
    header = request_headers
    bearer = req.headers.get("Authorization")
    header["Authorization"] = bearer
    return header


request_headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer"
}


def get_order_list():
    s3 = get_s3_resource()
    direct_order_list = s3.Object("pos-test-tool", app.config["API_ROUTES"]["ORDER_PATH"])
    data = direct_order_list.get()["Body"].read()
    return json.loads(data)


def save_order(req):
    request = req.get_json(force=True)
    now = datetime.datetime.now()
    integration = req.args.get("integration")
    now_timestamp = datetime.datetime.timestamp(now)
    s3 = get_s3_resource()
    order_list = s3.Object("pos-test-tool", app.config["API_ROUTES"]["ORDER_PATH"])
    data = order_list.get()["Body"].read()
    direct_orders = json.loads(data)

    new_order = {
        "order_id": request.get("order_id"),
        "client_name":  request.get("client")["name"],
        "order_code": request.get("order_code"),
        "external_order_id": request.get("external_order_id"),
        "created_at": now_timestamp,
        "integration_type": integration_type(integration),
    }
    direct_orders["orders"].append(new_order)
    order_list.put(Body=json.dumps(direct_orders))
    return "Order processed"


def clear_orders():
    s3 = get_s3_resource()
    order_list = s3.Object("pos-test-tool", app.config["API_ROUTES"]["ORDER_PATH"])
    data = order_list.get()["Body"].read()
    direct_orders = json.loads(data)
    direct_orders["orders"] = []
    order_list.put(Body=json.dumps(direct_orders))
    return "Orders cleared"


def get_s3_resource():
    return boto3.resource(
        "s3",
        region_name=app.config["S3"]["REGION"],
        aws_access_key_id=app.config["S3"]["ACCESS_KEY_ID"],
        aws_secret_access_key=app.config["S3"]["SECRET_ACCESS_KEY"]
    )


def integration_type(int_type):
    if int_type == "direct":
        return "VENDOR_INTEGRATION_TYPE_POS_DIRECT_INTEGRATED"
    return "VENDOR_INTEGRATION_TYPE_POS_INDIRECT_INTEGRATED"


def get_order(req):
    selected_api = next((api for api in app.config["API_ROUTES"]["API"] if api["name"] == req.args.get("api")), None)
    if req.args.get("test") == "true":
        sample_url = selected_api["GET_TEST"]
    else:
        sample_url = selected_api["GET"]

    url = sample_url.replace("{order_id}", req.args.get("order_id"))
    response = requests.get(url, headers=auth_header(req))
    return Response(response.text, status=response.status_code)


def update_order(req):
    selected_api = next((api for api in app.config["API_ROUTES"]["API"] if api["name"] == req.args.get("api")), None)
    if req.args.get("test") == "true":
        sample_url = selected_api["PUT_TEST"]
    else:
        sample_url = selected_api["PUT"]
    url = sample_url.replace("{order_id}", req.args.get("order_id"))
    response = requests.put(url=url, data=req.data, headers=auth_header(req))
    return Response(response.text, status=response.status_code)


def get_profiles():
    s3 = get_s3_resource()
    profiles = s3.Object("pos-test-tool", app.config["API_ROUTES"]["PROFILE_PATH"])
    data = profiles.get()["Body"].read()
    return data


def put_profile(req):
    """if any(p["name"] == request.get("name") for p in profiles):
           return Response("Item already exists.", 400)"""
    request = req.get_json(force=True)
    s3 = get_s3_resource()
    order_list = s3.Object("pos-test-tool", app.config["API_ROUTES"]["PROFILE_PATH"])
    data = order_list.get()["Body"].read()
    profiles = json.loads(data)

    filtered_profiles = list(filter(lambda p: p["name"] == request.get("name"), profiles))
    if filtered_profiles:
        filtered_profiles[0]["name"] = request.get("name")
        filtered_profiles[0]["token"] = request.get("token")
        filtered_profiles[0]["api"] = request.get("api")
        filtered_profiles[0]["test"] = request.get("test")
    else:
        new_profile = {
            "name": request.get("name"),
            "token": request.get("token"),
            "api": request.get("api"),
            "test": request.get("test")
        }
        profiles.append(new_profile)

    order_list.put(Body=json.dumps(profiles))
    return json.dumps(profiles)


def delete_profile(req):
    request = req.get_json(force=True)
    s3 = get_s3_resource()
    order_list = s3.Object("pos-test-tool", app.config["API_ROUTES"]["PROFILE_PATH"])
    data = order_list.get()["Body"].read()
    profiles = json.loads(data)

    new_profiles = [p for p in profiles if p["name"] != request.get("name")]

    order_list.put(Body=json.dumps(new_profiles))
    return json.dumps(new_profiles)
