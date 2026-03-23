#!/bin/bash
cd /home/admin/.openclaw/workspace/blog
while true; do
    python3 app.py >> /tmp/blog-daemon.log 2>&1
    echo "Restarting..." >> /tmp/blog-daemon.log
    sleep 2
done
