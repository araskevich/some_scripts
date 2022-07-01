##################################################################################
# Send 5 custom "100 Trying" SIP messages.                                       #
# Usage example: python3.6 udp_message_sender.py sip-outbound-proxy.example.com  #
##################################################################################

import socket
import sys
import time


def main(ip):
    BIND_IP = '10.0.0.1'
    BIND_PORT = 0
    UDP_IP = ip
    UDP_PORT = 9999
    MESSAGE = f'''SIP/2.0 100 Trying\r
Via: SIP/2.0/UDP 10.0.2.15:5060;branch=qwerty;rport=50498;received=10.0.2.15\r
To: <sip:11111111111@sip.example.com:5060;transport=UDP>\r
From: <sip:11111111111@sip.example.com:5060;transport=UDP>;tag=qwerty\r
Call-ID: qwerty\r
CSeq: 1 REGISTER\r
User-Agent: TEST {UDP_IP}
Content-Length: 0\r\n\r\n'''.encode('utf-8')

    # print(time.ctime(), "Will send custom \"100 Trying\" SIP message:")
    # print(MESSAGE.decode('utf-8'))

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(10)
        # s.bind((host, port))
        s.bind((BIND_IP, BIND_PORT))

        for i in range(1, 6):
            # print(time.ctime(), f"Sent message {i} times to {UDP_IP}:{UDP_PORT}")
            s.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            time.sleep(1)
        s.close()

    except Exception as e:
        print(time.ctime(), f"Test failed: Sent message {i} times to {UDP_IP}:{UDP_PORT}. Exception: {e}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("\nUsage example: python3.6 udp_message_sender.py sip-outbound-proxy.example.com \n")
        sys.exit(1)
    main(str(sys.argv[1]))
