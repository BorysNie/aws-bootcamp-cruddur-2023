from datetime import datetime, timedelta, timezone
from aws_xray_sdk.core import xray_recorder

class UserActivities:
  def run(user_handle):
    try:
      # XRay
      segment = xray_recorder.begin_segment("user_activities")

      model = {
        'errors': None,
        'data': None
      }

      now = datetime.now(timezone.utc).astimezone()

      if user_handle == None or len(user_handle) < 1:
        model['errors'] = ['blank_user_handle']
      else:
        now = datetime.now()
        results = [{
          'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
          'handle':  'Andrew Brown',
          'message': 'Cloud is fun!',
          'created_at': (now - timedelta(days=1)).isoformat(),
          'expires_at': (now + timedelta(days=31)).isoformat()
        }]
        model['data'] = results

      # XRay
      hash = {
        "now": now.isoformat(),
        "results_size": len(model['data'])
        }
      subsegment = xray_recorder.begin_subsegment("subsegment-mock-data")
      segment.put_metadata("key", hash, "namespace")

    except Exception as exc:
      print("Error encontered within user activities")
      raise exc
    finally:
      xray_recorder.end_subsegment()

    return model