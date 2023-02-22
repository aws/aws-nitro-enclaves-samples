# Vsock Communication Sample

A hello-world example for Nitro Enclaves vsock server and client communication.

## Prerequisites

1. The `vsock-sample` is a Nitro Enclaves application that can be run either
as a server or a client. The client sends the “Hello, world!” message to the
server. The server receives the message and prints it to the standard output.

2. The sample is written and tested in Go 1.19. Any Go version 1.17+ should work with this example (as the vsock package dependency is written in 1.17).

## How to use the enclave as the server and the parent instance as the client

1. Build the Enclave Image File (EIF) starting from the `Dockerfile.server` file
in this directory. We chose to use a multi-stage build to build the Docker image
from *go-alpine* and then deploy the application using a *scratch* image to keep
the enclave image as small as possible, but you can also use other Docker images.

__Note__: You can use any other port number besides 5005 by modifying the command
inside the `Dockerfile.server` file.

```
docker build -t vsock-sample-server -f Dockerfile.server .
nitro-cli build-enclave --docker-uri vsock-sample-server --output-file vsock_sample_server.eif
```

2. Configure the pool of memory and vCPUs (the `nitro-cli-config` script can be used)
and run the enclave using the previously-built EIF.

```
// 1 vCPUs and 128 MiB memory
nitro-cli-config -t 1 -m 128
nitro-cli run-enclave --eif-path vsock_sample_server.eif --cpu-count 1 --memory 128 --debug-mode
```

3. Connect to the enclave console using `nitro-cli`.

```
nitro-cli console --enclave-id $ENCLAVE_ID
```

4. In another terminal, build and run the client.

```
docker build -t vsock-sample-client -f Dockerfile.client .
docker run -it --rm vsock-sample-client -cid $ENCLAVE_CID -port 5005
```

__Note__: Here `$ENCLAVE_CID` is a generated integer value (e.g. 16) of the enclave CID.

5. The enclave console output should look like this:

```
[    0.051633] rtc-pl031 40002000.rtc: setting system clock to 2022-12-08 20:21:47 UTC (1670530907)
[    0.052366] Freeing unused kernel memory: 512K
[    0.056733] nsm: loading out-of-tree module taints kernel.
[    0.057098] nsm: module verification failed: signature and/or required key missing - tainting kernel
[    0.058013] NSM RNG: returning rand bytes = 16
[    0.058493] NSM RNG: returning rand bytes = 128
[    0.058803] random: fast init done
[    0.059766] NSM RNG: returning rand bytes = 128
[    0.060030] random: crng init done
Listening on :5005
2022/12/08 20:22:43 [INFO]: Hello, world!
```

## How to use the parent instance as the server and the enclave as the client

1. Build the Enclave Image File (EIF) starting from the `Dockerfile.client` file
in this directory. We chose to use a multi-stage build to build the Docker image
from *go-alpine* and then deploy the application using a *scratch* image to keep
the enclave image as small as possible, but you can also use other Docker images.

__Notes__:
* The value 3 is the CID of the parent instance
* You can use any other port number besides 5005 by modifying the command inside the Dockerfile.client file

```
docker build -t vsock-sample-client -f Dockerfile.client .
```

```
nitro-cli build-enclave --docker-uri vsock-sample-client --output-file vsock_sample_client.eif
```

2. Build and run the server inside the parent instance.

```
docker build -t vsock-sample-server -f Dockerfile.server .
docker run -itd --name vsock-sample-server vsock-sample-server
```

3. Configure the pool of memory and vCPUs (the `nitro-cli-config`
script can be used) and run the enclave using the built EIF.

```
// 2 vCPUs and 128 MiB memory
nitro-cli-config -t 1 -m 128
nitro-cli run-enclave --eif-path vsock_sample_client.eif --cpu-count 1 --memory 128 --debug-mode
```

4. The server container output should print __Hello, world!__.

```
docker logs vsock-sample-server
Listening on :5005
[INFO]: Hello, world!
```

__Note__:
* The client application inside the enclave sends the message once and then exits thus the enclave shall terminate.

Now you can replace the client/server code with your own code.
