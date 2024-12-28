import gradio as gr
import os
from pathlib import Path
from typing import Tuple
from utils import cleanup, download_profile, organize_files, validate_username


def get_download_stats(username: str) -> Tuple[int, int]:
    """
    Get the count of downloaded images and videos.

    Args:
        username (str): Username whose files to count

    Returns:
        Tuple[int, int]: Count of (images, videos)
    """
    base_path = Path(os.getcwd()) / username
    images_path = base_path / "images"
    videos_path = base_path / "videos"

    image_count = len(list(images_path.glob("*.jpg"))) + \
        len(list(images_path.glob("*.png"))) if images_path.exists() else 0
    video_count = len(list(videos_path.glob("*.mp4"))
                      ) if videos_path.exists() else 0

    return image_count, video_count


def fetch_profile(username: str, cleanup_files: bool) -> Tuple[str, str, str]:
    """
    Download and organize Instagram profile data for the given username.

    Args:
        username (str): Instagram username to fetch.
        cleanup_files (bool): Whether to clean up temporary files after download.

    Returns:
        Tuple[str, str, str]: Status message, Download path, Error details (if any)
    """
    try:
        username = username.strip().lower()
        if not username:
            return "Error: Username cannot be empty.", "", "Username field is required"

        if not validate_username(username):
            return (
                "Error: Invalid username format.",
                "",
                "Username must be 30 characters or less and contain only letters, numbers, periods, and underscores."
            )

        # Download and organize profile data
        download_profile(username)
        organize_files(username)

        # Get statistics
        image_count, video_count = get_download_stats(username)

        # Clean up if requested
        if cleanup_files:
            cleanup(username)
            base_path = "Files cleaned up after organization"
        else:
            base_path = str(Path(os.getcwd()) / username)

        status = f"""Download complete for @{username}!
        • {image_count} images downloaded
        • {video_count} videos downloaded"""

        return status, base_path, ""

    except Exception as e:
        error_msg = str(e)
        if "Profile does not exist" in error_msg:
            return f"Error: Profile '{username}' does not exist.", "", "Please check the username and try again."
        elif "Login required" in error_msg:
            return "Error: Login required to access this profile.", "", "This profile is private or requires authentication."
        else:
            return f"Error processing profile '{username}'", "", f"Details: {error_msg}"


def create_interface() -> gr.Interface:
    """
    Create and configure the Gradio interface.

    Returns:
        gr.Interface: Configured Gradio interface
    """
    # Define interface components
    with gr.Blocks(title="InstaVideo") as interface:
        gr.Markdown("""
        # InstaVideo
        Download and organize Instagram profile content with ease.
        
        ### Instructions:
        1. Enter an Instagram username
        2. Choose whether to clean up temporary files
        3. Click 'Download' to begin
        """)

        with gr.Row():
            username_input = gr.Textbox(
                label="Instagram Username",
                placeholder="Enter username (without @)",
                show_label=True
            )
            cleanup_checkbox = gr.Checkbox(
                label="Clean up temporary files",
                value=True,
                show_label=True
            )

        download_button = gr.Button("Download", variant="primary")

        with gr.Row():
            status_output = gr.Textbox(
                label="Status",
                show_label=True,
                interactive=False
            )
            path_output = gr.Textbox(
                label="Download Location",
                show_label=True,
                interactive=False
            )

        error_output = gr.Textbox(
            label="Error Details",
            show_label=True,
            interactive=False,
            visible=False
        )

        # Handle download button click
        download_button.click(
            fn=fetch_profile,
            inputs=[username_input, cleanup_checkbox],
            outputs=[status_output, path_output, error_output],
            api_name="download"
        )

        # Show error output when there's an error
        def show_error(error_msg):
            return gr.update(visible=bool(error_msg))

        error_output.change(
            fn=show_error,
            inputs=[error_output],
            outputs=[error_output]
        )

    return interface


def run(port: int = 7860, share: bool = True):
    """
    Launch the Gradio interface for the InstaVideo application.

    Args:
        port (int): Port to run the interface on
        share (bool): Whether to create a public link
    """
    interface = create_interface()
    interface.queue().launch(
        server_port=port,
        share=share,
        show_error=True,
        server_name="0.0.0.0"
    )


if __name__ == "__main__":
    run()
