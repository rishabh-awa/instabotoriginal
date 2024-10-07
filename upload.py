import cloudinary
import cloudinary.uploader
import cloudinary.api

import os
from dotenv import load_dotenv

import requests
import time

from imagegen import createpost

load_dotenv()
# Set up your Cloudinary credentials
def setuplink():
    cloudinary.config(
    cloud_name = os.getenv("NAME"),
    api_key = os.getenv("CLOUD"),
    api_secret = os.getenv("SEC")
    )

    # Path to the downloaded video (you can replace this with the in-memory file if needed)
    video_path = r"temp/tempo.mp4"

    # Upload the video to Cloudinary
    upload_result = cloudinary.uploader.upload_large(
        video_path,
        resource_type = "video"
    )

    # Get the URL of the uploaded video
    video_url = upload_result.get("secure_url")
    video_id = upload_result.get("public_id")
    print(f"Video URL: {video_url}")
    return [video_url,video_id]


def post():
    accounts = ["17841469797379138","17841468375966036"]
    diction = {17841469797379138:"gloryxstoics",17841468375966036:"asxension.n.glory"}
    for i in accounts:    
        stat = None
        tempoi = int(i)
        accname = diciton[tempoi]
        # Access Token (replace with your token)
        access_token = os.getenv("ACCESS")
        # Facebook API endpoint for fetching accounts
        urlforvideo = setuplink()
        urlvideo = urlforvideo[0]
        text = f"Let me manipulate you into being better.\n \nfollow: @{accname}\nfollow: @{accname} \n\n %23strongmen %23stoics %23growth"


        posturi= f"https://graph.facebook.com/v20.0/{i}/media?media_type=REELS&video_url={urlvideo}&caption={text}&access_token={access_token}"
        # Make the request
        post = requests.post(posturi)
        data = post.json()

        id = int(data["id"])
        print(id)

        while stat==None or stat=='IN_PROGRESS':
            staturi=f"https://graph.facebook.com/v20.0/{id}?fields=status_code&access_token={access_token}"
            status = requests.get(staturi)
            stat = status.json()
            stat = stat["status_code"]
            time.sleep(3)
        print(stat)
        publishuri = f"https://graph.facebook.com/v20.0/{i}/media_publish?creation_id={id}&access_token={access_token}"
        publish = requests.post(publishuri)
        dat = publish.json()


        print("Instagram Account ID:", data)
        print(dat)
    cloudinary.uploader.destroy(urlforvideo[1], resource_type="video")   

def complete():
    createpost()
    post()

complete()
