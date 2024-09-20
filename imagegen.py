import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import requests
import base64

import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import textwrap

from moviepy.editor import ImageClip,AudioFileClip

def getimage(quotename):
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  # necessary for Windows OS
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

    driver = uc.Chrome(options=chrome_options)
    driver.get("https://www.artbreeder.com/create/composer")
    time.sleep(1)
    ele = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    elem = driver.find_element(By.TAG_NAME, "textarea")
    elem.clear()
    lst = ["Theatrical, dramatic, frame, black and white, for instagram post with a melancholic image, feels like winter, silhoutte of a man and a horse, medieval",
           "Theatrical, dramatic, frame, black and white, for instagram post with a melancholic image,darker shadows,motivating statue of "]
    prompt = lst[1]+quotename
    try:
        elem.send_keys(prompt)
        time.sleep(10)
        image = driver.find_element(By.TAG_NAME,"img")
        source = image.get_attribute("src")
        base64_data = source.split(',')[1]
        image_bytes = base64.b64decode(base64_data)
        with open(r"temp/tempo.jpg", "wb") as file:
            file.write(image_bytes)
        
    except:
        print("there was an error accessing the page")

    image = Image.open(r"temp/tempo.jpg")
    enhancer = ImageEnhance.Brightness(image)
    darkened_image = enhancer.enhance(0.8)   
    darkened_image.save("temp/tempo.jpg")
    driver.close()

def getstoicquote():
    

    url = "https://stoic-quotes.com/api/quote"  # Example API URL
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"{data['text']} - {data['author']}")
    else:
        print("Failed to retrieve a quote.")

    with open("quotes.txt","r") as file:
        lst=file.readlines()
        if (data["text"]+"\n") in lst:
            quote = getstoicquote()
            return quote

    with open("quotes.txt","a+") as file:
        file.write(data['text']+"\n")
    
    return [data['text'],data['author']]

print(getstoicquote())

def convertclip(path="temp/content.jpg" ,duration=8,outputpath="temp/tempo.mp4",audio_path="contentmusic.mp3"):
    clip = ImageClip(path, duration=duration)
    audio = AudioFileClip(audio_path)
    # Set the frame rate (frames per second)
    clip = clip.set_fps(24)  # You can adjust the frame rate as needed
    audio = audio.subclip(0, duration)
    # Write the video file
    clip = clip.set_audio(audio)
    clip.write_videofile(outputpath, codec='libx264')

def createpost():
        # Open the image
    lst = getstoicquote()
    author = lst[1]
    quote = lst[0]
    text = f"{quote}\n- {author}"
    getimage(author)
    image = Image.open(r"temp/tempo.jpg")

    draw = ImageDraw.Draw(image)

    # Define the font (you may need to specify the path to a .ttf font file on your system)
    font_path = r"font\LibreBaskerville-Bold.ttf"  # Adjust path as needed
    image_width, image_height = image.size
    
    # Try to fit the text by decreasing font size until it fits
    font_size = 30
    font = ImageFont.truetype(font_path, font_size)
    text_width = text_height = 4
    line = text.split("\n")
    # Try to fit the text by decreasing font size until it fits
    font_size = 30
    while font_size >= 28:
        font = ImageFont.truetype(font_path, font_size)
        # Get the bounding box of the text
        lines = textwrap.wrap(text, width=40)
        total_text_height = sum([draw.textbbox((0, 0), line, font=font)[3] for line in lines])
        # Check if the text fits within the image width (with padding)
        if total_text_height + 2 * 2 <= image_height:
            break  # Text fits, so we can stop reducing the font size
        
        # Reduce font size for next iteration
        font_size -= 1
    


    y_offset = (image_height - total_text_height) // 2  # Start from the vertical center
    for line in lines:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:]
        text_x = (image_width - text_width) // 2  # Center each line horizontally
        draw.text((text_x, y_offset), line, font=font, fill="white")
        y_offset += text_height  # Move the y position down for the next line

    
    # Add the text to the image
    
    # Save the image with text
    image.save("temp/content.jpg")
    os.remove(r"temp/tempo.jpg")
    convertclip()
    os.remove(r"temp/content.jpg")
# Example usage



createpost()