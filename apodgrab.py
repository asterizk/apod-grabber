from bs4 import BeautifulSoup  # for html snippet parsing
from PIL import Image, ImageFont, ImageDraw  # for image manipulation. To install: pip3 install pillow
from datetime import date  # for naming the captioned image
import shutil  # for file copy
import tempfile  # for generating temp files
import urllib.request  # for downloading from internet
import subprocess  # to execute shell script
import os  # to get current working directory, make a new one, and expand ~

# Given a font, wrap text into a given set of dimensions
#   see https://stackoverflow.com/a/62418837
def text_wrap(text, font, writing, max_width, max_height):
    def _dims(s):
        l, t, r, b = writing.multiline_textbbox((0, 0), s, font=font)
        return (r - l, b - t)

    def _composed():
        return '\n'.join(' '.join(line) for line in lines if line)
    lines = [[]]
    words = text.split()
    for word in words:
        # try putting this word in last line then measure
        lines[-1].append(word)
        w, h = _dims(_composed())
        if w > max_width:
            moved = lines[-1].pop()
            lines.append([moved])
            w, h = _dims(_composed())
            if h > max_height:
                lines.pop()
                lines[-1][-1] += '...'
                while True:
                    w, h = _dims(_composed())
                    if w <= max_width or len(lines[-1]) == 1:
                        break
                    lines[-1].pop()
                    lines[-1][-1] += '...'
                break
    return '\n'.join([' '.join(line) for line in lines])


# Given a URL, return the parsed HTML tag soup
def get_tag_soup(url):
    html_text = urllib.request.urlopen(url).read()
    return BeautifulSoup(html_text, features="html.parser")


# Given an apod HTML tag soup, return the apod image title
def get_apod_title(soup):
    center_with_title = soup.body.find_all('center')[1]
    title = center_with_title.find_all('b')[0]
    return title.get_text(" ", strip=True)


# Given an apod HTML tag soup, return the apod image explanation
def get_apod_explanation(soup):
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#get-text
    text = soup.get_text(" ", strip=True)

    # get rid of extra linefeeds in source before stripping out html entities, see
    # https://stackoverflow.com/questions/24878437/cant-remove-line-breaks-from-beautifulsoup-text-output-python-2-7-5
    text = text.replace("\t", "").replace("\r", "").replace("\n", " ").replace("  ", " ")

    # fix errors with spaces before and after periods
    text = text.replace(" .", ".").replace(" ,", ",")

    # Add 12 so that the word 'Explanation:' isn't included
    location = text.find("Explanation:") + 12
    end_location = text.find("Tomorrow's picture")
    explanation = text[location:end_location]
    return explanation


# Determine file that needs downloading
def get_apod_fullsize_image_url(soup):
    center_with_fullsize_image = soup.body.find_all('center')[0]
    fullsize_image_path = center_with_fullsize_image.find_all('a')[1].get('href')
    return 'https://apod.nasa.gov/apod/' + fullsize_image_path


def set_wallpaper_macos_all(image_path: str):
    """
    1) Set the wallpaper on ALL desktops (all monitors/spaces) via System Events.
    2) Style the active Space via AppKit: Fit-to-Screen, no clipping, black background.
    """
    path = os.path.abspath(image_path)
    safe_path = path.replace('"', '\\"')  # escape double-quotes for AppleScript

    # --- Step 1: AppleScript (all desktops / all displays) ---
    ascript = (
        'tell application "System Events"\n'
        f'  set p to "{safe_path}"\n'
        '  set ds to a reference to every desktop\n'
        '  repeat with d in ds\n'
        '    set picture of contents of d to p\n'
        '    delay 0.1\n'
        '  end repeat\n'
        'end tell'
    )
    try:
        subprocess.run(
            ["/usr/bin/osascript", "-e", ascript],
            check=True,
            text=True,
            capture_output=True,
        )
        print("Wallpaper image applied to all desktops (AppleScript).")
    except subprocess.CalledProcessError as e:
        print("AppleScript step failed; continuing:", e.stderr or e.stdout or repr(e))

    # --- Step 2: PyObjC styling (current Space only) ---
    try:
        from AppKit import (
            NSWorkspace, NSScreen, NSColor,
            NSWorkspaceDesktopImageScalingKey,
            NSWorkspaceDesktopImageAllowClippingKey,
            NSWorkspaceDesktopImageFillColorKey,
            NSImageScaleProportionallyUpOrDown,
        )
        from Foundation import NSURL

        ws = NSWorkspace.sharedWorkspace()
        url = NSURL.fileURLWithPath_(path)
        options = {
            NSWorkspaceDesktopImageScalingKey: NSImageScaleProportionallyUpOrDown,  # "Fit to Screen"
            NSWorkspaceDesktopImageAllowClippingKey: False,                          # don't crop
            NSWorkspaceDesktopImageFillColorKey: NSColor.blackColor(),               # black bars
        }
        for screen in NSScreen.screens():
            ok, err = ws.setDesktopImageURL_forScreen_options_error_(url, screen, options, None)
            if not ok:
                raise RuntimeError(err)
        print("Applied Fit-to-Screen + black background (PyObjC).")
    except Exception as e:
        print("PyObjC styling step skipped/fell back:", repr(e))

# Start main script
tag_soup = get_tag_soup('https://apod.nasa.gov/apod/')
fullsize_url = get_apod_fullsize_image_url(tag_soup)
apod_title = get_apod_title(tag_soup)
apod_explanation = get_apod_explanation(tag_soup)

with urllib.request.urlopen(fullsize_url) as response:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copyfileobj(response, tmp_file)

bg = Image.open(tmp_file.name)
# Comment-out line above and uncomment line below for local-image debugging
# bg = Image.open('/var/folders/qy/bpj3cz615s30nhrw3q90hrfr0000gp/T/tmp1np2w9gk')
# print('Image is ' + str(bg.width) + ' x ' + str(bg.height))
writing = ImageDraw.Draw(bg)

# Smaller factor = smaller text.
title_font_size_factor = 0.020
desc_font_size_factor = 0.015
title_font_size = int(bg.width * title_font_size_factor)
desc_font_size = int(bg.width * desc_font_size_factor)

title_font = ImageFont.truetype("Arial Black.ttf", size=title_font_size)
desc_font = ImageFont.truetype("Arial Narrow Italic.ttf", size=desc_font_size)

# The dimensions of the text box are a factor of the source image
explanation_wrapped = text_wrap(apod_explanation, desc_font, writing, int(bg.width * 0.25), int(bg.height * 0.7))

# write title and explanation
writing.text((int(bg.width * 0.02), int(bg.height * 0.05)), apod_title, font=title_font)

# The offset of the text box from the upper left corner is a factor of the source image dimensions
writing.text((int(bg.width * 0.05), (int(bg.height * 0.11))), explanation_wrapped, font=desc_font)

# below line for debugging only
# bg.show()

# create a temporary directory using the context manager
tmpdirname = tempfile.gettempdir()
# TODO: Make use of tmpdir vs archiving to '~/Pictures/apod/' a preference
# os.makedirs(tmpdirname + '/apod', exist_ok=True)
os.makedirs(os.environ['HOME'] + '/Pictures/apod', exist_ok=True)
today = date.today()
# captionedImageFilePath = tmpdirname+'/apod/'+str(today)+'.png'
captionedImageFilePath = os.environ['HOME'] + '/Pictures/apod/'+str(today)+'.png'
bg.save(captionedImageFilePath)

print('Setting the new desktop picture: ', captionedImageFilePath)
set_wallpaper_macos_all(captionedImageFilePath)         # apply scaling/bg to current Space

