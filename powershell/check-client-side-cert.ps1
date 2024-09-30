# Define the server and port
$server = "portal.YOUR_WORKSPACE_ID.quix.io" 
$port = 443

# Create a TCP connection to the server
$tcpClient = New-Object System.Net.Sockets.TcpClient
$tcpClient.Connect($server, $port)

# Get the stream for the connection
$sslStream = New-Object System.Net.Security.SslStream($tcpClient.GetStream(), $false)
$sslStream.AuthenticateAsClient($server)

# Get the certificate
$cert = $sslStream.RemoteCertificate

# Close the connection
$sslStream.Close()
$tcpClient.Close()

# Output the certificate
$cert | Format-List