"""
Scansion with Jumper at entire subcorpus level.
(Just one text-file per subcorpus, give it all to annotate).
"""

import os
from external import jumper

dario_sonnets = "raw_sources/sonetos_dario.txt"
chocano_sonnets = "raw_sources/sonetos_chocano.txt"
filipino_sonnet_dir = "/home/ruizfabo/projects/pd/projects/potes/disco_private_2022/disco_private/dh2022/out/cleantxt"
all_filipino_txt = "raw_sources/all_filipino_text.txt"
outdir = os.path.join("out", "jumper_scansion")

if not os.path.exists(outdir):
  os.mkdir(outdir)

with open(dario_sonnets) as ds:
  dario_txt = ds.read()

with open(chocano_sonnets) as cs:
  chocano_txt = cs.read()

if os.path.exists(all_filipino_txt):
  os.remove(all_filipino_txt)

os.system("./collect_filipino_text.sh")

with open(all_filipino_txt) as fs:
  filipino_txt = fs.read()

print("- Scan Darío")
dario_scan = jumper.escandir_texto(dario_txt)
print("- Scan Chocano")
chocano_scan = jumper.escandir_texto(chocano_txt)
print("- Scan Filipino")
filipino_scan = jumper.escandir_texto(filipino_txt)

print("- Write out")

header_fields = ["n", "lnTxtJumper", "etiquetadoJumper", "nbSylJumper", "metJumper", "metNoExtraJumper", "lnTypJumper", "matchJumper"]
header = "\t".join(header_fields) + "\n"

# dario
out_dario_with_titles = os.path.join(outdir, os.path.basename(dario_sonnets).replace(".txt", "_out.txt"))
out_dario_no_titles = os.path.join(outdir, os.path.basename(dario_sonnets).replace(".txt", "_out_no_titles.txt"))
with open(out_dario_with_titles, mode="w") as do, \
     open(out_dario_no_titles, mode="w") as donot:
  do.write(header)
  donot.write(header)
  for dinfos in dario_scan:
    dinfos[3] = " ".join([str(m) for m in dinfos[3]])
    dinfos[4] = " ".join([str(m) for m in dinfos[4]])
    do.write("dario\t" + "\t".join([str(x) for x in dinfos]) + "\n")
  skip_line = False
  for dinfos in dario_scan:
    # skip French sonnet
    #  start skip at title
    if dinfos[0] == "$HELDA":
      skip_line = True
      print(f"  - SKIP: {dinfos[0]}")
      continue
    #  keep skipping until next title
    if skip_line and dinfos[0][0] != "$":
      print(f"  - SKIP: {dinfos}")
      continue
    else:
      skip_line = False
    # skip titles and dedications
    if dinfos[0][0] in ("$", "*"):
      continue
    donot.write("dario\t" + "\t".join([str(x) for x in dinfos]) + "\n")

# chocano
out_chocano_with_titles = os.path.join(outdir, os.path.basename(chocano_sonnets).replace(".txt", "_out.txt"))
out_chocano_no_titles = os.path.join(outdir, os.path.basename(chocano_sonnets).replace(".txt", "_out_no_titles.txt"))
with open(out_chocano_with_titles, mode="w") as co, \
     open(out_chocano_no_titles, mode="w") as conot:
  co.write(header)
  conot.write(header)
  for cinfos in chocano_scan:
    cinfos[3] = " ".join([str(m) for m in cinfos[3]])
    cinfos[4] = " ".join([str(m) for m in cinfos[4]])
    co.write("chocano\t" + "\t".join([str(x) for x in cinfos]) + "\n")
  for cinfos in chocano_scan:
    # skip titles and dedications
    if cinfos[0][0] in ("$", "*"):
      continue
    conot.write("chocano\t" + "\t".join([str(x) for x in cinfos]) + "\n")

# fil
out_fil_no_titles = os.path.join(outdir, os.path.basename(all_filipino_txt).replace(".txt", "_out_no_titles.txt"))
with open(out_fil_no_titles, mode="w") as fo:
  fo.write(header)
  for finfos in filipino_scan:
    # skip dedications
    #TODO: this is too drastic, two cases with [ are not dedications
    #TODO: conversely, some cases with parentheses are actually dedications
    if "[" in finfos[0]:
      continue
    finfos[3] = " ".join([str(m) for m in finfos[3]])
    finfos[4] = " ".join([str(m) for m in finfos[4]])
    fo.write("filip\t" + "\t".join([str(x) for x in finfos]) + "\n")
