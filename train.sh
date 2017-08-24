#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage : ./train.sh src_font"
else
  if [[ -d binary/$1 ]]; then
    python train.py --experiment_dir=binary/$1 --experiment_id=0 --batch_size=16 --lr=0.001 --epoch=60 --sample_steps=100 --schedule=20  --L1_penalty=100 --Lconst_penalty=15 --freeze_encoder=1
    python train.py --experiment_dir=binary/$1 --experiment_id=0 --batch_size=16 --lr=0.001 --epoch=30 --sample_steps=100 --schedule=10  --L1_penalty=500 --Lconst_penalty=1000 --freeze_encoder=1
  else
    echo "Binay folder 'binary/$1' not exist"
  fi
fi
