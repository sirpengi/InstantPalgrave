# InstantPalgrave
Instant Palgrave, the free open-source digital assistant who's ready to help even offline

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
* Fourth: create an app, set the redirect_uri to https://kaiete.uk/InstantPalgrave/spotify/done
* Fifth: put credentials into settings.ini (these will never be shared with anyone else, ever. Never enter your Spotify password here.)
* Sixth: launch Palgrave and say \`enable music\`
* Palgrave will guide you through the steps.

*Deezer support coming soon.*

If you are using "what's the weather":
* First: go to settings.ini and set `city` to your city.

If you are helping with the development:
* First: go to settings.ini and set `debug` to `on`.

## Trouble with pyaudio

In fedora I had to `dnf install portaudio-devel`. Ubuntu users might need `portaudio19-dev`

# Important!
Palgrave does not work with Windows yet - why? No idea, but just use Ubuntu / Fedora instead, it's easier (you might be able to run palgrave in an ubuntu20.04 wsl thingy, IDK). If you really want palgrave and you don't want Linux (for some odd reason) here you go https://gitlab.com/kaiete/palgrave-txt
