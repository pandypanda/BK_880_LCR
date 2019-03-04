#############################################################################
# 				Andy's test for BK Precision LCR Meter 880					#
# 				Using SCPI command thru Python with VISA module				#
#				Visit https://pyvisa.readthedocs.io for install				#
#############################################################################
# Com negociated/conf by VISA 												#
# Baudrate : 9600			Data bits : 8			Flow Control : None		#
# Parity   : None			Stop bits : 1									#
# Host returning a result after a querry command : <Result> + <CR> <LF>		#
#############################################################################


import visa

rm = visa.ResourceManager()
rm.list_resources()
('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::12::INSTR')
# Port path copied from visa console '>list'
inst = rm.open_resource('ASRL/dev/ttyUSB1::INSTR')

# Querries - ask the meter who he is and current status of all its functions

# Status Querry
ID = inst.query("*IDN?")			# ID of the device
LOCK = 0							# Store the Lockout status (see *LLO and *GTL)
FREQ = inst.query("FREQ?")			# Mesurement frequency <100|120|1k|10k|100k>
VOLT = inst.query("VOLT?")			# Mesurement voltage <0.3v|0.6v|1v>
FUNC_A = inst.query("FUNC:impa?")	# Primary <L|C|R|Z|DCR|NULL>
FUNC_B = inst.query("FUNC:impb?")	# Secondary <D|Q|THETA|ESR|NULL>
MODE = inst.query("FUNC:EQU?")		# Equivalent mode <SER|PAL>

# Tolerance mode variables
TOL_STAT = inst.query("CALC:TOL:STAT?")		# Status <ON|OFF>
TOL_NOM = inst.query("CALC:TOL:NOM?")		# Nominal value <NR3|-->
TOL_VAL = inst.query("CALC:TOL:VALU?")		# Percentage value <NR3|-->
TOL_RANGE = inst.query("CALC:TOL:RANG?")	# Tolerance range <BIN1|BIN2|BIN3|BIN4|-->

# Recording mode variables
REC_STAT = inst.query("CALC:REC:STAT?")		# Status <ON|OFF>
REC_MIN = inst.query("CALC:REC:MIN?")		# Minimum value <NR3,NR3|-->
REC_MAX = inst.query("CALC:REC:MAX?")		# Maximum value <NR3,NR3|-->
REC_AVG = inst.query("CALC:REC:AVER?")		# Average value <NR3,NR3|-->
REC_INST = inst.query("CALC:REC:PRES?")		# Present value <NR3,NR3|-->

# Fetching displayed data 			# Fetch the primary, secondary and tolerance
FETCH = inst.query("FETC?")			# If LCR <NR3,NR3,NR1>, if DCR <NR3,NR1>
	 								
# Store the lot in a tuple called "data"
data = (ID, LOCK, FREQ, VOLT, FUNC_A, FUNC_B, MODE, TOL_STAT, TOL_NOM, 
		TOL_VAL, TOL_RANGE, REC_STAT, REC_MIN, REC_MAX, REC_AVG, REC_INST, FETCH)

# Display function
# Print status and fetched datas in a decorated way
print(data) # for testing :)
