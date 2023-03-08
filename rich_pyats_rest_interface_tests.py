import os
import json
import logging
import cairosvg
import requests
from pyats import aetest
from pyats.log.utils import banner
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv
from requests_toolbelt.multipart.encoder import MultipartEncoder

# ENV FOR WEBEX
load_dotenv()

webexToken = os.getenv("WEBEX_TOKEN")
webexRoomId = os.getenv("WEBEX_ROOMID")

# ----------------
# Get logger for script
# ----------------

log = logging.getLogger(__name__)

# ----------------
# AE Test Setup
# ----------------
class common_setup(aetest.CommonSetup):
    """CommSetup section"""
# ----------------
# Connected to devices
# ----------------
    @aetest.subsection
    def connect_to_devices(self, testbed):
        """Connect to all the devices"""
        testbed.connect()
# ----------------
# Mark the loop for Input Discards
# ----------------
    @aetest.subsection
    def loop_mark(self, testbed):
        aetest.loop.mark(Test_OpenConfig_Interface, device_name=testbed.devices)
        aetest.loop.mark(Test_Cisco_IOS_XE_Interface_Oper, device_name=testbed.devices)

# ----------------
# Test Case #1
# ----------------
class Test_OpenConfig_Interface(aetest.Testcase):
    """Parse the OpenConfig YANG Model - interfaces:interfaces"""

    @aetest.test
    def setup(self, testbed, device_name):
        """ Testcase Setup section"""
        # Loop over devices in tested for testing
        self.device = testbed.devices[device_name]
    
    @aetest.test
    def get_test_yang_data(self):
        # Use the RESTCONF OpenConfig YANG Model 
        parsed_openconfig_interfaces = self.device.rest.get("/restconf/data/openconfig-interfaces:interfaces")
        # Get the JSpayload
        self.parsed_json=parsed_openconfig_interfaces.json()

    @aetest.test
    def create_pre_test_files(self):
        # Create .JSfile
        with open(f'JSON/{self.device.alias}_OpenConfig_Interfaces.json', 'w') as f:
            f.write(json.dumps(self.parsed_json, indent=4, sort_keys=True))

    @aetest.test
    def test_interface_input_crc_errors(self):
        # Test for input discards
        in_crc_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input CRC Errors")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input CRC Threshold", style="magenta")
        table.add_column("Input CRC Errors", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'openconfig-if-ethernet:ethernet' in intf:
                counter = intf['openconfig-if-ethernet:ethernet']['state']['counters']['in-crc-errors']
                if counter:
                    if int(counter) > in_crc_errors_threshold:
                        table.add_row(self.device.alias,intf['name'],str(in_crc_errors_threshold),counter,'Failed',style="red")
                        self.failed_interfaces[intf['name']] = int(counter)
                        self.interface_name = intf['name']
                        self.error_counter = self.failed_interfaces[intf['name']]
                    else:
                        table.add_row(self.device.alias,intf['name'],str(in_crc_errors_threshold),counter,'Passed',style="green")
                else:
                    table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="yellow")           
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())
        
        # Save table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interface Input CRC Errors.svg", title = f"{ self.device.alias } Open Config Interface Input CRC Errors")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interface Input CRC Errors.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interface Input CRC Errors.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The Device { self.device.alias } Has Interface Input CRC Errors',
                          'files': (f"Test Results/{ self.device.alias } Open Config Interface Input CRC Errors.png", open(f"Test Results/{ self.device.alias } Open Config Interface Input CRC Errors.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)
            self.failed('Some interfaces have input CRC errors')
        else:
            self.passed('No interfaces have input CRC errors')

    @aetest.test
    def test_interface_input_fragment_errors(self):
        # Test for input discards
        in_fragment_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input Fragment Frames")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Fragment Frames Threshold", style="magenta")
        table.add_column("Input Fragment Frames", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'openconfig-if-ethernet:ethernet' in intf:
                counter = intf['openconfig-if-ethernet:ethernet']['state']['counters']['in-fragment-frames']
                if counter:
                    if int(counter) > in_fragment_errors_threshold:
                        table.add_row(self.device.alias,intf['name'],str(in_fragment_errors_threshold),counter,'Failed',style="red")
                        self.failed_interfaces[intf['name']] = int(counter)
                        self.interface_name = intf['name']
                        self.error_counter = self.failed_interfaces[intf['name']]
                    else:
                        table.add_row(self.device.alias,intf['name'],str(in_fragment_errors_threshold),counter,'Passed',style="green")
                else:
                    table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="yellow")           
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interface Input Fragment Frames.svg", title = f"{ self.device.alias } Open Config Interface Input Fragment Frames")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interface Input Fragment Frames.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interface Input Fragment Frames.png")
       
        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The Device { self.device.alias } Has Interface Input Fragment Frames',
                          'files': (f"Test Results/{ self.device.alias } Open Config Interface Input Fragment Frames.png", open(f"Test Results/{ self.device.alias } Open Config Interface Input Fragment Frames.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have input fragment frames')
        else:
            self.passed('No interfaces have input fragment frames')

    @aetest.test
    def test_interface_input_jabber_errors(self):
        # Test for input discards
        in_jabber_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input Jabber Frames")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Jabber Frames Threshold", style="magenta")
        table.add_column("Input Jabber Frames", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'openconfig-if-ethernet:ethernet' in intf:
                counter = intf['openconfig-if-ethernet:ethernet']['state']['counters']['in-jabber-frames']
                if counter:
                    if int(counter) > in_jabber_errors_threshold:
                        table.add_row(self.device.alias,intf['name'],str(in_jabber_errors_threshold),counter,'Failed',style="red")
                        self.failed_interfaces[intf['name']] = int(counter)
                        self.interface_name = intf['name']
                        self.error_counter = self.failed_interfaces[intf['name']]
                    else:
                        table.add_row(self.device.alias,intf['name'],str(in_jabber_errors_threshold),counter,'Passed',style="green")
                else:
                    table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="yellow")           
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interface Input Jabber Frames.svg", title = f"{ self.device.alias } Open Config Interface Input Jabber Frames")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interface Input Jabber Frames.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interface Input Jabber Frames.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } Has Interface Input Jabber Frames',
                          'files': (f"Test Results/{ self.device.alias } Open Config Interface Input Jabber Frames.png", open(f"Test Results/{ self.device.alias } Open Config Interface Input Jabber Frames.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have input jabber frames')
        else:
            self.passed('No interfaces have input jabber frames')

    @aetest.test
    def test_interface_input_mac_pause_errors(self):
        # Test for input discards
        in_mac_pause_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input MAC Pause Frames")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input MAC Pause Frames Threshold", style="magenta")
        table.add_column("Input MAC Pause Frames", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'openconfig-if-ethernet:ethernet' in intf:
                counter = intf['openconfig-if-ethernet:ethernet']['state']['counters']['in-mac-pause-frames']
                if counter:
                    if int(counter) > in_mac_pause_errors_threshold:
                        table.add_row(self.device.alias,intf['name'],str(in_mac_pause_errors_threshold),counter,'Failed',style="red")
                        self.failed_interfaces[intf['name']] = int(counter)
                        self.interface_name = intf['name']
                        self.error_counter = self.failed_interfaces[intf['name']]
                    else:
                        table.add_row(self.device.alias,intf['name'],str(in_mac_pause_errors_threshold),counter,'Passed',style="green")
                else:
                    table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="yellow")           
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interface Input MAC Pause Frames.svg", title = f"{ self.device.alias } Open Config Interface Input MAC PAuse Frames")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interface Input MAC Pause Frames.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interface Input MAC Pause Frames.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } Has Interface Input MAC Pause Frames',
                          'files': (f"Test Results/{ self.device.alias } Open Config Interface Input MAC Pause Frames.png", open(f"Test Results/{ self.device.alias } Open Config Interface Input MAC Pause Frames.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have input MAC Pause frames')
        else:
            self.passed('No interfaces have input MAC Pause frames')

    @aetest.test
    def test_interface_input_oversize_frames_errors(self):
        # Test for input discards
        in_oversize_frames_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input Oversize Frames")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Oversize Frames Threshold", style="magenta")
        table.add_column("Input Oversize Frames", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'openconfig-if-ethernet:ethernet' in intf:
                counter = intf['openconfig-if-ethernet:ethernet']['state']['counters']['in-oversize-frames']
                if counter:
                    if int(counter) > in_oversize_frames_threshold:
                        table.add_row(self.device.alias,intf['name'],str(in_oversize_frames_threshold),counter,'Failed',style="red")
                        self.failed_interfaces[intf['name']] = int(counter)
                        self.interface_name = intf['name']
                        self.error_counter = self.failed_interfaces[intf['name']]
                    else:
                        table.add_row(self.device.alias,intf['name'],str(in_oversize_frames_threshold),counter,'Passed',style="green")
                else:
                    table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="yellow")           
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interface Input Oversize Frames.svg", title = f"{ self.device.alias } Open Config Interface Input Oversize Frames")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interface Input Oversize Frames.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interface Input Oversize Frames.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Input Oversize Frames',
                          'files': (f"Test Results/{ self.device.alias } Open Config Interface Input Oversize Frames.png", open(f"Test Results/{ self.device.alias } Open Config Interface Input Oversize Frames.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have input oversize frames')
        else:
            self.passed('No interfaces have input oversize frames')

    @aetest.test
    def test_interface_output_pause_frames_errors(self):
        # Test for input discards
        in_output_pause_frames_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Output MAC Pause Frames")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Output Output MAC Pause Frames Threshold", style="magenta")
        table.add_column("Output Output MAC Pause Frames", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'openconfig-if-ethernet:ethernet' in intf:
                counter = intf['openconfig-if-ethernet:ethernet']['state']['counters']['out-mac-pause-frames']
                if counter:
                    if int(counter) > in_output_pause_frames_threshold:
                        table.add_row(self.device.alias,intf['name'],str(in_output_pause_frames_threshold),counter,'Failed',style="red")
                        self.failed_interfaces[intf['name']] = int(counter)
                        self.interface_name = intf['name']
                        self.error_counter = self.failed_interfaces[intf['name']]
                    else:
                        table.add_row(self.device.alias,intf['name'],str(in_output_pause_frames_threshold),counter,'Passed',style="green")
                else:
                    table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="yellow")           
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interface Output MAC Pause Frames.svg", title = f"{ self.device.alias } Open Config Interface Output MAC Pause Frames")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interface Output MAC Pause Frames.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interface Output MAC Pause Frames.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Output MAC Pause Frames',
                          'files': (f"Test Results/{ self.device.alias } Open Config Interface Output MAC Pause Frames.png", open(f"Test Results/{ self.device.alias } Open Config Interface Output MAC Pause Frames.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have output MAC pause frames')
        else:
            self.passed('No interfaces have output MAC pause frames')

    @aetest.test
    def test_interface_input_discards(self):
        # Test for input discards
        in_discards_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input Discards")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Discards Threshold", style="magenta")
        table.add_column("Input Discards", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            counter = intf['state']['counters']['in-discards']
            if counter:
                if int(counter) > in_discards_threshold:
                    table.add_row(self.device.alias,intf['name'],str(in_discards_threshold),counter,'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(in_discards_threshold),counter,'Passed',style="green")
            else:
                table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="yellow")           
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interface Input Discards.svg", title = f"{ self.device.alias } Open Config Interface Input Discards")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interface Input Discards.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interface Input Discards.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Input Discards',
                          'files': (f"Test Results/{ self.device.alias } Open Config Interface Input Discards.png", open(f"Test Results/{ self.device.alias } Open Config Interface Input Discards.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have input discards')
        else:
            self.passed('No interfaces have input discards')

    @aetest.test
    def test_interface_input_errors(self):
        # test for interface input errors
        in_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input Discards")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Errors Threshold", style="magenta")
        table.add_column("Input Errors", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            counter = intf['state']['counters']['in-discards']
            if counter:
                if int(counter) > in_errors_threshold:
                    table.add_row(self.device.alias,intf['name'],str(in_errors_threshold),counter,'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(in_errors_threshold),counter,'Passed',style="green")
            else:
                table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="yellow")           
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interface Input Errors.svg", title = f"{ self.device.alias } Open Config Interface Input Errors")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interface Input Errors.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interface Input Errors.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Input Errors',
                          'files': (f"Test Results/{ self.device.alias } Open Config Interface Input Errors.png", open(f"Test Results/{ self.device.alias } Open Config Interface Input Errors.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have input errors')
        else:
            self.passed('No interfaces have input errors')        

    @aetest.test
    def test_interface_input_fcs_errors(self):
        # Test for input fcs errors
        in_fcs_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input FCS Errors")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input FCS Errors Threshold", style="magenta")
        table.add_column("Input FCS Errors", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            counter = intf['state']['counters']['in-fcs-errors']
            if counter:
                if int(counter) > in_fcs_errors_threshold:
                    table.add_row(self.device.alias,intf['name'],str(in_fcs_errors_threshold),counter,'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(in_fcs_errors_threshold),counter,'Passed',style="green")
            else:
                table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="yellow")           
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interface Input FCS Errors.svg", title = f"{ self.device.alias } Open Config Interface Input FCS Errors")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interface Input FCS Errors.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interface Input FCS Errors.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Input FCS Errors',
                          'files': (f"Test Results/{ self.device.alias } Open Config Interface Input FCS Errors.png", open(f"Test Results/{ self.device.alias } Open Config Interface Input FCS Errors.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have input fcs errors')
        else:
            self.passed('No interfaces have input fcs errors') 

    @aetest.test
    def test_interface_input_unknown_protocols(self):
        # Test for input unknown protocols
        in_unknown_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input Unknown Protocols")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Unknown Protocols Threshold", style="magenta")
        table.add_column("Input Unknown Protocols", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            counter = intf['state']['counters']['in-unknown-protos']
            if counter:
                if int(counter) > in_unknown_threshold:
                    table.add_row(self.device.alias,intf['name'],str(in_unknown_threshold),counter,'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(in_unknown_threshold),counter,'Passed',style="green")
            else:
                table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="yellow")           
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interface Input Unknown Protocols.svg", title = f"{ self.device.alias } Open Config Interface Input Unknown Protocols")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interface Input Unknown Protocols.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interface Input Unknown Protocols.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Input Unknown Protocols',
                          'files': (f"Test Results/{ self.device.alias } Input Unknown Protocols.png", open(f"Test Results/{ self.device.alias } Input Unknown Protocols.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have input unknown protocols')
        else:
            self.passed('No interfaces have input unknown protocols')    

    @aetest.test
    def test_interface_output_discards(self):
        # Test for output discards
        out_discards_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Output Discards")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Output Discard Threshold", style="magenta")
        table.add_column("Output Discard", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            counter = intf['state']['counters']['out-discards']
            if counter:
                if int(counter) > out_discards_threshold:
                    table.add_row(self.device.alias,intf['name'],str(out_discards_threshold),counter,'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(out_discards_threshold),counter,'Passed',style="green")
            else:
                table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="yellow")           
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interface Output Discards.svg", title = f"{ self.device.alias } Open Config Interface Output Discards")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interface Output Discards.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interface Output Discards.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Output Discards',
                          'files': (f"Test Results/{ self.device.alias } Open Config Interface Output Discards.png", open(f"Test Results/{ self.device.alias } Open Config Interface Output Discards.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have output discards')
        else:
            self.passed('No interfaces have output discards')

    @aetest.test
    def test_interface_output_errors(self):
        # test for interface output errors
        out_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Output Errors")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Errors Threshold", style="magenta")
        table.add_column("Input Errors", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            counter = intf['state']['counters']['out-discards']
            if counter:
                if int(counter) > out_errors_threshold:
                    table.add_row(self.device.alias,intf['name'],str(out_errors_threshold),counter,'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(out_errors_threshold),counter,'Passed',style="green")
            else:
                table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="yellow")           
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interface Output Errors.svg", title = f"{ self.device.alias } Open Config Interface Output Errors")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interface Output Errors.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interface Output Errors.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Output Errors',
                          'files': (f"Test Results/{ self.device.alias } Open Config Interface Output Errors.png", open(f"Test Results/{ self.device.alias } Open Config Interface Output Errors.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have output errors')
        else:
            self.passed('No interfaces have output errors')

    @aetest.test
    def test_interface_full_duplex(self):
        # test for interface output errors
        duplex_threshold = "FULL"
        self.failed_interfaces = {}        
        table = Table(title="Interface Full Duplex")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Duplex Mode", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'openconfig-if-ethernet:ethernet' in intf:
                counter = intf['openconfig-if-ethernet:ethernet']['state']['negotiated-duplex-mode']
                if counter != duplex_threshold:
                    table.add_row(self.device.alias,intf['name'],counter,'Failed',style="red")
                    self.failed_interfaces[intf['name']] = counter
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],counter,'Passed',style="green")
            else:
                table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="yellow")           
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interfaces Are Full Duplex.svg", title = f"{ self.device.alias } Open Config Interfaces Are Full Duplex")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interfaces Are Full Duplex.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interfaces Are Full Duplex.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interfaces that are not Full Duplex',
                          'files': (f"Test Results/{ self.device.alias } Open Config Interfaces Are Full Duplex.png", open(f"Test Results/{ self.device.alias } Open Config Interfaces Are Full Duplex.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces are not full duplex')
        else:
            self.passed('All interfaces are full duplex')
  
    @aetest.test
    def test_interface_admin_oper_status(self):
    # Test for oper status
        self.failed_interfaces = {}
        table = Table(title="Interface Admin / Oper Status")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Admin Status", style="magenta")
        table.add_column("Oper Status", style="green")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'admin-status' in intf['state']:            
                admin_status = intf['state']['admin-status']
                oper_status = intf['state']['oper-status']
                if oper_status != admin_status:
                    table.add_row(self.device.alias,intf['name'],admin_status,oper_status,'Failed',style="red")
                    self.failed_interfaces[intf['name']] = oper_status
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],admin_status,oper_status,'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interfaces Admin Status Matches Oper Status.svg", title = f"{ self.device.alias } Open Config Interfaces Admin Status Matches Oper Status")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interfaces Admin Status Matches Oper Status.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interfaces Admin Status Matches Oper Status.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interfaces with Admin and Oper Status mismatches',
                          'files': (f"Test Results/{ self.device.alias } Open Config Interfaces Admin Status Matches Oper Status.png", open(f"Test Results/{ self.device.alias } Open Config Interfaces Admin Status Matches Oper Status.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces are admin / oper state mismatch')
        else:
            self.passed('All interfaces admin / oper state match')

    @aetest.test
    def test_interface_description(self):
    # Test for description
        self.failed_interfaces = {}
        table = Table(title="Interface Has Description")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Description", style="magenta")
        table.add_column("Passed/Failed", style="green")        
        for self.intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'description' in self.intf['config']:
                actual_desc = self.intf['config']['description']
                if actual_desc:
                    table.add_row(self.device.alias,self.intf['name'],actual_desc,'Passed',style="green")
                else:
                    table.add_row(self.device.alias,self.intf['name'],actual_desc,'Failed',style="red")
                    self.failed_interfaces = "failed"
            else:
                table.add_row(self.device.alias,self.intf['name'],"N/A",'Failed',style="red")
                self.failed_interfaces = "failed"                                    
    #     # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Table as SVG
        console.save_svg(f"Test Results/{ self.device.alias } Open Config Interfaces Have Descriptions.svg", title = f"{ self.device.alias } Open Config Interfaces Have Descriptions")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Open Config Interfaces Have Descriptions.svg", write_to=f"Test Results/{ self.device.alias } Open Config Interfaces Have Descriptions.png")

    # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } Has Interfaces without Descriptions',
                          'files': (f"Test Results/{ self.device.alias } Open Config Interfaces Have Descriptions.png", open(f"Test Results/{ self.device.alias } Open Config Interfaces Have Descriptions.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)           
            self.failed('Some interfaces have no description')            
        else:
            self.passed('All interfaces have descriptions')

class Test_Cisco_IOS_XE_Interface_Oper(aetest.Testcase):
    """Parse the Cisco IOS XE Interface Oper YANG Model"""

    @aetest.test
    def setup(self, testbed, device_name):
        """ Testcase Setup section"""
        # Loop over devices in tested for testing
        self.device = testbed.devices[device_name]
    
    @aetest.test
    def get_test_yang_data(self):
        # Use the RESTCONF Cisco IOS-XE YANG Model 
        parsed_cisco_ios_xe_interfaces_oper = self.device.rest.get("/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces")
        # Get the JSpayload
        self.parsed_json=parsed_cisco_ios_xe_interfaces_oper.json()

    @aetest.test
    def create_pre_test_files(self):
        # Create .JSfile
        with open(f'JSON/{self.device.alias}_Cisco_IOS_XE_Interfaces_Oper.json', 'w') as f:
            f.write(json.dumps(self.parsed_json, indent=4, sort_keys=True))

    @aetest.test
    def test_interface_description(self):
    # Test for description
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface Has Description")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Description", style="magenta")
        table.add_column("Passed/Failed", style="green")        
        for self.intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'description' in self.intf:
                actual_desc = self.intf['description']
                if actual_desc:
                    table.add_row(self.device.alias,self.intf['name'],actual_desc,'Passed',style="green")
                else:
                    table.add_row(self.device.alias,self.intf['name'],actual_desc,'Failed',style="red")
                    self.failed_interfaces = "failed"
    #     # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Table as SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS XE Interfaces Have Descriptions.svg", title = f"{ self.device.alias } Cisco IOS XE Interfaces Have Descriptions")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS XE Interfaces Have Descriptions.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS XE Interfaces Have Descriptions.png")

    # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } Has Interfaces without Descriptions',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS XE Interfaces Have Descriptions.png", open(f"Test Results/{ self.device.alias } Cisco IOS XE Interfaces Have Descriptions.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)           
            self.failed('Some interfaces have no description')            
        else:
            self.passed('All interfaces have descriptions')

    @aetest.test
    def test_interface_input_crc_errors(self):
        # Test for input crc errors
        in_crc_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface Input CRC Errors")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input CRC Threshold", style="magenta")
        table.add_column("Input CRC Errors", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'in-crc-errors' in intf['statistics']:
                counter = intf['statistics']['in-crc-errors']
                if counter:
                    if int(counter) > in_crc_errors_threshold:
                        table.add_row(self.device.alias,intf['name'],str(in_crc_errors_threshold),counter,'Failed',style="red")
                        self.failed_interfaces[intf['name']] = int(counter)
                        self.interface_name = intf['name']
                        self.error_counter = self.failed_interfaces[intf['name']]
                    else:
                        table.add_row(self.device.alias,intf['name'],str(in_crc_errors_threshold),counter,'Passed',style="green")
                else:
                    table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="yellow")           
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())
        
        # Save table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS XE Interface Input CRC Errors.svg", title = f"{ self.device.alias } Cisco IOS XE Interface Input CRC Errors")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS XE Interface Input CRC Errors.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS XE Interface Input CRC Errors.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The Device { self.device.alias } Has Interface Input CRC Errors',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS XE Interface Input CRC Errors.png", open(f"Test Results/{ self.device.alias } Cisco IOS XE Interface Input CRC Errors.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)
            self.failed('Some interfaces have input CRC errors')
        else:
            self.passed('No interfaces have input CRC errors')

    @aetest.test
    def test_interface_input_discards(self):
        # Test for input discards
        in_discards_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface Input Discards")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Discards Threshold", style="magenta")
        table.add_column("Input Discards", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'in-discards' in intf['statistics']:
                counter = intf['statistics']['in-discards']
                if counter > in_discards_threshold:
                    table.add_row(self.device.alias,intf['name'],str(in_discards_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(in_discards_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Discards.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface Input Discards")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Discards.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Discards.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Input Discards',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Discards.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Discards.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have input discards')
        else:
            self.passed('No interfaces have input discards')

    @aetest.test
    def test_interface_input_discards_64(self):
        # Test for input discards 64
        in_discards_64_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface Input Discards 64")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Discards 64 Threshold", style="magenta")
        table.add_column("Input Discards 64", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'in-discards-64' in intf['statistics']:
                counter = int(intf['statistics']['in-discards-64'])
                if counter > in_discards_64_threshold:
                    table.add_row(self.device.alias,intf['name'],str(in_discards_64_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(in_discards_64_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Discards 64.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface Input Discards 64")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Discards 64.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Discards 64.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Input Discards 64',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Discards 64.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Discards 64.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have input discards 64')
        else:
            self.passed('No interfaces have input discards 64')

    @aetest.test
    def test_interface_input_errors(self):
        # Test for input errors
        in_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface Input Errors")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Errors Threshold", style="magenta")
        table.add_column("Input Errors", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'in-errors' in intf['statistics']:
                counter = intf['statistics']['in-errors']
                if counter > in_errors_threshold:
                    table.add_row(self.device.alias,intf['name'],str(in_errors_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(in_errors_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Errors.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface Input Errors")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Errors.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Errors.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Input Errors',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Errors.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Errors.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have input errors')
        else:
            self.passed('No interfaces have input errors')

    @aetest.test
    def test_interface_input_errors_64(self):
        # Test for input errors 64
        in_errors_64_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface Input Errors 64")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Errors 64 Threshold", style="magenta")
        table.add_column("Input Errors 64", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'in-errors-64' in intf['statistics']:
                counter = int(intf['statistics']['in-errors-64'])
                if counter > in_errors_64_threshold:
                    table.add_row(self.device.alias,intf['name'],str(in_errors_64_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(in_errors_64_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Errors 64.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface Input Errors 64")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Errors 64.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Errors 64.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Input Errors 64',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Errors 64.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Errors 64.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have input errors 64')
        else:
            self.passed('No interfaces have input errors 64')

    @aetest.test
    def test_interface_input_unknown_protocols(self):
        # Test for input unknown-protos
        in_unknown_protocols_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface Input Unknown Protocols")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Unknown Protocols Threshold", style="magenta")
        table.add_column("Input Unknown Protocols", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'in-unknown-protos' in intf['statistics']:
                counter = intf['statistics']['in-unknown-protos']
                if counter > in_unknown_protocols_threshold:
                    table.add_row(self.device.alias,intf['name'],str(in_unknown_protocols_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(in_unknown_protocols_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Unknown Protocols.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface Input Unknown Protocols")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Unknown Protocols.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Unknown Protocols.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Input Unknown Protocols',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Unknown Protocols.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Unknown Protocols.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have input unknown protocols')
        else:
            self.passed('No interfaces have input unknown protocols')

    @aetest.test
    def test_interface_input_unknown_protocols_64(self):
        # Test for input unknown protocols 64
        in_unknown_protocols_64_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface Input Unknown Protocols 64")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Unknown Protocols 64 Threshold", style="magenta")
        table.add_column("Input Unknown Protocols 64", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'in-unknown-protos-64' in intf['statistics']:
                counter = int(intf['statistics']['in-unknown-protos-64'])
                if counter > in_unknown_protocols_64_threshold:
                    table.add_row(self.device.alias,intf['name'],str(in_unknown_protocols_64_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(in_unknown_protocols_64_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Unknown Protocols 64.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface Input Unknown Protocols 64")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Unknown Protocols 64.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Unknown Protocols 64.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Uknown Protocols 64',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Unknown Protocols 64.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Input Unknown Protocols 64.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have input unknown protocols 64')
        else:
            self.passed('No interfaces have input unknown protocols 64')

    @aetest.test
    def test_interface_number_flaps(self):
        # Test for interface flaps
        flaps_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface Flaps")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Flaps Threshold", style="magenta")
        table.add_column("Flaps", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'num-flaps' in intf['statistics']:
                counter = int(intf['statistics']['num-flaps'])
                if counter > flaps_threshold:
                    table.add_row(self.device.alias,intf['name'],str(flaps_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(flaps_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Flaps.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface Flaps")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Flaps.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Flaps.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Flaps',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Flaps.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Flaps.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have flaps')
        else:
            self.passed('No interfaces have flaps')

    @aetest.test
    def test_output_discards(self):
        # Test for output discards
        output_discards_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface Output Discards")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Output Discards Threshold", style="magenta")
        table.add_column("Output Discards", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'out-discards' in intf['statistics']:
                counter = int(intf['statistics']['out-discards'])
                if counter > output_discards_threshold:
                    table.add_row(self.device.alias,intf['name'],str(output_discards_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(output_discards_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Output Discards.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface Output Discards")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Output Discards.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Output Discards.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Output Discards',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Output Discards.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Output Discards.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have output discards')
        else:
            self.passed('No interfaces have output discards')

    @aetest.test
    def test_output_errors(self):
        # Test for output errors
        output_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface Output Errors")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Output Errors Threshold", style="magenta")
        table.add_column("Output Errors", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'out-errors' in intf['statistics']:
                counter = int(intf['statistics']['out-errors'])
                if counter > output_errors_threshold:
                    table.add_row(self.device.alias,intf['name'],str(output_errors_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(output_errors_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Output Errors.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface Output Errors")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Output Errors.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Output Errors.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface Output Errors',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Output Errors.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Output Errors.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have output errors')
        else:
            self.passed('No interfaces have output errors')

    @aetest.test
    def test_v4_protocol_input_discarded_packets(self):
        # Test for v4 protocol input discarded packets
        input_discarded_packets_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface v4 Protocol Input Discard Packets")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Discarded Packet Threshold", style="magenta")
        table.add_column("Input Discarded Packets", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'in-discarded-pkts' in intf['v4-protocol-stats']:
                counter = int(intf['v4-protocol-stats']['in-discarded-pkts'])
                if counter > input_discarded_packets_threshold:
                    table.add_row(self.device.alias,intf['name'],str(input_discarded_packets_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(input_discarded_packets_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Input Discarded Packets.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Input Discarded Packets")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Input Discarded Packets.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Input Discarded Packets.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface v4 Protocol Input Discarded Packets',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Input Discarded Packets.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Input Discarded Packets.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have v4 protocol input discarded packets')
        else:
            self.passed('No interfaces have v4 protocol input discarded packets')

    @aetest.test
    def test_v4_protocol_input_error_packets(self):
        # Test for v4 protocol input error packets
        input_error_packets_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface v4 Protocol Input Error Packets")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Error Packet Threshold", style="magenta")
        table.add_column("Input Error Packets", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'in-error-pkts' in intf['v4-protocol-stats']:
                counter = int(intf['v4-protocol-stats']['in-error-pkts'])
                if counter > input_error_packets_threshold:
                    table.add_row(self.device.alias,intf['name'],str(input_error_packets_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(input_error_packets_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Input Error Packets.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Input Error Packets")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Input Error Packets.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Input Error Packets.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface v4 Protocol Input Error Packets',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Input Error Packets.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Input Error Packets.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have v4 protocol input error packets')
        else:
            self.passed('No interfaces have v4 protocol input error packets')

    @aetest.test
    def test_v4_protocol_output_discarded_packets(self):
        # Test for v4 protocol output discarded packets
        output_discarded_packets_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface v4 Protocol Output Discard Packets")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Output Discarded Packet Threshold", style="magenta")
        table.add_column("Output Discarded Packets", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'out-discarded-pkts' in intf['v4-protocol-stats']:
                counter = int(intf['v4-protocol-stats']['out-discarded-pkts'])
                if counter > output_discarded_packets_threshold:
                    table.add_row(self.device.alias,intf['name'],str(output_discarded_packets_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(output_discarded_packets_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Output Discarded Packets.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Output Discarded Packets")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Output Discarded Packets.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Output Discarded Packets.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface v4 Protocol Output Discarded Packets',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Output Discarded Packets.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Output Discarded Packets.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have v4 protocol output discarded packets')
        else:
            self.passed('No interfaces have v4 protocol output discarded packets')

    @aetest.test
    def test_v4_protocol_output_error_packets(self):
        # Test for v4 protocol output error packets
        output_error_packets_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface v4 Protocol Output Error Packets")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Output Error Packet Threshold", style="magenta")
        table.add_column("Output Error Packets", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'out-error-pkts' in intf['v4-protocol-stats']:
                counter = int(intf['v4-protocol-stats']['out-error-pkts'])
                if counter > output_error_packets_threshold:
                    table.add_row(self.device.alias,intf['name'],str(output_error_packets_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(output_error_packets_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Output Error Packets.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Output Error Packets")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Output Error Packets.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Output Error Packets.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface v4 Protocol Output Error Packets',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Output Error Packets.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v4 Protocol Output Error Packets.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have v4 protocol output error packets')
        else:
            self.passed('No interfaces have v4 protocol output error packets')

    @aetest.test
    def test_v6_protocol_input_discarded_packets(self):
        # Test for v4 protocol input discarded packets
        input_discarded_packets_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface v6 Protocol Input Discard Packets")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Discarded Packet Threshold", style="magenta")
        table.add_column("Input Discarded Packets", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'in-discarded-pkts' in intf['v6-protocol-stats']:
                counter = int(intf['v6-protocol-stats']['in-discarded-pkts'])
                if counter > input_discarded_packets_threshold:
                    table.add_row(self.device.alias,intf['name'],str(input_discarded_packets_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(input_discarded_packets_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Input Discarded Packets.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Input Discarded Packets")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Input Discarded Packets.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Input Discarded Packets.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface v6 Protocol Input Discarded Packets',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Input Discarded Packets.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Input Discarded Packets.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have v6 protocol input discarded packets')
        else:
            self.passed('No interfaces have v6 protocol input discarded packets')

    @aetest.test
    def test_v6_protocol_input_error_packets(self):
        # Test for v6 protocol input error packets
        input_error_packets_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface v6 Protocol Input Error Packets")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Error Packet Threshold", style="magenta")
        table.add_column("Input Error Packets", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'in-error-pkts' in intf['v6-protocol-stats']:
                counter = int(intf['v6-protocol-stats']['in-error-pkts'])
                if counter > input_error_packets_threshold:
                    table.add_row(self.device.alias,intf['name'],str(input_error_packets_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(input_error_packets_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Input Error Packets.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Input Error Packets")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Input Error Packets.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Input Error Packets.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface v6 Protocol Input Error Packets',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Input Error Packets.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Input Error Packets.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have v6 protocol input error packets')
        else:
            self.passed('No interfaces have v6 protocol input error packets')

    @aetest.test
    def test_v6_protocol_output_discarded_packets(self):
        # Test for v6 protocol output discarded packets
        output_discarded_packets_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface v6 Protocol Output Discard Packets")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Output Discarded Packet Threshold", style="magenta")
        table.add_column("Output Discarded Packets", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'out-discarded-pkts' in intf['v6-protocol-stats']:
                counter = int(intf['v6-protocol-stats']['out-discarded-pkts'])
                if counter > output_discarded_packets_threshold:
                    table.add_row(self.device.alias,intf['name'],str(output_discarded_packets_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(output_discarded_packets_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Output Discarded Packets.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Output Discarded Packets")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Output Discarded Packets.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Output Discarded Packets.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface v6 Protocol Output Discarded Packets',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Output Discarded Packets.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Output Discarded Packets.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have v6 protocol output discarded packets')
        else:
            self.passed('No interfaces have v6 protocol output discarded packets')

    @aetest.test
    def test_v6_protocol_output_error_packets(self):
        # Test for v6 protocol output error packets
        output_error_packets_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Cisco IOS-XE Interface v6 Protocol Output Error Packets")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Output Error Packet Threshold", style="magenta")
        table.add_column("Output Error Packets", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
            if 'out-error-pkts' in intf['v6-protocol-stats']:
                counter = int(intf['v6-protocol-stats']['out-error-pkts'])
                if counter > output_error_packets_threshold:
                    table.add_row(self.device.alias,intf['name'],str(output_error_packets_threshold),str(counter),'Failed',style="red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],str(output_error_packets_threshold),str(counter),'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Tabele to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Output Error Packets.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Output Error Packets")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Output Error Packets.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Output Error Packets.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interface v6 Protocol Output Error Packets',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Output Error Packets.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface v6 Protocol Output Error Packets.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces have v6 protocol output error packets')
        else:
            self.passed('No interfaces have v6 protocol output error packets')

    @aetest.test
    def test_interface_admin_oper_status(self):
    # Test for oper status
        self.failed_interfaces = {}
        table = Table(title="Interface Admin / Oper Status")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Admin Status", style="magenta")
        table.add_column("Oper Status", style="green")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:          
            admin_status = intf['admin-status']
            oper_status = intf['oper-status']
            if admin_status == "if-state-up":
                if oper_status != 'if-oper-state-ready':
                    table.add_row(self.device.alias,intf['name'],admin_status,oper_status,'Failed',style="red")
                    self.failed_interfaces[intf['name']] = oper_status
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],admin_status,oper_status,'Passed',style="green")
        # display the table
        console = Console(record=True)
        with console.capture() as capture:
            console.print(table,justify="center")
        log.info(capture.get())

        # Save Table to SVG
        console.save_svg(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Admin Status Matches Oper Status.svg", title = f"{ self.device.alias } Cisco IOS-XE Interface Admin Status Matches Oper Status")

        # Save SVG to PNG
        cairosvg.svg2png(url=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Admin Status Matches Oper Status.svg", write_to=f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Admin Status Matches Oper Status.png")

        # should we pass or fail?
        if self.failed_interfaces:
            if webexToken:
                m = MultipartEncoder({'roomId': f'{ webexRoomId }',
                          'text': f'The device { self.device.alias } has Interfaces with Admin and Oper Status mismatches',
                          'files': (f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Admin Status Matches Oper Status.png", open(f"Test Results/{ self.device.alias } Cisco IOS-XE Interface Admin Status Matches Oper Status.png", 'rb'),
                          'image/png')})

                webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m,
                      headers={'Authorization': f'Bearer { webexToken }',
                      'Content-Type': m.content_type})

                print(f'The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)            
            self.failed('Some interfaces are admin / oper state mismatch')
        else:
            self.passed('All interfaces admin / oper state match')

class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, testbed):
        testbed.disconnect()

# for running as its own executable
if __name__ == '__main__':
    aetest.main()