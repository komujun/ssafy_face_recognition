#!/bin/sh
#open server and get data
LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1 python3 trainer.py
./on.sh