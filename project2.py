from pyfirmata import Arduino
import pandas as pd
import sys
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
import time

calib_curve = pd.read_csv('calibration_curve.csv')
calib_curve = calib_curve[calib_curve['Temperature'] <= 80]
calib_curve = calib_curve[calib_curve['Temperature'] >= 0].reset_index()

Tpred = interp1d(calib_curve['Resistance'], calib_curve['Temperature'], kind='cubic')
dTpred = interp1d(calib_curve['Resistance'], calib_curve['dT'], kind = 'cubic')
port = 'COM5'

#testing interpolation accuracy
def test_interp():
    test = np.linspace(5000, 30000, 100)
    plt.plot(test, Tpred(test), linewidth = 2, label = 'pred')
    plt.plot(calib_curve['Resistance'], calib_curve['Temperature'], linestyle='--', label = 'actual data')
    plt.legend()
    plt.show()

def room_temp():
    board = Arduino(port)
    input_pin = board.get_pin('a:0:i')  # analog, input to the computer
    VA0 = np.float64(input_pin.read())
    print(VA0)



def gather_data():
    data = pd.DataFrame(columns=['PWMinput', 'T'])
    board = Arduino(port)
    input_pin = board.get_pin('a:0:i')  # analog, input to the computer
    PWM_pin = board.get_pin('d:3:p')  # digital, output from the computer
    PWM_pin.mode = 3
    R3 = 15000 #ohm
    V5 = 5 #volts
    PWMrange = np.linspace(0,1,50)

    for PWM in PWMrange:
        PWM_pin.write(PWM)
        time.sleep(15)
        VA0 = np.float64(input_pin.read())

        if VA0 != float:
            print(f'VA0 = {VA0} is invalid.')
            sys.exit()

        R4 = R3 * VA0 / (V5 - VA0)
        data = data.append({'PWMinput':PWM,
                            'R' : R4,
                            'T': Tpred(R4),
                            'error' : dTpred(R4)}, ignore_index = True)
        print(f'Done with PWM = {PWM}')
    data.to_csv('test_data.csv')
    print('Data collection completed')

gather_data()

def graph():
    data = pd.read_csv('test_data.csv')
    R = data['R']
    PWM = data['PWMinput']
    T = data['T']
    error = data['error']

    fig,ax = subplots(2)

    ax[0].plot(R, T, label = 'Calculated Curve')
    ax[0].plot(calib_curve['Resistance'], calib_curve['Temperature'], label = 'True Calibration Curve')
