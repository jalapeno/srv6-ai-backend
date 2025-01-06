### Next steps
* Centralize the FLB app
* Use Ansible to push FLB computed routes into hosts
* `Enhance Jalapeño to support BGP only fabrics (no IGP) - complete 12/28/2024%`
* `Populate Graph DB with telemetry stats for fabric bandwidth management - complete 1/05/2025`
* `Develop GUI for FLB app to visualize pinning of flows to fabric paths - complete 1/05/2025`
* Programatically collect GPU / Training jobs endpoints and map it into Graph DB


### Notes:
FLB app (flow load balancer)
* Currently runs on individual hosts
* Computes and installs Linux/VPP route entry with SID list (SRv6)

### Jalapeno components
* BMP into Graph DB
* Kafka
* Graph DB (topology model)
* InfluxDB
* Telegraf
* Grafana