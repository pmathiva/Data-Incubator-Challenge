import pandas as pd
import numpy as np
from geopy.distance import great_circle
import decimal
decimal.getcontext().prec = 10
D = decimal.Decimal

def DataCheck ():
    res = []
    temp = ()
    for data in frames:
        temp = data.shape[0],data.shape[1],len(data)-data.count()
        res.append(temp)
    return res
    
d1 = pd.read_csv("C:\\Users\\priya.cse2009\\Documents\\Python Scripts\\dataInc\\201501-citibike-tripdata.csv")
d2 = pd.read_csv("C:\\Users\\priya.cse2009\\Documents\\Python Scripts\\dataInc\\201502-citibike-tripdata.csv")
d3 = pd.read_csv("C:\\Users\\priya.cse2009\\Documents\\Python Scripts\\dataInc\\201503-citibike-tripdata.csv")
d4 = pd.read_csv("C:\\Users\\priya.cse2009\\Documents\\Python Scripts\\dataInc\\201504-citibike-tripdata.csv")
d5 = pd.read_csv("C:\\Users\\priya.cse2009\\Documents\\Python Scripts\\dataInc\\201505-citibike-tripdata.csv")
d6 = pd.read_csv("C:\\Users\\priya.cse2009\\Documents\\Python Scripts\\dataInc\\201506-citibike-tripdata.csv")
d7 = pd.read_csv("C:\\Users\\priya.cse2009\\Documents\\Python Scripts\\dataInc\\201507-citibike-tripdata.csv")
d8 = pd.read_csv("C:\\Users\\priya.cse2009\\Documents\\Python Scripts\\dataInc\\201508-citibike-tripdata.csv")
d9 = pd.read_csv("C:\\Users\\priya.cse2009\\Documents\\Python Scripts\\dataInc\\201509-citibike-tripdata.csv")
d10 = pd.read_csv("C:\\Users\\priya.cse2009\\Documents\\Python Scripts\\dataInc\\201510-citibike-tripdata.csv")
d11 = pd.read_csv("C:\\Users\\priya.cse2009\\Documents\\Python Scripts\\dataInc\\201511-citibike-tripdata.csv")
d12 = pd.read_csv("C:\\Users\\priya.cse2009\\Documents\\Python Scripts\\dataInc\\201512-citibike-tripdata.csv")

frames = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12]
print DataCheck()
data = pd.concat(frames)
data["start"] = zip(data["start station latitude"], data["start station longitude"])
data["end"] = zip(data["end station latitude"], data["end station longitude"])
data["dist"] = data.apply(lambda x: great_circle(x[15], x[16]), axis = 1)
data.to_csv ( "C:\\Users\\priya.cse2009\\Documents\\Python Scripts\\dataInc\\data.csv",index =False)


data = pd.read_csv("C:\\Users\\priya.cse2009\\Documents\\Python Scripts\\dataInc\\data.csv")
totlen = len(data)
print data.shape
print data.dtypes


tripDuration = data["tripduration"]
print "Median trip duration: ",tripDuration.median() 
frac1 = len(data[ data["start station id"] == data["end station id"] ]) 
print "Fraction of rides starting and ending at the same station: ",D(frac1)/D(totlen)

def myfunc(df):
    stncnt = set()
    stncnt.update( df['start station id'].unique())
    stncnt.update( df['end station id'].unique())
    return len(stncnt)
    
cnt = data.groupby('bikeid').apply(myfunc)
print "Stdev of number of stations visited by a bike: ",np.std(cnt)
"""
tmp = data[ data["start station id"] != data["end station id"] ]
dist = data.apply(lambda x: great_circle(x[15], x[16]), axis = 1)
#print "The average dist.in kms: ",np.mean(dist)
print len(tmp)
print len(dist)
#print frac1
print totlen
print type(dist)

"""

def TimesMoved(x):
    x= x.sort_values(by = "starttime").reset_index(drop=True)
    start = x["start station id"]
    del start[0]
    lastitem = len(x)-1
    end = x["end station id"]
    del end[lastitem]
    table = [start,end]
    cols = ["start","end"]
    df = pd.DataFrame(table)
    df = df.transpose()
    df.columns = cols
    moved = df[df[ "start"] != df["end"] ]
    noMoved = len(moved)
    return noMoved

timesMoved = data.groupby('bikeid').apply(TimesMoved)
print "The average times a bike is moved is: ",np.mean(timesMoved)


#Average trip duration every month
def MeanTripDuration(x):
     return x['tripduration'].mean()

data["starttime"] = pd.to_datetime(data["starttime"], coerce=True)
meanTripDuration= data.groupby(data["starttime"].dt.month).apply(MeanTripDuration)
diffMeanTripDuration = max(meanTripDuration) - min(meanTripDuration)
print "Difference, in seconds, between the longest and shortest average durations :",diffMeanTripDuration

groups = data.groupby("usertype")		#Group data based on usertype
cnt = 0
for name, group in groups:
    if name == "Customer": 
        cust =  group["tripduration"]>=1800		#Filter rides which exceeds time limit - 30mins
        cnt += len(group.loc[cust])
    if name == "Subscriber": 
        sub = group["tripduration"]>=2700			#Filter rides which exceeds time limit - 45mins
        cnt += len(group.loc[sub])
        
print "The fraction of rides exceeding their time limit : " , D(cnt)/D(totlen)   

def GetCount(x):
    return len(x)
        #data["starttime"] = pd.to_datetime(data["starttime"], errors='coerce')
hourGrp = data.groupby(data["starttime"].dt.hour)

hourlySysUsage = []
stnUsage = {}

for name,gr in hourGrp:
    sysUsageFrac = D(len(gr))/D(totlen)
    hourlySysUsage .append(sysUsageFrac)
    stnGroups =  gr.groupby("start station id")
    for n,g in stnGroups:
          hrStnKey = "H:"+ str(name)+ " StationID:"+str(n)
          stnUsageFrac = D(len(g))/D(len(gr))
          ratio = D(stnUsageFrac) / D(sysUsageFrac)
          stnUsage[hrStnKey] = ratio
          
stnHrPair = max(stnUsage, key=stnUsage.get) 
print   stnHrPair,stnUsage[stnHrPair]


    
        