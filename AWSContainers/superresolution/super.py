import io
import numpy as np
from PIL import Image, ImageOps
from ISR.models import RDN, RRDN
import requests
import boto3
import os
import time

#keep tabs on which images have already been ran
ran = {}


#load super resolution models
model_lg = RDN(weights="psnr-large")
model_sm = RDN(weights="psnr-small") 
model_nc = RDN(weights="noise-cancel")
gan_model = RRDN(weights='gans')

ACCESS_KEY = os.environ["ACCESS_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]

s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

def pre_scan(bucket="arden-w251"):
    result = s3.list_objects(Bucket = bucket, Prefix='super/')
    if result and "Contents" in result:
        for o in result['Contents']:
            key = o["Key"]
            key = key.split("/")[-1]
            ran[key] = True

def run_scan(bucket="arden-w251"):
    result = s3.list_objects(Bucket = bucket, Prefix='raw/')
    for x in result["Contents"]:
        key = x["Key"]
        print(key)
        sk = key.split("/")[-1]
        if sk in ran:
            print("skipping {}".format(key))
            continue
        print("running {}".format(key))

        data = s3.get_object(Bucket=bucket, Key=key)
        contents = data['Body']
        im = Image.open(contents)
        arr = np.array(im)
        super_arr = super_res_arr(arr)
        
        s3.put_object(
            Body=super_arr,
            Bucket=bucket,
            Key="super/{}".format(sk))
        ran[sk] = True
        print("saved to: {}".format("super/{}".format(sk)))
    

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
    
    #run our pre-scan
    pre_scan()

    while True:
        run_scan()
        time.sleep(5)



