#!/usr/bin/python3

import socket
from PySide2.QtNetwork import QTcpSocket
from PySide2.QtCore import QObject, Slot, Signal, QRegExp
from PySide2.QtGui import QRegExpValidator

from PySide2 import QtCore
from PySide2.QtWidgets import QWidget, QSpinBox, QPushButton
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QPlainTextEdit
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QVBoxLayout

import sys
import json
from typing import Dict


class Client(QObject):
    output_std = Signal(str)
    output_err = Signal(str)

    def __init__(self, parent, ip, port):
        super().__init__(parent)
        self.sock = QTcpSocket()
        self.sock.connectToHost(ip, port)
        self.sock.readyRead.connect(self.onReadyRead)
        self.sock.disconnected.connect(self.disconnected)
        self.pkt_id = 0

    def __del__(self):
        print('closing socket')
        self.sock.close()

    disconnected = Signal()

    def disconnect(self):
        """ Method will close the socket connection."""
        self.sock.close()

    def onReadyRead(self):
        """ Method will read sended data out of socket and change appearance. Data will be check for errors or methods."""
        packet = self.sock.readAll().data().decode()
        packet = packet.replace('}{', '},{')
        packet = '[' + packet + ']'

        objs = json.loads(packet)

        for obj in objs:
            if "result" in obj:
                pass
                # print(obj["result"])
            elif "error" in obj:
                err = obj["error"]
                if "message" in err:
                    self.output_err.emit(err["message"])
                if "data" in err:
                    self.output_err.emit(str(err["data"]))
            elif "method" in obj:
                if obj["method"] == "stdout":
                    self.output_std.emit(obj["params"]["text"])
                elif obj["method"] == "stderr":
                    self.output_err.emit(obj["params"]["text"])

    def send_obj(self, obj: str):
        """ Send Obj to socket after encoding.
        :param obj: Object which will be written to socket
        :type obj: str
        """
        text = json.dumps(obj)
        text = text.encode()
        self.sock.write(text)

    def buildJsonRpc(self, func, params) -> Dict:
        """Helper method to build a JSON-RPC-Call to send to server.

        :param func: Name of function/method that should be called.
        :type func: function or str
        :param params: Array or object with params for parsed function.
        :type params: Any
        :return: Builded JSON-RPC-Call
        :rtype: Dict
        """
        self.pkt_id += 1

        return {
            'jsonrpc': '2.0',
            'method': func,
            'params': params,
            'id': self.pkt_id
        }

    def callFunc(self, func, **kwargs):
        """ Helper method to send a JSON-RPC which calls a specific function.

        Kwargs:
        By kwargs you can specify params for called function.

        :param func: Name of fucntion that should be called.
        :type func: Str or function
        """
        packet = self.buildJsonRpc(func, kwargs)
        self.send_obj(packet)

    def remoteInteractive(self, script: str) -> Dict:
        """ Toplevel function to start remote interactive function.

        :param script: Script function that should be started
        :type script: str
        :return: Builded JSON-RPC
        :rtype: Dict
        """
        return self.callFunc('interactive', script=script)

    def remoteEval(self, script) -> Dict:
        """Toplevel function to start remote eval function.

        :param script: Script function that should be started
        :type script: str
        :return: Builded JSON-RPC
        :rtype: Dict
        """
        return self.callFunc('eval', script=script)


class HistoryLineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.returnPressed.connect(self.onInputFinished)
        self.__history = []
        self.__history_idx = 0

    def onInputFinished(self):
        """ Method to append command-text and length to History dict by input finish."""
        self.__history.append(self.text())
        self.__history_idx = len(self.__history)

    def keyPressEvent(self, event):
        if self.__history:
            if event.key() == QtCore.Qt.Key_Up:
                self.__history_idx -= 1
                self.__history_idx = max(0, self.__history_idx)
                self.setText(self.__history[self.__history_idx])
            elif event.key() == QtCore.Qt.Key_Down:
                self.__history_idx += 1
                self.__history_idx = min(
                    len(self.__history) - 1, self.__history_idx)
                self.setText(self.__history[self.__history_idx])
            else:
                self.__history_idx = len(self.__history)

        super().keyPressEvent(event)


class Window(QWidget):
    def __init__(self):
        """ Constructor to set up QT Window"""
        super().__init__()

        self.setWindowTitle("Analyzer4D remote Python console")
        self.setGeometry(300, 300, 500, 400)
        self.ip = QLineEdit(self)
        re = QRegExp(
            '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]).){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
        self.ip.setValidator(QRegExpValidator(re))
        self.ip.setText('127.0.0.1')

        self.port = QSpinBox(self)
        self.port.setMaximum(99999)
        self.port.setValue(36401)

        self.connButton = QPushButton('Connect', self)
        self.connButton.pressed.connect(self.onConnButtonPressed)

        self.output = QPlainTextEdit(self)
        self.input = HistoryLineEdit(self)

        self.output.setTextInteractionFlags(
            self.output.textInteractionFlags() & ~QtCore.Qt.TextEditable)
        self.input.returnPressed.connect(self.onInputFinished)
        self.input.setFocus()
        self.input.setDisabled(True)
        self.output.setDisabled(True)

        self.client = None

        layout = QVBoxLayout()

        layout.addWidget(self.ip)
        layout.addWidget(self.port)
        layout.addWidget(self.connButton)
        layout.addWidget(self.output)
        layout.addWidget(self.input)

        self.setLayout(layout)
        self.__history = []

    def onInputFinished(self):
        text = self.input.text()
        self.input.clear()
        self.client.remoteInteractive(text)
        self.output.appendPlainText('>' + text)
        self.__history.append(text)

    def onServerOutput(self, text):
        text = text.rstrip()
        if text:
            self.output.appendPlainText(text)

    def onDisconnect(self):
        self.disconnect(self.client)
        self.client = None
        self.input.setEnabled(False)
        self.output.setEnabled(False)

    def onConnButtonPressed(self):
        if self.client:
            self.client.disconnect()
            self.connButton.setText('Connect')
        else:
            try:
                self.client = Client(self, self.ip.text(), self.port.value())
                self.client.disconnected.connect(self.onDisconnect)
                self.input.setEnabled(True)
                self.output.setEnabled(True)
                self.client.output_std.connect(self.onServerOutput)
                self.client.output_err.connect(self.onServerOutput)
                self.connButton.setText('Disconnect')
            except:
                self.client = None


app = QApplication(sys.argv)

mainWin = Window()
mainWin.show()


app.exec_()
