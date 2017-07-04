#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage : ./train.sh src_font"
else
  if [[ -d binary/$1 ]]; then
    python train.py --experiment_dir=binary/batang --experiment_id=0 --batch_size=16 --lr=0.001 --epoch=40 --sample_steps=50 --schedule=20 --L1_penalty=100 --Lconst_penalty=15 2>&1 | tee train.log
  fi
fi
