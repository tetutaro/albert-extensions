# -*- coding: utf-8 -*-
"""Extension which basically wraps the command line utility scrot to make \
screenshots from albert. The extension supports taking screenshots of \
the whole screen, an specific area or the current active window.

When the screenshot was made you will hear a sound which indicates that the \
screenshot was taken successfully.

Screenshots will be saved in XDG_PICTURES_DIR or in the temp directory."""

import os
import subprocess
import tempfile
from shutil import which
from albertv0 import iconLookup, Item, FuncAction


__iid__ = "PythonInterface/v0.1"
__prettyname__ = "Screen Shot"
__version__ = "1.0"
__trigger__ = "ss "
__author__ = "Tetsutaro Maruyama"
__dependencies__ = ["scrot", "xclip"]


if which("scrot") is None:
    raise Exception("'scrot' is not in $PATH.")
if which("xclip") is None:
    raise Exception("'xclip' is not in $PATH.")
iconPath = iconLookup("camera-photo")

ss_items = {
    'screen': Item(
        id="screen-shot-whole-screen",
        icon=iconPath,
        text="Screen",
        completion=__trigger__ + "Screen",
        subtext="Take a screenshot of the whole screen",
        actions=[FuncAction(
            "Take screenshot of whole screen",
            lambda: doScreenshot([])
        )]
    ),
    'screen multi': Item(
        id="screen-shot-whole-screen-multi",
        icon=iconPath,
        text="Screen Multi",
        completion=__trigger__ + "Screen Multi",
        subtext="Take a screenshot of multiple displays",
        actions=[FuncAction(
            "Take screenshot of multiple displays",
            lambda: doScreenshot(["--multidisp"])
        )]
    ),
    'area': Item(
        id="screen-shot-area-of-screen",
        icon=iconPath,
        text="Area",
        completion=__trigger__ + "Area",
        subtext="Draw a rectangle with your mouse to capture an area",
        actions=[FuncAction(
            "Take screenshot of selected area",
            lambda: doScreenshot(["--select"])
        )]
    ),
    'window': Item(
        id="screen-shot-current-window",
        icon=iconPath,
        text="Window",
        completion=__trigger__ + "Window",
        subtext="Take a screenshot of the current active window",
        actions=[FuncAction(
            "Take screenshot of window with borders",
            lambda: doScreenshot(["--focused", "--border"])
        )]
    ),
    'window noborder': Item(
        id="screen-shot-current-window-noborder",
        icon=iconPath,
        text="Window NoBorder",
        completion=__trigger__ + "Window NoBorder",
        subtext="Take a screenshot of the current window without borders",
        actions=[FuncAction(
            "Take screenshot of window without borders",
            lambda: doScreenshot(["--focused"])
        )]
    ),
}


def handleQuery(query):
    if query.isTriggered:
        args = query.string.strip().lower()
        if len(args) == 0:
            return list(ss_items.values())
        items = list()
        for cmd, item in ss_items.items():
            if cmd.startswith(args):
                items.append(item)
        if len(items) > 0:
            return items
        return [
            Item(
                id="screen-shot-no-hit",
                icon=iconPath,
                text="Not Found",
                subtext="invoke the collect command"
            )
        ]


def getScreenshotDirectory():
    if which("xdg-user-dir") is None:
        return tempfile.gettempdir()
    proc = subprocess.run(["xdg-user-dir", "DESKTOP"], stdout=subprocess.PIPE)
    pictureDirectory = proc.stdout.decode("utf-8")
    if pictureDirectory:
        return pictureDirectory.strip()
    return tempfile.gettempdir()


def doScreenshot(additionalArguments):
    file = os.path.join(getScreenshotDirectory(), "%Y-%m-%d-%T-screenshot.png")
    command = "sleep 0.1 && "
    command += "scrot --exec 'xclip -selection c -t image/png < $f' %s " % file
    subprocess.Popen(
        command + " ".join(additionalArguments),
        shell=True
    )
