# Vsock Communication Sample

A hello-world example for Nitro Enclaves vsock server and client communication.

## Prerequisites

1. The `vsock-sample` is a Nitro Enclaves application that can be run either
as a server or a client. The client sends the “Hello, world!” message to the
server. The server receives the message and prints it to the standard output.

2. The sample is written and tested in Python 3.7.9. Any Python version
should work as long as it has `AF_VSOCK` socket support.

## How to use the enclave as the server and the parent instance as the client

1. Build the Enclave Image File (EIF) starting from the `Dockerfile.server` file
in this directory. We chose to start from the *python-alpine* Docker image to keep
the enclave image as small as possible, but you can also use other optimized
Docker images to further decrease the final image size.

__Note__: You can use any other port number besides 5005 by modifying the command
inside the `Dockerfile.server` file.

```
docker build -t vsock-sample-server -f Dockerfile.server .
nitro-cli build-enclave --docker-uri vsock-sample-server --output-file vsock_sample_server.eif
```

2. Configure the pool of memory and vCPUs (the `nitro-cli-config` script can be used)
and run the enclave using the previously-built EIF.

```
// 2 vCPUs and 256 MiB memory
nitro-cli-config -t 2 -m 256
nitro-cli run-enclave --eif-path vsock_sample_server.eif --cpu-count 2 --memory 256 --debug-mode
```

3. Connect to the enclave console using `nitro-cli`.

```
nitro-cli console --enclave-id $ENCLAVE_ID
```

4. In another terminal, run the client.

```
python3 vsock-sample.py client $ENCLAVE_CID 5005
```

__Note__: Here `$ENCLAVE_CID` is a generated integer value (e.g. 16) of the enclave CID.

5. The enclave console output should look like this:

```
[    0.127079] Freeing unused kernel memory: 476K
[    0.127631] nsm: loading out-of-tree module taints kernel.
[    0.128055] nsm: module verification failed: signature and/or required key missing - tainting kernel
[    0.200988] random: python3: uninitialized urandom read (24 bytes read)
Hello, world!
```

## How to use the parent instance as the server and the enclave as the client

1. Build the Enclave Image File (EIF) starting from the `Dockerfile.client` file
in this directory. We chose to start from the python-alpine docker image to keep
the enclave image as small as possible, but you can also use other optimized
Docker images to further decrease the final image size.

__Notes__:
* The value 3 is the CID of the parent instance
* You can use any other port number besides 5005 by modifying the command inside the Dockerfile.client file

```
docker build -t vsock-sample-client -f Dockerfile.client .
```

```
nitro-cli build-enclave --docker-uri vsock-sample-client --output-file vsock_sample_client.eif
```

2. Run the server inside the parent instance.

```
python3 vsock-sample.py server 5005
```

3. Configure the pool of memory and vCPUs (the `nitro-cli-config`
script can be used) and run the enclave using the built EIF.

```
// 2 vCPUs and 256 MiB memory
nitro-cli-config -t 2 -m 256
nitro-cli run-enclave --eif-path vsock_sample_client.eif --cpu-count 2 --memory 256 --debug-mode
```

4. The server should print __Hello, world!__.

```
python3 vsock-sample.py server 5005
Hello, world!
```

__Note__:
* The client application inside the enclave sends the message once and then exits thus the enclave shall terminate.

Now you can replace the client/server code with your own code.
