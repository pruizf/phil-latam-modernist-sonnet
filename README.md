Data and code for distant analysis of Hispano-Filipino Modernism vs. Latin-American Modernism
========================

This repository contains data and code for the following paper:

> Martínez Cantón, C., Ortuño Casanova, R., & Ruiz Fabo, P. (accepted) ¿Es el modernismo hispanofilipino una simple copia del latinoamericano? Un análisis distante de la forma y el contenido de dos corpus de sonetos [Is Hispano-Filipino Modernism a Mere Copy of Latin American Modernism? A Distant Analysis of the Form and Content of Two Sonnet Corpora], accepted in February 2024 to appear at [*Ogigia*](https://revistas.uva.es/index.php/ogigia).

## Final data

- The final data (including manual corrections) are at [`out/2023-02-03-h23-df-plus-jumper.ods`](out/2023-02-03-h23-df-plus-jumper.ods). They were generated as detailed below, including automatic annotations for metrics, rhyme and enjambment. Rhyme and metrical annotations were then corrected manually by Clara Martínez. 

## Sources

- `raw_sources_orig`: Original source files compiled by Clara and Rocío
- `raw_sources`: Use these for the workflow. These files have pseudo-markup for sonnet-sequences and more explicit pseudo-markup. These files also have somme corrections to the text

## Reproduce

Run this script with the relevant CLI options (see script for options):

```
create_corpus.sh
```

If ANJA results already available, run as below to output per-author and per-sonnet TEI including ANJA results, plus the text versions

```
create_corpus.sh -jti
```

If no ANJA results yet, can run as follows:

```
create_corpus.sh -nti
```

See script for other options (`-t` creates text versions (per-author and per-sonnet), and `-i` creates per-sonnet TEI files).

### Output dataframe

To create the annotation dataframe, do `python extract_annotations_to_df.py`. This outputs `out/h23-df.tsv`.

Dataframe fields are the following:

|field|meaning|
|---|---|
|aId|disco author id|
|sId|disco sonnet id|
|orig|ame, i.e. Chocano and Darío, or fil (Filipino)|
|au|author full name|
|title|sonnet title|
|incipit|incipit|
|irreg|1 if poem does not have 14 lines, otherwise 0|
|nbLin|number of lines|
|nbLg|number of `lg` elements|
|lnNbr|line number|
|lnTxt|line text|
|met|metrical scheme|
|rhys|rhyme scheme|
|rw|rhyme word|
|r1|regular sonnets only: rhyme scheme for stanza 1|
|r2|regular sonnets only: rhyme scheme for stanza 2|
|r3|regular sonnets only: rhyme scheme for stanza 3|
|r4|regular sonnets only: rhyme scheme for stanza 4|
|enj|1 if has enjambment, otherwise 0|
|ent|enjambment type|

## Details

The paragraphs below describe the workflow.

We created files in several steps.

### Initial versions

First the per-author TEI were created with `txt2tei.py`. Then based on that, the per-sonnet TEI and both per-author and per-sonnet text versions were created, with XSLT.

### Enjambment

Then enjambment annotations are obtained based on the per-sonnet text versions. Then the procedure was run again to inject the enjambment results into the per-author files, and the per-sonnet files are generated again.

For ANJA, the following command was run:

```

python2 run_anja.py -b ame-001 -i 'out/cleantxt' -n 'out/cleantxt_enj/nlp' -p 'out/cleantxt_enj/pos' -o 'out/cleantxt_enj/out' -l 'out/cleantxt_enj/logs' -e 'out/cleantxt_enj/prepro'
```

The results are at `out/cleantxt_enj/out/ame-001_corpus_results_const_0_deps_1_sto_norules.txt`

In order to process the results, a header was added:

```
sonnet\tstart\tend\ttype\tdummy\ttype2\tdummy2
```

Tags were translated to English with `scripts/translate_anja_tags.py` at the tool's location, giving `out/cleantxt_enj/out/ame-001_corpus_results_const_0_deps_1_sto_norules.txt`.

### Metrical reannotation

The files were reannotated for metrics, as follows:

- The scansion tool originally chosen was Rantanplan, but it became clear that Jumper performs better with this corpus (given the large proprotion of complex meter, with ≥ 12 metrical syllables). So we did the following:
    - Reannotate with Jumper, in two ways:
        - Giving entire subcorpora to the tool (Latin American vs. Filipino), with `jumper_scansion.py` preceded by `collect_filipino_text.sh`.
        - Doing per-poem scansion; it is configurable in `ameconfig.py` whether Rantanplan or Jumper will be used, and scansion takes place per poem, when generating the TEI with `txt2tei.py`
    - Given that per-subcorpus results were better, we adopted these, they were manually corrected by Clara (`out/2023-02-03-h23-df-plus-jumper.ods`) and they were reinjected in the per-author TEI with `inject_jumper_scansion.py` 

### Corpus splits

As regards the creation of the different ways to present the content in this corpus (`per-author` and `per-sonnet` splits), the paragraphs below describe each script, but `create_corpus.sh` already automates most of the workflow, with options to select which parts to run.

#### TEI Per-author files

From folder containing this readme:

```
python txt2tei.py
```

This will generate per-author files that contain at:
- `out/out-19/per-author`
- `out/out-20/per-author`

#### TEI Per-sonnet files

- With saxon and `../xslt/per-sonnet.xsl` based on the per-author files above

#### Text versions

Two XSLT for this:
  - `../xslt/tei2txt_per-author.xsl`: Generates per-author directories in the TXT distribution of the corpus (under `per-author`, one directory per author, named by author ID, and all poems by the author inside it)
  - `../xslt/tei2txt_per-sonnet.xsl`: Generates per-sonnet TXT files
    
Both take the per-sonnet TEI directories as their input.

### Other processing

Some textual errors were corrected by Clara in the dataframe with the metrics results, these corrections were reflected back into the TEI corpus with `source_corrections.py`.

### Metadata tables and documentation

Note that these metadata creation scripts do not affect the TEI and some of these scripts may read off the directories for the public repository, or a local directory structure that closely follows it (they do not necessarily read off the results available here)

- `create_incipit_table.py`: Its result is what gets published as `poem_metadata.tsv` in the public repo
- `create_distribution_table.py`: Outputs the corpus distribution used in the public [README](https://github.com/pruizf/disco#data-distribution). Reads sonnet IDs among other metdata in the per-author files to get the counts 
- `extract_prosopography.py`: The teiHeader now contains all the personography information (unlike early versions of the corpus), but we're still keeping the external personography. So this reproduces teiHeader information into `md/prosopography.xml`

### Public versions

- The TEI were copied to the public repository, but the author ID for Chocano was modified prior to that (which affects file names for this author, their content and the content of metadata tables). This was done to maintain the same practice as in earlier releases, where authors some of whose production takes place up to 1936 are kept together with other 19th-century authors. Given this, his ID was changed to `592n` (a 19th-century ID in this corpus) instead of `010t` and (in `create_corpus.sh`) the files were copied to the `19th` directories.
- Other modifications done directly in the public repo:
    - Changing last name for Chocano to "Santos Chocano" in the relevant `teiHeader` elements and in the metadata tables like `poem_metadata.tsv`
    - Adding schema declaration to individual sonnets (so far it was only there in the per-author sonnets that the individual sonnets are generated from), with `add_schema_declaration_to_indiv_sonnets.sh`
    - Upon validation, five 20th-century individual sonnets coming from two sonnet sequences had validation errors, these were corrected directly by hand instead of looking to debug the XSLT or other source of error:
       - Author: 003t, Sequence: 0039, Sonnets: 01 02 03
       - Author: 007t, Sequence: 0150, Sonnets: 01 02
