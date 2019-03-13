# BK_880_LCR
Python - VISA - SCPI scrypt to controll them all :)

Work in progress to control the BK Precision 880 LCR Meter (for Linux as no soft available).

Serial connection over USB managed by VISA (https://pyvisa.readthedocs.io).

Sending commands/queries and retrieving instrument data is achieved using SCPI commands
(RTFM for SCPI commands and format:)) according to IEEE 488.2 standard.
(https://www.bkprecision.com/products/component-testers/880-dual-display-handheld-100khz-lcr-meter-with-esr.html)

The GUI needs PyQt5 (see 'GUI' code)

----
This is my first proper program (with a GUI) in Python... not finished yet :).
Feel free to comment / help as Im new to Python (more used to #ASM on µC and x86)

Update (13 march 2019):
  -  	GUI_880_LCR_MERGE.py  <-- trying to bodge together the GUI and the prog ;)
      Quite crude for now but command of functions works (need to add more/finish)
      Primary and secondary display not functionnal yet....

TODO (11 march 2019):
  - Functions to compute and format the primary and secondary display
    format +/_ 6 digits +exp (+6.74095e-13) TO -/+ 6 digits and readable unit (46.8274 µF)
  - Display unit after 'LED' display (ex: µF, kΩ, mH, ...)
  - Display current settings / mode (L, C, R, ...) below LEDs displays or change
    the color of the corresponding button ???
  - Add a Quit/Exit button
  - MERGE the GUI and main prog
  - Hide keypad option, to keep only the display on screen
  - Clean the GUI, select a background color for the LCD displays,
    static size/proportions for the window, format for 6 digit display, ...
  - Third display for Tolerance check (Nominal Value|+/-Value|1/5/10/20%) ???
  - Record function display (MIN, MAX, AVG, Present value) ???
  - ...
  
Send me a word (andy_ecam [at] hotmail (.) com) if you see something wrong in the code or want to help finish, butcher a part,...
It's quite basic and not really usefull if you don't have the LCR meter. The GUI should run even if you don't have the meter
(as it is independant... just a few buttons and display without 'brain'). The prog 'BK_880_LCR.py' needs the meter.

Andy
