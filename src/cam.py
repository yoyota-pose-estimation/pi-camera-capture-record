import os
import datetime
from picamera import PiCamera
from minio import Minio
from minio.error import ResponseError

picture_dir = '/home/pi/Pictures'

cam = PiCamera()
cam.rotation = 180
cam.resolution = (300, 300)

minioClient = Minio(
    os.environ.get('S3_ENDPOINT'),
    access_key=os.environ.get('AWS_ACCESS_KEY_ID'),
    secret_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    secure=True)


def upload(object_name, file_path):
    minioClient.fput_object(
        'pi-camera',
        object_name,
        file_path)
    os.remove(file_path)


def capture(section):
    today = str(datetime.datetime.utcnow()) + '.jpg'
    save_path = os.path.join(picture_dir, today)
    cam.capture(save_path)
    object_name = os.path.join(section, today)
    upload(object_name, save_path)
