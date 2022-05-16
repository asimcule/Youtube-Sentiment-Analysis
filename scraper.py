# -*- coding: utf-8 -*-

# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
import googleapiclient.discovery

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "#Add your developer key"
id = "#Add the video ID"
comments_and_authors = []


youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)

request = youtube.commentThreads().list(
    part="id, snippet, replies",
    videoId=id
)

response = request.execute()

count = 0
#parsing the response
items = response["items"]
for item in items:
    count += 1
    dic = {"Author":item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"], "Comment":item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]}
    if "replies" in item.keys():
        temp=[]
        count += len(item["replies"]["comments"])
        for reply in item["replies"]["comments"]:
            temp.append({"Author":reply["snippet"]["authorDisplayName"],"Reply":reply["snippet"]["textDisplay"]})
        dic["REPLIES"]=temp
    comments_and_authors.append(dic)  

#looping through all the search results using the nextpagetoken parameter
while True:
    if "nextPageToken" in response.keys():
        token = response["nextPageToken"]
        request = youtube.commentThreads().list(
            part="id, snippet, replies",
            pageToken = token,
            videoId=id

        )
        response = request.execute()
        items = response["items"]
        count += len(items)
        for item in items:
            dic = {"Author":item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"], "Comment":item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]}
            if "replies" in item.keys():
                temp=[]
                count += len(item["replies"]["comments"])
                for reply in item["replies"]["comments"]:
                    temp.append({"Author":reply["snippet"]["authorDisplayName"],"Reply":reply["snippet"]["textDisplay"]})
                dic["REPLIES"]=temp
            comments_and_authors.append(dic)            
    else:
        break

print(comments_and_authors)
print(count)

