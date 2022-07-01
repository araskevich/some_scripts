crontab -u root -e

MAILTO=""
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

01 * * * * python3.6 /opt/trafficMonitor/trafficMonitor.py &> /opt/trafficMonitor/trafficMonitor.log
