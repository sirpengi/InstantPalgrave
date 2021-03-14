# InstantPalgrave
Instant Palgrave, the open-source digital assistant


## Setup dev

Create a python3(.8??) vitualenv and then:

```console
pip install -r requirements.txt
```

Grab the english model file from http://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip and unzip it here

and then run:

```console
python palgrave.py
```


## Trouble with pyaudio

In fedora I had to `dnf install portaudio-devel`. Ubuntu users might need `portaudio19-dev`
