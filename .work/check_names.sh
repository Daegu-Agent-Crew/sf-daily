#!/data/data/com.termux/files/usr/bin/bash
set -u
ID=$(curl -s "https://archive.org/advancedsearch.php?q=title%3A%22heads+of+cerberus%22+AND+mediatype%3Atexts&fl%5B%5D=identifier&rows=5&output=json" | grep -oE '"identifier":"[^"]+"' | head -1 | cut -d'"' -f4)
echo "ID=$ID"
if [ -n "$ID" ]; then
  curl -sL "https://archive.org/download/$ID/${ID}_djvu.txt" -A "Mozilla/5.0" -o /tmp/hoc.txt --max-time 90
  wc -c /tmp/hoc.txt
  echo "Trenmore=$(grep -c Trenmore /tmp/hoc.txt) Drayton=$(grep -c Drayton /tmp/hoc.txt) Viola=$(grep -c Viola /tmp/hoc.txt)"
  grep -m3 -oE "Penn Service|grey dust|gray dust|collar of [a-z]+" /tmp/hoc.txt | head -5
fi
