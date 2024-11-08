#! /bin/bash

sudo brctl addbr LF07-host
sudo brctl addbr LF08-host
sudo brctl addbr LF09-host
sudo brctl addbr LF10-host

sudo ip link set LF07-host up
sudo ip link set LF08-host up
sudo ip link set LF09-host up
sudo ip link set LF10-host up
