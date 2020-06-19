#https://numpy.org/doc/1.18/user/quickstart.html
import numpy as np
#Source https://pandas.pydata.org/docs/user_guide/index.html
import pandas as pd
#Source https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html
#Also used docs for settings.
from sklearn.ensemble import GradientBoostingRegressor
#Used K-Fold when we had less data, left it to show things we tried.
from sklearn.model_selection import train_test_split, KFold
import ast
#Source https://joblib.readthedocs.io/en/latest/
import joblib

#Import Data
df = pd.read_csv('game_data2.csv')
#Prepare Data
print(len(df))
#Drop duplicates
#df = df.drop_duplicates(keep=False)
print(len(df))
#Remove bad moves
#split for players
print(df)
""""""
#Player 1
#df = df.loc[df['player'] == '-1']
#Player 2
df = df.loc[df['player'] == '1']
""""""
print(len(df))
#Split the data
x_data = np.array(df['board'])
y_data = np.array(df['win_percent']).astype(np.float)
#Boards were saved as string, ast.literal_eval turns the string into a List of numbers
#Found implementation at https://stackoverflow.com/questions/23119472/in-pandas-python-reading-array-stored-as-string
x_data = np.array([ast.literal_eval(each) for each in x_data])
print(x_data)
print(len(x_data))
print(len(y_data))
print(y_data)
#Split data into sets
x_train, x_test, y_train, y_test = train_test_split(x_data,y_data)

#gbr settings
#Found that this setting worked well
gbr = GradientBoostingRegressor(n_estimators = 100 , max_depth=5)
gbr.fit(x_train, y_train)
print(gbr.score(x_test, y_test))
#KFold training
"""
kf = KFold(n_splits = 5, shuffle = False)
gbr_out = []
for x, y in kf.split(x_data):
    gbr.fit(x_data[x],y_data[x])
    gbr_out.append(gbr.score(x_data[y], y_data[y]))
print("Gradient Boosting Regressor: {}".format((sum(gbr_out)/5)))
"""
#Save the model
#Change based in the player
joblib.dump(gbr, 'player_2.1_model.pkl', compress=9)
