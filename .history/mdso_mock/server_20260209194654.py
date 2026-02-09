from flask import Flask, request, jsonify

app = Flask(__name__)
services = {}

@app.route("/provision", methods=["POST"])
def provision_service():
    data = request.json
    service_id = f"svc_{len(services)+1}"
    services[service_id] = {
        "name": data.get("name", "Generic Service"),
        "status": "Provisioned",
        "bandwidth": data.get("bandwidth", "1Gbps")
    }
    return jsonify({"message": "Service provisioned", "service_id": service_id})

@app.route("/status", methods=["GET"])
def check_status():
    service_id = request.args.get("service_id")
    if service_id in services:
        return jsonify({"service_id": service_id, "status": services[service_id]["status"]})
    return jsonify({"error": "Service not found"}), 404

@app.route("/optimize", methods=["POST"])
def optimize_service():
    data = request.json
    service_id = data.get("service_id")
    if service_id in services:
        services[service_id]["bandwidth"] = data.get("bandwidth", "2Gbps")
        services[service_id]["status"] = "Optimized"
        return jsonify({"message": "Service optimized", "service_id": service_id})
    return jsonify({"error": "Service not found"}), 404

if __name__ == "__main__":
    app.run(port=5000)