import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

#TODO Find better way to display dates
#TODO make more graphs

#Returns Database of rock climbing data
def generateDatabase():
    #Set file to read from here
    file = 'Climbing Log.csv'
    #csv file should contain 3 columns: Date, Success (True/False value), Grade (standard YDS for rock climbing, supports 5.2-5.15d)
    return pd.read_csv(file, parse_dates= ['Date'], dtype={'Grade': 'str'})

#Sanitizes data in provided database
def sanitizeData(df):    
    #Convets grade letters to fractional system to make it easier for analysis
    df['Grade'] = df['Grade'].replace(to_replace='a', value='00', regex=True)
    df['Grade'] = df['Grade'].replace(to_replace='b', value='25', regex=True)
    df['Grade'] = df['Grade'].replace(to_replace='c', value='50', regex=True)
    df['Grade'] = df['Grade'].replace(to_replace='d', value='75', regex=True)
    
    #Changes + to halfway between current grade to next grade
    df['Grade'] = df['Grade'].replace(to_replace='\+', value='5', regex=True)
    
    #Fixes 5.2s-5.9s from appearing larger than 5.10s-5.15s
    df['Grade'] = df['Grade'].replace(to_replace='(5\.)(?=[2-9]+)', value='5.0', regex=True)
    
    #Fixes Date and Grade columns to proper types
    df['Grade'] = pd.to_numeric(df['Grade'])
    
    #Sort by Date
    df = df.sort_values(by=['Date'])
    
    return df

#Generates Boxplot Chart showing distribution of successful ascent grades
def generateBoxplotChart(df):
    df = df[df['Success'] == True]
    df.boxplot(column=['Grade'], by=['Date'])
    plt.title('Daily Distribution of Successful Ascents')
    plt.suptitle("")
    plt.xlabel('Date')
    plt.ylabel('Grade')
    plt.ylim(5.0, 5.16)
    plt.yticks(np.arange(5.0, 5.16, .01))
    plt.xticks(rotation=15)
    plt.show()
    
db = generateDatabase()
db = sanitizeData(db)
generateBoxplotChart(db)
