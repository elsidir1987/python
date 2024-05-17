import pandas as pd



#with open('Thessaloniki,Greece.json') as f:
  # data=json.load(f)
df=pd.read_csv("Thessaloniki,Greece.csv",index_col=0)

df.to_json("mydata.json",orient='columns')
#use normdalize to convert the json
#df=pd.json_normalize(data,['days'],['hours',['datetime','temp','humidity','pressure']])
    
#df=pd.json_normalize(data['days'],record_path=['hours'],meta=['hours',['datetime','temp','pressure','humidity']],errors="raise")

#rename the columns
#df.columns=['Hours','Date','Temperature','Humidity','Pressure']

print(df)
