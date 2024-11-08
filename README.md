# srv6-ai-backend

1. Spin up topology
```
sudo containerlab deploy -t xrd-topo.yaml
```

or
```
sudo containerlab deploy -t sonic-topo.yaml
```

2. Check the status of the nodes
```
docker ps
```

3. spin up Trex
```
sudo containerlab deploy -t trex.yaml
```

4. verify BGP sessions, etc.
```
ssh cisco@clab-xrd-clos-LF09
show bgp ipv6 unicast summary
show bgp ipv6 unicast 
```

5. docker exec into a trex container and add a route with SRv6 encap 
```
docker exec -it clab-trex-ubtrex01 bash
ip -6 route add fc00:0:1000:4::/64 encap seg6 mode encap segs fc00:0:3:2:5:10:: dev eth1
```

6. start a ping
```
ping fc00:0:1000:4::1
```

7. open a second terminal and start a tcpdump on LF07
```
docker exec -it clab-xrd-clos-LF07 tcpdump -ni Gi0-0-0-2
```

8. follow the packet through the network
```
docker exec -it clab-xrd-clos-LF07 tcpdump -ni Gi0-0-0-0
docker exec -it clab-xrd-clos-SP03 tcpdump -ni Gi0-0-0-2
docker exec -it clab-xrd-clos-SP03 tcpdump -ni Gi0-0-0-1
etc.
```

9. docker exec into the second trex container and add a route with SRv6 encap 
```
docker exec -it clab-trex-ubtrex02 bash
ip addr add fc00:0:1000:4::/64 eth2
ip -6 route add fc00:0:1000:1::/64 encap seg6 mode encap segs fc00:0:10:5:2:3:: dev eth2
```

10. start a ping from trex01
```
ping fc00:0:1000:4::
```

11. run some tcpdumps
```
docker exec -it clab-xrd-clos-SP05 tcpdump -ni Gi0-0-0-1
docker exec -it clab-xrd-clos-SP03 tcpdump -ni Gi0-0-0-2
docker exec -it clab-xrd-clos-SP03 tcpdump -ni Gi0-0-0-1
```
