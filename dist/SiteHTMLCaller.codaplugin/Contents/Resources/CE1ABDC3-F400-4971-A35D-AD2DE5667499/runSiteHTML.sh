
env python2.7 -m SiteHTML "$CODA_SITE_LOCAL_PATH" | env awk 'BEGIN{print "<html><head><style type=""\x22""text/css""\x22"">*{background-color: black;color:white;}</style></head><body><h1>SiteHTML Output</h1><code>"};{print $0, "<br>"};END{print "</code></body></html>"}'
