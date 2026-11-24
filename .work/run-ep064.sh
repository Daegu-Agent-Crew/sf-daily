#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home/tmp/sf-daily
echo "=== EP064 P1 START $(date +%T) ==="
codex exec --skip-git-repo-check -s danger-full-access "$(cat .work/prompt-ep064-p1.txt)" > codex-ep064-p1.log 2>&1
echo "P1_EXIT:$?"
echo "=== EP064 P2 START $(date +%T) ==="
codex exec --skip-git-repo-check -s danger-full-access -i .work/ep064-p1-notext.png - < .work/prompt-ep064-p2.txt > codex-ep064-p2.log 2>&1
echo "P2_EXIT:$?"
echo "=== EP064 P3 START $(date +%T) ==="
codex exec --skip-git-repo-check -s danger-full-access -i .work/ep064-p2-notext.png - < .work/prompt-ep064-p3.txt > codex-ep064-p3.log 2>&1
echo "P3_EXIT:$?"
echo "=== EP064 ALL DONE $(date +%T) ==="
