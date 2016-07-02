import subprocess
import plistlib
import binascii

p1 = subprocess.Popen(['/usr/bin/env', 'dscl', '-plist', '.', '-read', '/Users/ethan', 'dsAttrTypeStandard:JPEGPhoto'
                       ], stdout=subprocess.PIPE)

stdo, stde = p1.communicate()

pl1 = plistlib.readPlistFromString(stdo)
jpeg_str = pl1['dsAttrTypeStandard:JPEGPhoto'][0]

jp1 = open('userpic3.jpeg', mode='wb')

try:
    for bword in jpeg_str.split():
        jp1.write(binascii.unhexlify(bword))

finally:
    jp1.close()


#   """dscl -plist . -read /Users/ethan dsAttrTypeStandard:JPEGPhoto"""
