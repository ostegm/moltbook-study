#!/bin/bash
# Quick progress check for the judge run
cd /home/node/.openclaw/workspace/moltbook-study
TOTAL=56700
DONE=$(wc -l < classified_posts.jsonl 2>/dev/null || echo 0)
PCT=$(python3 -c "print(f'{100*$DONE/$TOTAL:.1f}')")
RUNNING=$(ps aux | grep run_judge | grep -v grep | wc -l)
echo "Progress: $DONE / $TOTAL ($PCT%)"
echo "Process running: $([ $RUNNING -gt 0 ] && echo 'YES' || echo 'NO')"
if [ -f judge_run.log ]; then
    echo "Last log lines:"
    tail -3 judge_run.log
fi
