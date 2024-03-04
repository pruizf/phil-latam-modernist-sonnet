"""
Take Clara's corrections to the source, in a dataframe,
and reproduce them in the original txt source, so that
we can run the entire workflow from the corrected source
from the start.

Note: only correcting Darío and Chocano by script, the
Filipino part was done by hand in the TEI and in the initial txt.
"""

import os
import pandas as pd
import re
from time import strftime, localtime

import ameconfig as cf


if __name__ == "__main__":
  print(f"= Reading df {strftime('%Y-%m-%d %H:%M:%S', localtime())}")
  df = pd.read_excel(cf.corrected_jumper_results, engine="odf")
  print(f"= Done {strftime('%Y-%m-%d %H:%M:%S', localtime())}")
  with open(os.path.join(cf.indir, "sonetos_dario.txt")) as dario_fh, \
       open(os.path.join(cf.indir, "sonetos_chocano.txt")) as chocano_fh:
    txt_dario = dario_fh.read()
    txt_chocano = chocano_fh.read()
    txt_dario_orig, txt_chocano_orig = txt_dario, txt_chocano
  with open(os.path.join(cf.indir, "sonetos_dario.txt"), mode="w") as dario_fh_out, \
       open(os.path.join(cf.indir, "sonetos_chocano.txt"), mode="w") as chocano_fh_out:
    for idx, row in df.iterrows():
      if row['testLnJumperOrigVsCorrection'] == 1:
        bad_text = row['lnTxtOriginal']
        ok_text = row['lnTxtJumper']
        if "Chocano" in row['au']:
          bad_text_re = re.findall(
            re.compile(f"^{re.escape(bad_text)}\s*$", re.M), txt_chocano)
          assert len(bad_text_re) == 1
          txt_chocano = re.sub(bad_text_re[0], ok_text, txt_chocano)
        else:
          if row["orig"] == "fil":
            continue
          assert "Darío" in row['au']
          bad_text_re = re.findall(
            re.compile(f"^{re.escape(bad_text)}\s*$", re.M), txt_dario)
          assert len(bad_text_re) == 1
          txt_dario = re.sub(bad_text_re[0], ok_text, txt_dario)
    chocano_fh_out.write(txt_chocano)
    dario_fh_out.write(txt_dario)
