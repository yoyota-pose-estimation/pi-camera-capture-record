for index in {0..2}
do
    rsync -avzh --exclude=.git ./ picam$index:~/work/pi-camera-caputre-server
done
