import subprocess
from PIL import Image


myscript = \
"""
import AppKit
import sys

screens = [x for x in AppKit.NSScreen.screens()]
shared_workspace = AppKit.NSWorkspace.sharedWorkspace()

sys.stdout.write(str(shared_workspace.desktopImageURLForScreen_(screens[0]).path.self))
sys.stdout.flush()
exit()

"""


def get_wallpaper_path():
    p1 = subprocess.Popen(['/usr/bin/python', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stdo, stderr = p1.communicate(myscript)

    if stderr:
        raise Exception(stderr)
    else:
        return stdo


def url_to_path(url_str):
    assert isinstance(url_str, (str, unicode))
    fp_result = url_str
    if url_str.startswith('file:///'):
        fp_result = url_str.partition('file://')[2]
    return fp_result


def counts_as_a_color(rgb_tup):
    thresh = 30
    return (max(rgb_tup) - min(rgb_tup)) >= thresh


def get_wallpaper_colors(verbose=False):

    wp_fp = url_to_path(get_wallpaper_path())

    if verbose:
        print wp_fp

    im1 = Image.open(wp_fp)

    grayscales_list = []
    colors_list1 = []
    colors_list2 = []
    colors_values_list = []
    colors_values_dict = {}
    colors_values_dict_keys = colors_values_dict.viewkeys()

    for im_color in im1.getcolors(maxcolors=99999):
        r, g, b = im_color[1]
        if r == g and g == b:
            grayscales_list.append(im_color)

        elif counts_as_a_color(im_color[1]):
            colors_list1.append(im_color)

        else:
            grayscales_list.append(im_color)

    if len(colors_list1) < 2:
        colors_list1 = grayscales_list

    if verbose:
        print len(grayscales_list)
        print len(colors_list1)

    for color_x in colors_list1:
        x_val = max(color_x[1])
        x_count = color_x[0]

        colors_list2.append((x_count, color_x[1], x_val))
        colors_values_list.append(x_val)

        if x_val in colors_values_dict_keys:
            if x_count > colors_values_dict[x_val][0]:
                colors_values_dict[x_val] = (x_count, color_x[1], x_val)
            #elif x_count == colors_values_dict[x_val][0][0]:
            #    colors_values_dict[x_val].append((x_count, color_x[1], x_val))
        else:
            colors_values_dict[x_val] = (x_count, color_x[1], x_val)

    colors_list2.sort(key=lambda x: x[2])

    if verbose:
        print len(set(colors_values_list))

    if verbose:
        for ck in sorted(colors_values_dict_keys):
            print ck, '\t:\t', colors_values_dict[ck]

    dark_color = (0, (0, 0, 0), 0)
    light_color = (0, (0, 0, 0), 0)

    sorted_c_keys = sorted(colors_values_dict_keys)

    for i, ck in enumerate(sorted(colors_values_dict_keys)):
        cv = colors_values_dict[ck]
        if i < (len(colors_values_dict_keys) / 2):
            if cv[0] > dark_color[0]:
                dark_color = cv
        else:
            if cv[0] > light_color[0]:
                light_color = cv

    if verbose:
        print "=" * 50
        print dark_color
        print light_color

    return {'dark': dark_color[1], 'light': light_color[1]}

if __name__ == '__main__':
    result = get_wallpaper_colors(True)
    print result

