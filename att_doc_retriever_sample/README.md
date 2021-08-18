# Attestation Document Retriever Sample

This is a sample application which retrieves an attestation document from an Enclave.
The attestation document is requested from the enclave using a Rust application which
is called by a python server for each incoming request from a python client that runs
on the parent instance.

## Build

Use the steps from https://docs.aws.amazon.com/enclaves/latest/user/getting-started.html to set up a parent instance that can run the generated enclave image.

Run the command below to build the docker image for the enclave.
`$ docker build -t att-doc-retriever-sample -f Dockerfile ..`

Generate the EIF using the command:
`$ nitro-cli build-enclave --docker-uri att-doc-retriever-sample --output-file att_doc_retriever_sample.eif`

## Run
Using the nitro tools, run the enclave providing the enclave image from the build step.
`$ nitro-cli run-enclave --cpu-count 2 --memory 512 --enclave-cid 16 --eif-path att_doc_retriever_sample.eif --debug-mode`

Start the client on parent instance(Note: 16 is the enclave CID)
`$ python3 py/att_doc_retriever_sample.py client 16 5010`

On the parent instance you should see the Attestation Document sent from the enclave
```
$ python3 py/att_doc_retriever_sample.py client 16 5010
Attestation { document: ...
```

