# Week 2 — Distributed Tracing

- create gitpod task to automatically install reactjs app
- add to aws xray sdk to requirements txt
- add xray imports to backend flask app
- create xray resource and its file
aws xray create-group --group-name "Cruddr" --filter-expression "service(\"backend-flask\")"
- create aws sampling rule
aws xray create-sampling-rule --cli-input-json file://aws/json/xray.json
- add to docker compose file xray daemon service