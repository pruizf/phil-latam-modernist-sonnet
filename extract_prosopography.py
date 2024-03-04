"""
Extract author information from the teiHeader into a prosopography file.
All the information in the exact prosopography format is in teiHeader,
making XML parsing unnecessary. Just extract it with a regex and copy it elsewhere.
@note: In an earlier corpus version part of the header was created FROM the prosopography,
this is why the formats are exactly the same now.
"""

import os
import re

import ameconfig as cf
from data import header_and_end_prosopography as hep

teidir = os.path.join(cf.teibasedir_for_incipits, "all-periods-per-author")

# spaces are for xml indentation
person_re = re.compile(r"""(<person xml:id="disco.+?</death>\s*)     """, re.DOTALL|re.UNICODE)

out_list = [hep.header_prosopography]

# create sort order (001g, 002g, ... , 001e, 002e, ...)
fns_to_sort = os.listdir(teidir)
ga_files = sorted([fn for fn in fns_to_sort if "g.xml" in fn])
ea_files = sorted([fn for fn in fns_to_sort if "e.xml" in fn])
na_files = sorted([fn for fn in fns_to_sort if "n.xml" in fn])
ta_files = sorted([fn for fn in fns_to_sort if "t.xml" in fn])
sorter = ga_files + ea_files + na_files + ta_files

for fn in sorted(os.listdir(teidir), key=lambda x: sorter.index(x)):
  ffn = os.path.join(teidir, fn)
  with open(ffn) as teifn:
    teistr = teifn.read()
    au_infos = re.search(person_re, teistr)
    assert au_infos
    if not cf.chocano_19:
      if "disco592n" in au_infos.group(1):
        continue
    out_list.append(au_infos.group(1))
    out_list.append("</person>\n             ")
out_list.append(hep.prosopography_end_tags)

with open(cf.prosopography_fn, mode="w") as outfn:
  outfn.write("".join(out_list))



