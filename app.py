import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

# Set up the Streamlit page
st.set_page_config(page_title="Mandala Art Generator", layout="centered")
st.title("🌀 Mandala Art Generator")
st.markdown("Generate intricate black and white mandala art inspired by your words.")

# Secure API Key Input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

if api_key:
    # Prompt Type Selection
    prompt_type = st.radio("Choose Prompt Type:", ["Single Word", "Detailed Prompt"])

    if prompt_type == "Single Word":
        user_input = st.text_input("Enter a single word for inspiration:")
    else:
        user_input = st.text_area("Enter your detailed prompt:")

    if st.button("Generate Mandala"):
        if user_input.strip() == "":
            st.error("Please enter a valid input.")
        else:
            # Construct Prompt
            if prompt_type == "Single Word":
                prompt = f"A highly detailed black and white mandala inspired by the concept of '{user_input}'. Intricate line art, symmetrical patterns, suitable for coloring and printing."
            else:
                prompt = user_input

            # API Request to OpenAI
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            json_data = {
                "model": "dall-e-3",
                "prompt": prompt,
                "size": "1024x1024",
                "quality": "hd",
                "response_format": "url",
                "n": 1
            }

            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=json_data
            )

            if response.status_code == 200:
                image_url = response.json()["data"][0]["url"]
                image_response = requests.get(image_url)
                image = Image.open(BytesIO(image_response.content))

                st.image(image, caption="Generated Mandala", use_column_width=True)

                # Convert to PDF
                pdf_buffer = BytesIO()
                c = canvas.Canvas(pdf_buffer, pagesize=A4)
                width, height = A4

                # Wrap the PIL image using ImageReader
                img_reader = ImageReader(image)

                # Draw the image onto the PDF
                c.drawImage(img_reader, 0, 0, width=width, height=height)
                c.showPage()
                c.save()
                pdf_buffer.seek(0)

            
