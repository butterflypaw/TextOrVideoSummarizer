# TextOrVideoSummarizer-G18-PS24
This repository is dedicated to the project ***Text/Video Summarizer***.
### Project Overview:
This tool summarizes the data provided by the user. The data can be in the form of documents or a video file or a blog link or an YouTube URL. The app is capable of running in the background enabling the push notifications whenever a new video is uploaded to the provided youtube channels. 

### Steps to be followed for using the code:
**Step 1** : Clone the repository in your desired directory. The following command can be used: 
```
git clone https://github.com/kmitofficial/TextOrVideoSummarizer-G18-PS24.git
```
**Step 2** : Install all the required libraries in the _Webapp_ directory using the command below: 
```
pip install -r requirements.txt
```
**Step 3** : Create a new file named *.env* in the same directory.  
**Step 4** : Add your *Gemini API key* in the *.env* as shown below.  
```
"API_KEY" = "your_api_key"
```
A Gemini API key can be created [here](https://aistudio.google.com/app/apikey).  
**Step 5** : Finally, run the application using the below command.  
```
cd ./WebApp
streamlit run app.py
```
Now, you are ready to use our web application.  
Upload _documents_ or _youtube links_ or _blog links_, and get your short and crisp summary.
