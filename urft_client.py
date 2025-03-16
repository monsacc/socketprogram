import socket
import time

with open("test_file.bin", "wb") as f:
    f.write(bytearray(1024 * 1024))  # 1MB ของข้อมูลว่าง

BUFFER_SIZE = 8192
server_ip = "127.0.0.1"
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(0.5)

filename = "test_file.bin"
seq_num = 0

start_time = time.time()  


print("📤 เริ่มส่งไฟล์...")
with open(filename, "rb") as f:
    while True:
        data = f.read(BUFFER_SIZE - 10)  # ลดขนาดให้เผื่อที่สำหรับ Sequence Number
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
                    break  # ส่งแพ็กเก็ตต่อไปได้
            except socket.timeout:
                print(f"Timeout, resending packet {seq_num}...")

client_socket.sendto(f"{seq_num}|EOF".encode(), (server_ip, server_port))  # ส่ง EOF แจ้งสิ้นสุด
end_time = time.time()  # ⏳ หยุดจับเวลา

elapsed_time = end_time - start_time
print(f"File sent successfully! ⏱️ ใช้เวลา: {elapsed_time:.2f} วินาที")
