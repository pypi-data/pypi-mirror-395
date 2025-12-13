# fmt: off
import socket
from typing import Any
from pathlib import Path
from functools import wraps
import json
import numpy as np
from enum import Enum, IntEnum
from typing import Dict, List, Union
import logging
import sys
import re
import threading
import queue
from collections import defaultdict
from retry import retry
import warnings
from packaging import version

def required_version(min_: Union[str, None] = None, max_: Union[str, None] = None):
    """Wrapper to check the Analyzer4D version before executing a command
    This wrapper only works for methods of the AnalyzerRemote class and will
    throw an error if used in other objects.

    :param min_: The minimum version as a string in the format "01.01.01.01"
    :param max_: The maximum version as a string in the format "01.01.01.01"
    """
    def inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            conn = args[0]
            assert isinstance(conn, AnalyzerRemote), "First argument was not an AnalyzerRemote object"
            if not conn.check_version(min_, max_):
                current_version = conn.get_analyzer_version()
                raise AnalyzerVersionError("For this command the Analyzer4D version must be "
                                           f"{'>=' + min_ if min_ is not None else ''}"
                                           f"{' ' if min_ is not None else ''}"
                                           f"{'<=' + max_ if max_ is not None else ''}"
                                           f"{' ' if max_ is not None else ''}"
                                           f"but was {current_version}")
            res = f(*args, **kwargs)
            return res
        return wrapper
    return inner

class Amplitudes(Enum):
    """ Enum class to list and check available amplitudes in mV to generate sine wave.""" 
    AMP_64_mV = 64
    AMP_128_mV = 128
    AMP_191_mV = 191
    AMP_255_mV = 255
    AMP_318_mV = 318
    AMP_382_mV = 382
    AMP_446_mV = 446
    AMP_509_mV = 509
    AMP_573_mV = 573
    AMP_637_mV = 637
    AMP_700_mV = 700
    AMP_764_mV = 764
    AMP_828_mV = 828
    AMP_891_mV = 891
    AMP_955_mV = 955


class Channels(IntEnum):
    """ Available selection box choices for channel in multiplexer configuration that will be addressed""" 
    CHANNEL_1 = 0
    CHANNEL_2 = 1
    CHANNEL_3 = 2
    CHANNEL_4 = 3


class ChannelPorts(IntEnum):
    """ Available selection box choices for channel port in multiplexer configuration that will be addressed""" 
    CHANNEL_PORT_1 = 0
    CHANNEL_PORT_2 = 1
    CHANNEL_PORT_3 = 2
    CHANNEL_PORT_4 = 3
    CHANNEL_PORT_5 = 4
    CHANNEL_PORT_6 = 5
    CHANNEL_PORT_7 = 6
    CHANNEL_PORT_8 = 7
    CHANNEL_VIRT_PORT_9 = 8
    CHANNEL_VIRT_PORT_10 = 9
    CHANNEL_VIRT_PORT_11 = 10
    CHANNEL_VIRT_PORT_12 = 11
    CHANNEL_VIRT_PORT_13 = 12
    CHANNEL_VIRT_PORT_14 = 13
    CHANNEL_VIRT_PORT_15 = 14
    CHANNEL_VIRT_PORT_16 = 15
    CHANNEL_NOT_USED = 17


class PreampPorts(IntEnum):
    """ Available selection box choices for preamplifier port in multiplexer configuration that will be addressed""" 
    PREAMP_PORT_1 = 0
    PREAMP_PORT_2 = 1
    PREAMP_PORT_3 = 2
    PREAMP_PORT_4 = 3
    PREAMP_PORT_5 = 4
    PREAMP_PORT_6 = 5
    PREAMP_PORT_7 = 6
    PREAMP_PORT_8 = 7


class Samplerates16Bit(IntEnum):
    """ Available selection box choices for used samplerate in multiplexer configuration""" 
    SAMPLERATE_100_MHz = 0
    SAMPLERATE_50_MHz = 1
    SAMPLERATE_25_MHz = 2
    SAMPLERATE_12_MHz = 3
    SAMPLERATE_6_MHz = 4
    SAMPLERATE_3_MHz = 5
    SAMPLERATE_1600_kHz = 6
    SAMPLERATE_800_kHz = 7
    SAMPLERATE_400_kHz = 8
    SAMPLERATE_200_kHz = 9
    SAMPLERATE_100_kHz = 10


class ExactSamplerates16Bit(IntEnum):
    """ Available exact samplerates in Hz with 16 Bit ADC.

    .. warning:: These values are just for calculations and cannot be used within AnalyzerRemote functions""" 
    SAMPLERATE_100_MHz = 100000e3
    SAMPLERATE_50_MHz = 50000e3
    SAMPLERATE_25_MHz = 25000e3
    SAMPLERATE_12_MHz = 12500e3
    SAMPLERATE_6_MHz = 6250e3
    SAMPLERATE_3_MHz = 3125e3
    SAMPLERATE_1600_kHz = 1562.5e3
    SAMPLERATE_800_kHz = 781.25e3
    SAMPLERATE_400_kHz = 390.63e3
    SAMPLERATE_200_kHz = 195.31e3
    SAMPLERATE_100_kHz = 97.66e3


class ExactSamplerates24Bit(IntEnum):
    """ Available exact samplerates in Hz with 24 Bit ADC.

    .. warning:: These values are just for calculations and cannot be used within AnalyzerRemote functions""" 
    SAMPLERATE_4_MHz = 4000e3
    SAMPLERATE_2_MHz = 2000e3
    SAMPLERATE_1_MHz = 1000e3
    SAMPLERATE_500_kHz = 500e3
    SAMPLERATE_250_kHz = 250e3
    SAMPLERATE_125_kHz = 125e3
    SAMPLERATE_60_kHz = 160.5e3
    SAMPLERATE_30_kHz = 30.25e3


class FFTOversampling(IntEnum):
    """ Available selection box choices for used oversampling in multiplexer configuration""" 
    FFT_OVERSAMPLING_2_TIMES = 1
    FFT_OVERSAMPLING_4_TIMES = 2
    FFT_OVERSAMPLING_8_TIMES = 3
    FFT_OVERSAMPLING_16_TIMES = 4
    FFT_OVERSAMPLING_32_TIMES = 5
    FFT_OVERSAMPLING_64_TIMES = 6
    NONE_FFT_OVERSAMPLING = 0


class FFTWindowing(IntEnum):
    """ Available selection box choices for used windowing function in multiplexer configuration""" 
    FFT_WINDOWING_HANNING = 0
    NONE_FFT_WINDOWING = 1


class FFTLogarithmic(IntEnum):
    """ Available selection box choices for displayed FFT logarithmic base in multiplexer configuration""" 
    FFT_LOGARITHMIC_BASE_1 = 1
    FFT_LOGARITHMIC_BASE_2 = 2
    FFT_LOGARITHMIC_BASE_3 = 3
    FFT_LOGARITHMIC_BASE_4 = 4
    FFT_LOGARITHMIC_BASE_5 = 5
    FFT_LOGARITHMIC_BASE_6 = 6
    FFT_LOGARITHMIC_BASE_7 = 7
    FFT_LOGARITHMIC_BASE_8 = 8
    FFT_LOGARITHMIC_BASE_9 = 9
    FFT_LOGARITHMIC_BASE_10 = 10
    FFT_LOGARITHMIC_BASE_11 = 11
    FFT_LOGARITHMIC_BASE_12 = 12
    FFT_LOGARITHMIC_BASE_13 = 13
    FFT_LOGARITHMIC_BASE_14 = 14
    FFT_LOGARITHMIC_BASE_15 = 15
    FFT_LOGARITHMIC_BASE_16 = 16
    NO_FFT_LOGARITHMIC_BASE = 0


class SysAmplitudesType(IntEnum):
    """ System amplitude types available in analyzer software. Helps to represent calculated
    maximum amplitudes in different styles.""" 
    AMPLITUDE_DEFAULT = 0
    #: Amplitude is original ADC output value from hardware
    AMPLITUDE_ADC_OUT = 1
    #: Amplitude is normalized energy value. (timedif x frqdif x normalized amplitude)
    AMPLITUDE_NORM_ENERGY = 2
    #: Amplitude normalized to 1 as full ADC value:
    AMPLITUDE_NORM_ONE = 3
    AMPLITUDE_MILLI_VOLT = 4
    AMPLITUDE_MICRO_VOLT = 5


class AreaViews(IntEnum):
    """ Available view possibilities in analyzer area view.""" 
    VIEW_1 = 1
    VIEW_2 = 2
    VIEW_3 = 3
    VIEW_4 = 4


class SysSettingsClass(IntEnum):
    """ Predefined system settings classes.""" 
    
    #: Wird zur Zeit auch per Voreinstellung in "./config/QASS/analyzer.conf" gespeichert
    NO_CLASS = 0 	
    #: Das ist die Default-Klasse für pVars, die in einem VarSet untergebracht sind
    VAR_SET_CLASS = 1
    #: Die Variable enthält System-Einstellungen, die später auch in ".config/QASS" gespeichert werden
    SYSTEM_CONFIG = 2
    USER_CONFIG = 3     # doc: Wird in "./config/QASS/analyzer.conf" in der USER Sektion gespeichert
    GLOBAL_TRIGGER_CONFIG = 4     # doc: Globale Triggereinstellung
    GLOBAL_MEASURE_CONFIG = 5     # doc Globale MeasureConfig Einstellung
    MEASURE_CONFIG = 6     # doc: MeasureConfig Struktur
    CLIENT_CONFIG = 7     # doc: Branding und application Start Einstellungen
    VIDEO_CONFIG = 8     # doc: This is a configuration Setting for a CAM or VideoRecording
    COLOR_CONFIG = 9
    NETWORK_CONFIG = 10    # doc: A network configuration
    FPGA_CONFIG = 11
    PR_SEARCH_CONFIG = 12
    GUI_CONFIG = 13    # doc: global GUI and StyleSheet settings
    SIM_BUFFER_CONFIG = 14    # doc: Configuration of Simulation files
    BACKUP_CONFIG = 15  # doc: Configuration for backups and automatic backups


class MultiPreampInput(IntEnum):
    """ Enums for Multi Input Preamps. The numeration starts on the uppest left input and goes rowise from left to right, too the lowest input (right side).""" 
    NONE_MULTI_INPUT = 999  # doc: Just a flag, to not use any input values. No internal anlyzer link!
    MULTI_INPUT_1 = 0
    MULTI_INPUT_2 = 1
    MULTI_INPUT_3 = 2
    MULTI_INPUT_4 = 3
    MULTI_INPUT_5 = 4
    MULTI_INPUT_6 = 6

class PreampType(IntEnum):
    """ Serial Number Ring for supported Preamp Types."""
    PASSIVE = 2023
    ACTIVE  = 2113

class ReceiverThreadError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class ConnectionError(Exception):
    def __init__(self, message):
        self.message = message 

    def __str__(self):
        return self.message
    
class AnalyzerError(RuntimeError):
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message  


class AnalyzerVersionError(Exception):
    pass

   
class ReceiveThread(threading.Thread):
    """ Receiving thread which runs due to contextmanager the whole time and listens to analyzer socket for responses.
    Responses will be processed and parsed to a callback function (regular: adds response to queue for main thread to fetch te data.""" 

    def __init__(self, socket_obj, logger_obj, suppress_cb_exceptions=True, group=None, target=None, name=None, args=()):
        threading.Thread.__init__(self, group, target, name, args)
        self.lock = threading.RLock()
        self.__callbacks = defaultdict(list)
        self.s = socket_obj
        self.logger = logger_obj
        #self.daemon = True
        self._suppress_cb_exceptions = suppress_cb_exceptions

    def warn_none_registered_response(self, message):
        """ Warning is used when a not expected or not registered message comes in from analyzer. A warning is send out and the message will be logged.""" 
        new_message = "Not registered analyzer response:" + str(message)
        self.logger.warning(new_message)

    def register_callbacks(self, recognition: Union[str, int], callback) ->  None:
        """ Function to register incoming analyzer response by msg_id or cmd name.
        Parsed callback will be registered by adding it as recognition-callback pair to a dict self.__callbacks.

        A MultiDict is used here which by default creates a list for every dict entry (basically a key-list-pair).
        So it is possible to store mutiple callbacks for one recognition.

        :param recognition: Recognition to identify message.
        :type recognition: str, int
        :param callback: Callback to handle response value. Receives the response as an argument.
        :type callback: function
        """ 
        with self.lock:
            self.__callbacks[recognition].append(callback)
            self.logger.debug(f"Registered (user) callback '{callback}' for key: {recognition}")

    def deregister_callbacks(self, recognition: Union[str, int], user_callback=None) ->  None:
        """ Remove registered callback.

        Due to the used MultiDict we have to check if only one callback has to be removed or the complete entry.

        :param recognition: Recognition to identify message.
        :type recognition: str, int
        :param user_callback: Deregister , defaults to None
        :type user_callback: function, optional
        """ 
        with self.lock:
            if user_callback:
                self.__callbacks[recognition].remove(user_callback)
                self.logger.debug(f"Deregistered user callback '{user_callback}' for key: {recognition}")
                if len(self.__callbacks[recognition]) == 0:
                    self.__callbacks.pop(recognition)
                    self.logger.debug(f"All user callbacks for key: {recognition} removed.")
            else:
                self.__callbacks.pop(recognition)
                self.logger.debug(f"Deregistered key: {recognition}")

    def handle_response(self, response, encoding_style="utf-8") ->  None:
        """ Handles every complete message. Handling means decoding the byte string to dict and apply the response to every registered callback.
        Therefore the response is not in unit form, we need an if block which handles recognition over cmd name and message id

        :param response: Complete analyzer response
        :type response: bytes string
        :param encoding_style: Encoding style used from Json module, defaults to "utf-8"
        :type encoding_style: str, optional
        """ 
        self.logger.debug(response)
        # change appearance
        response = response.decode(encoding_style)
        response = json.loads(response)
        callbacks = None

        # handle cases
        with self.lock:
            # case start_operator: sends a second message which has no cmd entry
            # if "cmd" not in response.keys() and "operator" in response.keys() and "finished" in response.keys():
            #         callbacks = self.__callbacks[response["operator"]]
            #         self.deregister_callbacks(callbacks)
            #         return
            
            # loop for supported key words trough response and save corresponding Callbacks 
            for v in ['cmd', 'resid', 'msgid']:
                if v in response:
                    # case for all AppCmds: reponse contains cmd but it is not unique--> has to use resid or msgid
                    if response[v] == "responseappcmd":
                        continue
                    callbacks = self.__callbacks[response[v]] # option to take also a MultiDict and use getlist metod
                    break
            # if key is not found in response warn
            if callbacks is None:
                # incooming messages wich are not registered will be just logged as warning
                self.warn_none_registered_response(response)
            else:
                # execute all callback functions
                for cb in callbacks:
                    try:
                        cb(response)
                    # catch exceptions which are related to bugs in parsed custom_callbacks
                    except Exception as e:
                        import traceback
                        exc_str = traceback.format_exception(e)
                        traceback.print_exception(e)
                        self.logger.error(exc_str)
                        self.logger.error(e)
                        # supress
                        if not self._suppress_cb_exceptions:
                            raise
    
    def handle_error(self, error):
        """ Small method to directly parse error to main thread. Therefore in open method of main thread there is a error callback registered."""
        # build mini command
        response = {'cmd': "error", 'kind': error}
        # callback is a put in queue
        callback = self.__callbacks[response['cmd']]
        for cb in callback:
            cb(response)

    def run(self) ->  None:
        """ Overriden run method of thread module will be executed as the thread starts.

        Method listens to socket in forever loop 'till kill_thread method is executed. Listens for small parts and puts messages together.
        If complete, messsage is parsed it is forwarded to the handle_response method.
        """ 
        current_len = 0
        buffer = bytearray()
        READ_SIZE = 4
        #self.run_thread = False
        #while not self.run_thread:
        self.kill = False
        while not self.kill:
            try:
                buffer.extend(self.s.recv(READ_SIZE))
            # catch socket.error mistakes
            except socket.error as e:
                if not self.kill:
                    self.logger.error(e)
                    if int.from_bytes(buffer, byteorder='big') > 0:
                        self.logger.warning("Unfinished message received:\n")
                        self.logger.warning(buffer)
                    # parse error to mainthread and go on listening
                    self.handle_error(ConnectionError("Connection to Analyzer4D software is lost. Please check connection avaibility of both devices."))
            # only enter for new current length setting or if message is complete
            while (len(buffer) >= current_len and len(buffer) != 0 and current_len != 0) or (current_len == 0 and len(buffer) >= 2):
                # initial incomming message length set as new current length
                if current_len == 0 and len(buffer) >= 2:
                    # every two first characters of a message are the incoming length
                    current_len = int.from_bytes(buffer[:2], byteorder='big')
                    # cut length away
                    buffer = buffer[2:]
                # if message is complete
                if len(buffer) >= current_len:
                    # seperate message
                    response = buffer[:current_len]
                    # handle response
                    self.handle_response(response)
                    # throw handled part away
                    buffer = buffer[current_len:]
                    # reset current_length
                    current_len = 0

    def kill_thread(self) ->  None:
        """ End forever loop in run method.""" 
        #self.daemon = True
        self.logger.info("Receiver thread is now closed.")
        self.join()


class AnalyzerRemote():
    """ Class provides methods for external analyzer control (system operator independant) over a TCP socket. Every method that gets a response is able to set a custom timeout for analyzer reponse. Should any kind of bugs happen without TCP socket crashing, Queue timeout will run into failstate. """ 

    def __init__(self, ip: str, port:int=17000, debug_mode:bool=False, timeout:int=4, suppress_cb_exceptions:bool=True, auto_stop:List=None):
        """ Constructor provides helper and creates logger module.

        :param ip: Analyzer IP in network.
        :type ip: str
        :param port: Required Analyzer port, by the default always 17000.
        :type port: int
        :param debug_mode: Logs debug messages into sys.stdout
        :type debug_mode: bool
        :param timeout: Sets global timeout for queue object in seconds, default is 4
        :type timeout: (pos) int 
        :param suppress_cb_exceptions: Flag to supress raised exceptions in callback functions, default True
        :type suppress_cb_exceptions: bool
        :param auto_stop: Parse list with commands to auto stop certain services started in Analyzer4D Software, by exit with statement, defaults to None
        :type auto_stop: List

        
        ==================  ==========================================================================================================================================
        auto_stop commands  services
        ==================  ==========================================================================================================================================
        all                 Activate service to send command for stopping beforehand remote startet service: measuring, monitoring, sine generator, operator functions
        measuring           Activate service to stop remote started measuring
        sineGen             Activate service to stop remote started sine generator
        monitoring          Activate service to stop remote started monitoring
        operatorFunctions   Activate service to stop remote started operator function output
        analyzer_version    Version number of connected Analyzer
        ==================  ========================================================================================================================================== 
        
        """
        # helper
        self.ip = ip
        self.port = port
        self.timeout = timeout # seconds
        self.error = False
        self.suppress_cb_exceptions = suppress_cb_exceptions
        # message ID to assign command to analyzer and specific response
        self.msgid = 0
        self.translator = {True: "true", "start": "true", "true": "true",
                           "beginn": "true", "enabled": "true", "enable": "true", "on": "true",
                           False: "false", "stop": "false", "end": "false", "disabled": "false",
                           "false": "false", "disable": "false", "off": "false", "monitor": "monitor"}
        # flags for exit method of context manager
        self._io_report_count = 0
        self.auto_stop = auto_stop
        self._proc_report_count = 0
        self._appvar_report_count = 0
        self._measuring_active = False
        self._sine_gen_active = False
        self._monitoring_active = False
        self._operator_functions_active = False
        self._analyzer_version = None
        self.q = queue.Queue()
        
        # short solution logger to sys.stdout
        if debug_mode:
            logging_level = logging.DEBUG
        else:
            logging_level = None
        logging.basicConfig(stream=sys.stdout, level=logging_level,
                            format='[%(asctime)s]  %(levelname)s: %(message)s')
        self.logger = logging.getLogger("networking")
   
    def __enter__(self):
        """Method to wrap open method behaviour for working with a contextmanager. Will open the connection to the Analyzer Instance and start a receiver thread.
        """ 
        self.open()
        return self

    def open(self):
        """Connects the machine to an analyzer reachable over user-given Input of IP (self.ip) and Port (self.port) via TCP and returns an instance of the class. Additionally a second thread (called receiving thread) will be started. This thread will run until close method will kill recieve thread. Every method contains the possibility to parse a custom timeout. This timeout value in second is determining when the queu waiting for results from the ReceiverThread runs into failstate.
        """
        # connect to socket
        self._connecting_analyzer()

        # create thread instance
        self.__recv_thread = ReceiveThread(self.s, self.logger, suppress_cb_exceptions=self.suppress_cb_exceptions,
                                           group=None, target=None, name="receive thread")
        self.__recv_thread.daemon = True
        # start thread
        self.__recv_thread.start()
        # Register simple put in queue callback for error messages
        def callback(result, queue_var=self.q): return queue_var.put(result)
        self.__recv_thread.register_callbacks('error', callback)
        
    def close(self):
        """ Method to close the TCP socket and stop the receiver thread. Settet flags will be checked for safe closing of all started analyzer features."""
  
        # save exit and stop all running services if wished
        if self.auto_stop:
            if "all" in self.auto_stop:
                if self._measuring_active:
                    self._value_parser(expect_response=False, cmd="AppCmd", p1="stopMeasuring")
                if self._sine_gen_active:
                    self._value_parser(expect_response=False, cmd="AppCmd", p1="StopSineGen")
                if self._monitoring_active:
                    self._value_parser(expect_response=False, cmd="startmonitoring", p1="false")
                if self._operator_functions_active:
                    self._value_parser(expect_response=False, cmd="stoppoperatorfunctionvalues")
            if "sineGen" in self.auto_stop and self._sine_gen_active:
                self._value_parser(expect_response=False, cmd="AppCmd", p1="StopSineGen")
            if "measuring" in self.auto_stop and self._measuring_active:
                self._value_parser(expect_response=False, cmd="AppCmd", p1="stopMeasuring")
            if "monitoring" in self.auto_stop and self._monitoring_active:
                self._value_parser(expect_response=False, cmd="startmonitoring", p1="false")
            if "operatorFunctions" in self.auto_stop and self._operator_functions_active:
                self._value_parser(expect_response=False, cmd="stoppoperatorfunctionvalues")

        self.__recv_thread.kill = True
        self.logger.debug("Receiver Thread Closed")
        #self.__recv_thread.kill_thread()
        self.s.close()
        del self.s
        self.logger.info("Socket connection closed")
        
    @retry(ConnectionError, tries=4, delay=1)
    def _connecting_analyzer(self):
        """ Method to create a TCP socket connection with socket address(ip and port) from constructor

        Retry decorator will retry method calls if a ConnectionError occurs. Here set delay layes by 1 second and
        decorator will try again for four times before giving up.

        :raises ConnectionError: Connection error is raisen if no connection can be established.
        """ 
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.settimeout(None)
            self.s.connect((self.ip, self.port))
            self.logger.info("Connected to optimizer")
        except (socket.timeout, socket.error):
            self.logger.error(f"Connection to ip: {self.ip} on port: {self.port} could not be established.\n")
            raise ConnectionError(f"Connection to ip: {self.ip} on port: {self.port} could not be established.\n")
        except KeyboardInterrupt as e:
            self.logger.error(e)
            self.__exit__(exc_type=e)

    def __exit__(self, exc_type, exc_value, traceback):
        """ If contextmanager is left, close method is called.
        """ 
        if exc_type != None:
            self.logger.error(f"\nExecution type: {exc_type}\nTraceback: {traceback}")
        self.close()   

    @property
    def get_socket_ip(self):
        """ Property that gives out connected IP.

        :rtype: str
        """ 
        return self.ip

    @property
    def get_socket_port(self):
        """ Property that gives out connected Port.

        :rtype: int
        """ 
        return self.port

    @property
    def get_measuring_state(self):
        """ Property that gives out if measuring has been started remotely.

        :rtype: boolean
        """ 
        return self._measuring_active

    @property
    def get_monitoring_state(self):
        """ Property that gives out if monitoring has been started remotely.

        :rtype: boolean
        """ 
        return self._monitoring_active

    @property
    def get_sine_gen_state(self):
        """ Property that gives out if sine generator has been activated remotely.

        :rtype: boolean
        """ 
        return self._sine_gen_active

    @property
    def get_operator_functions_state(self):
        """ Property that gives out if operator functions has been activated remotely.

        :rtype: boolean
        """ 
        return self._operator_functions_active

    @property
    def get_translator(self):
        """ Returns supported keys from translator

        :rtype: List
        """ 
        return self.translator.keys()

    
    def set_global_function_timeout(self, timeout:int) -> None:
        """Sets the global timeout for all function to a higher value. Single function can further be overwritten by custom_timeout."""
        self.timeout = timeout

    def get_analyzer_version(self):
        """
        Checks if analyzer version is already determined and saved in self._analyzer_version.
        Otherwise get_project_info() is used to determine the analyzer version

        :raises ConnectionError: Raises if determination of version number fails
        :rtype: str

        """
        if self._analyzer_version is None:
            project_info = self.get_project_info()
            if 'analyzerversion' in project_info:
                self._analyzer_version = project_info['analyzerversion']
            else:
                raise ConnectionError("Analyzer Version determination failed!")
        return self._analyzer_version

    def check_version(self, minimum_needed_version:Union[str,None]=None, maximum_supported_version:Union[str,None]=None):
        """ Method checks if the version of the connected Analyzer is larger equal to the minimum_needed_version and smaller equal the maximum_supported_version. Ignores minimum_needed_version or maximum_supported_version when they are None.  Determines the analyzer version with get_analyzer_version() 
        
        :param minimum_needed_version: minimum Analyzer Version needed to use feature. can have different structure than actual version(more or less numbers). 
        :type project_name: str, optional

        :param maximum_supported_version: maximum Analyzer Version that supports feature. can have different structure than actual version(more or less numbers). 
        :type project_name: str, optional
        
        :rtype: bool
        """     
        version_analyzer = version.parse(self.get_analyzer_version())
        if minimum_needed_version is not None:
            if version_analyzer < version.parse(minimum_needed_version):
                return False
        if maximum_supported_version is not None:
            if version_analyzer > version.parse(maximum_supported_version):
                return False

        return True


    def start_measuring(self, custom_timeout=None) -> None:
        """ Method sends a command to the connected analyzer to start a measuring process.
        
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="AppCmd", p1="startMeasuring", user_timeout=custom_timeout)
        self._measuring_active = True

    def start_sineGenerator(self, frequency: int, amplitude: Union[int, str, Amplitudes], expert:bool=False, custom_timeout=None) -> None:
        """ Method to start sine wave generation with custom frequency and amplitude settings.

        .. warning:: Sine generator has to be already switched on!
        
        .. note:: Note that you should consider that the sine generator needs a couple of µs to start.

        :param int frequency: Used frequency to generate sine wave with in Hz. The suitable range is between 50Hz and 1200Hz (not considerd experts).
        :param amplitude: Used amplitude to generate sine wave in mV (e.g. 955, 'AMP_955_mV' or Amplitudes.AMP_955_mV). Only discrete amplitude values are valid.
        :type amplitude: int, str, Amplitudes
        :param bool expert: Expert mode to disable all user safety structure. Auto evaluation of supported amplitudes and sine waves is disabled.
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :raises ValueError: Set amplitude has to be equal to an int, string or object of class Amplitudes. The frequency value has to to be valid. If exception is raised the program is terminated.
        """ 
        if not expert:
            min_frequency = 50
            max_frequency = 1200

            if (frequency >= min_frequency and frequency <= max_frequency) != True:
                self.logger.error(f'SineGenerator will not be started! Frequency of {frequency}Hz is not in the range of {min_frequency}Hz...{max_frequency}Hz.')
                raise ValueError

        if isinstance(amplitude, int):
            if any(x.value == amplitude for x in Amplitudes):
                pass
            else:
                self.logger.error(f'SineGenerator will not be started! Amplitude {amplitude} is not supported.')
                raise ValueError
        elif isinstance(amplitude, str):
            if any(x.name == amplitude for x in Amplitudes):
                amplitude = Amplitudes[amplitude].value
            else:
                self.logger.error(f'SineGenerator will not be started! Amplitude {amplitude} is not supported.')
                raise ValueError
        elif isinstance(amplitude, Enum):
            if any(x.name == str(amplitude.name) for x in Amplitudes):
                amplitude = amplitude.value
            else:
                self.logger.error(f'SineGenerator will not be started! Amplitude {amplitude} is not supported.')
                raise ValueError
        else:
            self.logger.error(f'SineGenerator will not be started! Amplitude {amplitude} is not supported.')
            raise ValueError

        self._value_parser(cmd="AppCmd", p1="StartSineGen", p2=f"{frequency} {amplitude}")
        self.logger.info(f"Sine generator started with f={frequency}Hz and {amplitude}mV amplitude.")
        self._sine_gen_active = True
        
    def stop_sineGenerator(self, custom_timeout=None) -> None:
        """ Stops generating sine waves.
        
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="AppCmd", p1="StopSineGen", user_timeout=custom_timeout)
        self._sine_gen_active = False

    def stop_measuring(self, custom_timeout=None) -> None:
        """ Method to stop a currently running measurement.
        
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="AppCmd", p1="stopMeasuring", user_timeout=custom_timeout)
        self._measuring_active = False

    def set_process_comment(self, proc_number:int, proc_comment: str, custom_timeout=None) -> None:
        """ Set a process comment for the parsed process. Parsed string will be saved in database under entry: process.comment

        :param proc_number: Process which should get the comment, identified by process number
        :param proc_number: int
        :param proc_comment: Text which should be seen and saved as process comment
        :type proc_comment: str
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="AppCmd", p1="setprocesscomment", p2=f"{proc_number} {proc_comment}", user_timeout=custom_timeout)

    def set_area_view(self, split: int, custom_timeout=None) -> None:
        """ Set analyzer view to a split view with up to 4 different splitted process. Reversed process to change back to
        single view.

        :param split: Amount of splitted area views. Limited to 4.
        :type split: int
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :raises ValueError: Raises if split lays out of bounds
        """ 
        if 0 < split <= 4:
            self._value_parser(user_timeout=custom_timeout, cmd="AppCmd", p1="SetAreaViews", p2=split)
        else:
            self.logger.error("Split amount vor view is out of bounds.")
            raise ValueError("Split amount vor view is out of bounds.")

    def save_area_view(self, template_num: int, custom_timeout=None) -> None:
        """ Saves current area view settings under template number. Each template can be set differently.

        :param template_num: Storage number to save.
        :type template_num: int
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="AppCmd", p1="SaveAreaView", p2=template_num, user_timeout=custom_timeout)
            
    def load_area_view(self, template_num: int, custom_timeout=None) -> None:
        """ Load presaved (!) area view template.

        :param template_num: Storage number to load.
        :type template_num: int
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="AppCmd", p1="LoadAreaView", p2=template_num, user_timeout=custom_timeout)
            
    def load_simulation_buffer(self, file_path: str, channel: int, do_not_copy_meta_data=False, custom_timeout=None) -> None:
        """ Load and set local simulation buffer for specific channel.

        .. warning:: AppCmds are user functions and due to that not null based. Implemented IntEnums are code based and have to be added by one each.

        :param file_path: Local file path to buffer.
        :type file_path: str
        :param channel: Channel where simulationbuffer gets loaded.
        :type channel: int
        :param do_not_copy_meta_data: Identical to analyzer check box, defaults to False
        :type do_not_copy_meta_data: bool, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 

        # AppCmds are user functions and due to that not null based. Implemented IntEnums are code based and have to be added by one each.
        channel += 1
        if do_not_copy_meta_data:
            p2_string = f"channel {channel} nometa path {file_path}"
        else:
            p2_string = f"channel {channel} path {file_path}"
        self._value_parser(cmd="AppCmd", p1="SimulationBuffer", p2=p2_string, user_timeout=custom_timeout)

    def set_simulation_buffer(self, channel_number: Union[str, int, ChannelPorts], mode: str, custom_timeout=None) -> None:
        """ Enable or disable already loaded simualtion buffer channel.

        :param channel_number: Channel to activate simualtion buffer on. Beside normal input, key "all" is supported.
        :type channel_number: str or int or ChannelPorts
        :param mode: If channel should be "enabled" or "disabled" as sim buffer. Check Translator dict for more keywords.
        :type mode: str
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        if channel_number == "all":
            self._value_parser(cmd="AppCmd", p1="SimulationBuffer", p2=f"path {self.translator[mode]}", user_timeout=custom_timeout)
        else:
            channel_number += 1
            self._value_parser(cmd="AppCmd", p1="SimulationBuffer", p2=f"channel {channel_number} {self.translator[mode]}", user_timeout=custom_timeout)

    def start_pulsetest_channel(self, channel_number: Union[int, Channels], gain: int = 800, count: int = 1, delay: int = 0, custom_timeout=None) -> None:
        """ External set of pulse test. Only avaible for exisiting ports and sensors.

        .. warning:: AppCmds are user functions and due to that not null based. Implemented IntEnums are code based and have to be added by one each.

        :param channel_number: Channel where pulsetest gets executed.
        :type channel_number: int or Channels
        :param gain: Used gain for pulsetest, defaults to 800
        :type gain: int, optional
        :param count: Used count for pulsetest, defaults to 1
        :type count: int, optional
        :param delay: Used delay for pulsetest, defaults to 0
        :type delay: int, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :raises ValueError: If gain is out of bounds: range(0,4096) | If count is out of bounds: range(0,200) | If delay is out of bounds: smaller zero
        """ 

        # AppCmds are user functions and due to that not null based. Implemented IntEnums are code based and have to be added by one each.
        channel_number += 1

        # check params limits
        if not 0 <= gain < 4096 and not 0 <= count < 201 and not 0 <= delay:
            self.logger.error("Params out of bounds")
            raise ValueError("Params out of bounds")

        p2_string = f"channel {channel_number} pulsetest {gain} {count} {delay}"
        self._value_parser(cmd="AppCmd", p1="Preamp", p2=p2_string, user_timeout=custom_timeout)
                               
    def start_pulsetest_port(self, port_number: Union[int, PreampPorts], gain: int = 800, count: int = 1, delay: int = 0, multi_preamp_input: Union[int, MultiPreampInput] = MultiPreampInput.NONE_MULTI_INPUT, custom_timeout=None) -> None:
        """ External set of pulse test. Only avaible for exisiting ports and sensors.

        .. warning:: AppCmds are user functions and due to that not null based. Implemented IntEnums are code based and have to be added by one each.

        :param port_number: Port where pulsetest gets executed.
        :type port_number: int or PreampPorts
        :param gain: Pulsetest gain in range(0,4096,  defaults to 800
        :type gain: int
        :param count: Pulsetest count in range(0,200,  defaults to 1
        :type count: int
        :param delay: Pulsetest delay in ms, defaults to 0
        :type delay: int
        :param multi_preamp_input: Input number for Multi Input Preamps, defaults to NONE. Default case is useable for none MultiInput Premaps.
        :type multi_preamp_input: int or MultiPreampInputs
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :raises ValueError: If gain is out of bounds: range(0,4096) | If count is out of bounds: range(0,200) | If delay is out of bounds: smaller zero
        """ 
        # ..warning AppCmds are user functions and due to that not null based. Implemented IntEnums are code based and have to be added by one each.
        port_number += 1

        # check params limits
        if not 0 <= gain < 4096 and not 0 <= count < 201 and not 0 <= delay:
            self.logger.error("Params out of bounds")
            raise ValueError("Params out of bounds")

        if multi_preamp_input == MultiPreampInput.NONE_MULTI_INPUT:
            p2_string = f"port {port_number} pulsetest {gain} {count} {delay}"
        else:
            # ..warning AppCmds are user functions and due to that not null based. Implemented IntEnums are code based and have to be added by one each.
            multi_preamp_input += 1
            p2_string = f"port {port_number} {multi_preamp_input} pulsetest {gain} {count} {delay}"
        self._value_parser(cmd="AppCmd", p1="Preamp", p2=p2_string, user_timeout=custom_timeout)

    def change_preamp_input(self, opti_port_number: Union[int, PreampPorts], preamp_input_number: Union[int, MultiPreampInput] = MultiPreampInput.MULTI_INPUT_2, custom_timeout=None) -> None:
        """ Method changes which physical preamp input will be used for datastream output to optimizer. Only avaible for multi input preamps.

        .. warning:: AppCmds are user functions and due to that not null based. Implemented IntEnums are code based and have to be added by one each.

        :param opti_port_number: opti port number to adress
        :type opti_port_number: int or PreampPorts
        :param preamp_input_number: Switched input channel from preamp (target,  defaults to MULTI_INPUT_2
        :type preamp_input_number: int or MultiPreampInput
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        # ..warning AppCmds are user functions and due to that not null based. Implemented IntEnums are code based and have to be added by one each.
        opti_port_number += 1
        preamp_input_number += 1
        self._value_parser(cmd="AppCmd", p1="Preamp", p2=f"port {opti_port_number} switchinput {preamp_input_number}", user_timeout=custom_timeout)

    def start_frequency_test_port(self, port_number: Union[int, PreampPorts], multi_preamp_input: Union[int, MultiPreampInput] = MultiPreampInput.NONE_MULTI_INPUT, custom_timeout=None) -> None:
        """ Execute a frequency test for a specific port.

        .. warning:: AppCmds are user functions and due to that not null based. Implemented IntEnums are code based and have to be added by one each.

        :param port_number: Port number for frequency test
        :type port_number: int or PreampPorts
        :param preamp_input: Used Input
        :type preamp_input: int or MultiPreampInput, defaults to NONE_MULTI_INPUT for no multi input preamp
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 

        # ..warning AppCmds are user functions and due to that not null based. Implemented IntEnums are code based and have to be added by one each.
        port_number += 1
        if multi_preamp_input == MultiPreampInput.NONE_MULTI_INPUT:
            self._value_parser(cmd="AppCmd", p1="Preamp", p2=f"port {port_number} frqtest", user_timeout=custom_timeout)
        else:
            # ..warning AppCmds are user functions and due to that not null based. Implemented IntEnums are code based and have to be added by one each.
            multi_preamp_input += 1
            self._value_parser(cmd="AppCmd", p1="Preamp", p2=f"port {port_number} input {multi_preamp_input} frqtest", user_timeout=custom_timeout)

    def start_frequency_test_channel(self, channel_number: Union[int, Channels], custom_timeout=None) -> None:
        """ Execute a frequency test for a specific port. Analyzer isn't resonsing in any way (not in a visual, acoustic or information way).

        .. warning:: AppCmds are user functions and due to that not null based. Implemented IntEnums are code based and have to be added by one each.

        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :param port_number: Channel number for frequency test
        :type port_number: int or Channels
        """ 
        # ..warning AppCmds are user functions and due to that not null based. Implemented IntEnums are code based and have to be added by one each.
        channel_number += 1
        self._value_parser(cmd="AppCmd", p1="Preamp", p2=f"channel {channel_number} frqtest", user_timeout=custom_timeout)

    def set_area_scale(self, area_number: int, scale: int = 500, custom_timeout=None) -> None:
        """ Set scale of each view area. Available for splitted analyzer view and single view. In case of single view area_number equals one.

        Scale should be in range(10,1001) | Area number should be in range(1,5), but is limited to current activated area views.

        :param area_number: Which area should be addressed
        :type area_number: int
        :param scale: which scale should be used, defaults to 500
        :type scale: int, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :raises ValueError: If parsed variables are out of bounds. See extended function summary.
        """ 
        if scale in range(10, 1001) and 0 < area_number <= 4:
             self._value_parser(cmd="AppCmd", p1="SetAreaScale", p2=f"{area_number} {scale}", user_timeout=custom_timeout)
        else:
            self.logger.error(
                "Choosen key is out of bounds. Scale should be in range(10,1001) and area number should be in range(1,5).")
            raise ValueError(
                "Choosen key is out of bounds. Scale should be in range(10,1001) and area number should be in range(1,5).")

    def set_area_colour(self, area_number: int, colour_scale: int = 200, custom_timeout=None) -> None:
        """ Set the colour scale for area view. Only available in area. 
        
        Colour scale should be in range(10,401) | Area should be in range(1,5)

        :param area_number: Which area should be addressed
        :type area_number: int
        :param colour_scale: which scale should be used, defaults to 200
        :type colour_scale: int, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :raises ValueError: If parsed variables are out of bounds. See extended function summary.
        """ 
        if colour_scale in range(10, 401) and 0 < area_number <= 4:
             self._value_parser(cmd="AppCmd", p1="SetAreaColor", p2=f"{area_number} {colour_scale}", user_timeout=custom_timeout)
        else:
            self.logger.error(
                "Choosen key is out of bounds. Scale should be in range(10,401) and area number should be in range(1,5).")
            raise ValueError(
                "Choosen key is out of bounds. Scale should be in range(10,401) and area number should be in range(1,5).")

    def set_area_time_range(self, area_number: int, start_time: int, time_range: int, custom_timeout=None) -> None:
        """ Set of shown time range for each area.

        :param area_number: Area which should be addressed
        :type area_number: int
        :param start_time: Start point of time range in ms.
        :type start_time: int
        :param time_range: Range that will be shown from start_time in ms.
        :type time_range: int
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="AppCmd", p1="SetAreaPosition", p2=f"{area_number} {start_time} {time_range}", user_timeout=custom_timeout)

    def load_process(self, process_number: int, start_time=0, custom_timeout=None) -> None:
        """ Load and display by process number.

        :param process_number: Process that will be loaded
        :type process_number: int
        :param start_time: Start time in ms, defaults to 0
        :type start_time: int, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="AppCmd", p1="LoadProcess", p2=f"{process_number} {start_time}", user_timeout=custom_timeout)
                           
    def get_service_parameter(self, param_setting: str, custom_timeout=None) -> str:
        """ Get Values from Service Parameter (Configuration->Settings->Parameter)
        
        .. note:: Only avaible for user level 8 or higher!

        :param param_setting: Service parameter that should be read
        :type param_setting: str
        :return: Current set service parameter value
        :rtype: str
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        settings =  self._value_parser(cmd="appfunc", p1="GetServiceParameter", p2=param_setting, user_timeout=custom_timeout)
        return settings.get("result")

    def set_service_parameter(self, param_setting: str, param_value: any, custom_timeout=None) -> None:
        """ Set Parameter in Service Parameter (Configuration->Settings->Parameter)
        
        .. note:: Only avaible for user level 8 or higher!

        :param param_setting: Service parameter that should be set
        :type param_setting: str
        :param param_value: New value of choosen service parameter
        :type param_value: any
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="AppCmd", p1="setServiceParameter", p2=f"{param_setting} {param_value}", user_timeout=custom_timeout)
        self.logger.info(
            f"Service parameter {param_setting} is changed to {param_value}")

    def send_analyzer_to_sleep(self, time=2000, custom_timeout=None) -> None:
        """ Only testing purpose. Command to send Analyzer system in sleep mode.

        :param time: Time to sleep in ms, defaults to 2000
        :type time: int, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="AppCmd", p1="sysSleep", p2=time, user_timeout=custom_timeout)
        self.logger.info("Analyzer tired. Analyzer sleep.")

    def set_appvar(self, appvar_name: str, appvar_value: Any, custom_timeout=None, storeevent: bool = False) -> None:
        """ Set the value of an AppVar by using the name of the AppVar. The prefix `pro_` will result in the AppVar being saved in the project and persist between restarts. The prefix `sys_` will result in the AppVar being saved globally and made available over all projects.

        If the AppVar doesn't exist yet it will be created.

        :param app_var_name: Name of the AppVar.
        :type app_var_name: str
        :param app_var_value: Value of AppVar. The type can be every datatype supported by python (e.g. float, int, str, json, ...).
        :type app_var_value: Any
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :param storeevent: Whether to save this update as a process event in the Analyzer4D database (Only available for Analyzer4D > V2.07.14.00)
            The eventtype will be the name of the appvar and the eventdata the value. Every write to the appvar will result in a process event,
            even if the value did not change.
        :type storeevent: bool, optional
        """ 
        self._value_parser(cmd="setappvar", p1=appvar_name, p2=appvar_value, storeevent=storeevent, user_timeout=custom_timeout)

    def get_appvar(self, appvar_name: str, custom_timeout=None) -> str:
        """ Get AppVar value by name.
        
        .. note: If requested Appvar is a json, the parsed value will be changed due to string escape.
        
        :param app_var_name: Name of AppVar to adress.
        :type app_var_name: str
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :return: AppVar value
        :rtype: str
        """ 
        val =  self._value_parser(cmd="getappvar", p1=appvar_name, user_timeout=custom_timeout)

        return val.get('result')

    def remove_appvar(self, appvar_name: str, custom_timeout=None) -> None:
        """ Clear and remove AppVar by name.

        :param appvar_name: Name of AppVar to remove.
        :type appvar_name: str
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="clearappvar", p1=appvar_name, user_timeout=custom_timeout)

    def remove_appvar_report_callback(self, callback, custom_timeout=None) -> None:
        """ Removes specific callback function from AppVar report callback list. By removing all callbacks the report function will be automatically stopped.

        :param callback: Callback function that should be removed from AppVar report functionalities.
        :type callback: function
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self.__recv_thread.deregister_callbacks(
            "responseappvars", callback)
        self._appvar_report_count -= 1
        self.logger.info(
            f"Callback {callback} for AppVar report removed")
        if self._appvar_report_count == 0:
            self._value_parser(cmd="reportappvars", p1="false", user_timeout=custom_timeout)
            self.logger.info("Report of AppVar stopped.")

    def add_appvar_report_callback(self, callback, custom_timeout=None) -> None:
        """ Add callback function to report of AppVar. Everytime a AppVar changes, added callback functions will be executed. See networking_example.py for an example. By adding first callback the report start automatically und will be stopped by removing all callbacks due to remove function. Beside the executed callback, analyzer sends state of all AppVars as information by every change.

        .. warning:: All callbacks need as first param "result" to catch analyzer response, if used or not.

        :param callback: Added callback function when report happens.
        :type callback: function
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        if self._appvar_report_count == 0:
             self._value_parser(user_callback=callback, cmd="reportappvars", p1="true", user_timeout=custom_timeout)
        else:
            self.__recv_thread.register_callbacks(
                "responseappvars", callback)
        self._appvar_report_count += 1
        self.logger.info(
            f"Callback {callback} for AppVar report added")

    def get_process_number(self, custom_timeout=None) -> int:
        """ Returns current process number (active buffer).

        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :return: Process number of selected process
        :rtype: int
        """ 
        obj =  self._value_parser(cmd="getprocessnumber", user_timeout=custom_timeout)

        return obj.get("processnumber")

    def create_project(self, project_name: str, custom_timeout=None) -> None:
        """ Create new project after used template with custom name.

        .. note:: Name size has to be at least 4. Avoid spaces or other typical forbidden characters in the project name.

        :param project_name: Name of new project
        :type project_name: str
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="createloadproject", p1=project_name, user_timeout=custom_timeout)

    def send_appcmd(self, param_one: str, param_two=None, custom_timeout=None) -> None:
        """ General method to send arbitrary AppCmd to analyzer.

        .. warning:: Developer function. Do not use without prior knowledge about AppCmds!

        :param param_one: AppCmd
        :type param_one: str
        :param param_two: If needed second parameter to specify params used in AppCmd, defaults to None
        :type param_two: str, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :raises TypeError: Type Check for second parameter, exception is raised if value is not equal to type str.
        """ 
        if param_two:
            if isinstance(param_two, str):
                 self._value_parser(cmd="AppCmd", p1=param_one, p2=param_two, user_timeout=custom_timeout)
            else:
                raise TypeError("Second parameter has to be a string.")
        else:
             self._value_parser(cmd="AppCmd", p1=param_one, user_timeout=custom_timeout)

    def set_multiplexer(self, channel=Channels.CHANNEL_1, chp=ChannelPorts.CHANNEL_PORT_1, preampport=PreampPorts.PREAMP_PORT_1,
                        fft=True, signal=False, samplerate=Samplerates16Bit.SAMPLERATE_1600_kHz, fftoversampling=FFTOversampling.FFT_OVERSAMPLING_8_TIMES,
                        fftwindowing=FFTWindowing.FFT_WINDOWING_HANNING, fftlogarithmic=FFTLogarithmic.FFT_LOGARITHMIC_BASE_14, filter=True, gain=800, subport=-1) ->  None:
        """ Method to set preamplifier and multiplexer settings.

        .. warning:: Range of params will not be checked.

        :param channel: Desired channel (Dropdown,  defaults to Channels.CHANNEL_1
        :type channel: int or Channels, optional
        :param chp: Desired channelport (Dropdown,  defaults to ChannelPorts.CHANNEL_PORT_1
        :type chp: int or Channelports, optional
        :param preampport: Which Preampport should be used, defaults to PreampPorts.PREAMP_PORT_1
        :type preampport: int or PreampPorts, optional
        :param fft: Checkbox if fft buffer should be recorded, defaults to True
        :type fft: bool, optional
        :param signal: Checkbox if signal buffer should be recorded, defaults to False
        :type signal: bool, optional
        :param samplerate: Desired samplerate (Dropdown) defaults to Samplerates16Bit.SAMPLERATE_1600_kHz
        :type samplerate: int or Samplerates16Bit, optional
        :param fftoversampling: Desired FFTOversampling (Dropdown,  defaults to FFTOversampling.FFT_OVERSAMPLING_8_TIMES
        :type fftoversampling: int or FFTOversampling, optional
        :param fftwindowing: Desired FFTOversampling (Dropdown,  defaults to FFTWindowing.FFT_WINDOWING_HANNING
        :type fftwindowing: int or FFTWindowing, optional
        :param fftlogarithmic: Desired FFTLogarithmic (Dropdown,  defaults to FFTLogarithmic.FFT_LOGARITHMIC_BASE_14
        :type fftlogarithmic: int or FFTLogarithmic, optional
        :param filter: If frequency filter should be set, defaults to True
        :type filter: bool, optional
        :param gain: Gain of Preamp, defaults to 800
        :type gain: int, optional
        :param subport: Desired Subport (Dropdown). Should only be used with MultiinputPreamps!, defaults to -1
        :type subport: int, optional
        """ 
        self._value_parser(cmd="setpreamp", expect_response=False, channel=channel, chp=chp, preampport=preampport, fft=fft, signal=signal, samplerate=samplerate,
                           fftoversampling=fftoversampling, fftwindowing=fftwindowing, fftlogarithmic=fftlogarithmic, filter=filter, gain=gain, subport=subport)

    def get_analyzer_versions(self, custom_timeout=None) -> str:
        """ Method to read out anlyzer version informations and return as string. Information are identical to in-software "about" button.

        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :return: Information out of info window in analyzer.
        :rtype: str
        """ 
        val =  self._value_parser(cmd="getversions", user_timeout=custom_timeout)
        # process response
        analyzer_info = val.get("v")
        while "\\n" in analyzer_info:
            analyzer_info = analyzer_info.replace("\\n", "\n")

        return analyzer_info

    def get_project_info(self, custom_timeout=None) -> Dict:
        """ Method to read out analyzer project informations as current used project ID/name or analyzer version.

        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :return: Information about current project.
        :rtype: dict [with dict.keys() = ['analyzerbcdversion', 'analyzerversion', 'projectid', 'projectname', 'pronameprojectid', 'unixtime']]

        """ 
        project_info =  self._value_parser(cmd="getinfo", user_timeout=custom_timeout)

        # process response
        project_info.pop("v")
        project_info.pop("cmd")
        project_info.pop("resid")
        project_info.pop("millisecondpart")

        return project_info

    def get_heartbeat(self, custom_timeout=None) -> bool:
        """ Checks if the little guy is still there.

        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :return: True if message comes back.
        :rtype: bool
        """ 
        val =  self._value_parser(cmd="heartbeat", user_timeout=custom_timeout)
        # process response
        if val:
            self.logger.info("No worries. I'm still alive.")
            return True

    def set_measuring_mode(self, mode: Union[bool, str]) -> None:
        """ Start or stop a measurement. Additionally mode provides possibility to start monitoring mode.

        Supported 'mode' keys: True, bool     | Start measuring
        Supported 'mode' keys: False, bool    | Stop measuring
        Supported 'mode' keys: 'monitor', str | Start monitoring

        .. list-table:: Supported modes
            :widths: 15 10 25
            :header-rows: 1

            * - Key
              - Value datatype
              - Measuring mode
            * - True
              - bool
              - Start measuring
            * - False
              - bool
              - Stop measuring
            * - "monitor"
              - bool
              - Start monitoring
            * - ["start", "true", "beginn", "enabled", "enable", "on"]        
              - str
              - Start measuring
            * - ["stop", "false", "end", "disabled", "disable", "off"]
              - str
              - Stop measuring 

        :param mode: Choosen measuring mode out of table above.
        :type mode: str, bool
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :raises KeyError: if keyword argument "mode" is parsed with invalid values.
        """ 
        self._value_parser(cmd="startmeasuring", expect_response=False, p1=self.translator[mode])
        # flags for context manager exit method
        if self.translator[mode] == "true":
            self._measuring_active = True
        elif self.translator[mode] == "false":
            self._measuring_active = False
        elif self.translator[mode] == "monitor":
            self._monitoring_active = True

    def set_monitoring_mode(self, mode: Union[bool, str], custom_timeout=None) -> None:
        """ Start or stop monitoring modus. When in doubt, check documentation.

        Supported 'mode' keys: True, bool     | Start monitoring
        Supported 'mode' keys: 'False', bool  | Stop monitoring

        .. list-table:: Supported modes
            :widths: 15 10 25
            :header-rows: 1

            * - Key
              - Value datatype
              - Measuring mode
            * - True
              - bool
              - Start monitoring
            * - False
              - bool
              - Stop monitoring
            * - ["start", "true", "beginn", "enabled", "enable", "on"]        
              - str
              - Start monitoring
            * - ["stop", "false", "end", "disabled", "disable", "off"]
              - str
              - Stop monitoring 

        :param mode: Switch between start monitoring (True) or stop monitoring (False). For supported keys see translator.
        :type mode: str, bool
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :raises KeyError: if keyword argument "mode" is parsed with invalid values.
        """ 
        self._value_parser(cmd="startmonitoring", p1=self.translator[mode], user_timeout=custom_timeout)
        # flags for context manager exit method
        if self.translator[mode] == "true":
            self._monitoring_active = True
        elif self.translator[mode] == "false":
            self._monitoring_active = False

    def get_max_amp_per_band(self, channel=Channels.CHANNEL_1, create_plot_buffer: bool = True, save_plot_buffer: bool = False, amplitude_type=SysAmplitudesType.AMPLITUDE_DEFAULT, custom_timeout=None) -> np.ndarray:
        """ Method to return maximum amplitude per band of current active buffer.

        :param channel: Datastream Channel, defaults to Channels.CHANNEL_1
        :type channel: int or Channel, optional
        :param create_plot_buffer: Creates a temporary plot buffer in the Analyzer software, defaults to True
        :type create_plot_buffer: bool, optional
        :param save_plot_buffer: Option to save plot buffer, defaults to False
        :type save_plot_buffer: bool, optional
        :param amplitude_type: Amplitude unit, defaults to SysAmplitudesType.AMPLITUDE_DEFAULT
        :type amplitude_type: int or SysAmplitudeType, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :return: Calculated maximum amplitude values per band
        :rtype: np.ndarray
        """ 
        response_dict =  self._value_parser(cmd="calcmaxamplitude", channel=channel, plot=create_plot_buffer, save=save_plot_buffer, amplitudetype=amplitude_type, user_timeout=custom_timeout,)
        # extract important information
        max_amp = response_dict.get("p1")

        return np.fromstring(max_amp, sep=',')

    def load_test_project(self, custom_timeout=None) -> None:
        """ Loads the set test project.
        
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="loadtestproject", user_timeout=custom_timeout)

    def load_last_user_project(self, custom_timeout=None) -> None:
        """ Loads last user project before a test project was loaded.

        .. warning:: To use this a test project must be loaded before!!!

        .. note:: If no testproject was loaded beforehand, <name_variable> in analyzer software will not be addressed and a new project without name!(="") is going to be created. Once a project like this exist, analyzer cannot perform this again and without loading a test project beforehand, function will do nothing (but parse any check).

        
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="loaduserproject", user_timeout=custom_timeout)
    
    def load_project(self, project_name:str, part_number:str="", custom_timeout=None) ->None:
        """ Loads project by project name. 

        :param project_name: Name of the project
        :type project_name: str
        :param part_number: Set part number, most of the time should be empty, defaults to ""
        :type part_number: str, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """
        self._value_parser(cmd="loadprojectbyname", p1=project_name, p2=part_number, user_timeout=custom_timeout)
    
    def load_project_by_IOid(self, project_IOid:Union[str, int], part_number:str="", custom_timeout=None) ->None:
        """ Loads project by set IO id. 

        :param project_IOid: Projects unique IO id
        :type project_IOid: Union[str, int]
        :param part_number: Set part number, most of the time should be empty, defaults to ""
        :type part_number: str, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """
        self._value_parser(cmd="loadprojectbyioid", p1=f"{project_IOid}", p2=part_number, user_timeout=custom_timeout)

    def get_measure_positions(self, custom_timeout=None) -> Dict:
        """ Gets a dictionary with all measure positions and if used an energy value.

        :return: Measurepositions and their calculated energy value.
        :rtype: dict [with dict.keys() = ['mp0','mp1','mp2','mp3','mp4','mp5','mp5','mp7','mp8','mp9','mp10','mp11','mp12', 'mp13','mp14','mp15']
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        response = self._value_parser(cmd="getmaxmeasurepositions", user_timeout=custom_timeout)
        response.pop("v")
        response.pop("cmd")

        return response

    def get_preamp_info(self, preamp_port: Union[PreampPorts, int], convert:bool=True, custom_timeout=None) -> Union[Dict,str]:
        """ By default returns a dictionary with preamp serial ring and number as the set s value. If convert is set to False the string is parsed as str without putting values into dictionary.

        :param preamp_port: Preamp port with connected preamp.
        :type preamp_port: int or PreampPorts
        :param convert: Flag to convert incomming information to more readble form, default True.
        :type convert: bool
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :raises KeyError: Raises if parsed variable is no supported preamp port
        :return: Serial ring, number and s-value parsed in dictionary.
        :rtype: dict or str [with dict.keys() = ['serial_type','serial_number','S-value']] 
        """ 
        if preamp_port in PreampPorts or preamp_port in range(0, 8):
            preamp_info =  self._value_parser(cmd="getpreampinfo", user_timeout=custom_timeout, p1=preamp_port)
            preamp_info = preamp_info.get('p1')
            if not convert:
                return preamp_info
            try:
                serial_ring, serial_num, s_value, __ = preamp_info.split(";")
                serial_ring_idx = serial_ring.find(":")
                serial_num_idx = serial_num.find(":")
                s_value_idx = s_value.find(":")
                preamp = {
                    "serial_type": serial_ring[serial_ring_idx+1:], "serial_number": serial_num[serial_num_idx+1:], "S-value": s_value[s_value_idx+1:]}
                return preamp
            except ValueError:
                self.logger.warning("The provided Preamp is not configurated properly. Please contact a QASS Service Technician to solve that.")
                return None
        else:
            self.logger.error(
                "Choosen preampport is not an analyzer system preamp port.")
            raise KeyError(
                "Choosen preampport is not an analyzer system preamp port.")
    
    def write_preamp_s_value(self, s_value:int, preampport:Union[PreampPorts, int]=PreampPorts.PREAMP_PORT_1):
        """ Method to set preamp s value in preamp EEPROM text.

        :param s_value: s-value which should be write to preamp EEPROM text
        :type s_value: int
        :param preampport: Preampport where Preamp is connected, defaults to PreampPorts.PREAMP_PORT_1
        :type preampport: Union[PreampPorts, int], optional
        """
        preamp_eeprom = self.get_preamp_info(preamp_port=preampport, convert=False, custom_timeout="never")
        replacement = f"s:{s_value};"
        preamp_eeprom = re.sub("s:-*\d\d*;", replacement, preamp_eeprom)
        self._value_parser(cmd="writepreampinfo", p1=preampport, p2=preamp_eeprom, expect_response=True, user_timeout="never")

    def _write_preamp_eeprom(self, preamp_type:Union[PreampType, int], serial_number:int, s_value:int, preampport:Union[PreampPorts, int]=PreampPorts.PREAMP_PORT_1):
        """ Private method to set preamp EEPROM text.

        :param preamp_type: Type of preamp
        :type preamp_type: PreampType or int
        :param serial_number: Serial Number
        :type serial_number: int
        :param s_value: s value for preamp
        :type s_value: int
        :param preampport: Preampport to which Preamp is connected, defaults to PreampPorts.PREAMP_PORT_1
        :type preampport: Union[PreampPorts, int], optional
        """
        preamp_eeprom = f"t:{preamp_type};s/n:{serial_number};s:{s_value};"
        self._value_parser(cmd="writepreampinfo", p1=preampport, p2=preamp_eeprom, expect_response=False)

    def start_operator_function(self, mode: Union[str, bool] = "start", custom_timeout=None) -> None:
        """ Start operator functions.

        :param mode: Function can start or end operator function by changing mode to a stopping key, defaults to "start". For more allowed keys look up translator dict.
        :type mode: str, bool, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="startoperatorfunctionvalues", user_timeout=custom_timeout, p1=self.translator[mode])
        # flags for context manager exit method
        if self.translator[mode] == "true":
            self._operator_functions_active = True
        elif self.translator[mode] == "false":
            self._operator_functions_active = False

    def stop_operator_function(self, custom_timeout=None) -> None:
        """ Stop of running operator function.
        
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="stoppoperatorfunctionvalues", user_timeout=custom_timeout)
        # flags for context manager exit method
        self._operator_functions_active = False

    def set_serial_number(self, serial_number: int, process_number: int, custom_timeout=None) -> None:
        """ Setting serial number for arbitary process.

        Serial number is stored in the database using the process.serial attribute

        :param serial_number: Serial number that should be set.
        :type serial_number: int
        :param process_number: Process which should be connected to serial.
        :type process_number: int
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="AppCmd", p1="SetProcessSerial", user_timeout=custom_timeout, p2=f"{process_number} {serial_number}")

    def set_serial_number_pending_process(self, serial_number: int, custom_timeout=None) -> None:
        """ Setting serial number for next process.

        Serial number is stored in the database using the process.serial attribute

        :param serial_number: Serial number for next process
        :type serial_number: int
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="setpendingserial", p1=serial_number, user_timeout=custom_timeout)

    def set_comment_pending_process(self, comment: str, custom_timeout=None) -> None:
        """ Set process comment for pending process.

        Comment is saved in the database using the process.comment attribute

        :param comment: Comment for next process.
        :type comment: str
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="setpendingcomment", p1=comment, user_timeout=custom_timeout)

    # def set_comment_current_process(self, comment: str, custom_timeout=None) -> None:
     #   """ Sets comment for current activatet process.

#        Similair to set_proces_comment but as JSON communication Server command.
 #       Comment is saved in database under process.comment
#
 #       :param comment: Process comment to set
 #       :type comment: str
 #      """ 
 #        self._value_parser(cmd="setcomment", p1=comment, quiet=False, user_timeout=custom_timeout)

    def start_operator(self, operator_name: str, operator_setting: str, user_callback=None) -> None:
        """ Manual start of existing operator by name. By adding a callback function,
        software will execute callback when operator finish.

        .. note:: Every callback needs an argument for passed response, whether it is used or not. 

        :param operator_name: Name of operator that should start
        :type operator_name: str
        :param operator_setting: Operator settings like "loop from 0 to -1 simulation 2"
        :type operator_setting: str
        :param user_callback: function receiving the response as a parameter.
            Will be called after the operator finishes.
        :type user_callback: function
        """ 
        if user_callback:
            self.__recv_thread.register_callbacks(
                operator_name, user_callback)
        self._value_parser(expect_response=False, cmd="startoperator", p1=operator_name, p2=operator_setting)

    def import_patterns(self, directory_path: str, ) -> None:
        """ Import all pattern files from a optimizer local directory.

        :param directory_path: Directory path to patterns that will be imported.
        :type directory_path: str
        """ 
        self._value_parser(expect_response=False, cmd="importpatterns", p1=f"\"{directory_path}\"")

    def import_trigger_list(self, filepath: str, append: bool = False, custom_timeout=None) -> None:
        """ Import a trigger list file from local path. Append option decides already exisitng triggers will be set active or not.

        :param filepath: Local filepath
        :type filepath: str
        :param append: Decision to set already existing trigger list active or passive by extending, defaults to False.
        :type append: bool, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        p2_string = f"triggerlist \"{filepath}\""

        if append:
            p2_string = p2_string + " -a"
        self._value_parser(cmd="AppCmd", user_timeout=custom_timeout, p1="import", p2=p2_string)

    def import_operator_network(self, filepath: str, custom_timeout=None) -> None:
        """ Import local operator network file. Command runs as root import.

        .. warning:: The current operator network will be replaced.

        :param filepath: Local filepath to operator network file
        :type filepath: str
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="AppCmd", user_timeout=custom_timeout, p1="import", p2=f"opnet \"{filepath}\"")

    def import_project_archive(self, filepath: str, project_name: str, keep_original_process_nums: bool = False, overwrite: bool = False) -> None:
        """ Import a complete project archive file (tar.gz). 

        .. warning:: If keep_original_process_nums is set, the proces structure will be kept like before the import. As an example if process 17000 has been exported, this flag will create 16999 empty processes before.

        .. warning:: If overwrite is activated this will be overwrite and delete current activated project.

        :param filepath: Local filepath to archive file
        :type filepath: str
        :param project_name: Name of the now imported project
        :type project_name: str
        :param original_nums: Keeps the original process number, defaults to False
        :type original_nums: bool, optional
        :param overwrite: Overwrites current active project, defaults to False
        :type overwrite: bool, optional
        """ 
        p2_string = f" \"{filepath}\" {project_name}"
        if keep_original_process_nums:
            p2_string = p2_string + " --originalnums"
        if overwrite:
            p2_string = p2_string + " --overwrite"

        self._value_parser(cmd="AppCmd", expect_response=False, p1="importprojectarchive", p2=p2_string)

    def export_operator_network(self, target_filepath: str, export: str = "root", custom_timeout=None) -> None:
        """ Exports operator network as JSON file. When in doubt, check documentation.

        Supported 'export' keys: 'root', str     | current activated
        Supported 'export' keys: 'all', str      | all networks
        Supported 'export' keys: 'template', str | network template

        .. list-table:: Keywords on one look
            :widths: 15 10 25
            :header-rows: 1

            * - Key
              - Value datatype 
              - Definition
            * - root
              - str
              - Exports current active operator network
            * - all
              - str
              - Exports all avaible operator networks
            * - template
              - str
              - Exports project specific operator network template

        :param folderpath: Target file path
        :type folderpath: str
        :param export: Decided what from operator will be exported. Current activated("root",  all operators or the template, defaults to "root"
        :type export: str, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        my_translator = {"root": "-r", "all": "-a", "template": "-t"}
        self._value_parser(cmd="AppCmd", expect_response=True, p1="export", p2=f"opnet \"{target_filepath}\" {my_translator[export]}", user_timeout=custom_timeout)

    def export_trigger_list(self, target_filepath: str, custom_timeout=None) -> None:
        """ Exports current trigger list to path. Target filepath should contain new file name.

        :param target_filepath: Target file path
        :type target_filepath: str
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="AppCmd", expect_response=True, p1="export", p2=f"triggerlist \"{target_filepath}\"", user_timeout=custom_timeout)

    def export_project_archive(self, target_filepath: str, export_name: str, export_process: int = None, export_pengui: bool = True, keep_folder: bool = True) -> None:
        """ Exports current active project to path as tar.gz file. This includes all patterns, trigger list and projects.

        :param target_filepath: Target folder path
        :type target_filepath: str
        :param export_name: Give export file a name
        :type export_name: str
        :param export_process: Exports an example process with measurement data, defaults to None
        :type export_process: int, optional
        :param export_pengui: Exports PenGUI, defaults to True
        :type export_pengui: bool, optional
        :param keep_folder: Preserves folder structure and exports this structure to target, defaults to True
        :type keep_folder: bool, optional
        """ 
        p2_string = f"\"{target_filepath}\" {export_name}"
        if export_process:
            p2_string = p2_string + f" --process {export_process}"
        if export_pengui:
            p2_string = p2_string + " --pengui"
        if keep_folder:
            p2_string = p2_string + " --keepfolder"

        self._value_parser(cmd="AppCmd", expect_response=False, p1="exportprojectarchive", p2=p2_string)

    # TODO: Test in newest analyzer version
    def flash_preamp_firmware(self, preampport: Union[int, PreampPorts], filepath: str) -> None:
        """ Flash preamp firmware by downloaded hexfile. Path should be absolute path.

        :param preampport: Connected Preamp
        :type preampport: int or PreampPorts
        :param filepath: Absolute (!) path to hexfile
        :type filepath: str
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        preampport += 1
        self._value_parser(cmd="appfunc", expect_response=False, p1="PreampTool", p2=f"flash {preampport} \"{filepath}\"")
                           
        #  self._value_parser(cmd="PreampTool", user_timeout=custom_timeout)
        #                   p1=f"flash {preampport} {filepath}")

    def detect_preamps(self) -> str:
        """ Method which let Analyzer check for connected Preamps (will not auto. activate them!)

        :return: String saying how much preamps are detected
        :rtype: str
        """
        custom_timeout="never"
        response = self._value_parser(cmd="appfunc", expect_response=True, p1="PreampTool", p2="detect", user_timeout=custom_timeout)
        return response.get("result")

    def get_preamp_firmware(self, preampport: Union[int, PreampPorts], custom_timeout=None)  -> str:
        """ Returns preamp firmware version.

        :param preampport: Port where preamp is connected
        :type preampport: Union[int, PreampPorts]
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :return: O-PA Firmware 
        :rtype: str
        """
        preampport += 1 # c++ analyzer source code handels here preampports between 1 to 8
        response = self._value_parser(cmd="appfunc", expect_response=True, p1="PreampTool", p2=f"version {preampport}", user_timeout=custom_timeout)
        return response.get("result")
    
    def reboot_preamp(self, preampport: Union[int, PreampPorts])   ->None:
        """ Reboots preamp for one second.

        :param preampport: Port where preamp is connected
        :type preampport: Union[int, PreampPorts]
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """
        preampport += 1 # c++ analyzer source code handels here preampports between 1 to 8
        p2_string = f"port {preampport} reboot"
        self._value_parser(cmd="AppCmd", p1="Preamp", p2=p2_string, user_timeout="never")

    def set_default_project(self, comment: str = None, custom_timeout=None) -> None:
        """ Set current active project as new default template.

        :param comment: Comment to describe template, defaults to None
        :type comment: str, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        if comment:
            self._value_parser(cmd="AppCmd", p1="SaveProjectasDefault", p2=f"-c {comment}", user_timeout=custom_timeout)
        else:
            self._value_parser(cmd="AppCmd", p1="SaveProjectasDefault", user_timeout=custom_timeout)

    def remove_default_project(self, custom_timeout=None) -> None:
        """ Removes current project template.""" 
        self._value_parser(cmd="AppCmd", p1="SaveProjectasDefault", p2="-e", user_timeout=custom_timeout)

    # TODO: Test
    def start_operator_results(self, mode: Union[str, bool] = "enable", custom_timeout=None) -> None:
        """ Sets enable flag to send ot operator results if avaible. Results will be sended separately

        :param mode: Enables start or stops by "disable", defaults to "enable"
        :type mode: str, optional
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="startoperatorresults", p1=self.translator[mode], user_timeout=custom_timeout)
                           
    # TODO: Test
    def stop_operator_results(self, custom_timeout=None) -> None:
        """ Sets operator results to stop.
        
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="stopoperatorresults", user_timeout=custom_timeout)

    def get_io_input(self, custom_timeout=None) -> int:
        """ Current get I/O input register as integer appearance (converted from hex).

        :return: I/O input register as integer appearance
        :rtype: int
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        val =  self._value_parser(cmd="readioin", user_timeout=custom_timeout)
        return int(val.get("result"))

    def get_io_output(self, custom_timeout=None) -> int:
        """ Returns get I/O output register as integer appearance (converted from hex).

        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :return: I/O output register as integer appearance
        :rtype: int
        """ 
        val =  self._value_parser(cmd="readioout", user_timeout=custom_timeout)
        return int(val.get("result"))

    def _shift_binary(self, original_bin: str) -> str:
        """ Helper method to convert incoming binary to least significant digit on the right side

        :param str original_bin: Incoming binary
        :param int custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :return str: Shifted binary
        """ 
        # helper list
        new_val = [0] * len(original_bin)

        # save current val to shifted position in list
        for (i, bit) in enumerate(original_bin):
            new_val[len(new_val)-1-i] = bit

        # convert list to string and return
        return "".join(new_val)

    def _binary_to_hexa(self, binary_str: str) -> str:
        """ Formats incoming binary to hexa representation with leading zeros. And leading "0xf" term.

        :param binary_str: Binary that should be converted to hexa representation.
        :type binary_str: str
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :return: hexa representation
        :rtype: str
        """ 
        hexa = "0xf" + "{0:0>4x}".format(int(binary_str, 2))
        return hexa

    def set_simulated_io_input_line(self, io_line: Union[str, int], state: Union[str, bool] =True, custom_timeout=None):
        """ Set the state for a dedicated io input line. The state will be simulated in the analyzer software.
        
        :param io_line: Gives the address of the io_line. This can be either a numeric value between 1 and 24 or a string in the format '[byte].[bit]'.
        :type io_line: str or int
        :param state: Gives the state for the referenced io_line. The state can be any out of ('on', 1, '1', True, 'True', 'true', 'enable', 'set') or ('off', 0, '0', False, 'False', 'false', 'disable', 'clear').
        :type state: str or bool, defaults to True.
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        true_states = ('on', 1, '1', True, 'True', 'true', 'enable', 'set')
        false_states = ('off', 0, '0', False, 'False', 'false', 'disable', 'clear')
        accepted_states = true_states + false_states
        if state not in accepted_states:
            raise ValueError(f'The state must be one of {accepted_states} but is {state}')
        
        if state in true_states:
            state = 'on'
        elif state in false_states:
            state = 'off'
        
        from numbers import Number
        if isinstance(io_line, Number):
            if not (1 <= io_line <= 24):
                raise ValueError(f'The given io_line is out of range (1<=io_line<=24): {io_line}')
        else:
            import re
            pattern = re.compile(r'^[124]\.[12345678]$')
            if not pattern.match(io_line):
                raise ValueError(f'The given io_line does not fulfill the expected pattern (e.g. 1.3): {io_line}')
            
        self._value_parser(cmd="AppCmd", p1="setsimioin", p2=f'{io_line} {state}', user_timeout=custom_timeout)

    def set_simulated_io_input(self, io: str, custom_timeout=None) -> None:
        """ Set simulated I/O input register. I/0 input register can be set by inverted hexa (smallest significant right)
        or by providing a binary representation of seen bits set in I/O register. When in doubt, see documentation.

        First 8 digits are first I/O input register. Second 8 digits are second I/O input register. Give in all inputs as strings only!

        .. list-table:: I/O Input possibilities
            :widths: 25 25
            :header-rows: 1

            * - Binary Representation
              - Hexadecimal Representation
            * - "00000000 00000000"
              - "0xf0000"
            * - "10000000 00000000"
              - "0xf0001"
            * - "01000000 00000000"
              - "0xf0002"
            * - "11000000 00000000"
              - "0xf0003"
            * - "00100000 00000000"
              - "0xf0004"
            * - "10100000 00000000"
              - "0xf0005"
            * - "01100000 00000000"
              - "0xf0006"
            * - "11100000 00000000"
              - "0xf0007"
            * - "00010000 00000000"
              - "0xf0008"
            * - "10010000 00000000"
              - "0xf0009"
            * - "01010000 00000000"
              - "0xf000A"
            * - "11010000 00000000"
              - "0xf000B"
            * - "00110000 00000000"
              - "0xf000C"
            * - "10110000 00000000"
              - "0xf000D"
            * - "01110000 00000000"
              - "0xf000E"
            * - "11110000 00000000"
              - "0xf000F"
            * - ...
              - ...
            * - "10001000 00000000"
              - "0xf0011"
            * - ...
              - ...

        :param io: Combination of bits set to I/O input register (one and two,  defaults to "0xf0000". For further information see extended summary.
        :type io: str
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :raises ValueError: If parsed I/O input is not supported in this form. Means no from like "00000000 00000000" or "0xf0000". 
        """ 
        # helper
        bin_ref = "00000000 00000000"
        hexa_ref = "0xf0000"
        # case handler
        if len(io) == len(bin_ref):  # binary case
            # replace white space if needed
            if " " in io:
                io = io.replace(" ", "")  # delete space
            # shift binary to least signifcant bit right
            io_binary = self._shift_binary(io)
            # convert binary to hexa
            io_hexa = self._binary_to_hexa(io_binary)
        elif len(io) == len(hexa_ref):  # hexa case
            io_hexa = io
        else:
            self.logger.error(
                "Given format of I/O input register state is not supported. Please check extended method documentation.")
            raise ValueError(
                "Given format of I/O input register state is not supported. Please check extended method documentation.")

        self._value_parser(cmd="setsimioin", p1=io_hexa, user_timeout=custom_timeout)
                           
    def add_io_report_callback(self, callback, custom_timeout=None) -> None:
        """ Adds callback function to report of I/O register. Everytime I/O register changes, added callback functions will be executed. See networking_example.py for an example.
        By adding first callback the report start automatically und will be stopped by removing all callbacks due to remove function.

        .. warning:: All callbacks need as first param "result" to catch analyzer response, if used or not.

        :param callback: Added callback function when report happens.
        :type callback: function
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        if self._io_report_count == 0:
             self._value_parser(user_callback=callback, cmd="reportio", p1="true", user_timeout=custom_timeout)         
        else:
            self.__recv_thread.register_callbacks("responsereportio", callback)
        self._io_report_count += 1
        self.logger.info(f"Callback {callback} for I/O report added")

    def remove_io_report_callback(self, callback, custom_timeout=None) -> None:
        """ Removes specific callback function from I/O report callback list. By removing all callbacks the report function will be automatically stopped.

        :param callback: Callback function that should be removed from I/O report functionalities.
        :type callback: function
        """ 
        self.__recv_thread.deregister_callbacks(
            self._recognition_translator("reportio",  callback))
        self._io_report_count -= 1
        self.logger.info(f"Callback {callback} for I/O report removed")
        if self._io_report_count == 0:
            self._value_parser(cmd="reportio", p1="false", user_timeout=custom_timeout)
            self.logger.info("I/O report stopped")

    def add_process_number_report_callback(self, callback, custom_timeout=None) -> None:
        """ Adds callback function to report of process number. Everytime the process number changes, added callback functions will be executed. See networking_example.py for an example. By adding first callback the report start automatically und will be stopped by removing all callbacks due to remove function.

        .. warning:: All callbacks need as first param "result" to catch analyzer response, if used or not.

        :param callback: Added callback function when report happens.
        :type callback: function
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        if self._proc_report_count == 0:
            self._value_parser(user_callback=callback, cmd="reportprocessnumber", user_timeout=custom_timeout, p1="true")
        else:
            self.__recv_thread.register_callbacks("responsereportprocessnumber", callback)
        self._proc_report_count += 1
        self.logger.info(
                f"Callback {callback} for process number report added")

    def set_io_output(self, io_line: int, state: bool, custom_timeout=None) -> None:
        """ Sets single I/O ouput line. As parameter only line number of third I/O line is required. When in doubt, check documentation.

        .. warning:: Changing output line 3.1 - 3.3 is not possible. 

        .. list-table:: I/O Output possibilities
            :widths: 25 25
            :header-rows: 1

            * - I/O line
              - parameter
            * - 3.1
              - 1
            * - 3.2
              - 2
            * - 3.3
              - 3
            * - 3.4
              - 4
            * - 3.5
              - 5
            * - 3.6
              - 6
            * - 3.7
              - 7
            * - 3.8
              - 8

        :param io_line: Line number in range(1,8)
        :type io_line: int
        :param state: Set Line high or low
        :type state: bool
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(expect_response=False, cmd="appcmd", p1="setioout", p2=f"{io_line} {state}", user_timeout=custom_timeout)

    def remove_process_number_report_callback(self, callback, custom_timeout=None) -> None:
        """ Removes specific callback function from process number report callback list. By removing all callbacks the report function will be automatically stopped.

        :param callback: Callback function that should be removed from process number report functionalities.
        :type callback: function
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self.__recv_thread.deregister_callbacks(
            "responsereportprocessnumber", callback)
        self._proc_report_count -= 1
        self.logger.info(
            f"Callback {callback} for process number report removed")
        if self._proc_report_count == 0:
            self._value_parser(cmd="reportprocessnumber", p1="false", user_timeout=custom_timeout)
            self.logger.info("Report of process number stopped.")

    # TODO: Test
    def start_script_function(self, function_name: str, function_param: any, custom_timeout=None) -> None:
        """ General syntax to start script function. Response is depending on called function.

        .. warning:: Service function, should not be used without prior kmowledge about remote scripts

        :param function_name: Name of script function
        :type function_name: str
        :param function_param: Passed param to script function
        :type function_param: any
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :return: Standard Analyzer response. Dict contains result of addressed function as str.
        :rtype: dict
        """ 
        return self._value_parser(cmd="appfunc", p1=function_name, p2=function_param, user_timeout=custom_timeout)
                                  
    def set_human_confirmation(self, process_IO=False, **kwargs) -> None:
        """ Send human confiramtion over current process. Score and comment can be parsed over kwargs. When in doubt, check documentation.
            
        Supported Kwargs Key: "comment", str | Human comment for confirmation
        Supported Kwargs Key: "score", int   | Score value for confirmation

        .. list-table:: Possible keyword arguments
            :widths: 15 10 25
            :header-rows: 1

            * - Key
              - Value datatype
              - Description
            * - comment
              - str
              - Human comment for confirmation
            * - score
              - int
              - Score value for confirmation

        :param process_IO: Confirmation if current process is IO or NIO, defaults to False
        :type process_IO: bool
        :raises ValueError: If kwargs key is not supported
        """ 
        translator = {False: "NIO", True: "IO"}
        settings = {"cmd": "confirmation",
                    "p1": translator[process_IO]}
        if kwargs:
            if kwargs.keys() not in ["comment", "score"]:
                self.logger.error(
                    "Key is not supported for operation human_confirmation")
                raise ValueError(
                    "Key is not supported for operation human_confirmation")
            if "comment" in kwargs.keys():
                settings["p2"] = kwargs["comment"]
            if "score" in kwargs.keys():
                settings["score"] = kwargs["score"]

        self._value_parser(expect_response=False, **settings)

    def write_to_database(self, result: any, comment=None) -> None:
        """ Writes database query for an entry with current project_id, process, process_id, result and comment as values

        :param result: Result which should be saved in database
        :type result: any
        :param comment: Comment for result, defaults to None
        :type comment: str, optional
        """ 
        if comment:
             self._value_parser(expect_response=False, cmd="humanconfirmationresult", p1=result, p2=comment)
        else:
             self._value_parser(expect_response=False, cmd="humanconfirmationresult", p1=result)

    def write_backup(self, custom_timeout=None) -> None:
        """ Creates an automatic Analyzer backup.
        
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        """ 
        self._value_parser(cmd="AppCmd", p1="writeBackup", user_timeout=custom_timeout)
  
    def set_sys_pengui_config(self, penguifile=None, reload=None, activate_on_load=None, disable_open_gl=None, 
                              disable_buffer_boxes=None, keepIfNotChanged=None, custom_timeout=None):
        """ Sets the entries under Preferences -> GUI -> Custom User Interface.
        This incorporates the behaviour of the qml GUI. It is probably no good idea to set reload and keepIfNotChanged both to True.
        
        :param str penguifile: The absolute path to the qml file that should be loaded.
        :param bool reload: Whether or not to reload the qml file whenever a project is loaded
        :param bool activate_on_load: Whether to display the qml GUI on program startup.
        :param bool disable_open_gl: Disable the openGL view whenever a qml GUI is actively displayed.
        :param bool disable_buffer_boxes: Disable Buffer bounding boxes.
        :param bool keepIfNotChanged: Do not reload qml GUI when the project is changed and the new project uses the same QML. Just available for Analyzer with Version >= "2.04.12.05", otherwise this attribute is ignored and a warning occures
        """
        
        #build p2 string for use of different optionm -> Analyzer searches for subcmd and then boolean value
        activated_params= []
        for key, value in [("penguifile", penguifile),  ("reload", reload),
                                                        ("activateOnLoad", activate_on_load),
                                                        ("disableOpenGL", disable_open_gl),
                                                        ("disableBufferBoxes", disable_buffer_boxes)]:
            if value is not None:
                activated_params.append(f"{key} \"{self.translator.get(value,value)}\" ")
        
        if keepIfNotChanged is not None:
            # check version
            if self.check_version(minimum_needed_version="2.04.12.05"):
                
                activated_params.append(f"keepIfNotChanged \"{self.translator.get(keepIfNotChanged,keepIfNotChanged)}\" ")
            else:
                self.logger.warning(f"keepIfNotChanged is no available attribute for method sysPenguiConfig because AnalyzerVersion {self._analyzer_version} is smaller than 2.04.12.05! Change attribute manually in Settings -> GUI or update Analyzer Version!")

        p2_str = "".join(activated_params)
        if p2_str == "":
            self.logger.info("Method 'set_sys_pengui_config' is not executed because of no valid parameters.")
            return
        self._value_parser(cmd="AppCmd", p1="sysPenguiConfig", p2=p2_str, user_timeout=custom_timeout)

    def set_python_init_hook(self, python_init_hook_path: Union[str, Path]):
        """
        Set the python init hook path in Preferences -> Python -> Python Init Hook

        :param str python_init_hook_path: The absolute path to the python script that should be executed during
            the startup phase of the analyzer software.
        """
        self._value_parser(cmd="AppCmd", p1="sysPathConfig", p2=f"pyinithook \"{str(python_init_hook_path)}\"")

    def reset_failstate(self, set_idle_state:bool=True, clear_all_windows:bool=True,custom_timeout=None) -> None:
        """ Reset failure status of optimizer (activates I/O Ready) 

        :param bool set_idle_state: Application state is set to IDLE, defaults to True
        :param bool clear_all_windows: Removes all message/notification windows, defaults to True
        """
        p2 = ""
        if set_idle_state:
            p2 = p2 + "-idle"
        if clear_all_windows:
            p2 = p2 + " -a"
        self._value_parser(cmd="AppCmd", p1="ResetFailstate", p2=p2,user_timeout=custom_timeout)

    def set_failstate(self, **kwargs):
        """ Set Analyzer4d Software into failstate. If no duration is provided, system stays in failstate (clear I/O ready).
            
        Supported Kwargs Key: "duration", int | Duration in ms for failstate status

        .. list-table:: Possible keyword arguments
            :widths: 15 10 25
            :header-rows: 1

            * - Key
              - Value datatype
              - Description
            * - comment
              - int
              - Duration in ms for failstate status
        """
        duration = kwargs.get("duration", None)
        if duration:
            if isinstance(duration, int):
                self._value_parser(cmd="AppCmd", p1="SetFailstate", p2=f"{duration}")
            else:
                raise ValueError("Only integer greater 0 are supported for failstate duration")
        else:
            self._value_parser(cmd="AppCmd", p1="SetFailstate") 
    
    def free_buffer_datablocks(self):
        """ Free all buffer standby datablocks. 
        
        .. warning:: Experts method
        """
        self._value_parser(cmd="AppCmd", p1="ExpertCmd", p2="RAM free-standby")
    
    def remove_delayed_trigger(self, delay_type:str=None, custom_timeout=None):
        """ Method to remove delayed trigger. 

        Supported key: "all", str        | Remove all delayed trigger commands from queue
        Supported key: "busy", str       | Remove trigger commands delayed to busy signal
        Supported key: "parameter", str  | Remove trigger commands delayed by parameters from queue

        .. list-table:: Possible delay types
            :widths: 15 10 25
            :header-rows: 1

            * - Key
              - Datatype
              - Definition
            * - 'all'
              - str
              - Remove all delayed trigger commands from queue
            * - 'busy'
              - str
              - Remove trigger commands delayed to busy signal
            * - 'parameter'
              - str
              - Remove trigger commands delayed by parameters from queue

        .. warning:: Experts method      
        
        :param delay_type: Type of delayed signal to remove, defaults to None
        :type delay_type: str, optional

        
        """
        remove_kinds = {"all":"remove-all", "busy":"remove-busy", "parameter":"remove-delayed"}
        self._value_parser(cmd="AppCmd", p1="ExpertCmd", p2=f"TRIGGER {remove_kinds[delay_type]}", user_timeout=custom_timeout)

    def start_shell_program(self, programm_path:Union[str,Path], detach_from_analyzer:bool=True):
        """ Start an arbitary system process via shell. By detaching start of program and analyzer context, start of programm runs asynchron. If false, analyzer waits for finsihed programm (max to 1 sec)

        :param programm_path: Path to Programm
        :type programm_path: str
        :param detach_from_analyzer: Flag to decide if process is completted async to analyzer context, defaults to True
        :type detach_from_analyzer: bool, optional
        """
        if detach_from_analyzer:
            sync_param  = "-detach"
        else:
            sync_param = "-noasync"
        self._value_parser(cmd="AppCmd", p1="StartProgram", p2=f"{sync_param} \"{str(programm_path)}\"")

    def restart_analyzer(self, wait_time:Union[int,str]=2000, **kwargs):
        """ Restart analyzer4D Software after system stayed a mininum time (= wait_time) in idel state. 
        By parsing "force_now", a reboot will be executed directly.


        Supported Kwargs Key: "last_words", str              | Displayed message from analyzer before restart
        Supported Kwargs Key: "last_words_display_time", int | Time frame in ms for displaying last words. Time frame > 0 and Time frame <= wait_time. Keyword is only settable by simultaneously using last_words.

        .. list-table:: Keyword arguments
            :widths: 15 10 25
            :header-rows: 1

            * - Key
              - Value datatype
              - Description
            * - last_words
              - str
              - Displayed message from analyzer before restart
            * - last_words_display_time
              - int
              - Time frame in ms for displaying last words. Time frame > 0 and Time frame <= wait_time. Keyword is only settable by simultaneously using last_words. 
            
        :param wait_time: Minimum time [ms] in idle state before analyzer software is closed, defaults to 2000 ms
        :type wait_time: Union[int,str], optional
        :raises ValueError: If wait_time is smaller or equal zero
        :raises ValueError: If display_message time is smaller or equal zero
        """
        if isinstance(wait_time, str) and wait_time == "force_now":
            self._value_parser(cmd="AppCmd", p1="RestartAnalyzer", p2="FORCE_NOW")
        elif isinstance(wait_time,int):
            if not wait_time > 0:
                raise ValueError("Display time has to be greater than 0 ms")
            last_words = kwargs.get("last_words", None)
            last_words_display_time = kwargs.get("last_words_display_time", 2000)
            p2 = f"{wait_time}"
            if last_words:
                if not last_words_display_time > 0:
                    raise ValueError("Display time has to be greater than 0 ms")
                if last_words_display_time > wait_time:
                    last_words_display_time = wait_time
                    self.logger.info("Disaply time for analyzer message is set to maximum time before restart (= 'wait_time')")
                p2  = p2 + f" {last_words_display_time} \"{last_words}\""
            self._value_parser(cmd="AppCmd", p1="RestartAnalyzer", p2=f"{p2}")

    #TODO: Description
    def set_frequency_mask(self, mask_id:int, measure_config:int):
        """ Set an already exisiting frequency mask.

        :param int mask_id:  ID of desired mask
        :param int measure_config: _description_
        """
        self._value_parser(cmd="AppCmd", p1="SetFrequencymask", p2=f"{mask_id} {measure_config}")
    
    def use_frequency_mask(self, mask_id:int):
        """ Use already existing frequnecy mask on process.

        :param int mask_id: Use frequency mask with provided ID
        """
        self._value_parser(cmd="AppCmd", p1="UseFrequencymask", p2=f"{mask_id}")
    
    def teach_frequency_mask(self, mask_id:int, mask_type:str):
        """ Teach new Frequency mask for loaded measurement.

        :param int mask_id: Frequency mask ID of new mask
        :param str mask_name: Frequency mask type
        """
        self._value_parser(cmd="AppCmd", p1="TeachFrequencymask", p2=f"{mask_id} {mask_type}")

    def set_GUI_tools_acitvated(self, show_buffer_bar:bool=True, show_toolbar:bool=True):
        """ Show and Hide buffer buttons and tools in GUI

        :param bool show_buffer_bar: Flag to show or hide buffer buttons, defaults to True
        :param bool show_toolbar: Flag to show or hide tools, defaults to True
        """
        if show_buffer_bar:
            buffer_bar = "showbufferbuttons"
        else:
            buffer_bar = "hidebufferbuttons"
        
        self._value_parser(cmd="AppCmd", p1="GuiCMD", p2=f"{buffer_bar}")
        
    def set_buffer_buttons_visible(self, visible:bool=True):
        """ Set GUI view of buffer buttons enabled/disabled.

        :param bool visible: Enable visualization, defaults to True
        """
        if visible:
            buffer_bar = "showbufferbuttons"
        else:
            buffer_bar = "hidebufferbuttons"
        self._value_parser(cmd="AppCmd", p1="GuiCMD", p2=f"{buffer_bar}")

    def set_toolbar_visible(self, visible:bool=True):
        """Set GUI view of tool bar enabled/disabled.

        :param bool visible: Enable visualization, defaults to True
        """
        if visible:
            toolbar = "showtools"
        else:
            toolbar = "hidetools"
        self._value_parser(cmd="AppCmd", p1="GuiCMD", p2=f"{toolbar}")

    def set_sys_python_path(self, python_sys_path:Union[str,Path]):
        """ Set system python path. [Preferences->Python->sys.path extensions]
        
        :param Union[str,Path] python_sys_path: Python path
        """
        self._value_parser(cmd="AppCmd", p1="sysPathConfig", p2=f"pysyspaths \"{python_sys_path}\"")

    def set_appvar_container_visible(self, visible:bool=True):
        """ Shows AppVar Container in Analyzer4D menu. 

        :param bool visible: Flag to activate vision, defaults to True
        """
        if visible:
            state = "enable"
        else:
            state = "disable"
        self._value_parser(cmd="AppCmd", p1="ShowTool", p2=f"APPVARS {state}")    
    
    def set_frq_mask_container_visible(self, visible:bool=True):
        """Shows Frequency mask manager in Analyzer4D menu. 

        :param bool visible: Flag to activate vision, defaults to True
        """
        if visible:
            state = "enable"
        else:
            state = "disable"
        self._value_parser(cmd="AppCmd", p1="ShowTool", p2=f"FRQMASKS {state}") 

    def set_classic_menu_view(self, enable:bool=True):
        """ Switch menu view in Analyzer4d Software to classic menu.

        :param bool enable: Enbale/Disable classic menu, defaults to True
        """
        if enable:
            state = "enable"
        else:
            state = "disable"
        self._value_parser(cmd="AppCmd", p1="ShowTool", p2=f"CLASSICMENU {state}") 

    def set_trigger_list(self, enable:bool=True):
        """ Set trigger list on enabled.

        :param bool enable: enable/disable trigger list, defaults to True
        """
        if enable:
            state = "on"
        else:
            state = "off"
        self._value_parser(cmd="AppCmd", p1="sysTriggerLoop", p2=f"{state}")

    # TODO: profibus
    # TODO: profibus report
        
    def _recognition_translator(self, cmd: str) ->  str:
        """ Private method to add "response" to already sended cmd str for later recognition.

        :param cmd: cmd string which needs to be changend.
        :type cmd: str
        :param custom_timeout: Custom timeout flag to get a response, defaults to None. For more information see class description.
        :type custom_timeout: int, optional
        :return: cmd string which will be sended by analyzer as response.
        :rtype: str
        """ 
        if cmd == "reportappvars":
            return "responseappvars"
        else:
            # case normal communication server command
            return "response" + cmd

    def _send(self, command: Dict) ->  None:
        """ Private method to send commands to analyzer. Command will be encoded to bytestring.

        :param command: Command dict which should be sent to connected analyzer.
        :type command: Dict
        """ 
        # print every sended command
        self.logger.debug(f"Command sent:{command}")
        # prepare command
        cmd_str = json.dumps(command).encode()
        cmd_str = (len(cmd_str)).to_bytes(2, 'big') + cmd_str
        # actual sending command
        self.s.sendall(cmd_str)

    def _value_parser(self, expect_response=True, user_callback=None, user_timeout=None, **kwargs) -> Dict:
        """ Function to coordinate sending parsed command settings and take back answer from receiver thread. By kwargs specification each command will be set.

        :param expect_response: Flag to not wait for analyzer response, defaults to True
        :type expect_response: bool, optional
        :return: Analyzer response
        :rtype: dict
        """ 
        # adding msgid
        self.msgid += 1

        # command ground structure
        command = {'cmd': "",
                   "msgid": self.msgid}

        # specify final command
        command.update(kwargs)
        # decide which recognition should be used, if possible use msgid
        if command['cmd'] == "AppCmd":
            recognition = self.msgid
        else:
            recognition = self._recognition_translator(command['cmd'])

        # if response is expected:
        # register callback before sending
        if expect_response and user_callback == None:
            # use class variabele self.q as queue object
            def callback(result, queue_var=self.q): return queue_var.put(result)
            self.__recv_thread.register_callbacks(recognition, callback)
        elif expect_response:
            self.__recv_thread.register_callbacks(
                recognition, user_callback)

        # send command in any case
        self._send(command)

        # receive response if avaible and expected
        # reports are handled external
        if expect_response and user_callback == None:
            try:
                if user_timeout:
                    # handle case that as timeout string "never" is parsed for a non blocking possibility
                    if isinstance(user_timeout, str) and user_timeout == "never":
                        user_timeout = None # equals block
                    # else just take normal parsed timeout as int
                    function_timeout = user_timeout
                # if nothing is parsed, take default
                else:
                    function_timeout = self.timeout  
                # get response out of queue for all cases without own custom_callback // handles also receiver thread errors
                analyzer_response = self.q.get(timeout=function_timeout)
            except queue.Empty: # Raise from None, excludes queue.Empty Error from Traceback 
                raise ReceiverThreadError("Analyzer was not responding in timeout time. Please check if communication between devices is lost or custom timeout method has to be used.") from None
            # check for message state and also if receiver thread gives back an error, unregister callbacks
            
            self._check_response(analyzer_response, recognition)
            
            return analyzer_response
        
    def _check_response(self, response:Dict, recognition:str):
        """ Private method to check received response for ErrorCallback or for analyzer response value under key="ok". If value is True, response is approved. Not ErrorCallbacks will be unregistered.

        :param response: Response dict from analyzer to check.
        :type response: dict
        :param recognition: Recognition for not ErrorCallbacks
        :type recognition: str
        :raises AnalyzerError: if command could not be performed, due to false syntax or params out of bounds.
        :raises ReceiverThreadError: if parsed from Receiver Thread
        """ 
        # ErrorCallbacks
        if 'cmd' in response and response.get('cmd') == "error":
            origin_error = response.get("kind")
            self.logger.error(
                f"Receiver Thread logs an unexpected error from {origin_error}")
            raise ReceiverThreadError(
                "Receiver Thread logs an unexpected error") from origin_error
        # check normal response
        elif "ok" in response:
            if response.get("ok") == False:
                self.logger.error(
                    "Analyzer4D software could not perform action: check log and documentation.")
                raise AnalyzerError(
                    "Analyzer4D software could not perform action: check log and documentation.")
        # deregister callbacks (ErrorCallback is not deregistered)
        self.__recv_thread.deregister_callbacks(recognition)


    @required_version("2.06.02.04")
    def set_ect_config(
            self,
            toolpath: Union[str, None] = None,
            processes: Union[int, None] = None,
            minutes: Union[float, int, None] = None,
            paras: Union[str, List[str], None] = None,
            ):
        """Set the parameters for the external cleanup tool under
        Configuration -> Preferences -> Cleanup Tool

        The minimal required Analyzer4D version is: 2.06.02.04.
        
        .. important::
            Make sure that you have the service parameter `pUseModExternalCleanupTool`
            enabled before using this function!

        :param toolpath: The path to the tool. This is the path that you are using
            when executing the tool from the command line. You can use substitions like
            `$HOMEPATH` which are available in the Analyzer4D software but using the
            absolute path to the tool should always work. The tool is always called with
            the parameters `--projectid` and `--process`
        :type toolpath: Union[str, None]
        :param processes: The amount of processes or measurements after which the tool
            should be executed by the Analyzer4D software
        :type processes: Union[int, None]
        :param minutes: The amount of minutes the Analzyer4D software has to idle before 
            the tool is executed by the Analyzer4D software
        :type minutes: Union[int, None]
        :param paras: Extra parameters to append to the call like `--extra-arg1 --extra-arg2`.
            Here you can also use appvar subsitions like `--appvar $$my_appvar` if your
            tool accepts an argument called `appvar`.
        :type paras: Union[List[str], str, None]
        """
        assert processes is None or processes >= 0, ("The processes parameter must be greater than or equal to zero "
                                                     f"but was {processes}")
        assert minutes is None or minutes >= 0, ("The minutes parameter must be greater than or equal to zero "
                                                     f"but was {minutes}")
        if isinstance(paras, list):
            paras = " ".join(paras)
        active_params = []
        for key, value in [
            ("toolpath", toolpath),
            ("processes", processes),
            ("minutes", minutes),
            ("paras", paras),
        ]:
            if value is None:
                continue
            active_params.append(f'{key} "{value}" ')
        if len(active_params) == 0:
            self.logger.info(
                "Method 'set_ect_config' is not executed because of no valid parameters."
            )
            return
        p2_str = "".join(active_params)
        self._value_parser(cmd="AppCmd", p1="sysECTConfig", p2=p2_str)

class AnalyzerCmd(AnalyzerRemote):
    """ Depricated class naming. Inherit from normal class.

    .. deprecated:: since 1.1
    Use :class:`AnalyzerRemote` class instead.

    :param AnalyzerRemote: Inherited class
    :type AnalyzerRemote: class
    """ 

    def __init__(self, ip: str, port=17000, debug_mode=False):
        super().__init__(ip, port, debug_mode)
        warnings.warn(
            "Class Name AnalyzerCmd is deprecated. Please use AnalyzerRemote!")
