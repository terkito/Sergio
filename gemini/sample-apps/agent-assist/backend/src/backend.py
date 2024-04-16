import pathlib
import secrets
import time
from datetime import datetime

import dateutil
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

import apis.customermanagement as customermanagement
import apis.leadsandsales as leadsandsales
import apis.marketingandoutreach as marketingandoutreach
import apis.performance as performance
from apis import calendar, chatbot, email, generateMail, kanban
from flask_session import Session
from utils.cal import Calendar
from utils.get_email_threads import get_email_threads_summary
from utils.get_users import get_users

app = Flask(
    __name__, static_url_path="", static_folder="build", template_folder="build"
)
app.secret_key = secrets.token_hex(24)
CORS(app, resources=r"/*")
directory_path = pathlib.Path(__file__).parent.resolve()
app.config["CORS_HEADERS"] = "Content-Type"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config.update(SESSION_COOKIE_SAMESITE="None")

socketio = SocketIO(app, cors_allowed_origins="*")
Session(app)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/users/contacted", methods=["GET"])
def get_real_users_contacted():
    users = get_users(isContact=True)
    return jsonify(users), 200


@app.route("/users/potential", methods=["GET"])
def get_real_users_potential():
    users = get_users(isContact=False)
    return jsonify(users), 200


@app.route("/users/mail_summary/<mail_id>", methods=["GET"])
def get_mail_summary(mail_id):
    print(mail_id)
    email_summary = get_email_threads_summary(mail_id)
    print(email_summary)
    return jsonify(email_summary), 200


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
        now_timestamp
    )
    return utc_datetime + offset


@app.route("/users/create_calendar_event", methods=["POST"])
def create_calendar_event():
    data = request.json
    mail_id = data.get("emailId")
    print("participants", mail_id)
    start_time = data.get("startValue")
    start_time = dateutil.parser.parse(start_time).time()
    end_time = data.get("endValue")
    end_time = dateutil.parser.parse(end_time).time()
    meet_date = data.get("meetDate")
    print(meet_date)
    meet_date = dateutil.parser.parse(meet_date).date()
    calendar = Calendar()
    startDateTime = datetime(
        meet_date.year,
        meet_date.month,
        meet_date.day,
        start_time.hour,
        start_time.minute,
    ).isoformat()
    endDateTime = datetime(
        meet_date.year, meet_date.month, meet_date.day, end_time.hour, end_time.minute
    ).isoformat()

    print(startDateTime, endDateTime)
    event = calendar.create_event(
        email=mail_id, startDateTime=startDateTime, endDateTime=endDateTime
    )
    print(mail_id, start_time, end_time, meet_date)
    return jsonify({"event": event}), 200


app.add_url_rule(
    "/workbench/performance", methods=["GET"], view_func=performance.getPerformanceData
)
app.add_url_rule(
    "/workbench/leadsandsales",
    methods=["GET"],
    view_func=leadsandsales.getLeadsAndSalesData,
)
app.add_url_rule(
    "/workbench/customermanagement",
    methods=["GET"],
    view_func=customermanagement.getCustomerManagementData,
)
app.add_url_rule(
    "/workbench/marketingandoutreach",
    methods=["GET"],
    view_func=marketingandoutreach.getMarketingAndOutreachData,
)
app.add_url_rule("/chatbot", methods=["POST"], view_func=chatbot.chatbot_entry)
app.add_url_rule(
    "/users/get_calendar_events",
    methods=["GET"],
    view_func=calendar.get_calendar_events,
)
app.add_url_rule("/mail", methods=["POST"], view_func=email.mail)
app.add_url_rule(
    "/agent-assist/generate_mail",
    methods=["POST"],
    view_func=generateMail.generate_mail,
)
app.add_url_rule(
    "/agent-assist/send_mail",
    methods=["POST"],
    view_func=generateMail.extract_and_send_mail,
)
app.add_url_rule(
    "/agent-assist/kanban", methods=["get"], view_func=kanban.get_kanban_data
)
app.add_url_rule(
    "/agent-assist/kanban/update", methods=["post"], view_func=kanban.update_kanban_data
)


@socketio.on("chat")
def handle_chatbot(data):
    print(data)
    emit("chat", ["Generating..."])
    chatbot_response = chatbot.chatbot_entry(data)
    print(chatbot_response)
    emit("chat", ["Done"])


if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)