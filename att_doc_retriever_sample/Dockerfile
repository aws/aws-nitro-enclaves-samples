# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

FROM ubuntu:latest AS builder
WORKDIR /root/att_doc_retriever_sample/rs/
COPY att_doc_retriever_sample/rs .
RUN apt-get update && apt-get install gcc \
                                      curl -y
# Get Rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustup target install x86_64-unknown-linux-musl
# Build rust app
RUN cargo build --release --target=x86_64-unknown-linux-musl


FROM python:3.7.9-alpine3.12
WORKDIR /root/att_doc_retriever_sample/py/
# Copy the Rust compiled binary from previous image
COPY --from=builder /root/att_doc_retriever_sample/rs/target/x86_64-unknown-linux-musl/release/att_doc_retriever_sample .
# Copy the python client-server handler logic to the container
COPY att_doc_retriever_sample/py/att_doc_retriever_sample.py .
# Copy the client-server logic from the vsock sample to the container
COPY vsock_sample/py/vsock-sample.py /root/vsock_sample/py/
# 5010 is the socket port
CMD ["/usr/local/bin/python3", "/root/att_doc_retriever_sample/py/att_doc_retriever_sample.py", "server", "5010"]

