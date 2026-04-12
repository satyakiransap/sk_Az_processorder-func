import azure.functions as func
import logging
import json
from datetime import datetime

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="orders/process", methods=["POST"])
def ProcessOrder(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("ProcessOrder function triggered.")

    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON payload"}),
            status_code=400,
            mimetype="application/json"
        )

    required = ["orderId", "customer", "amount", "status"]
    missing = [field for field in required if field not in body]

    if missing:
        return func.HttpResponse(
            json.dumps({"error": f"Missing fields: {', '.join(missing)}"}),
            status_code=400,
            mimetype="application/json"
        )

    processed_order = {
        "orderId": body["orderId"],
        "customer": body["customer"],
        "amount": body["amount"],
        "originalStatus": body["status"],
        "processedStatus": "Processed",
        "processedAt": datetime.utcnow().isoformat() + "Z"
    }

    logging.info(f"Order processed: {processed_order}")

    return func.HttpResponse(
        json.dumps(processed_order),
        status_code=200,
        mimetype="application/json"
    )
