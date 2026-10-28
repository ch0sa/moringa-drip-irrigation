import os
import base64

art_dir = r"C:\Users\sk\.gemini\antigravity\brain\53b382f4-89b2-422d-a44c-0283f9db8dd7"
pkg_dir = r"C:\Users\sk\Desktop\drip irrigation moringa\irrigation_package"

def get_b64(fname):
    p = os.path.join(pkg_dir, fname)
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

b64_dossier = get_b64("Moringa_2Acre_Irrigation_Master_Dossier.pdf")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Moringa Drip Irrigation — Mobile &amp; Remote PDF Downloader</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-3">
  <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-5 shadow-2xl max-w-lg mx-auto">
    <div class="flex items-center gap-3 border-b border-[var(--border)] pb-3 mb-4">
      <div class="w-10 h-10 rounded-xl bg-sky-500/20 text-sky-400 flex items-center justify-center text-xl shrink-0 border border-sky-500/30">
        📥
      </div>
      <div class="min-w-0 flex-1">
        <h3 class="font-bold text-base text-[var(--foreground)] truncate">Master Engineering Dossier</h3>
        <p class="text-xs text-[var(--muted-foreground)]">Tap below to download directly to your device</p>
      </div>
      <span class="text-xs font-mono font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-full shrink-0">
        512 KB
      </span>
    </div>

    <div class="space-y-2 mb-4 text-xs text-[var(--muted-foreground)] bg-[var(--background)]/70 p-3 rounded-xl border border-[var(--border)]">
      <div class="flex items-center gap-1.5 text-[var(--foreground)] font-semibold">
        <span>✓</span> <span>Full 20-Page Complete Dossier (IS 12786 / IS 4985)</span>
      </div>
      <div class="grid grid-cols-2 gap-1 text-[11px] pt-1 border-t border-[var(--border)]/50">
        <div>• 10-Sec Field Manual</div>
        <div>• Scale CAD Blueprint</div>
        <div>• 4ft Riser Detail</div>
        <div>• Exploded Assemblies</div>
        <div>• GridCraft BOM &amp; Cuts</div>
        <div>• Briefing Summary</div>
      </div>
    </div>

    <!-- PRIMARY INSTANT DOWNLOAD BUTTON -->
    <button onclick="downloadDossier()" id="dlBtn" class="w-full bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 text-white font-bold py-3 px-4 rounded-xl shadow-lg flex items-center justify-center gap-2.5 transition-all active:scale-[0.98] cursor-pointer text-sm">
      <svg class="w-5 h-5 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
      </svg>
      <span id="btnText">Tap to Download PDF (512 KB)</span>
    </button>
    <p id="statusMsg" class="text-[11px] text-center text-emerald-400 mt-2 font-medium hidden">✓ File saved to device Downloads!</p>
  </div>

  <script>
    const dossierData = "{b64_dossier}";

    function downloadDossier() {{
      const btn = document.getElementById('dlBtn');
      const text = document.getElementById('btnText');
      const status = document.getElementById('statusMsg');
      
      text.innerText = "Downloading...";
      
      try {{
        const byteCharacters = atob(dossierData);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {{
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }}
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], {{ type: 'application/pdf' }});

        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "Moringa_2Acre_Irrigation_Master_Dossier.pdf";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        setTimeout(() => {{
          URL.revokeObjectURL(url);
          text.innerText = "Downloaded Successfully!";
          status.classList.remove('hidden');
        }}, 600);
      }} catch (err) {{
        console.error(err);
        text.innerText = "Download Error";
      }}
    }}
  </script>
</body>
</html>
"""

out_path = os.path.join(art_dir, "download_portal.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

file_size = os.path.getsize(out_path)
print(f"Direct Download Portal generated: {out_path} ({file_size} bytes)")
