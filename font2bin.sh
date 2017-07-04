#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage : ./font2bin.sh src_font dst_font"
else
  if [[ -f fonts/$1 && -f fonts/$2 ]]; then
    FONT1=$(echo $1 | awk -F'.' '{print $(NF-1)}')
    FONT2=$(echo $2 | awk -F'.' '{print $(NF-1)}')
    FOLDER=${FONT1}-${FONT2}
    if [ ! -d image/$FOLDER ]; then
      echo "font2img.py $FONT1 $FONT2"
      mkdir -p image/$FOLDER
      python font2img.py --src_font=fonts/$1 --dst_font=fonts/$2 --sample_count=1000 --sample_dir=image/$FOLDER --label=0 --filter=1 --shuffle=1
    fi
    if [ ! -d binary/$FOLDER/data ]; then
      echo "package.py image/$FOLDER binary/$FOLDER/data"
      mkdir -p binary/$FOLDER/data
      python package.py --dir=image/$FOLDER --save_dir=binary/$FOLDER/data
    fi
  fi
fi
