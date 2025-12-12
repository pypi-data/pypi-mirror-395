#!/usr/bin/env python3
"""Fetch SNMP agent uptime using Zino high-level APIs"""

import argparse
import asyncio
import logging

from zino.config.polldevs import read_polldevs
from zino.snmp import SNMP

_log = logging.getLogger(__name__)


def main():
    args = parse_args()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s (%(threadName)s) - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S %Z",
    )
    asyncio.get_event_loop().run_until_complete(run(args))


async def run(args: argparse.Namespace):
    devices = {d.name: d for d in read_polldevs("polldevs.cf")}
    device = devices[args.router]

    snmp = SNMP(device)
    yellow_alarm_count = await snmp.get("JUNIPER-ALARM-MIB", "jnxYellowAlarmCount", 0)
    _log.info("Response from %s: %r (%s)", device.name, yellow_alarm_count, type(yellow_alarm_count))


def parse_args():
    devicenames = [d.name for d in read_polldevs("polldevs.cf")]
    parser = argparse.ArgumentParser(description="Fetch yellow alert count from a device in polldevs.cf")
    parser.add_argument("router", type=str, help="Zino router name", choices=devicenames)
    return parser.parse_args()


if __name__ == "__main__":
    main()
