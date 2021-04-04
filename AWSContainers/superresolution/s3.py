import io
from PIL import Image
import numpy as np
import requests
import boto3
import os

import time

ACCESS_KEY = os.environ["ACCESS_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]

s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)


def run_scan(bucket="arden-w251"):
    result = s3.list_objects(Bucket = bucket, Prefix='raw/')
    for x in result["Contents"]:
        key = x["Key"]
        print(key)
        
        data = s3.get_object(Bucket=bucket, Key=key)
        contents = data['Body']
        im = Image.open(contents)
        arr = np.array(im)
        print(arr.shape)



if __name__ == "__main__":
    
    while True:
        run_scan()
        time.sleep(10)



