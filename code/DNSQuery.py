import struct
import sys

def createDNSQuery(hostname):

    print("Preparing DNS query..")

    transaction_id = 0x1234
    flags = 0x0100
    QDCOUNT = 0x01
    ANCOUNT = 0x00
    NSCOUNT = 0x00
    ARCOUNT = 0x00

    header = struct.pack(">HHHHHH", transaction_id, flags, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT)

    qname = b"".join((len(part).to_bytes(1, 'big') + part.encode() for part in hostname.split("."))) + b'\x00'
    qtype = 1
    qclass = 1

    question = struct.pack(">HH", qtype, qclass)

    return header + qname + question