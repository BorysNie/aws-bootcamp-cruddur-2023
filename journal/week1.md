# Week 1 — App Containerization

## ToDo Checklist<p>

### Watch videos
- [Watched Grading Homework Summaries](https://www.youtube.com/watch?v=FKAScachFgk&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=25)<br>
- [Week 1 - Live Stream](https://www.youtube.com/watch?v=zJnNe5Nv4tE&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=22)<br>
- [Week 1 - Spending Considerations](https://www.youtube.com/watch?v=OAMHu1NiYoI&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=24)<br>
- [Week 1 - Container Security Considerations](https://www.youtube.com/watch?v=OjZz4D0B-cA&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=25)<br>

### OpenAPI<p>

- Review the OpenAPI specifications
- Create and document valid schema for our application API
<br>

### Docker<p>

- Dockerize the frontend and backend application
- Create docker compose file to build and spin up services ie.
  - Frontend and backend, including their ports and custom network
  - PostgreSQL database with docker volume
  - DynamoDB database with local volume bind
<br>

### Application<p>

- Create Notifications API endpoint
  - Created a backend service which responds when notifications API is called with set schema
  - Add to application the endpoint which returns said data once called
  - Create frontend route to the notification page
  - Create page and styling for the notification page
<br>

### Databases<p>

- Create PostgreSQL database service for local use
- Create DynamoDB database service for later
- Investigate PostgreSQL VS Code extension and psql client
<br>

### Homework challenges<p>

- Replace Dockerfile CMD with command within docker compose
- Docker build, tag and push (you'll need to login using docker login cmd)
```sh
docker build -t frontend-react-js:0.1 .
docker push frontend-react-js:0.1
```
- Investigate and learn more about Multi-stage Docker building
- Create healthcheck script and add var to dockerfile
- Research docker best practises and implement them in Dockerfiles
<br>

### Gitpod docker cleanup<p>

- Compose down current services
```sh
docker compose --file <PATH-TO-COMPOSE.yaml> down
```
- Stop all running docker containers
```sh
docker stop $(docker ps --all --quiet)
```
- Remove all containers
```sh
docker rm $(docker ps --all --quiet)
```
- Docker remove all images
```sh
docker rmi $(docker image ls --all --quiet)
```
- Docker remove **all**!<br>
The following will remove all stopped containers, custom networks, volumes and dangling images as well as build cache be cautious!
```sh
docker system prune --all --force --volumes
```
