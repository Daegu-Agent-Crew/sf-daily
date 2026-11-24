import json, subprocess
ident = "darkwatervoicesf0000dubo_w0f6"
d = json.loads(subprocess.run(["curl", "-s", "https://archive.org/metadata/" + ident], capture_output=True, text=True).stdout)
print("top keys:", sorted(d.keys()))
for k in d:
    if k in ("files",):
        continue
    v = d[k]
    print(k, "=>", json.dumps(v, ensure_ascii=False)[:300])
