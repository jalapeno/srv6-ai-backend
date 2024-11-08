#!/bin/bash

sudo brctl addbr xrd-LF07-host1
sudo brctl addbr xrd-LF08-host1
sudo brctl addbr xrd-LF09-host1
sudo brctl addbr xrd-LF10-host1
sudo brctl addbr xrd-LF07-host2
sudo brctl addbr xrd-LF08-host2
sudo brctl addbr xrd-LF09-host2
sudo brctl addbr xrd-LF10-host2

sudo ip link set xrd-LF07-host1 up
sudo ip link set xrd-LF08-host1 up
sudo ip link set xrd-LF09-host1 up
sudo ip link set xrd-LF10-host1 up
sudo ip link set xrd-LF07-host2 up
sudo ip link set xrd-LF08-host2 up
sudo ip link set xrd-LF09-host2 up
sudo ip link set xrd-LF10-host2 up
