#!/usr/bin/env bash

indiv_19=out/out-19/tei/per-sonnet
indiv_20=out/out-20/tei/per-sonnet
indiv_19_jumper=out/out-19/tei-jumper/per-sonnet
indiv_20_jumper=out/out-20/tei-jumper/per-sonnet

schema_decl='<?xml-model href="https://raw.githubusercontent.com/pruizf/disco/master/schema/tei_all_DISCO.rnc" type="application/relax-ng-compact-syntax"?>'

sed -i "2i $schema_decl" $indiv_19/*
sed -i "2i $schema_decl" $indiv_20/*
sed -i "2i $schema_decl" $indiv_19_jumper/*
sed -i "2i $schema_decl" $indiv_20_jumper/*