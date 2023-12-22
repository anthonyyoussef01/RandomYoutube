# Libraries for drawing and generating random numbers
import numpy as np
import matplotlib.pyplot as plt
# Libraries for compiling a video and handling files
import moviepy.editor as mpy
import os

# Libraries for handling dates and interacting with the YouTube Data API
# import datetime
# from Google import Create_Service
# from googleapiclient.http import MediaFileUpload

if __name__ == '__main__':
    # Step 1: Generate a video with random pixels
    def generate_random_video(filename, duration, fps, width, height):
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
        clip.write_videofile(filename, codec='libx264')

        # Delete the frame images
        for frame_filename in frames:
            os.remove(frame_filename)


    # Generate a random video
    generate_random_video('random.mp4', 10, 30, 640, 480)
