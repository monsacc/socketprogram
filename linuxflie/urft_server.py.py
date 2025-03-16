import socket
import time
import sys  

BUFFER_SIZE = 8192

if len(sys.argv) != 3:
    print("Usage: python3 urft_server.py <server_ip> <server_port>")
    sys.exit(1)

server_ip = sys.argv[1]
server_port = int(sys.argv[2])

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

        print(f"📥 Received SEQ: {seq_num}")

        if seq_num == expected_seq:
            if packet_data == b"EOF":
                break  
            f.write(packet_data)  
            server_socket.sendto(seq_num.to_bytes(4, "big"), client_addr)
            expected_seq += 1
            print(f"✅ ACK sent for SEQ: {seq_num}")

        elif seq_num < expected_seq:
            server_socket.sendto(seq_num.to_bytes(4, "big"), client_addr)
            print(f"🔁 Duplicate SEQ {seq_num} ignored. ACK sent.")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"✅ File received successfully! ⏱️ ใช้เวลา: {elapsed_time:.2f} วินาที")
