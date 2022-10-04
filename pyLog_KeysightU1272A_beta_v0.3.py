'''
This is the logger script for save data from Keysight U1272A to ".csv" file.
Tobias Haueter PF32
'''
# send_receive('*IDN?')              - Identification
# send_receive('SYST:BATT?')         - Request batterie status. Not sure what units are returned.
# send_receive('CONF?')              - Request confirguration display (e.g. "VOLT:AC +5.00000000E+00,+1.00000000E-04")
# send_receive('CONF? @2')           - Request confirguration secondary display (e.g. "VOLT:AC +5.00000000E+00,+1.00000000E-04")
# send_receive('STAT?')              - Request unit status. I have not decoded the meaning of the return value for this. (e.g. "000000I00302L00004001")
# send_receive('FETC?')              - Request current reading (display)
# send_receive('FETC? @2')           - Request current reading (secondary display)
# send_receive('*RST')               - Meter reset
# send_receive('SYST:VERS?')         - Unknown, my meter returns 1990.0
# send_receive('SYST:ERR?')          - Unknown, probably returns the last error
# send_receive('READ?')              - Request current reading. I don't believe that the @2 option works for this command.
# send_receive(LOG:AUTO xx)          - Request value of auto-log position xx
# send_receive(LOG:HAND xx)          - Request value of manual log position xx
# send_receive('SYST:AOFF:TIME 10')  - Auto Power OFF Enabled with timer 10min
# send_receive('SYST:AOFF:TIME 0')  - Auto Power OFF Disabled


# lib import
import os
import serial
import sys
import time
from datetime import datetime
# import csv
import serial.tools.list_ports
from art import *

# file import
import my3xceptions

# SCRIPT CONFIGURATION
# ---------------------------------------------------------------------------------------------------------------------
# File Name
fileName_1 = "keysightU1272a-log"

# File Content
header = f"Counter,Timestamp,Reading,RangeSetting,SecondaryReading,SecondaryRange,BatteryStatus\n"

# Communication
comport_usb = 'COM6'  # Windows
# comport_usb = '/dev/ttyUSB0' # Linux

# Logger
samples_time_ms = 1000
# ---------------------------------------------------------------------------------------------------------------------
# CLI
# banner
cwd = str(os.getcwd())
print('------------------------------------------------------------------')
print('pyKeysight U1272A Logger                                 beta v0.3')
print('------------------------------------------------------------------')
print(text2art("KEYSIGHT") + '                                            2022 by Tobias Haueter')
print('------------------------------------------------------------------')
print('Current Working Directory: ' + cwd)
print('------------------------------------------------------------------')

# check all usb com ports
ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
    print(f"{port}: {desc} | [{hwid}]")
print('------------------------------------------------------------')
comport_usb = input(f'Choose USB ComPort (Keysight U1272A -> Prolific): ')
print(f'ComPort -> {comport_usb}')
print('------------------------------------------------------------')

samples_time_ms = input(f'Choose sample time in ms (default: 1000 ms): ')
if not samples_time_ms:
    samples_time_ms = 1000
    float(samples_time_ms)

print(f'Samples per second -> {samples_time_ms}')
print('************************************************************')

print(f' -- STOP LOG: Press <Ctrl+C> --')
input(f'Press <ENTER> to start the logger')

print('************************************************************')

# ---------------------------------------------------------------------------------------------------------------------

# AVOR
# Get the current time to build a time-stamp.
appStartTime = datetime.now()
startTimeStr = appStartTime.strftime("%Y-%m-%dT%H:%M:%S")
timeStr = appStartTime.strftime("%Y%m%dT%H%M%S")

# Get the current working directory
# folder = 'Keysight-DataLogs'
# cwd = str(os.getcwd()) + '/' + str(folder)
# cwd = str(os.getcwd())

# Create File Name
# fileName = f"{fileName_1}_" + timeStr + ".csv"
fileName = "%s.csv" % (fileName_1)
filePath = os.path.join(cwd, fileName)
print(filePath)

# Choose ComPort USB
if len(sys.argv) == 2:
    serial_devname = sys.argv[1]
else:
    serial_devname = comport_usb

try:
    ser = serial.Serial(serial_devname, 9600, timeout=0.5)

except:
    my3xceptions.logger.error('   - [%s/loggerToFile()] -- Serial Connection ERROR --' % (os.path.basename(__file__)))


# FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------
def autopoweroff(state):
    if state == 'off':
        send_command(b'SYST:AOFF:TIME 0')  # Auto Power OFF Disabled
        send_command(b'SYST:AOFF:TIME 0')  # Auto Power OFF Disabled
        print('AutoPowerOff -> not Active')

    if state == 'on':
        send_command(b'SYST:AOFF:TIME 10')  # Auto Power OFF Enabled with timer 10min
        send_command(b'SYST:AOFF:TIME 10')  # Auto Power OFF Enabled with timer 10min
        print('AutoPowerOff -> Active (10min)')


def send_command(command):
    if ser.inWaiting():
        # Providing a way to resynchronize, if we have several outstanding
        # requests. (Only seen this when the user rotates the range switch)
        raise ValueError("ERROR: Unexpected characters read. Throwing away " +
                         "\"" + str(ser.read(1000)) + "\"")

    ser.write(command + b'\n')
    time.sleep(0.01)
    received = ser.readline()


def send_receive(command):
    if ser.inWaiting():
        # Providing a way to resynchronize, if we have several outstanding
        # requests. (Only seen this when the user rotates the range switch)
        raise ValueError("ERROR: Unexpected characters read. Throwing away " +
                         "\"" + str(ser.read(1000)) + "\"")

    ser.write(command + b'\n')
    time.sleep(0.01)
    received = ser.readline()

    if len(received) and received[0] == '*':
        # Rotation of the range switch sends messages starting with a "*" which
        # destroys our synchronization. (What we read is not the response of
        # the command we sent.)
        raise ValueError("ERROR: Unexpected characters read. Throwing away \"" +
                         str(received) + "\"")

    if len(received) == 0:
        raise ValueError("ERROR: No response received for command \"" +
                         command + "\"")

    received = received.replace(b'\n', b'')
    received = received.replace(b'\r', b'')
    return received.decode("utf-8")


def loggerToFile():

    global reading1, conf1, reading2, conf2, batt, idn

    try:
        idn = send_receive(b'*IDN?')
        print('-----------------------------------------------------------------------')
        print('# Measurement source: %s\n' % idn)
    except ValueError as e:
        my3xceptions.logger.error(
            '   - [%s/loggerToFile()] -- idn = send_receive(b\'*IDN?\') ERROR --' % (os.path.basename(__file__)))
        print(e.args, file=sys.stderr)
        print("ERROR: terminating since meter failed to respond to \"*IDN?\"."
              + "\nIs the meter turned on and connected?", file=sys.stderr)
        exit(1)

    # open file with write mode to add the header.
    try:
        f = open(fileName, mode='w', encoding='UTF8')
        f.write(header)
        f.close()
    except:
        my3xceptions.logger.error(
            '   - [%s/loggerToFile()] -- Write header to file ERROR --' % (os.path.basename(__file__)))

    my3xceptions.logger.info('    - **************************************')
    my3xceptions.logger.info('    - [%s/loggerToFile()] ** Logger START **' % (os.path.basename(__file__)))
    my3xceptions.logger.info(f'    - [%s/loggerToFile()] ** {idn} | {comport_usb} **' % (os.path.basename(__file__)))
    my3xceptions.logger.info(f'    - [%s/loggerToFile()] ** ComPort: {comport_usb} | Sample time [ms]: {samples_time_ms} **' % (os.path.basename(__file__)))
    my3xceptions.logger.info('    - **************************************')
    time.sleep(0.2)


    print("Counter\tTimestamp\t                Reading\t    Range setting\tSecondary reading\t" +
          "Secondary range\t BatteryStatus")

    # Loop with read and save data
    loopCnt = 0
    try:
        while True:
            tic = time.perf_counter()

            now = datetime.now()
            # commands
            try:
                reading1 = send_receive(b'READ?')
                reading2 = send_receive(b'FETC? @2')
                conf1 = send_receive(b'CONF?')
                conf2 = send_receive(b'CONF? @2')
                batt = send_receive(b'SYST:BATT?')
            except:
                my3xceptions.logger.error(
                    '   - [%s/loggerToFile()] -- Reading values from DMM ERROR --' % (os.path.basename(__file__)))

            # timestamp
            msecs = now.microsecond / 1000
            timestring = now.strftime("%Y-%m-%d %H:%M:%S") + '.%04d' % (msecs)

            # actual data preparation and print to terminal
            data = (f'{loopCnt},{timestring},{float(reading1):.5f},{conf1},{float(reading2):.5f},{conf2},{batt}\n')
            print(
                f'{loopCnt}\t    {timestring}\t{float(reading1):.5f}\t    {conf1}\t    {float(reading2):.5f}\t        {conf2}\t         {batt}\t')

            # open file with append mode to add the data under the header.
            try:
                f = open(fileName, mode='a', encoding='UTF8')
                f.write(data)
                f.close()
            except:
                my3xceptions.logger.error(
                    '   - [%s/loggerToFile()] -- Open file and append to file ERROR --' % (os.path.basename(__file__)))

            # Rate limit sampling by sleeping to achieve the samplerate <<samples_time_ms>>

            toc = time.perf_counter()
            # my3xceptions.logger.debug(
            #     f'   - [%s/loggerToFile()] -- Executet in {toc - tic:0.4f} seconds --' % (os.path.basename(__file__)))
            round((toc - tic), 4)

            sleep_ms = samples_time_ms - (toc - tic)
            time.sleep(sleep_ms / 1000)

            loopCnt += 1

    except Exception as e:
        my3xceptions.logger.error(f'   - [%s/loggerToFile()] -- {e} --' % (os.path.basename(__file__)))

    autopoweroff('on')


if __name__ == "__main__":
    try:
        autopoweroff('off')
        loggerToFile()
    except Exception as e:
        my3xceptions.logger.error(f'   - [%s/main()] -- {e} --' % (os.path.basename(__file__)))
        autopoweroff('on')
    except KeyboardInterrupt:
        autopoweroff('on')
        my3xceptions.logger.info(
            '    - [%s/main()] ++ Logger Stopped via KeyboardInterrupt ++' % (os.path.basename(__file__)))
        input(f'EXIT: Press <ENTER>')
