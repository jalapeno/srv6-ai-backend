#! /bin/bash

sudo ip link set xrd-LF07-host1 down
sudo ip link set xrd-LF08-host1 down
sudo ip link set xrd-LF09-host1 down
sudo ip link set xrd-LF10-host1 down
sudo ip link set xrd-LF07-host2 down
sudo ip link set xrd-LF08-host2 down
sudo ip link set xrd-LF09-host2 down
sudo ip link set xrd-LF10-host2 down

sudo brctl delbr xrd-LF07-host1
sudo brctl delbr xrd-LF08-host1
sudo brctl delbr xrd-LF09-host1
sudo brctl delbr xrd-LF10-host1
sudo brctl delbr xrd-LF07-host2
sudo brctl delbr xrd-LF08-host2
sudo brctl delbr xrd-LF09-host2
sudo brctl delbr xrd-LF10-host2
