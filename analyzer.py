from flair.models import TextClassifier
from flair.data import Sentence
import pandas as pd
import re
from googleapiclient.discovery import build
import requests
from youtube_transcript_api import YouTubeTranscriptApi

class yt_classifier():

    def __init__(self):
        self.classifier = TextClassifier.load('en-sentiment')
        self.api = build('youtube', 'v3', developerKey="<API_KEY>")

    def clean_text(self, text):
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove non-alphabetical characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize the text (split into words)
        words = text.split()
        
        # Remove stopwords (common words like "the", "and", etc.)
        stopwords = set(["the", "and", "is", "it", "to", "i", "you", "u", "a", "in", "for", "so", "that", "when"])
        words = [word for word in words if word not in stopwords]
        
        # Remove extra whitespace
        cleaned_text = ' '.join(words)
        
        return cleaned_text

    def classify(self,text):
        if text != "":
            sentence = Sentence(text)
            self.classifier.predict(sentence)
            value = sentence.labels[0].value

            if value == "POSITIVE":
                value="pos"
            else:
                value="neg"
        else:
            value="N/A"
        return value

    def get_top_level_comments(self,video_url):
        id = self.extract_video_id(video_url)
        video_response=self.api.commentThreads().list(
                part='snippet,replies',
                videoId=id
                ).execute()
        data_list = []
        print(f"Getting comments for Video: {id}....")
        while video_response:
            for item in video_response['items']:
            # Extracting comments
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                
                data_list.append(comment)
                
            # Again repeat
            if 'nextPageToken' in video_response:
                video_response = self.api.commentThreads().list(
                        part = 'snippet,replies',
                        videoId = id,
                        pageToken = video_response['nextPageToken']
                    ).execute()
            else:
                break
        return data_list

    def process_and_classify_comments(self, video_url):
        # Get top-level comments
        comments = self.get_top_level_comments(video_url)

        # Create a list to store processed comments
        processed_comments = []

        # Process and classify each comment
        for comment_text in comments:
            cleaned_comment = self.clean_text(comment_text)
            sentiment = self.classify(cleaned_comment)
            processed_comments.append([comment_text, cleaned_comment, sentiment])

        # Create a DataFrame from the processed comments
        df = pd.DataFrame(processed_comments, columns=["Original Comment", "Cleaned Comment", "Sentiment"])

        return df
    
    def get_vid_details(self,video_url):
        video_id = self.extract_video_id(video_url)
        details = self.api.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        return details['items'][0]['snippet']['title']
    
    def extract_video_id(self,youtube_url):
        # Split the URL using "v=" as the delimiter
        parts = youtube_url.split("v=")
        
        # Check if the URL contains "v=" and has at least one more character
        if len(parts) > 1 and len(parts[1]) > 0:
            video_id = parts[1]
            
            # Check if there is an ampersand (&) in the URL and remove it along with any additional parameters
            ampersand_index = video_id.find("&")
            if ampersand_index != -1:
                video_id = video_id[:ampersand_index]
            
            return video_id
        else:
            return None
        
    def export_to_csv(df, output_file):
        df.to_csv(output_file, index=False)