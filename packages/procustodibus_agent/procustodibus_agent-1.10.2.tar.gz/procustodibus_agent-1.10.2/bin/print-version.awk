#!/bin/awk -f
# prints the package version number from the VERSION/TAG env var or from git
BEGIN {
  $0 = ENVIRON["VERSION"]
  if (! $0) { $0 = ENVIRON["TAG"] }
  if (! $0) {
    # format git-describe as PEP 440 version to match versioningit
    # eg convert '1.2.3-4-g567890a' to '1.2.3.post4+g567890a'
    # and '1.2.3-4-g567890a+d20250101' to '1.2.3.post4+g567890a.d20250101'
    describe="git describe --dirty=+d" strftime("%Y%m%d") " 2>/dev/null"
    distance="s/-([0-9]+)-(g[0-9a-f]+)$/.post\\1+\\2/"
    distance_dirty="s/-([0-9]+)-(g[0-9a-f]+)\\+d([0-9]{8})$/.post\\1+\\2.d\\3/"
    (describe " | sed -E '" distance ";" distance_dirty "'") | getline
  }
  if (! $0) { $0 = "0.0.0" }
  # sanitize version number, stripping unexpected chars
  # eg convert '1.2.3-foo+5~x; echo "evil"' to '1.2.3-foo+5~xechoevil'
  gsub(/[^0-9A-Za-z+.~-]/, "")
  print
}
