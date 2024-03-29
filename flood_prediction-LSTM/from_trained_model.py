# -*- coding: utf-8 -*-
"""from_trained_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xkS8OrcWGZTc8qaKwhmu8YD_iASwlJn8
"""

from tensorflow.python.keras.models import load_model
import pandas

model = load_model('my_model.h5')

model.summary()

# convert series to supervised learning
# structure data for multivariate lstm
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = pandas.DataFrame(data)
	cols, names = list(), list()
 
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]

	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]

	# put it all together
	agg = pandas.concat(cols, axis=1)
	agg.columns = names

	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

#10 hours historical data (sensor data)
realtime_data = {'rainfall (mm)': [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.9,0.0,0.0,0.0],
        'Level (m)': [0.34051556,0.44051556,0.44051556,0.42424242,0.42424242,0.42624242,0.42424242,0.42424242,0.42424242,0.42424242,0.42424242]
        }
demo_df = pandas.DataFrame(realtime_data, columns = ['rainfall (mm)', 'Level (m)'])

print (demo_df.head())

n_hours = 10
n_features = 2

#reframe
demo_data = demo_df.to_numpy()
#demo_data = concatenate((demo_data, demo_data,demo_data), axis=1)
print(demo_data.shape)
reframed_data = series_to_supervised(demo_data, n_hours, 1)
reframed_data = reframed_data.values
reframed_data = reframed_data[:,:20]
print(reframed_data.shape)

#reshaping
reframed_data = reframed_data.reshape((reframed_data.shape[0], n_hours, n_features))
# print(reframed_data.shape)

#make prediction (10 hours ahead of time)
predicted_waterlevel = model.predict(reframed_data)

print(predicted_waterlevel)

# invert scaling for forecast
inv_predicted_waterlevel = predicted_waterlevel[0][0] * 3.3
print(inv_predicted_waterlevel)

#@title Flood possibility

print('Expected water level in 10 hours is %.3f m' % inv_predicted_waterlevel )

#based on the dataset it is likely to flood when predicted water level exceeds 1.5 m
if (inv_predicted_waterlevel > 1.5):
  print("FLOOD")
else:
  print("No FLOOD")