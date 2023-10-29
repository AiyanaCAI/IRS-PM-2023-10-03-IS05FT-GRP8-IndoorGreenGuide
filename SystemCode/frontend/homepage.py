from PIL import Image
import webbrowser
import streamlit as st
import pandas as pd
import numpy as np
import sys
from streamlit.components.v1 import html
# TODO: Replace with your project address!
sys.path.append('/templates')

from backend.recommender import get_recommendation 
new_url = "file:///.../templates/page1.html" #TODO: Replace with your project address!
image = Image.open("./plant7-2.jpg")
st.image(image)


## Par1:head ##
st.title("P L :evergreen_tree: N T S ")
st.markdown('<h1 style="font-size: 40px"> And More For YOU</h1>', unsafe_allow_html=True)

# st.write("Bring Nature and Comfort to your place")
st.write(" ")
st.markdown('<span style="font-family: Georgia; font-size: 20px; font-style: italic;">Bring nature and comfort to your place :leaves:</span>', unsafe_allow_html=True)
st.markdown('<span style="font-size: 20px">:sparkles: Answer some questions to get the most suitable indoor plants for you!  &darr;&darr;&darr;</span>', unsafe_allow_html=True)
st.write(" ")

# create back button
if st.button("<<< Back"):
    
    webbrowser.open(new_url)

## Part2: multiple choice questions ##
# light_preference = st.radio("What is your preferred light condition?", ["Direct Sunlight", "Indirect Sunlight", "Shady"])
st.markdown('<h3 style="font-size: 24px;">What is your preferred light condition?</h3>', unsafe_allow_html=True)
light_preference = st.radio("Preferred light condition", ["Direct Sunlight", "Indirect Sunlight", "Shade"])

st.markdown('<h3 style="font-size: 24px;">What height of plants do you prefer?</h3>', unsafe_allow_html=True)
height_preference = st.radio("Preferred plant height", ["Short", "Medium", "Tall"])

st.markdown('<h3 style="font-size: 24px;">How much time can you devote to plant care?</h3>', unsafe_allow_html=True)
care_preference = st.radio("Plant care time", ["Low", "Medium", "High"])

st.markdown('<h3 style="font-size: 24px;">What plant species do you prefer?</h3>', unsafe_allow_html=True)
species_preference = st.selectbox("Plant species", ["None", "Cactus", "Climber", "Creeper", "Fern", "Herbs", 
                                                                        "Orchid", "Shrub", "Succulent", "Tree", "Tropical"])

st.markdown('<h3 style="font-size: 24px;">Do you have other preferences?</h3>', unsafe_allow_html=True)
other_preference = st.selectbox("Other preferences", ["None", "Flowers", "Family", "No soil", "Decorative"])

# set button response
if light_preference == "Direct Sunlight":
    light_pref = "direct"
elif light_preference == "Indirect Sunlight":
    light_pref = "indirect"
else:
    light_pref = "shade"

if height_preference == "Short":
    height_pref = "Small"
elif height_preference == "Medium":
    height_pref = "Medium"
else:
    height_pref = "Large"

if care_preference == "Low":
    care_pref = "Easy to care"
else:
    care_pref = "Need careful care"


# Add a button to trigger back-end 
if st.button("Get Recommendations"):
    st.write("Your preferences have been submitted.")
    st.write("Searching suitable plants...")
    
    user_answers = [light_pref, height_pref, care_pref, species_preference, other_preference]
    print(user_answers)
    recommendations = get_recommendations(user_answers)
    
    # show recommendations
    st.write("Recommendations:")

    # Streamlit columns component
    columns = st.columns(3)
    i = 0 
    for recommendation in recommendations:
        # get plant information
        name = recommendation["Name:"]
        picture_url = recommendation["Picture:"]
        url = recommendation["url:"]
        description = recommendation["Description:"]        
        # Displays plant information in each column
        with columns[ i % 3 ]:
            st.image(picture_url, use_column_width=True, caption=name)
            st.markdown(f"[Link]({url})")
            st.write(description)
        i += 1


