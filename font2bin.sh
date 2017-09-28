#!/bin/bash

if [ "$#" -eq 0 ]; then
  echo "Usage : ./font2bin.sh src_font font_family ( font family ... )"
else
  if [ -f fonts/$1 ]; then
    echo "SRC FONT : "$1
    SRCFONT=$1
    FOLDER=$(echo $1 | awk -F'.' '{print $(NF-1)}')
    INDEX=1
    shift
    echo "Index  FONT" > mapping.log
    for FAMILY in "$@"
    do
      echo "FONT FAMILY : "$FAMILY
      if [ -d fonts/$FAMILY ]; then
	for TARGETFONT in $(find fonts/$FAMILY -type f | sort)
	do
	  echo "TARGET FONT : "$TARGETFONT
	  echo "font2img.py $SRCFONT $TARGETFONT"
	  mkdir -p image/$FOLDER
	  python font2img.py --src_font=fonts/$SRCFONT --dst_font=$TARGETFONT --sample_count=2000 --sample_dir=image/$FOLDER --label=${INDEX} --filter=1
	  TARGET=$(echo $TARGETFONT | awk -F'/' '{print $(NF)}')
	  echo "  $INDEX    $TARGET" >> mapping.log
	  ((INDEX++))
	done
      fi
    done
    echo "package.py image/$FOLDER binary/$FOLDER/data"
    mkdir -p binary/$FOLDER/data
    python package.py --dir=image/$FOLDER --save_dir=binary/$FOLDER/data
  else
    echo "Source font 'fonts/$1' not exist"
  fi
fi
