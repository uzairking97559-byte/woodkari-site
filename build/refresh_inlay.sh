#!/bin/bash
# Re-make the inlay table pictures from agency-research photos/ai/inlay (OW-xx-a..f.png) and rebuild the site.
# Use after new letters (-b..-f) or a new picture for a design appear. -a = main picture, the rest show in order as the gallery.
# OW-42: -a (cube on a corner) is skipped; -e (flat cube) is its main picture (see make_inlay).
set -e
R=/home/user/woodkari-site
git -C /home/user/agency-research pull -q --rebase origin design/warm-studio
for p in "OW-38 bone-inlay-coffee-table-38" "OW-39 bone-inlay-coffee-table-39" "OW-40 bone-inlay-coffee-table-40" \
         "OW-41 bone-inlay-stool-41" "OW-42 bone-inlay-side-table-42" "OW-43 bone-inlay-coffee-table-43"; do
  set -- $p; python3 $R/build/mto_images.py inlay $1 $2
done
python3 $R/build/build.py .
