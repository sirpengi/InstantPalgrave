# InstantPalgrave
Instant Palgrave, the free open-source digital assistant who's ready to help even offline

## Setup dev

*By using Palgrave, you agree to the terms set out in terms.md, section 1 and by forking and then editing, you agree to section 2.*

Create a python3(.8??) virtualenv and then:

```bash
# You need root to install portaudio
pip install -r requirements.txt
# On Ubuntu / PiOS / anything with apt (except Termux):
apt-get install portaudio19-dev
# On Fedora
dnf install portaudio-devel
# dev or devel is for development i.e. stable I guess
```

and then:

```bash
python3 palgrave.py
```
On crostini (linux vm in chrome os) you first need to:
```bash
sudo apt install espeak alsa-utils
```
There are other bot modes you can run by specifying the bot implementation:

```bash
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
* Sixth: launch Palgrave and say 'enable music'
* Palgrave will guide you through the steps.

*Deezer support may be added later.*

If you are using "what's the weather":
* First: go to settings.ini and set `city` to your city.

If you are helping with the development:
* First: go to settings.ini and set `debug` to `on`.

***Never*** commit your personal settings.ini file.

## Making Packages with PPC

If you want to make an add-on for Palgrave, you can do so!

Find a tutorial at https://github.com/kaiete/example-palgrave-package

## Palgrave Package Center

To install packages (aka add-ons), go to the directory where you have installed Palgrave and run `./ppcinstall`. The installer will guide you throught the steps.

If something goes wrong, create an issue [here](https://github.com/kaiete/InstantPalgrave/issues).

# Important!
Palgrave does not work with Windows yet - why? No idea, but just use Ubuntu / Fedora instead, it's easier (you might be able to run palgrave in an ubuntu20.04 wsl thingy, IDK). If you really want palgrave and you don't want Linux (for some odd reason) here you go https://gitlab.com/kaiete/palgrave-txt

<hr>

<script type="text/javascript">
  (function(d, t) {
      var v = d.createElement(t), s = d.getElementsByTagName(t)[0];
      v.onload = function() {
        window.voiceflow.chat.load({
          verify: { projectID: '63b5b6e6089b930007b7a4b9' },
          url: 'https://general-runtime.voiceflow.com',
          versionID: 'production'
        });
      }
      v.src = "https://cdn.voiceflow.com/widget/bundle.mjs"; v.type = "text/javascript"; s.parentNode.insertBefore(v, s);
  })(document, 'script');
</script>
