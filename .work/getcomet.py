import subprocess
url = "https://standardebooks.org/ebooks/w-e-b-du-bois/darkwater/text/chapter-10"
out = subprocess.run(["curl", "-s", "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "-o", ".work/comet.html", "-w", "%{http_code}:%{size_download}", url], capture_output=True, text=True)
print("curl:", out.stdout, out.stderr)
