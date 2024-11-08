#!/bin/bash

sudo ip link set LF07-host1 down
sudo ip link set LF08-host1 down
sudo ip link set LF09-host1 down
sudo ip link set LF10-host1 down
sudo ip link set LF07-host2 down
sudo ip link set LF08-host2 down
sudo ip link set LF09-host2 down
sudo ip link set LF10-host2 down

sudo brctl delbr LF07-host1
sudo brctl delbr LF08-host1
sudo brctl delbr LF09-host1
sudo brctl delbr LF10-host1
sudo brctl delbr LF07-host2
sudo brctl delbr LF08-host2
sudo brctl delbr LF09-host2
sudo brctl delbr LF10-host2
