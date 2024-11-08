#!/bin/bash

sudo brctl addbr sonic-LF07-host1
sudo brctl addbr sonic-LF08-host1
sudo brctl addbr sonic-LF09-host1
sudo brctl addbr sonic-LF10-host1
sudo brctl addbr sonic-LF07-host2
sudo brctl addbr sonic-LF08-host2
sudo brctl addbr sonic-LF09-host2
sudo brctl addbr sonic-LF10-host2

sudo ip link set sonic-LF07-host1 up
sudo ip link set sonic-LF08-host1 up
sudo ip link set sonic-LF09-host1 up
sudo ip link set sonic-LF10-host1 up
sudo ip link set sonic-LF07-host2 up
sudo ip link set sonic-LF08-host2 up
sudo ip link set sonic-LF09-host2 up
sudo ip link set sonic-LF10-host2 up
