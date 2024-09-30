# Define the server and port
$server = "kafka.YOUR_WORKSPACE_ID.quix.io"
$port = 443

# Load the system's trusted root certificates (equivalent to /etc/ssl/certs)
$certStore = New-Object System.Security.Cryptography.X509Certificates.X509Store("Root", "LocalMachine")
$certStore.Open("ReadOnly")
$trustedCerts = $certStore.Certificates
$certStore.Close()

# Create a TCP connection to the server
$tcpClient = New-Object System.Net.Sockets.TcpClient
$tcpClient.Connect($server, $port)

# Get the SSL stream
$sslStream = New-Object System.Net.Security.SslStream($tcpClient.GetStream(), $false)

# Define a callback function to validate the server certificate
$sslCallback = {
    param ($sender, $certificate, $chain, $sslPolicyErrors)
    
    # Output any SSL policy errors
    Write-Host "SSL Policy Errors: $sslPolicyErrors"
    
    # Check each element in the certificate chain
    foreach ($chainElement in $chain.ChainElements) {
        Write-Host "Certificate Subject: $($chainElement.Certificate.Subject)"
        Write-Host "Certificate Issuer: $($chainElement.Certificate.Issuer)"
        Write-Host "------------------------------------"
    }
    
    # Check if the certificate is trusted by the system
    $chain.ChainPolicy.RevocationMode = [System.Security.Cryptography.X509Certificates.X509RevocationMode]::NoCheck
    $isChainValid = $chain.Build($certificate)
    
    if ($isChainValid) {
        Write-Host "The certificate chain is valid."
        return $true
    } else {
        Write-Host "The certificate chain is NOT valid."
        return $false
    }
}

# Authenticate the SSL connection using the callback for certificate validation
$sslStream.AuthenticateAsClient($server, $null, [System.Security.Authentication.SslProtocols]::Tls12, $false)

# Get the remote certificate
$remoteCert = $sslStream.RemoteCertificate

# Output the server certificate details
$certDetails = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2 $remoteCert
$certDetails | Format-List

# Close the connection
$sslStream.Close()
$tcpClient.Close()