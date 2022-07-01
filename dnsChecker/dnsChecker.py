import unittest
import subprocess
import argparse
import sys

#  cat DNS_test.txt 
#  >>>
#  name-1-example.com 10.0.0.10
#  name-2-example.com 10.0.0.11
#  <<<

A = {}

with open('DNS_test.txt', 'r') as f:
    for line in f:
        rr = line.rstrip("\n").split(" ")
        A.update({rr[0]:rr[1]})

print(A)

def parse_args(args):
    parser = argparse.ArgumentParser(description = 'DNS Records checker with IP pinger task.')
    parser.add_argument('-r', '--removed', dest = 'records', default = True, help = 'DNS Records shouldn\'t exist', action = 'store_false')
    parser.add_argument('-p', '--ping', dest = 'ping', default = False, help = 'Activate IP pinger task', action = 'store_true')
    return parser.parse_args()
		
parser = parse_args(sys.argv[1:])
records = parser.records
ping = parser.ping	


class TestStringMethods(unittest.TestCase):

    @unittest.skipIf(records == False, "skip if records shouldn't exist")
    def test_resolv_dns(self):
        for host_name, host_ip in A.items():
            with self.subTest(host_name = host_name, host_ip = host_ip):
                self.assertEqual(resolver_DNS(host_name, "8.8.8.8"), host_ip)

    @unittest.skipIf(records == False, "skip if records shouldn't exist")
    def test_resolv_prt(self):
        for host_name, host_ip in A.items():
            with self.subTest(host_name = host_name, host_ip = host_ip):
                self.assertEqual(resolver_PTR(host_ip, "8.8.8.8"), host_name + ".")

    @unittest.skipIf(ping == False, "skip if records shouldn't exist")  
    def test_ip_ping(self):
        for host_name, host_ip in A.items():
            with self.subTest(host_name = host_name, host_ip = host_ip):
                self.assertEqual(pinger(host_ip), 1)    

    @unittest.skipIf(records == False, "skip if records shouldn't exist")
    def test_resolv_dns_local(self):
        for host_name, host_ip in A.items():
            with self.subTest(host_name = host_name, host_ip = host_ip):
                self.assertEqual(resolver_DNS(host_name, "dns.example.com"), host_ip)

    @unittest.skipIf(records == False, "skip if records shouldn't exist")
    def test_resolv_prt_local(self):
        for host_name, host_ip in A.items():
            with self.subTest(host_name = host_name, host_ip = host_ip):
                self.assertEqual(resolver_PTR(host_ip, "dns.example.com"), host_name + ".")

    @unittest.skipIf(records == True, "skip if records should exist")
    def test_resolv_dns_del(self):
        for host_name, host_ip in A.items():
            with self.subTest(host_name = host_name, host_ip = host_ip):
                self.assertEqual(resolver_DNS(host_name, "8.8.8.8"), "NONE")

    @unittest.skipIf(records == True, "skip if records should exist")
    def test_resolv_prt_del(self):
        for host_name, host_ip in A.items():
            with self.subTest(host_name = host_name, host_ip = host_ip):
                self.assertEqual(resolver_PTR(host_ip, "8.8.8.8"), "NONE")

    @unittest.skipIf(records == True, "skip if records should exist")
    def test_resolv_dns_del_local(self):
        for host_name, host_ip in A.items():
            with self.subTest(host_name = host_name, host_ip = host_ip):
                self.assertEqual(resolver_DNS(host_name, "dns.example.com"), "NONE")

    @unittest.skipIf(records == True, "skip if records should exist")
    def test_resolv_prt_dela_local(self):
        for host_name, host_ip in A.items():
            with self.subTest(host_name = host_name, host_ip = host_ip):
                self.assertEqual(resolver_PTR(host_ip, "dns.example.com"), "NONE")


def pinger(host_ip):
    # return 1 if host don't have ping
    response = subprocess.getstatusoutput('ping -c 1 ' + host_ip)
    return response[0]


def resolver_DNS(host_name, dns):
    response = subprocess.getstatusoutput('dig  @' + dns  + ' A ' + host_name + ' +short')
    if response[1] == "":
        return "NONE"
    else:
        return response[1]


def resolver_PTR(host_ip, dns):
    response = subprocess.getstatusoutput('dig @' + dns + ' -x ' + host_ip + ' +short')
    if response[1] == "":
        return "NONE"
    else:
        return response[1]
      


if __name__ == '__main__':
    # unittest.main(verbosity=2)

    runner = unittest.TextTestRunner() 
    itersuite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods) 
    runner.run(itersuite) 
    
    print("Number of test cases:", itersuite.countTestCases())




