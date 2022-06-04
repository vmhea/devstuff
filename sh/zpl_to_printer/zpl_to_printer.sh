#!/bin/bash

# zpl_to_printer.sh
# =============================================
# Version:
#     v1.0 (5/10/2022)
#
# Author:
#     Heath Vernet (hvernet93@gmail.com)
#
# Description:
#     Send ZPL file to a list of IP addresses and port range.
#
# Notes:
#     - ZPL documentation: https://support.zebra.com/cpws/docs/zpl/zpl_manual.pdf
#     - Seperate IP addresses with \n.
#
# Issues:
#     - No port checking to verify if a service is running.
#
# Usage:
#     *optional args
#     zpl_to_printer.sh [zpl_file] [ip_list] *[port_start] *[port_end] *[delay] *[log_file]
#
# Defaults:
#     port_start  <5964>
#     port_end    <5966>
#     delay       <60>
#     log_file    <zpl_to_printer.log>

zpl_file=$1
ip_list=$2
port_start=${3:-"5964"}
port_end=${4:-"5966"}
delay=${5:-"60"}
log_file=${6:-"zpl_to_printer.log"}

if [[ -z "$1" || -z "$2" ]]; then
    echo "[ERROR] Invalid input"
    echo "Required arguments: [zpl_file] [ip_list]"
    exit
fi

date +"%d-%m-%Y %r" >> $log_file
echo "Script started" | tee -a $log_file

for ip in $(cat $ip_list); do
    if (ping -c 1 -w 3 $ip > /dev/null); then
        echo "[INFO] $ip is online" | tee -a $log_file
        for ((p=$port_start-1; p<$port_end+1; p++)); do
            cat $zpl_file | netcat -w 1 $ip $p
        done
        echo "[INFO] $ip commands sent" | tee -a $log_file
        ((i++))
        if [ $i -eq 7 ]; then
            echo "[INFO] Sleeping $delay seconds"
            sleep $delay
            i=0
        fi
    else
        echo "[WARNING] $ip is unreachable" | tee -a $log_file
        echo "[WARNING] $ip skipped" | tee -a $log_file
    fi
done

echo "Script finished" | tee -a $log_file
echo "===========================================" >> $log_file
echo "Output saved to $log_file"
