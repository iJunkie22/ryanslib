from __future__ import print_function, unicode_literals
import plistlib
import biplist
from collections import namedtuple

__author__ = 'Ethan Randall'


PXMLayerTypes = namedtuple('PXMLayerTypes',
                           ['bitmap', 'vector']
                           )('com.pixelmatorteam.pixelmator.layer.bitmap',
                             'com.pixelmatorteam.pixelmator.layer.vector')


class NSMutableData(biplist.Data):
    pass


class NSData(biplist.Data):
    pass


class NSName(str):
    pass


class NSSize(float):
    pass


class NSfFlags(int):
    pass


class NSMutableDictionary(dict):
    pass


class NSDictionary(dict):
    pass


class NSFont(dict):
    @property
    def NSName(self):
        return NSName(self['NSName'])

    @property
    def NSSize(self):
        return NSSize(self['NSSize'])

    @property
    def NSfFlags(self):
        return NSfFlags(self['NSfFlags'])


class NSColor(object):
    def __init__(self):
        self.NSColorSpace = NotImplemented
        self.NSComponents = NotImplemented
        self.NSRGB = NotImplemented

    @classmethod
    def from_dict(cls, d1):
        nsc1 = cls()
        # if isinstance(d1['NSComponents'], biplist.Uid):
        #     raise KeyError
        # if isinstance(d1['NSColorSpace'], biplist.Uid):
        #     raise KeyError
        if not d1.get('NSColorSpace'):
            pass

        if d1.get('NSComponents'):
            nsc1.NSComponents = NSComponents(d1['NSComponents'])

        nsc1.NSColorSpace = d1['NSColorSpace']
        if d1.get('NSRGB'):
            nsc1.NSRGB = NSRGB(d1['NSRGB'])

        return nsc1


class NSRGB(biplist.Data):
    @property
    def r(self):
        return float(self.split()[0])

    @property
    def g(self):
        return float(self.split()[1])

    @property
    def b(self):
        return float(self.split()[2])

    @property
    def a(self):
        return float(self.split()[3])


class NSComponents(biplist.Data):
    @property
    def is_greyscale(self):
        return len(self.split()) < 3

    @property
    def has_alpha(self):
        return (len(self.split()) % 2) == 0

    @property
    def r(self):
        pieces = self.split()
        if self.is_greyscale:
            return pieces[0]
        else:
            return pieces[0]

    @property
    def g(self):
        pieces = self.split()
        if self.is_greyscale:
            return pieces[0]
        else:
            return pieces[1]

    @property
    def b(self):
        pieces = self.split()
        if self.is_greyscale:
            return pieces[0]
        else:
            return pieces[2]

    @property
    def a(self):
        pieces = self.split()
        if self.has_alpha:
            if self.is_greyscale:
                return pieces[1]
            else:
                return pieces[3]
        else:
            raise AttributeError('alpha not included')


class NSArchivedPlist(object):
    def __init__(self):
        self.arc_plist = {}
        self.real_plist = {}
        self.uids = {}

    @property
    def top_uid(self):
        if self.arc_plist.get('$top'):
            if self.arc_plist['$top'].get('root'):
                return self.arc_plist['$top']['root']
            else:
                return -1
        else:
            return None

    @property
    def arc_top(self):
        if self.top_uid:
            if self.top_uid == -1:
                return self.arc_plist['$top']
            else:
                return self.arc_plist['$objects'][self.top_uid]
        else:
            return {}

    def q_ns_class(self, class_uid):
        class_str = self.uids[class_uid]
        if class_str == 'NSMutableString' or class_str == 'NSString':
            return lambda d: d['NS.string']

        elif class_str == 'NSMutableDictionary':
            return lambda d: NSMutableDictionary(zip(
                [self.uids[ku] for ku in d['NS.keys']],
                [self.uids[vu] for vu in d['NS.objects']]
            ))

        elif class_str == 'NSDictionary':
            return lambda d: NSDictionary(zip(
                [self.uids[ku] for ku in d['NS.keys']],
                [self.uids[vu] for vu in d['NS.objects']]
            ))

        elif class_str == 'NSMutableArray' or class_str == 'NSArray':
            return lambda d: [self.uids[iu] for iu in d['NS.objects']]

        elif class_str == 'NSMutableData':
            return lambda d: NSMutableData(d['NS.data'])

        elif class_str == class_str == 'NSData':
            return lambda d: NSData(d['NS.data'])

        elif class_str == 'NSValue':
            return lambda d, st=('NS.pointval', 'NS.sizeval', 'NS.rectval'): \
                eval(self.uids[d[st[d['NS.special'] - 1]]].replace('{', '(').replace('}', ')'))

        elif class_str == 'NSColorSpace':
            print('Skipped pythonizing for an NSColorSpace.')
            return lambda d: dict(zip(
                [self.uids[ku] if isinstance(ku, biplist.Uid) else ku for ku in d.keys()],
                [self.uids[vu] if isinstance(vu, biplist.Uid) else vu for vu in d.values()]
            ))

        elif class_str == 'NSColor':
            print('Skipped pythonizing for an NSColor.')
            return lambda d: NSColor.from_dict(d)
            # return lambda d: dict(zip(
            #     [self.uids[ku] if isinstance(ku, biplist.Uid) else ku for ku in d.keys()],
            #     [self.uids[vu] if isinstance(vu, biplist.Uid) else vu for vu in d.values()]
            # ))

        elif class_str == 'GCColorStop':
            print('Skipped pythonizing for a GCColorStop.')
            return lambda d: dict(zip(
                [self.uids[ku] if isinstance(ku, biplist.Uid) else ku for ku in d.keys()],
                [self.uids[vu] if isinstance(vu, biplist.Uid) else vu for vu in d.values()]
            ))

        elif class_str == 'GCGradient':
            print('Skipped pythonizing for a GCGradient.')
            return lambda d: dict(zip(
                [self.uids[ku] if isinstance(ku, biplist.Uid) else ku for ku in d.keys()],
                [self.uids[vu] if isinstance(vu, biplist.Uid) else vu for vu in d.values()]
            ))

        elif class_str == 'PXLayerStyle':
            print('Skipped pythonizing for a PXLayerStyle.')
            return lambda d: dict(zip(
                [self.uids[ku] if isinstance(ku, biplist.Uid) else ku for ku in d.keys()],
                [self.uids[vu] if isinstance(vu, biplist.Uid) else vu for vu in d.values()]
            ))

        elif class_str == 'PXSmartShape':
            print('Skipped pythonizing for a PXSmartShape.')
            return lambda d: dict(zip(
                [self.uids[ku] if isinstance(ku, biplist.Uid) else ku for ku in d.keys()],
                [self.uids[vu] if isinstance(vu, biplist.Uid) else vu for vu in d.values()]
            ))

        elif class_str == 'NSFont':
            print('Skipped pythonizing for an NSFont.')
            return lambda d: NSFont(zip(
                [self.uids[ku] if isinstance(ku, biplist.Uid) else ku for ku in d.keys()],
                [self.uids[vu] if isinstance(vu, biplist.Uid) else vu for vu in d.values()]
            ))

        else:
            raise ValueError('No known python type for that!')

    @classmethod
    def load(cls, plist_in):
        nsap1 = cls()
        nsap1.arc_plist = plist_in
        if nsap1.top_uid is None:
            nsap1.real_plist = {}
            return nsap1

        assert nsap1.arc_plist['$archiver'] == 'NSKeyedArchiver'

        #  load class names
        numbered_objects = list(enumerate(nsap1.arc_plist['$objects']))
        trash = []
        for i1, o1 in reversed(numbered_objects):
            if isinstance(o1, dict) and '$classname' in o1.keys():
                nsap1.uids[i1] = o1['$classname']
                trash.append(i1)
            elif not isinstance(o1, dict):
                nsap1.uids[i1] = o1
                trash.append(i1)

        numbered_objects2 = list(numbered_objects)
        for t in sorted(trash, reverse=True):
            del numbered_objects[t]

        unfinished = True
        trash = []

        while unfinished:
            unfinished = False

            for i2, o2 in reversed(numbered_objects):
                if i2 != nsap1.top_uid and isinstance(o2, dict) and o2.get('$class'):
                    if 'NS.keys' not in o2.keys():

                        try:
                            nsap1.uids[i2] = nsap1.q_ns_class(o2['$class'])(o2)
                            trash.append(i2)

                        except KeyError:
                            unfinished = True

            for t in sorted(trash, reverse=True):
                numbered_objects.remove(numbered_objects2[t])


            trash = []

            for i3, o3 in reversed(numbered_objects):
                if i3 != nsap1.top_uid:

                    try:
                        nsap1.uids[i3] = nsap1.q_ns_class(o3['$class'])(o3)
                        trash.append(i3)

                    except KeyError:
                        unfinished = True

            for t in sorted(trash, reverse=True):
                numbered_objects.remove(numbered_objects2[t])

            trash = []

        root = nsap1.arc_top

        if len(numbered_objects) == 1 and root.get('NS.keys'):
            root2 = dict(zip(
                [nsap1.uids[ku2] for ku2 in root['NS.keys']],
                [nsap1.uids[vu2] for vu2 in root['NS.objects']]
            ))
        else:
            root2 = dict(zip(
                [nsap1.uids[ku] if isinstance(ku, biplist.Uid) else ku for ku in root.keys()],
                [nsap1.uids[vu] if isinstance(vu, biplist.Uid) else vu for vu in root.values()]
            ))

        nsap1.real_plist = root2
        return nsap1


class AppleTermPrefs(object):
    bkeys = ('BackgroundColor', 'BackgroundImageBookmark','CursorColor',
             'Font', 'SelectionColor',
             'TextBoldColor', 'TextColor')

    def __init__(self):
        self.main_pl = {}

    @property
    def BackgroundBlur(self):
        """
        :rtype: float
        """
        return self.main_pl['BackgroundBlur']

    @property
    def BackgroundColor(self):
        r1 = self.main_pl['BackgroundColor']
        r2 = biplist.readPlistFromString(r1.data)
        r3 = NSArchivedPlist.load(r2)
        r4 = r3.q_ns_class(2)(r3.arc_plist['$objects'][1])
        return r4

    @property
    def BackgroundImageBookmark(self):
        r1 = self.main_pl['BackgroundImageBookmark']
        r2 = biplist.readPlistFromString(r1.data)
        r3 = NSArchivedPlist.load(r2)
        r4 = r3.q_ns_class(2)(r3.arc_plist['$objects'][1])
        return r4

    @property
    def BackgroundSettingsForInactiveWindows(self):
        """
        :rtype: bool
        """
        return self.main_pl['BackgroundSettingsForInactiveWindows']

    @property
    def Bell(self):
        """
        :rtype: bool
        """
        return self.main_pl['Bell']

    @property
    def CursorBlink(self):
        """
        :rtype: bool
        """
        return self.main_pl['CursorBlink']

    @property
    def CursorColor(self):
        r1 = self.main_pl['CursorColor']
        r2 = biplist.readPlistFromString(r1.data)
        r3 = NSArchivedPlist.load(r2)
        r4 = r3.q_ns_class(2)(r3.arc_plist['$objects'][1])
        return r4

    @property
    def DisableANSIColor(self):
        """
        :rtype: bool
        """
        return self.main_pl['DisableANSIColor']

    @property
    def EscapeNonASCIICharacters(self):
        """
        :rtype: bool
        """
        return self.main_pl['EscapeNonASCIICharacters']

    @property
    def Font(self):
        r1 = self.main_pl['Font']
        r2 = biplist.readPlistFromString(r1.data)
        r3 = NSArchivedPlist.load(r2)
        r4 = r3.q_ns_class(3)(r3.arc_plist['$objects'][1])
        return r4

    @property
    def FontAntialias(self):
        """
        :rtype: bool
        """
        return self.main_pl.get('FontAntialias', True)

    @property
    def FontWidthSpacing(self):
        """
        :rtype: float
        """
        return self.main_pl['FontWidthSpacing']

    @property
    def ProfileCurrentVersion(self):
        """
        :rtype: float
        """
        return self.main_pl['ProfileCurrentVersion']

    @property
    def SelectionColor(self):
        r1 = self.main_pl['SelectionColor']
        r2 = biplist.readPlistFromString(r1.data)
        r3 = NSArchivedPlist.load(r2)
        r4 = r3.q_ns_class(2)(r3.arc_plist['$objects'][1])
        return r4

    @property
    def ShowActiveProcessInTitle(self):
        """
        :rtype: bool
        """
        return self.main_pl['ShowActiveProcessInTitle']

    @property
    def ShowShellCommandInTitle(self):
        """
        :rtype: bool
        """
        return self.main_pl['ShowShellCommandInTitle']

    @property
    def TerminalType(self):
        """
        :rtype: str
        """
        return self.main_pl['TerminalType']

    @property
    def TextBoldColor(self):
        r1 = self.main_pl['TextBoldColor']
        r2 = biplist.readPlistFromString(r1.data)
        r3 = NSArchivedPlist.load(r2)
        r4 = r3.q_ns_class(2)(r3.arc_plist['$objects'][1])
        return r4

    @property
    def TextColor(self):
        r1 = self.main_pl['TextColor']
        r2 = biplist.readPlistFromString(r1.data)
        r3 = NSArchivedPlist.load(r2)
        r4 = r3.q_ns_class(2)(r3.arc_plist['$objects'][1])
        return r4

    @property
    def UseBrightBold(self):
        """
        :rtype: bool
        """
        return self.main_pl['UseBrightBold']

    @property
    def VisualBellOnlyWhenMuted(self):
        """
        :rtype: bool
        """
        return self.main_pl['VisualBellOnlyWhenMuted']

    @property
    def columnCount(self):
        """
        :rtype: int
        """
        return self.main_pl['columnCount']

    @property
    def name(self):
        """
        :rtype: str
        """
        return self.main_pl['name']

    @property
    def rowCount(self):
        """
        :rtype: int
        """
        return self.main_pl['rowCount']

    @property
    def type(self):
        """
        :rtype: str
        """
        return self.main_pl['type']

    @classmethod
    def from_file(cls, fp_in):
        o1 = cls()
        o1.main_pl = plistlib.readPlist(fp_in)
        return o1


FP1 = "iJunkie22.terminal"

term_pl1 = AppleTermPrefs.from_file(FP1)
blah = term_pl1.TextColor
moo = term_pl1.BackgroundImageBookmark
bark = term_pl1.Font
print(blah)


print("j")

