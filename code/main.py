import DNSQuery
import SendQuery
import ReceiveResponse
import socket
import sys

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: python3 dns_client.py <hostname>")
        sys.exit(1)

    hostname = sys.argv[1]
    ip = "8.8.8.8"
    port = 53

    query = DNSQuery.createDNSQuery(hostname)
    response = SendQuery.sendDNSQuery(query, ip, port)
    ReceiveResponse.receiveResponse(response)
