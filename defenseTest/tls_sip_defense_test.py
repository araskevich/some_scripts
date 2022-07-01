############################################################################################################
# continue to sent message until componentOne stop respond to you or you sent 1000 message to componentOne #
# usage example: python3.6 tls_sip_defense_test.py sip-outbound-proxy.example.com                          #
############################################################################################################

import socket
import ssl
import sys
import time

if len(sys.argv) != 2:
    print("\nUsage example: python3.6 tls_sip_defense_test.py sip-outbound-proxy.example.com\n")
    sys.exit(1)

DST_IP = str(sys.argv[1])
DST_PORT = 9999 
Connected = False
Recv_buffer = []

message = b'''REGISTER sip:sip.example.com:5060;transport=TLS SIP/2.0\r
Via: SIP/2.0/TLS 10.0.2.15:5060;branch=qwerty;rport\r
Max-Forwards: 70\r
Contact: <sip:11111111111@10.0.2.15:5060;rinstance=qwerty;transport=tls>\r
To: <sip:11111111111@sip.example.com:5060;transport=TLS>\r
From: <sip:11111111111@sip.example.com:5060;transport=TLS>;tag=qwerty\r
Call-ID: qwerty\r
CSeq: 1 REGISTER\r
Expires: 3600\r
User-Agent: sip_defense_test\r
Allow-Events: presence, kpml, talk\r
Content-Length: 0\r\n\r\n'''


try:                
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)

    # ssl.wrap_socket(sock, keyfile=None, certfile=None, server_side=False, cert_reqs=CERT_NONE, ssl_version=PROTOCOL_TLS, 
    #     ca_certs=None, do_handshake_on_connect=True, suppress_ragged_eofs=True, ciphers=None)

    wrappedSocket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1)

    print(time.ctime(), f"Connecting using TLS to {DST_IP}:{DST_PORT}")
    wrappedSocket.connect((DST_IP, DST_PORT))
    Connected = True
    print(time.ctime(), f"Connected using TLS to {DST_IP}:{DST_PORT}")

    print(time.ctime(), f"Going to send message to {DST_IP}: \n", message.decode('utf-8'))

    for i in range(1, 1001): 
        wrappedSocket.send(message)
        print(time.ctime(), f"Sent message {i} times to {DST_IP}. Please wait some response from componentOne.")
        # print(time.ctime(), f"Received message {i} times from componentOne.", s.recv(1024).decode('utf-8')) 
        Recv_buffer.append(wrappedSocket.recv(1024).decode('utf-8'))

    wrappedSocket.close()
    print(time.ctime(), f"Test failed: Sent message {i} times to {DST_IP}. Your TLS endpoint not blacklisted on componentOne.")

except Exception as e:
    if Connected == True:
        print(time.ctime(), f"Test passed: Sent message {i} times to {DST_IP}. Your TLS endpoint blacklisted on componentOne.")
    else:
        print(time.ctime(), f"Test failed:", e)

finally:
    if Connected == True:
        print(time.ctime(), "Last two messages from componentOne: \n",  Recv_buffer[len(Recv_buffer)-2], "\n", Recv_buffer[len(Recv_buffer)-1]) 
