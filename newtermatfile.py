import sys
import os.path
import subprocess


myscript = \
"""
tell application "Terminal"
    activate
    set var1 to "{0}"
    set var2 to "{1}"
    set currentTab to do script ("cd " & quoted form of var1 & ";")
    do script ("tput clear;") in currentTab
    do script ("FINDER_FILE=" & quoted form of var2 & ";") in currentTab
end tell
"""

fp_in = sys.stdin.read()

fp_dn, fp_bn = os.path.split(fp_in)

fp_out = fp_dn

p1 = subprocess.Popen(['/usr/bin/osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)

stdo, stderr = p1.communicate(myscript.format(fp_out + "/", "./" + str(fp_bn).splitlines()[0]))
