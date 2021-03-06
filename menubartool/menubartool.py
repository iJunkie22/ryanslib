#!/usr/bin/python2.7
import Foundation
import subprocess
import sys


class AppleInterFaceStyle(int, object):
    @property
    def name(self):
        return ('Light', 'Dark')[self]

styles = ('0', '1', 'Light', 'Dark', 'light', 'dark', 0, 1)


def refresh_ui_theme():
    notif_class = Foundation.NSDistributedNotificationCenter
    notif_inst = notif_class.defaultCenter()
    return notif_inst.postNotificationName_object_('AppleInterfaceThemeChangedNotification', None)


def set_menu_style(new_style=1):
    style_str = AppleInterFaceStyle(new_style).name
    p1 = subprocess.Popen(['/usr/bin/defaults', 'write', '.GlobalPreferences', 'AppleInterfaceStyle', style_str],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p1.wait()
    return p1.returncode


def main(args):
    if len(args) == 2 and args[1] in styles:
        style_int = styles.index(args[1]) % 2
        set_menu_style(style_int)
        refresh_ui_theme()
    else:
        print 'USAGE: ' + str(sys.argv[0]) + ' ' + repr(list(styles))

if __name__ == '__main__':
    main(sys.argv)
