#!/usr/local/bin/python3

# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import argparse
import socket
import sys
import time

def reverse_connections(src, dst):
    return dst, src

def proxy_handler(args):
    # proxy_server connects to (server_cid, server_port)
    # client connects to proxy_server
    # It send the data back and forth between client and server
    proxy_client = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    proxy_server = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    server_addr = (args.server_cid, args.server_port)
    proxy_client.connect(server_addr)

    proxy_server.bind((socket.VMADDR_CID_ANY, args.client_port))
    proxy_server.listen(1024)
    (conn, addr) = proxy_server.accept()

    with conn:
        print("Client enclave: %s" % str(addr))
        print("Server enclave: %s" % str(server_addr))
        src = conn
        dst = proxy_client
        print("%15s | %-29s --> %-29s" % ("Message", "Source enclave", "Destination enclave"))
        while True:
            saddr = src.getpeername()
            daddr = dst.getpeername()
            template = "{{cid:{:6}, port:{:10}}}"
            src_addr = template.format(saddr[0], saddr[1])
            dst_addr = template.format(daddr[0], daddr[1])
            try:
                data = src.recv(1024).decode()
            except socket.error as e:
                print("Socket error: ", e)
                break
            if not data:
                print("Connection closed")
                break

            print("%15s | %s --> %s" % (data, src_addr, dst_addr))
            dst.sendall(data.encode())
            src, dst = reverse_connections(src, dst)
    proxy_client.close()
    proxy_server.close()

def main():
    parser = argparse.ArgumentParser(prog='proxy')
    parser.add_argument("client_port", type=int, help="The local port to listen on.")
    parser.add_argument("server_port", type=int, help="Port to forward the connection")
    parser.add_argument("server_cid", type=int, help="Cid of the enclave running the server")

    args = parser.parse_args()
    print("Starting proxy on port %d to exchange data with (%d, %d)" % 
            (args.client_port, args.server_cid, args.server_port))
    proxy_handler(args)
    print("Exiting proxy")

if __name__ == "__main__":
    main()
