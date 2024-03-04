"""
Given a DISCO-formatted TEI corpus and a dataframe containing Jumper results,
enter these results as the @met attribute of each line (replacing an already
existing @met)
"""

from lxml import etree
import os
import pandas as pd
import re
from time import localtime, strftime
from typing import Iterable

import ameconfig as cf

from ameconfig import NSMAP, NSMAP_W, TEI_NAMESPACE, XML_NAMESPACE

# IO
phil_dir = cf.phil_dir
ame_dirs = cf.ame_dirs

# IDs filipino and American TEI
ids_phil = cf.ids_phil
ids_ame = cf.ids_ame


def prepro_line(lne):
  """
  Preprocess lines so that can compare them

  Args:
      lne (str): line
  Returns:
      str: preprocessed line
  """
  # “” --> ", no spaces, remove — goes out, two or more dots go to one only
  # apeloronada, deaciñe, desdefíosa
  # cmo el destino cómo el destino
  #TODO: implement if need to do this type of comparison
  pass


def create_met_with_signs(nb_syll: int, met_as_numbers: str) -> str:
  """Get a metrical signature expressed as a digit string for stressed
  positions and return the signature encoded with '-' for weak and '+' for
  strong syllables.

  Args:
    nb_syll (int): Number of metrical syllables as given by Jumper
    met_as_numbers (str): Metrical signature as a string of digits for stressed positions

  Returns:
    str: The metrical signature expressed as a string of '+' and '-' (strong vs weak position)
         Empty string if there was an error.
  """
  try:
    # strip() is because if there have been manual corrections, a space may have been added
    last_stressed_position = [int(x) for x in met_as_numbers.strip().split(" ")][-1]
  except AttributeError:
    return ""
  max_signs = int(nb_syll) if int(nb_syll) >= last_stressed_position else last_stressed_position
  met_as_signs = ["-" for x in range(max_signs)]
  for nbr in met_as_numbers.strip().split(" "):
    met_as_signs[int(nbr) - 1] = "+"
  return "".join(met_as_signs)


def reannotate_sonnets(path_list: Iterable[str], jdf: pd.core.frame.DataFrame,
                       mode: str, replace_met_decl=False):
  """
  Given a list of paths for DISCO formatted sonnets, replace
  the `@met` attribute with information in a dataframe. If the new metrical
  information only has one position, keeps the old one (this is meant to deal
  with odd behaviour of Jumper in an exeption case; Rantanplan was handling it better.

  Args:
    path_list (Iterable[str]): List of paths for sonnets to treat
    jdf (pandas.core.frame.DataFrame): Pandas DataFrame containing Jumper annotations
    mode (str): Mode 'ame' is for the American sonnets, mode 'phil' for the Filipino ones.
      What changes is that in Filipino sonnets a `<change>` element is added to indicate
      reannotation with Jumper.
    replace_met_decl (bool): Whether need to replace Rantanplan metDecl for Jumper or not
      (Filipino sonnets were done with Rantanplan, earlier, so need to replace this).
  """
  assert mode in ("ame", "phil")
  for ffn in sorted(path_list):
    tree = etree.parse(ffn)
    # change resp for metrical annotations
    resp_name_to_delete = tree.xpath("//tei:respStmt/tei:name", namespaces=NSMAP)[0]
    resp_to_delete = tree.xpath("//tei:respStmt/tei:resp", namespaces=NSMAP)[0]
    resp_info_parent = resp_to_delete.getparent()
    resp_info_parent.remove(resp_name_to_delete)
    resp_info_parent.remove(resp_to_delete)
    resp_info_parent.append(etree.fromstring(cf.jumper_scansion_resp))
    resp_info_parent.append(etree.fromstring(cf.jumper_scansion_resp_name))
    # change metDecl
    if replace_met_decl:
      # it's the second metDecl (third child given a listPrefixDef first)
      met_decl_to_delete = tree.xpath("//tei:metDecl", namespaces=NSMAP)[1]
      met_decl_parent = met_decl_to_delete.getparent()
      met_decl_parent.remove(met_decl_to_delete)
      met_decl_parent.insert(2, etree.fromstring(cf.new_met_decl))
    rev_desc = tree.xpath("/tei:TEI/tei:teiHeader/descendant::tei:revisionDesc", namespaces=NSMAP)
    if mode == "phil":
      rev_desc[0].append(etree.fromstring(cf.changes_to_jumper_met))
    rev_desc[0].append(etree.fromstring(cf.manual_correction_to_jumper_met))

    # treat sonnets
    sonnets_for_au = tree.xpath("//tei:lg[@type='sonnet']", namespaces=NSMAP)
    for sonnet in sonnets_for_au:
      sid = sonnet.attrib[f"{{{XML_NAMESPACE}namespace}}id"]
      slines = sonnet.xpath("descendant::tei:l", namespaces=NSMAP)
      # get original metrics from df
      met_jumper = jdf.loc[df.sId == sid, 'metJumper'].tolist()
      nb_syl_jumper = jdf.loc[df.sId == sid, 'nbSylJumper'].tolist()[0]
      assert len(met_jumper) == len(slines)
      # reannotate
      for idx, met in enumerate(met_jumper):
        #TODO may consider verifying line match (even if no diff on git other than metrics)
        met_as_signs = create_met_with_signs(nb_syl_jumper, met)
        if len(met_as_signs) > 0:
          slines[idx].attrib["met"] = met_as_signs
    ser = etree.tostring(tree, pretty_print=True, encoding="UTF-8", xml_declaration=True)
    outdir = outdir_19 if "n.xml" in ffn else outdir_20
    #out_path = os.path.join(cf.outdir_jumper, os.path.basename(ffn))
    out_path = os.path.join(outdir, os.path.basename(ffn))
    print(out_path)
    with open(out_path, mode="w", encoding="UTF-8") as ofh:
      ofh.write(ser.decode("utf-8"))


if __name__ == "__main__":
  # if not os.path.exists(cf.outdir_jumper):
  #   os.mkdir(cf.outdir_jumper)

  outdir_19 = os.path.join(cf.outdir, "out-19" + os.sep + "tei-jumper" + os.sep + "per-author")
  outdir_20 = os.path.join(cf.outdir, "out-20" + os.sep + "tei-jumper" + os.sep + "per-author")
  for dname in outdir_19, outdir_20:
    if not os.path.exists(dname):
      os.makedirs(dname)

  print(f"\n= Read df, {strftime('%Y-%m-%d %H:%M:%S', localtime())}")

  # read metrical annots off Jumper results
  df = pd.read_excel(cf.corrected_jumper_results, engine="odf")

  # collect paths for sonnets to treat
  phil_paths = set()
  ame_paths = set()

  for fn in sorted(os.listdir(phil_dir)):
    ffn = os.path.join(phil_dir, fn)
    if fn.replace("disco", "").replace(".xml", "") not in ids_phil:
      continue
    phil_paths.add(ffn)

  for audir in ame_dirs:
    for fn in sorted(os.listdir(audir)):
      ffn = os.path.join(audir, fn)
      ame_paths.add(ffn)

  print(f"\n= Start @met rewrite, {strftime('%Y-%m-%d %H:%M:%S', localtime())}")
  reannotate_sonnets(phil_paths, df, mode="phil", replace_met_decl=True)
  reannotate_sonnets(ame_paths, df, mode="ame", replace_met_decl=True)
  print(f"\n= End, {strftime('%Y-%m-%d %H:%M:%S', localtime())}")
