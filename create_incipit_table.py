"""
Create incipit table based on the TEI per-sonnet version of the corpus.
@note: based on the dh2022 script for the same purpose
"""

from lxml import etree
import os
import re
from string import punctuation

import ameconfig as cf

TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
NSMAP = {"tei": TEI_NAMESPACE,
         "xml": 'http://www.w3.org/XML/1998/namespace'}


basepath = cf.teibasedir_for_incipits
out_table = cf.incipit_table

out_lines = []

punctuation = punctuation.replace("[", "").replace("]", "").replace("-", "")
punctuation = " ([" + re.escape(punctuation) + "-]+)$"


def clean_text(txt):
    txt = re.sub(r"\s{2,}", " ", txt)
    txt = re.sub(r"\n+", " ", txt)
    return txt


for per in cf.period_names:
    period_dir = os.path.join(basepath, per + os.sep + "per-sonnet")
    for fname in sorted(os.listdir(period_dir)):
        ffname = os.path.join(period_dir, fname)
        tree = etree.parse(ffname)
        # poem id
        poem_id_ele = tree.xpath("//tei:lg[@type='sonnet']", namespaces=NSMAP)[0]
        poem_id = poem_id_ele.attrib["{http://www.w3.org/XML/1998/namespace}id"]
        poem_id = re.sub(r"^s", "", poem_id)
        # author names
        has_last_name = False
        has_first_name = False
        use_short = False
        short = tree.xpath("//tei:persName[@type='short']/text()", namespaces=NSMAP)[0]
        for nm in ["Fray", "Marqués", "Escalante", "Duque", "Sor", "Cavalier"]:
            if nm in short:
                author_name = clean_text(short)
                use_short = True
        if not use_short:
            try:
                last_name = tree.xpath("//tei:persName[@type='full']/tei:surname/text()", namespaces=NSMAP)[0]
                has_last_name = True
            except IndexError:
                short = tree.xpath("//tei:persName[@type='short']/text()", namespaces=NSMAP)[0]
                if short != "":
                    author_name = clean_text(short)
            if has_last_name:
                try:
                    first_name = tree.xpath("//tei:forename/text()", namespaces=NSMAP)[0]
                    has_first_name = True
                except IndexError:
                    author_name = last_name
                if has_first_name:
                    try:
                        name_link = tree.xpath("//tei:nameLink/text()", namespaces=NSMAP)[0]
                    except IndexError:
                        name_link = ""
                    if name_link != "":
                        author_name = last_name + ", " + first_name + " " + name_link
                    else:
                        author_name = last_name + ", " + first_name
                    author_name = clean_text(author_name)
        # author id
        author_id = tree.xpath("//tei:titleStmt/tei:author/@resource", namespaces=NSMAP)[0]
        author_id = author_id.replace("disco:", "")
        author_id = re.sub(r"^s", "", author_id)
        author_id = re.sub(r"_.+", "", author_id)
        # incipit
        incipit_ele = tree.xpath("//tei:l", namespaces=NSMAP)[0]
        incipit_text = incipit_ele.xpath(".//text()")
        incipit = " ".join([x.strip() for x in incipit_text])
        incipit = re.sub(r"\s{2,}", " ", incipit)
        incipit = re.sub(r"^\n", " ", incipit).strip()
        has_punct = re.search(punctuation, incipit)
        if has_punct:
            incipit = re.sub(punctuation, r"\1", incipit)
        incipit = re.sub(r'"([\w ]+)"', r"«\1»", incipit)
        # titles
        try:
            sequence_title = \
                "".join([x.strip()
                         for x in tree.xpath("//tei:body/tei:head//text()",
                             namespaces=NSMAP)])
        except IndexError:
            sequence_title = ""
        if sequence_title != "":
            sequence_title = re.sub(r"^Part of:", "", sequence_title)
        title = tree.xpath("//tei:lg[@type='sonnet']/tei:head/text()", namespaces=NSMAP)[0]
        title = re.sub(r"\s{2,}", " ", title)
        title = re.sub(r"\n+", " ", title)
        if sequence_title != "":
            sequence_title = re.sub(r"\s{2,}", " ", sequence_title)
            sequence_title = re.sub(r"\n+", " ", sequence_title)
            title = sequence_title + " – " + title
        #out_lines.append("\t".join((poem_id, author_id, author, incipit, title)))
        out_lines.append((poem_id, author_id, author_name, incipit, title))
        #print("\t".join((poem_id, author_id, author, incipit, title)))


def extract_sort_key_from_poem_id(poid):
    period_sorter = ["g", "e", "n", "t"]
    parts = re.split(r"[_-]", poid)
    period_marker = re.search(r"([gnte])", parts[0])
    part1 = int(re.sub(r"[gnte]", "", parts[0]))
    part2 = int(parts[1])
    part3 = int(parts[2]) if len(parts) > 2 else 0
    return part1, period_sorter.index(period_marker.group(1)), part2, part3


out_list = sorted(out_lines,
    key=lambda x: extract_sort_key_from_poem_id(x[0]))


with open(out_table, mode="w", encoding="utf8") as ofh:
    ofh.write("poem_id\tauthor_id\tauthor\tincipit\ttitle\n")
    ofh.write("\n".join(["\t".join(x) for x in out_list]))
