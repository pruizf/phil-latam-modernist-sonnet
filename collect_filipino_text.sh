#!/usr/bin/env bash

outfile=raw_sources/all_filipino_text.txt
[[ -f $outfile ]] && rm $outfile
fildir=/home/ruizfabo/projects/pd/projects/potes/disco_private_2022/disco_private/dh2022/out/cleantxt

touch $outfile
for x in $(ls $fildir) ; do
  cat $fildir/$x >> $outfile
  echo -e "\n" >> $outfile
done