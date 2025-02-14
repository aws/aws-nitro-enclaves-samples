package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"path/filepath"

	"github.com/linuxkit/virtsock/pkg/vsock"
)

func main() {
	var showVersion bool
	flag.BoolVar(&showVersion, "version", false, "Prints version information.")

	clientCmd := flag.NewFlagSet("client", flag.ExitOnError)
	cCid := clientCmd.Int("cid", 3, "The remote endpoint CID.")
	cPort := clientCmd.Int("port", 5005, "The remote endpoint port.")

	serverCmd := flag.NewFlagSet("server", flag.ExitOnError)
	sPort := serverCmd.Uint("port", 5005, "The local port to listen on.")

	switch os.Args[1] {
	case "client":
		clientCmd.Parse(os.Args[2:])
		fmt.Printf("CID:\t%d\nPort:\t%d\n", *cCid, *cPort)

		conn, err := vsock.Dial(uint32(*cCid), uint32(*cPort))
		if err != nil {
			log.Fatalf("failed to connect: %v", err)
		}
		defer conn.Close()

		message := "Hello, world!"
		w := bufio.NewWriter(conn)
		n, merr := w.WriteString(message)
		if merr != nil {
			log.Fatalf("failed to write message: %v", merr)
		}
		w.Flush()
		fmt.Printf("Wrote %d bytes to connection: %s\n", n, message)

	case "server":
		serverCmd.Parse(os.Args[2:])

		lis, err := vsock.Listen(vsock.CIDAny, uint32(*sPort))
		if err != nil {
			log.Fatalf("failed to listen: %v", err)
		}
		defer lis.Close()
		fmt.Printf("Listening on :%d\n", *sPort)
		for {
			conn, err := lis.Accept()
			if err != nil {
				fmt.Println("Error accepting", err.Error())
				os.Exit(1)
			}
			defer conn.Close()

			go func(c net.Conn) {
				r := bufio.NewReader(c)
				data, err := r.ReadString('\n')
				if err != nil && err != io.EOF {
					log.Println("[ERROR]: couldn't read from connection:", err.Error())
					return
				}
				log.Printf("[INFO]: %s\n", data)
			}(conn)
		}

	default:
		flag.Parse()

		if showVersion {
			fmt.Printf("%s 0.1.0\n", filepath.Base(os.Args[0]))
			os.Exit(0)
		}
	}

}
