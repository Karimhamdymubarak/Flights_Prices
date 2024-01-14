import pandas as pd
import streamlit as st
import joblib
import category_encoders
import sklearn
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
geolocator = Nominatim(user_agent="lat,long")
model = joblib.load("Final_Model_G4.pkl")
inputs = joblib.load("Inputs.pkl")

def Prediction(Airline,Source,Destination,Stops,Day_of_Journey_in_numbers, Month_of_Journey, Dep_Hour,Arrival_Hour, Arrival_Period, Dep_Period, Duration_Categorized,Distance_Categorized, Meal):
    test_df = pd.DataFrame(columns=inputs)
    test_df.at[0,'Airline'] = Airline
    test_df.at[0,"Source"] = Source
    test_df.at[0,"Destination"] = Destination
    test_df.at[0,"Month_of_Journey"] = Month_of_Journey
    test_df.at[0,"Stops"] = Stops
    test_df.at[0,"Day_of_Journey_in_numbers"] = Day_of_Journey_in_numbers
    test_df.at[0,"Duration_Categorized"] = Duration_Categorized
    test_df.at[0,"Distance_Categorized"] = Distance_Categorized
    test_df.at[0,"Dep_Hour"] = Dep_Hour
    test_df.at[0,"Arrival_Hour"] = Arrival_Hour
    test_df.at[0,"Dep_Period"] = Dep_Period
    test_df.at[0,"Arrival_Period"] = Arrival_Period
    test_df.at[0,"Meal"] = Meal
    result = model.predict(test_df)
    return result[0]
    
def get_day_period(r):
    if int(r) in range(5,13) : 
        return "Morning"
    elif int(r) in range(13,18):
        return "Afternoon"
    elif int(r) in range(18,23):
        return "Evening"
    else:
        return "Night"   
def get_distance(source , dest):
    loc = geolocator.geocode(source)
    source_lat = loc.raw['lat']
    source_long = loc.raw["lon"]
    source_axis = (source_lat , source_long)
    loc = geolocator.geocode(dest)
    dest_lat = loc.raw['lat']
    dest_long = loc.raw["lon"]
    dest_axis = (dest_lat , dest_long)
    distance = great_circle(source_axis , dest_axis).kilometers
    if distance <= 1000 :
        return 'short Dist'
    elif distance <=2000:
        return 'Medium Dist'
    else:
        return 'Long Dist'
    
    
def main():
    st.title("Flights Price Prediction")
    Airline = st.selectbox("Airline" , ['Air India', 'Jet Airways', 'IndiGo', 'SpiceJet','Multiple carriers', 'GoAir', 'Vistara', 'Air Asia'])
    Source = st.selectbox("Source" , ['Kolkata', 'Delhi', 'Banglore', 'Chennai', 'Mumbai'])
    Destination = st.selectbox("Destination" ,['Banglore', 'Cochin', 'New Delhi', 'Kolkata', 'Delhi', 'Hyderabad'] )
    Month_of_Journey = st.selectbox("Month_of_Journey" , ['May', 'June', 'March', 'April'])
    Stops = st.selectbox("Stops" , [2, 1, 0, 3, 4])
    Day_of_Journey_in_numbers = st.selectbox("Day_of_Journey_in_numbers" ,range(1,32))
    Duration = st.slider("Duration" , min_value=100 , max_value=10000,value=1000,step=20)
    if Duration <= 750 :
        Duration_Categorized = 'short Duration'
    elif Duration <= 1500 :
        Duration_Categorized = 'Medium Duration'
    elif Duration < 10000 :
        Duration_Categorized = 'Long Duration'
    Distance_Categorized = get_distance(Source , Destination)
    Dep_Hour = st.selectbox("Dep_Hour" , range(0,24))
    Arrival_Hour = st.selectbox("Arrival_Hour" , range(0,24))
    Dep_Period = get_day_period(Dep_Hour)
    Arrival_Period = get_day_period(Arrival_Hour)
    Meal = st.selectbox("Meal" , [0,1])
    if st.button("Predict"):
        result = Prediction(Airline,Source,Destination,Stops,Day_of_Journey_in_numbers, Month_of_Journey, Dep_Hour,Arrival_Hour, Arrival_Period, Dep_Period, Duration_Categorized,Distance_Categorized, Meal)
        st.text(result)
main()
