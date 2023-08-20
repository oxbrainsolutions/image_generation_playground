import streamlit as st
import openai
import cv2
from PIL import Image
import numpy as np

def generate_images(image_description, n_variations):

    images = []

    try:
        img_response = openai.Image.create(
        prompt = image_description,
        n=n_variations,
        size="256x256")
    except openai.error.Timeout as e:
        #Handle timeout error, e.g. retry or log
        print(f"OpenAI API request timed out: {e}")
        st.session_state.error_indicator = True
        error_field.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.APIError as e:
        #Handle API error, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        st.session_state.error_indicator = True
        error_field.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.APIConnectionError as e:
        #Handle connection error, e.g. check network or log
        print(f"OpenAI API request failed to connect: {e}")
        st.session_state.error_indicator = True
        error_field.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.InvalidRequestError as e:
        #Handle invalid request error, e.g. validate parameters or log
        print(f"OpenAI API request was invalid: {e}")
        st.session_state.error_indicator = True
        error_field.error("Error: Your request was rejected by the safety system. Please amend your input and try again.")
        spinner.empty()
        return None
    except openai.error.AuthenticationError as e:
        #Handle authentication error, e.g. check credentials or log
        print(f"OpenAI API request was not authorized: {e}")
        st.session_state.error_indicator = True
        error_field.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.PermissionError as e:
        #Handle permission error, e.g. check scope or log
        print(f"OpenAI API request was not permitted: {e}")
        st.session_state.error_indicator = True
        error_field.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.RateLimitError as e:
        #Handle rate limit error, e.g. wait or log
        print(f"OpenAI API request exceeded rate limit: {e}")
        st.session_state.error_indicator = True
        error_field.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None

    if st.session_state.error_indicator == False:
        for idx, data in enumerate(img_response['data']):
            img_url = data['url']
            img_filename = f"img_{idx}.png"  # Use unique filenames
            urllib.request.urlretrieve(img_url, img_filename)
            img = Image.open(img_filename)
            images.append(img)
    
        return images


def display_images(images):
    num_images = len(images)
    images_border = []
    for idx, img in enumerate(images):
        img_array = np.array(img.convert("RGB"))
        cv2.rectangle(img_array, (0, 0), (img_array.shape[1], img_array.shape[0]), (250, 250, 250, 0), 3)
        images_border.append(img_array)
        
    if num_images == 1:
      col1, col2, col3 = st.columns([2, 2, 2])
      with col2:
        text = '<p class="information_text" style="margin-top: 2em; margin-bottom: 0.5em; text-align: center;"><span style="font-family:sans-serif; color:#FCBC24; font-size: 1em; ">Generated Image</span></p>'
        st.markdown(information_media_query + text, unsafe_allow_html=True)
        st.image(images_border[0], use_column_width=True)
    elif num_images == 2:
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        with col2:
            text = '<p class="information_text" style="margin-top: 2em; margin-bottom: 0.5em; text-align: center;"><span style="font-family:sans-serif; color:#FCBC24; font-size: 1em; ">Generated Image 1</span></p>'
            st.markdown(information_media_query + text, unsafe_allow_html=True)
            st.image(images_border[0], use_column_width=True)
        with col3:
            text = '<p class="information_text" style="margin-top: 2em; margin-bottom: 0.5em; text-align: center;"><span style="font-family:sans-serif; color:#FCBC24; font-size: 1em; ">Generated Image 2</span></p>'
            st.markdown(information_media_query + text, unsafe_allow_html=True)
            st.image(images_border[1], use_column_width=True)
    elif num_images == 3:
        col1, col2, col3, col4, col5 = st.columns([1, 1.333, 1.333, 1.333, 1])
        with col2:
            text = '<p class="information_text" style="margin-top: 2em; margin-bottom: 0.5em; text-align: center;"><span style="font-family:sans-serif; color:#FCBC24; font-size: 1em; ">Generated Image 1</span></p>'
            st.markdown(information_media_query + text, unsafe_allow_html=True)
            st.image(images_border[0], use_column_width=True)
        with col3:
            text = '<p class="information_text" style="margin-top: 2em; margin-bottom: 0.5em; text-align: center;"><span style="font-family:sans-serif; color:#FCBC24; font-size: 1em; ">Generated Image 2</span></p>'
            st.markdown(information_media_query + text, unsafe_allow_html=True)
            st.image(images_border[1], use_column_width=True)
        with col4:
            text = '<p class="information_text" style="margin-top: 2em; margin-bottom: 0.5em; text-align: center;"><span style="font-family:sans-serif; color:#FCBC24; font-size: 1em; ">Generated Image 3</span></p>'
            st.markdown(information_media_query + text, unsafe_allow_html=True)
            st.image(images_border[2], use_column_width=True)
    elif num_images == 4:
        col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
        with col2:
            text = '<p class="information_text" style="margin-top: 2em; margin-bottom: 0.5em; text-align: center;"><span style="font-family:sans-serif; color:#FCBC24; font-size: 1em; ">Generated Image 1</span></p>'
            st.markdown(information_media_query + text, unsafe_allow_html=True)
            st.image(images_border[0], use_column_width=True)
        with col3:
            text = '<p class="information_text" style="margin-top: 2em; margin-bottom: 0.5em; text-align: center;"><span style="font-family:sans-serif; color:#FCBC24; font-size: 1em; ">Generated Image 2</span></p>'
            st.markdown(information_media_query + text, unsafe_allow_html=True)
            st.image(images_border[1], use_column_width=True)
        with col4:
            text = '<p class="information_text" style="margin-top: 2em; margin-bottom: 0.5em; text-align: center;"><span style="font-family:sans-serif; color:#FCBC24; font-size: 1em; ">Generated Image 3</span></p>'
            st.markdown(information_media_query + text, unsafe_allow_html=True)
            st.image(images_border[2], use_column_width=True)
        with col5:
            text = '<p class="information_text" style="margin-top: 2em; margin-bottom: 0.5em; text-align: center;"><span style="font-family:sans-serif; color:#FCBC24; font-size: 1em; ">Generated Image 4</span></p>'
            st.markdown(information_media_query + text, unsafe_allow_html=True)
            st.image(images_border[3], use_column_width=True)
