# Quix Edge Connectivity Test Scripts

This repository contains various scripts to verify your Quix Edge installation is communicating correctly with Quix Cloud. 

The scripts included in this repository serve different purposes, from producing and consuming messages to checking client-side certificates.

Before running each script:
 . Ensure you have replaced `YOUR_WORKSPACE_ID` with your actual workspace ID.

## Scripts

### PowerShell Script: `powershell/check-client-side-cert.ps1`

This script is used to check the client-side certificate for a secure connection to the Quix portal.

#### Usage:
1. Replace `YOUR_WORKSPACE_ID` with your workspace ID.
2. Run the script in a PowerShell environment to verify the client-side certificate.

### Shell Script: `shell/check-client-side-cert.sh`

This script performs a similar function to the PowerShell script but is intended for Unix-based systems. It uses `openssl` to check the client-side certificate.

#### Usage:
1. Replace `YOUR_WORKSPACE_ID` with your workspace ID.
2. Run the script in a Unix-based shell to verify the client-side certificate.

### Python Script: `python/main.py`

This script verifies that you can exchange messages with the Quix platform.

#### Key Features:
- **Produce a Message**: Sends a message to a specified topic.
- **Consume a Message**: Reads messages from the specified topic and processes them.

#### Usage:
1. Fill in your Quix details and credentials in the environment variables.
2. Run the script to produce and consume messages.
