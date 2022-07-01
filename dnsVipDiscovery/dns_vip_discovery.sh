#!/bin/bash

case $1 in
    check_api)
       case $2 in
            componentOne)
                api_test=( $(timeout 3 curl -s "http://localhost:5000/v1/configuration" 2>/dev/null | jq -r '.vips |. as $object | keys[] | select($object[.].description | contains("media") or contains("SIP/WSS"))' 2>/dev/null))
                ;;
            componentTwo)
                api_test=( $(timeout 3 curl -s "http://localhost:5000/v1/configuration" 2>/dev/null | jq -r '.vips[].ip' 2>/dev/null))
                ;;
            *)
                echo "Wrong command, need argument (componentOne|componentTwo)"
                exit 1
                ;;
        esac

        if [ "$api_test" = "" ]; then
            echo -n 0
        else
            echo -n 1
        fi
        ;;

    discovery_vip)
        case $2 in
            componentOne)
                ip_list=( $(timeout 3 curl -s "http://localhost:5000/v1/configuration" 2>/dev/null | jq -r '.vips |. as $object | keys[] | select($object[.].description | contains("media") or contains("SIP/WSS"))' 2>/dev/null))
                ;;
            componentTwo)
                ip_list=( $(timeout 3 curl -s "http://localhost:5000/v1/configuration" 2>/dev/null | jq -r '.vips[].ip' 2>/dev/null))
                ;;
            *)
                echo "Wrong command, need argument (componentOne|componentTwo)"
                exit 1
                ;;
        esac

        ip_list_len=${#ip_list[@]}

        echo -n "{"
        echo -n "\"data\":["

        for (( i=0; i<$ip_list_len; i++ ))
        do
            echo -n {\"{#IP}\": \"${ip_list[$i]}\"}

            if [ "$(($i+1))" -ne "$ip_list_len" ]; then
                echo -n  ","
            fi
        done

            echo -n "]"
            echo -n "}"
        ;;

    check_vip)
        vip_ip=$2
        dns_a=$(timeout 3 host $vip_ip 2>/dev/null | tail -n 1 | grep 'domain name pointer' | awk '{print $5}' 2>/dev/null)
        dns_ptr=$(timeout 3 host $dns_a 2>/dev/null | tail -n 1 | grep 'has address' | awk '{print $4}' 2>/dev/null)

        if [ "$vip_ip" = "$dns_ptr" ]; then
            echo -n 1
        else
            echo -n 0
        fi
        ;;
			
   *)
       echo "Wrong command, need argument (check_api|discovery_vip|check_vip)"
       exit 1
       ;;
esac
