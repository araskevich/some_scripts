import requests
import sys
import subprocess
import asyncio
import threading
import time

# python36 "PRO/STAGE" "HOST" 

HOSTS = sys.argv[2]
dict_host = {}

if sys.argv[1] == "PRO":
    link = ("http://pro.example.com/interfaces-search/?q=host_name~(%s)&fields=host_name,ip,name&format=json" %HOSTS)
if sys.argv[1] == "STAGE":
    link = ("http://stage.example.com/interfaces-search/?q=host_name~(%s)&fields=host_name,ip,name&format=json" %HOSTS)

r = requests.get(link)
for i in range(len(r.json())):
    if r.json()[i]["name"] == "nic0":
        # print(r.json()[i]["host_name"]) # env01-stage-componentOne01
        # print(r.json()[i]["name"])      # nic0
        # print(r.json()[i]["ip"])        # 10.0.0.10

        host_name = r.json()[i]["host_name"]
        host_ip = r.json()[i]["ip"]
        # print(host_name, "ansible_host=" +  host_ip)
        dict_host.update({host_name: host_ip})

print(dict_host)

dict_val = {}

## red
CRED = '\033[91m'
## green
CGREEN = '\033[92m'
## null
CEND = '\033[0m'

async def printData():
    while True:
        print(time.ctime(), "Doing the print thing")
        if dict_val != {}:
            print(time.ctime(),'confirm non empty dictionary')
            wait = 25
            for key, value in dict_val.items():
                if value == "UP":
                    print(key, CGREEN, value, CEND)
                elif value == "DOWN":
                    print(key, CRED, value, CEND)
                else:
                    print(key, value)
        else:
            print(time.ctime(), 'confirm empty dictionary')
            wait = 5
        await asyncio.sleep(wait)


async def pingJob():
    while True:
        print(time.ctime(), "Doing the ping thing")
        try:
            for host_name, host_ip in dict_host.items():
                print(time.ctime(), "start_thread: ", host_name, host_ip)
                w = threading.Thread(target = pinger, args = (host_name, host_ip))
                w.start()
        except RuntimeError:
            print(time.ctime(), "Oops! RuntimeError: looks like dictionary changed size during iteration")
        finally:
            print(time.ctime(), "Pinger job sleeping 25 sec")
            await asyncio.sleep(25)


def pinger(host_name, host_ip):
    response = subprocess.getstatusoutput('ping -c 1 ' + host_ip)
    if response[0] == 0:
        dict_val.update({host_name: "UP"})
    else:
        dict_val.update({host_name: "DOWN"})
    

loop = asyncio.get_event_loop()
loop.create_task(pingJob())
loop.create_task(printData())
loop.run_forever()


# ioloop = asyncio.get_event_loop()
# tasks = [ioloop.create_task(pingJob()), ioloop.create_task(printData())]
# wait_tasks = asyncio.wait(tasks)
# ioloop.run_until_complete(wait_tasks)
# ioloop.close()

