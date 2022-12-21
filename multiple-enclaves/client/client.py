#!/usr/local/bin/python3

# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import argparse
import socket
import sys
import time

def client_handler(args):
    # Send data to server, read response and print it
    client = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    client.connect((args.cid, args.port))
    for i in range(1, 4):
        msg = 'Hello %d!' % i
        print("\nSent: %s" % msg)
        client.sendall(msg.encode())
        sent = len(msg)
        recv = 0
        while recv < sent:
            data = client.recv(1024).decode()
            if not data:
                break
            recv += len(data)
            print("Recv: %s" % data)
    client.close()

def main():
    parser = argparse.ArgumentParser(prog='client')
    parser.add_argument("cid", type=int, help="The remote endpoint CID.")
    parser.add_argument("port", type=int, help="The remote endpoint port.")

    print("Starting client")
    client_handler(parser.parse_args())
    print("Exiting client")

if __name__ == "__main__":
    main()
