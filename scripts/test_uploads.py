import urllib.request, urllib.parse, json, uuid, re

pdf_path = r"C:\Users\sk\Desktop\drip irrigation moringa\irrigation_package\Moringa_2Acre_Irrigation_Master_Dossier.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# 1. Check filebin HTML links
try:
    url = "https://filebin.net/moringa-90eb6c10"
    with urllib.request.urlopen(url) as resp:
        html = resp.read().decode("utf-8")
        matches = re.findall(r'href="([^"]+)"', html)
        print("Filebin links:", [m for m in matches if "pdf" in m.lower() or "download" in m.lower() or "moringa" in m.lower()])
except Exception as e:
    print("Filebin error:", e)

# 2. Test tmpfiles.org
try:
    boundary = "----WebKitFormBoundary" + uuid.uuid4().hex
    body = []
    body.append(f"--{boundary}".encode())
    body.append(b'Content-Disposition: form-data; name="file"; filename="Moringa_2Acre_Irrigation_Master_Dossier.pdf"')
    body.append(b"Content-Type: application/pdf")
    body.append(b"")
    body.append(pdf_bytes)
    body.append(f"--{boundary}--".encode())
    body.append(b"")
    payload = b"\r\n".join(body)

    req = urllib.request.Request("https://tmpfiles.org/api/v1/upload", data=payload, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print("tmpfiles success:", res)
        # tmpfiles direct link: replace tmpfiles.org/ with tmpfiles.org/dl/
        raw_url = res["data"]["url"]
        dl_url = raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
        print("tmpfiles direct download:", dl_url)
except Exception as e:
    print("tmpfiles error:", e)

# 3. Test litterbox.catbox.moe
try:
    boundary = "----WebKitFormBoundary" + uuid.uuid4().hex
    body = []
    body.append(f"--{boundary}".encode())
    body.append(b'Content-Disposition: form-data; name="reqtype"')
    body.append(b"")
    body.append(b"fileupload")
    body.append(f"--{boundary}".encode())
    body.append(b'Content-Disposition: form-data; name="time"')
    body.append(b"")
    body.append(b"72h")
    body.append(f"--{boundary}".encode())
    body.append(b'Content-Disposition: form-data; name="fileToUpload"; filename="Moringa_2Acre_Irrigation_Master_Dossier.pdf"')
    body.append(b"Content-Type: application/pdf")
    body.append(b"")
    body.append(pdf_bytes)
    body.append(f"--{boundary}--".encode())
    body.append(b"")
    payload = b"\r\n".join(body)

    req = urllib.request.Request("https://litterbox.catbox.moe/resources/internals/api.php", data=payload, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("User-Agent", "Mozilla/5.0")
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = resp.read().decode("utf-8")
        print("litterbox success:", res)
except Exception as e:
    print("litterbox error:", e)

# 4. Test file.io
try:
    boundary = "----WebKitFormBoundary" + uuid.uuid4().hex
    body = []
    body.append(f"--{boundary}".encode())
    body.append(b'Content-Disposition: form-data; name="file"; filename="Moringa_2Acre_Irrigation_Master_Dossier.pdf"')
    body.append(b"Content-Type: application/pdf")
    body.append(b"")
    body.append(pdf_bytes)
    body.append(f"--{boundary}--".encode())
    body.append(b"")
    payload = b"\r\n".join(body)

    req = urllib.request.Request("https://file.io", data=payload, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print("file.io success:", res)
except Exception as e:
    print("file.io error:", e)
