from subprocess import call
from time import sleep
call("git remote add origin https://github.com/kaiete/InstantPalgrave && git pull --set-upstream origin main")
print("palgrave: update attempt finished")
sleep(3)
quit()