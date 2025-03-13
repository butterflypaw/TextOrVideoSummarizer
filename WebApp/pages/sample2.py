import os
import streamlit as st
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]



def main():
    channelMail = st.text_input("Enter channel mail")
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "desktop.json"

    # Get credentials and create an API client
    if(st.button("Enter")):
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_local_server(port=0)
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            forHandle=channelMail
        )
        response = request.execute()
        channelID = response["items"][0]["id"]
        request = youtube.search().list(
            part="snippet",
            channelId=channelID,
            maxResults=1,
            order="date"
        )
        response = request.execute()
        st.write(response["items"][0]["id"]["videoId"]);
        print(response["items"][0]["id"]["videoId"])

if __name__ == "__main__":
    main()
