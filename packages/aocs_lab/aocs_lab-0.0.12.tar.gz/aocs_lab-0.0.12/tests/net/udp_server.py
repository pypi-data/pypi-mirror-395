import socket

def start_udp_server(host='0.0.0.0', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"UDP server started on {host}:{port}")

        while True:
            message, client_address = server_socket.recvfrom(1024)
            print(f"Received message from {client_address}: {message.hex()}")

if __name__ == "__main__":
    start_udp_server()
