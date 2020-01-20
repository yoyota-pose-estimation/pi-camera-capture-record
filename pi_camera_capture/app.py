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
    os.environ.get("S3_ENDPOINT"),
    access_key=os.environ.get("AWS_ACCESS_KEY_ID"),
    secret_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    secure=True,
)


def upload(object_name, stream):
    length = stream.getbuffer().nbytes
    minioClient.put_object("pi-camera", object_name, stream, length)


def copy_stream(stream):
    copied = io.BytesIO()
    copyfileobj(stream, copied)
    copied.seek(0)
    return copied


def capture():
    stream = io.BytesIO()
    cam.capture(stream, "jpeg", True)
    stream.seek(0)
    return stream


def get_object_name():
    now = datetime.datetime.utcnow()
    filename = "{}_{}.jpg".format(now.isoformat(), socket.gethostname())
    object_name = os.path.join(
        "record",
        now.strftime("%Y-%m-%d"),
        now.strftime("%H"),
        now.strftime("%M"),
        filename,
    )
    return object_name


def main():
    while True:
        sleep(0.1)
        try:
            object_name = get_object_name()
            stream = capture()
            Thread(
                target=upload, args=(object_name, copy_stream(stream))
            ).start()
        except Exception as e:
            print(e)
            sleep(0.1)


if __name__ == "__main__":
    main()
