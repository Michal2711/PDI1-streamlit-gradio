import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import lyricsgenius
from PIL import Image

api_key = "AIzaSyBaXW__PIdpuKWulbgsIuA2RubJBO3ZENo"
youtube = build('youtube', 'v3', developerKey=api_key)


def get_video_link(video_title):

    if video_title == "":
        return None, None

    request = youtube.search().list(
            q=video_title + " audio",
            type="video",
            part="id,snippet",
            maxResults=1,
            videoCategoryId=10  # category music
        )
    response = request.execute()

    video_id = response['items'][0]['id']['videoId']
    video_link = f"https://www.youtube.com/watch?v={video_id}"
    return video_link, response


def get_song_text(song_name):
    genius = lyricsgenius.Genius("DPUxSBz63Zv8gMbb0ju3AJq8G1jffaynHs-ctPzIsR3H12nVIPPKLZeQPPl6GNlC")
    song = genius.search_song(song_name)
    return song if song else None


def main():

    hide_default_format = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """

    logo = Image.open('content/note.png')
    st.set_page_config(layout="wide", page_title="Music+lyrics", page_icon=logo)

    st.title("Search for music and lyrics")
    st.markdown(hide_default_format, unsafe_allow_html=True)

    st.sidebar.markdown("# Searching for music ")

    video_title = st.text_input("Song:", key="name")
    st.session_state.name

    song_lyrics = None

    left_column, right_column = st.columns(2)

    with left_column:
        if st.button("Szukaj"):
            st.session_state.search_component = True
            if "lyrics" in st.session_state:
                st.session_state.lyrics = False
                song_lyrics.lyrics = False

        if "search_component" in st.session_state:
            try:
                video_link, search_response = get_video_link(video_title)
                if video_link is not None and search_response.get("items"):
                    st.write(f"URL to youtube: {video_link}")
                    video_id = search_response["items"][0]["id"]["videoId"]
                    st.video(f"https://www.youtube.com/watch?v={video_id}")
                else:
                    st.error(f"Song {video_title} not found")
            except HttpError as error:
                st.error(f"Error: {error}")

    with right_column:
        if st.button("Show lyrics"):
            st.session_state.lyrics = True

        if "lyrics" in st.session_state:
            song_lyrics = get_song_text(video_title)

            if song_lyrics is None:
                st.error("Lyrics not found")
            else:
                st.write("Lyrics:")
                st.write(song_lyrics.lyrics)


if __name__ == "__main__":
    main()
