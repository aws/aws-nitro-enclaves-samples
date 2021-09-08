use nsm_io::Request;
use serde_bytes::ByteBuf;

fn main() {
    let nsm_fd = nsm_driver::nsm_init();

    let public_key = ByteBuf::from("my super secret key");
    let hello = ByteBuf::from("hello, world!");

    let request = Request::Attestation {
        public_key: Some(public_key),
        user_data: Some(hello),
        nonce: None,
    };

    let response = nsm_driver::nsm_process_request(nsm_fd, request);
    println!("{:?}", response);

    nsm_driver::nsm_exit(nsm_fd);
}
