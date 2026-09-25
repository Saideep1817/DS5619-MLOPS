# Week 7: CI/CD & Integration Testing

Welcome to my Week 7 project for the MLOps course! This week was all about automation, reliability, and making sure our code doesn't break things when we push it to GitHub. 

## What did we build?

Instead of manually testing our application every time we make a change, I built an automated **Continuous Integration (CI) pipeline** using GitHub Actions. 

Our application is an object detection API. Since it relies on a specific environment, testing it properly means we need to test the actual Docker container that will run in production, not just the Python code in isolation.

## The Pipeline Breakdown

Whenever code is pushed to the `main` branch (or a pull request is opened), our GitHub Actions workflow (`ci.yml`) kicks in and runs three distinct jobs:

### 1. Linting (`lint`)
First, we check our code style using `flake8`. This ensures our Python code is clean, readable, and follows PEP-8 standards. It's a fast and cheap check.

### 2. Unit Tests (`unit-test`)
Next, we run our unit tests using `pytest` and Flask's test client. This tests the logic of our API endpoints without needing to spin up Docker or load heavy models. It's another fast check to catch basic logic errors early.

### 3. Integration Test (`integration-test`)
This is where the magic happens! **This job only runs if the first two jobs pass successfully.** Why? Because building Docker images is expensive and time-consuming. We don't want to waste cloud compute resources building a container for code that has a typo!

Once it runs, the integration test script (`scripts/integration_test.sh`):
1. **Builds** the Docker image (`week7-detector`).
2. **Starts** the container in detached mode, exposing port 8080.
3. **Waits** and pings the `/health` endpoint until the container is fully ready.
4. **Tests** the `/detect` endpoint by sending a real image fixture via `curl` and verifies that the API correctly returns detections.
5. **Cleans up** and tears down the container automatically when the test finishes.

## How to run it locally

If you want to run the integration test locally on your own machine (requires Docker and Bash):

```bash
# Make the script executable
chmod +x scripts/integration_test.sh

# Run the test
./scripts/integration_test.sh
```
