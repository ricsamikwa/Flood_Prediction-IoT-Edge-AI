from tensorflow.python.keras.models import load_model
import pandas
import random
from time import sleep

#sensor data arrays
rainfall_array = []
water_level_array= []

# load trained LSTM model and print model summary
def loadTrainedLSTMModel():
    print("\n===========STARTING=============")
    model = load_model('./flood_prediction-LSTM/my_model.h5')
    print("\nModel Loaded\n")
    model.summary()
    return model

# structure data for multivariate lstm forecasting
def create_multivariate_LSTM_form(sensor_data_sequence, num_past_hours=1, num_predictions=1):
    
	num_features = sensor_data_sequence.shape[1]

	sensor_data_sequence_df = pandas.DataFrame(sensor_data_sequence)
	columns, names = list(), list()
 
	# past data to be observed for each prediction, i.e. input sequence (t-10, ... t-1)
	for n in range(num_past_hours, 0, -1):

		columns.append(sensor_data_sequence_df.shift(n))
		names += [('var%d(t-%d)' % (m+1, n)) for m in range(num_features)]

	# specifying the predicted output sequence i.e. (t,t+1, ...., t+10)
    # output is (t+10) in this case
	for n in range(0, num_predictions):
		columns.append(sensor_data_sequence_df.shift(-n))
		if n == 0:
			names += [('var%d(t)' % (m+1)) for m in range(num_features)]
		else:
			names += [('var%d(t+%d)' % (m+1, n)) for m in range(num_features)]

	# combine all columns and remove NaN values
	combined_data = pandas.concat(columns, axis=1)
	combined_data.columns = names
	combined_data.dropna(inplace=True)

	return combined_data

def getCurrentSensorData():
    current_rainfall_scaled = random.random()
    current_water_level_scaled = random.random()
    
    print('\nRainfall : %.3f mm' %(current_rainfall_scaled*111.4))
    print('Water Level : %.3f m\n' %(current_water_level_scaled*3.3))

    rainfall_array.append(current_rainfall_scaled)
    water_level_array.append(current_water_level_scaled)

def getSensorDataSequence():
    sleep(1)
    print("\n=========>\nProcessing data for forecasting at time : ",(pred_num +1))
    
    realtime_historical_data = {'rainfall (mm)': rainfall_array[pred_num:pred_num+11],
        'Level (m)': water_level_array[pred_num:pred_num+11]
        }
    print("\nDataframe with scaled values (required input for LSTM)")
    realtime_historical_data_df = pandas.DataFrame(realtime_historical_data, columns = ['rainfall (mm)', 'Level (m)'])
    print (realtime_historical_data_df)

    return realtime_historical_data_df


#data preprocessing
def dataPreprosessing(sensor_data_sequence_df):

    #number of hours to be observed when making a each forecast
    num_past_hours = 10

    #number of features to be observed
    features = 2

    #change data frame to array
    sensor_data_sequence = sensor_data_sequence_df.to_numpy()
    print(sensor_data_sequence.shape)
    
    #reframing the data for multivariate LSTM time series forecasting
    multi_LSTM_reframed_data = create_multivariate_LSTM_form(sensor_data_sequence, num_past_hours, 1)
    multi_LSTM_reframed_data = multi_LSTM_reframed_data.values
    #selecting required values
    multi_LSTM_reframed_data = multi_LSTM_reframed_data[:,:20]
    print(multi_LSTM_reframed_data.shape)

    #reshaping 
    multi_LSTM_reframed_data = multi_LSTM_reframed_data.reshape((multi_LSTM_reframed_data.shape[0], num_past_hours, features))

    return multi_LSTM_reframed_data

#prediction num
pred_num = 0

if __name__ == '__main__':
    
    #load model once
    model = loadTrainedLSTMModel()

    while True:
        getCurrentSensorData()

        if(len(rainfall_array) > 10):
            #10 hours historical rainfall and water level data
            sensor_data_sequence_df = getSensorDataSequence()

            processed_data =  dataPreprosessing(sensor_data_sequence_df)
        
            #make prediction of water level (10 hours ahead of time)
            predicted_waterlevel = model.predict(processed_data)

            print("==========>Forecasting")
            # invert scaling for forecast
            inv_predicted_waterlevel = predicted_waterlevel[0][0] * 3.3

            #@title Flood possibility

            print('Expected water level in 10 hours (t + 10) is %.3f m' % inv_predicted_waterlevel )

            print("-------------Flood possibility----------------")
            #based on the dataset it is likely to flood when predicted water level exceeds 1.5 m
            if (inv_predicted_waterlevel > 1.5):
                print("FLOOD")
                print("================>Issue Alert==============>")
            else:
                print("No FLOOD")

            print("Sleep")
            pred_num = pred_num + 1
            sleep(2)
        sleep(2)