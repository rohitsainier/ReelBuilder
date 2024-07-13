import gradio as gr
import os
import datetime
from utils import cleanup, download_profile, organize_files, create_video_clips, create_final_video


def run():
    username = gr.Textbox(label="Enter username")
    output_message = gr.Textbox(label="Status")

    def fetchProfile(username):
        download_profile(username)
        organize_files(username)
        return "Download and organization complete for " + username

    gr.Interface(fn=fetchProfile, inputs=[
                 username], outputs=output_message, title="InstaVideo").queue().launch(share=True)


if __name__ == "__main__":
    run()
