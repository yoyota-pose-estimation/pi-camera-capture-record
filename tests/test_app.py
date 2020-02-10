import io
import re
import socket
from time import time
import email.parser


import responses
import pi_camera_capture.picamera_mock  # pylint: disable=unused-import
from pi_camera_capture.cam import capture
from pi_camera_capture.app import (
    upload_image,
    query_distance,
    upload_image_if_distance_exist,
)


UPLOAD_SERVER_URL = "http://localhost:8080/test/upload_image"
DISTANCE_SERVER_URL = "http://localhost"
RESP_DISTANCE = 0.1212321
TIME = int(time() * 10 ** 9)


def add_upload_server_responses():
    responses.add(responses.POST, UPLOAD_SERVER_URL, status=204)


@responses.activate
def test_upload_image():
    add_upload_server_responses()
    stream = capture()
    stream.name = "test.png"
    assert upload_image(UPLOAD_SERVER_URL, stream).status_code == 204


def add_distance_server_responses():
    url = re.compile("{}/\\?time=\\d+".format(DISTANCE_SERVER_URL))
    responses.add(responses.GET, url, status=200, json={})
    responses.add(
        responses.GET,
        url,
        status=200,
        json={"time": TIME, "distance": RESP_DISTANCE},
    )


@responses.activate
def test_query_distance():
    add_distance_server_responses()

    now = int(time() * 10 ** 9)
    url = "{}/?time={}".format(DISTANCE_SERVER_URL, now)
    result = query_distance(url)
    assert bool(result) is False

    result = query_distance(url)
    assert result["distance"] == RESP_DISTANCE
    assert result["time"] == TIME


@responses.activate
def test_upload_image_if_distance_exist():
    add_distance_server_responses()
    add_upload_server_responses()
    upload_image_if_distance_exist(DISTANCE_SERVER_URL, UPLOAD_SERVER_URL)
    assert len(responses.calls) == 1
    upload_image_if_distance_exist(DISTANCE_SERVER_URL, UPLOAD_SERVER_URL)
    assert len(responses.calls) == 3
    msg = email.parser.BytesParser().parsebytes(responses.calls[2].request.body)
    filename = re.search('filename="(.*)"', msg.as_string()).group(1)
    matched = re.match(
        str(TIME)
        + r"_\d{19}_"
        + socket.gethostname()
        + "_"
        + str(RESP_DISTANCE)
        + ".jpg",
        filename,
    )
    assert matched is not None
