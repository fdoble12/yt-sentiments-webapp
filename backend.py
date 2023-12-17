from flask import Flask, request, jsonify, Response
import analyzer
import pandas as pd
from flask_cors import CORS
import csv
from io import StringIO

app = Flask(__name__)
CORS(app)

classifier = analyzer.yt_classifier()

@app.route('/analyze', methods=['POST'])
def analyze_video():
    try:
        # Get the video URL from the request's JSON data
        data = request.json
        video_url = data.get('video_url')

        if not video_url:
            return jsonify({'error': 'Invalid input: video_url is required'}), 400

        # Process and classify comments for the video
        df, word_frequencies, pos_freq, neg_freq = classifier.process_and_classify_comments(video_url)

        # Calculate and send the counts in the response
        video_title = classifier.get_vid_details(video_url)
        total_comments = len(df)
        total_positive_comments = len(df[df['Sentiment'] == 'pos'])
        total_negative_comments = len(df[df['Sentiment'] == 'neg'])

        response_data = {
            'total_comments': total_comments,
            'total_positive_comments': total_positive_comments,
            'total_negative_comments': total_negative_comments,
            'video_title': video_title,
            'word_cloud_data': word_frequencies,
            'pos_word_cloud': pos_freq,
            'neg_word_cloud': neg_freq
        }

        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/download-csv', methods=['POST'])
def download_csv():
    try:
        # Get the video URL from the request's JSON data
        data = request.json
        video_url = data.get('video_url')

        if not video_url:
            return jsonify({'error': 'Invalid input: video_url is required'}), 400

        # Process and classify comments for the video
        df = classifier.process_and_classify_comments(video_url)

        # Create a CSV file in memory
        csv_data = StringIO()
        df.to_csv(csv_data, index=False)

        # Return the CSV file as a downloadable response
        response = Response(csv_data.getvalue(), content_type='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=classified_comments.csv'

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
