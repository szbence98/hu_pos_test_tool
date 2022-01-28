from flask import current_app as app, send_from_directory, request
import os
import service


@app.route('/', defaults={'path': ''})
@app.route("/<path:path>")
def serve_static(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory("public", 'index.html')


@app.route("/static/js/<path:path>")
def serve_static_js(path):
    return send_from_directory("public/static/js", path)


@app.route("/static/css/<path:path>")
def serve_static_css(path):
    return send_from_directory("public/static/css", path)


@app.route("/data/<path:path>")
def serve_static_data(path):
    return send_from_directory("data", path)


@app.route("/api/get_orders", methods=["GET"])
def get_orders():
    return service.get_order_list()


@app.route('/api/test', methods=["GET"])
def is_logged_in_route():
    return "HI"


@app.route("/api/save_order", methods=["POST", "PUT"])
def save_request():
    return service.save_order(request)


@app.route("/api/get_order", methods=["GET"])
def get_order():
    return service.get_order(request)


@app.route("/api/update_order", methods=["PUT"])
def update_order():
    return service.update_order(request)


@app.route("/api/clear_orders", methods=["DELETE"])
def delete_orders():
    return service.clear_orders()


@app.route("/api/get_profiles", methods=["GET"])
def get_profiles():
    return service.get_profiles()


@app.route("/api/put_profile", methods=["PUT", "CREATE"])
def update_profile():
    return service.put_profile(request)


@app.route("/api/delete_profile", methods=["DELETE"])
def delete_profile():
    return service.delete_profile(request)


@app.route("/api/get_api_routes", methods=["GET"])
def get_api_routes():
    return app.config["API_ROUTES"]

