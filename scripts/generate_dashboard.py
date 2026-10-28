import os
import sys

def build_dashboard(pkg_dir, root_dir):
    # Paths to generated files
    master_svg_path = os.path.join(pkg_dir, "CAD_Master_Blueprint.svg")
    riser_svg_path = os.path.join(pkg_dir, "Riser_Manifold_Detail.svg")
    exploded_svg_path = os.path.join(pkg_dir, "Riser_Manifold_Exploded_View.svg")
    takeoff_svg_path = os.path.join(pkg_dir, "Lateral_Takeoff_Details.svg")

    with open(master_svg_path, "r", encoding="utf-8") as f:
        master_svg_content = f.read()
    with open(riser_svg_path, "r", encoding="utf-8") as f:
        riser_svg_content = f.read()
    with open(exploded_svg_path, "r", encoding="utf-8") as f:
        exploded_svg_content = f.read()
    with open(takeoff_svg_path, "r", encoding="utf-8") as f:
        takeoff_svg_content = f.read()

    # Strip XML header from SVGs if present
    def clean_svg(s):
        idx = s.find("<svg")
        if idx != -1:
            return s[idx:]
        return s

    master_svg_clean = clean_svg(master_svg_content)
    riser_svg_clean = clean_svg(riser_svg_content)
    exploded_svg_clean = clean_svg(exploded_svg_content)
    takeoff_svg_clean = clean_svg(takeoff_svg_content)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>2-Acre Moringa Drip Irrigation — Engineering Master Dashboard</title>
  <style>
    :root {{
      --bg: #090d16;
      --card-bg: #111827;
      --panel-bg: #1e293b;
      --border: #334155;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --primary: #0284c7;
      --primary-light: #38bdf8;
      --accent-green: #10b981;
      --accent-orange: #f97316;
      --accent-purple: #a855f7;
      --accent-yellow: #facc15;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      line-height: 1.5;
      overflow-x: hidden;
    }}
    header {{
      background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
      border-bottom: 2px solid var(--border);
      padding: 1.5rem 2rem;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }}
    .header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }}
    .title-group h1 {{
      font-size: 1.75rem;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}
    .badge {{
      font-size: 0.75rem;
      padding: 0.25rem 0.6rem;
      border-radius: 9999px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .badge-primary {{ background: rgba(2, 132, 199, 0.2); color: var(--primary-light); border: 1px solid var(--primary); }}
    .badge-green {{ background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid var(--accent-green); }}
    .badge-orange {{ background: rgba(249, 115, 22, 0.2); color: #fb923c; border: 1px solid var(--accent-orange); }}
    .subtitle {{
      color: var(--text-muted);
      font-size: 0.95rem;
      margin-top: 0.25rem;
    }}
    .toolchain-pills {{
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }}
    .pill {{
      background: #1e293b;
      border: 1px solid #475569;
      color: #cbd5e1;
      padding: 0.3rem 0.7rem;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 600;
    }}
    .kpi-bar {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-top: 1.25rem;
      padding-top: 1.25rem;
      border-top: 1px solid rgba(255,255,255,0.1);
    }}
    .kpi-card {{
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.75rem 1rem;
    }}
    .kpi-label {{
      font-size: 0.75rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .kpi-val {{
      font-size: 1.25rem;
      font-weight: 800;
      color: #ffffff;
      margin-top: 0.15rem;
    }}
    .main-layout {{
      display: grid;
      grid-template-columns: 1fr 380px;
      gap: 1.5rem;
      padding: 1.5rem 2rem;
      max-width: 1920px;
      margin: 0 auto;
    }}
    @media (max-width: 1200px) {{
      .main-layout {{
        grid-template-columns: 1fr;
      }}
    }}
    .viewer-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }}
    .tabs-header {{
      display: flex;
      background: #0f172a;
      border-bottom: 1px solid var(--border);
      overflow-x: auto;
    }}
    .tab-btn {{
      background: none;
      border: none;
      color: var(--text-muted);
      padding: 1rem 1.5rem;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      border-bottom: 3px solid transparent;
      white-space: nowrap;
      transition: all 0.2s;
    }}
    .tab-btn:hover {{
      color: #ffffff;
      background: rgba(255,255,255,0.02);
    }}
    .tab-btn.active {{
      color: var(--primary-light);
      border-bottom-color: var(--primary-light);
      background: rgba(2, 132, 199, 0.08);
    }}
    .viewer-toolbar {{
      background: #1e293b;
      padding: 0.75rem 1.25rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
      border-bottom: 1px solid var(--border);
    }}
    .tool-group {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .btn {{
      background: #334155;
      color: #ffffff;
      border: 1px solid #475569;
      padding: 0.4rem 0.8rem;
      border-radius: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.2s;
      text-decoration: none;
    }}
    .btn:hover {{
      background: #475569;
      border-color: #64748b;
    }}
    .btn-primary {{
      background: var(--primary);
      border-color: #0284c7;
    }}
    .btn-primary:hover {{
      background: #0369a1;
    }}
    .btn-success {{
      background: #059669;
      border-color: #10b981;
    }}
    .btn-success:hover {{
      background: #047857;
    }}
    .layer-toggles {{
      display: flex;
      gap: 0.4rem;
      flex-wrap: wrap;
    }}
    .layer-chip {{
      font-size: 0.75rem;
      padding: 0.25rem 0.6rem;
      border-radius: 4px;
      cursor: pointer;
      border: 1px solid transparent;
      user-select: none;
      font-weight: 600;
    }}
    .chip-mainline {{ background: rgba(59, 130, 246, 0.2); border-color: #3b82f6; color: #93c5fd; }}
    .chip-plota {{ background: rgba(16, 185, 129, 0.2); border-color: #10b981; color: #6ee7b7; }}
    .chip-plotb {{ background: rgba(249, 115, 22, 0.2); border-color: #f97316; color: #fdba74; }}
    .chip-valves {{ background: rgba(239, 68, 68, 0.2); border-color: #ef4444; color: #fca5a5; }}
    .chip-annotations {{ background: rgba(250, 204, 21, 0.2); border-color: #facc15; color: #fef08a; }}
    
    .viewport-container {{
      position: relative;
      background: #070b14;
      height: 680px;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
      cursor: grab;
    }}
    .viewport-container:active {{
      cursor: grabbing;
    }}
    .svg-wrapper {{
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      transform-origin: center center;
      transition: transform 0.05s ease-out;
    }}
    .svg-wrapper svg {{
      max-width: 100%;
      max-height: 100%;
      display: block;
    }}
    .coord-hud {{
      position: absolute;
      bottom: 12px;
      left: 12px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border);
      padding: 0.35rem 0.75rem;
      border-radius: 6px;
      font-family: monospace;
      font-size: 0.8rem;
      color: var(--primary-light);
      pointer-events: none;
    }}
    
    /* SIDEBAR & INSPECTOR */
    .sidebar {{
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }}
    .panel {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.25rem;
      box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .panel-title {{
      font-size: 1.1rem;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.5rem;
    }}
    .node-selector {{
      width: 100%;
      background: #1e293b;
      border: 1px solid #475569;
      color: #ffffff;
      padding: 0.6rem;
      border-radius: 6px;
      font-size: 0.9rem;
      margin-bottom: 1rem;
    }}
    .inspector-prop {{
      display: flex;
      justify-content: space-between;
      padding: 0.45rem 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      font-size: 0.85rem;
    }}
    .inspector-prop:last-child {{
      border-bottom: none;
    }}
    .prop-name {{
      color: var(--text-muted);
    }}
    .prop-val {{
      font-weight: 600;
      color: #ffffff;
      text-align: right;
    }}
    
    /* CHECKLIST */
    .checklist {{
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
    }}
    .check-item {{
      display: flex;
      align-items: flex-start;
      gap: 0.6rem;
      background: #1e293b;
      padding: 0.6rem 0.8rem;
      border-radius: 6px;
      border: 1px solid #334155;
      font-size: 0.85rem;
      cursor: pointer;
    }}
    .check-item input {{
      margin-top: 0.2rem;
      accent-color: var(--accent-green);
    }}
    .progress-bar {{
      height: 8px;
      background: #334155;
      border-radius: 4px;
      overflow: hidden;
      margin-top: 0.5rem;
      margin-bottom: 1rem;
    }}
    .progress-fill {{
      height: 100%;
      background: var(--accent-green);
      width: 25%;
      transition: width 0.3s;
    }}

    /* DOWNLOAD CENTER */
    .download-section {{
      padding: 2rem;
      background: #0f172a;
      border-top: 2px solid var(--border);
      margin-top: 2rem;
    }}
    .download-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.25rem;
      margin-top: 1.25rem;
    }}
    .dl-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s, border-color 0.2s;
    }}
    .dl-card:hover {{
      transform: translateY(-3px);
      border-color: var(--primary-light);
    }}
    .dl-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 0.25rem;
    }}
    .dl-meta {{
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-bottom: 1rem;
    }}
    .dl-links {{
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }}
    .table-responsive {{
      overflow-x: auto;
      margin-top: 1rem;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
    }}
    th, td {{
      padding: 0.6rem 0.8rem;
      text-align: left;
      border-bottom: 1px solid var(--border);
    }}
    th {{
      background: #1e293b;
      color: var(--text-muted);
      font-weight: 600;
    }}
    tr:hover td {{
      background: rgba(255,255,255,0.02);
    }}
  </style>
</head>
<body>

  <header>
    <div class="header-top">
      <div class="title-group">
        <h1>2-ACRE MORINGA DRIP IRRIGATION</h1>
        <span class="badge badge-primary">PKM-1 &amp; BHAGYA</span>
        <span class="badge badge-green">ENGINEERING DOSSIER APPROVED</span>
      </div>
      <div class="toolchain-pills">
        <span class="pill">CADCraft 2D</span>
        <span class="pill">VectorCraft SVG</span>
        <span class="pill">GridCraft Excel</span>
        <span class="pill">WordCraft Docs</span>
        <span class="pill">DeckCraft Slides</span>
        <span class="pill">PdfCraft Combined</span>
      </div>
    </div>
    <p class="subtitle">Complete Hydraulic, Drafting &amp; Field Plumbing Execution Master Control Dashboard</p>

    <div class="kpi-bar">
      <div class="kpi-card">
        <div class="kpi-label">Solar Water Source</div>
        <div class="kpi-val">5.0 HP DC Submersible</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Dynamic Head &amp; Pressure</div>
        <div class="kpi-val">2.5 kg/cm² (35.5 PSI)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">2" Mainline Pipeline</div>
        <div class="kpi-val">730 ft (63mm PVC)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Plot A Plants (PKM-1)</div>
        <div class="kpi-val">3,000 Plants (3x5 ft)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Plot B Plants (Bhagya)</div>
        <div class="kpi-val">750 Plants (7x8 ft)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Overhead Riser Stations</div>
        <div class="kpi-val">8 Stations (+4.0' Waist)</div>
      </div>
    </div>
  </header>

  <div class="main-layout">
    <!-- LEFT COLUMN: BLUEPRINT VIEWER -->
    <div class="viewer-card">
      <div class="tabs-header">
        <button class="tab-btn active" onclick="switchTab('master')">CAD Master Blueprint (Plan View)</button>
        <button class="tab-btn" onclick="switchTab('riser')">4ft Riser Manifold Elevation</button>
        <button class="tab-btn" onclick="switchTab('exploded')">Exploded Vector Assembly</button>
        <button class="tab-btn" onclick="switchTab('takeoff')">Lateral Take-Off Details</button>
        <button class="tab-btn" onclick="switchTab('bom')">Live Master BOM &amp; Rates</button>
      </div>

      <div class="viewer-toolbar">
        <div class="tool-group">
          <button class="btn" onclick="zoomIn()">🔍+ Zoom In</button>
          <button class="btn" onclick="zoomOut()">🔍- Zoom Out</button>
          <button class="btn" onclick="resetZoom()">↺ Reset</button>
          <span style="font-size:0.85rem; color:var(--text-muted); margin-left:0.5rem;" id="zoomLevel">100%</span>
        </div>

        <div class="layer-toggles" id="masterLayerToggles">
          <span class="layer-chip chip-mainline" onclick="toggleLayer('02_MAINLINE_2IN_63MM')">2" Mainline</span>
          <span class="layer-chip chip-plota" onclick="toggleLayer('03_SUBLINE_1.5IN_50MM_PLOTA')">1.5" Subline A</span>
          <span class="layer-chip chip-plotb" onclick="toggleLayer('04_SUBLINE_1.25IN_40MM_PLOTB')">1.25" Subline B</span>
          <span class="layer-chip chip-plota" onclick="toggleLayer('05_LATERALS_16MM_INLINE_PLOTA')">Inline Laterals A</span>
          <span class="layer-chip chip-plotb" onclick="toggleLayer('06_LATERALS_16MM_ONLINE_PLOTB')">Online Laterals B</span>
          <span class="layer-chip chip-valves" onclick="toggleLayer('07_RISER_VALVES_FITTINGS')">Valves &amp; Risers</span>
          <span class="layer-chip chip-annotations" onclick="toggleLayer('08_DIMENSIONS_ANNOTATIONS')">Dimensions</span>
        </div>
      </div>

      <!-- VIEWPORT 1: MASTER BLUEPRINT -->
      <div class="viewport-container" id="viewportMaster" onmousemove="updateCoords(event)">
        <div class="svg-wrapper" id="svgWrapperMaster">
          {master_svg_clean}
        </div>
        <div class="coord-hud" id="coordHud">CAD Coordinates: X=500.0 ft, Y=100.0 ft (Tee A)</div>
      </div>

      <!-- VIEWPORT 2: RISER DETAIL -->
      <div class="viewport-container" id="viewportRiser" style="display:none;">
        <div class="svg-wrapper" id="svgWrapperRiser">
          {riser_svg_clean}
        </div>
      </div>

      <!-- VIEWPORT 3: EXPLODED VIEW -->
      <div class="viewport-container" id="viewportExploded" style="display:none;">
        <div class="svg-wrapper" id="svgWrapperExploded">
          {exploded_svg_clean}
        </div>
      </div>

      <!-- VIEWPORT 4: TAKEOFF DETAILS -->
      <div class="viewport-container" id="viewportTakeoff" style="display:none;">
        <div class="svg-wrapper" id="svgWrapperTakeoff">
          {takeoff_svg_clean}
        </div>
      </div>

      <!-- VIEWPORT 5: LIVE BOM TABLE -->
      <div class="viewport-container" id="viewportBom" style="display:none; overflow-y:auto; padding:1.5rem; align-items:flex-start;">
        <div style="width:100%;">
          <h3 style="margin-bottom:0.75rem; color:var(--primary-light);">GridCraft Multi-Sheet Inventory &amp; Cost Breakdown</h3>
          <div class="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Item #</th>
                  <th>Category</th>
                  <th>Description</th>
                  <th>Unit</th>
                  <th>Ordered</th>
                  <th>Planned</th>
                  <th>Spare</th>
                  <th>Rate (₹)</th>
                  <th>Total (₹)</th>
                </tr>
              </thead>
              <tbody>
                <tr><td>1</td><td>PVC Pipes</td><td>2" (63mm) PVC Pipe Class 2 (20ft)</td><td>Lengths</td><td>45</td><td>37</td><td>8</td><td>420.00</td><td>18,900.00</td></tr>
                <tr><td>2</td><td>PVC Fittings</td><td>2" PVC 90° Elbow</td><td>Nos</td><td>30</td><td>18</td><td>12</td><td>45.00</td><td>1,350.00</td></tr>
                <tr><td>3</td><td>PVC Fittings</td><td>2" PVC Equal Tee</td><td>Nos</td><td>30</td><td>12</td><td>18</td><td>55.00</td><td>1,650.00</td></tr>
                <tr><td>7</td><td>PVC Pipes</td><td>1.5" (50mm) PVC Pipe Class 2</td><td>Lengths</td><td>10</td><td>8</td><td>2</td><td>310.00</td><td>3,100.00</td></tr>
                <tr><td>8</td><td>PVC Fittings</td><td>1.5" PVC 90° Elbow</td><td>Nos</td><td>40</td><td>16</td><td>24</td><td>32.00</td><td>1,280.00</td></tr>
                <tr><td>11</td><td>PVC Pipes</td><td>1.25" (40mm) PVC Pipe Class 2</td><td>Lengths</td><td>15</td><td>14</td><td>1</td><td>240.00</td><td>3,600.00</td></tr>
                <tr><td>12</td><td>PVC Fittings</td><td>1.25" PVC 90° Elbow</td><td>Nos</td><td>30</td><td>16</td><td>14</td><td>25.00</td><td>750.00</td></tr>
                <tr style="background:rgba(2,132,199,0.1);"><td>18</td><td>Drip Invoice</td><td>16mm Plain Lateral Pipe</td><td>Mtrs</td><td>2000</td><td>1610</td><td>390</td><td>7.25</td><td>14,500.00</td></tr>
                <tr style="background:rgba(2,132,199,0.1);"><td>19</td><td>Drip Invoice</td><td>Tunning Dripper (P)</td><td>Nos</td><td>800</td><td>768</td><td>32</td><td>4.00</td><td>3,200.00</td></tr>
                <tr style="background:rgba(2,132,199,0.1);"><td>25</td><td>Drip Invoice</td><td>16x4x40 Inline Pipe</td><td>Mtrs</td><td>3000</td><td>2926</td><td>74</td><td>5.50</td><td>16,500.00</td></tr>
                <tr style="background:rgba(2,132,199,0.1);"><td>26</td><td>Drip Invoice</td><td>50x16x2 Way Take-Off Collar</td><td>Nos</td><td>25</td><td>24</td><td>1</td><td>30.00</td><td>750.00</td></tr>
                <tr style="background:rgba(2,132,199,0.1);"><td>23</td><td>Drip Invoice</td><td>40x16x1Way TF Collar</td><td>Nos</td><td>35</td><td>32</td><td>3</td><td>25.00</td><td>875.00</td></tr>
                <tr style="background:rgba(2,132,199,0.1);"><td>28</td><td>Drip Invoice</td><td>2" Filter 'T' Type</td><td>Nos</td><td>1</td><td>1</td><td>0</td><td>2,750.00</td><td>2,750.00</td></tr>
                <tr style="background:rgba(2,132,199,0.1);"><td>29</td><td>Drip Invoice</td><td>40mm Plain Ball Valve</td><td>Nos</td><td>8</td><td>8</td><td>0</td><td>130.00</td><td>1,040.00</td></tr>
                <tr style="background:rgba(2,132,199,0.1);"><td>30</td><td>Drip Invoice</td><td>50mm Plain Ball Valve</td><td>Nos</td><td>8</td><td>8</td><td>0</td><td>210.00</td><td>1,680.00</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- RIGHT COLUMN: NODE INSPECTOR & EXECUTION PROGRESS -->
    <div class="sidebar">
      <!-- NODE INSPECTOR PANEL -->
      <div class="panel">
        <div class="panel-title">
          <span>⚙️ Station &amp; Node Inspector</span>
        </div>
        <select class="node-selector" id="nodeSelect" onchange="inspectNode(this.value)">
          <option value="borewell">Solar Borewell &amp; Head Unit (590, 20)</option>
          <option value="corner">2" Corner Tee Station (590, 100)</option>
          <option value="teea" selected>Tee A — Plot A Center Entry (500, 100)</option>
          <option value="teeb">Tee B — Plot B Entry Corner (285, 100)</option>
          <option value="ra1">Riser Station A1 (500, 130)</option>
          <option value="ra2">Riser Station A2 (500, 160)</option>
          <option value="ra3">Riser Station A3 (500, 190)</option>
          <option value="ra4">Riser Station A4 (500, 220)</option>
          <option value="rb1">Riser Station B1 (285, 124)</option>
          <option value="rb2">Riser Station B2 (285, 188)</option>
          <option value="rb3">Riser Station B3 (285, 252)</option>
          <option value="rb4">Riser Station B4 (285, 316)</option>
        </select>

        <div id="inspectorContent">
          <div class="inspector-prop"><span class="prop-name">Station Identity:</span><span class="prop-val" id="insName">Tee A (Plot A Center Entry)</span></div>
          <div class="inspector-prop"><span class="prop-name">CAD Coordinates:</span><span class="prop-val" id="insCoords">X=500.00', Y=100.00'</span></div>
          <div class="inspector-prop"><span class="prop-name">Zone Allocation:</span><span class="prop-val" id="insZone">Zone 2 (Plot A) &amp; Zone 1 Mainline</span></div>
          <div class="inspector-prop"><span class="prop-name">Mainline Pipe:</span><span class="prop-val" id="insPipe">2" PVC (63mm) Class 2</span></div>
          <div class="inspector-prop"><span class="prop-name">Branch Direction:</span><span class="prop-val" id="insBranch">North to (500,245) &amp; West to (285,100)</span></div>
          <div class="inspector-prop"><span class="prop-name">Fittings Installed:</span><span class="prop-val" id="insFittings">2" PVC Equal Tee</span></div>
          <div class="inspector-prop"><span class="prop-name">Connected Load:</span><span class="prop-val" id="insLoad">Feeds 3,000 PKM-1 + 750 Bhagya</span></div>
          <div class="inspector-prop"><span class="prop-name">Dynamic Pressure:</span><span class="prop-val" id="insPress">2.35 kg/cm²</span></div>
        </div>
      </div>

      <!-- STAGE CHECKLIST PANEL -->
      <div class="panel">
        <div class="panel-title">
          <span>📋 Field Execution Checklist</span>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:var(--text-muted);">
          <span>Completion Progress</span>
          <span id="progressText" style="font-weight:700; color:var(--accent-green);">100%</span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" id="progressFill" style="width:100%;"></div>
        </div>
        <div class="checklist">
          <label class="check-item"><input type="checkbox" checked onchange="updateProgress()"> <strong>Stage 1:</strong> Solar Borewell Head &amp; 2" Mainline (730')</label>
          <label class="check-item"><input type="checkbox" checked onchange="updateProgress()"> <strong>Stage 2:</strong> Plot A 4 Overhead Risers &amp; 24 Inline Trenches</label>
          <label class="check-item"><input type="checkbox" checked onchange="updateProgress()"> <strong>Stage 3:</strong> Plot B 4 Overhead Risers &amp; 32 Online Rows</label>
          <label class="check-item"><input type="checkbox" checked onchange="updateProgress()"> <strong>Stage 4:</strong> Subline Flushing (16 Valves) &amp; Pressure Test</label>
          <label class="check-item"><input type="checkbox" checked onchange="updateProgress()"> <strong>Stage 5:</strong> Emitter Uniformity Audit &amp; Handover</label>
        </div>
      </div>
    </div>
  </div>

  <!-- ARTCRAFT DOWNLOAD CENTER -->
  <section class="download-section">
    <div style="max-width:1920px; margin:0 auto;">
      <h2 style="font-size:1.5rem; font-weight:800; color:#ffffff; display:flex; align-items:center; gap:0.5rem;">
        <span>📦 ArtCraft Engineering Package Deliverables</span>
        <span class="badge badge-primary">8 Toolchain Formats</span>
      </h2>
      <p style="color:var(--text-muted); font-size:0.95rem; margin-top:0.25rem;">
        All engineering assets generated via headless MCP &amp; CLI execution into <code>./irrigation_package/</code>
      </p>

      <div class="download-grid">
        <!-- 1. Master CAD Drawings -->
        <div class="dl-card">
          <div>
            <div class="dl-title">CADCraft Master Drawings</div>
            <div class="dl-meta">Scale: 1 Unit = 1 Foot • Model &amp; Detail Sheets</div>
          </div>
          <div class="dl-links">
            <a href="Moringa_2Acre_Irrigation_Master.dwg" download class="btn btn-primary">.DWG</a>
            <a href="Moringa_2Acre_Irrigation_Master.dxf" download class="btn">.DXF</a>
            <a href="CAD_Master_Blueprint.pdf" download class="btn">.PDF</a>
            <a href="CAD_Master_Blueprint.svg" download class="btn">.SVG</a>
            <a href="CAD_Master_Blueprint.png" download class="btn">.PNG</a>
          </div>
        </div>

        <!-- 2. Riser Cross-Section CAD -->
        <div class="dl-card">
          <div>
            <div class="dl-title">Riser Manifold Cross-Section</div>
            <div class="dl-meta">CADCraft Detail Sheet • +4.0' Overhead Manifold</div>
          </div>
          <div class="dl-links">
            <a href="Riser_Manifold_Detail.dwg" download class="btn btn-primary">.DWG</a>
            <a href="Riser_Manifold_Detail.dxf" download class="btn">.DXF</a>
            <a href="Riser_Manifold_Detail.pdf" download class="btn">.PDF</a>
            <a href="Riser_Manifold_Detail.svg" download class="btn">.SVG</a>
            <a href="Riser_Manifold_Detail.png" download class="btn">.PNG</a>
          </div>
        </div>

        <!-- 3. VectorCraft Diagrams -->
        <div class="dl-card">
          <div>
            <div class="dl-title">VectorCraft Assembly Diagrams</div>
            <div class="dl-meta">Exploded Isometric &amp; Take-off Comparative Details</div>
          </div>
          <div class="dl-links">
            <a href="Riser_Manifold_Exploded_View.svg" download class="btn btn-success">Exploded SVG</a>
            <a href="Riser_Manifold_Exploded_View.pdf" download class="btn">Exploded PDF</a>
            <a href="Lateral_Takeoff_Details.svg" download class="btn btn-success">Take-off SVG</a>
            <a href="Lateral_Takeoff_Details.pdf" download class="btn">Take-off PDF</a>
          </div>
        </div>

        <!-- 4. GridCraft Multi-Sheet Workbook -->
        <div class="dl-card">
          <div>
            <div class="dl-title">GridCraft BOM &amp; Schedule</div>
            <div class="dl-meta">Live Excel Formulas • Zone Splits • Tape Schedules</div>
          </div>
          <div class="dl-links">
            <a href="Moringa_Irrigation_BOM_and_Schedule.xlsx" download class="btn btn-success">.XLSX Workbook</a>
            <a href="BOM_Schedule.pdf" download class="btn">Plotted PDF</a>
          </div>
        </div>

        <!-- 5. WordCraft Installation Manual -->
        <div class="dl-card">
          <div>
            <div class="dl-title">Field Installation Manual</div>
            <div class="dl-meta">WordCraft 10-Section Field Plumbing Guide</div>
          </div>
          <div class="dl-links">
            <a href="Field_Plumbing_Installation_Manual.docx" download class="btn btn-primary">.DOCX</a>
            <a href="Field_Plumbing_Installation_Manual.pdf" download class="btn">.PDF</a>
            <a href="Field_Plumbing_Installation_Manual.md" download class="btn">.MD</a>
          </div>
        </div>

        <!-- 6. DeckCraft Presentation -->
        <div class="dl-card">
          <div>
            <div class="dl-title">DeckCraft Execution Briefing</div>
            <div class="dl-meta">Stage-by-Stage Field Briefing Slide Deck</div>
          </div>
          <div class="dl-links">
            <a href="Irrigation_Execution_Briefing.pptx" download class="btn btn-primary">.PPTX Deck</a>
            <a href="Irrigation_Execution_Briefing.pdf" download class="btn">.PDF Slides</a>
          </div>
        </div>

        <!-- 7. Master Unified Dossier -->
        <div class="dl-card" style="border-color:var(--accent-green); background:rgba(16, 185, 129, 0.05);">
          <div>
            <div class="dl-title" style="color:#34d399;">PdfCraft Master Dossier</div>
            <div class="dl-meta">Unified 20-Page Bookmarked Engineering Package</div>
          </div>
          <div class="dl-links">
            <a href="Moringa_2Acre_Irrigation_Master_Dossier.pdf" download class="btn btn-success" style="width:100%; justify-content:center; padding:0.6rem;">
              📥 Download Complete Master Dossier (.PDF)
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <script>
    // Tab switching
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');

      document.getElementById('viewportMaster').style.display = (tabId === 'master') ? 'flex' : 'none';
      document.getElementById('viewportRiser').style.display = (tabId === 'riser') ? 'flex' : 'none';
      document.getElementById('viewportExploded').style.display = (tabId === 'exploded') ? 'flex' : 'none';
      document.getElementById('viewportTakeoff').style.display = (tabId === 'takeoff') ? 'flex' : 'none';
      document.getElementById('viewportBom').style.display = (tabId === 'bom') ? 'block' : 'none';

      document.getElementById('masterLayerToggles').style.display = (tabId === 'master') ? 'flex' : 'none';
    }}

    // Pan & Zoom Logic
    let currentScale = 1.0;
    let translateX = 0;
    let translateY = 0;
    let isDragging = false;
    let startX = 0;
    let startY = 0;

    const wrapper = document.getElementById('svgWrapperMaster');
    const viewport = document.getElementById('viewportMaster');

    function applyTransform() {{
      wrapper.style.transform = `scale(${{currentScale}}) translate(${{translateX}}px, ${{translateY}}px)`;
      document.getElementById('zoomLevel').innerText = Math.round(currentScale * 100) + '%';
    }}

    function zoomIn() {{
      currentScale = Math.min(currentScale * 1.25, 5.0);
      applyTransform();
    }}

    function zoomOut() {{
      currentScale = Math.max(currentScale / 1.25, 0.4);
      applyTransform();
    }}

    function resetZoom() {{
      currentScale = 1.0;
      translateX = 0;
      translateY = 0;
      applyTransform();
    }}

    viewport.addEventListener('mousedown', (e) => {{
      isDragging = true;
      startX = e.clientX - translateX;
      startY = e.clientY - translateY;
    }});

    window.addEventListener('mouseup', () => {{
      isDragging = false;
    }});

    viewport.addEventListener('mousemove', (e) => {{
      if (isDragging) {{
        translateX = e.clientX - startX;
        translateY = e.clientY - startY;
        applyTransform();
      }}
    }});

    viewport.addEventListener('wheel', (e) => {{
      e.preventDefault();
      if (e.deltaY < 0) zoomIn();
      else zoomOut();
    }});

    // Layer Toggling
    function toggleLayer(layerName) {{
      const el = event.target;
      el.classList.toggle('inactive');
      const opacity = el.classList.contains('inactive') ? '0.1' : '1.0';
      
      // Look for elements with this layer inside the SVG
      const layerNodes = wrapper.querySelectorAll(`[id*="${{layerName}}"], [class*="${{layerName}}"]`);
      layerNodes.forEach(node => {{
        node.style.opacity = opacity;
      }});
    }}

    // Coordinate HUD
    function updateCoords(e) {{
      const rect = viewport.getBoundingClientRect();
      const relX = (e.clientX - rect.left) / rect.width;
      const relY = (e.clientY - rect.top) / rect.height;
      
      // Map to real CAD bounds: X [80, 720], Y [0, 380]
      const cadX = Math.round(80 + relX * (720 - 80));
      const cadY = Math.round(380 - relY * (380 - 0));
      
      document.getElementById('coordHud').innerText = `CAD Coordinates: X = ${{cadX}} ft, Y = ${{cadY}} ft (Scale: 1 Unit = 1 Foot)`;
    }}

    // Node Inspector Database
    const nodeDb = {{
      borewell: {{
        name: "5 HP Solar Borewell & Head Unit",
        coords: "X = 590.00', Y = 20.00'",
        zone: "Zone 1 (Head Infrastructure)",
        pipe: "2\" Class 2 (6 kg/cm²) PVC",
        branch: "Northward Run to Corner Tee (80 ft)",
        fittings: "2\" NRV, 2\" Gate Valve, 2\" T-Filter, 2\" End Cap (S)",
        load: "Full Farm Flow Capacity: 22,000 LPH",
        press: "2.50 kg/cm² (Delivery Pressure)"
      }},
      corner: {{
        name: "Corner Tee Station",
        coords: "X = 590.00', Y = 100.00'",
        zone: "Zone 1 Mainline Junction",
        pipe: "2\" PVC Class 2",
        branch: "Westward Run to Tee A (90 ft)",
        fittings: "2\" Equal Tee, 2\" End Cap (East Stub)",
        load: "Transfers Full Flow to Tee A",
        press: "2.45 kg/cm²"
      }},
      teea: {{
        name: "Tee A — Plot A Center Entry",
        coords: "X = 500.00', Y = 100.00'",
        zone: "Plot A Center Entry & Inter-Plot Mainline",
        pipe: "2\" PVC Class 2",
        branch: "North 145' up Plot A & West 215' to Tee B",
        fittings: "2\" Equal Tee Junction",
        load: "Feeds Plot A (3,000 plants) & Plot B (750 plants)",
        press: "2.40 kg/cm²"
      }},
      teeb: {{
        name: "Tee B — Plot B Entry Corner",
        coords: "X = 285.00', Y = 100.00'",
        zone: "Plot B East-Boundary Entry",
        pipe: "2\" PVC Class 2",
        branch: "North 240' along East Edge of Plot B",
        fittings: "2\" Equal Tee, 2\" End Cap (West Stub)",
        load: "Feeds Plot B (750 Bhagya plants)",
        press: "2.30 kg/cm²"
      }},
      ra1: {{
        name: "Riser Station A1",
        coords: "X = 500.00', Y = 130.00' (30' from Tee A)",
        zone: "Plot A (PKM-1)",
        pipe: "2\" Riser to 1.5\" (50mm) Sublines",
        branch: "Sublines: 15' South & 15' North (Y=115 to 145)",
        fittings: "4ft Riser, Overhead Tee, 2x 50mm Valves, 2x Flush Valves",
        load: "6 Trenches (750 PKM-1 trees)",
        press: "2.20 kg/cm²"
      }},
      ra2: {{
        name: "Riser Station A2",
        coords: "X = 500.00', Y = 160.00' (60' from Tee A)",
        zone: "Plot A (PKM-1)",
        pipe: "2\" Riser to 1.5\" (50mm) Sublines",
        branch: "Sublines: 15' South & 15' North (Y=145 to 175)",
        fittings: "4ft Riser, Overhead Tee, 2x 50mm Valves, 2x Flush Valves",
        load: "6 Trenches (750 PKM-1 trees)",
        press: "2.18 kg/cm²"
      }},
      ra3: {{
        name: "Riser Station A3",
        coords: "X = 500.00', Y = 190.00' (90' from Tee A)",
        zone: "Plot A (PKM-1)",
        pipe: "2\" Riser to 1.5\" (50mm) Sublines",
        branch: "Sublines: 15' South & 15' North (Y=175 to 205)",
        fittings: "4ft Riser, Overhead Tee, 2x 50mm Valves, 2x Flush Valves",
        load: "6 Trenches (750 PKM-1 trees)",
        press: "2.15 kg/cm²"
      }},
      ra4: {{
        name: "Riser Station A4",
        coords: "X = 500.00', Y = 220.00' (120' from Tee A)",
        zone: "Plot A (PKM-1)",
        pipe: "2\" Riser to 1.5\" (50mm) Sublines",
        branch: "Sublines: 15' South & 15' North (Y=205 to 235)",
        fittings: "4ft Riser, Overhead Tee, 2x 50mm Valves, 2x Flush Valves",
        load: "6 Trenches (750 PKM-1 trees)",
        press: "2.12 kg/cm²"
      }},
      rb1: {{
        name: "Riser Station B1",
        coords: "X = 285.00', Y = 124.00' (24' from Tee B)",
        zone: "Plot B (Bhagya)",
        pipe: "2\" Riser to 1.25\" (40mm) Sublines",
        branch: "Sublines: 32' South & 32' North (Y=92 to 156)",
        fittings: "4ft Riser, Overhead Tee, 2x 40mm Valves, 2x Flush Valves",
        load: "8 Rows (192 Bhagya trees)",
        press: "2.15 kg/cm²"
      }},
      rb2: {{
        name: "Riser Station B2",
        coords: "X = 285.00', Y = 188.00' (88' from Tee B)",
        zone: "Plot B (Bhagya)",
        pipe: "2\" Riser to 1.25\" (40mm) Sublines",
        branch: "Sublines: 32' South & 32' North (Y=156 to 220)",
        fittings: "4ft Riser, Overhead Tee, 2x 40mm Valves, 2x Flush Valves",
        load: "8 Rows (192 Bhagya trees)",
        press: "2.12 kg/cm²"
      }},
      rb3: {{
        name: "Riser Station B3",
        coords: "X = 285.00', Y = 252.00' (152' from Tee B)",
        zone: "Plot B (Bhagya)",
        pipe: "2\" Riser to 1.25\" (40mm) Sublines",
        branch: "Sublines: 32' South & 32' North (Y=220 to 284)",
        fittings: "4ft Riser, Overhead Tee, 2x 40mm Valves, 2x Flush Valves",
        load: "8 Rows (192 Bhagya trees)",
        press: "2.08 kg/cm²"
      }},
      rb4: {{
        name: "Riser Station B4",
        coords: "X = 285.00', Y = 316.00' (216' from Tee B)",
        zone: "Plot B (Bhagya)",
        pipe: "2\" Riser to 1.25\" (40mm) Sublines",
        branch: "Sublines: 32' South & 32' North (Y=284 to 348)",
        fittings: "4ft Riser, Overhead Tee, 2x 40mm Valves, 2x Flush Valves",
        load: "8 Rows (192 Bhagya trees)",
        press: "2.05 kg/cm²"
      }}
    }};

    function inspectNode(nodeKey) {{
      const d = nodeDb[nodeKey];
      if (!d) return;
      document.getElementById('insName').innerText = d.name;
      document.getElementById('insCoords').innerText = d.coords;
      document.getElementById('insZone').innerText = d.zone;
      document.getElementById('insPipe').innerText = d.pipe;
      document.getElementById('insBranch').innerText = d.branch;
      document.getElementById('insFittings').innerText = d.fittings;
      document.getElementById('insLoad').innerText = d.load;
      document.getElementById('insPress').innerText = d.press;
    }}

    // Checklist Progress
    function updateProgress() {{
      const boxes = document.querySelectorAll('.check-item input');
      let checked = 0;
      boxes.forEach(b => {{ if (b.checked) checked++; }});
      const pct = Math.round((checked / boxes.length) * 100);
      document.getElementById('progressFill').style.width = pct + '%';
      document.getElementById('progressText').innerText = pct + '%';
    }}
  </script>
</body>
</html>
"""
    # Write to package dir
    pkg_index = os.path.join(pkg_dir, "index.html")
    with open(pkg_index, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Master Dashboard written to package: {pkg_index}")

    # Write also to root dir
    root_index = os.path.join(root_dir, "index.html")
    # For root index, adjust relative links to point to irrigation_package/
    root_html = html_content.replace('href="', 'href="irrigation_package/')
    with open(root_index, "w", encoding="utf-8") as f:
        f.write(root_html)
    print(f"Master Dashboard written to root: {root_index}")

if __name__ == "__main__":
    pkg = sys.argv[1] if len(sys.argv) > 1 else "./irrigation_package"
    root = sys.argv[2] if len(sys.argv) > 2 else "."
    build_dashboard(pkg, root)
