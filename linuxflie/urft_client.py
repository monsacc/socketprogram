import socket
import time
import sys  

BUFFER_SIZE = 8192

if len(sys.argv) != 4:
    print("Usage: python urft_client.py <file_path> <server_ip> <server_port>")
    sys.exit(1)

filename = sys.argv[1]
server_ip = sys.argv[2]
server_port = int(sys.argv[3])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(0.5)

seq_num = 0
start_time = time.time()

print("เริ่มส่งไฟล์...")
with open(filename, "rb") as f:
    while True:
        data = f.read(BUFFER_SIZE - 4)  
        if not data:
            break

        packet = seq_num.to_bytes(4, "big") + data  
        while True:
            client_socket.sendto(packet, (server_ip, server_port))
            print(f"Sent SEQ: {seq_num}")
            try:
                ack, _ = client_socket.recvfrom(4) 
                if int.from_bytes(ack, "big") == seq_num:
                    print(f"ได้รับ ACK {seq_num}")
                    seq_num += 1
                    break 
            except socket.timeout:
                print(f"Timeout, resending SEQ {seq_num}...")

client_socket.sendto(seq_num.to_bytes(4, "big") + b"EOF", (server_ip, server_port))  
end_time = time.time()

elapsed_time = end_time - start_time
print(f"File sent successfully! ⏱️ ใช้เวลา: {elapsed_time:.2f} วินาที")
