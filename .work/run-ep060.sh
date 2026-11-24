#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home/tmp/sf-daily
echo "=== EP060 P1 START $(date +%T) ==="
codex exec --skip-git-repo-check -s danger-full-access "$(cat .work/prompt-ep060-p1.txt)" > codex-ep060-p1.log 2>&1
echo "P1_EXIT:$?"
echo "=== EP060 P2 START $(date +%T) ==="
codex exec --skip-git-repo-check -s danger-full-access -i .work/ep060-p1-notext.png - < .work/prompt-ep060-p2.txt > codex-ep060-p2.log 2>&1
echo "P2_EXIT:$?"
echo "=== EP060 P3 START $(date +%T) ==="
codex exec --skip-git-repo-check -s danger-full-access -i .work/ep060-p2-notext.png - < .work/prompt-ep060-p3.txt > codex-ep060-p3.log 2>&1
echo "P3_EXIT:$?"
echo "=== EP060 ALL DONE $(date +%T) ==="