#Import the Libraries

import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
import numpy as np
import pickle
import datetime
import matplotlib.pyplot as plt
from sklearn import linear_model

method="get"
apikey="JMFZKWVARCGA8SQ439P4F2C5X"
url="https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Thessaloniki%2CGreece/2023-05-01/2023-05-14?unitGroup=metric&include=hours&key=GRTDJUY3ANUKFNS6TR6N7G9ZB&contentType=json"
auth=HTTPBasicAuth("elenisidiraki@gmail.com","%Z?qc?*5Ney2jA_")
rsp=requests.request(method,url,headers=None,auth=auth)

#print(rsp.text)
#print(rsp.encoding)

#store the api response in a variable

response=rsp.json()
#print(type(response))
#print(response.keys())

alldays={'datetime':[],
         'Pressure':[],
         'Humidity':[],
         'Temperature':[]}

days=response['days']

for i in range(len(days)):
    day=days[i]

    hours=day['hours']
    for j in range(len(hours)):
        aday=hours[j]

        #βρίσκουμε την ημερομηνία από το unix timestamp που υπάρχει
#στα δεδομένα datetimeEpoch
        alldays['datetime'].append(datetime.datetime.fromtimestamp(aday['datetimeEpoch']).strftime('%Y-%m-%d %H:%M:%S'))
        alldays['Pressure'].append(aday['pressure'])
        alldays['Humidity'].append(aday['humidity'])
        alldays['Temperature'].append(aday['temp'])

#Κατασκευή Dataframe από το λεξικό
df = pd.DataFrame.from_dict(alldays)
#Εύρεση της ώρας από την πλήρη ημερομηνία
df['Hour'] = pd.to_datetime(df['datetime']).dt.hour

#Αποθήκευση σε csv των στηλών που διατηρήσαμε
df.to_csv("Thessaloniki,Greece.csv", index = False)

df = pd.read_csv("Thessaloniki,Greece.csv")
#print(df)

#grafimata
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(20, 20))
#diagramma diakumansis piesis
ax1.plot(df['datetime'],df['Pressure'],color='red')
ax1.set_title("I am happy to done it!")
ax1.set_xlabel("Date")
ax1.set_ylabel("Pressure[inHg]")
ax1.set_xticks(df['datetime'][::20])
ax1.set_xticklabels(df['datetime'][::20],rotation=25)
#diagramma diakumansis thermokrasias
ax2.plot(df['datetime'],df['Temperature'],color='green')
ax2.set_xlabel("Date")
ax2.set_ylabel("Temperature (°C)")
ax2.set_xticks(df['datetime'][::20])
ax2.set_xticklabels(df['datetime'][::20],rotation=25)
#diagramma diakumansis ygrasias
ax3.plot(df['datetime'],df['Humidity'],color='blue')
ax3.set_xlabel("Date")
ax3.set_ylabel("Humidity")
ax3.set_xticks(df['datetime'][::20])
ax3.set_xticklabels(df['datetime'][::20],rotation=25)
                               
plt.show()

# Ορίζουμε τις ανεξάρτητες μεταβλητές που θα χρησιμοποιήσουμε σαν λίστα
feat_cols = ['Hour', 'Humidity', 'Pressure']
# Κατασκευή του διαγράμματος που συσχετίζει τις ανεξάρτητες μεταβλητές με τη θερμοκρασία
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))
ax1.scatter(df[feat_cols[0]], df['Temperature'], color='red', alpha=0.2)
ax2.scatter(df[feat_cols[1]], df['Temperature'], color='orange', alpha=0.2)
ax3.scatter(df[feat_cols[2]], df['Temperature'], color='green', alpha=0.2)
ax1.set_xlabel(feat_cols[0])
ax2.set_xlabel(feat_cols[1])
ax3.set_xlabel(feat_cols[2])
plt.tight_layout()
plt.show()

# Μετασχηματίζουμε τα δεδομένα της ανεξάρτητης μεταβλητής σε πίνακα 2 διαστάσεων
h_array = df[feat_cols].values
w_array = df['Temperature'].values

# Δημιουργία μοντέλου πολλαπλής γραμμικής παλινδρόμησης
model_reg = linear_model.LinearRegression().fit(h_array, w_array)

# Εκτύπωση συντελεστών
print("---------- Εκτύπωση συντελεστών ----------")
print("Παράμετροι βν: ", list(zip(model_reg.coef_, feat_cols)))
print("Παράμετρος β0: " + str(model_reg.intercept_))
print("Συντελεστής προσδιορισμού: " + str(model_reg.score(h_array, w_array)))
print("")

# Αποθήκευση του εκπαιδευμένου μοντέλου στο δίσκο
with open("model.pickle", "wb") as f:
    pickle.dump(model_reg, f)

start_menu()
#############
# Συναρτήσεις
#############
# Συνάρτηση για την είσοδο του χρήστη και τον έλεγχο αυτής
def user_input():
    # Ανακτούμε την τρέχουσα ώρα
    hour = pd.Timestamp.now().hour
    while True:
        try:
            hum = float(input('Πληκτρολογήστε την υγρασία: '))
            press = float(input('Πληκτρολογήστε την πίεση: '))
            if hum > 0 and press > 0:
                break
            else:
                print("Παρακαλώ δώστε θετική τιμή")
        except ValueError:
            print("Λάθος τιμή.")
    return hour, hum, press


# Συνάρτηση για την Ανάκτηση του εκπαιδευμένου μοντέλου
def get_model():
    # Ανάκτηση του εκπαιδευμένου μοντέλου από το δίσκο
    print("Ανάκτηση προγνωστικού μοντέλου...\n")
    with open("model.pickle", "rb") as f:
        model_load = pickle.load(f)

    return model_load


# Συνάρτηση εμφάνισης μενού
def start_menu():
    print("========== Πρόγνωση της θερμοκρασίας την επόμενη ώρα ==========")
    while True:
        print('Επιλέξτε λειτουργία πληκτρολογώντας το γράμμα που της αντιστοιχεί:\n')
        print('Α - Πρόβλεψη της θερμοκρασίας την επόμενη ώρα \n')
        print('B - Τερματισμός προγράμματος\n')

        func = input('Δώστε την επιλογή σας: \n')

        if func == 'A':
            # Ανακτούμε την ώρα, υγρασία και την πίεση ως είσοδο του χρήστη
            hour, humidity, pressure = user_input()

            # Δεδομένα εισόδου στο μοντέλο
            input_data = [hour, humidity, pressure]

            # Μετασχηματίζουμε τα δεδομένα σε πίνακα 2 διαστάσεων
            final_input = np.array([input_data]).reshape((1, -1))

            # Πρόγνωση
            print("Πρόγνωση...\n")
            model_load = get_model()
            prediction_1 = model_load.predict(final_input)

            # Η έξοδος είναι πίνακας με 1 στοιχείο
            print("Την επόμενη ώρα η θερμοκρασία θα είναι: " + str(prediction_1[0]))
        elif func == 'B':
            print('Τερματισμός προγράμματος...\n')
            break
        else:
            print("Η επιλογή που δώσατε είναι λανθασμένη.\n")


########################################
# Κλήση συνάρτησης μενού επιλογών χρήστη
########################################


    
