# network-security-labs

![Cisco Packet Tracer](https://img.shields.io/badge/Cisco-Packet%20Tracer%209.0-1BA0D7?logo=cisco&logoColor=white)
![CCNA](https://img.shields.io/badge/CCNA-in%20progress-0A66C2)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Cisco routing, switching and network security labs built in Packet Tracer. Each lab includes the topology, addressing plan, device configs, captured verification output and troubleshooting notes.

## Labs

| Lab | Description | Topics |
|-----|-------------|--------|
| [01-two-site-ospf](labs/01-two-site-ospf) | Two sites connected over a point-to-point link, routed with OSPF, then hardened | VLSM, OSPF area 0, DR/BDR, SSHv2, VTY ACL, login block-for, OSPF MD5 auth |
| [02-vlan-router-on-a-stick](labs/02-vlan-router-on-a-stick) | Two VLANs on one switch with inter-VLAN routing and DHCP on the router | VLANs, 802.1Q trunking, subinterfaces, DHCP pools |

## Repository layout

```
labs/
  <lab>/
    README.md          overview, addressing, design notes
    configs/           device configurations (paste into the CLI)
    security/          hardening configs (where applicable)
    outputs/           show / ping output captured from the running lab
    images/            topology screenshot
    *.pkt              Packet Tracer file (where included)
tools/
  vlsm.py              VLSM subnet calculator used for the addressing plans
```

## Tools

`tools/vlsm.py` allocates subnets largest-first from a base network and prints mask, wildcard, gateway and host range for each:

```
$ python tools/vlsm.py 192.168.10.0/24 Sales=50 IT=25 R1-R2=2
| Name  | Needed | Subnet           | Mask            | Wildcard  | Usable | Gateway       | Host range                    | Broadcast     |
| Sales | 50     | 192.168.10.0/26  | 255.255.255.192 | 0.0.0.63  | 62     | 192.168.10.1  | 192.168.10.2 - 192.168.10.62  | 192.168.10.63 |
| IT    | 25     | 192.168.10.64/27 | 255.255.255.224 | 0.0.0.31  | 30     | 192.168.10.65 | 192.168.10.66 - 192.168.10.94 | 192.168.10.95 |
| R1-R2 | 2      | 192.168.10.96/30 | 255.255.255.252 | 0.0.0.3   | 2      | 192.168.10.97 | 192.168.10.98 - 192.168.10.98 | 192.168.10.99 |
```

## Environment

- Cisco Packet Tracer 9.0
- Routers: ISR4331, switches: Catalyst 2960-24TT

Passwords in the configs are lab placeholders.

## Roadmap

- [ ] Switch security: port security, DHCP snooping, DAI, BPDU guard
- [ ] Standard and extended ACLs
- [ ] NAT/PAT to an ISP
- [ ] Multi-area OSPF
- [ ] Site-to-site VPN (GRE over IPsec)
