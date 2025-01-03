from flask import Flask, request, jsonify
import os
import re
import json
from googleapiclient.discovery import build
from datetime import timedelta
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
@app.route('/api/duration', methods=['POST'])
def get_playlist_duration():
    link = request.get_json()

    # regular expression for getting playlist id from the youtube link.
    playlist_pattern = re.compile(r'^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?.*?(?:v|list)=(.*?)(?:&|$)|^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?(?:(?!=).)*\/(.*)$')

    # searching for playlist id in the playlist link data with the help of regular expressions.
    playlist_link = playlist_pattern.search(link['link'])

    # taking the playlist id data.
    playlist_link = playlist_link.group(1)

    # api key
    api_key = os.getenv('API_KEY')

    # getting youtube api with proper version using build.
    youtube = build('youtube', 'v3', developerKey=api_key)

    # nextPageToken for getting playlists having more than 50 videos( for pagination)
    nextPageToken = None

    # regular expression for getting hours, minutes and seconds from the API Data of Duration
    hours_pattern = re.compile(r'(\d+)H')
    minutes_pattern = re.compile(r'(\d+)M')
    seconds_pattern = re.compile(r'(\d+)S')

    # variable for keeping the count of total number of seconds of the playlist.
    total_seconds = 0

    # while loop which does api calls till we get the durations of all the videos in the playlist.
    while True:
        # API request to get the details of the playlist.
        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId= playlist_link,
            maxResults=50,
            pageToken=nextPageToken
        )

        # executing the playlistItems request to get the response from the API.
        pl_response = pl_request.execute()

        # list which stores the video ids of all the videos of the playlist
        vid_ids = []

        # for loop to get the video ids in the vid_ids list.
        for item in pl_response['items']:
            vid_ids.append(item['contentDetails']['videoId'])

        # API request to get the details about the videos.
        vid_requests = youtube.videos().list(
            part='contentDetails',
            id=','.join(vid_ids)
        )

        # executing the videos request to get the response from the API.
        vid_response = vid_requests.execute()

        # for loop to calculate the total duration of all the videos
        for item in vid_response['items']:
            duration = item['contentDetails'].get('duration', 'PT0H0M0S')

            # searching for the hours, minutes and seconds in the duration data with the help of regular expressions.
            hours = hours_pattern.search(duration)
            minutes = minutes_pattern.search(duration)
            seconds = seconds_pattern.search(duration)

            # assigning hours, minutes and seconds variable to int and if it is not in the duration data then assigning it to zero value.
            hours = int(hours.group(1)) if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            seconds = int(seconds.group(1)) if seconds else 0

            # using timedelta function to convert hours, minutes and seconds into total seconds duration of the video.
            video_seconds = timedelta(
                hours = hours,
                minutes = minutes,
                seconds = seconds
            ).total_seconds()

            # adding video seconds to get the total duration of playlist in seconds.
            total_seconds += video_seconds

        # getting the nextPageToken to see if there are more videos in the playlist.
        nextPageToken = pl_response.get('nextPageToken')

        # checking if there are more videos to get from the playlist.
        if not nextPageToken:
            break

    # calculating hours, minutes and seconds from the total_seconds.
    total_seconds = int(total_seconds)

    minutes, seconds = divmod(total_seconds, 60)

    hours, minutes = divmod(minutes, 60)

    duration = str(hours)+':'+str(minutes)+':'+str(seconds)

    print(duration)

    return duration

if __name__ == '__main__':
    app.run(debug=True)
