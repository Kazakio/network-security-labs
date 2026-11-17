#!/usr/bin/env python3
"""VLSM / subnet planner for the network-engineer skill.

Usage examples:
  python vlsm.py 192.168.10.0/24 "Sales=50" "IT=25" "Guests=10" "R1-R2=2"
  python vlsm.py 10.0.0.0/16 Office=200 Lab=100 --csv plan.csv --md plan.md

Each argument NAME=HOSTS asks for a subnet with at least HOSTS usable hosts.
Subnets are allocated largest-first (standard VLSM) from the base network.
The first usable address is suggested as the gateway.
"""
import argparse
import csv
import ipaddress
import math
import sys


def prefix_for_hosts(hosts: int) -> int:
    if hosts <= 0:
        raise ValueError("host count must be positive")
    if hosts <= 2:
        # /30 gives 2 usable hosts (classic point-to-point link)
        return 30
    bits = math.ceil(math.log2(hosts + 2))
    return 32 - bits


def plan(base: str, requests):
    net = ipaddress.ip_network(base, strict=False)
    reqs = sorted(requests, key=lambda r: r[1], reverse=True)
    cursor = int(net.network_address)
    end = int(net.broadcast_address)
    rows = []
    for name, hosts in reqs:
        pfx = prefix_for_hosts(hosts)
        size = 2 ** (32 - pfx)
        # align cursor to the subnet size
        if cursor % size:
            cursor += size - (cursor % size)
        if cursor + size - 1 > end:
            raise SystemExit(f"ERROR: not enough space in {net} for '{name}' ({hosts} hosts, /{pfx}).")
        sub = ipaddress.ip_network(f"{ipaddress.ip_address(cursor)}/{pfx}")
        hosts_list = list(sub.hosts())
        rows.append({
            "name": name,
            "needed_hosts": hosts,
            "subnet": str(sub),
            "mask": str(sub.netmask),
            "wildcard": str(sub.hostmask),
            "usable_hosts": len(hosts_list),
            "gateway": str(hosts_list[0]),
            "first_host": str(hosts_list[1]) if len(hosts_list) > 1 else str(hosts_list[0]),
            "last_host": str(hosts_list[-1]),
            "broadcast": str(sub.broadcast_address),
        })
        cursor += size
    free = ipaddress.ip_address(cursor) if cursor <= end else None
    return net, rows, free


def to_markdown(net, rows, free):
    head = "| Name | Needed | Subnet | Mask | Wildcard | Usable | Gateway | Host range | Broadcast |\n"
    head += "|---|---|---|---|---|---|---|---|---|\n"
    body = "".join(
        f"| {r['name']} | {r['needed_hosts']} | {r['subnet']} | {r['mask']} | {r['wildcard']} | "
        f"{r['usable_hosts']} | {r['gateway']} | {r['first_host']} - {r['last_host']} | {r['broadcast']} |\n"
        for r in rows
    )
    tail = f"\nBase network: {net}. " + (f"Next free address: {free}." if free else "Base network fully used.")
    return head + body + tail + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base", help="base network, e.g. 192.168.1.0/24")
    ap.add_argument("subnets", nargs="+", help="NAME=HOSTS entries")
    ap.add_argument("--csv", help="write the plan to this CSV file")
    ap.add_argument("--md", help="write the plan to this Markdown file")
    a = ap.parse_args()
    reqs = []
    for item in a.subnets:
        if "=" not in item:
            sys.exit(f"ERROR: '{item}' must look like NAME=HOSTS")
        name, hosts = item.rsplit("=", 1)
        reqs.append((name.strip(), int(hosts)))
    net, rows, free = plan(a.base, reqs)
    md = to_markdown(net, rows, free)
    print(md)
    if a.md:
        with open(a.md, "w", encoding="utf-8") as f:
            f.write(md)
    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)


if __name__ == "__main__":
    main()
