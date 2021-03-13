import json
from pathlib import Path

import pyaudio
import vosk

MODEL = "vosk-model-small-en-us-0.15"
AUDIO_BITRATE = 44100
AUDIO_BUFFER = 1024


class PalgraveImplementation():
	def __init__(self):
		pass

	def callback_receive_text(self, text):
		print("I heard: {}".format(text))


def get_recognizer():
	if not Path(MODEL).exists():
		raise Exception("Model {} doesn't exist, maybe download it from: https://alphacephei.com/vosk/models and unzip it here".format(MODEL))
	vosk_model = vosk.Model(MODEL)
	rec = vosk.KaldiRecognizer(vosk_model, AUDIO_BITRATE)
	return rec


def get_audio_stream():
	audio = pyaudio.PyAudio()
	stream = audio.open(
		format = pyaudio.paInt16,
		channels = 1,
		rate = AUDIO_BITRATE,
		input = True,
		frames_per_buffer = AUDIO_BUFFER,
	)
	return stream
	

def main():
	recognizer = get_recognizer()
	stream = get_audio_stream()
	robot = PalgraveImplementation()
	while 1:
		data = stream.read(AUDIO_BUFFER)
		if recognizer.AcceptWaveform(data):
			raw_result = recognizer.Result()
			result = json.loads(raw_result)
			text = result.get("text")
			if text:
				robot.callback_receive_text(text)


if __name__ == "__main__":
	main()
