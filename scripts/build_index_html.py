import os
import sys

def build_index(pkg_dir, root_dir):
    s1_path = os.path.join(pkg_dir, "CAD_Master_Blueprint.svg")
    s2_path = os.path.join(pkg_dir, "Riser_Manifold_Detail.svg")

    with open(s1_path, "r", encoding="utf-8") as f:
        s1_svg = f.read()
    with open(s2_path, "r", encoding="utf-8") as f:
        s2_svg = f.read()

    # Strip XML declaration if present
    def clean_svg(s):
        idx = s.find("<svg")
        if idx != -1:
            return s[idx:]
        return s

    s1_clean = clean_svg(s1_svg)
    s2_clean = clean_svg(s2_svg)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>2-Acre Moringa Irrigation — Classic Architectural Blueprint</title>
  <style>
    :root {{
      --blue-bg: #0B2545;
      --blue-border: #134074;
      --white: #FFFFFF;
      --ice-cyan: #E0F2FE;
      --cyan-lateral: #7DD3FC;
      --dim-blue: #BAE6FD;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }}
    html, body {{
      width: 100%;
      height: 100%;
      overflow: hidden;
      background-color: var(--blue-bg);
      color: var(--white);
      font-family: 'Courier New', Courier, monospace;
    }}
    /* Top Architectural Header & Controls */
    header {{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 64px;
      background: rgba(11, 37, 69, 0.95);
      border-bottom: 2px solid var(--white);
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 1.5rem;
      z-index: 1000;
      backdrop-filter: blur(8px);
    }}
    .header-left {{
      display: flex;
      align-items: center;
      gap: 1.5rem;
    }}
    .project-tag {{
      font-size: 1.15rem;
      font-weight: bold;
      letter-spacing: 2px;
      color: var(--white);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .sheet-switchers {{
      display: flex;
      gap: 0.5rem;
      background: #081a33;
      padding: 0.25rem;
      border: 1px solid var(--dim-blue);
      border-radius: 6px;
    }}
    .sheet-btn {{
      background: none;
      border: none;
      color: var(--dim-blue);
      font-family: inherit;
      font-size: 0.85rem;
      font-weight: bold;
      letter-spacing: 1px;
      padding: 0.45rem 1rem;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .sheet-btn.active {{
      background: var(--white);
      color: var(--blue-bg);
    }}
    .header-right {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}
    .btn {{
      background: #081a33;
      color: var(--white);
      border: 1px solid var(--dim-blue);
      font-family: inherit;
      font-size: 0.85rem;
      font-weight: bold;
      padding: 0.45rem 0.9rem;
      border-radius: 4px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      text-decoration: none;
      transition: all 0.2s;
    }}
    .btn:hover {{
      background: var(--dim-blue);
      color: var(--blue-bg);
    }}
    .btn-white {{
      background: var(--white);
      color: var(--blue-bg);
      border-color: var(--white);
    }}
    .btn-white:hover {{
      background: var(--ice-cyan);
      border-color: var(--ice-cyan);
    }}

    /* Main Fullscreen Canvas Container */
    #canvasContainer {{
      position: absolute;
      top: 64px;
      bottom: 36px;
      left: 0;
      right: 0;
      background: var(--blue-bg);
      overflow: hidden;
      cursor: grab;
      display: flex;
      justify-content: center;
      align-items: center;
    }}
    #canvasContainer:active {{
      cursor: grabbing;
    }}
    .blueprint-viewport {{
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      transform-origin: center center;
      transition: transform 0.04s ease-out;
    }}
    .blueprint-viewport svg {{
      width: 100%;
      height: 100%;
      display: block;
    }}

    /* Bottom Status HUD */
    footer {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 36px;
      background: #081a33;
      border-top: 1px solid var(--blue-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 1.5rem;
      font-size: 0.75rem;
      color: var(--dim-blue);
      letter-spacing: 1px;
      z-index: 1000;
    }}
    .hud-left {{
      display: flex;
      gap: 2rem;
    }}
    .hud-right {{
      display: flex;
      gap: 1.5rem;
    }}
    
    /* Print Overlay Rules */
    @media print {{
      header, footer {{
        display: none !important;
      }}
      #canvasContainer {{
        top: 0 !important;
        bottom: 0 !important;
        position: relative !important;
        overflow: visible !important;
      }}
      @page {{
        size: A3 landscape;
        margin: 0;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Navigation & Architectural Controls -->
  <header>
    <div class="header-left">
      <div class="project-tag">
        <span>📐</span>
        <span>2-ACRE MORINGA IRRIGATION BLUEPRINT</span>
      </div>
      <div class="sheet-switchers">
        <button class="sheet-btn active" id="btnS1" onclick="switchSheet('sheet1')">SHEET 1: MASTER FIELD PLAN</button>
        <button class="sheet-btn" id="btnS2" onclick="switchSheet('sheet2')">SHEET 2: 4FT RISER DETAIL</button>
      </div>
    </div>

    <div class="header-right">
      <button class="btn" onclick="zoomIn()">ZOOM +</button>
      <button class="btn" onclick="zoomOut()">ZOOM -</button>
      <button class="btn" onclick="resetView()">RESET FIT</button>
      <span style="font-size:0.85rem; color:var(--dim-blue); min-width:55px; text-align:center;" id="zoomDisplay">100%</span>
      <a href="Moringa_2Acre_Irrigation_Blueprint_2Page.pdf" download class="btn btn-white">
        <span>📥 EXPORT BLUEPRINT PDF (2-PAGE)</span>
      </a>
      <button class="btn" onclick="window.print()">PRINT BLUEPRINT</button>
    </div>
  </header>

  <!-- Interactive Pan/Zoom Blueprint Viewport -->
  <main id="canvasContainer" onmousemove="handleMouseMove(event)">
    <!-- Sheet 1 (Master Plan) -->
    <div class="blueprint-viewport" id="viewportSheet1">
      {s1_clean}
    </div>

    <!-- Sheet 2 (Riser Elevation) -->
    <div class="blueprint-viewport" id="viewportSheet2" style="display:none;">
      {s2_clean}
    </div>
  </main>

  <!-- Engineering HUD Status Bar -->
  <footer>
    <div class="hud-left">
      <span id="coordDisplay">COORDINATES: X = 500.0 FT | Y = 100.0 FT</span>
      <span>SCALE: ARCHITECTURAL 1 FT = 5 PX (A0 / ARCH E)</span>
      <span id="activeSheetInfo">SHEET 1 OF 2: TOP-DOWN MASTER DISTRIBUTION BLUEPRINT</span>
    </div>
    <div class="hud-right">
      <span>PALETTE: CLASSIC PRUSSIAN BLUE (#0B2545) &amp; PURE WHITE</span>
      <span>APPROVED FOR FIELD EXECUTION</span>
    </div>
  </footer>

  <script>
    let activeSheet = 'sheet1';
    let scale = 1.0;
    let panX = 0;
    let panY = 0;
    let isDragging = false;
    let startX = 0;
    let startY = 0;

    const vp1 = document.getElementById('viewportSheet1');
    const vp2 = document.getElementById('viewportSheet2');
    const container = document.getElementById('canvasContainer');
    const zoomText = document.getElementById('zoomDisplay');
    const coordText = document.getElementById('coordDisplay');

    function getActiveViewport() {{
      return (activeSheet === 'sheet1') ? vp1 : vp2;
    }}

    function applyTransform() {{
      const vp = getActiveViewport();
      vp.style.transform = `scale(${{scale}}) translate(${{panX}}px, ${{panY}}px)`;
      zoomText.innerText = Math.round(scale * 100) + '%';
    }}

    function zoomIn() {{
      scale = Math.min(scale * 1.25, 8.0);
      applyTransform();
    }}

    function zoomOut() {{
      scale = Math.max(scale / 1.25, 0.25);
      applyTransform();
    }}

    function resetView() {{
      scale = 1.0;
      panX = 0;
      panY = 0;
      applyTransform();
    }}

    function switchSheet(sheetKey) {{
      activeSheet = sheetKey;
      document.getElementById('btnS1').classList.toggle('active', sheetKey === 'sheet1');
      document.getElementById('btnS2').classList.toggle('active', sheetKey === 'sheet2');

      vp1.style.display = (sheetKey === 'sheet1') ? 'flex' : 'none';
      vp2.style.display = (sheetKey === 'sheet2') ? 'flex' : 'none';

      document.getElementById('activeSheetInfo').innerText = 
        (sheetKey === 'sheet1') ? 'SHEET 1 OF 2: TOP-DOWN MASTER DISTRIBUTION BLUEPRINT'
                               : 'SHEET 2 OF 2: 4-FOOT OVERHEAD DOUBLE-TEE RISER MANIFOLD DETAIL';

      resetView();
    }}

    // Pan interactions
    container.addEventListener('mousedown', (e) => {{
      isDragging = true;
      startX = e.clientX - panX;
      startY = e.clientY - panY;
    }});

    window.addEventListener('mouseup', () => {{
      isDragging = false;
    }});

    container.addEventListener('mousemove', (e) => {{
      if (isDragging) {{
        panX = e.clientX - startX;
        panY = e.clientY - startY;
        applyTransform();
      }}
    }});

    container.addEventListener('wheel', (e) => {{
      e.preventDefault();
      if (e.deltaY < 0) zoomIn();
      else zoomOut();
    }});

    // Live Coordinate readout
    function handleMouseMove(e) {{
      const rect = container.getBoundingClientRect();
      const normX = (e.clientX - rect.left) / rect.width;
      const normY = (e.clientY - rect.top) / rect.height;

      if (activeSheet === 'sheet1') {{
        // Map 0..1 to CAD Foot Coordinates
        const feetX = Math.round(100 + normX * (700 - 100));
        const feetY = Math.round(380 - normY * (380 - 0));
        coordText.innerText = `FIELD COORD: X = ${{feetX}} FT | Y = ${{feetY}} FT`;
      }} else {{
        const elev = (4.0 - normY * 7.0).toFixed(2);
        coordText.innerText = `ELEVATION: ${{elev}} FT DATUM`;
      }}
    }}

    // Keyboard navigation
    window.addEventListener('keydown', (e) => {{
      if (e.key === '1') switchSheet('sheet1');
      if (e.key === '2') switchSheet('sheet2');
      if (e.key === '+' || e.key === '=') zoomIn();
      if (e.key === '-' || e.key === '_') zoomOut();
      if (e.key === '0' || e.key === 'r') resetView();
    }});
  </script>
</body>
</html>
"""
    # Write to package dir
    pkg_index = os.path.join(pkg_dir, "index.html")
    with open(pkg_index, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Interactive Blueprint HTML written to package: {pkg_index}")

    # Write also to root dir
    root_index = os.path.join(root_dir, "index.html")
    # For root index, fix relative PDF links to point to irrigation_package/
    root_html = html.replace('href="Moringa_2Acre_Irrigation_Blueprint_2Page.pdf"', 'href="irrigation_package/Moringa_2Acre_Irrigation_Blueprint_2Page.pdf"')
    with open(root_index, "w", encoding="utf-8") as f:
        f.write(root_html)
    print(f"Interactive Blueprint HTML written to root: {root_index}")

if __name__ == "__main__":
    pkg = sys.argv[1] if len(sys.argv) > 1 else "./irrigation_package"
    root = sys.argv[2] if len(sys.argv) > 2 else "."
    build_index(pkg, root)
