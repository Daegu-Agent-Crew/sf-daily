import json, subprocess
q = "https://archive.org/advancedsearch.php?q=title%3A%28darkwater%29+AND+creator%3A%28dubois%29&fl%5B%5D=identifier&fl%5B%5D=title&rows=8&output=json"
out = subprocess.run(["curl", "-s", q], capture_output=True, text=True).stdout
d = json.loads(out)
for x in d["response"]["docs"]:
    print(x["identifier"], "|", x.get("title", ""))
