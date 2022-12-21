# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

FROM public.ecr.aws/docker/library/python:3.7.9-alpine3.12

COPY server.py .

CMD ["/usr/local/bin/python3", "server.py", "5001"]
