from subprocess import call
from time import sleep as wait
call("upgrade.sh")
print("palgrave: update attempt finished")
wait(3)
quit()