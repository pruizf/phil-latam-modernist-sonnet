"""
Extract metrical and other annotations from corpus to a dataframe
"""

from lxml import etree
import os
import pandas as pd

import ameconfig as cf

from ameconfig import NSMAP


# IO
phil_dir = cf.phil_dir
ame_dirs = cf.ame_dirs

out_df = os.path.join("out", "h23-df_re.tsv")

# IDs filipino and American sonnets
ids_phil = cf.ids_phil
ids_ame = cf.ids_ame

ame_paths = set()
phil_paths = set()


def corpus_to_df(pathlist, mode="ame"):
  """
  Takes a list of directories containing per-author sonnets.
  The `mode` will only affect the "origin" field in the output dataframe.
  *ame* is Darío and Chocano, *fil* is the Filipino authors.
  """
  assert mode in ("ame", "fil")
  myrows = []
  for pa in pathlist:
    atree = etree.parse(pa)
    auid = atree.xpath("//tei:profileDesc/tei:particDesc/tei:listPerson/tei:person/@xml:id",
                       namespaces=NSMAP)[0].replace("disco_", "")
    aufull = atree.xpath("//tei:persName[@type='source']", namespaces=NSMAP)[0].text.strip()
    # better to use our own clue on the ID than the TEI content to get the century
    #cent = int(atree.xpath("//tei:date[@type='century']", namespaces=NSMAP)[0].text.strip())
    cent = 20 if auid.endswith("t") and auid != "010t" else 19
    # shape of rows to create (row values)
    # aId,sId,orig,cent,au,title,incipit,irreg,nbLin,nbLg,lnTxt,met,rhyS,r1,r2,r3,r4,rw,enj,ent
    #   sonnet level
    for son in atree.xpath("//tei:lg[@type='sonnet']", namespaces=NSMAP):
      sid = son.xpath("@xml:id", namespaces=NSMAP)[0]
      orig = mode
      try:
        title = son.xpath("tei:head", namespaces=NSMAP)[0].text.strip()
      except (IndexError, AttributeError):
        title = ""
      line_eles = son.xpath(".//tei:l", namespaces=NSMAP)
      incipit_ele = line_eles[0]
      incipit = "".join(incipit_ele.itertext()).strip()
      nb_lines = len(line_eles)
      lgs = son.xpath(".//tei:lg", namespaces=NSMAP)
      nb_stan = len(lgs)
      rhyme_scheme = "".join(son.xpath(".//@rhyme", namespaces=NSMAP))
      assert nb_lines == len(rhyme_scheme)
      if len(rhyme_scheme) != 14:
        print(f"{auid}||{aufull}||{title}||{len(rhyme_scheme)}")
        irreg = True
      else:
        irreg = False
      if not irreg:
        r1 = rhyme_scheme[0:4]
        r2 = rhyme_scheme[4:8]
        r3 = rhyme_scheme[8:11]
        r4 = rhyme_scheme[11:14]
        rhyme_scheme_f = f"{r1} {r2} {r3} {r4}"
      else:
        r1, r2, r3, r4 = "", "", "", ""
        rhyme_scheme_f = rhyme_scheme
      #   line level
      for idx, le in enumerate(line_eles):
        line_text = "".join(le.itertext()).strip()
        met = le.xpath("@met")[0]
        met_dig = " ".join([str(i + 1) for i, ltr in enumerate(met)
                            if ltr == "+"])
        rw_ele = le.xpath("tei:w[@type='rhyme']", namespaces=NSMAP)
        rw = rw_ele[0].text if len(rw_ele) > 0 else ""
        if "enjamb" in le.attrib:
          enj_presence = True
          enj_type = le.attrib["enjamb"]
        else:
          enj_presence, enj_type = False, ""
        # reminder of row values to create
        # aId,sId,orig,cent,au,title,incipit,irreg,nbLin,nbLg,lnTxt,met,rhyS,r1,r2,r3,r4,rw,enj,ent
        row = [auid, sid, orig, cent, aufull, title, incipit, int(irreg), nb_lines, nb_stan, idx+1,
               line_text, met_dig, rhyme_scheme_f, rw, r1, r2, r3, r4, int(enj_presence), enj_type]
        myrows.append(row)
  return myrows

if __name__ == "__main__":
  # collect paths for sonnets to treat
  for fn in sorted(os.listdir(phil_dir)):
    ffn = os.path.join(phil_dir, fn)
    if fn.replace("disco", "").replace(".xml", "") not in ids_phil:
      continue
    phil_paths.add(ffn)

  for audir in ame_dirs:
    for fn in sorted(os.listdir(audir)):
      ffn = os.path.join(audir, fn)
      ame_paths.add(ffn)

  amerows = corpus_to_df(ame_paths, mode="ame")
  philrows = corpus_to_df(phil_paths, mode="fil")
  all_rows = amerows + philrows

  df = pd.DataFrame(columns=[
    "aId",
    "sId",
    "orig",
    "cent",
    "au",
    "title",
    "incipit",
    "irreg",
    "nbLin",
    "nbLg",
    "lnNbr",
    "lnTxt",
    "met",
    "rhys",
    "rw",
    "r1",
    "r2",
    "r3",
    "r4",
    "enj",
    "ent"
    ], data=all_rows)

  df.to_csv(out_df, sep="\t", index=False)

