import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.metrics import r2_score
style.use('ggplot')
import sys

data = pd.read_csv('p3_experimental_data.csv')

cooling_model = LinearRegression()
cooling_model.fit(np.array(data['DCd1']).reshape(-1,1),data['Td1'])

heating_model1 = LinearRegression()
heating_model2 = LinearRegression()
heating_model1.fit(np.array(data['DC1']).reshape(-1,1), data['T1'])
heating_model2.fit(np.array(data['DC2']).reshape(-1,1), data['T2'])

DCrange = np.linspace(0,1, 100)
predictedTd1 = cooling_model.predict(DCrange.reshape(-1,1))
predictedT1 = heating_model1.predict(DCrange.reshape(-1,1))
predictedT2 = heating_model2.predict(DCrange.reshape(-1,1))

coolingR2 = r2_score(data['Td1'], cooling_model.predict(np.array(data['DCd1']).reshape(-1,1)))
heating1R2 = r2_score(data['T1'], heating_model1.predict(np.array(data['DC1']).reshape(-1,1)))
heating2R2 = r2_score(data['T2'], heating_model2.predict(np.array(data['DC2']).reshape(-1,1)))
#heating1 model produces better R2


def graph():
    fig, ax = plt.subplots(2)

    ax[0].plot(DCrange, predictedT1, label = 'Model')
    ax[0].scatter(data['DC1'], data['T1'], color = 'royalblue', label =  'Experimental Data')
    ax[0].legend()
    ax[0].set_ylabel('Temperature (C)', labelpad=10)
    ax[0].set_title('Heating')
    ax[0].annotate(f'R2 = {round(heating1R2,2)}', (.25, 23.1), fontsize = 15)


    ax[1].plot(DCrange, predictedTd1, label = 'Model')
    ax[1].scatter(data['DCd1'], data['Td1'], color= 'royalblue',  label = 'Experimental Data')
    ax[1].legend()
    ax[1].set_ylabel('Temperature (C)', labelpad=10)
    ax[1].set_xlabel('DC Input',labelpad=10)
    ax[1].set_title('Cooling')
    ax[1].set_xlim(1.05,-.05)
    ax[1].annotate(f'R2 = {round(coolingR2, 2)}', (.25, 23.1), fontsize=15)

    plt.show()
graph()
print(cooling_model.coef_)
print(heating_model1.coef_)