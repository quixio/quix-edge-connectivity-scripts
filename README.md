# Quix Edge Connectivity Test Scripts

This repository contains a script to verify your **Quix Edge installation is communicating correctly with Quix Cloud**. It allows you to verify SSL certificate trust, connectivity to a website, and Kafka server availability using Docker. The script supports custom configurations and an optional CA certificate for SSL verification.

## Prerequisites

- Docker installed on your system.
- A `config.yaml` file with the necessary configuration for the test suite.
- (Optional) A custom CA certificate (`ca.pem`) if you want to use a non-standard Certificate Authority for SSL certificate verification.



## Setup

1. **Clone the repository or download the files** (if building locally):
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Prepare the Configuration**: 
   
    The example_config.yaml file provides a template for the configuration. You need to copy this file to config.yaml and update the configuration fields with your specific details.
    ```bash
    cp example_config.yaml config.yaml
    ```
3. **Edit `config.yaml`**:
   
    Open the config.yaml file and update the necessary fields. Here's an example:
    ```bash
    platform:
        customca_cert_path: ""  # Optional: Path of the Custom CA certificate file (if required)
        portal_url: "https://portal.custname.quix.io/"  # Use the appropriate portal URL for your environment
        api_url: "https://portal-api.custname.quix.io/swagger/index.html"  # Use the appropriate API URL for your environment
        quix:
            workspace_id: "local-test-testing"  # Your Quix workspace ID
            topic: "test-suite"  # Your Kafka topic name in Quix
            sdk_token: ""  # Your Quix SDK token

    kafka:
        bootstrap_servers: "kafka.custname.quix.io:30095,kafka.custname.quix.io:30096,kafka.custname.quix.io:30097"  # Kafka bootstrap servers for Quix
        reachable: false  # Set to true if Kafka is reachable from where you are running the suite
    ```

   - `platform.customca_cert_path`: (Optional) Path to the custom CA certificate file for SSL verification.
   - `platform.portal_url`: The Quix Portal URL to test.
   - `platform.api_url`: The Quix API URL to test.
   - `platform.quix.workspace_id`: The ID of the Quix workspace you want to test.
   - `platform.quix.topic`: The Kafka topic in your workspace to use.
   - `platform.quix.sdk_token`: Your Quix SDK token for authentication.
   - `kafka.bootstrap_servers`: The Quix Kafka servers to test connectivity with.
   - `kafka.reachable`: Set this to true if Kafka is reachable from the machine running this suite.
4. **(Optional) Add a Custom CA Certificate**:
    If your environment uses a custom CA certificate, you can specify the path in `config.yaml` under `platform.customca_cert_path`. You can also provide the `ca.pem` file in the root of the project:

    ```bash
    cp /path/to/your/ca.pem .
    ```

## Usage Options
You can either build the Docker image locally or pull the pre-built image from the Docker registry.
### Option 1: Pull the Pre-Built Docker Image
You can pull the pre-built image from the Docker registry and run it directly without needing to build it locally.

1. **Pull the Pre-Built Image**:

    You can pull the latest version of the test suite image from the Docker registry:
    ```bash
    docker pull quixpublic.azurecr.io/test-suite:latest
    ```

2. **Run the Pre-Built Image**:
    Once you have the `config.yaml` ready, you can run the container directly, mounting `config.yaml` (and optionally `ca.pem)`:
    - **With config.yaml only**:
   ```bash
    docker run --rm -v $(PWD)/config.yaml:/app/config.yaml quixpublic.azurecr.io/test-suite:latest
    ```
    - **With config.yaml and ca.pem**:
    ```bash
   docker run --rm -v $(PWD)/config.yaml:/app/config.yaml -v $(PWD)/ca.pem:/app/ca.pem quixpublic.azurecr.io/test-suite:latest
    ```
### Option 2: Build Locally 
Alternatively, you can build the image locally.

1. **Build the Docker Image**: To build the Docker image locally, use the following command from the root of the project:

    ```bash
    docker build -t test-suite .
    ```

2. **Run the Test Suite:**:
   After configuring the `config.yaml` and optionally providing ca.pem, you can run the test suite with the following commands.
    - **With config.yaml only**:
   ```bash
    docker run --rm -v $(PWD)/config.yaml:/app/config.yaml test-suite
    ```
    - **With config.yaml and ca.pem**:
    ```bash
    docker run --rm -v $(PWD)/config.yaml:/app/config.yaml -v $(PWD)/ca.pem:/app/ca.pem test-suite
    ```

## Examples of outputs
### Everything is ok
```bash
✅ SSL certificate for portal.custname.quix.io:443 is trusted.
✅ Connectivity to https://portal.custname.quix.io/ is successful.
✅ SSL certificate for portal-api.custname.quix.io:443 is trusted.
✅ Connectivity to https://portal-api.custname.quix.io/swagger/index.html is successful.
✅ Successfully connected to Kafka at kafka.custname.quix.io:30095
✅ Successfully connected to Kafka at kafka.custname.quix.io:30096
✅ Successfully connected to Kafka at kafka.custname.quix.io:30097
✅ Successfully connected to Kafka using quixstream
```
### Something is wrong
```bash
✅ SSL certificate for portal.custname.quix.io:443 is trusted.
✅ Connectivity to https://portal.custname.quix.io/ is successful.
✅ SSL certificate for portal-api.custname.quix.io:443 is trusted.
✅ Connectivity to https://portal-api.custname.quix.io/swagger/index.html is successful.
✅ Successfully connected to Kafka at kafka.custname.quix.io:30095
✅ Successfully connected to Kafka at kafka.custname.quix.io:30096
✅ Successfully connected to Kafka at kafka.custname.quix.io:30097
❌ Failed to connect to Kafka using QuixStreams because Error 401 for url "https://portal-api.custname.quix.io/workspaces/local-test-testing/broker/librdkafka": {'message': 'User is not authenticated', 'correlationId': '2332CBB8'}
```
### Missing Configuration
```bash
✅ SSL certificate for portal.custname.quix.io:443 is trusted.
✅ Connectivity to https://portal.custname.quix.io/ is successful.
✅ SSL certificate for portal-api.custname.quix.io:443 is trusted.
✅ Connectivity to https://portal-api.custname.quix.io/swagger/index.html is successful.
❗ Kafka connectivity will not be tested. If you are interested on this, fill the kafka block and set as true
❗QuixStreams will not be no tested from this side, If you are interested on this, fill the quix block
```