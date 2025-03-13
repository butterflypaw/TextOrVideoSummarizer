import os
import streamlit as st
import googleapiclient.discovery
import googleapiclient.errors

def main():
    api_key = ""  # Replace with your API key
    channelMail = st.text_input("Enter channel mail")

    api_service_name = "youtube"
    api_version = "v3"

    # Create an API client
    if st.button("Enter"):
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=api_key)

        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            forHandle=channelMail  
        )
        response = request.execute()
        
        if "items" in response and len(response["items"]) > 0:
            channelID = response["items"][0]["id"]
            request = youtube.search().list(
                part="snippet",
                channelId=channelID,
                maxResults=1,
                order="date"
            )
            response = request.execute()
            st.write(response["items"][0]["id"]["videoId"])
            print(response["items"][0]["id"]["videoId"])
        else:
            st.write("No channel found for the provided email.")

if __name__ == "__main__":
    main()
