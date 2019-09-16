import io
import os
import sys
import socket
import datetime
from time import sleep
from picamera import PiCamera
from minio import Minio
from minio.error import ResponseError


cam = PiCamera()
cam.rotation = 180
cam.resolution = (300, 300)


minioClient = Minio(
    os.environ.get('S3_ENDPOINT'),
    access_key=os.environ.get('AWS_ACCESS_KEY_ID'),
    secret_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    secure=True)


def upload(object_name, file_obj):
    length = file_obj.getbuffer().nbytes
    minioClient.put_object(
        'pi-camera',
        object_name,
        file_obj,
        length)


def capture(section):
    filename = str(datetime.datetime.utcnow()) + \
        socket.gethostname() + '.jpg'
    stream = io.BytesIO()
    cam.capture(stream, 'jpeg')
    stream.seek(0)
    object_name = os.path.join(section, filename)
    upload(object_name, stream)
