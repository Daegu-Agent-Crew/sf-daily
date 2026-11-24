import json, subprocess
for ident in ["darkwatervoicesf0000dubo_w0f6", "darkwater0000bani"]:
    out = subprocess.run(["curl", "-s", "https://archive.org/metadata/" + ident], capture_output=True, text=True).stdout
    try:
        d = json.loads(out)
    except Exception as e:
        print(ident, "ERR", e); continue
    print("=====", ident, "|", d.get("metadata", {}).get("title"), "| access:", d.get("access_restricted_item"))
    for f in d.get("files", []):
        n = f.get("name", "")
        if n.endswith((".txt", ".md", ".xml")) or "_djvu" in n:
            print("   ", n, f.get("size", "?"))
