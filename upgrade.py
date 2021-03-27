from subprocess import call
from time import sleep
call("upgrade.sh")
print("palgrave: update attempt finished")
sleep(3)
quit()