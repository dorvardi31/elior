#!/bin/bash

python data_processing.py &
python fileupload.py &
wait
