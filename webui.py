import gradio as gr
import os
import datetime
from utils import cleanup, download_profile, organize_files, create_video_clips, create_final_video


def run():
    username = gr.Textbox(label="Enter username")
    enableAudio = gr.Checkbox(label="Skip Audio", value=False)
    audio = gr.Audio(source="upload", type="filepath",
                     label="Replace Original Audio")

    def fetchProfile(username, enableAudio, audio):
        download_profile(username)
        organize_files(username)
        video_clips = create_video_clips(username)
        # append date to output file
        output_file = os.path.join(
            os.getcwd(), datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".mp4")
        create_final_video(video_clips, output_file,
                           not enableAudio, audio)
        cleanup(username)
        return output_file

    gr.Interface(fn=fetchProfile, inputs=[
                 username, enableAudio, audio], outputs=gr.Video(autoplay=True), title="InstaVideo").queue().launch(share=True)


if __name__ == "__main__":
    run()
