"""
Notification server to send the email to the user using the email server
"""

from os import environ

from flask import Flask, jsonify, request

from logging_module import logger
from smtp2go_client import send_the_email

app = Flask(__name__)

AUTH_TOKEN = environ.get("AUTH_TOKEN")


@app.get("/")
def index():
    """
    Home page of the server to check if the server is running
    """

    return "Hello World"


@app.post("/email")
def email():
    """
    Receive the message and receiver from the user and
    send the email to the receiver using the email server
    """

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        logger.error("No Authorization header found")
        msg = {"status": "failure", "message": "No Authorization header found"}
        return jsonify(msg), 401

    __token = auth_header.split(" ")[1]

    if __token != AUTH_TOKEN:
        logger.error("Invalid token")
        msg = {"status": "failure", "message": "Invalid token"}
        return jsonify(msg), 401

    data = request.get_json()
    print(data)

    if send_the_email(data["receiver"], data["subject"], data["message"]):
        logger.info(
            f"Receiver: {data['receiver']}, Subject: {data['subject']}, Sent successfully"
        )
        return jsonify({"status": "success", "message": "Email sent successfully"}), 200
    else:
        logger.warning(
            f"Receiver: {data['receiver']}, Subject: {data['subject']}, Failed to send"
        )
        return jsonify({"status": "failed", "message": "Email sending failed"}), 400


@app.post("/sms")
def sms():
    msg = {"status": "failure", "message": "Not implemented yet"}
    return jsonify(msg), 400


if __name__ == "__main__":
    logger.info("Starting the notification server")
    app.run(host="0.0.0.0", port=5000, debug=True)
