#!/bin/bash

sudo ip link set sonic-LF07-host1 down
sudo ip link set sonic-LF08-host1 down
sudo ip link set sonic-LF09-host1 down
sudo ip link set sonic-LF10-host1 down
sudo ip link set sonic-LF07-host2 down
sudo ip link set sonic-LF08-host2 down
sudo ip link set sonic-LF09-host2 down
sudo ip link set sonic-LF10-host2 down

sudo brctl delbr sonic-LF07-host1
sudo brctl delbr sonic-LF08-host1
sudo brctl delbr sonic-LF09-host1
sudo brctl delbr sonic-LF10-host1
sudo brctl delbr sonic-LF07-host2
sudo brctl delbr sonic-LF08-host2
sudo brctl delbr sonic-LF09-host2
sudo brctl delbr sonic-LF10-host2
