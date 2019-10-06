for index in {0..3}
do
    rsync -avzh --exclude=.git ./ picam$index:~/work/pi-camera-capture-record
done
