import streamlit as st
import requests

from PIL import Image

# Pour vérifier si les coordonnées sont bien dans marseille

from Tool.util import coordinates_in_city


from geopy.geocoders import Nominatim

import numpy as np

import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Projet Hack4Nature", # => Projet_Hack4Nature - Streamlit
    page_icon="🌳",
    layout="wide", # wide
    initial_sidebar_state="auto") # collapsed
_, title1, title2 = st.beta_columns([1.75,0.5,5])
image = Image.open('images/wagon.png')
with title1:
    st.image(image, caption="Le Wagon", width=64, use_column_width=None)
with title2:
    st.title("Hack4Nature - Batch #610 Marseille")


st.sidebar.markdown('''Pour faire notre prédiction, nous proposons deux méthodes.
''')

direction = st.sidebar.radio('Selectionner une méthode :', ('Telecharger une image','Entrer une adresse'))

st.write(direction)

if direction == 'Telecharger une image':

    st.set_option('deprecation.showfileUploaderEncoding', False)

    uploaded_file = st.file_uploader("Choose a png file", type="png")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='map', use_column_width=False)
        
        url = 'http://localhost:8000/predict_image_given'
    
    
        
    params = dict(
        image = image
    )
            
    response = requests.get(
        url,
        params=params
    )  
    
    if response.status_code == 200:
        st.image(np.array(response.json()["image"]))
    else:
        st.markdown("La carte n'a pas pu être appelé ")
            
else :

    site = st.radio('Choisissez un site pour la carte', ('bing','google_maps','mapbox'))

    locator = Nominatim(user_agent='google')
    
    user_location = st.text_input('Veuillez entrer une adresse','Marseille')
    
    location = locator.geocode(user_location)
    
    if  location != None:
        st.write('Latitude = {}, Longitude = {}'.format(location.latitude, location.longitude))    

        if coordinates_in_city(location.latitude,location.longitude):
            st.success('Les coordonnées sont dans Marseille.')
        else :
            st.error("⚠️ Vous n'êtes pas dans Marseille.")
    else :
        st.error('''Je n'ai pas compris votre adresse. Veuillez ne pas rouler votre tête contre le clavier''')
        
        
    url = 'http://localhost:8000/predict_image'
            
    params = dict(
        latitude = location.latitude ,
        longitude = location.longitude
    )
            
    response = requests.get(
        url,
        params=params
    )  
    
    if response.status_code == 200:
        st.image(np.array(response.json()["image"]))
    else:
        st.markdown("La carte n'a pas pu être appelé ")

