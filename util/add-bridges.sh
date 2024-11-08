#!/bin/bash

sudo brctl addbr LF07-host1
sudo brctl addbr LF08-host1
sudo brctl addbr LF09-host1
sudo brctl addbr LF10-host1
sudo brctl addbr LF07-host2
sudo brctl addbr LF08-host2
sudo brctl addbr LF09-host2
sudo brctl addbr LF10-host2

sudo ip link set LF07-host1 up
sudo ip link set LF08-host1 up
sudo ip link set LF09-host1 up
sudo ip link set LF10-host1 up
sudo ip link set LF07-host2 up
sudo ip link set LF08-host2 up
sudo ip link set LF09-host2 up
sudo ip link set LF10-host2 up
