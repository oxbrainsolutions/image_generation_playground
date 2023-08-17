import streamlit as st
import openai
import torch
from dalle_pytorch import DALLE
from dalle_pytorch.diffusion import StableDiverseDiffusion

# Set your OpenAI API key here
openai.api_key = "YOUR_OPENAI_API_KEY"

# Set up DALL-E model
dalle = DALLE.load_model("path_to_your_dalle_model.pth")

# Set up Stable Diffusion model
diffusion = StableDiverseDiffusion(dalle)

# Streamlit app
def main():
    st.title("DALL-E 2 Streamlit App")

    # User input
    user_idea = st.text_area("Enter your idea:", "")

    if st.button("Generate"):
        if user_idea:
            # Generate prompt based on user idea
            prompt = f"Image that represents the idea: {user_idea}"
            
            # Generate image using Stable Diffusion
            image = generate_image(prompt)
            
            # Display generated image and prompt
            st.image(image, caption="Generated Image", use_column_width=True)
            st.write("Generated Prompt:", prompt)

def generate_image(prompt):
    # Generate image using Stable Diffusion
    image = diffusion.generate_images(prompt)[0]
    
    # Convert to a format that Streamlit can display
    image = torch.clip(image, 0, 1)
    image = (image * 255).byte().permute(1, 2, 0).numpy()
    
    return image

if __name__ == "__main__":
    main()
