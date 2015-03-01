#!/bin/bash

# Description: Script for blocking particular websites using iptables.
# Author:      Maciej 'mc' Suchecki

if [ $# -ne 1 ]; then
  echo "Usage: $0 [address]"
  exit 1
fi

if [ `id -u` != 0 ]; then
  echo "This script must be run as root!" 1>&2
  exit 1
fi

echo "Blocking $1 website..."
iptables -A INPUT -s $1 -j DROP
iptables -A OUTPUT -s $1 -j DROP
iptables-save > /etc/iptables.conf

echo 'Done!'
exit 0
