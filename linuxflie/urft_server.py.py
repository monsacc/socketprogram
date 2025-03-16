import socket
import time

BUFFER_SIZE = 8192
server_ip = "127.0.0.1"
server_port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

print(f"Server listening on {server_ip}:{server_port}")

expected_seq = 0
start_time = time.time()

with open("received_file.bin", "wb") as f:
    while True:
        data, client_addr = server_socket.recvfrom(BUFFER_SIZE)

        seq_num = int.from_bytes(data[:4], "big")
        packet_data = data[4:]

        print(f"Received seq_num: {seq_num}")

        if seq_num == expected_seq:
            f.write(packet_data)  
            server_socket.sendto(seq_num.to_bytes(4, "big"), client_addr)
            expected_seq += 1
            print(f"ACK sent for seq_num: {seq_num}")

        elif seq_num < expected_seq:
            server_socket.sendto(seq_num.to_bytes(4, "big"), client_addr)
            print(f"Duplicate seq_num {seq_num} ignored. ACK sent.")

        if packet_data == b"EOF":  
            break

end_time = time.time()
elapsed_time = end_time - start_time
print(f"✅ File received successfully! ใช้เวลา: {elapsed_time:.2f} วินาที")
