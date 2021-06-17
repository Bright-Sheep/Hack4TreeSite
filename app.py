import streamlit as st
import requests

from PIL import Image

# Pour vérifier si les coordonnées sont bien dans marseille

from Tool.util import coordinates_in_city


from geopy.geocoders import Nominatim

import numpy as np

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


#st.sidebar.markdown('''Pour faire notre prédiction, nous proposons deux méthodes.
#''')

#direction = st.sidebar.radio('Selectionner une méthode :', ('Telecharger une image','Entrer une adresse'))

#st.write(direction)

# if direction == 'Telecharger une image':

#     st.set_option('deprecation.showfileUploaderEncoding', False)

#     uploaded_file = st.file_uploader("Choose a png file", type="png")

#     if uploaded_file is not None:
#         image = Image.open(uploaded_file)
#         st.image(image, caption='map', use_column_width=False)
        
#         url = 'http://localhost:8000/predict_image_given'
    
#     st.markdown(type(uploaded_file))
    
#     image = Image.open(uploaded_file)
    
#     st.markdown(type(image))
    
#     img = np.array(image).tolist()
    
#     st.markdown(type(img))
    
#     params = dict(
#         image = img
#     )
            
#     response = requests.post(
#         url,
#         params=params
#     )  
    
#     if response.status_code == 200:
#         st.image(np.array(response.json()["image"]))
#     else:
#         st.markdown("L'image n'a pas pu être appelé ")
            
# else :

st.markdown('''Ce site propose de récupérer des images de Marseille à partir d'une adresse et de localiser les arbres présents sur l'image.''')
# st.markdown('''Pour commencer, choisissez simplement une adresse et un service pour obtenir la carte, puis laissez nous faire le reste.''')
st.markdown('''Pour commencer, choisissez simplement une adresse la carte, puis laissez nous faire le reste 🙂''')

user_location = st.text_input('Veuillez entrer une adresse :','Marseille')

# site = st.radio('Choisissez un service pour la carte :', ('bing','google_maps','mapbox'))

locator = Nominatim(user_agent='google')

location = locator.geocode(user_location)

if  location != None:
    st.write('Latitude = {}, Longitude = {}'.format(location.latitude, location.longitude))    

    if coordinates_in_city(location.latitude,location.longitude):
        st.success('Les coordonnées sont dans Marseille.')
    else :
        st.error("⚠️ Vous n'êtes pas dans Marseille.")
else :
    st.error('''Je n'ai pas compris votre adresse.''')
        
        
#url = 'http://localhost:8000/predict_image'
url = 'https://hacknature-qhptkplhyq-ew.a.run.app/predict_image'

if  location != None:
            
    params = dict(
        latitude = location.latitude ,
        longitude = location.longitude,
        # service = site
    )
    if st.button("Charger l'image"):
        # print is visible in server output, not in the page
        
        response = requests.get(
            url,
            params=params
        )  

        if response.status_code == 200:
                col1, col2, col3 = st.beta_columns([6,1,6])
                
                with col1:
                    st.image(np.array(response.json()["original_image"]),caption = "Image d'origine")

                with col2:
                    st.write("")

                with col3:
                    st.image(np.array(response.json()["image"]),caption='Arbres repérés')
                
                
        else:
            st.markdown("La carte n'a pas pu être appelé ")

