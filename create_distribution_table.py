"""
Extract data about corpus distribution per period, gender, origin.
"""

from lxml import etree
import os

TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
XML_NAMESPACE = "http://www.w3.org/XML/1998/"

# to output, don't add a tei prefix
NSMAP_W = {None: TEI_NAMESPACE, "xml": XML_NAMESPACE}
# to read TEI, do use the prefix
NSMAP = {"tei": TEI_NAMESPACE,
         "xml": XML_NAMESPACE}

#tei_dir = "/home/ruizfabo/projects/pd/projects/potes/release_2021_v3/disco_for_incipits/tei/all-periods-per-author"
tei_dir = "/home/ruizfabo/projects/pd/projects/potes/disco_last_release/disco/tei/all-periods-per-author"
files_to_treat = sorted(os.listdir(tei_dir))

letter2period = {"g": "15th-17th", "e": "18th", "n": "19th", "t": "20th"}

for period_letter in ("g", "e", "n", "t"):
  md = {"gender": {}, "origin": {}, "sonnets": 0, "authors": 0, "tokens": 0,
        "author_countries": {}}
  period_author_files = [os.path.join(tei_dir, fn) for fn in files_to_treat
                         if f"{period_letter}.xml" in fn]
  for ffn in period_author_files:
    md["authors"] += 1
    tree = etree.parse(ffn)
    au_gender = tree.xpath("//tei:sex/@content", namespaces=NSMAP)[0]
    md["gender"].setdefault(au_gender, 0)
    md["gender"][au_gender] += 1
    au_origin = tree.xpath("//tei:birth/descendant::tei:bloc", namespaces=NSMAP)[0].text
    md["origin"].setdefault(au_origin, 0)
    md["origin"][au_origin] += 1
    try:
      au_country= tree.xpath("//tei:birth/descendant::tei:country", namespaces=NSMAP)[0].text
    except IndexError:
      au_country = "unknown"
    md["author_countries"].setdefault(au_country, 0)
    md["author_countries"][au_country] += 1
    md["sonnets"] += len(tree.xpath("//tei:lg[@type='sonnet']", namespaces=NSMAP))
    md["tokens"] += int(
      tree.xpath("//tei:extent/tei:measure[@unit = 'tokens']", namespaces=NSMAP)[0].text)
  print(letter2period[period_letter])
  for mdtype in ("sonnets", "authors", "tokens", "origin"):
    print(mdtype, md[mdtype])
  print("author_countries", sorted(md["author_countries"].items(), key=lambda x: -x[-1]), "\n")
