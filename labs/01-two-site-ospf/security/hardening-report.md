# Hardening report - two-site-ospf

Apply `hardening-R1.txt` and `hardening-R2.txt` **after** the base configs in `..\configs\`. They only add security; addressing and routing stay the same.

| # | Control | Why | Verify |
|---|---|---|---|
| 1 | `security passwords min-length 10`, strong `enable secret`, local `admin` user | Stops weak/default passwords; per-user accountability | `show running-config \| include secret` |
| 2 | `service password-encryption` | Hides plain-text line passwords in the config | `show running-config` |
| 3 | `login block-for 120 attempts 3 within 60` | Slows brute-force login attempts | `show login` |
| 4 | SSH v2 (domain name + 2048-bit RSA key) and `transport input ssh` | Telnet sends passwords in clear text; SSH encrypts | `show ip ssh` -> version 2.0 |
| 5 | `MGMT-ONLY` ACL on vty (`access-class`) | Only the two LANs can reach remote management | `show access-lists MGMT-ONLY` |
| 6 | `exec-timeout 5 0` on console and vty | Idle sessions close automatically | wait 5 min idle |
| 7 | Timestamps + `logging buffered 16384` | Keeps a timed record of security events | `show logging` |
| 8 | OSPF MD5 authentication on G0/0/1 (both routers, same key) | Stops a rogue router injecting fake routes | `show ip ospf interface g0/0/1` -> "Message digest authentication enabled"; `show ip ospf neighbor` -> FULL |

## Order of operations
1. Paste `hardening-R1.txt` into R1, then **immediately** `hardening-R2.txt` into R2 (OSPF drops until both have the same key).
2. Check `show ip ospf neighbor` is FULL on both.
3. From PC-Sales: `ssh -l admin 192.168.10.1` (password `R1-Admin!2026`). It should work; Telnet should be refused.

## Still recommended (next steps)
- Switches S1/S2: shut unused ports, port security on PC ports, BPDU guard, change native VLAN, `switchport nonegotiate`.
- A syslog/NTP server so all devices log with the same time.
- Replace the example lab passwords before any real deployment.
