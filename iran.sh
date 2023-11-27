#!/bin/bash

read -p "Auto setup from IP system ? (Y/yes or N/no )"  auto_ip




if [ ${auto_ip^^} == "Y" ] || [ ${auto_ip^^} == "YES" ];then 
      interface=$( ip link | grep -oP "en.*(?=:)")
      ip=$( ip address show $interface | grep -oP "inet \K.*(?=/)")

      cd  /etc/openvpn/server
      sed  -i "s/\(local\).*[0-9]/\1 $ip/" servertcp.conf
      sed  -i "s/\(local\).*[0-9]/\1 $ip/" server.conf
      cd /etc/firewalld/
      sed  -i "s/\(--to \).*[0-9]/\1 $ip/" direct.xml
      cd /etc/radcli
      sed  -i "s/\(^authserver \).*/\1 127.0.0.1/" radiusclient.conf
      echo "OK"
elif [ ${auto_ip^^} == "N" ] || [ ${auto_ip^^} == "NO" ]; then
      read -p "IP address ? :" ip_s
      cd  /etc/openvpn/server
      sed -i "s/\(local\).*[0-9]/\1 $ip_s/" servertcp.conf
      sed -i "s/\(local\).*[0-9]/\1 $ip_s/" server.conf
      cd /etc/firewalld/
      sed  -i "s/\(--to \).*[0-9]/\1 $ip_s/" direct.xml
      cd /etc/radcli
      sed  -i "s/\(^authserver \).*/\1 127.0.0.1/" radiusclient.conf
      echo "OK"
else 
      echo "آقای هاشمی ؟"
fi
