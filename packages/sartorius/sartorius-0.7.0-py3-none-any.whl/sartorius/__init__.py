"""
Python driver for Sartorius and Minebea Intec scales.

Distributed under the GNU General Public License v2
"""
from __future__ import annotations

from sartorius.driver import Scale


def command_line(args_list: list | None = None) -> None:
    """Command line tool exposed through package install."""
    import argparse
    import asyncio
    import json

    parser = argparse.ArgumentParser(description="Read scale status.")
    parser.add_argument('address', help="The serial or IP address of the scale.")
    parser.add_argument('-n', '--no-info', action='store_true', help="Exclude "
                        "scale information. Reduces communication overhead.")
    parser.add_argument('-z', '--zero', action='store_true', help="Tares and "
                        "zeroes the scale.")
    args = parser.parse_args(args_list)

    async def get() -> None:
        async with Scale(address=args.address) as scale:
            if args.zero:
                await scale.zero()
            d: dict = await scale.get()  # type: ignore
            if not args.no_info and d.get('on', True):
                d['info'] = await scale.get_info()
            print(json.dumps(d, indent=4))
    asyncio.run(get())


if __name__ == '__main__':
    command_line()
