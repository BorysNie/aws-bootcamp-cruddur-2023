# Week 2 — Distributed Tracing

- create gitpod task to automatically install reactjs app
- add to aws xray sdk to requirements txt
- add xray imports to backend flask app
- create xray resource and its file
aws xray create-group --group-name "Cruddr" --filter-expression "service(\"backend-flask\")"
- create aws sampling rule
aws xray create-sampling-rule --cli-input-json file://aws/json/xray.json
- add to docker compose file xray daemon service

- watch honecomb livestream setup
- encountered issues setting up honecomb and getting containers to work as per video (issues with import within home activities)
- following traces in honeycomb were successful
- issues with formatting home activities to add results span
- xray issues retrieving aws ec2 metadata (container running and port not open)
- change env var to AWS_REGION for xray daemon
-
