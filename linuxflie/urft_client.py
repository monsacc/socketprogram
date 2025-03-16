import socket
import time
import sys  

if len(sys.argv) != 4:
    print("Usage: python urft_client.py <file_path> <server_ip> <server_port>")
    sys.exit(1)

filename = sys.argv[1]
server_ip = sys.argv[2]
server_port = int(sys.argv[3])

BUFFER_SIZE = 8192
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(0.5)

seq_num = 0
start_time = time.time()

print("เริ่มส่งไฟล์...")
with open(filename, "rb") as f:
    while True:
        data = f.read(BUFFER_SIZE - 10)  
        if not data:
            break

        packet = f"{seq_num}|".encode() + data  
        while True:
            client_socket.sendto(packet, (server_ip, server_port))
            print(f"Sent SEQ: {seq_num}")
            try:
                ack, _ = client_socket.recvfrom(BUFFER_SIZE)
                if ack.decode() == f"ACK {seq_num}":
                    print(f"ได้รับ ACK {seq_num}")
                    seq_num += 1
                    break  
            except socket.timeout:
                print(f"Timeout, resending packet {seq_num}...")

client_socket.sendto(f"{seq_num}|EOF".encode(), (server_ip, server_port))
end_time = time.time()

elapsed_time = end_time - start_time
print(f"File sent successfully! ใช้เวลา: {elapsed_time:.2f} วินาที")
