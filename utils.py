import instaloader
import os
import shutil
import logging
from typing import Optional
from pathlib import Path
from typing import Union

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('instagram_downloader.log')
    ]
)
logger = logging.getLogger(__name__)


class InstagramDownloaderError(Exception):
    """Custom exception class for Instagram downloader errors."""
    pass


def validate_username(username: str) -> bool:
    """
    Validate Instagram username format.

    Args:
        username (str): Instagram username to validate.

    Returns:
        bool: True if username is valid, False otherwise.
    """
    if not username or not isinstance(username, str):
        return False
    # Basic Instagram username validation (30 characters max, alphanumeric, underscores and periods)
    return len(username) <= 30 and all(c.isalnum() or c in ['_', '.'] for c in username)


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('instagram_downloader.log')
    ]
)
logger = logging.getLogger(__name__)


def download_profile(username: str):
    """
    Download all posts (photos and videos) from an Instagram profile.

    Args:
        username (str): Instagram username to download.
    """
    try:
        logger.info(f"Starting download for profile: {username}")

        # Create an instance of the Instaloader class
        loader = instaloader.Instaloader()

        # Load the profile with the given username
        profile = instaloader.Profile.from_username(loader.context, username)

        # Disable saving metadata and downloading video thumbnails
        loader.save_metadata = False
        loader.download_video_thumbnails = False

        # Download all posts (photos and videos) from the profile
        loader.download_profile(profile, profile_pic_only=False)

        logger.info(f"Successfully downloaded profile: {username}")

    except Exception as e:
        logger.error(f"Error downloading profile '{username}': {str(e)}")
        raise


def organize_files(username: str):
    """
    Organize downloaded files into 'images' and 'videos' folders.

    Args:
        username (str): Username whose files to organize.
    """
    try:
        logger.info(f"Organizing files in: {username}")

        # Create 'images' and 'videos' folders if they don't exist
        for folder_name in ['images', 'videos']:
            folder_path = os.path.join(username, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                logger.info(f"Created directory: {folder_path}")

        # Log files before organization
        files_before = os.listdir(username)
        logger.info(f"Files found before organization: {len(files_before)}")

        # Move photos to the 'images' folder and videos to the 'videos' folder
        image_count = 0
        video_count = 0

        for filename in os.listdir(username):
            source_path = os.path.join(username, filename)

            # Skip if it's a directory
            if os.path.isdir(source_path):
                continue

            try:
                if filename.endswith((".jpg", ".png")):
                    target_path = os.path.join(username, 'images', filename)
                    os.rename(source_path, target_path)
                    image_count += 1
                    logger.debug(f"Moved image: {filename}")
                elif filename.endswith(".mp4"):
                    target_path = os.path.join(username, 'videos', filename)
                    os.rename(source_path, target_path)
                    video_count += 1
                    logger.debug(f"Moved video: {filename}")
            except Exception as e:
                logger.warning(f"Failed to move file {filename}: {e}")

        logger.info(f"Organized {image_count} images and {video_count} videos")

    except Exception as e:
        logger.error(f"Error organizing files: {str(e)}")
        raise


def cleanup(username: str):
    """
    Clean up the downloaded and processed files.

    Args:
        username (str): Username whose files to clean up.
    """
    try:
        folder = os.path.join(os.getcwd(), username)
        if os.path.exists(folder):
            # Only remove files that aren't in images or videos folders
            for item in os.listdir(folder):
                item_path = os.path.join(folder, item)
                if item not in ['images', 'videos'] and os.path.exists(item_path):
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        os.rmdir(item_path)
            logger.info(f"Cleanup completed successfully")
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        raise


def main(username: str, output_dir: Optional[Path] = None, keep_media: bool = True):
    """
    Main function to coordinate the download, organization, and cleanup process.

    Args:
        username (str): Instagram username to download.
        output_dir (Path, optional): Custom output directory.
        keep_media (bool): If True, preserve media files after cleanup.
    """
    try:
        profile_dir = download_profile(username, output_dir)
        stats = organize_files(profile_dir)
        cleanup(profile_dir, keep_media)

        logger.info(f"Process completed successfully for {username}")
        logger.info(
            f"Downloaded and organized {stats['images']} images and {stats['videos']} videos")

    except Exception as e:
        logger.error(f"Process failed: {str(e)}")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Download and organize Instagram profile content")
    parser.add_argument("username", help="Instagram username to download")
    parser.add_argument("--output-dir", type=Path,
                        help="Custom output directory")
    parser.add_argument("--keep-media", action="store_true",
                        help="Keep media files after cleanup")

    args = parser.parse_args()
    main(args.username, args.output_dir, args.keep_media)
