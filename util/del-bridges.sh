#! /bin/bash

sudo ip link set LF07-host down
sudo ip link set LF08-host down
sudo ip link set LF09-host down
sudo ip link set LF10-host down

sudo brctl delbr LF07-host
sudo brctl delbr LF08-host
sudo brctl delbr LF09-host
sudo brctl delbr LF10-host
