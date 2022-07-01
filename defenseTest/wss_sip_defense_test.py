############################################################################################################
# continue to sent message until componentOne stop respond to you or you sent 1000 message to componentOne # 
# usage example: python3.6 wss_sip_defense_test.py sip-outbound-proxy.example.com                          #
############################################################################################################

import websocket
import ssl
import sys
import time

if len(sys.argv) != 2:
    print("\nUsage example: python3.6 wss_sip_defense_test.py sip-outbound-proxy.example.com\n")
    sys.exit(1)

DST_IP = str(sys.argv[1])
Timeout = 10
Connected = False
Recv_buffer = []

message = b'''REGISTER sip:sip.example.com SIP/2.0\r
Via: SIP/2.0/WSS qwerty;branch=qwerty\r
Max-Forwards: 70\r
To: <sip:11111111111@sip.example.com>\r
From: <sip:11111111111@sip.example.com>;tag=qwerty\r
Call-ID: qwerty\r
CSeq: 1 REGISTER\r
Contact: <sip:qwerty@qwerty;transport=ws>;expires=600\r
Allow: ACK,CANCEL,INVITE,MESSAGE,BYE,OPTIONS,INFO,NOTIFY,REFER\r
Supported: path, gruu, outbound\r
User-Agent: sip_defense_test\r
Content-Length: 0\r\n\r\n'''

try:
    print(time.ctime(), f"Connecting to wss://{DST_IP}:9999/.")
    ws = websocket.create_connection("wss://" + DST_IP + ":9999/",Timeout , header=["Sec-WebSocket-Protocol: sip"], sslopt={"cert_reqs": ssl.CERT_NONE})
    Connected = True
    print(time.ctime(), f"Connected to wss://{DST_IP}:9999/.")

    print(time.ctime(), f"Going to send message to {DST_IP}: \n", message.decode('utf-8'))

    for i in range(1, 1001):
        ws.send(message)
        print(time.ctime(), f"Sent message {i} times to {DST_IP}. Please wait some response from componentOne.")      
        # print(time.ctime(), f"Received message {i} times from componentOne.", ws.recv())
        Recv_buffer.append(ws.recv())

    ws.close()
    print(time.ctime(), f"Test failed: Sent message {i} times to {DST_IP}. Your WSS endpoint not blacklisted on componentOne.")

except Exception as e:
    if Connected == True:
        print(time.ctime(), f"Test passed: Sent message {i} times to {DST_IP}. Your WSS endpoint blacklisted on componentOne.")
    else:
        print(time.ctime(), f"Test failed:", e)
finally:
    if Connected == True:
        print(time.ctime(), "Last two messages from componentOne: \n",  Recv_buffer[len(Recv_buffer)-2], "\n", Recv_buffer[len(Recv_buffer)-1])
