import json
from os import name
import sys
from typing import Dict
import socket
from datetime import datetime
from paramiko import SSHClient, AutoAddPolicy, ssh_exception, channel
import getpass
import logging
import re
import time
from typing import Union, List
from tqdm.auto import tqdm


class BadPswdException(Exception):
    def __init__(self, message="Password authenticification failed three times. Programm will be interupted."):
        self.message = message
        super().__init__(self.message)

class MissingPswdError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SSHConnector():
    def __init__(self, ip: str, user: str = "opti", ssh_password:str=None, debug_mode: bool = False): # type: ignore
        """ Initalizing helper values. Creating two different Logger instances to inherit from logger used by Paramiko module and creating own logger. Both are addressing sys.stdout.

        :param ip: IP for executing SSH connection
        :type ip: str
        :param user: Username for executing SSH connection, defaults to "opti"
        :type user: str, optional
        :param ssh_password: Password for SSH connection with host, defaults to None
        :type ssh_password: str, optional
        :param debug_mode: Debug mode which will lower the level of logged entries to DEBUG and helps to find bugs by providing more informations, defaults to False
        :type debug_mode: bool, optional
        """
        self.ip = ip
        self.username = user
        self.ssh_pswd = ssh_password
        self.sudo_pswd = None
        self.paths = {}
   
        # set logger level after user
        msg_mode = logging.DEBUG if debug_mode else logging.INFO
        self._define_paramiko_logger(msg_mode)
        self._create_module_logger(msg_mode)

    def __enter__(self):
        """Contextmanager uses open method to open SSH connection and setting automatically host key policy."""
        self.open()
        return self
    
    def open(self):
        """ Method for initalizing connection to host without contextmanager. Opens connection and sets host key policy automatically."""
        # Open SSH connection
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        # set ssh_pswd
        if not self.ssh_pswd:
            self.ssh_pswd = getpass.getpass(prompt="Add ssh passwort for opti:\n")
        # connect
        self.client.connect(self.ip, username=self.username, password=self.ssh_pswd)

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit method for contextmanager."""
        self.close()
        if exc_type != None:
            self.logger.error(
                f"\nExecution type: {exc_type}\nTraceback: {traceback}")

    def close(self):
        """Closes all still open connections and delets set root password for this session."""
        self.sudo_pswd = None
        self.pswd = None
        self.client.close()
        self.logger.info("SSH connection closed")

    def set_sudo_password(self, sudo_password:str):
        """ Method to set sudo password before executing SSH commands which need root rights

        :param str sudo_password: Sudo password for connected system
        """
        self.sudo_pswd = sudo_password

    def send_command(self, command:str, give_out_stderr:bool=False, timeout:int=None): # type: ignore
        """ Method for easy command handling with SSH terminal. Command will be checked for sudo term. If term is not containing '-S' option, it will be added. In this way, beforehand set sudo password will be flushed to channel.

        :param str command: Command line for linux Terminal
        :param bool give_out_stderr: Flag to give out additional ,defaults to False
        :return List: Terminal response, if command executed wihtout error
        """
        try:
            if not timeout:
                timeout = 3 
            if "sudo" in command:
                if "-S" not in command:
                    command = command.replace("sudo","sudo -S")
            stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
            if "sudo" in command:
                if not self.sudo_pswd:
                    raise MissingPswdError("Sudo password is needed but missing. Please set beforehand.")
                pswd_flush = "".join((str(self.sudo_pswd),"\n")) 
                stdin.write(pswd_flush)
            output = stdout.readlines()
            if give_out_stderr == True:
                err_output = stderr.readlines()
                return output, err_output
            else:
                return output  
        except TimeoutError:
            raise BadPswdException("Command could not be executed, most likely because of password failure. Pls check your sudo password for typos.") 
        
    def _define_paramiko_logger(self, level_mode, stream=sys.stdout):
        """Overwrite already exisitng paramiko logger and adapting it to print out to sys.stdout and log custom message and time, log level.

        :param str level_mode: logging msg mode (e.g. logging.debug) that will be used
        :param stream stream: Stream to which message will be send, defaults to sys.stdout
        """
        #  use paramikos logger
        self.paramiko_logger = logging.getLogger("paramiko")
        # create and define handler to print to std.out
        stdout_channel = logging.StreamHandler(stream=stream)
        stdout_channel.set_name("stdout_channel")
        stdout_channel.setLevel(level_mode)
        logging_FORMAT = logging.Formatter(
            '[%(asctime)s]  %(levelname)s: %(message)s')
        stdout_channel.setFormatter(logging_FORMAT)
        # add handler to logger
        self.paramiko_logger.addHandler(stdout_channel)

    def _create_module_logger(self, level_mode, stream=sys.stdout) -> None:
        """Creates a logger which will print out to sys.stdout and log custom message and time, log level.

        :param level_mode: logging msg mode (e.g. logging.debug)
        :type level_mode: Message level that will be displayed
        """
        logging.basicConfig(stream=stream, level=level_mode,
                            format='[%(asctime)s]  %(levelname)s: %(message)s')
        self.logger = logging.getLogger("SSH_logger")

    def detect_harddrives(self, return_paths=False) -> None:
        """ Searches for path of systemplate(s) and dataplate(s). Paths are saved as class variable or returned by keyword argument.

        :raises ValueError: If no systempath can be estimated.
        :raises ValueError: If zero dataplatepaths can be estimated.
        """
        datapaths = []
        try:
            # find system path
            # search for device which is mounted as /home
            result = self.send_command("df /home -H --output=source")
            if len(result) == 0:
                raise ValueError
            systempath = str(result[1])
            if "\n" in systempath:
                systempath = systempath.strip()
            if systempath[-1].isdigit(): # check for last char: mountpint is /dev/sda3 but for later use we only need sda
                systempath = systempath[:-1]
            self.paths.update({"systempath":systempath}) # type: ignore
            if systempath == None or systempath == "":
                raise ValueError
        except Exception as e:
            self.logger.debug(e)
            self.logger.warning(
                "Automatic detection of systemplate(s) failed. Please check manually.")
        try:
            # find dataplate paths; arbitary amount
            devices = self.send_command("lsblk -o Name,Type,MOUNTPOINT")
            # iterate through all devices
            for dev in devices:
                dev = str(dev)
                if "/data" in dev:
                    name, type, mount = dev.split(" ")
                    # convert name to path
                    path = re.sub(r'\W+','',name) # replace all non alphanumeric characters ('_' is not replaced) 
                    if path[-1].isdigit(): # check for last char: example: mountpoint is sda3 but for later use we only need sda
                        path = path[:-1]
                    path = '/dev/' + path
                    
                    # convert mount
                    mount = mount.strip()
                    datapaths.append((path,mount))
                    
                #if "/home" in dev:
            self.paths.update({"datapaths":datapaths}) # type: ignore
            if len(datapaths) == 0:
                raise ValueError
        except Exception as e:
            self.logger.debug(e)
            self.logger.warning(
                "Automatic detection of dataplate(s) failed. Please check manually.")
        if return_paths:
            return self.paths # type: ignore
 
    def get_harddrive_information(self, device:str, attributes:List=None)    -> Dict: # type: ignore
        """ Function to (partly) read out information from harrddisk, Information origin from smartctl and therefore smartctl has to be isntalled on linux device. 
        
        Following information can be read out:

        * 'SATA_version'
        * 'SATA_linkspeed'
        * 'manufacturer_serial'
        * 'model'
        * 'relocated_areas'
        * 'power_on_hours'
        * 'size'
        * 'health_state'

        :param str device: Device (device path)
        :param List attributes: List with all attribute keywords which should be read out. Without any parsed values, full list of attributes is used, defaults to None
        :return Dict: Dictionary with desired information 
        """
        disk_info = {}
        output = self.send_command("sudo smartctl -a " + device + " --json") # use json format
        
        # output is always list with strings so convert
        output = "".join(output) # type: ignore
        smartctl = json.loads(output) # now json again

        if not attributes:
            attributes = ["SATA_version", "SATA_linkspeed", "manufacturer_serial", "model", "relocated_areas", "power_on_hours", "size", "health_state"]

        
        function_translator= {"SATA_version": self._get_disk_SATA_version, "SATA_linkspeed":self._get_disk_SATA_linkspeed, 
                              "manufacturer_serial":self._get_disk_manufacturer_serial, "model":self._get_disk_model, "relocated_areas":self._get_disk_relocated_areas,
                                "power_on_hours":self._get_disk_power_on_hours, "size":self._get_disk_size, "health_state":self._get_disk_health_state}
        for attr in attributes:
            disk_info.update({str(attr):function_translator[attr](smartctl)})

        return disk_info
    
    def _get_disk_SATA_version(self, smartctl_output) -> str:
        """ Reads out disks SATA Version from smartctl output.

        :param json smartctl_output: Terminal output from "smartctl" command in JSON format
        :raises KeyError: If key is not found and returns empty string and warning.
        :return str: Disk SATA linkspeed version
        """
        try:
            return smartctl_output["sata_version"]["string"]
        except KeyError:
            self.logger.warning("SATA Version could not be read out. Empty string will be returned.")
            return str()

    def _get_disk_SATA_linkspeed(self, smartctl_output) -> str:
        """ Reads out disks SATA linkspeed from smartctl output.

        :param json smartctl_output: Terminal output from "smartctl" command in JSON format
        :raises KeyError: If key is not found and returns empty string and warning.
        :return str: Disk SATA linkspeed ability
        """
        try:
            return smartctl_output["interface_speed"]["current"]["string"]
        except KeyError:
            self.logger.warning("SATA Linkspeed could not be read out. Empty string will be returned.")
            return str()

    def _get_disk_manufacturer_serial(self, smartctl_output) -> str:
        """ Reads out manufacturer serial number from smartctl output

        :param json smartctl_output: Terminal output from "smartctl" command in JSON format
        :raises KeyError: If key is not found and returns empty string and warning.
        :return str: Serial number from manufacturer of disk
        """
        try:
            return smartctl_output["serial_number"]
        except KeyError:
            self.logger.warning("Manufacturer serial could not be read out. Empty string will be returned.")
            return str()

    def _get_disk_model(self, smartctl_output) -> str:
        """ Reads out disk model from smartctl output

        :param json smartctl_output: Terminal output from "smartctl" command in JSON format
        :raises KeyError: If key is not found and returns empty string and warning.
        :return str: Disk model name
        """
        try:
            return smartctl_output["model_name"]
        except KeyError:
            self.logger.warning("Manufacturer serial could not be read out. Empty string will be returned.")
            return str()
        
    def _get_disk_relocated_areas(self, smartctl_output) -> int:
        """ Reads out reloacated areas from smartctl output as health sign from harddrive.

        :param json smartctl_output: Terminal output from "smartctl" command in JSON format
        :raises KeyError: If key is not found and returns empty string and warning.
        :return int: Amount of relocated areas
        """
        try:
            for idx, table_obj in enumerate(smartctl_output["ata_smart_attributes"]["table"]):
                var = table_obj.get("name", None)
                if var == "Reallocated_Sector_Ct":
                    target_idx = idx
                    break
            
            return smartctl_output["ata_smart_attributes"]["table"][target_idx]["raw"]["value"]
        except KeyError:
            self.logger.warning("Relocated areas number could not be read. mpty string will be returned.")
            return str()
        
    def _get_disk_power_on_hours(self, smartctl_output) -> int:
        """ Reads out harddrive power on hours from smartctl ouput.

        :param json smartctl_output: Terminal output from "smartctl" command in JSON format
        :raises KeyError: If key is not found and returns empty string and warning.
        :return int: Power-on hours of disk
        """
        try:
            return smartctl_output["power_on_time"]["hours"]  # hours
        except KeyError:
            self.logger.warning("Power on time in hours could not be read out. Empty string will be returned.")
            return str()
        
    def _get_disk_size(self, smartctl_output) -> str:
        """ Reads out harddrive capacity in Gb from smartctl

        :param json smartctl_output: Terminal output from "smartctl" command in JSON format
        :raises KeyError: If key is not found and returns empty string and warning.
        :return str: Real user usable capacity from disk in Gb
        """
        try:
            size = smartctl_output["user_capacity"]["bytes"] # bytes
            return round(size / 1e+9)
        except KeyError:
            self.logger.warning("Size could not be read out. Empty string will be returned.")
            return str()

    def _get_disk_health_state(self, smartctl_output) -> str:
        """ Get disk health state from smartctl output

        :param json smartctl_output: Terminal output from "smartctl" command in JSON format
        :raises KeyError: If key is not found and returns empty string and warning.
        :return str: Either "healthy" or "logged error state"
        """
        try:
            health = smartctl_output["smart_status"].get("passed", None)
            if health == "true" or health == True:
                return "healthy"
            else:
                return "logged error state"
        except KeyError:
            self.logger.warning("Health state could not be read out. Empty string will be returned.")
            return str()

    def get_BIOS_information(self) -> Dict:
            """Reads out BIOS vendor name, version and fabrication date [keys=vendor,version,date]. Sudo rights required.

            Used module is dmidecode. If required information cannot be read out, a wild warning will appear. In this case return will be empty string.

            :return Dict: BIOS Information
            """
            try:
                bios = self.send_command("sudo dmidecode | grep -A3 'BIOS Information'")
                # build dict from terminal response
                vendor = str(bios[1]).strip() # type: ignore
                version = str(bios[2]).strip() # type: ignore
                date = str(bios[3]).strip() # type: ignore
                # split every info by key value 
                ven_key, ven_val = vendor.split(": ")
                ver_key, ver_val = version.split(": ")
                date_key, date_val = date.split(": ")
                bios_infos = {ven_key: ven_val,
                            ver_key: ver_val, date_key: date_val}
                return bios_infos
            except Exception as e:
                self.logger.debug(e)
                self.logger.warning(
                    "BIOS information could not be read out. Return is empty string.")
                return "" # type: ignore
            
    def get_linux_version(self) -> str:
        """Method to read out Linux Version.

        Information is extracted out /etc/os-release file.If required information cannot be read out, a wild warning will appear. In this case return will be empty string.

        :return str: Linux version
        """
        try:
            # terminal command
            info = self.send_command("cat /etc/os-release | grep 'PRETTY_NAME'") #e.g. ['PRETTY_NAME="openSUSE Leap 15.3"\n']
            _,name,_ = str(info).split(sep='"')
            return name
        except Exception as e:
            self.logger.debug(e)
            self.logger.warning(
                "Could not find Linux version. Return is empty string")
            return ""
    
    def get_CPU_name(self) -> str:
        """Method gets CPU model name. 

        Information is extracted out /proc/cpuinfo file. If required information cannot be read out, a wild warning will appear. In this case return will be empty string.

        :return str: CPU model name
        """
        try:
            # terminal command line
            cmd_info = self.send_command("cat /proc/cpuinfo | grep 'model name' | uniq") 
            #e.g. ['model name\t: AMD Ryzen 7 5700G with Radeon Graphics\n']
            _, cpu = str(cmd_info[0]).split(": ")
            return cpu
        except Exception as e:
            self.logger.debug(e)
            self.logger.warning(
                "CPU Name could not be read out. Return is empty string.")
            return ""

    def get_IP_address(self) -> str:
        """Reads out IP address.

        Information is extracted by terminal command "hostname -I". If required information cannot be read out, a wild warning will appear. In this case return will be empty string.

        :return str: IP address in local network
        """
        # find analyzer_ip
        try:
            ip = self.send_command("hostname -I") #e.g.['192.168.3.241 \n']
            ip = str(ip[0]).strip()
            return ip
        except Exception as e:
            self.logger.debug(e)
            self.logger.warning(
                "IP address could not be read out. Return is empty string.")
            return ""

    def get_RAM_size(self) -> str:
        """Reads out RAM size in Gb. 

        Information is extracted out /proc/meminfo file. If required information cannot be read out, a wild warning will appear. In this case return will be empty string.

        :return str: RAM memory size
        """
        try:
            # terminal command
            cmd_info = self.send_command("cat /proc/meminfo | grep 'MemTotal'")
            # filter for size only
            total_ram_kB = int("".join(filter(str.isdigit, str(cmd_info))))
            # converting to GB
            return round(total_ram_kB / (1024*1024), 2) # type: ignore
        except Exception as e:
            self.logger.debug(e)
            self.logger.warning(
                "RAM memory could not be read out. Return is empty string")
            return ""

    def get_FPGA_version(self) -> str:
        """ Method gets FPGA version.

        Information is extracted out /sys/class/qass/info file. If required information cannot be read out, a wild warning will appear. In this case return will be empty string.

        :return str: CPU model name
        """
        try:
            # terminal command line
            cmd_info = self.send_command("cat /sys/class/qass/info | grep 'FPGA Version'")
            _, fpga = str(cmd_info[0]).split(": ")
            return fpga
        except Exception as e:
            self.logger.debug(e)
            self.logger.warning(
                "FPGA version could not be read out. Return is empty string.")
            return ""

    def get_hardware_information(self, systempath:str=None, datapaths:List=None)  -> Dict: # type: ignore
        """ Function to get all ready-to-use hardware information from connected device per SSH. See Example file to see dictionary structure and keys.

        :param str systempath: Optional way to set datapaths if auto detection failed. Parsed argument should be tuple (device_path, mountpoint), defaults to None
        :param List datapaths: Optional way to set datapaths if auto detection failed. List should contain tuples with (device_path, mountpoint), defaults to None
        :return Dict: Dictionary with all ready-to-use hardware information
        """
        # datapaths List with tuple (path,mountpoint)
        self.detect_harddrives()
        # get path to system disk # choose auto path or set by hand
        if systempath:
            systemdisk_path = systempath
        else:
            systemdisk_path = self.paths.get("systempath", None)
        
        # get datadisk paths and infos
        datadisk_info = []
        # choose auto path or set by hand
        if datapaths:
            datadisk_paths = datapaths
        else:
            datadisk_paths = self.paths["datapaths"]
        
        # Create dict for all datadisks
        for path, mountpoint in datadisk_paths:
            disk = {"device_path": path,
                "mountpoint": mountpoint,
                #"infos": self.get_harddrive_information(path)}
                }
            disk.update(self.get_harddrive_information(path))
            datadisk_info.append(disk)

        # create dict with all remaining informationa nd append datadisk dict
        system_dict = { "device_path": systemdisk_path,
                            "mountpoint": "/home"}
        system_dict.update(self.get_harddrive_information(systemdisk_path))
        info = {
            "CPU_name": self.get_CPU_name(),
            "IP_address": self.get_IP_address(),
            "linux_version": self.get_linux_version(),
            "RAM_size_Gb": self.get_RAM_size(),
            "FPGA_version": self.get_FPGA_version(),
            "systemdisk": system_dict,
                           # "infos": self.get_harddrive_information(systemdisk_path)},
            "datadisk": datadisk_info}
        
        return info
    
    def export_to_json(self, export_dict: Dict, filename:str = None) -> None:
        """ Function exports parsed dictionary to a JSON file. If not set by hand, auto filename and path will be set to optimizer hostname and creation date,
        located in the same directory as python script.

        :param str export_dict: Dictionary that should be exported to local file.
        :param str filename: Possible filename (+ path if needed) for export JSON. Optional, default to None
        """
        if not filename:
            cmd_info = self.send_command("hostname")
            analyzer_hostname = str(cmd_info[0]).replace("\n", "")
            time_now = datetime.now()
            # reconstruct
            date_string = time_now.strftime("_%Y-%m-%d_%H-%M-%S")
            file_name = analyzer_hostname + date_string + ".json"
        else:
            if not filename.endswith(".json"):
                filename = filename + ".json"
            file_name = filename
        with open(file_name, 'w') as file:
            json.dump(export_dict, file)