# WebsocketServerMS

The **WebSocket Server Microservice** acts as the interface between users and
the Redis database, providing real-time updates on the status and metrics
of battery data (BESS). It leverages FastAPI WebSocket capabilities to
establish and maintain real-time communication with connected users.

When a user connects to the WebSocket, the microservice sends the initial data
and subscribes the user to specific Redis channels. As RedisBackendMS publishes
updates to those channels, WebsocketServerMS detects the changes and pushes the
updated data to the user. This architecture ensures minimal latency and
simulates real-time updates for battery data.

## Key Responsibilities

1. **User Connection Management**: Establishes WebSocket connections with users
   and sends initial data upon connection.
2. **Channel Subscription**: Subscribes users to specific Redis channels based
   on their connection parameters.
3. **Real-Time Data Delivery**: Detects updates published by RedisBackendMS and
   pushes the new data to users, simulating real-time updates on battery
   metrics and status.

Here is a visualization of the WebsocketServerMS's role within the Pipeline
architecture:

![Pipeline Diagram](assets/images/WebsocketServerMS_in_Pipeline.png "Pipeline
Diagram")

## Installation

**Note**: This guide is for local installation. You may need `sudo`
privileges to execute some of these commands.

### Prerequisites

1. A Linux system (developed and tested on Ubuntu).
2. Redis installed and active. You may need to adjust certain `redis.conf`
   files to add a password.
3. Postman or equivalent, or a basic html file (to test the websocket
   connection).
4. Docker installed and active.
5. A Python virtual environment:
    - Create and activate a virtual environment (`venv`).
    - Run `pipenv install` to install dependencies.
    - Run `pipenv install --dev` to install development dependencies.

### Environment Variables

Ensure in the root directory there is an `.env` file with the following
parameters:

```plaintext
# Redis Configuration Settings
REDIS_HOST=
REDIS_PORT=
REDIS_DB=
REDIS_PASS=

# Server Configuration Settings
WS_HOST=
WS_PORT=
```

### Setup

- Make the CI/CD simulation script executable:
   ```bash
   chmod +x simulate_cicd.sh
    ```
- Run the simulation script to create the Docker container:
    ```bash 
    ./simulate_cicd.sh 
    ```
  This will create and start the Docker container.

**Note**: This script is intended to simulate a CI/CD deployment. The
actual `.github/workflows/deploy.yml` is simply a placeholder and would
be the next stage in the development process. Hence, this script will do
the following:

- stop and remove all previously running docker containers and images
  with the same image name and same container name (ensures a clean build)
- lint the project in accordance with PEP 8 standards with `pylint .`
- run unit tests with `pytest -v`
- build the docker image
- then run a docker container with that same image

For the purpose of the demo, I figured simulating a CI/CD deployment
pipeline via bash script would be easier to show/explain in a
limited amount of time, especially since the Pipeline is intended to run
"on-premise".

### Teardown

- Make the teardown script executable:
  ```bash
  chmod +x teardown.sh
  ```
- Run the teardown script:

    ```bash
    ./teardown.sh
    ```

- This will simply remove any docker images and containers associated with
  this specific Microservice.

## Usage

- To view the logs of the running Docker container, use the
  following command:
  ```bash
    docker logs -f ws_server_ms_simulation_container_1
    ```

**Note:** In a production environment, the logs would typically be redirected
to a
file and integrated with an ELK stack (Elasticsearch, Logstash, and Kibana) to
enable visualization and analysis on a dashboard. However, for the purposes of
this demo, I opted against introducing additional overhead to the Docker
container to minimize latency as much as possible.

### Websocket Connection

`WEBSOCKET` `ws://localhost:8001/ws`

#### Description

This WebSocket connection allows clients to receive real-time updates for
battery data. On establishing the WebSocket connection, an initial payload
containing the current state of the battery is sent. Subsequent updates are
pushed to the client as new data becomes available.

#### Initial Connection Response

Upon connecting, the server sends a JSON response containing the current state
of the battery data.

#### Example Initial Response

```json
{
  "battery:1:data": {
    "timestamp": 1731801715542,
    "voltage": 136,
    "current": 108,
    "temperature": 347,
    "state_of_charge": 36,
    "state_of_health": 49
  },
  "battery:2:data": {
    ...
  },
  ...
}
```

#### Update Messages

After the initial connection, the client receives updates as new data becomes
available. Each update includes all fields from the initial response, along
with additional fields such as `latency_ms`.

#### Example Update

```json
{
  "battery:1:data": {
    "timestamp": 1731801715549,
    "voltage": 130,
    "current": 110,
    "temperature": 340,
    "state_of_charge": 35,
    "state_of_health": 48,
    "latency_ms": 7
  }
}
```

#### Notes

- Ensure the WebSocket client can handle real-time updates and processes
  incoming
  data efficiently.
- The `latency_ms` field is only present in updates, providing an estimate of
  the
  data latency.
- If the connection is interrupted, reconnect to receive the latest data and
  updates.

## Testing

There is no need to explicitly run the linter or unit tests, since the
script `simulate_cicd.sh` already takes care of this.

## MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
