__all__ = [
    'info'
]

import asyncio
import logging
import pexpect
import pexpect.spawnbase
import time
import esptool
import re

from rich.console import Console
from rich.table import Table
from pexpect.fdpexpect import fdspawn
from typing import Optional, Type, NamedTuple
from esptool.cmds import detect_chip

from ..common.const import SERIAL_NUM_PATTERN

# Logger 
FORMAT = '%(name)s:%(levelname)s: %(message)s'
logging.basicConfig(level=logging.ERROR, format=FORMAT)
logger = logging.getLogger(__name__)

# Rich console
console = Console()

DUT = Type[pexpect.spawnbase.SpawnBase]

class GatherInfoError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self._message : str           = message

class DeviceInfo(NamedTuple):
    """ Base device information """
    app_ver: str
    compile_time: str
    app_sha: str
    hw_ver: str
    mac:str
    sn: str

async def board_type_get(dut: DUT) -> Optional[str]:
    result = await dut.expect([r'MAIN: Starting (?:\w+ )?(CELL|SHELF) CONTROLLER application', pexpect.TIMEOUT], timeout=5.0, async_=True)
    if result:
        raise GatherInfoError('Unknown type of board or device has not been flashed yet')
    board_type = dut.match.group(1).decode('utf-8').lower()
    return board_type.lower()

async def device_info_get(dut: DUT) -> Optional[DeviceInfo]:
    # I (00:00:01.100) DEVICE_INFO: 
    #     app version: b366ae1
    #     compile time: 13:00:08
    #     sha256: 3c050c5d0ea4aea33643eba2b7e840c607af710176e4387b3b22f183c920f09e
    #     hw version: 1.0
    #     MAC: 64:E8:33:48:EF:C4
    #     serial: XXXXXXXX
    MATCH_PATTERN = re.compile(
        r'DEVICE_INFO:\s+app version:\s+(\w{{7}}|\w{{7}}-dirty)\s+compile time:\s+(\d{{2}}:\d{{2}}:\d{{2}})\s+sha256:\s+(\w{{64}})\s+hw version:\s+(\d{{1}}\.\d{{1}})\s+MAC:\s+(\w{{2}}:\w{{2}}:\w{{2}}:\w{{2}}:\w{{2}}:\w{{2}})\s+serial:\s+({SERIAL_NUM_PATTERN})'.format(SERIAL_NUM_PATTERN=SERIAL_NUM_PATTERN)
    )
    result = await dut.expect([MATCH_PATTERN, pexpect.TIMEOUT], timeout=5.0, async_=True)
    if result:
        raise GatherInfoError('Failed to collect information about the device')
    device_info = DeviceInfo(
        app_ver      = dut.match.group(1).decode('utf-8').lower(),
        compile_time = dut.match.group(2).decode('utf-8').lower(),
        app_sha      = dut.match.group(3).decode('utf-8').lower(),
        hw_ver       = dut.match.group(4).decode('utf-8').lower(),
        mac          = dut.match.group(5).decode('utf-8').lower(),
        sn           = dut.match.group(6).decode('utf-8').lower()
    )
    return device_info

async def gather_info(device, argv) -> int:
    device.hard_reset()

    # NOTE: we are working with an already open port in another place (ESPLoader) !!!
    dut: DUT = fdspawn(device._port, timeout=180)
    last_error = 0
    try:
        # get board type
        board_type = await board_type_get(dut)

        # get device info
        dev_info = await device_info_get(dut)

        table = Table(title=f"{board_type.capitalize()} controller information", show_lines=True)

        table.add_column("Info", justify="left", style="cyan", no_wrap=True)
        table.add_column("Value", justify="left", style="green")

        table.add_row('Application version', dev_info.app_ver)
        table.add_row('Application SHA', dev_info.app_sha)
        table.add_row('Hardware version', dev_info.hw_ver)
        table.add_row('MAC', dev_info.mac)
        table.add_row('Serial number', dev_info.sn)

        console.print(table)

    except GatherInfoError as err:
        console.print(err, style="bold red")
        last_error = -1
    except pexpect.TIMEOUT:
        console.print('Waiting time exceeded', style="bold red")
        last_error = -1
        
    try:
        dut.close()
    except OSError as err:
        logger.debug(f'OSError: {err}')

    return last_error


def info(argv) -> int:
    port     = argv.port if argv.port is not None else esptool.ESPLoader.DEFAULT_PORT
    connects = 10 # NOTE: the workaround to the issue "Could not open /dev/tty..., the port is busy or doesn't exist" 
    for _ in range(connects): 
        try:
            with detect_chip(port=port, connect_attempts=0) as device:
                return asyncio.run(gather_info(device, argv))
        except OSError:
            # NOTE: we are trying to close an already closed port (in device_test()), 
            # thus an OSError occurs (invalid file descriptor)
            return 0
        except esptool.util.FatalError as err:
            logger.debug(err)
            time.sleep(1.0)

    console.print("Can't connect to the device", style="bold red")
    return -1