txts=$( ls | grep *.txt )
mp4s=$( ls | grep *.mp4 )
pngs=$( ls | grep *.png )
if [ "$1" == "--dryrun" ]; then
    echo "rm -f $txts $mp4s $pngs"
elif [ "$1" == "--real" ]; then
    rm -f *.txt *.mp4 *.png
elif [ "$1" == "--movie" ]; then
    if [ -z "$2" ]; then
        echo "Must supply a movie directory to clean!"
    else
        rm -f $2/*
    fi
else
    echo "run with --dryrun, --real, or --movie as first argument"
fi
