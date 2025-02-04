import json
from functools import partial

import requests
from django.http import JsonResponse
from django.shortcuts import redirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.conf import settings


def google_login(request):
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],
        redirect_uri=settings.GOOGLE_OAUTH2_REDIRECT_URI
    )
    authorization_url, _ = flow.authorization_url(
        prompt='consent'
    )
    return JsonResponse({'auth_url': authorization_url})


def auth_callback(request):
    code = request.GET.get('code')
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],
        redirect_uri=settings.GOOGLE_OAUTH2_REDIRECT_URI
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials
    user = request.user
    user.youtubeauth.credentials = json.loads(credentials.to_json())
    user.youtubeauth.save()
    return JsonResponse({'access_token': credentials.token})


def get_videos(request):
    access_token = request.GET.get('access_token')
    youtube = build('youtube', 'v3', credentials=Credentials(token=access_token))
    request = youtube.videos().list(
        part='snippet',
        mine=True,
        maxResults=50
    )
    response = request.execute()
    return JsonResponse(response)

def get_comments(request, video_id):
    access_token = request.GET.get('access_token')
    youtube = build('youtube', 'v3', credentials=Credentials(token=access_token))
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=50
    )
    response = request.execute()
    return JsonResponse(response)


def post_comment(request, video_id):
    access_token = request.GET.get('access_token')
    youtube = build('youtube', 'v3', credentials=Credentials(token=access_token))

    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=50
    )
    response = request.execute()
    return JsonResponse(response)


def like_all_comments(request, video_id):
    access_token = request.GET.get('access_token')
    youtube = build('youtube', 'v3', credentials=Credentials(token=access_token))
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=50
    )
    response = request.execute()
    for comment in response['items']:
        comment_id = comment['id']
        request = youtube.comments().setModerationStatus(
            id=comment_id,
            moderationStatus='published'
        )
        request.execute()
    return JsonResponse({'message': 'All comments liked'})


def delete_all_comments(request, video_id):
    access_token = request.GET.get('access_token')
    youtube = build('youtube', 'v3', credentials=Credentials(token=access_token))

    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=50
    )

    bad_words = ['bad', 'ugly', 'nasty', 'mean']

    response = request.execute()
    for comment in response['items']:
        text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
        if any(word in text.lower() for word in bad_words):
            comment_id = comment['id']
            request = youtube.commentThreads().delete(
                id=comment_id
            )
            request.execute()

    return JsonResponse({'message': 'All comments deleted'})
