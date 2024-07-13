import moviepy.editor as mp
import instaloader
import os
import random
import shutil

# add option for start and end date to download profile data


def download_profile(username: str):
    try:
        # Create an instance of the Instaloader class
        loader = instaloader.Instaloader()
        # Load the profile with the given username
        profile = instaloader.Profile.from_username(loader.context, username)
        # Disable saving metadata and downloading video thumbnails
        loader.save_metadata = False
        loader.download_video_thumbnails = False
        # Download all posts (photos and videos) from the profile
        loader.download_profile(profile, profile_pic_only=False)
    except Exception as e:
        print(f"Error downloading profile: {e}")


def organize_files(username):
    try:
        # Create 'images' and 'videos' folders if they don't exist
        for folder_name in ['images', 'videos']:
            folder_path = os.path.join(username, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    # Move photos to the 'images' folder and videos to the 'videos' folder
        for filename in os.listdir(username):
            if filename.endswith((".jpg", ".png")):
                os.rename(os.path.join(username, filename),
                          os.path.join(username, 'images', filename))
            elif filename.endswith(".mp4"):
                os.rename(os.path.join(username, filename),
                          os.path.join(username, 'videos', filename))
    except Exception as e:
        print(f"Error organizing files: {e}")


def create_video_clips(username, skipPhotos: bool = False, skipVideos: bool = False):
    try:
        # Create a list to store the video clips
        video_clips = []

        # Read the images from the 'images' folder
        if not skipPhotos:
            image_folder = os.path.join(username, 'images')
            for filename in os.listdir(image_folder):
                path = os.path.join(image_folder, filename)
                clip = mp.ImageClip(path, duration=random.uniform(2, 3))
                # clip = clip.resize((target_width, target_height))
                video_clips.append(clip)

        # Read the videos from the 'videos' folder
        if not skipVideos:
            video_folder = os.path.join(username, 'videos')
            for filename in os.listdir(video_folder):
                path = os.path.join(video_folder, filename)
                video_duration = mp.VideoFileClip(path).duration
                if video_duration > 10:
                    clip = mp.VideoFileClip(path).subclip(
                        0, random.uniform(5, 10))
                else:
                    clip = mp.VideoFileClip(path)
                    # clip = clip.resize((target_width, target_height))
                video_clips.append(clip)

        return video_clips
    except Exception as e:
        print(f"Error creating video clips: {e}")
        return []


def create_final_video(video_clips, output_path, enableAudio: bool = True, audioPath: str = ""):
    try:
        # Shuffle the video clips randomly
        random.shuffle(video_clips)
        print("Video clips shuffled successfully")

        # Concatenate the video clips into a final video
        final_clip = mp.concatenate_videoclips(video_clips, method="compose")
        # final_clip = final_clip.resize((final_clip.w, final_clip.h))
        print("Video clips concatenated successfully")
        print(enableAudio, audioPath)
        # Add music to the video
        if enableAudio and audioPath != None and audioPath != "":
            final_clip = addMusicToVideo(final_clip, audio=audioPath)
            print("Music added to the video")
        else:
            print("No music added to the video")

        # Write the final video to a file
        final_clip.write_videofile(output_path, audio=enableAudio, fps=24)
        print(f"Final video written to {output_path}")

        # Return the final video
        return final_clip
    except Exception as e:
        print(f"Error creating final video: {e}")


def cleanup(username):
    try:
        folder = os.path.join(os.getcwd(), username)
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Folder {folder} has been removed")

    except Exception as e:
        print(f"Error cleaning up: {e}")


def addMusicToVideo(clip, audio: str = "music.mp3"):
    try:
        music = mp.AudioFileClip(audio)
        # Set accoring to clip duration
        if clip.duration < music.duration:
            music = music.subclip(0, clip.duration)
        else:
            music = music.subclip(0, music.duration)
        return clip.set_audio(music)
    except Exception as e:
        print(f"Error adding music to video: {e}")

# Create single video from images folder or videos folder


def createVideo(source: str, destination: str, fps: int = 24, enableAudio: bool = True, audioPath: str = "music.mp3", mix: bool = False):
    clipsArray = []
    try:
        dataFolder = os.path.join(source)
        for filename in os.listdir(dataFolder):
            if filename.endswith((".jpg", ".png")):
                path = os.path.join(dataFolder, filename)
                clip = mp.ImageClip(path, duration=random.uniform(2, 3))
                clipsArray.append(clip)
            elif filename.endswith(".mp4"):
                path = os.path.join(dataFolder, filename)
                clip = mp.VideoFileClip(path)
                clipsArray.append(clip)

        # Shuffle the video clips randomly
        if mix:
            random.shuffle(clipsArray)

        final_clip = mp.concatenate_videoclips(clipsArray, method="compose")
        if enableAudio:
            final_clip = addMusicToVideo(final_clip, audio=audioPath)
        final_clip.write_videofile(destination, audio=enableAudio, fps=fps)
    except Exception as e:
        print(f"Error creating local video: {e}")

# add subtitles to video
    def addSubtitlesToVideo(videoPath: str, subtitle: str):
        try:
            clip = mp.VideoFileClip(videoPath)
            subtitle_clip = mp.TextClip(
                subtitle, fontsize=20, color='white')
            final_clip = mp.CompositeVideoClip([clip, subtitle_clip])
            final_clip.write_videofile("output.mp4")
        except Exception as e:
            print(f"Error adding subtitles to video: {e}")
