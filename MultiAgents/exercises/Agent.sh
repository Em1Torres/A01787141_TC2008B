#!/bin/bash

channel="UCX6OQ3DkcsbYNE6H8uQQuVA"

: "${YOUTUBE_API_KEY:?Set your YouTube API key first}"

echo "# MrBeast Subscribers Monitor" > Info.md
echo "| Date | Subscribers |" >> Info.md
echo "|---|---|" >> Info.md

while true
do
    response=$(curl -fsS --get \
        "https://www.googleapis.com/youtube/v3/channels" \
        --data-urlencode "part=statistics" \
        --data-urlencode "id=$channel" \
        --data-urlencode "key=$YOUTUBE_API_KEY")

    if [ $? -eq 0 ]; then
        subs=$(echo "$response" | jq -r \
            '.items[0].statistics.subscriberCount // empty')
    else
        subs=""
    fi

    if [ -z "$subs" ]; then
        subs="Not available"
        echo "Could not retrieve subscriber count"
    fi

    echo "Subscribers: $subs"

    echo "| $(date '+%Y-%m-%d %H:%M:%S') | $subs |" >> Info.md

    sleep 60
done