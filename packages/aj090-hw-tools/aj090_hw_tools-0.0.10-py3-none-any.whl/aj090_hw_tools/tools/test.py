__all__ = [
    'test',
]

import asyncio
import logging
import pexpect
import pexpect.spawnbase
import re
import time
import esptool

from aioconsole import aprint
from colorama import Fore, Style
from pexpect.fdpexpect import fdspawn
from typing import Optional, Type, NamedTuple
from esptool.cmds import detect_chip

from ..common.const import SERIAL_NUM_PATTERN

DEFAULT_BAUDRATE = 115200
DEFAULT_SERIAL_TIMEOUT_IN_SECONDS = 2 

# Logger 
FORMAT = '%(name)s:%(levelname)s: %(message)s'
logging.basicConfig(level=logging.ERROR, format=FORMAT)
logger = logging.getLogger(__name__)

DUT = Type[pexpect.spawnbase.SpawnBase]

class BootInfo(NamedTuple):
    idf_version: str
    boot_offset: str
    app_version: str

class DeviceInfo(NamedTuple):
    """ Base device information """
    app_ver: str
    compile_time: str
    app_sha: str
    hw_ver: str
    mac:str
    sn: str

def br(text) -> str:
    return Style.BRIGHT + f'{text}' + Style.RESET_ALL

def yellow(text) -> str:
    return Fore.YELLOW + f'{text}' + Style.RESET_ALL

def red(text) -> str:
    return Style.BRIGHT + Fore.RED + f'{text}' + Style.RESET_ALL

def green(text) -> str:
    return Style.BRIGHT + Fore.GREEN + f'{text}' + Style.RESET_ALL

class TestError(Exception):
    def __init__(self, message, expected_output: str = None, before: str = None):
        super().__init__(message)
        self._message : str           = message
        self._expected: Optional[str] = expected_output
        self._before  : Optional[str] = before
    
    @property
    def before(self) -> Optional[str]:
        return self._before

    def __str__(self):
        if self._expected is not None:
            return f'{red(self._message)}:\r\n\t{br("Expected output")}: {self._expected}'
        else:
            return f'{red(self._message)}'

async def do_test(dut: DUT, unit:str, expected: str, timeout: float = 5.0) -> int:
    result = await dut.expect([expected, pexpect.TIMEOUT], timeout=timeout, async_=True)
    if result:
        raise TestError(f'{unit} test error', expected, dut.before)
    else:
        await aprint(f'{unit} test: {green("OK")}')

    return result

async def device_boot_test(dut: DUT) -> BootInfo:
    boot_expect = [
        r'boot: ESP-IDF v(\d\.\d(?:.\d)*|\d\.\d+(?:.\d)*-dirty) 2nd stage bootloader',
        r'boot: Loaded app from partition at offset (0x\d{5,})',
        r'app_init: App version:\s+(\w{7})'
    ]

    await do_test(dut, '2nd stage bootloader', boot_expect[0])
    idf_version = dut.match.group(1).decode('utf-8').lower()
    await do_test(dut, 'Load app', boot_expect[1])
    boot_offset = dut.match.group(1).decode('utf-8')
    await do_test(dut, 'App version', boot_expect[2])
    app_version = dut.match.group(1).decode('utf-8').lower()

    boot_info = BootInfo(
        idf_version = idf_version,
        app_version = app_version,
        boot_offset = boot_offset
    )
    logger.debug(f'Device boot info: {boot_info}')

    return boot_info

async def common_modules_init_test(dut: DUT) -> int:
    expected_outputs = [
        ('Firmware manager', r'FW_MANAGER: Firmware manager has been successfully initialized'),
        ('File storage', r'STORAGE: Storage manager has been successfully initialized'),
        ('Configuration manager', r'CFG_MANAGER: Configuration manager has been successfully initialized'),
        ('Board', r'BOARD: Board has been successfully initialized')
    ]
    for unit, output in expected_outputs:
        await do_test(dut, unit, output)

async def board_type_test(dut: DUT) -> str:
    await do_test(dut, 'Board type', r'MAIN: Starting (?:\w+ )?(CELL|SHELF) CONTROLLER application')
    board_type = dut.match.group(1).decode('utf-8').lower()
    return board_type.lower()

async def device_info_test(dut: DUT) -> DeviceInfo:
    # I (00:00:01.100) DEVICE_INFO: 
    #     app version: b366ae1
    #     compile time: 13:00:08
    #     sha256: 3c050c5d0ea4aea33643eba2b7e840c607af710176e4387b3b22f183c920f09e
    #     hw version: 1.0
    #     MAC: 64:E8:33:48:EF:C4
    #     serial: XXXXXXXX
    MATCH_PATTERN = re.compile(
        r'DEVICE_INFO:\s+app version:\s+(\w{{7}})\s+compile time:\s+(\d{{2}}:\d{{2}}:\d{{2}})\s+sha256:\s+(\w{{64}})\s+hw version:\s+(\d{{1}}\.\d{{1}})\s+MAC:\s+(\w{{2}}:\w{{2}}:\w{{2}}:\w{{2}}:\w{{2}}:\w{{2}})\s+serial:\s+({SERIAL_NUM_PATTERN})'.format(SERIAL_NUM_PATTERN=SERIAL_NUM_PATTERN)
    )
    await do_test(dut, 'Device info', MATCH_PATTERN)
    device_info = DeviceInfo(
        app_ver      = dut.match.group(1).decode('utf-8').lower(),
        compile_time = dut.match.group(2).decode('utf-8').lower(),
        app_sha      = dut.match.group(3).decode('utf-8').lower(),
        hw_ver       = dut.match.group(4).decode('utf-8').lower(),
        mac          = dut.match.group(5).decode('utf-8').lower(),
        sn           = dut.match.group(6).decode('utf-8').lower()
    )
    return device_info

async def cell_test(dut: DUT, app_version: str) -> int:
    await do_test(dut, 'Cells initialization', r'CELL_CONTROLLER: initialize cells of the (\w{6,9}) board')
    cell_type = dut.match.group(1).decode('utf-8').lower()
    await do_test(dut, 'Application', r'MAIN: The application has been successfully initialized')
    match cell_type:
        case 'retail':
            await do_test(dut, 'Cells#0 measurements', r'CELL_CONTROLLER: cell#0 measure result', timeout=20)
            await do_test(dut, 'Cells#1 measurements', r'CELL_CONTROLLER: cell#1 measure result', timeout=20)
        case 'wholesale':
            await do_test(dut, 'Cell measurements', r'CELL_CONTROLLER: cell#0 measure result', timeout=20)
        case _:
            raise TestError(f'Unknown cell type: {cell_type}')
    return 0

async def shelf_test(dut: DUT, app_version: str) -> int:
    await do_test(dut, 'Main task start', r'SHELF_CONTROLLER: Shelf controller main task started')
    await do_test(dut, 'Environment sensor initialization', r'ENV_SENSOR: sensor created')
    await do_test(dut, 'Application', r'MAIN: The application has been successfully initialized')
    await do_test(dut, 'Environment sensor measurements', r'SHELF_CONTROLLER: Temperature: (\d{1,3}[.,]\d+); humudity: (\d{1,2}[.,]\d+)')

    return 0

async def device_test(device, argv):
    device.hard_reset()

    # NOTE: we are working with an already open port in another place (ESPLoader) !!!
    dut: DUT = fdspawn(device._port, timeout=180)
    last_error = 0
    try:
        boot_info = await device_boot_test(dut)
        await aprint(yellow(f'Device boot info: {boot_info}'))
        await common_modules_init_test(dut)

        board_type = await board_type_test(dut)
        if argv.device != board_type:
            raise TestError(f'Wrong board type. Got: {board_type.upper()}', f'{argv.device.upper()}')
        
        device_info = await device_info_test(dut)
        await aprint(yellow(f'Device info: {device_info}'))

        match argv.device:
            case 'cell':
                last_error = await cell_test(dut, device_info.app_ver)
            case 'shelf':
                last_error = await shelf_test(dut, device_info.app_ver)

            case _:
                raise Exception('Unsupported device')
    except TestError as err:
        await aprint(err)
        last_error = -1
    except pexpect.TIMEOUT:
        await aprint('Waiting time exceeded')
        last_error = -1
        
    try:
        dut.close()
    except OSError as err:
        logger.debug(f'OSError: {err}')

    if last_error:
        await aprint(red('FAILED'))
    else:
        await aprint(green('PASSED'))
        
    return last_error


def test(argv) -> int:
    port     = argv.port if argv.port is not None else esptool.ESPLoader.DEFAULT_PORT
    connects = 10 # NOTE: the workaround to the issue "Could not open /dev/tty..., the port is busy or doesn't exist" 
    for _ in range(connects): 
        try:   
            with detect_chip(port=port, connect_attempts=0) as device:
                return asyncio.run(device_test(device, argv))
        except OSError:
            # NOTE: we are trying to close an already closed port (in device_test()), 
            # thus an OSError occurs (invalid file descriptor)
            return 0
        except esptool.util.FatalError as err:
            logger.debug(err)
            time.sleep(1.0)
    print("Can't connect to the device")
    return -1
