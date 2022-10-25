import subprocess
import sys

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    import pyfirmata #facilitates communication with Arduino https://pyfirmata.readthedocs.io/en/latest/
except:
    install('pyfirmata')
    import pyfirmata
try:
    import time  #Required to use delay functions
except:
    install('time')
    import time
#try:
#    from progress.bar import ChargingBar
#except:
#    install('progress.bar')
#    from progress.bar import ChargingBar
try:
    from tqdm import tqdm
except:
    install('tqdm')
    from tqdm import tqdm

""" 
Tester function to check the circuit assembly. The input port must be a
string specifying the computer port your circuit is plugged into,
'COMxx'. While this tester function can point you to possible errors, it
is not meant to be an all-rounded benchmark routine. It works by
connecting to arduino and setting the PWM output to the maximal value
and comparing the initial signal with the heated up signal. If the latter
is smaller, than R2 can heat up fine. I recommend using a thermocouple to
measure the temperature of R2 while heating up, so you can manually check
if it works. Always start from room temperature (~22 C). Make sure that
the temperature of R2 is steady at the start. The signal difference
should be around 0.3 V if R2 is not insulated and started from 22 C. If
the signal difference is equal to zero than the problem is in the
readout. """


portName = 'COM5'
# portName = '/dev/cu.usbmodem14201'
arduino = pyfirmata.Arduino(portName)
cnd = False
it = pyfirmata.util.Iterator(arduino)
it.start()

try:
    #Connect to arduino hardware on input port.
    input_pin = arduino.get_pin('a:0:i') #analog, input to the computer
    output_pin = arduino.get_pin('d:3:o') #digital, output from the computer
    output_pin.mode = 3  #PWM mode
    # Set the output of digital pin 3 to high (5V), this will heat R2
    output_pin.write(1) #writes to D3
    time.sleep(5)
    #set the output of digital pin 3 to low (0V)
    output_pin.write(0)
    print('Connection established. \n')
    cnd = True

except:
    print('Can not connect. \n')
    print('Possible errors: \n')
    print('- the arduino is not installed properly.  \n Ensure that the proper driver is installede and the correct .inf file is uploaded to ruggeduino. \n')
    print('- the connection between arduino and the computer is faulty. \n Try restarting the computer or a different USB cable \n')

if cnd:
    try:
        # Read the voltage to the analog pin 0 when the digital pin 3 signal
        # is low
        signal0 = 5*input_pin.read()
        # Set digital pin 3 to high to heat up resistor R2
        output_pin.write(1)
        #bar = ChargingBar('Heating up...', max=20)
        signal1 = 0
        for i in tqdm(range(20)):
            time.sleep(3)
            #bar.next()
            #if i == 20:
        # Read the voltage to analog pin 0 after R2 has heated
        signal1 = 5*input_pin.read()
        print((signal0 - signal1),' V.')
        # Set the ouptut of digital pin 3 to low (0V)
        output_pin.write(0)
        #bar.finish()

        if signal0 - signal1 > 0.2:
            print('R2 heating is functional. \n')
            print('Circuit assembled successfully. \n')
        elif signal0 - signal1 > 0.1 and signal0 - signal1 <= 0.2:
            print('R2 heating is functional but the power output is too low. \n')
            print('Are you running the test at steady room temperature?. \n')
        else:
            print('R2 heating does not work, the environment is extreme \n or the signals can not be read out. \n')

    except:
        print('Can not write the PWM output properly. \n')
        print('Possible problems: \n')
        print('- the circuit is not assembled correctly. Check the schematic. \n')
        print('- your R2 resistor is too hot. Wait for it to cool down. \n')


wait = input("Press Enter to Continue")