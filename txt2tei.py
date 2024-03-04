"""
Text to TEI conversion for JS Chocano and R Darío sonnets
"""

from _collections import OrderedDict
import html
from importlib import reload
from lxml import etree
from nltk import word_tokenize
import os
import pandas as pd
from pprint import pprint
import re
from rantanplan.core import get_scansion
from rhymetagger import RhymeTagger
from string import ascii_uppercase
from string import punctuation
import spacy
import sys
from time import localtime, strftime

import ameconfig as cf
from data.header_dario_per_author import header_dario_pa
from data.header_chocano_per_author import header_chocano_pa
from external import jumper

DBGV = True


def filter_line(line):
  """Return True if line passes the filters"""
  return line.strip() != '' and not re.search(r"^\d+$", line.strip())


def clean_title(txt):
  """Clean some errors seen in the source"""
  txt = re.sub(r" {2,}", " ", txt)
  txt = txt.replace(". ..", "...")
  txt = re.sub(r'"([^"]+)"', r"«\1»", txt)
  return txt


def clean_text(txt):
  """Clean some errors seen in the source"""
  txt = re.sub(r" {2,}", " ", txt)
  txt = txt.replace(". ..", "...")
  return txt


def split_file_into_sonnets(fname, mode="d"):
  """
  Extract sonnets from either Darío or Chocano file.
  Returns OrderedDict mapping the book-title line to a sonnet list,
  in the list each sonnet is contained in a dictionary.
  """
  assert mode in ("c", "d")
  total_sonnets = 0
  sonnet_list = []
  last_id = cf.ids_by_mode[mode]["start_soid"]
  with open(fname, mode="r", encoding="utf8") as infi:
    txt = infi.read()
  sonnets = re.findall(cf.sonnet_re, txt)
  offset = None
  add_to_seq = False
  for idx, sonnet in enumerate(sonnets):
    lines = re.split(r"(?:\r?\n)+", sonnet)
    title_raw = re.sub("^\$", "", lines[0])
    # to handle sonnet sequences
    # note that a sonnet can start a seq and be the first one after the previous seq
    is_seq_start = True if "##SS" in title_raw else False
    previous_ends_seq = True if "##SO" in title_raw else False
    # initial sonnet IDs
    # note: 'soid' field useless cos want to number IN AUTHOR ORDER, and sonnets
    #       get regrouped later by author. Will be renumbered later
    #       still, the 'offset' field that shows whether the sonnet is sequence-first,
    #       sequence-internal or indepenedent is used later when renumbering
    soid = last_id + idx
    if is_seq_start:
      offset = 0
      add_to_seq = True
    if previous_ends_seq and not is_seq_start:
      add_to_seq = False
    title = re.sub(r"##S[SO]", "", title_raw)
    if title in cf.skip_sonnets:
      print(f"- Skipping {title}")
      continue
    sdict = {"title": clean_title(title.strip()),
             "lines": [clean_text(line.strip()) for line in lines[1:] if filter_line(line)],
             "is_seq_start": is_seq_start,
             "previous_ends_seq": previous_ends_seq,
             "soid": soid, "nbrinseq": None}
    # dedications
    dedications = [(idx, ll) for idx, ll in enumerate(sdict["lines"])
                   if ll.startswith("*")]
    if len(dedications) > 0:
      #breakpoint()
      for idx, dedication in dedications:
        assert idx < 2
      keep_lines = sdict["lines"][dedications[-1][0]+1:]
      sdict["lines"] = keep_lines
      sdict["dedication"] = [dd[1].strip("*") for dd in dedications]

    if add_to_seq:
      sdict.update({"nbrinseq": offset})
      offset += 1
      # DBGV and print(sdict)
    sonnet_list.append(sdict)
  print(f"- Total sonnets: {len(sonnet_list)}")
  return sonnet_list


def group_sequences(sl, mode="d"):
  """
  Given list of sonnet dicts in `sl`, create unique entries
  for sonnet sequences; the sonnets for each sequence will
  be in a list of dicts in the sequence "sonnets" field
  """
  sl2 = []
  last_id = cf.ids_by_mode[mode]["start_soid"] - 1
  new_source = False
  for idx, sdict in enumerate(sl):
    assert "nbrinseq" in sdict
    # sequence
    if sdict["nbrinseq"] is not None:
      if sdict["is_seq_start"]:
        last_id += 1
        itemdict = {"item_type": "sequence",
                    "item_title": sdict["title"],
                    "item_id": \
                      cf.sonnet_id_shape.format(
                        author_id=str.zfill(str(cf.ids_by_mode[mode]['start_auid']), 3),
                        period_sfx=cf.ids_by_mode[mode]['period_sfx'],
                        sonnet_id=str.zfill(str(last_id), 4)),
                    "sonnets": [],
                    "flag": "is_seq_start",
                    "source": "new" if new_source else "old"}
        sl2.append(itemdict)
      else:
        sl2[-1]["sonnets"].append(
          {"item_title": sdict["title"] \
            if len(sdict["title"].strip()) > 0 else sdict["lines"][0] + "...",
           "item_id": cf.sonnet_id_shape_inseq.format(
             author_id=str.zfill(str(cf.ids_by_mode[mode]['start_auid']), 3),
             period_sfx=cf.ids_by_mode[mode]['period_sfx'],
             sonnet_id=str.zfill(str(last_id), 4),
             nbrinseq=str.zfill(str(sdict["nbrinseq"]), 2)
           ),
           "lines": sdict["lines"],
           "item_type": "inseq",
           "nbrinseq": sdict["nbrinseq"]})
        if "dedication" in sdict:
          sl2[-1]["sonnets"][-1]["dedication"] = sdict["dedication"]
    # individual sonnet
    else:
      last_id += 1
      itemdict = {"item_type": "indiv",
                  "item_title": sdict["title"],
                  "item_id": \
                    cf.sonnet_id_shape.format(
                      author_id=str.zfill(str(cf.ids_by_mode[mode]['start_auid']), 3),
                      period_sfx=cf.ids_by_mode[mode]['period_sfx'],
                      sonnet_id=str.zfill(str(last_id), 4)),
                  "source": "new" if new_source else "old",
                  "sonnets": [{"lines": sdict["lines"]}]}
      if "dedication" in sdict:
        itemdict["sonnets"][-1]["dedication"] = sdict["dedication"]
      sl2.append(itemdict)
    if sdict["title"] == "Ahora es dolor":
      print("- Switching to Chocano new source")
      new_source = True
  return sl2


def create_bibl(sl, mode="c"):
  """
  Create strings representing bibl elements for the per-author
  sonnets based on sonnet-dict list in `sl`.
  """
  out_bibl = []
  for idx, it in enumerate(sl):
    # we ignore level below the sequence
    #  only Chocano (mode c) has more than one source
    if mode == "c":
      source_str = ' source="#antologia"' if it["source"] == "old" else ' source="#completas-I #completas-II"'
    else:
      source_str = ''
    sonnet_bibl = cf.bibl_template.format(
      sonnet_id=it["item_id"],
      source_id=source_str,
      sonnet_title=it["item_title"],
      # Sequence incipit is incipit for its first poem.
      # In single sonnets the sonnet is also inside the it["sonnets"] list
      sonnet_incipit=it["sonnets"][0]["lines"][0].strip(punctuation)
    )
    out_bibl.append(sonnet_bibl)
  return "\n".join(out_bibl)


def define_quatrain_type(rs):
  """Given rhmye-scheme in `rs` (for a quatrain), return
     whether quatrain has enclosed or alternate rhyme.
     Rhyme-scheme will be in ABAB format, missing rhymes
     will be a hyphen.
  """
  # exceptions
  if rs == ['A', 'C', 'A']:
    return "cuarteto"
  elif (((rs[0] == rs[2] and rs[1] == rs[3]) or
      (rs[0] == rs[2] and "-" in (rs[1], rs[3])) or
      (rs[1] == rs[3] and "-" in (rs[0], rs[2]))) and
     # avoid AAAA or A-AA and such
     len(set([x for x in rs if x != "-"])) > 1):
    return "serventesio"
  else:
    return "cuarteto"


def create_tei_per_author(sl, bibl_list, enj_info,
                          mode="d", add_enjambment=False,
                          scan_tool=cf.scan_with):
  """
  Given list of sonnet dicts, create body elements. Then serialize and
  concatenate with chains for header and final closing tags.
  `bibl_list` is an already created string with the bibl info, `enj_info`
  is a dataframe with enjambment results (anja). The `mode` determines
  configuration settings to use and IO. `add_enjambment` determines whether enjambment
  results will be processed or not. (We first generate TEI without, and then with).
  """
  assert scan_tool in ("rantanplan", "jumper")

  print("- Create per author TEI")
  nlp = spacy.load("es_core_news_md")

  rt = RhymeTagger()
  rt.load_model(model="es", verbose=False)

  body = etree.Element("body")
  for idx, it in enumerate(sl):
    # prepare top element for either sequence or single sonnet
    if it["item_type"] == "sequence":
      top_ele = etree.SubElement(body, "lg", type="sonnet-sequence",
                                xmlid=it["item_id"])
      top_head = etree.SubElement(top_ele, "head")
      top_head.text = it["item_title"]
    else:
      top_ele = body
    # individual sonnets
    for son in it["sonnets"]:
      # define ID
      if it["item_type"] == "sequence":
        xml_id = son["item_id"]
        son_title = son["item_title"]
      else:
        xml_id = it["item_id"]
        son_title = it["item_title"]
      indiv_sonnet_lg = etree.SubElement(top_ele, "lg", type="sonnet",
                                         xmlid=xml_id)
      indiv_sonnet_head = etree.SubElement(indiv_sonnet_lg, "head")
      indiv_sonnet_head.text = son_title

      # scansion
      poem_text = re.sub(r"\n{2,}", "\n", "\n".join(son["lines"]))
      # if "y ufanos" in poem_text:
      #   breakpoint()
      #TODO: create function to produce scansion results
      #TODO (uniform format across tools), then call it here
      if scan_tool == "rantanplan":
        scansion = get_scansion(poem_text, rhyme_analysis=True)
      elif scan_tool == "jumper":
        scansion = []
        scansion_jumper_orig = jumper.escandir_texto(poem_text)
        for line_info in scansion_jumper_orig:
          # When translating this to +/- notation, we can only have metrical syllable sequences
          # i.e. +- at end of line (or hemistich) will be output regardless of whether that +
          # means an end-stressed word, penult or antepenult
          line_sign_list = ["-" for x in range(line_info[2])]
          for position in line_info[3]:
            line_sign_list[position-1] = "+"
          scansion.append("".join(line_sign_list))
          #scansion.append(" ".join([str(x) for x in scansion_jumper_orig[3]]))
      assert len(scansion) == len(son["lines"])

      # rhyme analysis
      rhymes = rt.tag(son["lines"], output_format=3)
      rhymes_letters = [ascii_uppercase[typ - 1]
                        if typ is not None else "-" for typ in rhymes]

      # enjambment
      if add_enjambment:
        has_enj = False
        #breakpoint()
        enj4sonnet = enj_info.loc[enj_info['sonnet'] == \
                                  re.sub("^s", "disco", xml_id)]
        if enj4sonnet.empty:
          print("  - No enjambment: [{}]".format(xml_id))
        else:
          has_enj = True
      else:
        enj4sonnet = None

      # stanzas
      #  prepare lg elements
      lg_c1 = etree.SubElement(indiv_sonnet_lg, "lg", n="1",
                               type=define_quatrain_type(rhymes_letters[0:4]))
      lg_c2 = etree.SubElement(indiv_sonnet_lg, "lg", n="2",
                               type=define_quatrain_type(rhymes_letters[4:8]))
      lg_t1 = etree.SubElement(indiv_sonnet_lg, "lg", n="3", type="terceto")

      #  last stanza: Darío exceptions: TRECE VERSOS, OSVALDO BAZIL
      if son_title in cf.lg_exceptions and len(cf.lg_exceptions[son_title]["stanza_types"]) == 4:
          lg_t2_type = None
      else:
        lg_t2_type = "terceto"
      lg_t2 = etree.SubElement(indiv_sonnet_lg, "lg", n="4")
      if lg_t2_type != None:
        lg_t2.attrib["type"] = lg_t2_type

      #  add annotations
      done_lines = 0
      for line in son["lines"][0:4]:
        add_line_element(nlp, lg_c1, line)
        done_lines = add_metrics_rhyme_and_enj(
          lg_c1, scansion, rhymes_letters, done_lines, enj4sonnet)
      for line in son["lines"][4:8]:
        add_line_element(nlp, lg_c2, line)
        done_lines = add_metrics_rhyme_and_enj(
          lg_c2, scansion, rhymes_letters, done_lines, enj4sonnet)
      for line in son["lines"][8:11]:
        add_line_element(nlp, lg_t1, line)
        done_lines = add_metrics_rhyme_and_enj(
          lg_t1, scansion, rhymes_letters, done_lines, enj4sonnet)
      for line in son["lines"][11:14]:
        add_line_element(nlp, lg_t2, line)
        done_lines = add_metrics_rhyme_and_enj(lg_t2, scansion,
                                               rhymes_letters, done_lines, enj4sonnet)

      #   extra stanza (Darío exceptions): DEBAYLE TOAST
      if son_title in cf.lg_exceptions and len(cf.lg_exceptions[son_title]["stanza_types"]) > 4:
        lg_extra = etree.SubElement(indiv_sonnet_lg, "lg", n="5")
        for line in son["lines"][14:20]:
          add_line_element(nlp, lg_extra, line)
          done_lines = add_metrics_rhyme_and_enj(
            lg_extra, scansion, rhymes_letters, done_lines, enj4sonnet)

    # serialize the per-author body
    ser_body = etree.tostring(top_ele, pretty_print=True, encoding="UTF-8")

  nbr_sonnets = str(len(top_ele.xpath("//lg[@type='sonnet']")))
  nbr_lines = str(len(top_ele.xpath("//l")))
  # need itertext bcs rhyme word is a child of l
  line_elements = top_ele.xpath("//l")
  line_texts = ["".join(le.itertext()) for le in line_elements]
  nbr_tokens = str(sum([len(word_tokenize(txt)) for txt in line_texts]))

  # build string for complete TEI
  header_to_fill = header_dario_pa if mode =="d" else header_chocano_pa
  #TODO: make metrics resp sensitive to annotator used (in case want
  # to use jumper on individual sonnets (not reinject its result for entire authors)
  header_filled = header_to_fill.format(
    nbr_of_sonnets=nbr_sonnets,
    nbr_of_tokens=nbr_tokens,
    nbr_of_lines=nbr_lines,
    list_bibl=bibl_list
  )

  final_str = str.encode(header_filled) + ser_body + str.encode(cf.final_closing_tags)
  final_str = clean_sertree(final_str)
  # output file name
  out_fn = os.path.join(cf.outdir + os.sep +
                        f"out-{cf.ids_by_mode[mode]['outdir_sfx']}"
                        + os.sep + "tei" + os.sep + "per-author",
           cf.fnshape_per_au.format(author_id=str.zfill(str(cf.ids_by_mode[mode]['start_auid']), 3),
                                    period_sfx=cf.ids_by_mode[mode]['period_sfx']))
  with open(out_fn, mode="w", encoding="UTF-8") as ofh:
    ofh.write(final_str.decode("utf-8"))
  return final_str


def add_line_element(nlp_ana, par, txt):
  """
  Create an lxml element with text in `txt`, tagging the
  last word as the rhyme word. Append it to parent node `par`.
  `tagger` is a spacy model loaded in the calling code."""
  toks = nlp_ana(txt)
  word_tok_mask = [True if not w.is_punct else False for w in toks]
  last_word_idx = word_tok_mask[::-1].index(True)
  last_word_idx_from_right = -1 - last_word_idx
  rhyme_word = toks[last_word_idx_from_right].text
  line_before_rhyme_word = [tok.text_with_ws for tok in toks][0:last_word_idx_from_right]
  if last_word_idx > 0:
    line_after_rhyme_word = [tok.text_with_ws for tok in toks][last_word_idx_from_right + 1:]
  else:
    line_after_rhyme_word = []
  line_text = "".join(line_before_rhyme_word) + f"<w type='rhyme'>{rhyme_word}</w>" + \
              "".join(line_after_rhyme_word)
  l_ele = etree.fromstring(f'<l>{line_text}</l>')
  par.append(l_ele)


def add_metrics_rhyme_and_enj(par, scan_infos, rhyme_infos, done_lines,
                              sonnet_enj=None, scan_tool=cf.scan_with):
  """
  Given parent lg `par`, Rantanplan results in `scan_infos`, RhymeTagger
  results in `rhyme_infos`, and ANJA results in `sonnet_enj`, add the
  attributes to the parent using `done_lines` as the `<l>` child index.
  """
  assert scan_tool in ("rantanplan", "jumper")
  if scan_tool == "rantanplan":
    par.xpath("//l")[-1].attrib["met"] = scan_infos[done_lines]["rhythm"]["stress"]
  elif scan_tool == "jumper":
    par.xpath("//l")[-1].attrib["met"] = scan_infos[done_lines]
  par.xpath("//l")[-1].attrib["rhyme"] = rhyme_infos[done_lines]
  if sonnet_enj is not None:
    if done_lines + 1 in sonnet_enj.start.tolist():
      type4idx = sonnet_enj.loc[sonnet_enj['start'] ==
                                done_lines + 1, 'type'].iloc[0]
      par.xpath(".//l")[-1].attrib["enjamb"] = type4idx
  done_lines += 1
  return done_lines


def clean_sertree(bo):
  """Replacements in string (in bytes rather) that represents serialized xml"""
  bo = bo.replace(b"xmlid", b"xml:id")
  return bo


def test_sonnet_length(sl):
  """Print message if poem does not have 14 lines"""
  print("- Test line number exceptions")
  for idx, it in enumerate(sl):
    for son in it["sonnets"]:
      if len(son["lines"]) != 14:
        print(mode, it["item_title"], len(son["lines"]), sep="\t")


if __name__ == "__main__":
  reload(cf)
  modes = ("c", "d")
  #modes = ("c")
  #modes = ("d")
  add_enjambment = False
  if len(sys.argv) > 1 and sys.argv[1] == "-e":
    add_enjambment = True
  for mode in modes:
    assert type(mode) is str and mode in ("c", "d")
    # IO
    out_by_author = os.path.join(cf.outdir + os.sep + \
          f"out-{cf.ids_by_mode[mode]['outdir_sfx']}", "tei" + os.sep + "per-author")
    out_by_sonnet = os.path.join(cf.outdir + os.sep + \
          f"out-{cf.ids_by_mode[mode]['outdir_sfx']}", "tei" + os.sep + "per-sonnet")
    for outdir in (out_by_author, out_by_sonnet):
      if not os.path.exists(outdir):
        print(outdir)
        os.makedirs(outdir)
      #TODO: are these directories needed or will XSLT create them after?
      cleantxtdir = os.path.join(cf.outdir,
                                 f"cleantxt-{cf.ids_by_mode[mode]['outdir_sfx']}")
      if not os.path.exists(cleantxtdir):
        os.makedirs(cleantxtdir)
  # Processing
  if add_enjambment:
    enj_data = pd.read_csv(cf.enj_results, sep="\t")
    print("* Will add enjambment")
  else:
    enj_data = None
  if "c" in modes:
    print(f"\n= Start mode [c], {strftime('%Y-%m-%d %H:%M:%S', localtime())}")
    slist_c = split_file_into_sonnets(cf.indir + os.sep + "sonetos_chocano.txt", mode="c")
    slpost_c = group_sequences(slist_c, mode="c")
    DBGV and test_sonnet_length(slpost_c)
    bibl_c = create_bibl(slpost_c)
    tei_full = create_tei_per_author(slpost_c, bibl_c, enj_data,
                                     mode="c", add_enjambment=add_enjambment,
                                     scan_tool=cf.scan_with)
  if "d" in modes:
    print(f"\n= Start mode [d], {strftime('%Y-%m-%d %H:%M:%S', localtime())}")
    slist_d = split_file_into_sonnets(cf.indir + os.sep + "sonetos_dario.txt", mode="d")
    slpost_d = group_sequences(slist_d, mode="d")
    DBGV and test_sonnet_length(slpost_d)
    bibl_d = create_bibl(slpost_d)
    tei_full = create_tei_per_author(slpost_d, bibl_d, enj_data, mode="d",
                                     add_enjambment=add_enjambment,
                                     scan_tool=cf.scan_with)

  # debug info
  if DBGV:
    from pprint import pprint
    for mode in modes:
      with open(cf.debug_groups + f"_{mode}", mode="w", encoding="utf8") as odb:
        myvar = [x for x in globals() if x.endswith(f"post_{mode}")]
        pprint(globals()[myvar[0]], stream=odb)

  print(f"\n= End {strftime('%Y-%m-%d %H:%M:%S', localtime())}")
