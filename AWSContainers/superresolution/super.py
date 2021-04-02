import io
import numpy as np
from PIL import Image, ImageOps
from ISR.models import RDN, RRDN
import requests


#load super resolution models
model_lg = RDN(weights="psnr-large")
model_sm = RDN(weights="psnr-small") 
model_nc = RDN(weights="noise-cancel")
gan_model = RRDN(weights='gans')

id2model = {
    "gan":gan_model,
    "nc":model_nc,
    "lg":model_lg,
    "sm":model_sm,
}

def super_res(img, pipeline=["gan", "nc"]):
    """ flexible pipeline for chaining multiple models
    """
    arr = np.array(img)
    for key in pipeline:
        model = id2model[key]
        arr = model.predict(arr)
    return Image.fromarray(arr)


def super_res_arr(arr, pipeline=["gan", "nc"]):
    for key in pipeline:
        model = id2model[key]
        arr = model.predict(arr)
    return arr


def decode_image(bytes):
    """ given raw bytes will decode and return a PIL image
    """
    f = io.BytesIO(base64.b64decode(b64string))
    pilimage = Image.open(f)
    return pilimage

def super_res_gan(img):
    """ Take a PIL image and use 
        the GAN model to increase to super resolution
    """
    arr = np.array(img)
    pred = gan_model.predict(arr)
    return Image.fromarray(pred)

def downsample(img, r=0.1):
    """ test function, downsample an image by a percentage
        :param img, a PIL Image format
        :r ratio, the percentage new image size
    """
    width, height = img.size
    w = int(width*r)
    h = int(height*r)
    if 'P' in img.mode: # check if image is a palette type
        img = img.convert("RGB") # convert it to RGB
        img = img.resize((w,h),Image.ANTIALIAS) # resize it
        img = img.convert("P",dither=Image.NONE, palette=Image.ADAPTIVE) 
           #convert back to palette
    else:
        img = img.resize((w,h),Image.ANTIALIAS) # regular resize
    return img

def download_image(url):
    """ helper function, download an image from url"""
    return Image.open(requests.get(url, stream=True).raw)


if __name__ == "__main__":
    dog_url = "https://mbtimetraveler.files.wordpress.com/2016/01/sad-cute-dog-high-resolution-wallpaper-for-desktop-background-download-dog-photos-free.jpg?w=1800"
    im = download_image(dog_url)
    small = downsample(im)
    hires = super_res(im)
    hires.save("hires_dog.jpg")

