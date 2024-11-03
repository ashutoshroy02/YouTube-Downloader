import os
import streamlit as st
from pytube import YouTube, Playlist

# Function to download videos from a playlist
def download_playlist_videos(playlist_link, save_path, start_episode, end_episode):
    playlist = Playlist(playlist_link)
    playlist_links = list(playlist.video_urls)
    num_videos = min(len(playlist_links), end_episode)
    st.write(f"Downloading episodes {start_episode} to {num_videos} from the playlist...")
    
    for i in range(start_episode-1, num_videos):
        link = playlist_links[i]
        yt = YouTube(link)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        title = yt.title
        video.download(save_path)
        st.write(f"Episode {i+1}: {title} - Downloaded.")

# Streamlit app
def main():
    st.title("YouTube Playlist Downloader")
    st.write("Enter the YouTube playlist link, choose the range of episodes to download, and specify where to save the videos.")

    # Input fields
    playlist_link = st.text_input("Enter the playlist link:")
    start_episode = st.number_input("Enter the start episode:", min_value=1, step=1)
    end_episode = st.number_input("Enter the end episode:", min_value=start_episode, step=1)
    default_download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    save_path = st.text_input("Enter the path to save the videos:", default_download_dir)

    # Download button
    if st.button("Download Videos"):
        if playlist_link and save_path:
            download_playlist_videos(playlist_link, save_path, start_episode, end_episode)
            st.write("Download completed.")
        else:
            st.write("Please provide both playlist link and save path.")

if __name__ == "__main__":
    main()
