from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import urllib.parse as p
import re
import os
import pickle

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def youtube_authenticate():
	os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
	api_service_name = "youtube"
	api_version = "v3"
	client_secrets_file = "credentials.json"
	creds = None
	# the file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first time
	if os.path.exists("token.pickle"):
		with open("token.pickle", "rb") as token:
			creds = pickle.load(token)
	# if there are no (valid) credentials availablle, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
			creds = flow.run_local_server(port=0)
			# save the credentials for the next run
			with open("token.pickle", "wb") as token:
				pickle.dump(creds, token)

	return build(api_service_name, api_version, credentials=creds)

def get_video_details(youtube, **kwargs):
	return youtube.videos().list(
		part="snippet,contentDetails,statistics",
		chart="mostPopular",
		**kwargs
	).execute()

def print_video_infos(video_response):
	for items in video_response.get("items"):
		# get the snippet, statistics & content details from the video response
		snippet         = items["snippet"]
		statistics      = items["statistics"]
		content_details = items["contentDetails"]
		# get infos from the snippet
		channel_title = snippet["channelTitle"]
		title         = snippet["title"]
		description   = snippet["description"]
		publish_time  = snippet["publishedAt"]
		# get stats infos
		comment_count = statistics["commentCount"]
		like_count    = statistics["likeCount"]
		dislike_count = statistics["dislikeCount"]
		view_count    = statistics["viewCount"]
		# get duration from content details
		duration = content_details["duration"]
		print(f"""\
			Title: {title}
			Description: {description}
			Channel Title: {channel_title}
			Publish time: {publish_time}
			Duration: {duration}
			Number of comments: {comment_count}
			Number of likes: {like_count}
			Number of dislikes: {dislike_count}
			Number of views: {view_count}
			""")
		print("----------------------------------------------------------------------");

if __name__ == '__main__':
	# authenticate to YouTube API
	youtube = youtube_authenticate()
	# loop through result pages
	next_token = None
	while True:
		# make API call to get video info
		response = get_video_details(youtube, pageToken=next_token)
		# print extracted video infos
		print_video_infos(response)
		# get next result page
		next_token = response.get("nextPageToken")
		if not next_token:
			break