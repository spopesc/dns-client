import socket

def sendDNSQuery(query, ip, port):

    print("Contacting DNS server..")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for i in range(1, 4):
            try:
                print("Sending DNS query..")
                sock.sendto(query, (ip, port))
                response = sock.recvfrom(512)[0]
                print(f"Received DNS response (attempt {i} of 3)")
                break
            except socket.timeout: print("Error: Request timed out")
            except Exception as e: print(f"Error: {e}")
            if i == 3: print("Giving up after 3 attempts.")
    return response