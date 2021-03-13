import pyaudio
import vosk

MODEL = "vosk-model-small-en-us-0.15"
AUDIO_BITRATE = 44100
AUDIO_BUFFER = 1024


def main():
	vosk_model = vosk.Model(MODEL)
	rec = vosk.KaldiRecognizer(vosk_model, AUDIO_BITRATE)
	audio = pyaudio.PyAudio()
	stream = audio.open(
		format = pyaudio.paInt16,
		channels = 2,
		rate = AUDIO_BITRATE,
		input = True,
		frames_per_buffer = AUDIO_BUFFER,
	)
	while 1:
		data = stream.read(AUDIO_BUFFER)
		if rec.AcceptWaveform(data):
			print(rec.Result())
		else:
			print(rec.PartialResult())


if __name__ == "__main__":
	main()