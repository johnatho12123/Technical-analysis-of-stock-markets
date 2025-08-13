#stock Analysis Dashboard used to calculate basic technical
#  metrics such as:
#volatility , SMA , daily return ,ROC and more
#this project uses yahoo finance api for relevant data given by ticker

import yfinance as yf
import math
import numpy as np 
from datetime import datetime, timedelta
from monte_carlo_sim import gbm_sim as sim
from monte_carlo_sim import plotting as plot

def volatility(tckr):
    ticker = yf.Ticker(tckr)
    StartDate = input("Start Date(YYYY-MM-DD):")
    EndDate = input("End date (YYYY-MM-DD): ")
    history = ticker.history(start=StartDate,end=EndDate )
    listed = list(history["Close"])
    volatility = np.std(listed)#the vlatility is the standard deviation of all close values 
    volatility = round(volatility , 2)
    print(f"volatility: {volatility}")

def rsi(tckr):
    subtracted_list = []
    gains = []  
    loss = []
    ticker = yf.Ticker(tckr)
    StartDate = input("Start Date(YYYY-MM-DD):")
    EndDate = input("End date (YYYY-MM-DD): ")
    history = ticker.history(start=StartDate,end=EndDate ) 
    listed = list(history["Close"])
    for i in range(1, len(listed)):  # start from index 1 to avoid listed[i-1] = listed[-1]
        change = listed[i] - listed[i - 1]
        subtracted_list.append(change)

    for i in subtracted_list:# take the list and sepeare whether its positive or negaitve
        if i > 0:#seperation
            gains.append(i)
        elif i < 0:
            loss.append(i)

    loss = [abs(l) for l in loss]#Takes the loss value in l and takes the absolute value of it

    AvgSumGain = sum(gains) / 14 #Calculatss the averae of all positive numbers
    AvgSumLoss = sum(loss) / 14# calculates the average of all negative values    
    relativ_strength = AvgSumGain/AvgSumLoss
    Rsi = 100 - (100/(1 + relativ_strength))
    Rsi = round(Rsi,2)
    print(f"RSI: {Rsi}")    

    if Rsi >= 70:
        print("The market is overbought consider selling")
    elif Rsi>=30 and Rsi<=70:
        print("The market is neutral")
    elif Rsi < 30:
        print("The market is oversold  consider buying")    
    return Rsi

def DailyReturn(tckr,Date):
    ticker = yf.Ticker(tckr)
    StartDate1 = datetime.strptime(Date, "%Y-%m-%d")#Takes date and strips into bareform(Used chatgpt for help for the date subtraction part)
    NewDate = StartDate1 - timedelta(days=1)# subtracted by taking the date and subtracting one day(Used Chagpt for the date subtraction help)
    EndDate = StartDate1 + timedelta(days=1)
    history = ticker.history(start = NewDate, end = EndDate)
    listed  = list(history["Close"])
    Daily_Return = ((listed[1] - listed[0]) / listed[0])*100 #formula
    print(f"the daily return is: {Daily_Return}%")

def sma(tckr,StartDate,EndDate):
    ticker = yf.Ticker(tckr)
    history = ticker.history(start=StartDate , end=EndDate)
    ClosedPrices = history["Close"]
    listed = list(ClosedPrices)
    sma = (sum(listed)) / len(listed)
    print(f"SMA: {sma}")
    
def ema(tckr):
    ticker = yf.Ticker(tckr)
    StartDate = input("Start Date (YYYY-MM-DD): ")
    EndDate = input("End date (YYYY-MM-DD): ")
    period = int(input("EMA period (e.g., 10, 20): "))

    history = ticker.history(start=StartDate, end=EndDate)
    closes = list(history["Close"])
    if len(closes) < period:
        print(f"Not enough data to calculate a {period}-day EMA.")
        return
    initial_sma = sum(closes[:period]) / period
    ema_values = [None] * (period - 1)  # first period-1 days have no EMA
    ema_values.append(initial_sma)

    k = 2 / (period + 1)
    for price in closes[period:]:
        prev_ema = ema_values[-1]
        new_ema = (price * k) + (prev_ema * (1 - k))
        ema_values.append(new_ema)
    print(f"Final {period}-day EMA: {round(ema_values[-1], 4)}")
    dates = history.index
    for date, val in zip(dates, ema_values):
        print(f"{date.date()}: {val}")



def roc(tckr):
    ticker = yf.Ticker(tckr)
    StartDate = input("Start date(YYYY-MM-DD): ")
    EndDate = input("End date(YYYY-MM-DD): ")
    history = ticker.history(start= StartDate , end= EndDate)
    listed = list(history["Close"])
    days = len(listed)
    RateOfChange = ((listed[len(listed) - 1] - listed[0]) / listed[0]) * 100
    print(f"rate of change: {RateOfChange}")

#Main Script
features = ["volatility", "RSI", "daily return", "SMA", "EMA", "ROC","monte carlo simulations"]  
print(", ".join(features))
feature_choice = input("please select a feature: ").lower()
if feature_choice == "volatility":
    tckr = input("Ticker: ").upper()
    volatility(tckr)

elif feature_choice == "rsi":
    tckr = input("Ticker: ").upper()
    rsi(tckr)

elif feature_choice == "daily return":
    tckr = input("Ticker: ").upper()
    Date = input("Please input date(YYYY-MM-DD): ")
    DailyReturn(tckr,Date)

elif feature_choice == "sma" or feature_choice == "simple moving average":
    tckr = input("Ticker: ").upper()
    StartDate = input("Start date(YYYY-MM-DD): ")
    EndDate = input("end date(YYYY-MM-DD): ")
    sma(tckr,StartDate,EndDate)

elif feature_choice == "monte carlo simulation":
    #inputing parameters
    initial = float(input("initial value ($): "))
    volatility1 = float(input("volatility (% per year): ")) / 100
    d_return = float(input("expected return (% per year): ")) / 100
    years = int(input("time (years): "))
    sims = int(input("number of simulations: "))
    total_days = years * 365
    ds = input("would you like the simulations plotted (yes/no): ").lower()

    if ds == "yes":
        plot(initial, d_return / 365, sims, volatility1 / math.sqrt(365), math.sqrt(365), total_days)
    else:
        prices = sim(initial, d_return / 365, volatility1 / math.sqrt(365), total_days)
        print(f"Final simulated price: ${prices[-1]:.2f}")

elif feature_choice == "ema" or feature_choice == "exponential moving average":
    tckr = input("Ticker: ").upper()
    ema(tckr)

elif feature_choice == "roc" or feature_choice == "rate of change":
    tckr = input("Ticker: ").upper()
    roc(tckr)
