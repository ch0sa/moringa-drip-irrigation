import os
import sys

def build_sheet1_svg(output_path):
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4200 2800" width="4200" height="2800" style="background:#0B2545; font-family:\'Courier New\', Courier, monospace;">')
    
    # 1. DEFS
    svg.append('''<defs>
  <pattern id="grid10" width="50" height="50" patternUnits="userSpaceOnUse">
    <path d="M 50 0 L 0 0 0 50" fill="none" stroke="rgba(255, 255, 255, 0.07)" stroke-width="1"/>
  </pattern>
  <pattern id="grid50" width="250" height="250" patternUnits="userSpaceOnUse">
    <rect width="250" height="250" fill="url(#grid10)" />
    <path d="M 250 0 L 0 0 0 250" fill="none" stroke="rgba(255, 255, 255, 0.16)" stroke-width="1.5"/>
  </pattern>
  <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#BAE6FD" />
  </marker>
  <marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6">
    <circle cx="5" cy="5" r="3" fill="#BAE6FD" stroke="#0B2545" stroke-width="1"/>
  </marker>
</defs>''')

    # Grid background
    svg.append('<rect width="4200" height="2800" fill="#0B2545"/>')
    svg.append('<rect width="4200" height="2800" fill="url(#grid50)"/>')

    # Borders
    svg.append('<rect x="120" y="80" width="3960" height="2640" fill="none" stroke="#FFFFFF" stroke-width="5"/>')
    svg.append('<rect x="145" y="105" width="3910" height="2590" fill="none" stroke="#FFFFFF" stroke-width="2"/>')

    # 1-Line Compact Pill Tag Helper
    def pill(x, y, text, width=None, anchor="left", font_size=13, stroke="#BAE6FD"):
        safe_text = text.replace("&", "&amp;")
        if width is None:
            width = len(text) * (font_size * 0.62) + 24
        h = 28
        rx = x
        if anchor == "center":
            rx = x - width / 2
        elif anchor == "right":
            rx = x - width
        ry = y - h / 2
        tx = rx + (width/2 if anchor == "center" else (width - 10 if anchor == "right" else 10))
        ta = "middle" if anchor == "center" else ("end" if anchor == "right" else "start")
        return f'<g><rect x="{rx:.1f}" y="{ry:.1f}" width="{width:.1f}" height="{h}" fill="#0B2545" stroke="{stroke}" stroke-width="1.2" rx="4"/><text x="{tx:.1f}" y="{ry + 19:.1f}" fill="#FFFFFF" font-size="{font_size}" font-weight="bold" text-anchor="{ta}">{safe_text}</text></g>'

    # 2. HEADER & TOP LEGEND BOX
    svg.append('''<g transform="translate(180, 160)">
  <text x="0" y="0" fill="#FFFFFF" font-size="32" font-weight="bold" letter-spacing="2">2-ACRE MORINGA IRRIGATION — MASTER BLUEPRINT</text>
  <text x="0" y="28" fill="#BAE6FD" font-size="16" letter-spacing="1">SHEET 1 OF 2 : TOP-DOWN MASTER FIELD BLUEPRINT</text>
</g>''')

    # Single Small Top Legend Box (Explaining one riser station for Plot A & Plot B)
    svg.append(f'''<g transform="translate(1550, 125)">
  <rect x="0" y="0" width="1950" height="66" fill="#0B2545" stroke="#BAE6FD" stroke-width="1.2" rx="5"/>
  <text x="16" y="26" fill="#BAE6FD" font-size="13" font-weight="bold">PLOT A RISER = 4\' 2" RISER + 2x 50MM BALL VALVES + 15\' N/S 1.5" SUBLINES + 2x 50MM FLUSH VALVES</text>
  <text x="16" y="50" fill="#BAE6FD" font-size="13" font-weight="bold">PLOT B RISER = 4\' 2" RISER + 2x 40MM BALL VALVES + 32\' N/S 1.25" SUBLINES + 2x 40MM FLUSH VALVES</text>
</g>''')

    # North Arrow
    svg.append('''<g transform="translate(3920, 160)">
  <circle cx="0" cy="0" r="32" fill="#0B2545" stroke="#FFFFFF" stroke-width="2"/>
  <polygon points="0,-26 -8,0 0,-6" fill="#FFFFFF"/>
  <polygon points="0,-26 8,0 0,-6" fill="#BAE6FD"/>
  <polygon points="0,26 -8,0 0,6" fill="#BAE6FD" opacity="0.6"/>
  <polygon points="0,26 8,0 0,6" fill="#FFFFFF" opacity="0.6"/>
  <text x="0" y="-36" fill="#FFFFFF" font-size="14" font-weight="bold" text-anchor="middle">N</text>
</g>''')

    # 3. COORDINATE DEFINITIONS (SHIFTED -450px LEFT, VERTICALLY OPTIMIZED)
    BASE_Y = 2100

    # Plot B
    PLOTB_WEST_X = 360
    PLOTB_EAST_X = 1185   # 825 px = 165 ft @ 5px/ft
    CORRIDOR_X = 1410     # Annotation channel center

    # Plot A
    PLOTA_WEST_X = 1635
    PLOTA_CENTER_X = 2610 # 975 px from West edge = 195 ft @ 5px/ft
    PLOTA_EAST_X = 3585   # 975 px from Centerline = 195 ft @ 5px/ft

    # Borewell & Corner Tee (90 ft East of Tee A: 2610 + 450 = 3060)
    CORNER_TEE_X = 3060
    CORNER_TEE_Y = 2100
    BOREWELL_X = 3060
    BOREWELL_Y = 2500     # 80 ft South: 2100 + 400 = 2500 (150px buffer above footer bar)

    # 4. ZONE 1: BOREWELL HEAD & MAINLINE
    svg.append(f'''<g id="BOREWELL_HEAD">
  <!-- Borewell Head Unit at (3060, 2500) -->
  <circle cx="{BOREWELL_X}" cy="{BOREWELL_Y}" r="16" fill="#0B2545" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="{BOREWELL_X}" cy="{BOREWELL_Y}" r="7" fill="#FFFFFF"/>
  <line x1="{BOREWELL_X}" y1="{BOREWELL_Y}" x2="{BOREWELL_X}" y2="{BOREWELL_Y + 25}" stroke="#FFFFFF" stroke-width="4.5"/>
  <line x1="{BOREWELL_X - 10}" y1="{BOREWELL_Y + 25}" x2="{BOREWELL_X + 10}" y2="{BOREWELL_Y + 25}" stroke="#FFFFFF" stroke-width="3.5"/>
  {pill(BOREWELL_X + 35, BOREWELL_Y, 'SOLAR BOREWELL')}

  <!-- 80 ft 2" Mainline North to Corner Tee -->
  <line x1="{BOREWELL_X}" y1="{BOREWELL_Y}" x2="{CORNER_TEE_X}" y2="{CORNER_TEE_Y}" stroke="#FFFFFF" stroke-width="4.5"/>
  {pill(BOREWELL_X + 25, (BOREWELL_Y + CORNER_TEE_Y)/2, '80\' (2")')}

  <!-- Inline NRV, Gate Valve, 2" Filter T -->
  <circle cx="{BOREWELL_X}" cy="{BOREWELL_Y - 80}" r="9" fill="#FFFFFF"/>
  {pill(BOREWELL_X + 25, BOREWELL_Y - 80, '2" NRV')}

  <polygon points="{BOREWELL_X - 7},{BOREWELL_Y - 160} {BOREWELL_X + 7},{BOREWELL_Y - 180} {BOREWELL_X - 7},{BOREWELL_Y - 180} {BOREWELL_X + 7},{BOREWELL_Y - 160}" fill="#FFFFFF"/>
  {pill(BOREWELL_X + 25, BOREWELL_Y - 170, '2" GATE VALVE')}

  <circle cx="{BOREWELL_X}" cy="{BOREWELL_Y - 260}" r="12" fill="#0B2545" stroke="#FFFFFF" stroke-width="2.5"/>
  {pill(BOREWELL_X + 25, BOREWELL_Y - 260, '2" FILTER \'T\'')}

  <!-- Corner Tee at (3060, 2100) -->
  <circle cx="{CORNER_TEE_X}" cy="{CORNER_TEE_Y}" r="10" fill="#FFFFFF"/>
  <!-- East capped stub -->
  <line x1="{CORNER_TEE_X}" y1="{CORNER_TEE_Y}" x2="{CORNER_TEE_X + 25}" y2="{CORNER_TEE_Y}" stroke="#FFFFFF" stroke-width="4.5"/>
  <line x1="{CORNER_TEE_X + 25}" y1="{CORNER_TEE_Y - 10}" x2="{CORNER_TEE_X + 25}" y2="{CORNER_TEE_Y + 10}" stroke="#FFFFFF" stroke-width="3.5"/>
  {pill(CORNER_TEE_X + 35, CORNER_TEE_Y, 'CORNER TEE')}

  <!-- 90 ft Mainline West to Tee A -->
  <line x1="{CORNER_TEE_X}" y1="{CORNER_TEE_Y}" x2="{PLOTA_CENTER_X}" y2="{BASE_Y}" stroke="#FFFFFF" stroke-width="4.5"/>
  {pill((CORNER_TEE_X + PLOTA_CENTER_X)/2, BASE_Y - 22, '90\' (2")', anchor="center")}
</g>''')

    # 5. TEE A & INTER-PLOT MAINLINE (215' WEST TO TEE B)
    svg.append(f'''<g id="TEE_A_AND_TEE_B">
  <!-- Tee A at (PLOTA_CENTER_X, BASE_Y) -->
  <circle cx="{PLOTA_CENTER_X}" cy="{BASE_Y}" r="12" fill="#FFFFFF"/>
  <circle cx="{PLOTA_CENTER_X}" cy="{BASE_Y}" r="5" fill="#0B2545"/>
  {pill(PLOTA_CENTER_X, BASE_Y + 30, 'TEE A', anchor="center")}

  <!-- 215 ft Mainline West to Tee B -->
  <line x1="{PLOTA_CENTER_X}" y1="{BASE_Y}" x2="{PLOTB_EAST_X}" y2="{BASE_Y}" stroke="#FFFFFF" stroke-width="4.5"/>
  {pill((PLOTA_CENTER_X + PLOTB_EAST_X)/2, BASE_Y + 30, '215\' (2")', anchor="center")}

  <!-- Tee B at (PLOTB_EAST_X, BASE_Y) -->
  <circle cx="{PLOTB_EAST_X}" cy="{BASE_Y}" r="12" fill="#FFFFFF"/>
  <circle cx="{PLOTB_EAST_X}" cy="{BASE_Y}" r="5" fill="#0B2545"/>
  <!-- West capped stub -->
  <line x1="{PLOTB_EAST_X}" y1="{BASE_Y}" x2="{PLOTB_EAST_X - 25}" y2="{BASE_Y}" stroke="#FFFFFF" stroke-width="4.5"/>
  <line x1="{PLOTB_EAST_X - 25}" y1="{BASE_Y - 10}" x2="{PLOTB_EAST_X - 25}" y2="{BASE_Y + 10}" stroke="#FFFFFF" stroke-width="3.5"/>
  {pill(PLOTB_EAST_X, BASE_Y + 30, 'TEE B', anchor="center")}
</g>''')

    # 6. PLOT B (BHAGYA, 750 PLANTS, 32 ROWS) — FIXED GEOMETRY
    PLOTB_START_Y = BASE_Y - 24 * 5     # Y = 1980
    RISER_B4_Y = BASE_Y - 240 * 5       # Y = 900 (Exact 240' North of Tee B)
    PLOTB_TOP_Y = RISER_B4_Y - 32 * 5   # Y = 740 (Top 40mm Flush Valve)

    RISER_B1_Y = PLOTB_START_Y - 54 * 5 # Y = 1710
    RISER_B2_Y = RISER_B1_Y - 54 * 5    # Y = 1440
    RISER_B3_Y = RISER_B2_Y - 54 * 5    # Y = 1170

    svg.append(f'''<g id="PLOT_B">
  <!-- Boundary Box -->
  <rect x="{PLOTB_WEST_X}" y="{PLOTB_TOP_Y - 15}" width="{PLOTB_EAST_X - PLOTB_WEST_X}" height="{PLOTB_START_Y - PLOTB_TOP_Y + 30}" fill="none" stroke="#7DD3FC" stroke-width="1.5" stroke-dasharray="8 6"/>
  <text x="{PLOTB_WEST_X + 15}" y="{PLOTB_TOP_Y - 30}" fill="#FFFFFF" font-size="18" font-weight="bold">PLOT B: BHAGYA (7x8\', 750 PLANTS)</text>

  <!-- Width Dimension: 165' -->
  <line x1="{PLOTB_WEST_X}" y1="{PLOTB_TOP_Y - 55}" x2="{PLOTB_EAST_X}" y2="{PLOTB_TOP_Y - 55}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  {pill((PLOTB_WEST_X + PLOTB_EAST_X)/2, PLOTB_TOP_Y - 55, '165\'', anchor="center")}

  <!-- 24 FT BARE 2" MAINLINE (NO ROWS): from Tee B (Y=2100) to Y=1980 -->
  <line x1="{PLOTB_EAST_X}" y1="{BASE_Y}" x2="{PLOTB_EAST_X}" y2="{PLOTB_START_Y}" stroke="#FFFFFF" stroke-width="4.5"/>
  {pill(PLOTB_EAST_X - 20, (BASE_Y + PLOTB_START_Y)/2, '24\' BARE (NO ROWS)', anchor="right", font_size=11)}

  <!-- 2" MAINLINE FROM Y=1980 TO RISER B4 (Y=900) - ENDS AT RISER B4 -->
  <line x1="{PLOTB_EAST_X}" y1="{PLOTB_START_Y}" x2="{PLOTB_EAST_X}" y2="{RISER_B4_Y}" stroke="#FFFFFF" stroke-width="4.5"/>
  <!-- 2" End Cap at Riser B4 -->
  <line x1="{PLOTB_EAST_X - 12}" y1="{RISER_B4_Y}" x2="{PLOTB_EAST_X + 12}" y2="{RISER_B4_Y}" stroke="#FFFFFF" stroke-width="4"/>

  <!-- Mainline Length Label in Corridor (Placed at Y=1300, between B2 at 1440 and B3 at 1170 to avoid collision) -->
  {pill(PLOTB_EAST_X + 25, 1300, '24\' Bare + 216\' (240\' Total 2")', anchor="left")}

  <!-- 1.25" Subline: ONLY subline continues above B4 (Y=900 to Y=740) -->
  <line x1="{PLOTB_EAST_X}" y1="{RISER_B4_Y}" x2="{PLOTB_EAST_X}" y2="{PLOTB_TOP_Y}" stroke="#E0F2FE" stroke-width="3"/>
  <!-- Subline below B4: Y=1980 to Y=900 -->
  <line x1="{PLOTB_EAST_X}" y1="{PLOTB_START_Y}" x2="{PLOTB_EAST_X}" y2="{RISER_B4_Y}" stroke="#E0F2FE" stroke-width="3" stroke-dasharray="10 4"/>

  <!-- Top Flush Valve at Y=740 -->
  <circle cx="{PLOTB_EAST_X}" cy="{PLOTB_TOP_Y}" r="7" fill="#0B2545" stroke="#E0F2FE" stroke-width="2"/>
  <line x1="{PLOTB_EAST_X}" y1="{PLOTB_TOP_Y}" x2="{PLOTB_EAST_X + 35}" y2="{PLOTB_TOP_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {pill(PLOTB_EAST_X + 40, PLOTB_TOP_Y, '40mm Flush Valve')}

  <!-- Bottom Flush Valve at Y=1980 -->
  <circle cx="{PLOTB_EAST_X}" cy="{PLOTB_START_Y}" r="7" fill="#0B2545" stroke="#E0F2FE" stroke-width="2"/>
  <line x1="{PLOTB_EAST_X}" y1="{PLOTB_START_Y}" x2="{PLOTB_EAST_X + 35}" y2="{PLOTB_START_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {pill(PLOTB_EAST_X + 40, PLOTB_START_Y, '40mm Flush Valve')}
''')

    # Plot B Risers & Callout Pills (in Corridor) - Exactly B1, B2, B3, B4
    b_risers = [
        ("B1", RISER_B1_Y),
        ("B2", RISER_B2_Y),
        ("B3", RISER_B3_Y),
        ("B4", RISER_B4_Y)
    ]
    for b_name, ry in b_risers:
        svg.append(f'''  <!-- {b_name} Symbol -->
  <circle cx="{PLOTB_EAST_X}" cy="{ry}" r="12" fill="#0B2545" stroke="#FFFFFF" stroke-width="2.5"/>
  <circle cx="{PLOTB_EAST_X}" cy="{ry}" r="5" fill="#FFFFFF"/>
  <line x1="{PLOTB_EAST_X}" y1="{ry}" x2="{PLOTB_EAST_X + 35}" y2="{ry}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {pill(PLOTB_EAST_X + 40, ry, b_name + (' (2" Mainline Ends)' if b_name == 'B4' else ''))}
''')

    # Plot B 32 Rows (Westward only)
    for r in range(32):
        row_y = (PLOTB_START_Y - 20) - r * 38.7
        svg.append(f'  <line x1="{PLOTB_EAST_X}" y1="{row_y:.1f}" x2="{PLOTB_WEST_X}" y2="{row_y:.1f}" stroke="#7DD3FC" stroke-width="1.2" opacity="0.85"/>')
        svg.append(f'  <circle cx="{PLOTB_EAST_X}" cy="{row_y:.1f}" r="3" fill="#E0F2FE"/>')
        svg.append(f'  <line x1="{PLOTB_WEST_X}" y1="{row_y - 5:.1f}" x2="{PLOTB_WEST_X}" y2="{row_y + 5:.1f}" stroke="#7DD3FC" stroke-width="2"/>')

    svg.append('</g>')

    # 7. PLOT A (PKM-1, 3,000 PLANTS, 24 TRENCHES)
    PLOTA_MAINLINE_END_Y = BASE_Y - 145 * 5  # Y = 1375
    RISER_A1_Y = BASE_Y - 30 * 5            # Y = 1950
    RISER_A2_Y = BASE_Y - 60 * 5            # Y = 1800
    RISER_A3_Y = BASE_Y - 90 * 5            # Y = 1650
    RISER_A4_Y = BASE_Y - 120 * 5           # Y = 1500
    PLOTA_ACTIVE_START_Y = BASE_Y - 15 * 5  # Y = 2025
    PLOTA_ACTIVE_END_Y = BASE_Y - 135 * 5   # Y = 1425

    svg.append(f'''<g id="PLOT_A">
  <!-- Boundary Box -->
  <rect x="{PLOTA_WEST_X}" y="{PLOTA_ACTIVE_END_Y - 15}" width="{PLOTA_EAST_X - PLOTA_WEST_X}" height="{PLOTA_ACTIVE_START_Y - PLOTA_ACTIVE_END_Y + 30}" fill="none" stroke="#7DD3FC" stroke-width="1.5" stroke-dasharray="8 6"/>
  <text x="{PLOTA_WEST_X + 15}" y="{PLOTA_ACTIVE_END_Y - 30}" fill="#FFFFFF" font-size="18" font-weight="bold">PLOT A: PKM-1 (3x5\', 3000 PLANTS)</text>

  <!-- Width Dimension: 390' (Placed at Y = 1300 to give 75px vertical clearance above end cap) -->
  <line x1="{PLOTA_WEST_X}" y1="1300" x2="{PLOTA_EAST_X}" y2="1300" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  {pill((PLOTA_WEST_X + PLOTA_EAST_X)/2, 1300, '390\'', anchor="center")}

  <!-- 2" CENTER MAINLINE: Runs North 145' to Y=1375 -->
  <line x1="{PLOTA_CENTER_X}" y1="{BASE_Y}" x2="{PLOTA_CENTER_X}" y2="{PLOTA_MAINLINE_END_Y}" stroke="#FFFFFF" stroke-width="4.5"/>
  <!-- 2" End Cap at North End -->
  <line x1="{PLOTA_CENTER_X - 12}" y1="{PLOTA_MAINLINE_END_Y}" x2="{PLOTA_CENTER_X + 12}" y2="{PLOTA_MAINLINE_END_Y}" stroke="#FFFFFF" stroke-width="4"/>
  {pill(PLOTA_CENTER_X, PLOTA_MAINLINE_END_Y - 22, '145\' (2") - 2" END CAP', anchor="center")}

  <!-- 1.5" Sublines (Y=2025 to Y=1425) -->
  <line x1="{PLOTA_CENTER_X}" y1="{PLOTA_ACTIVE_START_Y}" x2="{PLOTA_CENTER_X}" y2="{PLOTA_ACTIVE_END_Y}" stroke="#E0F2FE" stroke-width="3" stroke-dasharray="10 4"/>

  <!-- Plot A Flush Valves (50mm) -->
  <circle cx="{PLOTA_CENTER_X}" cy="{PLOTA_ACTIVE_START_Y}" r="7" fill="#0B2545" stroke="#E0F2FE" stroke-width="2"/>
  <circle cx="{PLOTA_CENTER_X}" cy="{PLOTA_ACTIVE_END_Y}" r="7" fill="#0B2545" stroke="#E0F2FE" stroke-width="2"/>
''')

    # Plot A Risers & 1-Line Compact Pills: A1 (30'), A2 (60'), A3 (90'), A4 (120')
    a_risers = [
        ("A1 (30')", RISER_A1_Y),
        ("A2 (60')", RISER_A2_Y),
        ("A3 (90')", RISER_A3_Y),
        ("A4 (120')", RISER_A4_Y)
    ]
    for a_name, ry in a_risers:
        svg.append(f'''  <!-- {a_name} Symbol -->
  <circle cx="{PLOTA_CENTER_X}" cy="{ry}" r="12" fill="#0B2545" stroke="#FFFFFF" stroke-width="2.5"/>
  <circle cx="{PLOTA_CENTER_X}" cy="{ry}" r="5" fill="#FFFFFF"/>
  <line x1="{PLOTA_CENTER_X}" y1="{ry}" x2="{PLOTA_EAST_X + 25}" y2="{ry}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot)"/>
  {pill(PLOTA_EAST_X + 30, ry, a_name, anchor="left")}
''')

    # Plot A 24 Trenches (East & West)
    for t in range(24):
        trench_y = (PLOTA_ACTIVE_START_Y - 12.5) - t * 25
        svg.append(f'  <line x1="{PLOTA_WEST_X}" y1="{trench_y:.1f}" x2="{PLOTA_EAST_X}" y2="{trench_y:.1f}" stroke="#7DD3FC" stroke-width="1.2" opacity="0.85"/>')
        svg.append(f'  <circle cx="{PLOTA_CENTER_X}" cy="{trench_y:.1f}" r="3.5" fill="#E0F2FE"/>')
        svg.append(f'  <line x1="{PLOTA_WEST_X}" y1="{trench_y - 5:.1f}" x2="{PLOTA_WEST_X}" y2="{trench_y + 5:.1f}" stroke="#7DD3FC" stroke-width="2"/>')
        svg.append(f'  <line x1="{PLOTA_EAST_X}" y1="{trench_y - 5:.1f}" x2="{PLOTA_EAST_X}" y2="{trench_y + 5:.1f}" stroke="#7DD3FC" stroke-width="2"/>')

    svg.append('</g>')

    # 8. TINY SINGLE-LINE FOOTER BAR (Bug 2: Replaces the 1200x400 title block)
    svg.append('''<g id="FOOTER_BAR">
  <rect x="145" y="2650" width="3910" height="45" fill="#0B2545" stroke="#FFFFFF" stroke-width="1.5"/>
  <text x="2100" y="2679" fill="#FFFFFF" font-size="16" font-weight="bold" letter-spacing="1.5" text-anchor="middle">2-ACRE MORINGA DRIP LAYOUT  |  PLOT A: PKM-1 (3x5\', 3000 PLANTS)  |  PLOT B: BHAGYA (7x8\', 750 PLANTS)  |  SCALE: 1 FT = 5 PX</text>
</g>''')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Sheet 1 SVG created: {output_path}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "CAD_Master_Blueprint.svg"
    build_sheet1_svg(out_file)
