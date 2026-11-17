# Verify the lab

## On R1 and R2
```
show ip interface brief
```
G0/0/0 and G0/0/1 should be **up / up** with the IPs from the addressing plan.

```
show ip ospf neighbor
```
- On R1: one neighbor, Neighbor ID **2.2.2.2**, state **FULL**, address 192.168.10.98
- On R2: one neighbor, Neighbor ID **1.1.1.1**, state **FULL**, address 192.168.10.97

```
show ip route
```
Expected on **R1**:
```
C    192.168.10.0/26 is directly connected, GigabitEthernet0/0/0
C    192.168.10.96/30 is directly connected, GigabitEthernet0/0/1
O    192.168.10.64/27 [110/2] via 192.168.10.98, GigabitEthernet0/0/1
```
Expected on **R2**:
```
C    192.168.10.64/27 is directly connected, GigabitEthernet0/0/0
C    192.168.10.96/30 is directly connected, GigabitEthernet0/0/1
O    192.168.10.0/26 [110/2] via 192.168.10.97, GigabitEthernet0/0/1
```
(`L` local /32 routes also appear; that is normal.)

## From the PCs (Desktop > Command Prompt)
```
PC-Sales> ping 192.168.10.66
PC-Sales> tracert 192.168.10.66
```
The ping should succeed (the first reply may time out while ARP resolves). `tracert` should show 192.168.10.1, then 192.168.10.98, then 192.168.10.66.

## If it does not work
- Interface down: check the cable and that `no shutdown` was applied.
- No OSPF neighbor: make sure G0/0/1 is **not** passive (`show ip protocols`) and both ends are in 192.168.10.96/30.
- PC cannot ping its gateway: check the PC's IP, mask and default gateway.
