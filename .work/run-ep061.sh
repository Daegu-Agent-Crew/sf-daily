#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home/tmp/sf-daily
echo "=== EP061 P1 START $(date +%T) ==="
codex exec --skip-git-repo-check -s danger-full-access "$(cat .work/prompt-ep061-p1.txt)" > codex-ep061-p1.log 2>&1
echo "P1_EXIT:$?"
echo "=== EP061 P2 START $(date +%T) ==="
codex exec --skip-git-repo-check -s danger-full-access -i .work/ep061-p1-notext.png - < .work/prompt-ep061-p2.txt > codex-ep061-p2.log 2>&1
echo "P2_EXIT:$?"
echo "=== EP061 ALL DONE $(date +%T) ==="