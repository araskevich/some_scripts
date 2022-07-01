[componentOne ~]$ sudo chown zabbix:zabbix /etc/zabbix/scripts/dns_vip_discovery.sh
[componentOne ~]$ sudo chmod 774 /etc/zabbix/scripts/dns_vip_discovery.sh
[componentOne ~]$ sudo ls -l /etc/zabbix/scripts/dns_vip_discovery.sh

Update /etc/zabbix/zabbix_agentd.d/zabbix_agentd_custom.conf

UserParameter=dns_vip.script,[ -f /etc/zabbix/scripts/dns_vip_discovery.sh ] && echo 1 || echo 0
UserParameter=dns_vip.check_api[*],/etc/zabbix/scripts/dns_vip_discovery.sh $1 $2
UserParameter=dns_vip.discovery_vip[*],/etc/zabbix/scripts/dns_vip_discovery.sh $1 $2
UserParameter=dns_vip.check_vip[*],/etc/zabbix/scripts/dns_vip_discovery.sh $1 $2

example of usage for componentOne:

dns_vip.check_api["check_api","componentOne"]
dns_vip.discovery_vip["discovery_vip","componentOne"]
dns_vip.check_vip["check_vip","<$ip>"]

[componentOne ~]$ sudo /etc/zabbix/scripts/dns_vip_discovery.sh discovery_vip componentOne | jq .
{
  "data": [
    {
      "{#IP}": "192.168.1.10"
    },
    {
      "{#IP}": "192.168.1.11"
    },
    {
      "{#IP}": "192.168.1.12"
    },
    {
      "{#IP}": "192.168.1.13"
    }
  ]
}
[componentOne ~]$ sudo /etc/zabbix/scripts/dns_vip_discovery.sh check_api componentOne | jq .
1
[componentOne ~]$ sudo /etc/zabbix/scripts/dns_vip_discovery.sh check_vip 192.168.1.10 | jq .
1