# Libraries for drawing and generating random numbers
import numpy as np
import matplotlib.pyplot as plt
import random
import string
# Libraries for compiling a video and handling files
import moviepy.editor as mpy
import os
# Libraries for handling dates and interacting with the YouTube Data API
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# Step 1: Generate a video with random pixels
def generate_random_video(filename, duration, fps, width, height):
    # TODO: remove this when uploading to YouTube functionality is added and delete the random.mp4 file at the end
    # delete random.mp4 if it exists
    if os.path.exists(filename):
        os.remove(filename)
    # Create a list to store all frames
    frames = []

    for _ in range(fps * duration):
        # Generate an array of random RGB values
        array = np.random.rand(height, width, 3)

        # Create an image from the array
        plt.imshow(array)
        plt.axis('off')

        # Save the frame as an image
        frame_filename = f'frame_{_:04d}.png'
        plt.savefig(frame_filename, bbox_inches='tight', pad_inches=0)

        # Add the frame to the list
        frames.append(frame_filename)

        # Clear the current figure
        plt.clf()

    # Compile the frames into a video
    clip = mpy.ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(filename, codec='libx264', bitrate='5000k', threads=10)

    # Delete the frame images
    for frame_filename in frames:
        os.remove(frame_filename)


# --------------------------------------------------------------------------------------------
# Step 2: Upload the video to YouTube

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def upload_video(youtube, file):
    # Generate a random title and description
    title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    description = ''.join(random.choices(string.ascii_uppercase + string.digits, k=50))

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": description,
                "title": title
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(file)
    )
    response = request.execute()

    print(f'Uploaded file id: {response["id"]}')

if __name__ == '__main__':
    # Generate a random video
    generate_random_video('random.mp4', 10, 30, 640, 480)
    youtube = get_authenticated_service()
    upload_video(youtube, 'random.mp4')
