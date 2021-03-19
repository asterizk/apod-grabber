from urllib.request import urlopen
from bs4 import BeautifulSoup #for html snippet parsing
from PIL import Image, ImageFont, ImageDraw #for image manipulation. To install: pip3 install pillow

# Given a font, wrap text into a given set of dimensions
#   see https://stackoverflow.com/a/62418837
def text_wrap(text,font,writing,max_width,max_height):
    lines = [[]]
    words = text.split()
    for word in words:
        # try putting this word in last line then measure
        lines[-1].append(word)
        (w,h) = writing.multiline_textsize('\n'.join([' '.join(line) for line in lines]), font=font)
        if w > max_width: # too wide
            # take it back out, put it on the next line, then measure again
            lines.append([lines[-1].pop()])
            (w,h) = writing.multiline_textsize('\n'.join([' '.join(line) for line in lines]), font=font)
            if h > max_height: # too high now, cannot fit this word in, so take out - add ellipses
                lines.pop()
                # try adding ellipses to last word fitting (i.e. without a space)
                lines[-1][-1] += '...'
                # keep checking that this doesn't make the textbox too wide, 
                # if so, cycle through previous words until the ellipses can fit
                while writing.multiline_textsize('\n'.join([' '.join(line) for line in lines]),font=font)[0] > max_width:
                    lines[-1].pop()
                    lines[-1][-1] += '...'
                break
    return '\n'.join([' '.join(line) for line in lines])

# Given a URL, return the parsed HTML tag soup
def get_tag_soup(url):
    htmlText = urlopen(url).read()
    return BeautifulSoup(htmlText, features="html.parser")

# Given an apod HTML tag soup, return the apod image title
def get_apod_title(soup):
    centerWithTitle = soup.body.find_all('center')[1]
    title = centerWithTitle.find_all('b')[0]
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

    location = text.find("Explanation:")
    endLocation = text.find("Tomorrow's picture")
    explanation = text[location:endLocation]
    return explanation

tag_soup = get_tag_soup('https://apod.nasa.gov/apod/')
apod_title = get_apod_title(tag_soup)
apod_explanation = get_apod_explanation(tag_soup)

bg = Image.open('/private/tmp/file.jpg')
writing = ImageDraw.Draw(bg)

title_font = ImageFont.truetype("Arial Black.ttf", size=42)
desc_font = ImageFont.truetype("Arial Narrow Italic.ttf", size=28)

# width, height
explanation_wrapped = text_wrap(apod_explanation,desc_font,writing,1000,500)

# write title and explanation
writing.text((20,5),apod_title,font=title_font)
writing.text((140,120),explanation_wrapped,font=desc_font)

bg.show()
