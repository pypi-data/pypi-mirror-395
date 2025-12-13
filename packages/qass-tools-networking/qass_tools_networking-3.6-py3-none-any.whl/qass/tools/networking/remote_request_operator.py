from Analyzer.Core import Process_IF
import analyzer_socket
from importlib import reload
reload(analyzer_socket)

import socket

remote_opti_ip = "192.168.1.152"  # param

def eval_process_init():
    try:
        remote_client = analyzer_socket.AnalyzerRemote(remote_opti_ip, 17000)
    except socket.timeout as e:
        raise RuntimeError(f'The remote optimizer connection timed out - the remote optimizer is not available via the ip {remote_opti_ip}')
    remote_process_number = remote_client.get_current_process_number()
    remote_client.close()
    
    proc = Process_IF()
    proc.setCustomInfo("remote_proc_no", remote_process_number)
    proc.saveToDatabase() 
