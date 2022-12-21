#!/usr/local/bin/python3

# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import argparse
import socket
import sys
import time

def server_handler(args):
    # Listen for data and return the reverse string of it
    server = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    server.bind((socket.VMADDR_CID_ANY, args.port))
    server.listen(1024)
    (conn, (remote_cid, remote_port)) = server.accept()
    while True:
        try:
            data = conn.recv(1024).decode()
        except socket.error as e:
            break
        if not data:
            break
        print("\nRecv: %s" % data)
        data = "ACK(" + data + ")"
        print("Sent: %s" % data)
        conn.sendall(data.encode())
    conn.close()
    server.close()

def main():
    parser = argparse.ArgumentParser(prog='server')
    parser.add_argument("port", type=int, help="The local port to listen on.")

    args = parser.parse_args()
    print("Starting server on port %d" % args.port)
    server_handler(args)
    print("Exiting server")

if __name__ == "__main__":
    main()
