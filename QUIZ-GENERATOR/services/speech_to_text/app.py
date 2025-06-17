from flask import Flask, jsonify
from google.cloud import speech
import os

app = Flask(_name_)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud.json"
AUDIO_FILE = "sample_audio.mp3"

def get_encoding(filename):
    if filename.endswith(".wav"):
        return speech.RecognitionConfig.AudioEncoding.LINEAR16
    elif filename.endswith(".flac"):
        return speech.RecognitionConfig.AudioEncoding.FLAC
    elif filename.endswith(".mp3"):
        return speech.RecognitionConfig.AudioEncoding.MP3
    elif filename.endswith(".ogg") or filename.endswith(".opus"):
        return speech.RecognitionConfig.AudioEncoding.OGG_OPUS
    else:
        raise ValueError("Unsupported audio format.")

@app.route("/transcribe", methods=["GET"])
def transcribe_audio():
    if not os.path.exists(AUDIO_FILE):
        return jsonify({"error": f"Audio file '{AUDIO_FILE}' not found."}), 404

    try:
        encoding = get_encoding(AUDIO_FILE.lower())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    with open(AUDIO_FILE, "rb") as audio_file:
        content = audio_file.read()

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
        model="video",
        use_enhanced=True,
        speech_contexts=[
            speech.SpeechContext(
                phrases=["OpenAI", "GPT", "ChatGPT", "flask", "API", "cloud"]
            )
        ],
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print("Transcription in progress...")

    response = operation.result(timeout=600)

    transcript = " ".join([result.alternatives[0].transcript for result in response.results])
    print("\n--- Transcript ---\n" + transcript)
    return jsonify({"transcript": transcript})

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5001, debug=True)