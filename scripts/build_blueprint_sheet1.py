import os
import sys

def build_sheet1_svg(output_path):
    # Canvas Size: 4200 x 2800 (A0 / Arch E Landscape)
    # Background: Prussian Blue #0B2545
    # Strict Palette: White #FFFFFF, Ice Cyan-White #E0F2FE, Lateral Cyan #7DD3FC, Annotation Light Blue #BAE6FD

    svg_lines = []
    svg_lines.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4200 2800" width="4200" height="2800" style="background:#0B2545; font-family:\'Courier New\', Courier, monospace;">')
    
    # 1. DEFS & PATTERNS
    svg_lines.append('''<defs>
  <!-- Subtle Blueprint Engineering Grid -->
  <pattern id="grid10" width="50" height="50" patternUnits="userSpaceOnUse">
    <path d="M 50 0 L 0 0 0 50" fill="none" stroke="rgba(255, 255, 255, 0.07)" stroke-width="1"/>
  </pattern>
  <pattern id="grid50" width="250" height="250" patternUnits="userSpaceOnUse">
    <rect width="250" height="250" fill="url(#grid10)" />
    <path d="M 250 0 L 0 0 0 250" fill="none" stroke="rgba(255, 255, 255, 0.16)" stroke-width="1.5"/>
  </pattern>

  <!-- Markers / Arrowheads -->
  <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#BAE6FD" />
  </marker>
  <marker id="arrow-white" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#FFFFFF" />
  </marker>
  <marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6">
    <circle cx="5" cy="5" r="3.5" fill="#BAE6FD" stroke="#0B2545" stroke-width="1"/>
  </marker>
</defs>''')

    # Grid background
    svg_lines.append('<rect width="4200" height="2800" fill="#0B2545"/>')
    svg_lines.append('<rect width="4200" height="2800" fill="url(#grid50)"/>')

    # 2. ARCHITECTURAL BORDER & TITLE BLOCK
    # Outer Border
    svg_lines.append('<rect x="120" y="100" width="3960" height="2600" fill="none" stroke="#FFFFFF" stroke-width="5"/>')
    # Inner Border (15px margin)
    svg_lines.append('<rect x="145" y="125" width="3910" height="2550" fill="none" stroke="#FFFFFF" stroke-width="2"/>')

    # Sheet Header (Top Left)
    svg_lines.append('''<g transform="translate(180, 190)">
  <text x="0" y="0" fill="#FFFFFF" font-size="44" font-weight="bold" letter-spacing="3">2-ACRE MORINGA COMMERCIAL ORCHARD — IRRIGATION ENGINEERING MASTER BLUEPRINT</text>
  <text x="0" y="38" fill="#BAE6FD" font-size="22" letter-spacing="1.5">HYDRAULIC DISTRIBUTION NETWORK • OVERHEAD DOUBLE-TEE RISERS • INLINE &amp; ONLINE DRIP LAYOUT</text>
  <text x="0" y="70" fill="#BAE6FD" font-size="16" letter-spacing="1">STANDARDS: IS 12786 (DRIP LATERALS) | IS 4985 (PVC PRESSURE PIPELINES) | DESIGN PRESSURE: 2.5 KG/CM²</text>
</g>''')

    # Compass & North Arrow (Top Right)
    svg_lines.append('''<g transform="translate(3780, 260)">
  <circle cx="0" cy="0" r="60" fill="#0B2545" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="0" cy="0" r="54" fill="none" stroke="#BAE6FD" stroke-width="1" stroke-dasharray="4 4"/>
  <polygon points="0,-50 -12,0 0,-10" fill="#FFFFFF"/>
  <polygon points="0,-50 12,0 0,-10" fill="#BAE6FD"/>
  <polygon points="0,50 -12,0 0,10" fill="#BAE6FD" opacity="0.6"/>
  <polygon points="0,50 12,0 0,10" fill="#FFFFFF" opacity="0.6"/>
  <line x1="-50" y1="0" x2="50" y2="0" stroke="#FFFFFF" stroke-width="1.5"/>
  <line x1="0" y1="-50" x2="0" y2="50" stroke="#FFFFFF" stroke-width="1.5"/>
  <rect x="-14" y="-76" width="28" height="22" fill="#0B2545" stroke="#FFFFFF" stroke-width="1" rx="3"/>
  <text x="0" y="-60" fill="#FFFFFF" font-size="16" font-weight="bold" text-anchor="middle">N</text>
  <text x="0" y="76" fill="#BAE6FD" font-size="14" font-weight="bold" text-anchor="middle">S</text>
  <text x="74" y="5" fill="#BAE6FD" font-size="14" font-weight="bold" text-anchor="middle">E</text>
  <text x="-74" y="5" fill="#BAE6FD" font-size="14" font-weight="bold" text-anchor="middle">W</text>
</g>''')

    # Helper function for Callout Pills (dark blue fill with cyan border)
    def callout_pill(x, y, text_lines, width=280, height=None, anchor="left", border_col="#BAE6FD", bg_col="#0B2545", font_size=15):
        line_height = font_size + 7
        if height is None:
            height = len(text_lines) * line_height + 16
        
        rx = x
        if anchor == "center":
            rx = x - width / 2
        elif anchor == "right":
            rx = x - width
            
        ry = y - height / 2
        res = [f'<g>']
        res.append(f'<rect x="{rx}" y="{ry}" width="{width}" height="{height}" fill="{bg_col}" stroke="{border_col}" stroke-width="1.2" rx="5"/>')
        for idx, raw_line in enumerate(text_lines):
            line = raw_line.replace("&", "&amp;") if "&amp;" not in raw_line else raw_line
            ty = ry + 16 + idx * line_height
            tx = rx + (width/2 if anchor=="center" else (width - 12 if anchor=="right" else 12))
            align = "middle" if anchor=="center" else ("end" if anchor=="right" else "start")
            col = "#FFFFFF" if idx == 0 else "#BAE6FD"
            weight = "bold" if idx == 0 else "normal"
            res.append(f'<text x="{tx}" y="{ty}" fill="{col}" font-size="{font_size}" font-weight="{weight}" text-anchor="{align}">{line}</text>')
        res.append('</g>')
        return "\n".join(res)

    # 3. COORDINATE MAPPING & LAYOUT CONSTANTS
    # Baseline Mainline Y: 2150 px (corresponds to Y = 100 ft)
    # Scale: 1 ft = 5 px vertically, horizontally scaled for spacious clear channels
    BASE_Y = 2150

    # Key X Coordinates:
    # PLOT B:
    # West edge: X = 450 (165 ft West of B east boundary)
    # East boundary: X = 1275 (Tee B at X = 1275, Y = 2150)
    PLOTB_WEST_X = 450
    PLOTB_EAST_X = 1275

    # ANNOTATION CORRIDOR: X = 1275 to X = 1950 (width 675 px of open Prussian Blue space)
    CORRIDOR_CENTER_X = 1620

    # PLOT A:
    # West edge: X = 2050 (195 ft West of Centerline)
    # Centerline: X = 3025 (Tee A at X = 3025, Y = 2150)
    # East edge: X = 4000 (195 ft East of Centerline)
    PLOTA_WEST_X = 2050
    PLOTA_CENTER_X = 3025
    PLOTA_EAST_X = 4000

    # BOREWELL & CORNER TEE:
    # Corner Tee: X = 3475, Y = 2150 (90 ft East of Tee A: 3025 + 450 = 3475)
    # Solar Borewell: X = 3475, Y = 2550 (80 ft South of Corner Tee: 2150 + 400 = 2550)
    CORNER_TEE_X = 3475
    CORNER_TEE_Y = 2150
    BOREWELL_X = 3475
    BOREWELL_Y = 2550

    # 4. ZONE 1: BOREWELL HEAD & 2" MAINLINE (BOTTOM RIGHT)
    # Solar array & pump house representation
    svg_lines.append(f'''<g id="ZONE_01_BOREWELL">
  <!-- Solar Array Box -->
  <rect x="{BOREWELL_X + 40}" y="{BOREWELL_Y - 80}" width="180" height="130" fill="#0B2545" stroke="#BAE6FD" stroke-width="1.5" stroke-dasharray="6 4" rx="4"/>
  <text x="{BOREWELL_X + 130}" y="{BOREWELL_Y - 50}" fill="#BAE6FD" font-size="14" font-weight="bold" text-anchor="middle">5.0 HP SOLAR</text>
  <text x="{BOREWELL_X + 130}" y="{BOREWELL_Y - 30}" fill="#BAE6FD" font-size="14" font-weight="bold" text-anchor="middle">PV ARRAY</text>
  <text x="{BOREWELL_X + 130}" y="{BOREWELL_Y - 10}" fill="#E0F2FE" font-size="12" text-anchor="middle">18-22 M³/HR</text>
  <text x="{BOREWELL_X + 130}" y="{BOREWELL_Y + 15}" fill="#E0F2FE" font-size="12" text-anchor="middle">2.5 KG/CM²</text>

  <!-- Borewell Casing Circle -->
  <circle cx="{BOREWELL_X}" cy="{BOREWELL_Y}" r="22" fill="#0B2545" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="{BOREWELL_X}" cy="{BOREWELL_Y}" r="12" fill="#FFFFFF"/>
  <circle cx="{BOREWELL_X}" cy="{BOREWELL_Y}" r="6" fill="#0B2545"/>

  <!-- South capped stub (2" End Cap) -->
  <line x1="{BOREWELL_X}" y1="{BOREWELL_Y}" x2="{BOREWELL_X}" y2="{BOREWELL_Y + 35}" stroke="#FFFFFF" stroke-width="4.5"/>
  <line x1="{BOREWELL_X - 14}" y1="{BOREWELL_Y + 35}" x2="{BOREWELL_X + 14}" y2="{BOREWELL_Y + 35}" stroke="#FFFFFF" stroke-width="4"/>
  <rect x="{BOREWELL_X - 60}" y="{BOREWELL_Y + 45}" width="120" height="24" fill="#0B2545" stroke="#BAE6FD" stroke-width="1" rx="3"/>
  <text x="{BOREWELL_X}" y="{BOREWELL_Y + 62}" fill="#BAE6FD" font-size="12" font-weight="bold" text-anchor="middle">2" END CAP</text>

  <!-- Inline Head Components (Running North 80 ft to Corner Tee) -->
  <!-- 2" Mainline pipe from Borewell to Corner Tee -->
  <line x1="{BOREWELL_X}" y1="{BOREWELL_Y}" x2="{CORNER_TEE_X}" y2="{CORNER_TEE_Y}" stroke="#FFFFFF" stroke-width="4.5"/>

  <!-- Component 1: 2" NRV (Non-Return Valve) at Y = 2450 -->
  <circle cx="{BOREWELL_X}" cy="{BOREWELL_Y - 70}" r="14" fill="#0B2545" stroke="#FFFFFF" stroke-width="2"/>
  <polygon points="{BOREWELL_X - 8},{BOREWELL_Y - 62} {BOREWELL_X + 8},{BOREWELL_Y - 62} {BOREWELL_X},{BOREWELL_Y - 78}" fill="#FFFFFF"/>

  <!-- Component 2: 2" Gate Valve at Y = 2370 -->
  <polygon points="{BOREWELL_X - 10},{BOREWELL_Y - 140} {BOREWELL_X + 10},{BOREWELL_Y - 160} {BOREWELL_X - 10},{BOREWELL_Y - 160} {BOREWELL_X + 10},{BOREWELL_Y - 140}" fill="#0B2545" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="{BOREWELL_X}" cy="{BOREWELL_Y - 150}" r="4" fill="#FFFFFF"/>

  <!-- Component 3: 2" Filter 'T' Type at Y = 2270 -->
  <circle cx="{BOREWELL_X}" cy="{BOREWELL_Y - 240}" r="18" fill="#0B2545" stroke="#FFFFFF" stroke-width="2.5"/>
  <line x1="{BOREWELL_X}" y1="{BOREWELL_Y - 240}" x2="{BOREWELL_X - 25}" y2="{BOREWELL_Y - 240}" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="{BOREWELL_X - 25}" cy="{BOREWELL_Y - 240}" r="9" fill="#E0F2FE"/>

  <!-- Corner Tee at (CORNER_TEE_X, CORNER_TEE_Y) -->
  <circle cx="{CORNER_TEE_X}" cy="{CORNER_TEE_Y}" r="12" fill="#FFFFFF"/>
  <circle cx="{CORNER_TEE_X}" cy="{CORNER_TEE_Y}" r="6" fill="#0B2545"/>
  <!-- East capped stub -->
  <line x1="{CORNER_TEE_X}" y1="{CORNER_TEE_Y}" x2="{CORNER_TEE_X + 35}" y2="{CORNER_TEE_Y}" stroke="#FFFFFF" stroke-width="4.5"/>
  <line x1="{CORNER_TEE_X + 35}" y1="{CORNER_TEE_Y - 14}" x2="{CORNER_TEE_X + 35}" y2="{CORNER_TEE_Y + 14}" stroke="#FFFFFF" stroke-width="4"/>
  <rect x="{CORNER_TEE_X + 45}" y="{CORNER_TEE_Y - 12}" width="110" height="24" fill="#0B2545" stroke="#BAE6FD" stroke-width="1" rx="3"/>
  <text x="{CORNER_TEE_X + 100}" y="{CORNER_TEE_Y + 5}" fill="#BAE6FD" font-size="12" font-weight="bold" text-anchor="middle">2" END CAP</text>

  <!-- 90 ft Mainline run West to Tee A -->
  <line x1="{CORNER_TEE_X}" y1="{CORNER_TEE_Y}" x2="{PLOTA_CENTER_X}" y2="{BASE_Y}" stroke="#FFFFFF" stroke-width="4.5"/>
</g>''')

    # Head Unit Callouts in East Margin (Clean Leader Lines)
    svg_lines.append(f'''<g>
  <!-- Leader to Filter -->
  <line x1="{BOREWELL_X - 25}" y1="{BOREWELL_Y - 240}" x2="{BOREWELL_X - 90}" y2="{BOREWELL_Y - 240}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(BOREWELL_X - 100, BOREWELL_Y - 240, ["2\" FILTER 'T' TYPE", "120-MESH DISC/SCREEN", "ITEM #11 (1 NO)"], width=230, anchor="right")}

  <!-- Leader to Gate Valve -->
  <line x1="{BOREWELL_X + 12}" y1="{BOREWELL_Y - 150}" x2="{BOREWELL_X + 240}" y2="{BOREWELL_Y - 150}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(BOREWELL_X + 250, BOREWELL_Y - 150, ["2\" GATE VALVE", "PRIMARY ISOLATION"], width=210, anchor="left")}

  <!-- Leader to NRV -->
  <line x1="{BOREWELL_X + 14}" y1="{BOREWELL_Y - 70}" x2="{BOREWELL_X + 240}" y2="{BOREWELL_Y - 70}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(BOREWELL_X + 250, BOREWELL_Y - 70, ["2\" NON-RETURN VALVE", "PREVENTS HAMMER"], width=210, anchor="left")}

  <!-- Leader to Borewell Head -->
  <line x1="{BOREWELL_X}" y1="{BOREWELL_Y}" x2="{BOREWELL_X - 90}" y2="{BOREWELL_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(BOREWELL_X - 100, BOREWELL_Y, ["SOLAR BOREWELL HEAD", "COORD: (590\', 20\')", "5 HP DC SUBMERSIBLE"], width=230, anchor="right")}

  <!-- 80 ft Dimension Callout -->
  <line x1="{BOREWELL_X + 15}" y1="{BOREWELL_Y}" x2="{BOREWELL_X + 15}" y2="{CORNER_TEE_Y}" stroke="#BAE6FD" stroke-width="1" stroke-dasharray="4 4"/>
  {callout_pill(BOREWELL_X + 20, (BOREWELL_Y + CORNER_TEE_Y)/2, ["80\'-0\" MAINLINE", "2\" (63MM) PVC CLASS 2"], width=220, anchor="left", font_size=13)}

  <!-- 90 ft Dimension Callout -->
  <line x1="{PLOTA_CENTER_X}" y1="{BASE_Y + 30}" x2="{CORNER_TEE_X}" y2="{BASE_Y + 30}" stroke="#BAE6FD" stroke-width="1" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  {callout_pill((PLOTA_CENTER_X + CORNER_TEE_X)/2, BASE_Y + 55, ["90\'-0\" 2\" PVC MAINLINE (63MM)"], width=290, anchor="center", font_size=13)}
</g>''')

    # 5. TEE A & INTER-PLOT MAINLINE (215 FT WEST TO TEE B)
    svg_lines.append(f'''<g id="TEE_A_AND_MAINLINE">
  <!-- Tee A at (PLOTA_CENTER_X, BASE_Y) -->
  <circle cx="{PLOTA_CENTER_X}" cy="{BASE_Y}" r="14" fill="#FFFFFF"/>
  <circle cx="{PLOTA_CENTER_X}" cy="{BASE_Y}" r="7" fill="#0B2545"/>

  <!-- 215 ft Mainline running West from Tee A to Tee B -->
  <line x1="{PLOTA_CENTER_X}" y1="{BASE_Y}" x2="{PLOTB_EAST_X}" y2="{BASE_Y}" stroke="#FFFFFF" stroke-width="4.5"/>

  <!-- Tee B at (PLOTB_EAST_X, BASE_Y) -->
  <circle cx="{PLOTB_EAST_X}" cy="{BASE_Y}" r="14" fill="#FFFFFF"/>
  <circle cx="{PLOTB_EAST_X}" cy="{BASE_Y}" r="7" fill="#0B2545"/>

  <!-- West capped stub at Tee B -->
  <line x1="{PLOTB_EAST_X}" y1="{BASE_Y}" x2="{PLOTB_EAST_X - 35}" y2="{BASE_Y}" stroke="#FFFFFF" stroke-width="4.5"/>
  <line x1="{PLOTB_EAST_X - 35}" y1="{BASE_Y - 14}" x2="{PLOTB_EAST_X - 35}" y2="{BASE_Y + 14}" stroke="#FFFFFF" stroke-width="4"/>
  <rect x="{PLOTB_EAST_X - 165}" y="{BASE_Y - 12}" width="120" height="24" fill="#0B2545" stroke="#BAE6FD" stroke-width="1" rx="3"/>
  <text x="{PLOTB_EAST_X - 105}" y="{BASE_Y + 5}" fill="#BAE6FD" font-size="12" font-weight="bold" text-anchor="middle">2" END CAP</text>

  <!-- Dimension line for 215 ft run -->
  <line x1="{PLOTB_EAST_X}" y1="{BASE_Y + 30}" x2="{PLOTA_CENTER_X}" y2="{BASE_Y + 30}" stroke="#BAE6FD" stroke-width="1" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  {callout_pill((PLOTB_EAST_X + PLOTA_CENTER_X)/2, BASE_Y + 65, [
      "215\'-0\" 2\" MAINLINE RUN (UNDER PLOT A & ROADWAY BUFFER)",
      "TRUE PIPE LENGTH: 215 FT | TEE A (500\', 100\') TO TEE B (285\', 100\')"
  ], width=520, anchor="center", font_size=13)}

  <!-- Tee A Callout below pipe -->
  <line x1="{PLOTA_CENTER_X}" y1="{BASE_Y}" x2="{PLOTA_CENTER_X}" y2="{BASE_Y + 110}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(PLOTA_CENTER_X, BASE_Y + 145, [
      "TEE A: PLOT A ENTRY",
      "COORD: (500\', 100\')",
      "2\" EQUAL TEE JUNCTION"
  ], width=250, anchor="center", font_size=14)}

  <!-- Tee B Callout below pipe -->
  <line x1="{PLOTB_EAST_X}" y1="{BASE_Y}" x2="{PLOTB_EAST_X}" y2="{BASE_Y + 110}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(PLOTB_EAST_X, BASE_Y + 145, [
      "TEE B: PLOT B ENTRY",
      "COORD: (285\', 100\')",
      "2\" TEE WITH WEST CAP"
  ], width=250, anchor="center", font_size=14)}
</g>''')

    # 6. PLOT B (WEST FIELD — BHAGYA, 750 PLANTS) — WITH FIXED GEOMETRY
    # CRITICAL FIXES IMPLEMENTED:
    # 1. 24 FT BARE GROUND RUN: From Tee B (Y=2150) straight North 24 ft (120 px) to Y=2030.
    #    NO PLANTS, NO ROWS below Y=2030!
    # 2. 2" MAINLINE TERMINATES AT RISER B4 (240-248 ft North):
    #    2" thick white pipe runs from Y=2150 to Y=910 (248 ft North of Tee B) and STOPS with a 2" End Cap!
    #    Above Riser B4, ONLY 1.25" subline (Cyan-White) continues 32 ft North to Y=750!
    # 3. 4 RISERS: B1 (offset 56'), B2 (offset 120'), B3 (offset 184'), B4 (offset 248').
    #    Subline coverage:
    #    - Riser B1: 56' North (Y=1870). South subline reaches 24' North (Y=2030, where plants start!). North arm reaches 88' (Y=1710).
    #    - Riser B2: 120' North (Y=1550). Covers 88' to 152' (Y=1710 to Y=1390).
    #    - Riser B3: 184' North (Y=1230). Covers 152' to 216' (Y=1390 to Y=1070).
    #    - Riser B4: 248' North (Y=910). 2" Mainline ENDS here! Covers 216' to 280' (Y=1070 to Y=750).
    # 4. 32 LATERAL ROWS: Spaced 8 ft apart (40 px), going WEST ONLY (X=1275 to X=450, 165 ft).

    PLOTB_START_Y = BASE_Y - 24 * 5  # Y = 2030 (24 ft North of Tee B)
    RISER_B1_Y = BASE_Y - 56 * 5    # Y = 1870
    RISER_B2_Y = BASE_Y - 120 * 5   # Y = 1550
    RISER_B3_Y = BASE_Y - 184 * 5   # Y = 1230
    RISER_B4_Y = BASE_Y - 248 * 5   # Y = 910  (2" Mainline ENDS here)
    PLOTB_TOP_Y = BASE_Y - 280 * 5   # Y = 750  (Top of 1.25" North subline arm)

    svg_lines.append(f'''<g id="ZONE_03_PLOT_B">
  <!-- Plot B Boundary Box (Dashed Cyan) -->
  <rect x="{PLOTB_WEST_X}" y="{PLOTB_TOP_Y - 20}" width="{PLOTB_EAST_X - PLOTB_WEST_X}" height="{PLOTB_START_Y - PLOTB_TOP_Y + 40}" fill="none" stroke="#7DD3FC" stroke-width="1.5" stroke-dasharray="8 6"/>
  <text x="{PLOTB_WEST_X + 20}" y="{PLOTB_TOP_Y - 35}" fill="#E0F2FE" font-size="20" font-weight="bold" letter-spacing="1.5">PLOT B: BHAGYA MORINGA (1 ACRE | 7ft x 8ft GRID | 750 TREES)</text>
  <text x="{PLOTB_WEST_X + 20}" y="{PLOTB_TOP_Y - 12}" fill="#BAE6FD" font-size="14">32 ROWS (WESTWARD ONLY) • 16MM PLAIN LATERALS • 24 PUNCHED TUNNING DRIPPERS/ROW (ITEM #2)</text>

  <!-- BARE GROUND 24 FT RUN (Tee B to Y=2030): NO PLANTS/ROWS -->
  <line x1="{PLOTB_EAST_X}" y1="{BASE_Y}" x2="{PLOTB_EAST_X}" y2="{PLOTB_START_Y}" stroke="#FFFFFF" stroke-width="4.5"/>
  <!-- Hatching or indicator for bare ground run -->
  <line x1="{PLOTB_EAST_X - 25}" y1="{BASE_Y - 60}" x2="{PLOTB_EAST_X + 25}" y2="{BASE_Y - 60}" stroke="#BAE6FD" stroke-width="1" stroke-dasharray="3 3"/>
  <rect x="{PLOTB_EAST_X - 220}" y="{BASE_Y - 75}" width="180" height="30" fill="#0B2545" stroke="#BAE6FD" stroke-width="1" rx="4"/>
  <text x="{PLOTB_EAST_X - 130}" y="{BASE_Y - 55}" fill="#BAE6FD" font-size="12" font-weight="bold" text-anchor="middle">24\' BARE GROUND RUN</text>
  <text x="{PLOTB_EAST_X - 130}" y="{BASE_Y - 38}" fill="#BAE6FD" font-size="11" text-anchor="middle">(NO PLANTS / NO ROWS)</text>

  <!-- 2" MAINLINE FROM Y=2030 TO RISER B4 (Y=910) - ENDS AT RISER B4 -->
  <line x1="{PLOTB_EAST_X}" y1="{PLOTB_START_Y}" x2="{PLOTB_EAST_X}" y2="{RISER_B4_Y}" stroke="#FFFFFF" stroke-width="4.5"/>

  <!-- 2" END CAP AT RISER B4 (TERMINATION OF 2" MAINLINE) -->
  <line x1="{PLOTB_EAST_X - 16}" y1="{RISER_B4_Y}" x2="{PLOTB_EAST_X + 16}" y2="{RISER_B4_Y}" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="{PLOTB_EAST_X}" cy="{RISER_B4_Y}" r="16" fill="#FFFFFF"/>
  <circle cx="{PLOTB_EAST_X}" cy="{RISER_B4_Y}" r="9" fill="#0B2545"/>

  <!-- ONLY 1.25" SUBLINE CONTINUES ABOVE RISER B4 (Y=910 to Y=750) -->
  <line x1="{PLOTB_EAST_X}" y1="{RISER_B4_Y}" x2="{PLOTB_EAST_X}" y2="{PLOTB_TOP_Y}" stroke="#E0F2FE" stroke-width="3"/>
  <!-- Top 40mm Flush Valve at Y=750 -->
  <circle cx="{PLOTB_EAST_X}" cy="{PLOTB_TOP_Y}" r="10" fill="#0B2545" stroke="#E0F2FE" stroke-width="2"/>
  <line x1="{PLOTB_EAST_X - 8}" y1="{PLOTB_TOP_Y}" x2="{PLOTB_EAST_X + 8}" y2="{PLOTB_TOP_Y}" stroke="#E0F2FE" stroke-width="2"/>

  <!-- 1.25" SUBLINE ARMS (TOTAL 256 FT FROM Y=2030 TO Y=750) -->
  <line x1="{PLOTB_EAST_X}" y1="{PLOTB_START_Y}" x2="{PLOTB_EAST_X}" y2="{PLOTB_TOP_Y}" stroke="#E0F2FE" stroke-width="3" stroke-dasharray="12 4"/>

  <!-- Bottom 40mm Flush Valve at Y=2030 (Where Plot B starts) -->
  <circle cx="{PLOTB_EAST_X}" cy="{PLOTB_START_Y}" r="10" fill="#0B2545" stroke="#E0F2FE" stroke-width="2"/>
  <line x1="{PLOTB_EAST_X - 8}" y1="{PLOTB_START_Y}" x2="{PLOTB_EAST_X + 8}" y2="{PLOTB_START_Y}" stroke="#E0F2FE" stroke-width="2"/>
''')

    # Plot B Overhead Riser Symbols at B1, B2, B3, B4
    for b_idx, (b_name, ry) in enumerate([("RISER B1", RISER_B1_Y), ("RISER B2", RISER_B2_Y), ("RISER B3", RISER_B3_Y), ("RISER B4", RISER_B4_Y)]):
        svg_lines.append(f'''  <!-- {b_name} Symbol -->
  <circle cx="{PLOTB_EAST_X}" cy="{ry}" r="18" fill="#0B2545" stroke="#FFFFFF" stroke-width="2.5"/>
  <circle cx="{PLOTB_EAST_X}" cy="{ry}" r="10" fill="#FFFFFF"/>
  <circle cx="{PLOTB_EAST_X}" cy="{ry}" r="5" fill="#0B2545"/>
  <!-- North & South Valve Stubs -->
  <circle cx="{PLOTB_EAST_X}" cy="{ry - 18}" r="5" fill="#E0F2FE"/>
  <circle cx="{PLOTB_EAST_X}" cy="{ry + 18}" r="5" fill="#E0F2FE"/>
''')

    # Plot B Intermediate Flush Valves (at arm transitions: Y=1710, 1390, 1070)
    for fy in [BASE_Y - 88*5, BASE_Y - 152*5, BASE_Y - 216*5]:
        svg_lines.append(f'''  <circle cx="{PLOTB_EAST_X}" cy="{fy}" r="9" fill="#0B2545" stroke="#E0F2FE" stroke-width="2"/>
  <line x1="{PLOTB_EAST_X - 6}" y1="{fy}" x2="{PLOTB_EAST_X + 6}" y2="{fy}" stroke="#E0F2FE" stroke-width="2"/>
''')

    # Plot B 32 Lateral Rows (Westward only: X = 1275 to 450, length 825px = 165 ft)
    # Spaced every 8 ft = 40 px, starting from Y = 2030 - 20 (Y=2010) up to Y = 770
    for r in range(32):
        row_y = (PLOTB_START_Y - 20) - r * 40
        # Lateral line
        svg_lines.append(f'  <line x1="{PLOTB_EAST_X}" y1="{row_y}" x2="{PLOTB_WEST_X}" y2="{row_y}" stroke="#7DD3FC" stroke-width="1.2" opacity="0.85"/>')
        # 40x16x1-Way Take-off collar on 1.25" subline (West barb)
        svg_lines.append(f'  <circle cx="{PLOTB_EAST_X}" cy="{row_y}" r="4" fill="#E0F2FE"/>')
        # 16mm End cap on West end
        svg_lines.append(f'  <line x1="{PLOTB_WEST_X}" y1="{row_y - 6}" x2="{PLOTB_WEST_X}" y2="{row_y + 6}" stroke="#7DD3FC" stroke-width="2"/>')
        
        # Representative drippers every 7 ft = 35 px (draw 6 representative drippers per row)
        for dx in range(PLOTB_EAST_X - 70, PLOTB_WEST_X + 70, -140):
            svg_lines.append(f'  <circle cx="{dx}" cy="{row_y}" r="2" fill="#BAE6FD" opacity="0.7"/>')

    svg_lines.append('</g>')

    # 7. PLOT A (EAST FIELD — PKM-1, 3,000 PLANTS)
    # Centerline at X = 3025.
    # 2" Mainline runs North 145 ft (725 px) from Tee A (Y=2150) to Y=1425, ending with 2" End Cap.
    # 4 Risers at 30', 60', 90', 120' North: Y = 2000, 1850, 1700, 1550.
    # Sublines: 1.5" (50mm), 15 ft (75 px) South & 15 ft (75 px) North from each riser.
    # Active subline zone: from 15 ft North (Y=2075) to 135 ft North (Y=1475) = 120 ft total.
    # 24 trenches spaced 5 ft apart (25 px), running 195 ft West (to X=2050) and 195 ft East (to X=4000).

    PLOTA_MAINLINE_END_Y = BASE_Y - 145 * 5  # Y = 1425
    RISER_A1_Y = BASE_Y - 30 * 5            # Y = 2000
    RISER_A2_Y = BASE_Y - 60 * 5            # Y = 1850
    RISER_A3_Y = BASE_Y - 90 * 5            # Y = 1700
    RISER_A4_Y = BASE_Y - 120 * 5           # Y = 1550
    PLOTA_ACTIVE_START_Y = BASE_Y - 15 * 5  # Y = 2075
    PLOTA_ACTIVE_END_Y = BASE_Y - 135 * 5   # Y = 1475

    svg_lines.append(f'''<g id="ZONE_02_PLOT_A">
  <!-- Plot A Boundary Box (Dashed Cyan) -->
  <rect x="{PLOTA_WEST_X}" y="{PLOTA_ACTIVE_END_Y - 30}" width="{PLOTA_EAST_X - PLOTA_WEST_X}" height="{PLOTA_ACTIVE_START_Y - PLOTA_ACTIVE_END_Y + 60}" fill="none" stroke="#7DD3FC" stroke-width="1.5" stroke-dasharray="8 6"/>
  <text x="{PLOTA_WEST_X + 20}" y="{PLOTA_ACTIVE_END_Y - 45}" fill="#E0F2FE" font-size="20" font-weight="bold" letter-spacing="1.5">PLOT A: PKM-1 ANNUAL MORINGA (1 ACRE | 3ft x 5ft HIGH-DENSITY | 3,000 PLANTS)</text>
  <text x="{PLOTA_WEST_X + 20}" y="{PLOTA_ACTIVE_END_Y - 22}" fill="#BAE6FD" font-size="14">24 ACTIVE TRENCHES @ 5\' SPACING • 16x4x40 INLINE DRIP LATERALS • 50x16x2-WAY TAKE-OFF COLLARS (V-CONNECTORS)</text>

  <!-- 2" CENTER MAINLINE (Tee A to Y=1425) -->
  <line x1="{PLOTA_CENTER_X}" y1="{BASE_Y}" x2="{PLOTA_CENTER_X}" y2="{PLOTA_MAINLINE_END_Y}" stroke="#FFFFFF" stroke-width="4.5"/>
  <!-- 2" End Cap at North end (Y=1425) -->
  <line x1="{PLOTA_CENTER_X - 16}" y1="{PLOTA_MAINLINE_END_Y}" x2="{PLOTA_CENTER_X + 16}" y2="{PLOTA_MAINLINE_END_Y}" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="{PLOTA_CENTER_X}" cy="{PLOTA_MAINLINE_END_Y}" r="12" fill="#FFFFFF"/>
  <circle cx="{PLOTA_CENTER_X}" cy="{PLOTA_MAINLINE_END_Y}" r="6" fill="#0B2545"/>
  <rect x="{PLOTA_CENTER_X - 80}" y="{PLOTA_MAINLINE_END_Y - 30}" width="160" height="22" fill="#0B2545" stroke="#BAE6FD" stroke-width="1" rx="3"/>
  <text x="{PLOTA_CENTER_X}" y="{PLOTA_MAINLINE_END_Y - 14}" fill="#BAE6FD" font-size="11" font-weight="bold" text-anchor="middle">2" MAINLINE END CAP</text>

  <!-- 1.5" (50mm) SUBLINES (Y=2075 to Y=1475 = 120 ft total) -->
  <line x1="{PLOTA_CENTER_X}" y1="{PLOTA_ACTIVE_START_Y}" x2="{PLOTA_CENTER_X}" y2="{PLOTA_ACTIVE_END_Y}" stroke="#E0F2FE" stroke-width="3" stroke-dasharray="10 4"/>

  <!-- Plot A Flush Valves (50mm) at Y=2075 (South end) and Y=1475 (North end) -->
  <circle cx="{PLOTA_CENTER_X}" cy="{PLOTA_ACTIVE_START_Y}" r="10" fill="#0B2545" stroke="#E0F2FE" stroke-width="2"/>
  <line x1="{PLOTA_CENTER_X - 8}" y1="{PLOTA_ACTIVE_START_Y}" x2="{PLOTA_CENTER_X + 8}" y2="{PLOTA_ACTIVE_START_Y}" stroke="#E0F2FE" stroke-width="2"/>
  <circle cx="{PLOTA_CENTER_X}" cy="{PLOTA_ACTIVE_END_Y}" r="10" fill="#0B2545" stroke="#E0F2FE" stroke-width="2"/>
  <line x1="{PLOTA_CENTER_X - 8}" y1="{PLOTA_ACTIVE_END_Y}" x2="{PLOTA_CENTER_X + 8}" y2="{PLOTA_ACTIVE_END_Y}" stroke="#E0F2FE" stroke-width="2"/>
''')

    # Plot A 4 Overhead Riser Stations (A1-A4)
    for a_idx, (a_name, ry) in enumerate([("RISER A1", RISER_A1_Y), ("RISER A2", RISER_A2_Y), ("RISER A3", RISER_A3_Y), ("RISER A4", RISER_A4_Y)]):
        svg_lines.append(f'''  <!-- {a_name} Symbol -->
  <circle cx="{PLOTA_CENTER_X}" cy="{ry}" r="18" fill="#0B2545" stroke="#FFFFFF" stroke-width="2.5"/>
  <circle cx="{PLOTA_CENTER_X}" cy="{ry}" r="10" fill="#FFFFFF"/>
  <circle cx="{PLOTA_CENTER_X}" cy="{ry}" r="5" fill="#0B2545"/>
  <!-- North & South 50mm Valve Stubs -->
  <circle cx="{PLOTA_CENTER_X}" cy="{ry - 18}" r="6" fill="#E0F2FE"/>
  <circle cx="{PLOTA_CENTER_X}" cy="{ry + 18}" r="6" fill="#E0F2FE"/>
''')

    # Plot A Intermediate Flush Valves (at arm ends: Y=1925, 1775, 1625)
    for fy in [BASE_Y - 45*5, BASE_Y - 75*5, BASE_Y - 105*5]:
        svg_lines.append(f'''  <circle cx="{PLOTA_CENTER_X}" cy="{fy}" r="9" fill="#0B2545" stroke="#E0F2FE" stroke-width="2"/>
  <line x1="{PLOTA_CENTER_X - 6}" y1="{fy}" x2="{PLOTA_CENTER_X + 6}" y2="{fy}" stroke="#E0F2FE" stroke-width="2"/>
''')

    # Plot A 24 Inline Trenches (Spaced every 5 ft = 25 px)
    # Covering Y=2075 + 12.5 px to Y=1475 - 12.5 px
    for t in range(24):
        trench_y = (PLOTA_ACTIVE_START_Y - 12.5) - t * 25
        # Full East-West trench lateral line (X = 2050 to 4000, 1950 px = 390 ft)
        svg_lines.append(f'  <line x1="{PLOTA_WEST_X}" y1="{trench_y}" x2="{PLOTA_EAST_X}" y2="{trench_y}" stroke="#7DD3FC" stroke-width="1.2" opacity="0.85"/>')
        # 50x16x2-Way Collar (V-connector) at Centerline
        svg_lines.append(f'  <circle cx="{PLOTA_CENTER_X}" cy="{trench_y}" r="4.5" fill="#E0F2FE"/>')
        # 16mm End caps at West and East extremities
        svg_lines.append(f'  <line x1="{PLOTA_WEST_X}" y1="{trench_y - 6}" x2="{PLOTA_WEST_X}" y2="{trench_y + 6}" stroke="#7DD3FC" stroke-width="2"/>')
        svg_lines.append(f'  <line x1="{PLOTA_EAST_X}" y1="{trench_y - 6}" x2="{PLOTA_EAST_X}" y2="{trench_y + 6}" stroke="#7DD3FC" stroke-width="2"/>')

    svg_lines.append('</g>')

    # 8. CENTRAL VERTICAL ANNOTATION CHANNEL (BETWEEN PLOT B AND PLOT A)
    # ZERO-OVERLAP RULE: All Riser and Flush Valve labels for Plot B sit here, connected by horizontal leader lines!
    svg_lines.append(f'''<g id="ANNOTATION_CORRIDOR">
  <!-- Central Corridor Divider / Grid Guideline -->
  <line x1="{CORRIDOR_CENTER_X}" y1="450" x2="{CORRIDOR_CENTER_X}" y2="2100" stroke="#BAE6FD" stroke-width="1" stroke-dasharray="8 8" opacity="0.4"/>
  <rect x="{CORRIDOR_CENTER_X - 180}" y="420" width="360" height="26" fill="#0B2545" stroke="#BAE6FD" stroke-width="1" rx="4"/>
  <text x="{CORRIDOR_CENTER_X}" y="438" fill="#BAE6FD" font-size="12" font-weight="bold" text-anchor="middle">CENTRAL ANNOTATION CHANNEL (ZERO-OVERLAP)</text>

  <!-- CALLOUT 1: RISER B4 & 2" MAINLINE TERMINATION (AT Y=910) -->
  <line x1="{PLOTB_EAST_X}" y1="{RISER_B4_Y}" x2="{CORRIDOR_CENTER_X - 160}" y2="{RISER_B4_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(CORRIDOR_CENTER_X - 150, RISER_B4_Y, [
      "RISER B4 (OFFSET: 248\'-0\" NORTH)",
      "2\" MAINLINE TERMINATES HERE (2\" END CAP)",
      "OVERHEAD 2\" TEE + 2x 40MM BALL VALVES",
      "ONLY 1.25\" SUBLINE CONTINUES 32 FT NORTH"
  ], width=360, anchor="left", font_size=12)}

  <!-- CALLOUT 2: TOP 40MM FLUSH VALVE (AT Y=750) -->
  <line x1="{PLOTB_EAST_X}" y1="{PLOTB_TOP_Y}" x2="{CORRIDOR_CENTER_X - 160}" y2="{PLOTB_TOP_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(CORRIDOR_CENTER_X - 150, PLOTB_TOP_Y, [
      "40MM FLUSH VALVE (NORTH TERMINAL)",
      "ELEVATION: -2\'-0\" IN SURFACE SLEEVE",
      "COVERS TOP 4 ROWS (ROWS #29-32)"
  ], width=320, anchor="left", font_size=12)}

  <!-- CALLOUT 3: RISER B3 (AT Y=1230) -->
  <line x1="{PLOTB_EAST_X}" y1="{RISER_B3_Y}" x2="{CORRIDOR_CENTER_X - 160}" y2="{RISER_B3_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(CORRIDOR_CENTER_X - 150, RISER_B3_Y, [
      "RISER B3 (OFFSET: 184\'-0\" NORTH)",
      "4FT DOUBLE-TEE + 2x 40MM BALL VALVES",
      "1.25\" SUBLINES: 32\' SOUTH & 32\' NORTH",
      "FEEDS 8 ROWS (ROWS #17-24 | 192 TREES)"
  ], width=350, anchor="left", font_size=12)}

  <!-- CALLOUT 4: RISER B2 (AT Y=1550) -->
  <line x1="{PLOTB_EAST_X}" y1="{RISER_B2_Y}" x2="{CORRIDOR_CENTER_X - 160}" y2="{RISER_B2_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(CORRIDOR_CENTER_X - 150, RISER_B2_Y, [
      "RISER B2 (OFFSET: 120\'-0\" NORTH)",
      "4FT DOUBLE-TEE + 2x 40MM BALL VALVES",
      "1.25\" SUBLINES: 32\' SOUTH & 32\' NORTH",
      "FEEDS 8 ROWS (ROWS #9-16 | 192 TREES)"
  ], width=350, anchor="left", font_size=12)}

  <!-- CALLOUT 5: RISER B1 (AT Y=1870) -->
  <line x1="{PLOTB_EAST_X}" y1="{RISER_B1_Y}" x2="{CORRIDOR_CENTER_X - 160}" y2="{RISER_B1_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(CORRIDOR_CENTER_X - 150, RISER_B1_Y, [
      "RISER B1 (OFFSET: 56\'-0\" NORTH)",
      "4FT DOUBLE-TEE + 2x 40MM BALL VALVES",
      "SOUTH ARM EXTENDS 32\' TO PLOT B START (24\')",
      "FEEDS 8 ROWS (ROWS #1-8 | 192 TREES)"
  ], width=360, anchor="left", font_size=12)}

  <!-- CALLOUT 6: PLOT B START & BOTTOM 40MM FLUSH VALVE (AT Y=2030) -->
  <line x1="{PLOTB_EAST_X}" y1="{PLOTB_START_Y}" x2="{CORRIDOR_CENTER_X - 160}" y2="{PLOTB_START_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(CORRIDOR_CENTER_X - 150, PLOTB_START_Y, [
      "PLOT B START BOUNDARY (24\'-0\" FROM TEE B)",
      "40MM FLUSH VALVE (SOUTH ARM TERMINAL)",
      "ROW #1 STARTS HERE (NO ROWS BELOW THIS LINE)"
  ], width=360, anchor="left", font_size=12)}
</g>''')

    # 9. PLOT A CALLOUTS (IN PLOT A OPEN MARGINS & RIGHT FLANK)
    svg_lines.append(f'''<g id="PLOTA_CALLOUTS">
  <!-- RISER A4 CALLOUT (AT Y=1550) - LEADER TO RIGHT -->
  <line x1="{PLOTA_CENTER_X}" y1="{RISER_A4_Y}" x2="{PLOTA_EAST_X + 60}" y2="{RISER_A4_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(PLOTA_EAST_X + 70, RISER_A4_Y, [
      "RISER A4 (OFFSET: 120\'-0\" NORTH)",
      "OVERHEAD 2\" TEE + 2x 50MM VALVES",
      "1.5\" SUBLINES: 15\' SOUTH & 15\' NORTH",
      "FEEDS 6 TRENCHES (750 PKM-1 PLANTS)"
  ], width=330, anchor="left", font_size=12)}

  <!-- RISER A3 CALLOUT (AT Y=1700) -->
  <line x1="{PLOTA_CENTER_X}" y1="{RISER_A3_Y}" x2="{PLOTA_EAST_X + 60}" y2="{RISER_A3_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(PLOTA_EAST_X + 70, RISER_A3_Y, [
      "RISER A3 (OFFSET: 90\'-0\" NORTH)",
      "OVERHEAD 2\" TEE + 2x 50MM VALVES",
      "1.5\" SUBLINES: 15\' SOUTH & 15\' NORTH",
      "FEEDS 6 TRENCHES (750 PKM-1 PLANTS)"
  ], width=330, anchor="left", font_size=12)}

  <!-- RISER A2 CALLOUT (AT Y=1850) -->
  <line x1="{PLOTA_CENTER_X}" y1="{RISER_A2_Y}" x2="{PLOTA_EAST_X + 60}" y2="{RISER_A2_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(PLOTA_EAST_X + 70, RISER_A2_Y, [
      "RISER A2 (OFFSET: 60\'-0\" NORTH)",
      "OVERHEAD 2\" TEE + 2x 50MM VALVES",
      "1.5\" SUBLINES: 15\' SOUTH & 15\' NORTH",
      "FEEDS 6 TRENCHES (750 PKM-1 PLANTS)"
  ], width=330, anchor="left", font_size=12)}

  <!-- RISER A1 CALLOUT (AT Y=2000) -->
  <line x1="{PLOTA_CENTER_X}" y1="{RISER_A1_Y}" x2="{PLOTA_EAST_X + 60}" y2="{RISER_A1_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(PLOTA_EAST_X + 70, RISER_A1_Y, [
      "RISER A1 (OFFSET: 30\'-0\" NORTH)",
      "OVERHEAD 2\" TEE + 2x 50MM VALVES",
      "1.5\" SUBLINES: 15\' SOUTH & 15\' NORTH",
      "FEEDS 6 TRENCHES (750 PKM-1 PLANTS)"
  ], width=330, anchor="left", font_size=12)}

  <!-- PLOT A LATERAL CALLOUT AT TOP-RIGHT -->
  <line x1="{PLOTA_EAST_X}" y1="{PLOTA_ACTIVE_END_Y + 40}" x2="{PLOTA_EAST_X + 60}" y2="{PLOTA_ACTIVE_END_Y + 40}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {callout_pill(PLOTA_EAST_X + 70, PLOTA_ACTIVE_END_Y + 40, [
      "16x4x40 INLINE LATERALS",
      "390 FT TOTAL TRENCH RUN",
      "195 FT WEST + 195 FT EAST",
      "16MM ENDCAPS ON BOTH ENDS"
  ], width=290, anchor="left", font_size=12)}
</g>''')

    # 10. OVERALL DIMENSIONS & LINE LABELS
    svg_lines.append(f'''<g id="OVERALL_DIMENSIONS">
  <!-- Plot B Width: 165'-0" West -->
  <line x1="{PLOTB_WEST_X}" y1="{PLOTB_TOP_Y - 70}" x2="{PLOTB_EAST_X}" y2="{PLOTB_TOP_Y - 70}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  {callout_pill((PLOTB_WEST_X + PLOTB_EAST_X)/2, PLOTB_TOP_Y - 70, ["165\'-0\" (PLOT B WIDTH)"], width=220, anchor="center", font_size=13)}

  <!-- Plot B Height: 256'-0" Active Height -->
  <line x1="{PLOTB_WEST_X - 40}" y1="{PLOTB_TOP_Y}" x2="{PLOTB_WEST_X - 40}" y2="{PLOTB_START_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  {callout_pill(PLOTB_WEST_X - 50, (PLOTB_TOP_Y + PLOTB_START_Y)/2, [
      "256\'-0\" ACTIVE HEIGHT",
      "32 ROWS @ 8\'-0\" SPACING"
  ], width=230, anchor="right", font_size=13)}

  <!-- Plot A Width: 390'-0" Total -->
  <line x1="{PLOTA_WEST_X}" y1="{PLOTA_ACTIVE_END_Y - 70}" x2="{PLOTA_EAST_X}" y2="{PLOTA_ACTIVE_END_Y - 70}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  {callout_pill(PLOTA_CENTER_X, PLOTA_ACTIVE_END_Y - 70, ["390\'-0\" (PLOT A OVERALL TRENCH WIDTH: 195\' W + 195\' E)"], width=460, anchor="center", font_size=13)}

  <!-- Plot A Mainline Height: 145'-0" -->
  <line x1="{PLOTA_WEST_X - 40}" y1="{PLOTA_MAINLINE_END_Y}" x2="{PLOTA_WEST_X - 40}" y2="{BASE_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  {callout_pill(PLOTA_WEST_X - 50, (PLOTA_MAINLINE_END_Y + BASE_Y)/2, [
      "145\'-0\" CENTER MAINLINE",
      "24 TRENCHES @ 5\' SPACING",
      "120 FT ACTIVE SUBLINE"
  ], width=250, anchor="right", font_size=13)}
</g>''')

    # 11. FORMAL CLASSIC ARCHITECTURAL TITLE BLOCK (BOTTOM RIGHT)
    TB_X = 2850
    TB_Y = 2270
    TB_W = 1200
    TB_H = 400

    svg_lines.append(f'''<g id="ARCHITECTURAL_TITLE_BLOCK">
  <!-- Title Block Frame -->
  <rect x="{TB_X}" y="{TB_Y}" width="{TB_W}" height="{TB_H}" fill="#0B2545" stroke="#FFFFFF" stroke-width="3"/>
  <rect x="{TB_X + 6}" y="{TB_Y + 6}" width="{TB_W - 12}" height="{TB_H - 12}" fill="none" stroke="#BAE6FD" stroke-width="1"/>

  <!-- Horizontal Dividers -->
  <line x1="{TB_X}" y1="{TB_Y + 90}" x2="{TB_X + TB_W}" y2="{TB_Y + 90}" stroke="#FFFFFF" stroke-width="2"/>
  <line x1="{TB_X}" y1="{TB_Y + 180}" x2="{TB_X + TB_W}" y2="{TB_Y + 180}" stroke="#FFFFFF" stroke-width="2"/>
  <line x1="{TB_X}" y1="{TB_Y + 280}" x2="{TB_X + TB_W}" y2="{TB_Y + 280}" stroke="#FFFFFF" stroke-width="1.5"/>

  <!-- Vertical Dividers in Rows 2 & 3 -->
  <line x1="{TB_X + 420}" y1="{TB_Y + 90}" x2="{TB_X + 420}" y2="{TB_Y + 280}" stroke="#FFFFFF" stroke-width="1.5"/>
  <line x1="{TB_X + 800}" y1="{TB_Y + 90}" x2="{TB_X + 800}" y2="{TB_Y + 280}" stroke="#FFFFFF" stroke-width="1.5"/>
  <line x1="{TB_X + 300}" y1="{TB_Y + 280}" x2="{TB_X + 300}" y2="{TB_Y + TB_H}" stroke="#FFFFFF" stroke-width="1.5"/>
  <line x1="{TB_X + 600}" y1="{TB_Y + 280}" x2="{TB_X + 600}" y2="{TB_Y + TB_H}" stroke="#FFFFFF" stroke-width="1.5"/>
  <line x1="{TB_X + 900}" y1="{TB_Y + 280}" x2="{TB_X + 900}" y2="{TB_Y + TB_H}" stroke="#FFFFFF" stroke-width="1.5"/>

  <!-- Section 1: Project Title -->
  <text x="{TB_X + 25}" y="{TB_Y + 40}" fill="#BAE6FD" font-size="14" letter-spacing="2">PROJECT &amp; LOCATION:</text>
  <text x="{TB_X + 25}" y="{TB_Y + 70}" fill="#FFFFFF" font-size="24" font-weight="bold" letter-spacing="2">2-ACRE MORINGA COMMERCIAL ORCHARD DRIP SYSTEM</text>

  <!-- Section 2: Drawing Title & Zone Description -->
  <text x="{TB_X + 25}" y="{TB_Y + 120}" fill="#BAE6FD" font-size="13">DRAWING TITLE:</text>
  <text x="{TB_X + 25}" y="{TB_Y + 150}" fill="#FFFFFF" font-size="18" font-weight="bold">MASTER FIELD BLUEPRINT</text>

  <text x="{TB_X + 440}" y="{TB_Y + 120}" fill="#BAE6FD" font-size="13">ZONE BREAKDOWN:</text>
  <text x="{TB_X + 440}" y="{TB_Y + 145}" fill="#FFFFFF" font-size="14" font-weight="bold">ZONE 1: 5HP SOLAR BOREWELL (2" MAINLINE)</text>
  <text x="{TB_X + 440}" y="{TB_Y + 168}" fill="#E0F2FE" font-size="13">ZONE 2: PLOT A (PKM-1, 24 TRENCHES, 3000P)</text>

  <text x="{TB_X + 820}" y="{TB_Y + 120}" fill="#BAE6FD" font-size="13">ZONE 3 (PLOT B SPEC):</text>
  <text x="{TB_X + 820}" y="{TB_Y + 145}" fill="#FFFFFF" font-size="14" font-weight="bold">BHAGYA (7X8 FT, 32 ROWS, 750P)</text>
  <text x="{TB_X + 820}" y="{TB_Y + 168}" fill="#E0F2FE" font-size="13">MAINLINE TERMINATES AT RISER B4</text>

  <!-- Section 3: Engineering Standards & Notes -->
  <text x="{TB_X + 25}" y="{TB_Y + 210}" fill="#BAE6FD" font-size="13">HYDRAULIC CRITERIA:</text>
  <text x="{TB_X + 25}" y="{TB_Y + 235}" fill="#FFFFFF" font-size="14" font-weight="bold">DESIGN VELOCITY: &lt; 1.5 M/S</text>
  <text x="{TB_X + 25}" y="{TB_Y + 258}" fill="#E0F2FE" font-size="13">HEAD LOSS: &lt; 2.0 M / 100M</text>

  <text x="{TB_X + 440}" y="{TB_Y + 210}" fill="#BAE6FD" font-size="13">FITTINGS SCHEDULE:</text>
  <text x="{TB_X + 440}" y="{TB_Y + 235}" fill="#FFFFFF" font-size="14" font-weight="bold">16x PLAIN BALL VALVES</text>
  <text x="{TB_X + 440}" y="{TB_Y + 258}" fill="#E0F2FE" font-size="13">16x FLUSH VALVES (SURFACE)</text>

  <text x="{TB_X + 820}" y="{TB_Y + 210}" fill="#BAE6FD" font-size="13">EMITTER SPECIFICATION:</text>
  <text x="{TB_X + 820}" y="{TB_Y + 235}" fill="#FFFFFF" font-size="14" font-weight="bold">PLOT A: 4 LPH INLINE @ 40CM</text>
  <text x="{TB_X + 820}" y="{TB_Y + 258}" fill="#E0F2FE" font-size="13">PLOT B: TUNNING DRIPPER @ 7FT</text>

  <!-- Section 4: Metadata Cells -->
  <text x="{TB_X + 25}" y="{TB_Y + 310}" fill="#BAE6FD" font-size="12">SCALE:</text>
  <text x="{TB_X + 25}" y="{TB_Y + 350}" fill="#FFFFFF" font-size="18" font-weight="bold">1 FT = 5 PX</text>
  <text x="{TB_X + 25}" y="{TB_Y + 375}" fill="#BAE6FD" font-size="11">(1:60 ON A0 / ARCH E)</text>

  <text x="{TB_X + 320}" y="{TB_Y + 310}" fill="#BAE6FD" font-size="12">DATE / STATUS:</text>
  <text x="{TB_X + 320}" y="{TB_Y + 350}" fill="#FFFFFF" font-size="16" font-weight="bold">OCTOBER 2026</text>
  <text x="{TB_X + 320}" y="{TB_Y + 375}" fill="#E0F2FE" font-size="12">APPROVED FOR FIELD</text>

  <text x="{TB_X + 620}" y="{TB_Y + 310}" fill="#BAE6FD" font-size="12">CAD STANDARD:</text>
  <text x="{TB_X + 620}" y="{TB_Y + 350}" fill="#FFFFFF" font-size="16" font-weight="bold">IS 12786 / 4985</text>
  <text x="{TB_X + 620}" y="{TB_Y + 375}" fill="#BAE6FD" font-size="11">CLASSIC BLUEPRINT</text>

  <text x="{TB_X + 920}" y="{TB_Y + 310}" fill="#BAE6FD" font-size="12">SHEET NUMBER:</text>
  <text x="{TB_X + 920}" y="{TB_Y + 355}" fill="#FFFFFF" font-size="28" font-weight="bold">SHEET 1 OF 2</text>
</g>''')

    # Close SVG
    svg_lines.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Sheet 1 SVG created: {output_path} ({len(svg_lines)} lines)")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "CAD_Master_Blueprint.svg"
    build_sheet1_svg(out_file)
