from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os

from services.home_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.notifications_activities import *
from services.create_message import *
from services.show_activity import *

# Import custom JWT module
from lib.cognito_jwt_token import CognitoJWTToken, TokenVerifyError, extract_access_token

# HoneyComb imports
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, \
  ConsoleSpanExporter, SimpleSpanProcessor

# AWS X-Ray imports
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# Cloudwatch logs imports
import watchtower
import logging
from time import strftime

# Rollbar imports
import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

# Configuring logger to use CloudWatch
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group="backend-flask")
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
LOGGER.info("Logging configured")

# HoneyComb init tracing exporter
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)

# Show logs within backend flask app stdout
# simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
# provider.add_span_processor(simple_processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app) # Init automatic
RequestsInstrumentor().instrument() # instrumentation with flask
frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
origins = [frontend, backend]
cors = CORS(
  app,
  resources={r"/api/*": {"origins": origins}},
  headers=['Content-Type', 'Authorization'],
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)

# AWS Cognito init
cognito_jwt_token = CognitoJWTToken(
  os.getenv("AWS_COGNITO_USER_POOL_ID"),
  os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"),
  os.getenv("AWS_DEFAULT_REGION"))

# AWS X-Ray init recorder and middleware services
xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service="backend-flask", dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)

# rollbar_access_token = os.getenv("ROLLBAR_ACCESS_TOKEN")
# @app.before_first_request
# def init_rollbar():
#   rollbar.init(
#     rollbar_access_token,
#     "production",
#     root = os.path.dirname(os.path.relpath(__file__)), # server root dir
#     allow_logging_basic_config=False
#   )

# Cloudwatch logs after each request
@app.after_request
def after_request(response):
  timestamp = strftime("[%Y-%b-%d %H:%M]")
  LOGGER.error(f"{timestamp} {request.remote_addr} {request.method} \
    {request.scheme} {request.full_path} {response.status}")
  return response

@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
  user_handle  = 'andrewbrown'
  model = MessageGroups.run(user_handle=user_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/messages/@<string:handle>", methods=['GET'])
def data_messages(handle):
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.args.get('user_reciever_handle')

  model = Messages.run(user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.json['user_receiver_handle']
  message = request.json['message']

  model = CreateMessage.run(message=message,user_sender_handle=user_sender_handle,user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities/home", methods=['GET'])
@xray_recorder.capture("activities_home")
def data_home():
  access_token = extract_access_token(request.headers)
  try:
    claims = cognito_jwt_token.verify(access_token)
    app.logger.debug(f"Tocken authenticated: {access_token}")
    app.logger.debug(claims['username'])
    data = HomeActivities.run(logger=LOGGER, cognito_user_id=claims['username'])
    app.logger.debug(claims)
  except TokenVerifyError as exc:
    _ = request.data
    app.logger.debug(f"Tocken unauthenticated: {exc}")

  return data, 200

@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
@xray_recorder.capture("activities_users")
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
  user_handle  = 'andrewbrown'
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, user_handle, ttl)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
@xray_recorder.capture("activities_show")
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'andrewbrown'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

# @app.route("/rollbar/test")
# def rollbar_test():
#   rollbar.report_message("Rollbar reports Hello World!", "warning")
#   return "Rollbar Hello World!"

@app.route('/api/health-check')
def health_check():
  return {'success': True}, 200

if __name__ == "__main__":
  app.run(debug=True)