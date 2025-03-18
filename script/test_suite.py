import yaml
import socket
import ssl
import os
import http.client
import logging
from urllib.parse import urlparse

from quixstreams import Application

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Load the YAML configuration


def load_config(config_file="config.yaml"):
    with open(config_file, "r") as file:
        return yaml.safe_load(file)

#  SSL certificate check function


def check_ssl_certificate(host, port, server_name=None, ca_cert_path=None):
    context = ssl.create_default_context(cafile=ca_cert_path)

    try:
        # Create a TCP connection and wrap it with SSL
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=server_name or host) as ssock:
                # Trigger the SSL handshake and retrieve the certificate
                cert = ssock.getpeercert()
                if cert:
                    logging.info(
                        f"✅ SSL certificate for {host}:{port} is trusted.")
                else:
                    logging.error(
                        f"❌ SSL certificate for {host}:{port} could not be verified.")

    except ssl.SSLError as e:
        logging.error(f"❌ SSL error while connecting to {host}:{port}: {e}")

    except (socket.timeout, socket.error) as e:
        logging.error(
            f"❌ Failed to connect to {host}:{port} for SSL check: {e}")


# Check if the site's certificate is trusted and if it is reachable via HTTPS
def check_site_certificate_and_connectivity(site_url, ca_cert_path=None):
    parsed_url = urlparse(site_url)
    host = parsed_url.hostname
    port = parsed_url.port or 443
    path = parsed_url.path
    # check the SSL certificate
    check_ssl_certificate(host, port, host, ca_cert_path)

    # check the HTTP connectivity
    try:
        conn = conn = http.client.HTTPSConnection(
            host, port, context=ssl.create_default_context(cafile=ca_cert_path), timeout=5)
        conn.request("GET", path)
        response = conn.getresponse()

        if response.status >= 200 and response.status <= 399:
            logging.info(f"✅ Connectivity to {site_url} is successful.")
        else:
            logging.error(
                f"❌ Failed to connect to {site_url}. Status code: {response.status}")
        conn.close()

    except Exception as e:
        logging.error(f"❌ Failed to connect to {site_url}: {e}")


# Check if TCP connectivity to Kafka is possible
def check_kafka_connectivity(bootstrap_servers):
    kafka_host, kafka_port = bootstrap_servers.split(':')
    try:
        # Create a secure SSL connection to Kafka
        with socket.create_connection((kafka_host, int(kafka_port)), timeout=5) as sock:
            logging.info(
                f"✅ Successfully connected to Kafka at {bootstrap_servers}")
    except ssl.SSLError as e:
        logging.error(
            f"❌ SSL error while connecting to Kafka at {bootstrap_servers}: {e}")
    except (socket.timeout, socket.error) as e:
        logging.error(
            f"❌ Failed to connect to Kafka at {bootstrap_servers}: {e}")

# Check with auth data if can be used quixstreams


def check_quix_streaming_data(workspace_id, portal_api, testing_topic, sdk_token, ca_cert_path=None):
    os.environ["Quix__Portal__Api"] = portal_api
    os.environ["Quix__Workspace__Id"] = workspace_id
    # also known as Streaming Token
    os.environ["Quix__Sdk__Token"] = sdk_token
    if ca_cert_path:
        os.environ["REQUESTS_CA_BUNDLE"] = ca_cert_path

    def check_for_exit_message(row):
        logging.info("✅ Successfully connected to Kafka using quixstream")
        app.stop()

    try:
        app = Application(
            consumer_group=testing_topic,
            auto_offset_reset="earliest",
            loglevel="CRITICAL",
            request_timeout=5)
        topic = app.topic(testing_topic)

        with app.get_producer() as producer:
            producer.produce(
                topic.name, '{"message": "Hello, World!"}', 'hello-world')

        sdf = app.dataframe(topic)
        sdf.update(check_for_exit_message)
        app.run(sdf)

    except Exception as e:
        logging.error(
            f"❌ Failed to connect to Kafka using QuixStreams because {e}")


def main():
    # Load the configuration
    config = load_config()
    # Get site and Kafka details from config
    platform_config = config['platform']
    customca_cert_path = config['platform'].get('customca_cert_path', None)

    if platform_config:
        check_site_certificate_and_connectivity(
            platform_config['portal_url'], ca_cert_path=customca_cert_path)
        check_site_certificate_and_connectivity(
            platform_config['api_url'], ca_cert_path=customca_cert_path)

    if config['kafka']['reachable']:
        kafka_bootstrap_servers = config['kafka']['bootstrap_servers']
        for server in kafka_bootstrap_servers.split(","):
            check_kafka_connectivity(server)
    else:
        logging.warning(
            "❗Kafka connectivity will not be tested. If you are interested on this, fill the kafka block and set as true")

    quix_config = config['platform']['quix']
    if quix_config['workspace_id'] != '' and quix_config['topic'] != '' and quix_config['sdk_token'] != '':
        parsed_url = urlparse(platform_config['api_url'])
        cleaned_url = f"{parsed_url.scheme}://{parsed_url.hostname}"
        check_quix_streaming_data(workspace_id=quix_config['workspace_id'], portal_api=cleaned_url,
                                  testing_topic=quix_config['topic'], sdk_token=quix_config['sdk_token'], ca_cert_path=customca_cert_path)
    else:
        logging.warning(
            "❗QuixStreams will not be no tested from this side, If you are interested on this, fill the quix block")


if __name__ == "__main__":
    main()
