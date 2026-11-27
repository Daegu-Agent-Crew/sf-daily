#!/bin/bash
cd /data/data/com.termux/files/home/tmp/sf-daily
[ -f "$HOME/.openclaw/workspace/.env" ] && source "$HOME/.openclaw/workspace/.env"
export OPENAI_API_KEY
for p in 1 2 3; do
  log="codex-ep082-p${p}.log"
  codex exec --skip-git-repo-check -s danger-full-access "$(cat "ep082-p${p}.txt")" > "$log" 2>&1
  echo "EXIT:$?" >> "$log"
  if ! python3 .work/validate082.py ".work/ep082-p${p}.png" >> "$log" 2>&1; then
    echo "RETRY p${p}" >> "$log"
    rm -f ".work/ep082-p${p}.png"
    codex exec --skip-git-repo-check -s danger-full-access "$(cat "ep082-p${p}.txt")" >> "$log" 2>&1
    echo "EXIT:$?" >> "$log"
    python3 .work/validate082.py ".work/ep082-p${p}.png" >> "$log" 2>&1
  fi
done
echo '=== FINAL VALIDATION ==='
python3 .work/validate082.py .work/ep082-p1.png .work/ep082-p2.png .work/ep082-p3.png
echo 'DRIVER_DONE'
