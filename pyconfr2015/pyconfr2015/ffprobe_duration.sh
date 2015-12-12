cat videos.json | jq -r '.[] | .videos | .[] | .src' | grep --color=never ".ogv" | while read -r line ; do
    echo "Processing $line"
    ffprobe "$line" 2>&1 | grep -i duration:
    echo
done
