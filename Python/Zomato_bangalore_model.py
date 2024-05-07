import pandas as pd
import numpy as np
import streamlit as st
import requests
from base64 import b64encode

url3 = "https://raw.githubusercontent.com/anishkatoch/Zomato-Recommendation-Model/main/Datasets/feedback.csv"

feedback_file_path = (url3)
feedback_data = pd.DataFrame(columns=["name", "feedback"])  

def save_feedback(name, feedback):
    global feedback_data
    if not isinstance(feedback_data, pd.DataFrame):
        print("Error: feedback_data is not a pandas DataFrame.")
        return
    try:
        feedback_data = feedback_data.append({"name": name, "feedback": feedback}, ignore_index=True)
        feedback_data.to_excel(feedback_file_path, index=False)
        print("Feedback saved successfully.")
    except Exception as e:
        print("An error occurred while saving feedback:", e)


def load_feedback_data():
    global feedback_data
    try:
        feedback_data = pd.read_csv(feedback_file_path)
    except FileNotFoundError:
        print("Feedback file not found. Creating a new DataFrame.")
        feedback_data = pd.DataFrame(columns=["Name", "Feedback"])

# Load existing feedback data if available
load_feedback_data()

url1 = "https://raw.githubusercontent.com/anishkatoch/Zomato-Recommendation-Model/main/Datasets/zomatoCleanData.csv"
zomatoData = pd.read_csv(url1)

url2 = "https://raw.githubusercontent.com/anishkatoch/Zomato-Recommendation-Model/main/Datasets/zomatoNewRestaurant.csv"
zomatoNewRestaurant = pd.read_csv(url2)

# Set dark theme
page_bg_img = '''
    <style>
    body {
        background-color: #1F1F1F;
        color: #FFFFFF;
    }
    </style>
    ''' 
st.markdown(page_bg_img, unsafe_allow_html=True)

def main():
    st.markdown("<h1 style='text-align: center; color: gold; padding: 15px; background-color: grey; font: bold 50px  heavy ; border-radius: 20px;'>ZOMATO MODEL</h1>", unsafe_allow_html=True)
    html_temp = """
    <div style='background-color: #333; padding: 2px; max-width: 400px; margin: 20px auto;'>
    <h1 style='color: red; text-align: center; font-family: "Bradley Hand ITC", cursive; font-weight: bold; border-radius: 20px;'><b>BANGALORE</b></h1>
    </div>
    """

    st.markdown(html_temp, unsafe_allow_html = True)

    # select the cuisine
    selectedCuisine = zomatoData['cuisine'].unique()
    st.markdown("<h2 style='font-size: 24px;margin-bottom: 0px;'><span style='color: red;'><b>Cuisine:</b></h2>", unsafe_allow_html=True)
    Cuisine = st.selectbox("",selectedCuisine) 

    #automatically display the location based on cuisine
    filterZomatoData = zomatoData[zomatoData['cuisine']==Cuisine]
    filterLocation = filterZomatoData['location'].unique()
    st.markdown("<h2 style='font-size: 24px;margin-bottom: 0px;'><span style='color: red;'>Location:</h2>", unsafe_allow_html=True)
    Location = st.selectbox("",filterLocation) 

    if st.button("Predict"):
        avgPrice = round(zomatoData[(zomatoData['cuisine'] == Cuisine) & (zomatoData['location'] == Location)]['price_for_one'].mean())

        bestRestaurant = zomatoData[(zomatoData['cuisine'] == Cuisine) & (zomatoData['location'] == Location)]
        bestMeanRatings = bestRestaurant['ratings'].mean()
        bestRestaurant = bestRestaurant[bestRestaurant['ratings'] >= bestMeanRatings]
        bestMedianReview = bestRestaurant['delivery_review_no'].median()
        bestRestaurant = bestRestaurant[bestRestaurant['delivery_review_no']>=bestMedianReview]
        minPrice = bestRestaurant['price_for_one'].min()
        bestRestaurant = bestRestaurant[bestRestaurant['price_for_one']>=minPrice].head(1)
        bestRestaurantName = bestRestaurant['restaurant_name'].to_string()
        showRestaurantName = bestRestaurantName[1:].strip()

        Timings = bestRestaurant[bestRestaurant['price_for_one']>=minPrice].head(1)['timings']
        Timings = "".join(Timings)
        

        navigateLink = bestRestaurant[bestRestaurant['price_for_one']>=minPrice].head(1)['links']
        surfTo = "".join(navigateLink)
        
        filter_loc = zomatoData[(zomatoData['location'] == Location)]
        avg_rating_loc = round(filter_loc['ratings'].mean(),2)
        pop_rest=filter_loc[filter_loc['ratings'] >=avg_rating_loc]
        pop_rest_name = pop_rest[pop_rest['delivery_review_no'] == pop_rest['delivery_review_no'].max()]['restaurant_name'].unique()
        pop_rest_name= " ".join(pop_rest_name)
        
        cusine_Serve = pop_rest[pop_rest['restaurant_name']==pop_rest_name]['cuisine'].unique()
        cusine_Serves = ", ".join(cusine_Serve)

        cusine_Serve =pop_rest[pop_rest['restaurant_name']==pop_rest_name]['timings'].unique()
        restTiming=", ".join(cusine_Serve)
       
        cusine_Serve =pop_rest[pop_rest['restaurant_name']==pop_rest_name]['links'].unique()
        restLink=", ".join(cusine_Serve)
        
        cus=filter_loc['cuisine'].value_counts().head(4)
        cus=cus.index.tolist()
        favCusine = ", ".join(cus)
        
        st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Standard Rate:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 30px;'>{}</span>".format(avgPrice), unsafe_allow_html=True)
        st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Restaurant Name:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'>{}</span>".format(showRestaurantName), unsafe_allow_html=True)
        st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Duration:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'>{}</span>".format(Timings), unsafe_allow_html=True)
        st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Surf To:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'>{}</span>".format(surfTo), unsafe_allow_html=True)

        st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Local Taste Kitchen:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'>{}</span>".format(pop_rest_name), unsafe_allow_html=True)
        st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Restaurant offers diverse cuisine:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'>{}</span>".format(cusine_Serves), unsafe_allow_html=True)
        st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Spice Hour:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'>{}</span>".format(restTiming), unsafe_allow_html=True)
        st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Navigate to:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'>{}</span>".format(restLink), unsafe_allow_html=True)
        st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Local culinary favorites:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'>{}</span>".format(favCusine), unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: teal;'>NEWLY OPEN RESTAURANT</h1>", unsafe_allow_html=True)

    Location_Name, Restaurant_Name = st.columns(2)

    with Location_Name:
        filterLocation = zomatoNewRestaurant['locations'].unique()
        st.markdown("<h2 style='font-size: 24px;margin-bottom: 0px;'><span style='color: red;'><b>Location:</b></h2>", unsafe_allow_html=True)
        Location = st.selectbox("", filterLocation)

    with Restaurant_Name:
        showRestaurant = zomatoNewRestaurant[zomatoNewRestaurant['locations']==Location]
        showRestaurantName = showRestaurant['restaurant_name'].unique()
        st.markdown("<h2 style='font-size: 24px;margin-bottom: 0px;'><span style='color: red;'><b>Restaurant Name:</b></h2>", unsafe_allow_html=True)
        Restaurant_Name = st.selectbox("", showRestaurantName, key="Restaurant_Name_selectbox")

    if st.button("Confirm"):
        restaurantInfo = showRestaurant[showRestaurant['restaurant_name'] == Restaurant_Name]
        Estimate = restaurantInfo['price_for_one'].to_string().split()[1]

        dishe = showRestaurant[showRestaurant['restaurant_name'] == Restaurant_Name]['cuisins'].unique()
        dishes = ",".join(dishe)

        navigateTo=showRestaurant[showRestaurant['restaurant_name']== Restaurant_Name]['links'].unique()
        navigateTo = "".join(navigateTo)

        st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Estimate Price:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 30px;'>{}</span>".format(Estimate), unsafe_allow_html=True)
        st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Cuisine:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'>{}</span>".format(dishes), unsafe_allow_html=True)
        st.markdown("<span style='color: Olivedrab; font-family: \"Times New Roman\", Times, serif; font-weight: bold; font-size: 32px; margin-right: 10px;'>Navigate To:</span><span style='color: purple; font-family: \"Georgia\", serif; font-weight: bold; font-size: 27px;'>{}</span>".format(navigateTo), unsafe_allow_html=True)

    load_feedback_data()
    st.markdown("<h1 style='text-align: center; color: DarkGoldenrod;'>FEEDBACK</h1>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='font-size: 24px;margin-bottom: 0px;'><span style='color: red;'><b>Name</b></h2>", unsafe_allow_html=True)
    name = st.text_input("")
    st.markdown("<h2 style='font-size: 24px;margin-bottom: 0px;'><span style='color: red;'>Feedback</h2>", unsafe_allow_html=True)
    feedback = st.text_area("")
    if st.button("Submit"):
        save_feedback(name, feedback)
        st.markdown("<span style='color: green; font-weight: bold; font-size: 35px;'>Feedback submitted successfully!</span>", unsafe_allow_html=True)
        

if __name__ == '__main__':
    main()