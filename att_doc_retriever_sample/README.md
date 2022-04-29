# Attestation Document Retriever Sample

This is a sample application which retrieves an attestation document from a Nitro enclave.
The attestation document is requested using a Rust application which is called by a Python server,
both running inside the enclave. A corresponding Python client runs on the parent instance and
makes requests to the enclave server through vsock.

## Build

Use the steps from https://docs.aws.amazon.com/enclaves/latest/user/getting-started.html to set up a parent instance that can run a Nitro enclave using the generated enclave image described below.

Run the command below to build the Docker image for the enclave.

__Note__: The platform's architecture must be provided in order to select the correct Rust toolchain.
```
docker build -t att-doc-retriever-sample -f Dockerfile --build-arg ARCH=$(uname -m) ..
```

Generate the enclave image (EIF) using the command:
```
nitro-cli build-enclave --docker-uri att-doc-retriever-sample --output-file att_doc_retriever_sample.eif
```

## Configure

Ensure the `nitro_enclaves` driver is inserted. Configure the vCPUs and the memory pool.

__Note__: The `nitro-cli-config` script from https://github.com/aws/aws-nitro-enclaves-cli may be used here.
```
// 2 vCPUs and 512 MiB of memory
nitro-cli-config -t 2 -m 512
```

## Run
Using the Nitro tools, run the enclave providing the previously-built enclave image.
```
nitro-cli run-enclave --cpu-count 2 --memory 512 --enclave-cid 16 --eif-path att_doc_retriever_sample.eif --debug-mode
```

Start the client on the parent instance.

__Note__: Here, 16 represents the enclave's CID and 5010 is the vsock port.
```
python3 py/att_doc_retriever_sample.py client 16 5010
```

On the parent instance you should now see the Attestation Document sent from the enclave.
```
python3 py/att_doc_retriever_sample.py client 16 5010
Attestation { document: ...
```

