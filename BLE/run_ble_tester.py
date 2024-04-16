#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import logging
import asyncio
import sys
import os
import signal
import subprocess
import afl
import random

from binascii import hexlify

from bumble.device import Device, Peer
from bumble.host import Host
from bumble.gatt import show_services
from bumble.core import ProtocolError
from bumble.controller import Controller
from bumble.link import LocalLink
from bumble.transport import open_transport_or_link
from bumble.utils import AsyncRunner
from bumble.colors import color

#p = subprocess.Popen(["GCOV_PREFIX=$(pwd) GCOV_PREFIX_STRIP=3 ./zephyr.exe","--bt-dev=127.0.0.1:9000"])

async def write_target(target, attribute, bytes):
    # Write
    try:
        bytes_to_write = bytearray(bytes)
        await target.write_value(attribute, bytes_to_write, True)
        print(color(f'[OK] WRITE Handle 0x{attribute.handle:04X} --> Bytes={len(bytes_to_write):02d}, Val={hexlify(bytes_to_write).decode()}', 'green'))
        return True
    except ProtocolError as error:
        print(color(f'[!]  Cannot write attribute 0x{attribute.handle:04X}:', 'yellow'), error)
    except TimeoutError:
        print(color('[X] Write Timeout', 'red'))
        
    return False


async def read_target(target, attribute):
    # Read
    try: 
        read = await target.read_value(attribute)
        value = read.decode('latin-1')
        print(color(f'[OK] READ  Handle 0x{attribute.handle:04X} <-- Bytes={len(read):02d}, Val={read.hex()}', 'cyan'))
        return value
    except ProtocolError as error:
        print(color(f'[!]  Cannot read attribute 0x{attribute.handle:04X}:', 'yellow'), error)
    except TimeoutError:
        print(color('[!] Read Timeout'))
    
    return None

# -----------------------------------------------------------------------------
class TargetEventsListener(Device.Listener):

    got_advertisement = False
    advertisement = None
    connection = None

    def on_advertisement(self, advertisement):

        print(f'{color("Advertisement", "cyan")} <-- '
              f'{color(advertisement.address, "yellow")}')
        
        # Indicate that an from target advertisement has been received
        self.advertisement = advertisement
        self.got_advertisement = True


    @AsyncRunner.run_in_task()
    # pylint: disable=invalid-overridden-method
    async def on_connection(self, connection):
        print(color(f'[OK] Connected!', 'green'))
        self.connection = connection

        # Discover all attributes (services, characteristitcs, descriptors, etc)
        print('=== Discovering services')
        target = Peer(connection)
        attributes = []
        await target.discover_services()
        for service in target.services:
            attributes.append(service)
            await service.discover_characteristics()
            for characteristic in service.characteristics:
                attributes.append(characteristic)
                await characteristic.discover_descriptors()
                for descriptor in characteristic.descriptors:
                    attributes.append(descriptor)

        print(color('[OK] Services discovered', 'green'))
        show_services(target.services)
        
        # -------- Main interaction with the target here --------
    
        print('=== Read/Write Attributes (Handles)')
        for attribute in attributes:
            
            #s = int(sys.stdin.read())
            a = [2, 3, 5, 7]
            byte_array = bytearray(a)
            await write_target(target, attribute, [a])
            await read_target(target, attribute)
        
        # randint = random.randint(0,len(attributes)-1)
        
        # a = [2, 3, 5, 7]
        # byte_array = bytearray(a)
        # await write_target(target, attributes[randint], [0x01])
        # await read_target(target, attributes[randint])
        
        print('---------------------------------------------------------------')
        print(color('[OK] Communication Finished', 'green'))
        print('---------------------------------------------------------------')
        #p.kill()
        outputfile = 'lcov4.info'
        p = subprocess.Popen(f"lcov --capture --directory ./ --output-file {outputfile} -q --rc lcov_branch_coverage=1", shell = True)
        p
        p.kill
        os._exit(0)
        # ---------------------------------------------------
        
        

# -----------------------------------------------------------------------------
async def main():
    
    # if len(sys.argv) != 2:
    #     print('Usage: run_controller.py <transport-address>')
    #     print('example: ./run_ble_tester.py tcp-server:0.0.0.0:9000')
    #     return

    print('>>> Waiting connection to HCI...')
    # async with await open_transport_or_link(sys.argv[1]) as (hci_source, hci_sink):
    async with await open_transport_or_link("tcp-server:127.0.0.1:9000") as (hci_source, hci_sink):
        print('>>> Connected')

        # Create a local communication channel between multiple controllers
        link = LocalLink()

        # Create a first controller for connection with host interface (Zephyr)
        zephyr_controller = Controller('Zephyr', host_source=hci_source,
                                 host_sink=hci_sink,
                                 link=link)


        # Create our own device (tester central) to manage the host BLE stack
        device = Device.from_config_file('tester_config.json')
        # Create a host for the second controller
        device.host = Host() 
        # Create a second controller for connection with this test driver (Bumble)
        device.host.controller = Controller('Fuzzer', link=link)
        # Connect class to receive events during communication with target
        device.listener = TargetEventsListener()
        
        # Start BLE scanning here
        await device.power_on()
        await device.start_scanning() # this calls "on_advertisement"

        #p
        
        print('Waiting Advertisment from BLE Target')
        while device.listener.got_advertisement is False:
            await asyncio.sleep(0.5)
            
        await device.stop_scanning() # Stop scanning for targets

        print(color('\n[OK] Got Advertisment from BLE Target!', 'green'))
        target_address = device.listener.advertisement.address

        # Start BLE connection here
        print(f'=== Connecting to {target_address}...')
        await device.connect(target_address) # this calls "on_connection"
        
        # Wait in an infinite loop
        await hci_source.wait_for_termination()


def read_lines_from_file(filename):
    """
    Reads lines from the specified file and returns a generator.
    """
    with open(filename, "r") as file:
        for line in file:
            yield line.strip()

def write_lines_to_file(filename, lines):
    """
    Appends lines to the specified file.
    """
    with open(filename, "a") as file:
        for line in lines:
            file.write( "\n"+line )
    return lines[0]

def remove_line_from_file(filename, line_to_remove):
    """
    Removes the first occurrence of a specific line from the specified file.
    """
    with open(filename, "r") as file:
        lines = file.readlines()

    with open(filename, "w") as file:
        removed = False
        for line in lines:
            if not removed and line.strip() == line_to_remove:
                removed = True
                continue  # Skip writing the line to remove
            file.write(line)


#HOW THE CODE SHOULD BE RUN
# def main():
#     filename = "filename.txt"  # Predefined filename
#     line_reader = read_lines_from_file(filename)
#     while True:
#         input_line = next(line_reader)
#         print(input_line)
#         mod_input="Test2ed"
#         remove_line_from_file(filename, input_line)  # Remove from file
        
#         write_lines_to_file(filename, [mod_input])  # Write to the same file
#         break



# -----------------------------------------------------------------------------
    
#logging.basicConfig(level=os.environ.get('BUMBLE_LOGLEVEL', 'INFO').upper())
#asyncio.run(main(a))

if __name__ == '__main__':
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)  # this should have no effect on the forkserver
    afl.init()
    
    
    asyncio.run(main())
    #p.kill()
    os._exit(0)