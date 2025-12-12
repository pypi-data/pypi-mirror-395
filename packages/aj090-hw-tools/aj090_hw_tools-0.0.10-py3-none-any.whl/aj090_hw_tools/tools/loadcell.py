__all__ = [
    'loadcell',
]

import logging
import serial
import time
import os
import re
from typing import List, Optional
from colorama import Fore, Style
import statistics

BAUDRATE = 115200
START_PATTERN = '~'

RETRIES_NUM   = 3
MAC           = 0xABCDEF123456
NO_CALIBRATED = 4294967294
FAIL          = 4294967295
RAW_ERROR     = 2147483647

RESPONSE_PATTERN = r'~([\dA-F]{24})\|(\w{3})\|(.*)\|([0-9A-F]{4})\r\n'

# Logger 
FORMAT = '%(name)s:%(levelname)s: %(message)s'
logging.basicConfig(level=logging.ERROR, format=FORMAT)
logger = logging.getLogger(__name__)

def br(text) -> str:
    return Style.BRIGHT + f'{text}' + Style.RESET_ALL

def yellow(text) -> str:
    return Fore.YELLOW + f'{text}' + Style.RESET_ALL

def red(text) -> str:
    return Style.BRIGHT + Fore.RED + f'{text}' + Style.RESET_ALL

def green(text) -> str:
    return Style.BRIGHT + Fore.GREEN + f'{text}' + Style.RESET_ALL

def _crc16_ccitt_false(data: bytearray, offset: int, length: int) -> int:
    if data is None or offset < 0 or offset + length > len(data):
        return 0
    crc = 0xFFFF
    for i in range(length):
        crc ^= data[offset + i] << 8
        for _ in range(8):
            if (crc & 0x8000) > 0:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return crc & 0xFFFF

def _build_command(address: str) -> bytes:
    payload = f'{START_PATTERN}{address}|RCD||'.encode('ascii')
    crc = _crc16_ccitt_false(bytearray(payload), 0, len(payload))
    return payload + f"{crc:04X}\r\n".encode('ascii')

def _send_command(ser: serial.Serial, address: str) -> bytes:
    ser.reset_input_buffer()
    ser.write(_build_command(address=address))
    time.sleep(0.5)
    return ser.read_until(b'\r\n')#, size=2048)

def _parse_response(raw: bytes, device_type: str ='shelf') -> Optional[List[dict]]:
    """
    Parse the raw response from the device.

    Args:
        raw (bytes): Raw bytes received from the device.
        device_type (str): Type of device ('cell' or 'shelf').

    Returns:
        Optional[List[dict]]: Parsed loadcell data or None if parsing fails.
    """
    if not raw:
        return None

    text = raw.decode('ascii', errors='ignore')
    match = re.search(RESPONSE_PATTERN, text, re.DOTALL)
    if not match:
        return None

    payload_str = match.group(3)
    cells_raw = [c.strip() for c in payload_str.split('|' if device_type == 'shelf' else ',') if c.strip()]

    computed_crc = _crc16_ccitt_false(bytearray(raw), 0, len(raw) - 6)
    received_crc = int(match.group(4), 16)
    if computed_crc != received_crc:
        return None

    data = []
    for idx, cell_text in enumerate(cells_raw, start=1):
        kv = {}
        for pair in cell_text.split(',' if device_type == 'shelf' else '|'):
            if '=' in pair:
                k, v = pair.split('=', 1)
                kv[k.strip()] = v.strip()

        try:
            measure = int(kv.get('MEASURE', '-1'))
            raw_val = int(kv.get('RAW_MEASURE', '-1'))
        except ValueError:
            measure = raw_val = -1

        if measure == FAIL:
            measure_str = "FAIL"
        elif measure == NO_CALIBRATED:
            measure_str = "NO CALIBRATED"
        elif measure >= 0:
            measure_str = str(measure)
        else:
            measure_str = "UNKNOWN"

        raw_str = "ERROR" if raw_val == RAW_ERROR else str(raw_val)

        data.append({
            'num': idx,
            'measure': measure_str,
            'raw': raw_str
        })

    return data

def _collect_data(ser: serial.Serial, device_type: str = 'cell') -> Optional[List[dict]]:
    """
    Collect loadcell data from the device.

    Args:
        ser (serial.Serial): The serial port object.
        device_type (str): Type of device ('cell' or 'shelf').
    Returns:
        Optional[List[dict]]: List of loadcell data dictionaries or None if no data.
    """
    ser.reset_input_buffer()
    data = []
    if device_type == 'cell':
        # For the cell device, request data for each cell individually by it's position
        for cell_pos in range(2):
            address  = f"{MAC:016X}00{cell_pos:02X}0000"
            for retry in range(RETRIES_NUM):
                raw = _send_command(ser, address=address)
                response = _parse_response(raw, device_type=device_type)
                if response:
                    response[0]['num'] = cell_pos + 1  
                    data.extend(response)
                    break
                elif retry == 2:
                    data.append({
                        'num': cell_pos + 1,
                        'measure': 'CONNECTION ERROR',
                        'raw': 'CONNECTION ERROR'
                    })
                else:
                    logger.debug("No valid response, retrying...")
                    time.sleep(0.2)
    else:
        # For the shelf device, request data for all cells at once
        address = f"{MAC:016X}FF000000"
        for retry in range(RETRIES_NUM):
            raw  = _send_command(ser, address=address)
            data = _parse_response(raw, device_type=device_type)
            if data:
                break
            elif retry == 2:
                return None
            else:
                logger.debug("No valid response, retrying...")
                time.sleep(0.2)

        for idx, cell in enumerate(data):
            cell['num'] = f'{idx//2 + 1}:{"1" if cell["num"]%2 else "2"}'
        
    return data if data else None

def _display_table(cells: List[dict]):
    """
    Display loadcell data in a formatted table.
    
    Args:
        cells (List[dict]): List of loadcell data dictionaries.
    """
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\033[1;46m LOADCELL MONITOR \033[0m".center(60))
    print()
    print(f" {'#':>17} {'Raw Value':>12}")
    print("  " + "─" * 47)
    for c in cells:
        print(f" {c['num']:>17} {c['raw']:>12}")
    print("  " + "─" * 47)
    print(f"  Active loadcells: {len(cells)} | Refresh: 1 Hz | Ctrl+C to exit")

def _show(ser: serial.Serial, device_type: str = 'cell') -> None:
    """
    Display loadcell data in real-time.
    
    Args:
        ser (serial.Serial): The serial port object.
        device_type (str): Type of device ('cell' or 'shelf').
    """
    while True:
        data = _collect_data(ser, device_type=device_type)
        
        if data:
            _display_table(data)
        else:
            print("Waiting for response...", end="\r", flush=True)

        time.sleep(0.5)

def _print_test_results(data: List[dict]) -> None:
    """
    Print the test results in a formatted manner.
    Args:
        data (List[dict]): List of loadcell data dictionaries.
    """
    total = len(data)
    passed = sum(1 for e in data if e['raw'] != "ERROR")
    failed = total - passed

    print()
    print("\033[1;46m LOADCELL TEST RESULTS \033[0m".center(60))
    print()
    print(f"{'Passed:':<12} {green(f'{passed}/{total}')}")
    print(f"{'Failed:':<12} {red(f'{failed}/{total}')}")
    print()
    print(f"{'#':<6} {'Status':<8} {'Raw Value'}")
    print("─" * 40)

    for cell in data:
        status = green("OK  ") if cell['raw'] != "ERROR" else red("FAIL")
        raw_val = cell['raw'] if cell['raw'] != "ERROR" else red("ERROR")
        print(f"{cell['num']:<4}  {status}     {raw_val}")

    print("─" * 40)
    print()
    print(f"Summary: {green('PASSED') if failed == 0 else red('FAILED')}")
    print()

def _test(ser: serial.Serial, device_type: str = 'shelf') -> None:
    """
    Perform loadcell test and print results.
    
    Args:
        ser (serial.Serial): The serial port object.
        device_type (str): Type of device ('cell' or 'shelf').  
    """
    data = _collect_data(ser, device_type=device_type)
    if data:
        _print_test_results(data)

def _stability_test(ser: serial.Serial, device_type: str = 'shelf') -> None:
    """
    Perform loadcell stability test to verify measurement consistency under load and recovery.
    This test measures loadcell stability by comparing readings in three states:
    1. Unloaded (baseline)
    2. Loaded (with weight applied)
    3. Recovery (after weight removal)
    The test passes if the recovery measurements are within a 5% threshold of the 
    unloaded baseline for all cells, indicating the loadcells return to stable readings.

    Args:
        ser (serial.Serial): Serial port connection to the device.
        device_type (str, optional): Type of device ('shelf' by default).
    Process:
        1. Takes N measurements at T second intervals in unloaded state.
        2. Calculates min, max, average, and mode for each loadcell.
        3. Prompts user to add weight and collects continuous measurements until Ctrl+C.
        4. Prompts user to remove weight and takes recovery measurements.
        5. Compares unloaded vs recovery averages for each cell.
        6. Displays tabular results and overall pass/fail status.
    Returns:
        None
    Raises:
        KeyboardInterrupt: User presses Ctrl+C during loaded measurements phase.
    """
    
    STABILITY_THRESHOLD = 0.05  # 5%
    MEASUREMENT_COUNT = 10
    MEASUREMENT_INTERVAL = 1.0
    STEP_LINE_WIDTH = 100
    TBL_LINE_WIDTH  = 50
    
    def get_numeric_value(raw_val: str) -> Optional[int]:
        try:
            return int(raw_val) if raw_val not in ["ERROR", "CONNECTION ERROR"] else None
        except ValueError:
            return None
    
    def get_mode(values):
        try:
            return statistics.mode(values)
        except statistics.StatisticsError:
            return "N/A"
    
    # Track all cells seen
    all_cells = set()
    
    # Unloaded measurements
    print("\n")
    print("\033[1;46m LOADCELL STABILITY TEST \033[0m".center(STEP_LINE_WIDTH))
    print("""
Perform loadcell stability test to verify measurement consistency under load and recovery.
This test measures loadcell stability by comparing readings in three states:
1. Unloaded (baseline)
2. Loaded (with weight applied)
3. Recovery (after weight removal)
The test passes if the recovery measurements are within a 5% threshold of the 
unloaded baseline for all cells, indicating the loadcells return to stable readings.
""")

    print(f"{br('Step 1')}")
    print(f"{br('Instructions')}: Ensure that the loadcells are installed correctly and have no additional weight.")
    input("Press Enter to start unloaded measurements...")
    print("=" * STEP_LINE_WIDTH)
    unloaded_data = {}
    
    for i in range(MEASUREMENT_COUNT):
        data = _collect_data(ser, device_type=device_type)
        if data:
            for cell in data:
                cell_num = cell['num']
                all_cells.add(cell_num)
                val = get_numeric_value(cell['raw'])
                if val is not None:
                    if cell_num not in unloaded_data:
                        unloaded_data[cell_num] = []
                    unloaded_data[cell_num].append(val)
                elif cell['raw'] in ["ERROR", "CONNECTION ERROR"]:
                    if cell_num not in unloaded_data:
                        unloaded_data[cell_num] = "N/A"
            msg = f"Taking unloaded measurements. Measurement {i+1}/{MEASUREMENT_COUNT}..."
            print(f"\r{msg.ljust(STEP_LINE_WIDTH)}", end='', flush=True)
        time.sleep(MEASUREMENT_INTERVAL)
    
    # Display unloaded results
    print("\nUnloaded Measurements Summary:")
    print(f"{'#':<6} {'Min':<10} {'Max':<10} {'Avg':<10} {'Mode':<10}")
    print("─" * TBL_LINE_WIDTH)
    for cell_num in sorted(all_cells, key=str):
        if cell_num in unloaded_data:
            if unloaded_data[cell_num] == "N/A":
                print(f"{cell_num:<6} {'N/A':<10} {'N/A':<10} {'N/A':<10} {'N/A':<10}")
            else:
                values = unloaded_data[cell_num]
                print(f"{cell_num:<6} {min(values):<10} {max(values):<10} {statistics.mean(values):<10.2f} {get_mode(values):<10}")
    
    # Loaded measurements
    print(f"\n{br('Step 2')}")
    print(f"{br('Instructions')}: Add a weight to the loadcells to perform loaded measurements.")
    input("Press Enter to start loaded measurements...")
    print("=" * STEP_LINE_WIDTH)
       
    loaded_data = {}
    start_time = time.time()
    measurement_num = 0
    print("Taking loaded measurements (press Ctrl+C to stop).")
    try:
        while True:
            data = _collect_data(ser, device_type=device_type)
            if data:
                measurement_num += 1
                for cell in data:
                    cell_num = cell['num']
                    all_cells.add(cell_num)
                    val = get_numeric_value(cell['raw'])
                    if val is not None:
                        if cell_num not in loaded_data:
                            loaded_data[cell_num] = []
                        loaded_data[cell_num].append(val)
                    elif cell['raw'] in ["ERROR", "CONNECTION ERROR"]:
                        if cell_num not in loaded_data:
                            loaded_data[cell_num] = "N/A"
                msg = f"Measurement number {measurement_num}. Time elapsed: {time.time() - start_time:.1f}s..."
                print(f"\r{msg.ljust(STEP_LINE_WIDTH)}", end='', flush=True)
            time.sleep(MEASUREMENT_INTERVAL)
    except KeyboardInterrupt:
        print("\nMeasurements stopped.")
    
    elapsed_time = time.time() - start_time
    
    # Display loaded results
    print(f"Loaded Measurements Summary (Time: {elapsed_time:.1f}s, Measurements: {measurement_num}):")
    print(f"{'#':<6} {'Min':<10} {'Max':<10} {'Avg':<10} {'Mode':<10}")
    print("─" * TBL_LINE_WIDTH)
    for cell_num in sorted(all_cells, key=str):
        if cell_num in loaded_data:
            if loaded_data[cell_num] == "N/A":
                print(f"{cell_num:<6} {'N/A':<10} {'N/A':<10} {'N/A':<10} {'N/A':<10}")
            else:
                values = loaded_data[cell_num]
                print(f"{cell_num:<6} {min(values):<10} {max(values):<10} {statistics.mean(values):<10.2f} {get_mode(values):<10}")
    
    # Unloaded recovery measurements
    print(f"\n{br('Step 3')}")
    print(f"{br('Instructions')}: Remove the weight from the loadcells to perform recovery measurements.")
    input("Press Enter to start recovery measurements...")
    print("=" * STEP_LINE_WIDTH)
    recovery_data = {}
    
    for i in range(MEASUREMENT_COUNT):
        data = _collect_data(ser, device_type=device_type)
        if data:
            for cell in data:
                cell_num = cell['num']
                all_cells.add(cell_num)
                val = get_numeric_value(cell['raw'])
                if val is not None:
                    if cell_num not in recovery_data:
                        recovery_data[cell_num] = []
                    recovery_data[cell_num].append(val)
                elif cell['raw'] in ["ERROR", "CONNECTION ERROR"]:
                    if cell_num not in recovery_data:
                        recovery_data[cell_num] = "N/A"
            print(f"\rTaking recovery measurements. Measurement {i+1}/{MEASUREMENT_COUNT}...", end='', flush=True)
        time.sleep(MEASUREMENT_INTERVAL)
    
    # Display recovery results
    print("\nRecovery Measurements Summary:")
    print(f"{'#':<6} {'Min':<10} {'Max':<10} {'Avg':<10} {'Mode':<10}")
    print("─" * TBL_LINE_WIDTH)
    for cell_num in sorted(all_cells, key=str):
        if cell_num in recovery_data:
            if recovery_data[cell_num] == "N/A":
                print(f"{cell_num:<6} {'N/A':<10} {'N/A':<10} {'N/A':<10} {'N/A':<10}")
            else:
                values = recovery_data[cell_num]
                print(f"{cell_num:<6} {min(values):<10} {max(values):<10} {statistics.mean(values):<10.2f} {get_mode(values):<10}")

    # Compare and display results
    print(f"\n\n{br('STABILITY TEST RESULTS')}")
    print("=" * STEP_LINE_WIDTH)
    print(f"{'#':<6} {'Unloaded':<12} {'Recovery':<12} {'Diff %':<8} {'Status':<6}")
    print("─" * TBL_LINE_WIDTH)
    
    all_passed = True
    passed_count = 0
    failed_count = 0
    error_count = 0
    
    for cell_num in sorted(all_cells, key=str):
        unloaded_vals = unloaded_data.get(cell_num, "N/A")
        recovery_vals = recovery_data.get(cell_num, "N/A")
        
        if unloaded_vals == "N/A" or recovery_vals == "N/A":
            status = red("N/A")
            error_count += 1
            all_passed = False
            print(f"{cell_num:<6} {'N/A':<12} {'N/A':<12} {'N/A':<8} {status:<6}")
        else:
            unloaded_avg = statistics.mean(unloaded_vals)
            recovery_avg = statistics.mean(recovery_vals)
            diff_percent = abs(recovery_avg - unloaded_avg) / unloaded_avg if unloaded_avg != 0 else 0
            status = green("PASS") if diff_percent <= STABILITY_THRESHOLD else red("FAIL")
            
            if diff_percent <= STABILITY_THRESHOLD:
                passed_count += 1
            else:
                failed_count += 1
                all_passed = False
            
            print(f"{cell_num:<6} {unloaded_avg:<12.2f} {recovery_avg:<12.2f} {diff_percent*100:<8.2f} {status:<6}")
    
    print("\n" + "=" * STEP_LINE_WIDTH)
    total = len(all_cells)
    print(f"Summary: Passed: {green(f'{passed_count}')}, Failed: {red(f'{failed_count}')}, Errors: {red(f'{error_count}')}, Total: {total}")
    result = green("PASSED") if all_passed else red("FAILED")
    print(f"{br('OVERALL RESULT')}: {result}\n")

def loadcell(argv) -> int:
    """
    Main function to handle loadcell operations based on command-line arguments.
    
    Args:
        argv: Command-line arguments containing operation details.
    
    Returns:
        int: Exit status code.
    """
    port = argv.port if argv.port is not None else "/dev/ttyUSB0"

    ser = serial.Serial(port, BAUDRATE, timeout=0.5)
    logger.info(f"Connected to {port} @ {BAUDRATE} bps")
    time.sleep(2)

    try:
        match argv.operation:
            case 'test':
                logger.info("Performing loadcell test...")
                _test(ser, device_type=argv.device)
            case 'stab':
                logger.info("Performing measurement stability test...")
                _stability_test(ser, device_type=argv.device)
            case 'show':
                logger.info("Starting loadcell monitoring...")
                _show(ser, device_type=argv.device)
            case _:
                logger.error(f"Unknown operation: {argv.operation}")
                raise ValueError(f"Unknown loadcell operation: {argv.operation}")
    
    except Exception as e:
        logger.error(f"Error: {e}")
        ser.close()
        return -1
    
    logger.info("Port closed.")
    ser.close()
    return 0