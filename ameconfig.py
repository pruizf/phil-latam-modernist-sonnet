"""Config for Darío and Chocano DISCO conversion"""

from collections import OrderedDict
import os
import re

indir = "raw_sources"

# paths
rawdir = "raw_sources"
mddir = "md"
outdir = "out"
# outdir_jumper = "out_jumper"

#   paths to ready TEI for further treatment (extract_annotations.py, inject_jumper_scansion.py)
phil_dir = "/home/ruizfabo/projects/pd/projects/potes/release_2021_v3/disco/tei/all-periods-per-author"
ame_dirs = ("out/out-19/tei/per-author", "out/out-20/tei/per-author")
ids_phil = [f"{aid}n" for aid in (692, 693)] + [f"00{aid}t" for aid in range(1,10)]
ids_ame = ["694n", "010t"]


# parsing
book_re = re.compile(r"""^(# .+)""", re.MULTILINE)
#sonnet_re = re.compile("""^\$.+?(?=^[$#])""", re.MULTILINE|re.DOTALL)
sonnet_re = re.compile("""\$.+?(?:\n(?=[$])|$)""", re.DOTALL)


TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
XML_NAMESPACE = "http://www.w3.org/XML/1998/"

# to output, don't add a tei prefix
NSMAP_W = {None: TEI_NAMESPACE, "xml": XML_NAMESPACE}
# to read TEI, do use the prefix
NSMAP = {"tei": TEI_NAMESPACE,
         "xml": XML_NAMESPACE}

# md
# disco public md
disco_md_table = os.path.join(mddir, "bkp_author_metadata.tsv")
new_disco_table = os.path.join(mddir, "new_md.tsv")
incipit_table = os.path.join(mddir, "incipits.tsv")
prosopography_fn = os.path.join(mddir, "prosopography.xml")
chocano_19 = False

# tei
# mode d = dario, c = chocano
ids_by_mode = {"d":
                 {"start_auid": 694,
                  "period_sfx": "n",
                  "start_soid": 2496,
                  "outdir_sfx": "19"},
               "c":
                 {"start_auid": 592,
                  "period_sfx": "n",
                  "start_soid": 182,
                  "outdir_sfx": "20"}
               }

fnshape_per_au = "disco{author_id}{period_sfx}.xml"
file_id_shape_per_au = "file_au_{author_id}{period_sfx}"
sonnet_id_shape = "s{author_id}{period_sfx}_{sonnet_id}"
sonnet_id_shape_inseq = "s{author_id}{period_sfx}_{sonnet_id}_{nbrinseq}"
teibasedir = "/home/ruizfabo/projects/pd/projects/potes/release_2021_v3/disco/tei"
period_names = ["15th-17th", "18th", "19th", "20th"]
teibasedir_for_incipits = "/home/ruizfabo/projects/pd/projects/potes/release_2021_v3/disco_for_incipits/tei"

# scansion

scan_with = "rantanplan"
assert scan_with in ("jumper", "rantanplan")
# dataframe with jumper results after manual correction
#jumper_results_without_corrections = os.path.join(outdir, "h23-df-plus-jumper.ods")
corrected_jumper_results = os.path.join(outdir, "2023-02-03-h23-df-plus-jumper.ods")

jumper_scansion_resp = """
               <resp>Metrical annotation done with <ref target="https://github.com/grmarco/jumper">Jumper</ref>, developed by</resp>
               """
jumper_scansion_resp_name = """
               <name>Guillermo Marco Remón</name>
               """

#TODO: add mention to manual corrections if applicable.
new_met_decl = """
         <metDecl type="met">
            <p>The metrical patterns were extracted automatically using the
             <ref target="https://github.com/grmarco/jumper">Jumper</ref> tool.
           </p>
           <p>The tool's output format is a series of numbers representing
             the position of stressed syllables. This was converted to a +/-
             notation to represent stressed and unstressed syllables.
           </p>
         </metDecl>
         """

#TODO: add to TEI mention to cimc manual corrections (in both phil and ame modes)
changes_to_jumper_met = ('<change when="2023-02-04" who="#prf">Automatic scansion reannotation with Jumper</change>')
manual_correction_to_jumper_met = ('\n              <change when="2023-02-10" who="#cimc">Manual corrections to automatic scansion</change>')

# enjambment
enj_results = "out/cleantxt_enj/out/" + \
              "ame-001_corpus_results_const_0_deps_1_sto_norules.txt.trans.txt"

# rhyme tagging (rt = Rhyme Tagger, tp = rantanplan)
rhyme_mode = "rt"
assert rhyme_mode in ("rt", "tp")

# titleStmt

principals = OrderedDict({
    "prf": "Pablo Ruiz Fabo",
    "heb": "Helena Bermúdez Sabel",
    "cimc": "Clara Isabel Martínez Cantón"
})

bibl_template = """                     <bibl resource="disco:{sonnet_id}"{source_id}>
                        <title property="dc:title">{sonnet_title}</title>
                        <title type="incipit" property="dc:alternative">{sonnet_incipit}</title>
                     </bibl>
"""

bibl_per_sonnet_template = """
                     <bibl resource="disco:{seq_id}">
                        <title property="dc:title">{seq_title}</title>
                        <title type="incipit" property="dc:alternative">{sonnet_incipit}</title>
                     </bibl>"""

sonnet_in_seq_head_template = """         <head>Part of: <title>{seq_title}</title>
         </head>"""

# debug

debug_groups = os.path.join(outdir, "debug_groups")

# lg exceptions

skip_sonnets = {"HELDA"}

lg_exceptions = {
  "EL SONETO DE TRECE VERSOS": {
    "split_at": None,
    "stanzas": [(0, 3), (4, 7), (8, 10), (11, 12)],
    "stanza_types": ["cuarteto", "cuarteto", "terceto", None]
  },
  "EN CASA DEL DOCTOR LUIS H. DEBAYLE TOAST": {
    "split_at": 14,
    "stanzas": [(0, 3), (4, 7), (8, 10), (11, 13), (14,19)],
    "stanza_types": ["cuarteto", "cuarteto", "terceto", "terceto", None]
  },
  "A MADAME OSVALDO BAZIL": {
    "split_at": None,
    "stanzas": [(0, 3), (4, 7), (8, 10), (11, 12)],
    "stanza_types": ["cuarteto", "cuarteto", "terceto", None]
  }
}

final_closing_tags = """</text></TEI>"""

