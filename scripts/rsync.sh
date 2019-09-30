for index in 3 
do
    rsync -avzh --exclude=.git ./ picam$index:~/work/pi-camera-capture-server
done

# {0..2}