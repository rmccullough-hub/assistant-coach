import csv
import os 

import pandas as pd
import numpy as np
from sklearn import linear_model

module_dir = os.path.dirname(__file__)

# code that predicts a given player's performace.
# takes the player's average points per game, rank of opponent, and file path to data specific to the player's position. 
def predictions(avg, opponent_rank, file):

	# the next two lines access a CSV file with the relevant data, given the position of the player.
    file_path = os.path.join(module_dir, file)

    df = pd.read_csv(open(file_path, 'r'))

    # trains a simple multivariate regression model.
    reg = linear_model.LinearRegression()
    reg.fit(df.drop('ftsp', axis='columns'), df.ftsp)

    return reg.predict([[avg, opponent_rank]])



