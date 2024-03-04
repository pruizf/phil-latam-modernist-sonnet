#!/usr/bin/env bash

# ./create-corpus -j will add enjambment results to per-author files
#                 -n will create per author files without enjambment
#                 -p will collect text per-author and run Jumper on it
#                 -x will reannotate @met given a dataframe with jumper results
#                 -i will create per-sonnet files in TEI
#                 -t will create text versions
#                 -d copies the outputs to the directory with DISCO public repo
#                 -v copies the outputs to directory from where the DISCOver scripts create the DB

while getopts "jnitpvdx" opt; do
  case "$opt" in
    j) AUTHOR_TEI_WITH_ENJ=1
    ;;
    n) AUTHOR_TEI_NO_ENJ=1
    ;;
    p) RUN_JUMPER=1
    ;;
    x) REANNOTATE_MET_FROM_JUMPER_DF=1
    ;;
    i) INDIV_TEI=1
    ;;
    t) CREATE_TEXT=1
    ;;
    d) COPY_TO_PUBLIC=1
    ;;
    v) COPY_TO_DISCOVER_REPO=1
    ;;
    *)
    echo "Incorrect options"
    exit 1
    ;;
  esac
done

# XSLT
SAXON=/home/ruizfabo/usr/local/saxon9he.jar

PER_SONNET_TEI_XSL=../xslt/per-sonnet.xsl
PER_AUTHOR_TXT_XSL=../xslt/tei2txt_per-author.xsl
PER_SONNET_TXT_XSL=../xslt/tei2txt_per-sonnet.xsl

# TEI
PER_AUTHOR_19=out/out-19/tei/per-author
PER_AUTHOR_19_JUMPER=out/out-19/tei-jumper/per-author
PER_AUTHOR_20=out/out-20/tei/per-author
PER_AUTHOR_20_JUMPER=out/out-20/tei-jumper/per-author
PER_SONNET_19=out/out-19/tei/per-sonnet
PER_SONNET_20=out/out-20/tei/per-sonnet
PER_SONNET_19_JUMPER=out/out-19/tei-jumper/per-sonnet
PER_SONNET_20_JUMPER=out/out-20/tei-jumper/per-sonnet

# TXT
PER_AUTHOR_19_TXT=out/out-19/txt/per-author
PER_AUTHOR_20_TXT=out/out-20/txt/per-author
PER_SONNET_19_TXT=out/out-19/txt/per-sonnet
PER_SONNET_20_TXT=out/out-20/txt/per-sonnet

# PUBLIC DISCO
PUBLIC_REPO=../../../disco_last_release/disco_for_incipits

# DISCOVER TEI (tei to feed to DISCOver scripts)

DISCOVER_TEI=../../discover_2023/tei-files

# create per-author TEI

function echo_per_author_creation(){
  echo "# Per-author TEI creation " $(date '+%Y-%m-%d %H:%M:%S')
  echo -e "\n"
}

if [[ $AUTHOR_TEI_WITH_ENJ == 1 ]]; then
    echo_per_author_creation
    python txt2tei.py -e;
  elif [[ $AUTHOR_TEI_NO_ENJ == 1 ]]; then
    echo_per_author_creation
    python txt2tei.py
fi

# reannotate from Jumper df

if [[ $REANNOTATE_MET_FROM_JUMPER_DF == 1 ]]; then
  echo -e "\n# Inject Jumper results in per-author TEI " $(date '+%Y-%m-%d %H:%M:%S')
  echo -e "\n"
  python inject_jumper_scansion.py
fi

# create per-sonnet TEI


if [[ $INDIV_TEI == 1 ]]; then
  echo -e "# Per-sonnet TEI creation " $(date '+%Y-%m-%d %H:%M:%S')
  echo -e "\n"
  if [[ $REANNOTATE_MET_FROM_JUMPER_DF == 1 ]]; then
      PER_AUTHOR_19=$PER_AUTHOR_19_JUMPER
      PER_AUTHOR_20=$PER_AUTHOR_20_JUMPER
      PER_SONNET_19=$PER_SONNET_19_JUMPER
      PER_SONNET_20=$PER_SONNET_20_JUMPER
  fi
  for indivdir in $PER_SONNET_19 $PER_SONNET_20; do
    echo "- Creating " $indivdir " if don't exist"
    [[ ! -d $indivdir ]] && mkdir -p $indivdir
  done
  echo "- Creating per-sonnet TEI"
  java -jar $SAXON -s:$PER_AUTHOR_19 -xsl:$PER_SONNET_TEI_XSL -o:$PER_SONNET_19
  java -jar $SAXON -s:$PER_AUTHOR_20 -xsl:$PER_SONNET_TEI_XSL -o:$PER_SONNET_20
fi

# extract sonnet texts

if [[ $CREATE_TEXT == 1 ]]; then
    echo -e "\n# TXT versions creation " $(date '+%Y-%m-%d %H:%M:%S')
    echo -e "\n"

    for txtdir in $PER_AUTHOR_19_TXT $PER_AUTHOR_20_TXT $PER_SONNET_19_TXT $PER_SONNET_20_TXT; do
      echo "- Creating " $txtdir " if don't exist"
      [[ ! -d $txtdir ]] && mkdir -p $txtdir
    done

    echo "- Creating TXT versions"
    java -jar $SAXON -s:$PER_SONNET_19 -xsl:$PER_AUTHOR_TXT_XSL -o:$PER_AUTHOR_19_TXT
    java -jar $SAXON -s:$PER_SONNET_19 -xsl:$PER_SONNET_TXT_XSL -o:$PER_SONNET_19_TXT

    java -jar $SAXON -s:$PER_SONNET_20 -xsl:$PER_AUTHOR_TXT_XSL -o:$PER_AUTHOR_20_TXT
    java -jar $SAXON -s:$PER_SONNET_20 -xsl:$PER_SONNET_TXT_XSL -o:$PER_SONNET_20_TXT
fi

# copy to discover

if [[ $COPY_TO_DISCOVER_REPO == 1 ]]; then
  echo -e "\n# Copying to DISCOver repo " $(date '+%Y-%m-%d %H:%M:%S')
  echo -e "\n"
  cp $PER_AUTHOR_19_JUMPER/* $DISCOVER_TEI
  cp $PER_AUTHOR_20_JUMPER/* $DISCOVER_TEI
fi

# copy to public
#   tei copied from out-(19|20)/tei-jumper, txt simply from out-(19|20)/txt
#   all copied to 19th (even if in intermediate steps it was divided into 19th/20th)
#   because of criteria adopted in DISCO for the directories
#   (authors producing up to 1936 so far in 19th)

if [[ $COPY_TO_PUBLIC ]]; then
  # tei per author
  cp -r $PER_AUTHOR_19_JUMPER/* $PUBLIC_REPO/tei/19th/per-author
  cp -r $PER_AUTHOR_19_JUMPER/* $PUBLIC_REPO/tei/all-periods-per-author
  cp -r $PER_AUTHOR_20_JUMPER/* $PUBLIC_REPO/tei/19th/per-author # sic
  cp -r $PER_AUTHOR_20_JUMPER/* $PUBLIC_REPO/tei/all-periods-per-author
  # tei per sonnet
  cp $PER_SONNET_19_JUMPER/* $PUBLIC_REPO/tei/19th/per-sonnet
  cp $PER_SONNET_20_JUMPER/* $PUBLIC_REPO/tei/19th/per-sonnet # sic
  # txt per author
  cp -r $PER_AUTHOR_19_TXT/* $PUBLIC_REPO/txt/19th/per-author
  cp -r $PER_AUTHOR_20_TXT/* $PUBLIC_REPO/txt/19th/per-author # sic
  #  txt all in one file per author
  for dname in $(ls $PER_AUTHOR_19_TXT | sort); do
    PUBLIC_ALL_TXT_FOR_AU=$PUBLIC_REPO/txt/19th/per-author/one-file-per-author
    [[ ! -d $PUBLIC_ALL_TXT_FOR_AU ]] && mkdir $PUBLIC_ALL_TXT_FOR_AU
    [[ -f $PUBLIC_ALL_TXT_FOR_AU/${dname}.txt ]] && continue
    for fname in $(ls $PER_AUTHOR_19_TXT/$dname | sort); do
      cat $PER_AUTHOR_19_TXT/$dname/$fname >> $PUBLIC_ALL_TXT_FOR_AU/${dname}.txt
      echo -e "\n" >> $PUBLIC_ALL_TXT_FOR_AU/${dname}.txt
    done
  done
  for dname in $(ls $PER_AUTHOR_20_TXT | sort); do
    PUBLIC_ALL_TXT_FOR_AU=$PUBLIC_REPO/txt/19th/per-author/one-file-per-author # sic
    [[ ! -d $PUBLIC_ALL_TXT_FOR_AU ]] && mkdir $PUBLIC_ALL_TXT_FOR_AU
    [[ -f $PUBLIC_ALL_TXT_FOR_AU/${dname}.txt ]] && continue
    for fname in $(ls $PER_AUTHOR_20_TXT/$dname | sort); do
      cat $PER_AUTHOR_20_TXT/$dname/$fname >> $PUBLIC_ALL_TXT_FOR_AU/${dname}.txt
      echo -e "\n" >> $PUBLIC_ALL_TXT_FOR_AU/${dname}.txt
    done
  done
  # txt per sonnet
  cp $PER_SONNET_19_TXT/* $PUBLIC_REPO/txt/19th/per-sonnet
  cp $PER_SONNET_20_TXT/* $PUBLIC_REPO/txt/19th/per-sonnet # sic
  if false; then # no need to remove as ID is now gonna be kept
    # remove files for the former Chocano ID
    # no longer needed since gonna keep in 19th folder (DISCO criteria)
    rm $PUBLIC_REPO/tei/19th/per-author/disco592n.xml
    rm $PUBLIC_REPO/tei/19th/per-sonnet/disco592n_*.xml
    rm $PUBLIC_REPO/tei/all-periods-per-author/disco592n.xml
    rm -r $PUBLIC_REPO/txt/19th/per-author/disco592n
    rm -r $PUBLIC_REPO/txt/19th/per-author/one-file-per-author/disco592n.txt
    rm $PUBLIC_REPO/txt/19th/per-sonnet/disco592n_*.txt
  fi
fi
