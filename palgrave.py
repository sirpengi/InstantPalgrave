import platform
import os
import time
x = platform.system()
if not x == "Linux" and not x == "Darwin":
	print("Eeek! Looks like your OS isn't compatible with InstantPalgrave. Try Linux.")
	quit()
elif x == "Darwin":
	print("You're using a iMac. InstantPalgrave won't run there, sorry! Try Linux.")
	quit()
if os.environ.get("perl") == "yes":
	print("perl? ok")
	os.system("perl palgrave.pl")
	print("you want perl, you get perl")
	print("adios, python")
	time.sleep(1)
	print("""Traceback (most recent call last):
  File "palgrave.py", line 17, in <module>
    raise Exception()
Exception
""")
	print("""Traceback (most recent call last):
  File "palgrave.py", line 22, in <module>
    raise IOError()
OSError
""")
	print("""Traceback (most recent call last):
  File "palgrave.py", line 17, in <module>
    raise Exception()
Exception

Traceback (most recent call last):
  File "palgrave.py", line 22, in <module>
    raise IOError()
OSError

Traceback (most recent call last):
  File "palgrave.py", line 27, in <module>
    raise ImportError()
ImportError
""")
	raise EOFError()
	raise NameError()
	raise NotADirectoryError()
	raise KeyboardInterrupt()
import configparser
import json
from pathlib import Path
import random
import sys
import time
import requests
import webbrowser
import urllib.parse
import datetime
from playsound import playsound
import subprocess

import pyaudio
import spotipy
import sounddevice
import vosk
import os
import dateparser.search

# Make sure that palgrave command exists
if not os.path.exists(os.environ.get("HOME") + "/.local/bin/palgrave"):
	print("\033[31m" + "Hmmm, looks like you haven't got the palgrave command. It's being installed for your convenience." + "\033[0m")
	x = open(os.environ.get("HOME") + "/.local/bin/palgrave","w")
	print("hi",end="")
	x.write("#!/bin/bash\npython3 " + os.environ.get("HOME") + "/InstantPalgrave/palgrave.py $1\n")
	print("#",end="")
	x.close()
	print("#",end="")
	time.sleep(.6)
	os.system("chmod +x $HOME/.local/share/palgrave")
	print("#]")
	print("Done!\nYou can now just type `palgrave` into your terminal to launch palgrave!")
MODEL = "vosk-model-small-en-us-0.15"
AUDIO_BITRATE = 44100
AUDIO_BUFFER = 1024

ENABLE_VOSK_DEBUG = False


class SpeakOutput():
	def __init__(self):
		# requires that you install pyttsx3
		try:
			import pyttsx3
		except ImportError:
			raise Exception("Please pip install pyttsx3")
		engine = pyttsx3.init()
		engine.setProperty("rate", 130) # words per minute
		engine.setProperty("volume", 1.0)
		#voices = engine.getProperty("voices")
		#for i, voice in enumerate(voices):
		#	print("{}: age: {} gender: {} id: {} languages: {} name: {}".format(
		#		i,
		#		voice.age,
		#		voice.gender,
		#		voice.id,
		#		voice.languages,
		#		voice.name,
		#	))
		engine.setProperty("voice", "english-north")
		self.engine = engine

	def callback_output_text(self, text):
		self.engine.say(text)
		self.engine.runAndWait()


class PrintOutput():
	def __init__(self):
		pass

	def callback_output_text(self, text):
		print(text)


class BaseRobot():
	def __init__(self, config, output):
		self.config = config
		self.output = output
		self.setup()

	def setup(self):
		pass

	def respond(self, text):
		self.output.callback_output_text(text)

	def callback_receive_tick(self, t):
		pass


class EchoImplementation(BaseRobot):
	"""
	Annoying bot that just repeats what you say.
	"""
	def callback_receive_text(self, text):
		self.respond(text)


class ReverseImplementation(BaseRobot):
	"""
	Bot that reverses what it hears:
	"Hi how are you" -> "you are how hi"
	"""
	def callback_receive_text(self, text):
		words = text.split()
		reversed_words = " ".join(reversed(words))
		self.respond(reversed_words)


class BackwardsImplementation(BaseRobot):
	"""
	Bot that repeats you but backwards:
	"Hi how are you" -> "uoy era woh ih"
	"""
	def callback_receive_text(self, text):
		self.respond(text[::-1])


class PalgraveImplementation(BaseRobot):
	"""
	The best bot
	"""

	def setup(self):
		self.mode = None
		self.spotify_enabled = False
		self.spotify_token = None
		self.last = None
		self.timers = set()

	def enable_spotify(self):
		if self.spotify_enabled:
			self.respond("Already enabled")
			return
		scopes = [
			"user-read-playback-state",
			"user-modify-playback-state",
			"user-read-currently-playing",
			"user-library-read",
		]
		token = spotipy.util.prompt_for_user_token(
			username = self.config["SPOTIFY_USERNAME"],
			client_id = self.config["SPOTIFY_CLIENT_ID"],
			client_secret = self.config["SPOTIFY_CLIENT_SECRET"],
			redirect_uri = self.config["SPOTIFY_REDIRECT_URI"],
			scope = " ".join(scopes),
		)
		self.spotify_token = token
		self.spotify_enabled = True
		self.respond("Music enabled")

	def get_spotify_currently_playing(self):
		if not self.spotify_enabled:
			self.respond("Music mode is not enabled")
			return
		spotify = spotipy.Spotify(auth=self.spotify_token)
		track = spotify.current_user_playing_track()
		# print(json.dumps(track, sory_keys=True, indent=4))
		artist = track["item"]["artists"][0]["name"]
		trackname = track["item"]["name"]
		self.respond("Currently playing {} by {}".format(
			trackname,
			artist,
		))

	def unpause_spotify(self):
		if not self.spotify_enabled:
			self.respond("Music mode is not enabled")
			return
		spotify = spotipy.Spotify(auth=self.spotify_token)
		spotify.start_playback()

	def pause_spotify(self):
		if not self.spotify_enabled:
			self.respond("Music mode is not enabled")
			return
		spotify = spotipy.Spotify(auth=self.spotify_token)
		spotify.pause_playback()
		self.respond("Paused")

	def handle_set_timer(self, inp):
		_, rest = inp.split("timer")
		found_dates = dateparser.search.search_dates(rest, settings={"PREFER_DATES_FROM": "future"})
		if not found_dates:
			self.respond("Could not determine a date from your command")
		else:
			found_input, found_date = found_dates[0]
			now = datetime.datetime.now()
			offset = found_date - now
			if offset < datetime.timedelta(0):
				self.respond("Can not set a timer in the past")
			else:
				self.respond("Timer set for {}".format(found_input))
				self.timers.add(found_date)

	def callback_receive_tick(self, t):
		now = datetime.datetime.now()
		do_alarm = False
		for timer in list(self.timers):
			if now >= timer:
				do_alarm = True
				self.timers.remove(timer)
		if do_alarm:
			playsound("alarm.wav")

	def callback_receive_text(self, text):
		text = text.replace("how grave","palgrave").replace("paul grave","palgrave").replace("how grave","palgrave")
		if self.mode == "awaitingSearch":
			webbrowser.open("https://duckduckgo.com/?q=" + urllib.parse.quote(text))
			self.respond("Opening web browser")
			self.mode = None
			return
		if self.mode == "awaitingNote":
			notes = open("palgravenotes","a")
			notes.write(text + ".\n")
			self.respond("Note saved successfully!")
			self.mode = None
			return
		if self.mode == "conversation1":
			if "ok" in text or "good" in text or "fine" in text or "brilliant" in text or "derp" in text or "happy" in text:
				self.respond("Good to hear you're feeling well. What have you been doing lately?")
				self.mode = "conversation2"
				return
			elif "bad" in text or "not ok" in text or "terrible" in text or "sad" in text:
				self.respond("Oh, that's not good. Hope you feel better soon, and in the meantime if there's anything I can do to help, just ask!")
				self.mode = None
				return
			else:
				self.respond("OK! What have you been doing, anything fun?")
				self.mode = "conversation2"
				return
		if self.mode == "conversation2":
			if "fun" in text or "good" in text or "nice" in text or "happy" in text or "exciting" in text:
				self.respond("That sounds super fun! I wish I could have done that too, but I suppose that's the disadvantage of living in a computer.")
				self.respond("Well, I'd better go and help some other people now. If there's anything I can do, just ask!")
				self.mode = None
				return
			elif "boring" in text or "bad" in text or "sad" in text or "not fun" in text:
				self.respond("Oh dear, that doesn't sound good. I hope you're happy though, because your feelings are my feelings so if you're feeling sad, I feel sad, and I don't want anyone to be sad.")
				self.respond("If I can help or cheer you up, just ask. Bye for now!")
				self.mode = None
				return
			else:
				self.respond("Ok! anything I can do for you, just ask, I'll always be there. Bye for now!")
				self.mode = None
				return
		if self.mode == "palgraveAnswers":
			y = requests.post("https://palgrave-answers.kaiete.workers.dev", data=text)
			y = y.text
			if not y == "Wolfram|Alpha did not understand your input":
				self.respond("According to Wolfram Alpha, " + y)
			else:
				self.respond("Hmmm, I'm not sure about that. Sorry.")
			self.mode = None
			return

		if text == "palgrave":
			self.respond("Hello!")
		if "enable" in text and "music" in text:
			self.enable_spotify()
		if text == "what is playing":
			self.get_spotify_currently_playing()
		if text == "stop music":
			self.pause_spotify()
		if "spotify" in text and "pause" in text:
			self.pause_spotify()
		if text == "continue music":
			self.unpause_spotify()
		if "i" in text and "bored" in text and not "not" in text:
			randomnumber = random.random()
			if randomnumber < 0.5:
				self.respond("Do a jigsaw")
			else:
				self.respond("Listen to music")
		if "exit" in text or "quit" in text or "goodbye" in text or "bye" in text or "see you later" in text and not "don't" in text and not "do not" in text:
			self.respond("Goodbye! See you later")
			time.sleep(2)
			quit()
		if "get" in text and "hypertext" in text:
			self.respond("Please type a URL")
			getURL = input("URL: ")
			getresponse = requests.get(getURL)
			print("Response: ")
			print(getresponse)
			print(getresponse.text)
			self.respond("Do you want to open this url in your web browser? Type y or n")
			openInWebbrowser = input("Open in web browser? y/n")
			if openInWebbrowser == "y":
				webbrowser.open(getURL)
			elif openInWebbrowser == "n":
				self.respond("OK")
			else:
				self.respond("I didn't receive y or n, so I didn't open the browser")
		if "thanks" in text or "thank you" in text:
			self.respond("No problem")
		if "search" in text:
			self.respond("What would you like to search?")
			self.mode = "awaitingSearch"
			return
		if "what" in text and "you" in text and "do" in text:
			self.respond("I can do many things.")
			x = random.random()
			if x < 0.5:
				time.sleep(0.6)
				self.respond("You can say, open website or search")
			elif x > 0.5:
				time.sleep(0.6)
				self.respond("You can say, thanks or i'm bored")
			else:
				self.respond("Sorry, an error occurred at line 293 (IP-ERROR: Unexpected number neither below zero point five, nor above zero point five. Could be zero point five causing the error.) I will send you to an error reporting link.")
				webbrowser.open("https://github.com/kaiete/InstantPalgrave/issues")
		if "open" in text and "website" in text:
			self.respond("Please type a URL")
			webbrowser.open(input("URL: "))
		if "note" in text and "save" in text:
			self.respond("Please say a note")
			self.mode = "awaitingNote"
			return
		if "date" in text and "what" in text:
			self.respond("The date today is " + str(datetime.date.today().strftime("%A the %d of %B, %Y")))
		if "time" in text and "what" in text:
			self.respond("The time is " + str(datetime.datetime.now().strftime("%H %M")))
		if "note" in text and "get" in text or "note" in text and "what" in text:
			self.respond("Your note is: . " + open("palgravenotes","r").read())
		if "google" in text and "auth" in text:
			webbrowser.open("https://kaiete.uk/InstantPalgrave/authbygoogle")
		if "what" in text and "i" in text and "said" in text or "what" in text and "i" in text and "say" in text:
			if not self.last == None:
				self.respond("You just said" + self.last)
			else:
				self.respond("I don't know what you just said, or this is the beginning of our conversation.")
		if "set" in text and "timer" in text:
			self.handle_set_timer(text)
			return
		if "hello" in text and "palgrave" in text:
			self.respond("Hello! How are you today?")
			self.mode = "conversation1"
			return
		if "roll" in text and "dice" in text and not "some" in text:
			self.respond("The correct term is, 'to roll a die', because dice is the plural and die is the singular, but I'll do it anyway.")
			self.respond("The outcome was " + str(random.randint(1,6)))
		if "roll" in text and "die" in text:
			self.respond("The outcome was " + str(random.randint(1,6)))
		if "what" in text and "weather" in text:
			city = self.config["city"]
			if self.config["debug"] == "on":
				print("city: {}".format(city))
			weatherapiurl = "https://palgrave-weather.kaiete.workers.dev"
			weather = requests.post(weatherapiurl,data=city)
			if self.config["debug"] == "on":
				print("response: {}".format(weather.text))
			weather = weather.text
			weather = json.loads(weather)
			weather = weather["current"]["condition"]["text"]
			self.respond("The weather is currently {}".format(weather))
			if "what" in text and "lyrics" in text:
				if not self.spotify_enabled:
					self.respond("Music mode is not enabled. Please say, 'enable music'.")
					return
				self.respond("Ok, looking for this song's lyrics on duckduckgo")
				spotify = spotipy.Spotify(auth=self.spotify_token)
				track = spotify.current_user_playing_track()
				trackname = track["item"]["name"]
				artist = track["item"]["artists"][0]["name"]
				webbrowser.open("https://duck.com/?q=lyrics%20{}%20{}".format(urllib.parse.quote(trackname),urllib.parse.quote(artist)))
		if "force" in text and "close" in text:
			print("palgrave: Exception: manually initiated crash!")
			print("exiting with error code MICV-{}\nplease DO NOT report this crash, it's not our fault\nYou were the one who said force close.".format(datetime.datetime.now()))
			x = open(".log","a")
			x.write("\nManually initiated crash, timestamp {}\n".format(datetime.datetime.now()))
			x.close()
			print("Logged, closing")
			quit(1)

# Wolfram|Aplha is not endorsed in any way by InstantPalgrave, and Wolfram|Alpha has not sponsored or endorsed this integration. I just thought it would be a good idea.
		if "hey palgrave" in text or "ok palgrave" in text:
			x = text
			x = x.replace("hey palgrave","").replace("ok palgrave","")
			if x == "":
				self.mode = "palgraveAnswers"
				self.respond("Hello! Ask me anything")
				return
			else:
				y = requests.post("https://palgrave-answers.kaiete.workers.dev", data=x)
				y = y.text
				if not y == "Wolfram|Alpha did not understand your input":
					self.respond("According to Wolfram Alpha, " + y)
				else:
					self.respond("Hmmm, I'm not sure about that. Sorry.")
		if "my day" in text:
			self.respond("Hey there! Here's the lowdown.")
			x = requests.post("https://palgrave-weather.kaiete.workers.dev",data=self.config["city"]).text
			x = json.loads(x)["current"]["condition"]["text"]
			# Not gonna do time.sleep for a pause in speech here, internet delay will do that for me
			self.respond("First, outside in {} it looks {}".format(self.config["city"],x))
			time.sleep(.6)
			self.respond("The time right now is " + str(datetime.datetime.now().strftime("%H %M")))#can you see where I got that snippet
			time.sleep(.6)
			self.respond("The date today is " + str(datetime.date.today().strftime("%A the %d of %B, %Y")))
			time.sleep(.6)
			y = open("palgravenotes")
			self.respond("Here's your notes: {}".format(y.read()))
			y.close()
			time.sleep(.6)
			self.respond("That's all for now. See you later!")
		with open("commands.json") as commands:
			commands = json.loads(commands.read())
			if commands["enabled"] == "true":
				x = commands["commands"]["list"][0]
				if commands["commands"][x]["wakeWord"] == text:
					exec(commands["commands"][x]["execute"])
					self.respond(commands["commands"][x]["response"])
		

		self.last = text


def get_recognizer(model):
	if not Path(model).exists():
		raise Exception("Model {} doesn't exist, maybe download it from: https://alphacephei.com/vosk/models and unzip it here".format(MODEL))
	if not ENABLE_VOSK_DEBUG:
		vosk.SetLogLevel(-1)
	vosk_model = vosk.Model(model)
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


def main(bot_mode):
	cp = configparser.ConfigParser()
	cp.read("settings.ini")
	config = cp["palgrave"]
	recognizer = get_recognizer(config["VOSK_MODEL"])
	stream = get_audio_stream()
	#output = PrintOutput()
	output = SpeakOutput()
	if bot_mode == "palgrave":
		robot = PalgraveImplementation(config=config, output=output)
	elif bot_mode == "echo":
		robot = EchoImplementation(config=config, output=output)
	elif bot_mode == "reverse":
		robot = ReverseImplementation(config=config, output=output)
	elif bot_mode == "backwards":
		robot = BackwardsImplementation(config=config, output=output)
	else:
		raise Exception("Unknown bot mode: {}".format(bot_mode))
	while 1:
		robot.callback_receive_tick(time.time())
		data = stream.read(AUDIO_BUFFER)
		if recognizer.AcceptWaveform(data):
			raw_result = recognizer.Result()
			result = json.loads(raw_result)
			text = result.get("text")
			if text:
				if not text == "huh":
					text = text.replace("how grave","palgrave").replace("paul grave","palgrave").replace("how grave","palgrave")
					print("I heard '{}'".format(text))
				stream.stop_stream()
				robot.callback_receive_text(text)
				stream.start_stream()


if __name__ == "__main__":
	if len(sys.argv) > 1:
		bot_mode = sys.argv[1]
	else:
		bot_mode = "palgrave"
	main(bot_mode)
