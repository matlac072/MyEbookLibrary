import io
import urllib.request
from PIL import Image, ImageTk

def get_cover_from_url(url):
    with urllib.request.urlopen(url) as connection:
        raw_data = connection.read()

    im = Image.open(io.BytesIO(raw_data))
    
    # Resizing the image
    target_height = 400
    hpercent = (target_height / float(im.size[1]))
    wsize = int((float(im.size[0]) * float(hpercent)))
    im = im.resize((wsize, target_height), Image.ANTIALIAS)
    
    image = ImageTk.PhotoImage(im)
    return image