import subprocess, re, html
q = "The Comet Du Bois Darkwater full text"
out = subprocess.run(["curl", "-s", "https://lite.duckduckgo.com/lite/", "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "--data-urlencode", "q=" + q, "https://lite.duckduckgo.com/lite/"], capture_output=True, text=True).stdout
links = re.findall(r'href="(https?://[^"]+)"[^>]*>(.*?)</a>', out)
for u, t in links[:15]:
    print(html.unescape(re.sub("<[^>]+>", "", t))[:70], "|", u[:100])
