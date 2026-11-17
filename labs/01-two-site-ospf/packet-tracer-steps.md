# Packet Tracer steps

## 1. Devices to add
- 2 x ISR4331 routers: **R1**, **R2**
- 2 x 2960 switches: **S1**, **S2**
- 2 x PCs: **PC-Sales** (next to S1), **PC-IT** (next to S2)

## 2. Cables (in this order)
| From | To | Cable |
|---|---|---|
| R1 G0/0/0 | S1 G0/1 | Copper Straight-Through |
| R2 G0/0/0 | S2 G0/1 | Copper Straight-Through |
| R1 G0/0/1 | R2 G0/0/1 | Copper Cross-Over (straight-through also works: ISR4331 is auto-MDIX) |
| PC-Sales Fa0 | S1 Fa0/1 | Copper Straight-Through |
| PC-IT Fa0 | S2 Fa0/1 | Copper Straight-Through |

The switches need no configuration for this lab (all ports are in VLAN 1 by default).

## 3. Configure the routers
Open each router > **CLI** tab, press Enter, and paste `configs\R1.txt` / `configs\R2.txt`.

## 4. Configure the PCs (Desktop > IP Configuration > Static)
| PC | IP address | Subnet mask | Default gateway |
|---|---|---|---|
| PC-Sales | 192.168.10.2 | 255.255.255.192 | 192.168.10.1 |
| PC-IT | 192.168.10.66 | 255.255.255.224 | 192.168.10.65 |

## 5. Test
See `verify.md`. OSPF takes about 30-40 seconds to come up after both routers are configured.
