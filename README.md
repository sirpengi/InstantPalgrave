# InstantPalgrave
Instant Palgrave, the open-source digital assistant

## Setup dev

Create a python3(.8??) virtualenv and then:

```console
pip install -r requirements.txt
```

and then:

```console
python3 palgrave.py
```

There are other bot modes you can run by specifying the bot implementation:

```console
python3 palgrave.py backwards
```

Supported implementations are `palgrave` (default, if you left blank), `echo`, `reverse`, and `backwards`.

If you are not going to use Spotify, this is all you need.

If you are using Spotify:
* First: You need Premium for it to work
* Second: go to https://developer.spotify.com
* Third: tap Dashboard then Sign In
* Fourth: create an app, set the redirect_uri to http://kaiete.github.io/InstantPalgrave/spotify/done
* Fifth: put credentials into settings.ini
* Sixth: launch Palgrave and say \`enable music\`
* Palgrave will guide you through the steps.

## Trouble with pyaudio

In fedora I had to `dnf install portaudio-devel`. Ubuntu users might need `portaudio19-dev`

# Important!
Palgrave does not work with Windows yet - why? No idea, but just use Ubuntu / Fedora instead, it's easier
