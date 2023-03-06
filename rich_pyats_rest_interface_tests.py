import json
import logging
from pyats import aetest
from pyats.log.utils import banner
from rich.console import Console
from rich.table import Table

# ----------------
# Get logger for script
# ----------------

log = logging.getLogger(__name__)

# ----------------
# AE Test Setup
# ----------------
class common_setup(aetest.CommonSetup):
    """Common Setup section"""
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
        aetest.loop.mark(Test_Interfaces, device_name=testbed.devices)

# ----------------
# Test Case #1
# ----------------
class Test_Interfaces(aetest.Testcase):
    """Parse the OpenConfig YANG Model - interfaces:interfaces"""

    @aetest.test
    def setup(self, testbed, device_name):
        """ Testcase Setup section """
        # Loop over devices in tested for testing
        self.device = testbed.devices[device_name]
    
    @aetest.test
    def get_test_yang_data(self):
        # Use the RESTCONF OpenConfig YANG Model 
        parsed_openconfig_interfaces = self.device.rest.get("/restconf/data/openconfig-interfaces:interfaces")
        # Get the JSON payload
        self.parsed_json=parsed_openconfig_interfaces.json()

    @aetest.test
    def create_pre_test_files(self):
        # Create .JSON file
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
        table.add_column("Input CRC Errors Counter", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'openconfig-if-ethernet:ethernet' in intf:
                counter = intf['openconfig-if-ethernet:ethernet']['state']['counters']['in-crc-errors']
                if counter:
                    if int(counter) > in_crc_errors_threshold:
                        table.add_row(self.device.alias,intf['name'],counter,'Failed',style="on red")
                        self.failed_interfaces[intf['name']] = int(counter)
                        self.interface_name = intf['name']
                        self.error_counter = self.failed_interfaces[intf['name']]
                    else:
                        table.add_row(self.device.alias,intf['name'],counter,'Passed',style="on green")
                else:
                    table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="on yellow")           
        # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())

        # should we pass or fail?
        if self.failed_interfaces:
            self.failed('Some interfaces have input CRC errors')
        else:
            self.passed('No interfaces have input CRC errors')
    
    @aetest.test
    def test_interface_input_fragment_errors(self):
        # Test for input discards
        in_crc_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input Fragment Frames")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Fragment Frames Counter", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'openconfig-if-ethernet:ethernet' in intf:
                counter = intf['openconfig-if-ethernet:ethernet']['state']['counters']['in-fragment-frames']
                if counter:
                    if int(counter) > in_crc_errors_threshold:
                        table.add_row(self.device.alias,intf['name'],counter,'Failed',style="on red")
                        self.failed_interfaces[intf['name']] = int(counter)
                        self.interface_name = intf['name']
                        self.error_counter = self.failed_interfaces[intf['name']]
                    else:
                        table.add_row(self.device.alias,intf['name'],counter,'Passed',style="on green")
                else:
                    table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="on yellow")           
        # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())
        
        # should we pass or fail?
        if self.failed_interfaces:
            self.failed('Some interfaces have input fragment frames')
        else:
            self.passed('No interfaces have input fragment frames')

    @aetest.test
    def test_interface_input_jabber_errors(self):
        # Test for input discards
        in_crc_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input Jabber Frames")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Jabber Frames Counter", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'openconfig-if-ethernet:ethernet' in intf:
                counter = intf['openconfig-if-ethernet:ethernet']['state']['counters']['in-jabber-frames']
                if counter:
                    if int(counter) > in_crc_errors_threshold:
                        table.add_row(self.device.alias,intf['name'],counter,'Failed',style="on red")
                        self.failed_interfaces[intf['name']] = int(counter)
                        self.interface_name = intf['name']
                        self.error_counter = self.failed_interfaces[intf['name']]
                    else:
                        table.add_row(self.device.alias,intf['name'],counter,'Passed',style="on green")
                else:
                    table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="on yellow")           
        # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())

        # should we pass or fail?
        if self.failed_interfaces:
            self.failed('Some interfaces have input jabber frames')
        else:
            self.passed('No interfaces have input jabber frames')

    @aetest.test
    def test_interface_input_mac_pause_errors(self):
        # Test for input discards
        in_crc_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input MAC Pause Frames")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input MAC Pause Frames Counter", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'openconfig-if-ethernet:ethernet' in intf:
                counter = intf['openconfig-if-ethernet:ethernet']['state']['counters']['in-mac-pause-frames']
                if counter:
                    if int(counter) > in_crc_errors_threshold:
                        table.add_row(self.device.alias,intf['name'],counter,'Failed',style="on red")
                        self.failed_interfaces[intf['name']] = int(counter)
                        self.interface_name = intf['name']
                        self.error_counter = self.failed_interfaces[intf['name']]
                    else:
                        table.add_row(self.device.alias,intf['name'],counter,'Passed',style="on green")
                else:
                    table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="on yellow")           
        # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())

        # should we pass or fail?
        if self.failed_interfaces:
            self.failed('Some interfaces have input MAC Pause frames')
        else:
            self.passed('No interfaces have input MAC Pause frames')

    @aetest.test
    def test_interface_input_oversize_frames_errors(self):
        # Test for input discards
        in_crc_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input Oversize Frames")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Oversize Frames Counter", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'openconfig-if-ethernet:ethernet' in intf:
                counter = intf['openconfig-if-ethernet:ethernet']['state']['counters']['in-oversize-frames']
                if counter:
                    if int(counter) > in_crc_errors_threshold:
                        table.add_row(self.device.alias,intf['name'],counter,'Failed',style="on red")
                        self.failed_interfaces[intf['name']] = int(counter)
                        self.interface_name = intf['name']
                        self.error_counter = self.failed_interfaces[intf['name']]
                    else:
                        table.add_row(self.device.alias,intf['name'],counter,'Passed',style="on green")
                else:
                    table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="on yellow")           
        # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())

        # should we pass or fail?
        if self.failed_interfaces:
            self.failed('Some interfaces have input oversize frames')
        else:
            self.passed('No interfaces have input oversize frames')

    @aetest.test
    def test_interface_output_pause_frames_errors(self):
        # Test for input discards
        in_crc_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Output MAC Pause Frames")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Output MAC Pause Frames Counter", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'openconfig-if-ethernet:ethernet' in intf:
                counter = intf['openconfig-if-ethernet:ethernet']['state']['counters']['out-mac-pause-frames']
                if counter:
                    if int(counter) > in_crc_errors_threshold:
                        table.add_row(self.device.alias,intf['name'],counter,'Failed',style="on red")
                        self.failed_interfaces[intf['name']] = int(counter)
                        self.interface_name = intf['name']
                        self.error_counter = self.failed_interfaces[intf['name']]
                    else:
                        table.add_row(self.device.alias,intf['name'],counter,'Passed',style="on green")
                else:
                    table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="on yellow")           
        # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())

        # should we pass or fail?
        if self.failed_interfaces:
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
        table.add_column("Input Discard Counter", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            counter = intf['state']['counters']['in-discards']
            if counter:
                if int(counter) > in_discards_threshold:
                    table.add_row(self.device.alias,intf['name'],counter,'Failed',style="on red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],counter,'Passed',style="on green")
            else:
                table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="on yellow")           
        # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())

        # should we pass or fail?
        if self.failed_interfaces:
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
        table.add_column("Input Errors Counter", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            counter = intf['state']['counters']['in-discards']
            if counter:
                if int(counter) > in_errors_threshold:
                    table.add_row(self.device.alias,intf['name'],counter,'Failed',style="on red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],counter,'Passed',style="on green")
            else:
                table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="on yellow")           
        # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())

        # should we pass or fail?
        if self.failed_interfaces:
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
        table.add_column("Input FCS Errors Counter", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            counter = intf['state']['counters']['in-fcs-errors']
            if counter:
                if int(counter) > in_fcs_errors_threshold:
                    table.add_row(self.device.alias,intf['name'],counter,'Failed',style="on red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],counter,'Passed',style="on green")
            else:
                table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="on yellow")           
        # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())

        # should we pass or fail?
        if self.failed_interfaces:
            self.failed('Some interfaces have input fcs errors')
        else:
            self.passed('No interfaces have input fcs errors') 

    @aetest.test
    def test_interface_input_unknown_protocols(self):
        # Test for input unknown protocols
        in_unknown_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Input FCS Errors")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Unknown Protocols Counter", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            counter = intf['state']['counters']['in-unknown-protos']
            if counter:
                if int(counter) > in_unknown_threshold:
                    table.add_row(self.device.alias,intf['name'],counter,'Failed',style="on red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],counter,'Passed',style="on green")
            else:
                table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="on yellow")           
        # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())

        # should we pass or fail?
        if self.failed_interfaces:
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
        table.add_column("Output Discard Counter", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            counter = intf['state']['counters']['out-discards']
            if counter:
                if int(counter) > out_discards_threshold:
                    table.add_row(self.device.alias,intf['name'],counter,'Failed',style="on red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],counter,'Passed',style="on green")
            else:
                table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="on yellow")           
        # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())

        # should we pass or fail?
        if self.failed_interfaces:
            self.failed('Some interfaces have output discards')
        else:
            self.passed('No interfaces have output discards')

    @aetest.test
    def test_interface_output_errors(self):
        # test for interface output errors
        in_errors_threshold = 0
        self.failed_interfaces = {}
        table = Table(title="Interface Output Discards")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Input Errors Counter", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            counter = intf['state']['counters']['out-discards']
            if counter:
                if int(counter) > in_errors_threshold:
                    table.add_row(self.device.alias,intf['name'],counter,'Failed',style="on red")
                    self.failed_interfaces[intf['name']] = int(counter)
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],counter,'Passed',style="on green")
            else:
                table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="on yellow")           
        # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())

        # should we pass or fail?
        if self.failed_interfaces:
            self.failed('Some interfaces have output errors')
        else:
            self.passed('No interfaces have output errors')

    @aetest.test
    def test_interface_full_duplex(self):
        # test for interface output errors
        duplex_threshold = "FULL"
        self.failed_interfaces = {}        
        table = Table(title="Interface Output Discards")
        table.add_column("Device", style="cyan")
        table.add_column("Interface", style="blue")
        table.add_column("Duplex Mode", style="magenta")
        table.add_column("Passed/Failed", style="green")
        for intf in self.parsed_json['openconfig-interfaces:interfaces']['interface']:
            if 'openconfig-if-ethernet:ethernet' in intf:
                counter = intf['openconfig-if-ethernet:ethernet']['state']['negotiated-duplex-mode']
                if counter != duplex_threshold:
                    table.add_row(self.device.alias,intf['name'],counter,'Failed',style="on red")
                    self.failed_interfaces[intf['name']] = counter
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],counter,'Passed',style="on green")
            else:
                table.add_row(self.device.alias,intf['name'],'N/A','N/A',style="on yellow")           
        # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())

        # should we pass or fail?
        if self.failed_interfaces:
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
                    table.add_row(self.device.alias,intf['name'],admin_status,oper_status,'Failed',style="on red")
                    self.failed_interfaces[intf['name']] = oper_status
                    self.interface_name = intf['name']
                    self.error_counter = self.failed_interfaces[intf['name']]
                else:
                    table.add_row(self.device.alias,intf['name'],admin_status,oper_status,'Passed',style="on green")
        # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())

        # should we pass or fail?
        if self.failed_interfaces:
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
                    table.add_row(self.device.alias,self.intf['name'],actual_desc,'Passed',style="on green")
                else:
                    table.add_row(self.device.alias,self.intf['name'],actual_desc,'Failed',style="on red")
                    self.failed_interfaces = "failed"
    #     # display the table
        console = Console()
        with console.capture() as capture:
            console.print(table)
        log.info(capture.get())

    # should we pass or fail?
        if self.failed_interfaces:
           self.failed('Some interfaces have no description')            
        else:
            self.passed('All interfaces have descriptions')

class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, testbed):
        testbed.disconnect()

# for running as its own executable
if __name__ == '__main__':
    aetest.main()