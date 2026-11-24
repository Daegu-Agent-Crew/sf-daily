import json, subprocess
q = "https://archive.org/advancedsearch.php?q=darkwater&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=access_restricted_item&rows=20&output=json"
out = subprocess.run(["curl", "-s", q], capture_output=True, text=True).stdout
d = json.loads(out)
for x in d["response"]["docs"]:
    print(x["identifier"], "|", x.get("title", ""), "| restricted:", x.get("access_restricted_item", False))
