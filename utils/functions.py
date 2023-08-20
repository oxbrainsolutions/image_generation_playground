import streamlit as st
import openai
import cv2
import urllib.request
from PIL import Image
import numpy as np
import io
import zipfile
import base64


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
                new_filename = f"oxbrAIn_Generated_Image_{i+1}.{file_ext}"
                zf.writestr(new_filename, data.getvalue())
                zf.filelist[-1].file_size = len(data.getvalue())
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
        
        filename_out = "oxbrAIn_Image_Generation_Playground.zip"
        st.download_button(
            label="Download",
            data=zip_file.getvalue(),
            file_name=f"{filename_out}.zip",
            mime="application/zip",
        )     

    def download_figure(self, data, file_ext, index):
        new_filename = "oxbrAIn_Generated_Image_{}.{}".format(index+1, file_ext)
        image = Image.open(data)
        new_image = Image.new(image.mode, size=(image.size[0], image.size[1]))
        new_image.putdata(image.getdata())  
        byte_array = io.BytesIO()
        new_image.save(byte_array, format='PNG', subsampling=0, quality=100)
        byte_array = byte_array.getvalue()
        return byte_array, new_filename

    def export_images(self, files):
        zip_file = io.BytesIO()
        with zipfile.ZipFile(zip_file, mode='w') as zf:
            for i, (data, file_ext) in enumerate(files):
                byte_array, new_filename = MultiFileDownloader().download_figure(data=data, file_ext=file_ext, index=i)
                zf.writestr(new_filename, byte_array)
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
        filename_out = "oxbrAIn_Image_Generation_Playground"
        st.download_button(
            label="Access",
            data=zip_file.getvalue(),
            file_name=f"{filename_out}.zip",
            mime="application/zip",
        )

def export_images(arrays):
  zip_file = io.BytesIO()
  with zipfile.ZipFile(zip_file, mode='w') as zf:
    for i, array in enumerate(arrays):
      new_filename = "oxbrAIn_Generated_Image_{}.png".format(i+1)
      zf.writestr(new_filename, array)
  zip_file.seek(0)
  b64 = base64.b64encode(zip_file.getvalue()).decode()
  filename_out = "oxbrAIn_Image_Generation_Playground"
  st.download_button(
      label="Download Images",
      data=zip_file.getvalue(),
      file_name=f"{filename_out}.zip",
      mime="application/zip",
  )


def generate_images(image_description, n_variations):

    images = []
    byte_arrays = []

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

            new_image = Image.new(img.mode, size=(img.size[0], img.size[1]))
            new_image.putdata(img.getdata())  
            byte_array = io.BytesIO()
            new_image.save(byte_array, format='PNG', subsampling=0, quality=100)
            byte_arrays = byte_array.getvalue()
            byte_arrays.append(byte_array)
    
        return images, byte_arrays


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
  images_out = [(img.tobytes(), "png") for img in images]
  downloader = MultiFileDownloader()
  downloader.export_images(images_out)
