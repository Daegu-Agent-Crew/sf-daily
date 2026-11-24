import json, subprocess
ident = "darkwatervoicesf0000dubo_w0f6"
d = json.loads(subprocess.run(["curl", "-s", "https://archive.org/metadata/" + ident], capture_output=True, text=True).stdout)
server = d.get("item", {}).get("server", "")
dirp = d.get("item", {}).get("dir", "")
fn = ident + "_djvu.txt"
print("server:", server, "dir:", dirp)
url = "https://%s/%s/%s" % (server, dirp, fn)
print("URL:", url)
out = subprocess.run(["curl", "-s", "-A", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36", "-o", ".work/darkwater.txt", "-w", "%{http_code} %{size_download}", url], capture_output=True, text=True)
print("curl:", out.stdout, out.stderr)
