import streamlit as st
import openai
import cv2
import urllib.request
from PIL import Image
import numpy as np
import io
import zipfile

marker_spinner_css = """
<style>
    #spinner-container-marker {
        display: flex;
        align-items: center;
        justify-content: center;
        position: fixed;
        top: 0%;
        left: 0%;
        transform: translate(54%, 0%);
        width: 100%;
        height: 100%;
        z-index: 9999;
    }

    .marker0 {
        position: absolute;
        left: 0;
        width: 1.5em;
        height: 0.375em;
        background: rgba(0, 0, 0, 0);
        animation: animateBlink 2s linear infinite;
        animation-delay: calc(2s * 0 / 12);
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 0 / 12)) translate(calc(2em * (1 - cos(2 * 3.14159 * 0 / 12))), calc(2em * sin(2 * 3.14159 * 0 / 12)));        
    }
    
    .marker1 {
        position: absolute;
        left: 0;
        width: 1.5em;
        height: 0.375em;
        background: rgba(0, 0, 0, 0);
        animation: animateBlink 2s linear infinite;
        animation-delay: calc(2s * 1 / 12);
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 1 / 12)) translate(calc(2em * (1 - cos(2 * 3.14159 * 1 / 12))), calc(2em * sin(2 * 3.14159 * 1 / 12)));
    }
    
    .marker2 {
        position: absolute;
        left: 0;
        width: 1.5em;
        height: 0.375em;
        background: rgba(0, 0, 0, 0);
        animation: animateBlink 2s linear infinite;
        animation-delay: calc(2s * 2 / 12);
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 2 / 12)) translate(calc(2em * (1 - cos(2 * 3.14159 * 2 / 12))), calc(2em * sin(2 * 3.14159 * 2 / 12)));
    }
    
    .marker3 {
        position: absolute;
        left: 0;
        width: 1.5em;
        height: 0.375em;
        background: rgba(0, 0, 0, 0);
        animation: animateBlink 2s linear infinite;
        animation-delay: calc(2s * 3 / 12);
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 3 / 12)) translate(calc(2em * (1 - cos(2 * 3.14159 * 3 / 12))), calc(2em * sin(2 * 3.14159 * 3 / 12)));
    }
    
    .marker4 {
        position: absolute;
        left: 0;
        width: 1.5em;
        height: 0.375em;
        background: rgba(0, 0, 0, 0);
        animation: animateBlink 2s linear infinite;
        animation-delay: calc(2s * 4 / 12);
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 4 / 12)) translate(calc(2em * (1 - cos(2 * 3.14159 * 4 / 12))), calc(2em * sin(2 * 3.14159 * 4 / 12)));
    }
    
    .marker5 {
        position: absolute;
        left: 0;
        width: 1.5em;
        height: 0.375em;
        background: rgba(0, 0, 0, 0);
        animation: animateBlink 2s linear infinite;
        animation-delay: calc(2s * 5 / 12);
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 5 / 12)) translate(calc(2em * (1 - cos(2 * 3.14159 * 5 / 12))), calc(2em * sin(2 * 3.14159 * 5 / 12)));
    }
    
    .marker6 {
        position: absolute;
        left: 0;
        width: 1.5em;
        height: 0.375em;
        background: rgba(0, 0, 0, 0);
        animation: animateBlink 2s linear infinite;
        animation-delay: calc(2s * 6 / 12);
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 6 / 12)) translate(calc(2em * (1 - cos(2 * 3.14159 * 6 / 12))), calc(2em * sin(2 * 3.14159 * 6 / 12)));
    }
    
    .marker7 {
        position: absolute;
        left: 0;
        width: 1.5em;
        height: 0.375em;
        background: rgba(0, 0, 0, 0);
        animation: animateBlink 2s linear infinite;
        animation-delay: calc(2s * 7 / 12);
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 7 / 12)) translate(calc(2em * (1 - cos(2 * 3.14159 * 7 / 12))), calc(2em * sin(2 * 3.14159 * 7 / 12)));
    }
    
    .marker8 {
        position: absolute;
        left: 0;
        width: 1.5em;
        height: 0.375em;
        background: rgba(0, 0, 0, 0);
        animation: animateBlink 2s linear infinite;
        animation-delay: calc(2s * 8 / 12);
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 8 / 12)) translate(calc(2em * (1 - cos(2 * 3.14159 * 8 / 12))), calc(2em * sin(2 * 3.14159 * 8 / 12)));
    }
    
    .marker9 {
        position: absolute;
        left: 0;
        width: 1.5em;
        height: 0.375em;
        background: rgba(0, 0, 0, 0);
        animation: animateBlink 2s linear infinite;
        animation-delay: calc(2s * 9 / 12);
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 9 / 12)) translate(calc(2em * (1 - cos(2 * 3.14159 * 9 / 12))), calc(2em * sin(2 * 3.14159 * 9 / 12)));
    }
    
    .marker10 {
        position: absolute;
        left: 0;
        width: 1.5em;
        height: 0.375em;
        background: rgba(0, 0, 0, 0);
        animation: animateBlink 2s linear infinite;
        animation-delay: calc(2s * 10 / 12);
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 10 / 12)) translate(calc(2em * (1 - cos(2 * 3.14159 * 10 / 12))), calc(2em * sin(2 * 3.14159 * 10 / 12)));
    }
    
    .marker11 {
        position: absolute;
        left: 0;
        width: 1.5em;
        height: 0.375em;
        background: rgba(0, 0, 0, 0);
        animation: animateBlink 2s linear infinite;
        animation-delay: calc(2s * 11 / 12);
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 11 / 12)) translate(calc(2em * (1 - cos(2 * 3.14159 * 11 / 12))), calc(2em * sin(2 * 3.14159 * 11 / 12)));
    }
    
    @keyframes animateBlink {
    0% {
        background: #FCBC24;
    }
    75% {
        background: rgba(0, 0, 0, 0);
    }   
}
@media (max-width: 1024px) {
    #spinner-container-marker {
        transform: translate(57.4%, 0%);
    }
    .marker0 {
        width: 5em;
        height: 1em;
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 0 / 12)) translate(calc(7.5em * (1 - cos(2 * 3.14159 * 0 / 12))), calc(7.5em * sin(2 * 3.14159 * 0 / 12)));
    }
    .marker1 {
        width: 5em;
        height: 1em;
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 1 / 12)) translate(calc(7.5em * (1 - cos(2 * 3.14159 * 1 / 12))), calc(7.5em * sin(2 * 3.14159 * 1 / 12)));
    }
    .marker2 {
        width: 5em;
        height: 1em;
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 2 / 12)) translate(calc(7.5em * (1 - cos(2 * 3.14159 * 2 / 12))), calc(7.5em * sin(2 * 3.14159 * 2 / 12)));
    }
    .marker3 {
        width: 5em;
        height: 1em;
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 3 / 12)) translate(calc(7.5em * (1 - cos(2 * 3.14159 * 3 / 12))), calc(7.5em * sin(2 * 3.14159 * 3 / 12)));
    }
    .marker4 {
        width: 5em;
        height: 1em;
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 4 / 12)) translate(calc(7.5em * (1 - cos(2 * 3.14159 * 4 / 12))), calc(7.5em * sin(2 * 3.14159 * 4 / 12)));
    }
    .marker5 {
        width: 5em;
        height: 1em;
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 5 / 12)) translate(calc(7.5em * (1 - cos(2 * 3.14159 * 5 / 12))), calc(7.5em * sin(2 * 3.14159 * 5 / 12)));
    }
    .marker6 {
        width: 5em;
        height: 1em;
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 6 / 12)) translate(calc(7.5em * (1 - cos(2 * 3.14159 * 6 / 12))), calc(7.5em * sin(2 * 3.14159 * 6 / 12)));
    }
    .marker7 {
        width: 5em;
        height: 1em;
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 7 / 12)) translate(calc(7.5em * (1 - cos(2 * 3.14159 * 7 / 12))), calc(7.5em * sin(2 * 3.14159 * 7 / 12)));
    }
    .marker8 {
        width: 5em;
        height: 1em;
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 8 / 12)) translate(calc(7.5em * (1 - cos(2 * 3.14159 * 8 / 12))), calc(7.5em * sin(2 * 3.14159 * 8 / 12)));
    }
    .marker9 {
        width: 5em;
        height: 1em;
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 9 / 12)) translate(calc(7.5em * (1 - cos(2 * 3.14159 * 9 / 12))), calc(7.5em * sin(2 * 3.14159 * 9 / 12)));
    }
    .marker10 {
        width: 5em;
        height: 1em;
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 10 / 12)) translate(calc(7.5em * (1 - cos(2 * 3.14159 * 10 / 12))), calc(7.5em * sin(2 * 3.14159 * 10 / 12)));
    }
    .marker11 {
        width: 5em;
        height: 1em;
        border-radius: 0.5em;
        transform: rotate(calc(360deg * 11 / 12)) translate(calc(7.5em * (1 - cos(2 * 3.14159 * 11 / 12))), calc(7.5em * sin(2 * 3.14159 * 11 / 12)));
    }
</style>

<div id="spinner-container-marker">
    <div class="marker0"></div>
    <div class="marker1"></div>
    <div class="marker2"></div>
    <div class="marker3"></div>
    <div class="marker4"></div>
    <div class="marker5"></div>
    <div class="marker6"></div>
    <div class="marker7"></div>
    <div class="marker8"></div>
    <div class="marker9"></div>
    <div class="marker10"></div>
    <div class="marker11"></div>
</div>
"""


information_media_query = '''
  <style>
  @media (max-width: 1024px) {
      p.information_text {
        font-size: 3.6em;
      }
  }
  </style>
'''

class MultiFileDownloader(object):

    def __init__(self):
        super(MultiFileDownloader, self).__init__()

    def download_generated_images(self, files):
        zip_file = io.BytesIO()
        with zipfile.ZipFile(zip_file, mode='w') as zf:
            for i, (data, file_ext) in enumerate(files):
                new_filename = "oxbrAIn Generated Image {}.{}".format(i+1, file_ext)
                zf.writestr(new_filename, data)
        zip_file.seek(0)
        b64 = base64.b64encode(zip_file.getvalue()).decode()
        st.markdown("""
            <style>
                button.css-ffss7.ef3psqc11 {
                    background-color: #25476A;
                    color: #FAFAFA;
                    border-color: #FAFAFA;
                    border-width: 3px;
                    width: 5.4em;
                    height: 1.8em;
                    margin-top: 0.8em;
                }

                button.css-ffss7.ef3psqc11:hover {
                    background-color: rgba(111, 114, 222, 0.6);
                    color: #25476A;
                    border-color: #25476A;
                }

                @media (max-width: 1024px) {
                    button.css-ffss7.ef3psqc11 {
                        width: 100% !important;
                        height: 10em !important;
                        margin-top: -3em;
                    }
                }
            </style>
            """, unsafe_allow_html=True)
        
        filename_out = "oxbrAIn Image Generation Playground"
        st.download_button(
            label="Download",
            data=zip_file.getvalue(),
            file_name=f"{filename_out}.zip",
            mime="application/zip",
        )     




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

def download_images(images):
  spinner = st.markdown(marker_spinner_css, unsafe_allow_html=True)
  images_out = [(images[0], "png"), (images[1], "png")]
  downloader = MultiFileDownloader()
  downloader.download_generated_images(images_out)
  spinner.empty()
