import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# Function to open and display image based on a given design.
def open_images(prompt ):
    folder_path = r"Data"  # Folder where the images are stored.
    prompt = prompt.replace(" " , "_") # Replace spaces in prompt with underscores.
    
    # Generate the filename for the user.
    Files = [f"{prompt}{i}.jpg" for i in range(1,5)]
    
    for jpg_files in Files :
        image_path = os.path.join(folder_path , jpg_files)
        
        try :
            # try to open and display the image.
            img = Image.open(image_path)
            print(f"Opening Image : {image_path}")
            img.show()
            sleep(1)  # Pause for 1 second before showing the next image.
            
        except IOError :
            print(f"Unable to open {image_path}")
            
# API details for the Hugging Face Stable Diffusion model.
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0" 
headers = {"Authorization" : f"Bearer {get_key('.env' , 'HuggingFaceAPIKey')}"}

# Async function to send a Query to the Hugging face API.
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
    return response.content


# Async function to generate image based on the given prompt.
async def generate_images(prompt : str) :
    tasks = []
    
    # Create 4 images generation tasks.
    for _ in range(4) :
        payload = {
            "inputs" : f"{prompt} , quality=4k , sharpness=maximum, Ultra High details , high resolution , send = {randint(0 , 1000000)}"
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)
        
        # Wait for all task to complete.
        image_bytes_list = await asyncio.gather(*tasks)
        
        # Save the generated images to files.
        prompt_filename = prompt.replace(" ", "_")
        for i , image_bytes in enumerate(image_bytes_list) :
            with open(fr"Data\{prompt_filename}{i+1}.jpg" , "wb") as f:
                f.write(image_bytes)
                
# Wrapper function to monitor image genberation reports.
def GenerateImages(prompt : str) :
    asyncio.run(generate_images(prompt))
    open_images(prompt)
    
# Main loop to monitor for image generation requests.
while True :
    
    try :
        # Read the status and prompt from the data file.
        with open(r"Frontend\Files\ImageGeneration.data" , "r") as f :
            Data : str = f.read()
            
        Prompt , Status = Data.split(",")
        Status = Status.strip()
        # If the status indicates an image generation request.
        if Status.strip() == "True" :
            print("Generating Images.....")
            ImageStatus = GenerateImages(prompt=Prompt)
            
            # Read the status in the file after generating images.
            with open(r"Frontend\Files\ImageGeneration.data" , "w") as f :
                f.write("False,False")
                break # Exit the loop after processing the requests
            
        else :
            sleep(1) # Wait for 1 second before checking again.
            
    except Exception as e:
        print(f"Error : {e}")