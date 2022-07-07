#!/bin/bash

# delete logs from previous pass
find "$(dirname "$0")" -name "*.log" -delete

./voice-gen.py voices/en-US.csv en-US-SaraNeural en_us-sara
./voice-gen.py voices/en-US.csv en-US-GuyNeural en_us-guy
./voice-gen.py voices/en-GB.csv en-IE-EmilyNeural en
./voice-gen.py voices/en-GB.csv en-GB-LibbyNeural en_gb-libby
./voice-gen.py voices/en-GB.csv en-GB-RyanNeural en_gb-ryan