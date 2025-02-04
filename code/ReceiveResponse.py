import struct
import socket

def receiveResponse(response):

    print("Processing DNS response..")
    print("----------------------------------------------------------------------------")

    header = struct.unpack(">HHHHHH", response[:12])
    transaction_id, flags, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT = header
    
    QR = (flags >> 15) & 1
    OPCODE = (flags >> 11) & 15
    AA = (flags >> 10) & 1
    TC = (flags >> 9) & 1
    RD = (flags >> 8) & 1
    RA = (flags >> 7) & 1
    RCODE = flags & 15

    print(f"header.ID = {transaction_id}")
    print(f"header.QR = {QR}")
    print(f"header.OPCODE = {OPCODE}")
    print(f"header.AA = {AA}")
    print(f"header.TC = {TC}")
    print(f"header.RD = {RD}")
    print(f"header.RA = {RA}")
    print(f"header.RCODE = {RCODE}")
    print(f"header.QDCOUNT = {QDCOUNT}")
    print(f"header.ANCOUNT = {ANCOUNT}")
    print(f"header.NSCOUNT = {NSCOUNT}")
    print(f"header.ARCOUNT = {ARCOUNT}")

    index = 12

    for i in range(QDCOUNT):
        qname, index = readName(response, 12)
        qtype, qclass = struct.unpack(">HH", response[index : index + 4])
        index += 4

        print(f"question.QNAME = {qname}")
        print(f"question.QTYPE = {qtype}")
        print(f"question.QCLASS = {qclass}")
    
    for i in range(ANCOUNT):
        name, index = readName(response, index)
        rtype, rclass, ttl, rdata_len = struct.unpack(">HHIH", response[index : index + 10])
        index += 10

        if rtype == 1: rdata = socket.inet_ntoa(response[index:index + rdata_len])
        else: rdata = response[index : index + rdata_len].hex()
        index += rdata_len

        print(f"answer.NAME = {name}")
        print(f"answer.TYPE = {rtype}")
        print(f"answer.CLASS = {rclass}")
        print(f"answer.TTL = {ttl}")
        print(f"answer.RDATA = {rdata} ## resolved IP address ##")
    
    print("----------------------------------------------------------------------------")

def readName(response, index):
    labels = []
    while index < len(response):
        length = response[index]
        if length == 0:
            index += 1
            break
        elif length & 192 == 192:
            pointer = struct.unpack(">H", response[index : index + 2])[0] & 16383
            name = readName(response, pointer)[0]
            labels.append(name)
            index += 2
            break
        else:
            index += 1
            labels.append(response[index : index + length].decode())
            index += length
    return ".".join(labels), index