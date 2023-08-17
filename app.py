import openai
import urllib.request
from PIL import Image
import streamlit as st

openai.api_key = "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"

st.set_page_config(page_title="Classifier Playground", page_icon="", layout="wide")



def generate_image(image_description):

  img_response = openai.Image.create(
    prompt = image_description,
    n=2,
    size="512x512")
  

  img_url = img_response['data'][0]['url']

  urllib.request.urlretrieve(img_url, 'img.png')

  img = Image.open("img.png")
  
  return img



# page title
st.title('DALL.E - Image Generation - OpenAI')

# text input box for image recognition
img_description = st.text_input('Image Desription')

if st.button('Generate Image'):
    
    generated_img = generate_image(img_description)
    st.image(generated_img)
