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

def export_images(arrays):
  zip_file = io.BytesIO()
  with zipfile.ZipFile(zip_file, mode='w') as zf:
    for i, array in enumerate(arrays):
      new_filename = "oxbrAIn_Generated_Image_{}.png".format(i+1)
      zf.writestr(new_filename, array)
  zip_file.seek(0)
  b64 = base64.b64encode(zip_file.getvalue()).decode()
  st.markdown("""
            <style>
                button.css-1uccjzq.ef3psqc11 {
                  background-color: #002147;
                  color: #FAFAFA;
                  border-color: #FAFAFA;
                  border-width: 0.15em;
                  width: 100%;
                  height: 0.2em !important;
                  margin-top: 0em;
                  font-family: sans-serif;
                }

                button.css-1uccjzq.ef3psqc11:hover {
                  background-color: #76787A;
                  color: #FAFAFA;
                  border-color: #002147;
                }

                @media (max-width: 1024px) {
                    button.css-1uccjzq.ef3psqc11 {
                      width: 100% !important;
                      height: 0.8em !important;
                      margin-top: 0em;
                      border-width: 0.15em; !important;
                    }
                }
            </style>
            """, unsafe_allow_html=True)
 
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
    error_field3 = st.empty()

    try:
        img_response = openai.Image.create(
        prompt = image_description,
        n=n_variations,
        size="256x256")
    except openai.error.Timeout as e:
        #Handle timeout error, e.g. retry or log
        print(f"OpenAI API request timed out: {e}")
        st.session_state.error_indicator = True
        error_field3.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.APIError as e:
        #Handle API error, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        st.session_state.error_indicator = True
        error_field3.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.APIConnectionError as e:
        #Handle connection error, e.g. check network or log
        print(f"OpenAI API request failed to connect: {e}")
        st.session_state.error_indicator = True
        error_field3.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.InvalidRequestError as e:
        #Handle invalid request error, e.g. validate parameters or log
        print(f"OpenAI API request was invalid: {e}")
        st.session_state.error_indicator = True
        error_field3.error("Error: Your request was rejected by the safety system. Please amend your input and try again.")
        return None
    except openai.error.AuthenticationError as e:
        #Handle authentication error, e.g. check credentials or log
        print(f"OpenAI API request was not authorized: {e}")
        st.session_state.error_indicator = True
        error_field3.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.PermissionError as e:
        #Handle permission error, e.g. check scope or log
        print(f"OpenAI API request was not permitted: {e}")
        st.session_state.error_indicator = True
        error_field3.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.RateLimitError as e:
        #Handle rate limit error, e.g. wait or log
        print(f"OpenAI API request exceeded rate limit: {e}")
        st.session_state.error_indicator = True
        error_field3.error("Error: An error occurred. Please try again.")
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
            byte_array = byte_array.getvalue()
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

category_prompts = {
"Nature": ["Foggy forest at night, watercolor style, mysterious mood", "Majestic waterfall, photorealistic style, awe-inspiring mood", "Rocky beach at sunrise, impressionist style, peaceful mood", "Snowy mountains in the distance, minimalist style, serene mood", "Sunflower field in the summer, oil painting style, happy mood", "Desert landscape at sunset, abstract style, contemplative mood", "Autumn leaves falling from trees, pointillism style, nostalgic mood", "Underwater coral reef, surreal style, dreamy mood", "Thunderstorm over the city, expressionist style, dramatic mood", "Rainbow over a meadow, pop art style, joyful mood"],
"Animals": ["Playful kitten with a ball of yarn, cartoon style, whimsical mood", "Majestic lion in the savannah, realistic style, powerful mood", "Elegant horse galloping in a field, sketch style, free-spirited mood", "Cute bunny eating a carrot, pastel style, innocent mood", "Mischievous raccoon stealing food, watercolor style, playful mood", "Majestic eagle soaring in the sky, oil painting style, awe-inspiring mood", "Sassy flamingo posing, neon style, confident mood", "Ferocious shark in the ocean, minimalist style, intense mood", "Regal peacock showing off its feathers, photorealistic style, proud mood", "Adorable otter holding hands, abstract style, loving mood"],
"Food & Drink": ["Delicious pizza with all the toppings, realistic style, savory mood", "Mouth-watering sushi rolls, watercolor style, fresh mood", "Tasty cupcake with frosting, sketch style, sweet mood", "Juicy hamburger with fries, pop art style, indulgent mood", "Refreshing fruit smoothie, pastel style, healthy mood", "Spicy bowl of noodles, abstract style, bold mood", "Icy margarita in a tropical setting, neon style, relaxed mood", "Crispy fried chicken, photorealistic style, satisfying mood", "Rich cup of coffee, minimalist style, energized mood", "Sweet bowl of ice cream with sprinkles, oil painting style, happy mood"],
"People": ["Energetic kids playing in the park, cartoon style, playful mood", "Romantic couple dancing under the stars, watercolor style, dreamy mood", "Confident businesswoman in a cityscape, realistic style, powerful mood", "Enthusiastic athlete running on a beach, sketch style, free-spirited mood", "Joyful family having a picnic, pastel style, happy mood", "Serious musician playing an instrument, abstract style, introspective mood", "Fashionable model on a runway, neon style, confident mood", "Wise elderly person in a cozy home, photorealistic style, wise mood", "Excited traveler exploring a new city, minimalist style, adventurous mood", "Creative artist in a studio, oil painting style, inspired mood"],
"Abstract": ["Abstract geometric pattern, illuminated in neon colors, vector design", "Abstract painting, with swirling shapes and colors, digital art", "Abstract sculpture, with no apparent form or function, 3D render", "Abstract music, with no discernible melody or rhythm, matte painting", "Abstract poem, with no apparent meaning or structure, vector design", "Swirling vortex of colors, digital art style, chaotic mood", "Geometric shapes in a monochrome palette, minimalist style, futuristic mood", "Distorted reflection of a city skyline, impressionist style, surreal mood", "Fluid brushstrokes in a neon palette, expressionist style, energetic mood", "Mosaic of patterns and textures, abstract style, intricate mood", "Kaleidoscope of shapes and colors, pop art style, playful mood", "Layers of shapes and lines, sketch style, introspective mood", "Gradient of colors fading into each other, pastel style, peaceful mood", "Collage of different images and textures, mixed media style, eclectic mood", "Doodles and scribbles in a notebook, marker style, whimsical mood"],
"Fantasy": ["Enchanted castle in the clouds, digital art style, magical mood", "Mythical dragon in a mystical forest, oil painting style, awe-inspiring mood", "Whimsical unicorn in a candy-colored landscape, cartoon style, playful mood", "Dark wizard casting a spell, photorealistic style, ominous mood", "Mermaid lounging on a rock in the ocean, watercolor style, serene mood", "Cyborg warrior battling futuristic monsters, concept art style, intense mood", "Elaborate fairy tale book cover, mixed media style, enchanting mood", "Steampunk airship soaring through the sky, sketch style, adventurous mood", "Gothic vampire in a Victorian mansion, realistic style, eerie mood", "Futuristic cityscape with neon lights, cyberpunk style, dystopian mood"],
"Sci-Fi": ["Spacecraft landing on an alien planet, digital art style, otherworldly mood", "Futuristic city skyline at night, neon style, cybernetic mood", "Futuristic soldier in a hi-tech suit, concept art style, intense mood", "Time machine in a laboratory, photorealistic style, scientific mood", "Dystopian wasteland with ruined buildings, abstract style, bleak mood", "Cybernetic implants in a human body, mixed media style, futuristic mood", "Androids in a futuristic society, sketch style, philosophical mood", "Extraterrestrial life form in a sci-fi landscape, oil painting style, surreal mood", "Advanced technology in a city of the future, minimalist style, inspiring mood", "Cosmic explosion in outer space, watercolor style, epic mood"],
"Urban": ["Bustling city street at night, realistic style, vibrant mood", "Graffiti-covered alleyway, impressionist style, gritty mood", "Retro diner with neon lights, pop art style, nostalgic mood", "Busy urban intersection during rush hour, photorealistic style, chaotic mood", "Run-down apartment building, sketch style, melancholic mood", "Modern skyscraper with a reflective surface, abstract style, futuristic mood", "Vintage storefronts on a cobblestone street, pastel style, quaint mood", "Public transportation station with commuters, minimalist style, busy mood", "Urban park with a fountain, oil painting style, tranquil mood", "Industrial factory with smokestacks, mixed media style, ominous mood"],
"Objects": ["Vintage camera with a leather strap, photorealistic style, classic mood", "Antique typewriter with a stack of paper, sketch style, nostalgic mood", "Colorful balloons floating in the sky, watercolor style, festive mood", "Sparkling diamond necklace on a black background, minimalist style, luxurious mood", "Retro radio with knobs and dials, mixed media style, vintage mood", "Succulent plant in a ceramic pot, impressionist style, natural mood", "Cup of steaming hot coffee on a saucer, oil painting style, cozy mood", "Old-fashioned record player with vinyl records, pop art style, groovy mood", "Glittering chandelier in a grand ballroom, photorealistic style, elegant mood", "Colorful pinwheel spinning in the wind, cartoon style, playful mood", "Antique book with gold-leaf pages, watercolor style, intellectual mood", "Classic pocket watch on a chain, sketch style, timeless mood", "Shiny red apple on a wooden table, pastel style, simple mood", "Vintage telephone with a rotary dial, abstract style, nostalgic mood", "Classic car with a polished chrome grille, mixed media style, retro mood"],
"Random": ["Majestic mountain range in the distance, oil painting style, serene mood", "Bright yellow taxi on a busy city street, digital art style, chaotic mood", "Majestic lion with a flowing mane, photorealistic style, powerful mood", "Rustic wooden cabin in the woods, watercolor style, cozy mood", "Vibrant street art on a brick wall, graffiti style, edgy mood", "Whimsical hot air balloon floating in the clouds, mixed media style, dreamy mood", "Traditional Japanese pagoda in a serene garden, ink drawing style, zen mood", "Colorful butterfly in flight, impressionist style, whimsical mood", "Spooky haunted mansion on a dark hill, dark art style, eerie mood", "Elegant ballerina in a tutu, sketch style, graceful mood", "Sparkling diamond ring on a velvet pillow, photorealistic style, luxurious mood", "Romantic couple embracing in the rain, oil painting style, passionate mood", "Modern skyscraper in a futuristic city, digital art style, high-tech mood", "Scary jack-o-lantern on a porch, cartoon style, Halloween mood", "Majestic bald eagle soaring through the sky, photorealistic style, majestic mood", "Rustic windmill on a farm, watercolor style, peaceful mood", "Vibrant cityscape at night, mixed media style, electric mood", "Playful cartoon character eating a giant sandwich, pop art style, funny mood", "Vintage travel poster for an exotic destination, impressionist style, adventurous mood", "Regal peacock with colorful plumage, sketch style, proud mood", "Modern abstract painting with bold colors, abstract style, creative mood", "Mysterious abandoned carnival at night, dark art style, haunting mood", "Colorful parrot perched on a branch, photorealistic style, tropical mood", "Sleek sports car on an open road, oil painting style, adventurous mood", "Beautiful mermaid swimming in the ocean, watercolor style, mystical mood", "Intricate mandala design with vibrant colors, digital art style, spiritual mood", "Cozy fireplace with crackling flames, mixed media style, warm mood", "Whimsical unicorn prancing through a meadow, cartoon style, magical mood", "Vintage movie poster for a classic film, photorealistic style, nostalgic mood", "Elegant ballroom with a crystal chandelier, oil painting style, sophisticated mood", "Cute cartoon animal playing a musical instrument, pop art style, fun mood", "Beautiful waterfall in a lush forest, impressionist style, tranquil mood", "Sleek motorcycle on an open road, watercolor style, daring mood", "Futuristic spaceship soaring through the stars, digital art style, epic mood", "Spooky graveyard at night with full moon, dark art style, ominous mood", "Colorful rainbow over a peaceful countryside, mixed media style, hopeful mood", "Whimsical fairy tale castle in the clouds, sketch style, fantastical mood", "Classic still life painting of fruit, oil painting style, simple mood", "Vibrant street scene in a bustling city, watercolor style, energetic mood", "Cute cartoon character enjoying a bubble bath, pop art style, relaxing mood", "Beautiful sailboat on a calm sea, photorealistic style, serene mood", "Majestic tiger prowling through the jungle, oil painting style, fierce mood", "Rustic barn on a country farm, watercolor style, peaceful mood", "Iconic Eiffel Tower at sunset, realistic style, romantic mood", "Famous Great Wall of China, watercolor style, historic mood", "Enchanting Taj Mahal at sunrise, sketch style, serene mood", "Grand Statue of Liberty, pastel style, patriotic mood"],
"Futuristic": ["Futuristic cityscape, reflecting sunset, concept art", "Futuristic spaceship, landing on a red planet, 3D render", "Futuristic city, with flying cars and robots, digital painting", "Futuristic landscape, with glowing cities and mountains, matte painting", "Futuristic interior, with sleek furniture and holographic displays, vector design"],
"Ancient": ["Ancient Egyptian temple, adorned with hieroglyphs, photorealistic", "Ancient Greek temple, surrounded by columns and statues, digital art", "Ancient Roman city, with ruins and crumbling buildings, 3D render", "Ancient forest, with towering trees and moss-covered rocks, matte painting", "Ancient cave, with stalactites and stalagmites, vector design"],
"Friendly": ["Friendly robot, serving coffee, 3D render", "Friendly alien, waving hello, digital art", "Friendly dog, wagging its tail, 3D render", "Friendly cat, purring and rubbing against your leg, matte painting", "Friendly person, smiling and giving a thumbs up, vector design"],
"Surreal": ["Surreal underwater garden, filled with glowing plants, digital painting", "Surreal landscape, with impossible architecture and floating islands, matte painting", "Surreal city, with buildings that twist and turn, vector design", "Surreal creature, with multiple eyes and limbs, 3D render", "Surreal object, with no apparent purpose or function, digital art"],
"Steampunk": ["Steampunk airship, soaring above forest, CGI", "Steampunk city, with cogs and gears everywhere, digital art", "Steampunk robot, with brass and leather armor, 3D render", "Steampunk weapon, with a steam-powered piston, matte painting", "Steampunk outfit, with a top hat and goggles, vector design"],
"Haunted": ["Haunted Victorian mansion, shrouded in fog, gothic art", "Haunted house, with creaking doors and rattling windows, digital art", "Haunted forest, with glowing eyes in the darkness, 3D render", "Haunted graveyard, with tombstones and skeletons, matte painting", "Haunted object, that seems to move on its own, vector design"],
"Cyberpunk": ["Cyberpunk city street, bustling with neon signs, matte painting", "Cyberpunk nightclub, with flashing lights and loud music, digital art", "Cyberpunk hacker, breaking into a computer system, 3D render", "Cyberpunk vehicle, with sleek design and glowing lights, vector design", "Cyberpunk weapon, with a laser sight and a holographic sight, matte painting"],
"Majestic": ["Majestic mountain range, basking in sunrise, landscape photography", "Majestic waterfall, crashing down a cliff face, digital art", "Majestic forest, with towering trees and lush green leaves, 3D render", "Majestic ocean, with waves crashing against the shore, matte painting", "Majestic animal, such as a lion or a tiger, vector design"],
"Whimsical": ["Whimsical unicorn, galloping through a field of flowers, digital art", "Whimsical teapot, with a spout that looks like a duck’s bill, 3D render", "Whimsical house, with a door that looks like a cat’s face, matte painting", "Whimsical creature, with a long tail and floppy ears, vector design", "Whimsical object, such as a toy or a piece of jewelry, digital art"]
}

def generate_similar_prompt(category):
    example_prompts = category_prompts.get(category, [])
    combined_prompts = "\n".join(example_prompts)
    new_prompt = f"Generate an image inspired by {category}:\n\n{combined_prompts}\n\nWrite a single prompt similar to the examples, describing a scene with modifiers for mood, style, lighting, and other attributes."

    total_tokens = len(new_prompt.split())
    max_tokens = total_tokens + 30  # Adding a buffer
  
    try:
      response = openai.Completion.create(
          engine="text-davinci-003",  # You can choose the appropriate engine
          prompt=new_prompt,
          max_tokens=max_tokens
      )
    except openai.error.Timeout as e:
        #Handle timeout error, e.g. retry or log
        print(f"OpenAI API request timed out: {e}")
        st.session_state.error_indicator = True
        error_field1.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.APIError as e:
        #Handle API error, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        st.session_state.error_indicator = True
        error_field1.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.APIConnectionError as e:
        #Handle connection error, e.g. check network or log
        print(f"OpenAI API request failed to connect: {e}")
        st.session_state.error_indicator = True
        error_field1.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.InvalidRequestError as e:
        #Handle invalid request error, e.g. validate parameters or log
        print(f"OpenAI API request was invalid: {e}")
        st.session_state.error_indicator = True
        error_field1.error("Error: Your request was rejected by the safety system. Please amend your input and try again.")
        spinner.empty()
        return None
    except openai.error.AuthenticationError as e:
        #Handle authentication error, e.g. check credentials or log
        print(f"OpenAI API request was not authorized: {e}")
        st.session_state.error_indicator = True
        error_field1.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.PermissionError as e:
        #Handle permission error, e.g. check scope or log
        print(f"OpenAI API request was not permitted: {e}")
        st.session_state.error_indicator = True
        error_field1.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None
    except openai.error.RateLimitError as e:
        #Handle rate limit error, e.g. wait or log
        print(f"OpenAI API request exceeded rate limit: {e}")
        st.session_state.error_indicator = True
        error_field1.error("Error: An error occurred. Please try again.")
        spinner.empty()
        return None

    return response.choices[0].text.strip()


