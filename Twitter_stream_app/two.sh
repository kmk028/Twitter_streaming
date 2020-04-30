#!/bin/bash
set -m

nohup python streamer.py &

python app.py
