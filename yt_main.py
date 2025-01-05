from pytubefix import YouTube
import streamlit as st
import os
from tkinter import Tk, filedialog

def choose_save_location(default_filename):
    root = Tk()
    root.withdraw()  
    root.attributes("-topmost", True)  

    save_path = filedialog.asksaveasfilename(
        initialfile=default_filename,
        defaultextension=".mp4",
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
    )
    root.destroy() 
    return save_path

st.title("🎥 YOUTUBE VIDEO DOWNLOADER 🫠")

def download_video_with_progress(video_url, save_path):
    try:
        yt = YouTube(video_url)
        
        st.write(f"**Title:** {yt.title}")
        st.write(f"**Author:** {yt.author}")
        st.write(f"**Video Length:** {yt.length // 60} min {yt.length % 60} sec")
        st.image(yt.thumbnail_url, caption="Video Thumbnail", use_column_width=True)
        
        stream = yt.streams.get_highest_resolution()
        total_file_size = stream.filesize
        progress_bar = st.progress(0)

        def progress_function(stream, chunk, bytes_remaining):
            percent_complete = (total_file_size - bytes_remaining) / total_file_size
            progress_bar.progress(min(percent_complete, 1.0))

        yt.register_on_progress_callback(progress_function)

        st.write("Downloading...")
        stream.download(output_path=os.path.dirname(save_path), filename=os.path.basename(save_path))

        st.success(f"✅ Download completed: {save_path}")
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")

video_url = st.text_input("🔗 Paste YouTube Video Link Below")

if st.button("Download Video"):
    if video_url:
        yt = YouTube(video_url)
        default_filename = f"{yt.title}.mp4"
        
        save_path = choose_save_location(default_filename)
        if save_path:
            download_video_with_progress(video_url, save_path)
        else:
            st.warning("⚠️ No file location selected. Download canceled.")
    else:
        st.error("❌ Please enter a valid YouTube URL.")
