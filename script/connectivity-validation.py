import yaml
import socket
import ssl
import http.client
import logging
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Load the YAML configuration
def load_config(config_file="config.yaml"):
    with open(config_file, "r") as file:
        return yaml.safe_load(file)

# Unified SSL certificate check function for both sites and Kafka
def check_ssl_certificate(host, port, server_name=None, ca_cert_path=None):
    context = ssl.create_default_context(cafile=ca_cert_path)

    try:
        # Create a TCP connection and wrap it with SSL
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=server_name or host) as ssock:
                # Trigger the SSL handshake and retrieve the certificate
                cert = ssock.getpeercert()
                if cert:
                    logging.info(f"✅ SSL certificate for {host}:{port} is trusted.")
                else:
                    logging.error(f"❌ SSL certificate for {host}:{port} could not be verified.")

    except ssl.SSLError as e:
        logging.error(f"❌ SSL error while connecting to {host}:{port}: {e}")

    except (socket.timeout, socket.error) as e:
        logging.error(f"❌ Failed to connect to {host}:{port} for SSL check: {e}")
 

# Check if the site's certificate is trusted and if it is reachable via HTTPS
def check_site_certificate_and_connectivity(site_url, ca_cert_path=None):
    parsed_url = urlparse(site_url)
    host = parsed_url.hostname
    port = parsed_url.port or 443
    path = parsed_url.path
    # check the SSL certificate
    check_ssl_certificate(host, port, host, ca_cert_path)

    # Now, check the HTTP connectivity
    try:
        conn = conn = http.client.HTTPSConnection(host, port, context=ssl.create_default_context(cafile=ca_cert_path), timeout=5)
        conn.request("GET", path)
        response = conn.getresponse()

        if response.status >= 200 and response.status <=399:
            logging.info(f"✅ Connectivity to {site_url} is successful.")
        else:
            logging.error(f"❌ Failed to connect to {site_url}. Status code: {response.status}")
        conn.close()
        
    except Exception as e:
        logging.error(f"❌ Failed to connect to {site_url}: {e}")
        

# Check if TCP connectivity to Kafka is possible
def check_kafka_connectivity(bootstrap_servers, ca_cert_path=None):
    kafka_host, kafka_port = bootstrap_servers.split(':')
    # check the SSL certificatep
    # check_ssl_certificate(kafka_host, kafka_port,kafka_host,ca_cert_path)
    try:
        # Create a secure SSL connection to Kafka
       
        with socket.create_connection((kafka_host, int(kafka_port)), timeout=5) as sock:
            #with context.wrap_socket(sock, server_hostname=kafka_host) as ssock:
            logging.info(f"✅ Successfully connected to Kafka TCP at {bootstrap_servers}")
    except ssl.SSLError as e:
        logging.error(f"❌ SSL error while connecting to Kafka at {bootstrap_servers}: {e}")
    except (socket.timeout, socket.error) as e:
        logging.error(f"❌ Failed to connect to Kafka TCP at {bootstrap_servers}: {e}")

def check_quix_streaming_data():
    pass

def main():
    # Load the configuration
    config = load_config()
    # Get site and Kafka details from config
    sites_url = config['platform']['urls']
    
    if sites_url:
        webca_cert_path = config['platform'].get('customca_cert_path', None)
        print (webca_cert_path)
        for site in sites_url:
            check_site_certificate_and_connectivity(site, ca_cert_path=webca_cert_path)

            

    if config['kafka']['recheable']:
        kafka_bootstrap_servers = config['kafka']['bootstrap_servers']
        for server in kafka_bootstrap_servers.split(","):
            check_kafka_connectivity(server)

if __name__ == "__main__":
    main()
