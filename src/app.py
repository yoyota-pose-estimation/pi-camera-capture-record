import io
import os
import socket
import datetime
from time import sleep
from threading import Thread
from shutil import copyfileobj
from minio import Minio
from picamera import PiCamera


cam = PiCamera()
cam.rotation = 180
cam.resolution = (300, 300)
sleep(2)


minioClient = Minio(
    os.environ.get('S3_ENDPOINT'),
    access_key=os.environ.get('AWS_ACCESS_KEY_ID'),
    secret_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    secure=True)


def upload(object_name, stream):
    length = stream.getbuffer().nbytes
    minioClient.put_object(
        'pi-camera',
        object_name,
        stream,
        length)


def copy_stream(stream):
    copied = io.BytesIO()
    copyfileobj(stream, copied)
    copied.seek(0)
    return copied


def capture():
    stream = io.BytesIO()
    cam.capture(stream, 'jpeg', True)
    stream.seek(0)
    return stream


def get_object_name():
    now = datetime.datetime.utcnow()
    filename = '{}-{}.jpg'.format(now.isoformat(), socket.gethostname())
    object_name = os.path.join(
        'record', now.strftime('%y-%m-%d'), now.strftime('%H-%M'), filename)
    return object_name


def main():
    while True:
        object_name = get_object_name()
        stream = capture()
        Thread(target=upload, args=(object_name, copy_stream(stream))).start()
        sleep(0.03)


if __name__ == "__main__":
    main()
