from flask import Flask, send_from_directory, render_template
from contextlib import closing
import boto3
import os


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/vai/<text>')
def hello_world(text):
    client = boto3.client(
        'polly',
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
    )

    response = client.synthesize_speech(
        OutputFormat='mp3',
        Text=text,
        VoiceId='Ricardo'
    )

    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            data = stream.read()
            fo = open("result.mp3", "wb")
            fo.write(data)
            fo.close()

    return send_from_directory(directory='.', filename='result.mp3')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
