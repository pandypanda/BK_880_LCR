#############################################################################
#               Andy's test for BK Precision LCR Meter 880                  #
#               Using SCPI command thru Python with VISA module             #
#               Visit https://pyvisa.readthedocs.io for install             #
#############################################################################
# Com negociated/conf by VISA                                               #
# Baudrate : 9600           Data bits : 8           Flow Control : None     #
# Parity   : None           Stop bits : 1                                   #
# Host returning a result after a querry command : <Result> + <CR> <LF>     #
#############################################################################
# GUI - Computing values and convert, format                                #
#       to display mesured values properly                                  #
#       Display status and config of the instrument                         #
#############################################################################

import sys
# Libs for pgm
import visa
import time
##############

from itertools import product
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFrame, QLCDNumber, QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout, QWidget

#--------------------------------------------------------------------------
# INIT serial connection via VISA
rm = visa.ResourceManager()
rm.list_resources()
('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::12::INSTR')
# Port path copied from visa console '>list'
inst = rm.open_resource('ASRL/dev/ttyUSB0::INSTR')

inst.baud_rate = 9600
inst.data_bits = 8
inst.stopBits = 1
inst.write_termination= '\r\n'
inst.read_termination = '\r\n'

# Defining meter status and functions variables
#
ID = inst.query("*IDN?")            # ID of the device

# Current functions variables
FREQ = inst.query("FREQ?")          # Mesurement frequency <100|120|1k|10k|100k>
VOLT = inst.query("VOLT?")          # Mesurement voltage <0.3v|0.6v|1v>
FUNC_A = inst.query("FUNC:impa?")   # Primary <L|C|R|Z|DCR|NULL>
FUNC_B = inst.query("FUNC:impb?")   # Secondary <D|Q|THETA|ESR|NULL>
MODE = inst.query("FUNC:EQU?")      # Equivalent mode <SER|PAL>

# Tolerance mode variables
TOL_STAT = inst.query("CALC:TOL:STAT?")     # Status <ON|OFF>
TOL_NOM = inst.query("CALC:TOL:NOM?")       # Nominal value <NR3|-->
TOL_VAL = inst.query("CALC:TOL:VALU?")      # Percentage value <NR3|-->
TOL_RANGE = inst.query("CALC:TOL:RANG?")    # Tolerance range <BIN1|BIN2|BIN3|BIN4|-->

# Recording mode variables
REC_STAT = inst.query("CALC:REC:STAT?")     # Status <ON|OFF>
REC_MIN = inst.query("CALC:REC:MIN?")       # Minimum value <NR3,NR3|-->
REC_MAX = inst.query("CALC:REC:MAX?")       # Maximum value <NR3,NR3|-->
REC_AVG = inst.query("CALC:REC:AVER?")      # Average value <NR3,NR3|-->
REC_INST = inst.query("CALC:REC:PRES?")     # Present value <NR3,NR3|-->

# Fetch the primary, secondary and tolerance
FETCH = inst.query("FETC?")                 # If LCR <NR3,NR3,NR1>, if DCR <NR3,NR1>
PRI_DIS, SEC_DIS = FETCH.split(",", 1)      # Isolate the Primary value
SEC_DIS, TOL_DIS = SEC_DIS.split(",", 1)    # Isolate the Secondary and Tolerance

#--------------------------------------------------------------------------
"""
def startupInfo():                      # Info that dont change
    ID = inst.query("*IDN?")            # ID of the device

def functionStatus():                   # Infos parsed after every function change
    LOCK = 0                            # Lockout status (see *LLO and *GTL) set to 0
    FREQ = inst.query("FREQ?")          # Mesurement frequency <100|120|1k|10k|100k>
    VOLT = inst.query("VOLT?")          # Mesurement voltage <0.3v|0.6v|1v>
    FUNC_A = inst.query("FUNC:impa?")   # Primary <L|C|R|Z|DCR|NULL>
    FUNC_B = inst.query("FUNC:impb?")   # Secondary <D|Q|THETA|ESR|NULL>
    MODE = inst.query("FUNC:EQU?")      # Equivalent mode <SER|PAL>

def calcStatus():
    TOL_STAT = inst.query("CALC:TOL:STAT?")     # Status <ON|OFF>
    TOL_NOM = inst.query("CALC:TOL:NOM?")       # Nominal value <NR3|-->
    TOL_VAL = inst.query("CALC:TOL:VALU?")      # Percentage value <NR3|-->
    TOL_RANGE = inst.query("CALC:TOL:RANG?")    # Tolerance range <BIN1|BIN2|BIN3|BIN4|-->

def recStatus():
    REC_STAT = inst.query("CALC:REC:STAT?")     # Status <ON|OFF>
    REC_MIN = inst.query("CALC:REC:MIN?")       # Minimum value <NR3,NR3|-->
    REC_MAX = inst.query("CALC:REC:MAX?")       # Maximum value <NR3,NR3|-->
    REC_AVG = inst.query("CALC:REC:AVER?")      # Average value <NR3,NR3|-->
    REC_INST = inst.query("CALC:REC:PRES?")     # Present value <NR3,NR3|-->
"""
def displayRefresh():                           # Continuous display refresh
    FETCH = inst.query("FETC?")                 # If LCR <NR3,NR3,NR1>, if DCR <NR3,NR1>
    PRI_DIS, SEC_DIS = FETCH.split(",", 1)      # Isolate the Primary value
    SEC_DIS, TOL_DIS = SEC_DIS.split(",", 1)    # Isolate the Secondary and Tolerance

#--------------------------------------------------------------------------
def tolTest():
    t = inst.query("CALC:TOL:STAT?")     # Status <ON|OFF>
    if t == "OFF":
        inst.query("CALC:TOL:STAT ON")
    else:
        inst.query("CALC:TOL:STAT OFF")


def recTest():
    r = inst.query("CALC:REC:STAT?")     # Status <ON|OFF>
    if r == 'OFF':
        inst.query("CALC:REC:STAT ON")
    else:
        inst.query("CALC:REC:STAT OFF")


def sendCommand(n):
    while True:
        if n == 'L':
            inst.query("FUNC:impa L")
        elif n == 'C':
            inst.query("FUNC:impa C")
        elif n == 'R':
            inst.query("FUNC:impa R")
        elif n == 'Z':
            inst.query("FUNC:impa Z")
        elif n == 'DCR':
            inst.query("FUNC:impa DCR")
        elif n == 'D':
            inst.query("FUNC:impb D")
        elif n == 'Q':
            inst.query("FUNC:impb Q")
        elif n == 'THETA':
            inst.query("FUNC:impb THETA")
        elif n == 'ESR':
            inst.query("FUNC:impb ESR")
        elif n == '100Hz':
            inst.query("FREQ 100")
        elif n == '120Hz':
            inst.query("FREQ 120")
        elif n == '1kHz':
            inst.query("FREQ 1000")
        elif n == '10kHz':
            inst.query("FREQ 10000")
        elif n == '100kHz':
            inst.query("FREQ 100000")
        elif n == '0,3v':
            inst.query("VOLT 0.3")
        elif n == '0,6v':
            inst.query("VOLT 0.6")
        elif n == '1v':
            inst.query("VOLT 1")
        elif n == 'SER':
            inst.query("FUNC:EQU SER")
        elif n == 'PAL':
            inst.query("FUNC:EQU PAL")
        elif n == 'TOL':
            tolTest()                       # ON / OFF toggle
        elif n == '1%':
            inst.query("CALC:TOL:RANG 1")
        elif n == '5%':
            inst.query("CALC:TOL:RANG 5")
        elif n == '10%':
            inst.query("CALC:TOL:RANG 10")
        elif n == '20%':
            inst.query("CALC:TOL:RANG 20")
        elif n == 'LLO':
            inst.query("*LLO")
        elif n == 'GTL':
            inst.query("*GTL")
        elif n == 'REC':
            recTest()                       # ON / OFF toggle
        elif n == 'TRG':
            inst.query("*TRG")
        else:
            return callfunction

#--------------------------------------------------------------------------
class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent=parent)
        self.layoutUI()

    def layoutUI(self):
        self.setStyleSheet("background-color: purple;")
        # Set ID of the instrument via a var = *IDN?
        self.setWindowTitle(ID)

        self.principalLayout = QHBoxLayout(self)

        self.rightFrame = QFrame(self)
        self.rightFrame.setFrameShape(QFrame.StyledPanel)
        self.rightFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.rightFrame)
        self.gridLayout = QGridLayout()

        # Affichage LCD PRIMARY
        self.lcdPRI = QLCDNumber()
        self.gridLayout.addWidget(self.lcdPRI, 0, 0, 2, 0)
        # Affichage LCD SECONDARY
        self.lcdSEC = QLCDNumber()
        self.gridLayout.addWidget(self.lcdSEC, 2, 0, 4, 0)

        btns = {(0, 0): "L", (0, 1): "C", (0, 2): "R", (0, 3): "Z", (0, 4): "DCR",
                (1, 0): "D", (1, 1): "Q", (1, 3): "THETA", (1, 4): "ESR",
                (2, 0): "100Hz", (2, 1): "120Hz", (2, 2): "1kHz", (2, 3): "10kHz", (2, 4): "100kHz",
                (3, 0): "0,3v", (3, 1): "0,6v", (3, 2): "1v", (3, 3): "SER", (3, 4): "PAL",
                (4, 0): "TOL", (4, 1): "1%", (4, 2): "5%", (4, 3): "10%", (4, 4): "20%",
                (5, 0): "LLO", (5, 1): "GTL", (5, 3): "REC", (5, 4): "TRG"}
        for pos, name in btns.items():
            x, y = pos
            btn = QPushButton(self.rightFrame)
            btn.setText(name)
            self.gridLayout.addWidget(btn, x+6, y)      # x+6 = hauteur affichages LCDs
            # When btn is clicked, send his 'name' to 'make_callfunction'
            btn.clicked.connect(self.make_callfunction(name))
        self.verticalLayout.addLayout(self.gridLayout)
        self.principalLayout.addWidget(self.rightFrame)
        # Display watever --> QLCDNumber a config pour l'affichage complet :
        self.lcdPRI.display(PRI_DIS)    # Format 6 digits +exp (p, n, u, m, unit)
        self.lcdSEC.display(SEC_DIS)    # Format (PRI: +6.74095e-13 SEC: +2.52358e-02)


    # Print the 'name' of the clicked btn inthe console
    def make_callfunction(self, name):
            def callfunction():
#                print(name)
                displayRefresh()
                sendCommand(name)
                #time.sleep(1)
            return callfunction

"""            while True:
                time.sleep(1)
                make_callfunction()
"""
#--------------------------------------------------------------------------


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
