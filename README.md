# pi camera capture
upload picamera image base on influxdb query result

## Usage

```shell
# sleep 10
# systemctl stop ntp
# ntpdate -u ntp_server
# systemctl start ntp
# sleep 60
pi-camera-capture time-query-server upload-minio-server/bucket/directory
```
