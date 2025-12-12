__all__ = [
    'serial'
]

import asyncio
import logging
import subprocess
import sys
import tempfile
import re
import esptool
import time

from esptool.cmds import detect_chip
from rich.console import Console

from ..common.const import SERIAL_INPUT_PATTERN

# Logger 
FORMAT = '%(name)s:%(levelname)s: %(message)s'
logging.basicConfig(level=logging.ERROR, format=FORMAT)
logger = logging.getLogger(__name__)

console = Console()

def nvs_partition_template(factory_mode: bool, hw_version: str, serial_number: str) -> str:
    return """key,type,encoding,value
factory,namespace,,
factory_mode,data,u8,{factory_mode}
hw_version,data,string,{hw_version}
serial,data,string,{serial_number}
""".format(
    factory_mode  = int(factory_mode),
    hw_version    = hw_version,
    serial_number = serial_number
)

async def nvs_write(device, bin_file: str, offset: int = 0x11000) -> None:
    def _write():
        command = ['write_flash', f'{offset}', f'{bin_file}']
        logger.debug("Using command ", " ".join(command))
        esptool.main(command, device)

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _write) 

def check_serial(serial: str) -> int:
    INPUT_SERIAL="""Serial number format: YYWWXXXXXX, where:
YY - 2 digits of the year of manufacture of the product;
WW - 2 digits of the product production week number;
XXXXXX - 6 digits of the serial number of the product.
"""
    match = re.search(SERIAL_INPUT_PATTERN, serial)
    if match is None:
        console.print('Wrong serial number format. Must be: YYWWXXXXXX', style='bold red')
        console.print(f'{INPUT_SERIAL}')
        return -1
    
    return 0

async def serial_write(device, device_type: str, serial: str) -> int:
    type = 'S' if device_type == "shelf" else "C"
    with tempfile.NamedTemporaryFile(suffix='.csv') as nvs_csv:
        data = bytes(nvs_partition_template(True, '1.0', f'{type}{serial}').encode())
        nvs_csv.write(data)
        nvs_csv.seek(0)
        logger.debug(f'CSV file data: {nvs_csv.read()}')

        with tempfile.NamedTemporaryFile(suffix='.bin') as nvs_bin:
            args   = ['generate', nvs_csv.name, nvs_bin.name, '0x10000']
            result = subprocess.run([sys.executable, '-m', 'esp_idf_nvs_partition_gen'] + args).returncode
            if not result:
                await nvs_write(device, nvs_bin.name)
            else:
                console.print('NVS partition generate error', style='bold red')
                return -1
    
    console.print('SUCCESS', style='bold green')

async def serial_read() -> int:
    return -1

def serial(argv) -> int:
    if check_serial(argv.serial):
        return -1
    port     = argv.port if argv.port is not None else esptool.ESPLoader.DEFAULT_PORT
    connects = 10 # NOTE: the workaround to the issue "Could not open /dev/tty..., the port is busy or doesn't exist" 
    for _ in range(connects): 
        try:   
            with detect_chip(port=port, connect_attempts=0) as device:
                match argv.operation:
                    case 'write':
                        return asyncio.run(serial_write(device, argv.device, argv.serial))
                    case 'read':
                        return asyncio.run(serial_read(device))
                    case _:
                        console.print('Unknown command', style='red bold')
                        return -1
        except OSError:
            # NOTE: we are trying to close an already closed port (in device_test()), 
            # thus an OSError occurs (invalid file descriptor)
            return 0
        except esptool.util.FatalError as err:
            logger.debug(err)
            time.sleep(1.0)
    print("Can't connect to the device")
    return -1


    