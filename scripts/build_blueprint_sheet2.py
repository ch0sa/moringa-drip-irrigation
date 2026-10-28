import os
import sys

def build_sheet2_svg(output_path):
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4200 2800" width="4200" height="2800" style="background:#0B2545; font-family:\'Courier New\', Courier, monospace;">')
    
    # 1. DEFS & PATTERNS
    svg.append('''<defs>
  <pattern id="grid10_s2" width="50" height="50" patternUnits="userSpaceOnUse">
    <path d="M 50 0 L 0 0 0 50" fill="none" stroke="rgba(255, 255, 255, 0.07)" stroke-width="1"/>
  </pattern>
  <pattern id="grid50_s2" width="250" height="250" patternUnits="userSpaceOnUse">
    <rect width="250" height="250" fill="url(#grid10_s2)" />
    <path d="M 250 0 L 0 0 0 250" fill="none" stroke="rgba(255, 255, 255, 0.16)" stroke-width="1.5"/>
  </pattern>
  <pattern id="groundHatch" width="40" height="40" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
    <line x1="0" y1="0" x2="0" y2="40" stroke="#BAE6FD" stroke-width="1" opacity="0.25"/>
  </pattern>
  <marker id="arrow_s2" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#BAE6FD" />
  </marker>
  <marker id="dot_s2" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6">
    <circle cx="5" cy="5" r="3.5" fill="#BAE6FD" stroke="#0B2545" stroke-width="1"/>
  </marker>
</defs>''')

    # Grid background
    svg.append('<rect width="4200" height="2800" fill="#0B2545"/>')
    svg.append('<rect width="4200" height="2800" fill="url(#grid50_s2)"/>')

    # Borders (identical margins to Sheet 1)
    svg.append('<rect x="120" y="80" width="3960" height="2640" fill="none" stroke="#FFFFFF" stroke-width="5"/>')
    svg.append('<rect x="145" y="105" width="3910" height="2590" fill="none" stroke="#FFFFFF" stroke-width="2"/>')

    # 1-Line Compact Pill Helper
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

    # 2. HEADER
    svg.append('''<g transform="translate(180, 160)">
  <text x="0" y="0" fill="#FFFFFF" font-size="32" font-weight="bold" letter-spacing="2">4-FOOT OVERHEAD DOUBLE-TEE RISER MANIFOLD — DETAIL ELEVATION</text>
  <text x="0" y="28" fill="#BAE6FD" font-size="16" letter-spacing="1">SHEET 2 OF 2 : SIDE-ELEVATION CROSS-SECTION (WAIST-HEIGHT DUAL CONTROLS)</text>
</g>''')

    # Small Top Legend Box
    svg.append(f'''<g transform="translate(1950, 125)">
  <rect x="0" y="0" width="1550" height="66" fill="#0B2545" stroke="#BAE6FD" stroke-width="1.2" rx="5"/>
  <text x="16" y="26" fill="#BAE6FD" font-size="13" font-weight="bold">PLOT A RISER: 2" RISER + 2x 50MM BALL VALVES + 1.5" DROPS TO 1.5" SUBLINE</text>
  <text x="16" y="50" fill="#BAE6FD" font-size="13" font-weight="bold">PLOT B RISER: 2" RISER + 2x 40MM BALL VALVES + 1.25" DROPS TO 1.25" SUBLINE</text>
</g>''')

    # Scale indicator top right
    svg.append('''<g transform="translate(3650, 160)">
  <rect x="0" y="-20" width="260" height="42" fill="#0B2545" stroke="#BAE6FD" stroke-width="1.2" rx="4"/>
  <text x="130" y="6" fill="#FFFFFF" font-size="13" font-weight="bold" text-anchor="middle">SCALE: 1 FT = 60 PX</text>
</g>''')

    # 3. ELEVATION GEOMETRY COORDINATES
    CX = 2100
    GRADE_Y = 1400
    OVERHEAD_Y = 920          # +4.0' above grade (480 px)
    SUBLINE_TRENCH_Y = 1640   # -2.0' below grade (240 px)
    MAINLINE_TRENCH_Y = 1700  # -2.5' below grade (300 px)
    PIPE_MAIN_Y = 1660

    LEFT_DROP_X = 1450
    RIGHT_DROP_X = 2750
    LEFT_FLUSH_X = 1000
    RIGHT_FLUSH_X = 3200

    # 4. GROUND PROFILE & TRENCH CUT EXCAVATION
    svg.append(f'''<g id="GROUND_AND_TRENCHES">
  <!-- Hatching below Grade Line -->
  <rect x="500" y="{GRADE_Y}" width="3200" height="500" fill="url(#groundHatch)" opacity="0.3"/>

  <!-- Finished Ground Level Line (0.00' Elev) -->
  <line x1="500" y1="{GRADE_Y}" x2="3700" y2="{GRADE_Y}" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="14 6"/>
  {pill(680, GRADE_Y - 20, "FINISHED GROUND LEVEL (0.00' ELEVATION)", anchor="center")}

  <!-- Mainline Trench Excavation Profile (-2'-6" Depth) -->
  <path d="M {CX - 120},{GRADE_Y} L {CX - 120},{MAINLINE_TRENCH_Y} L {CX + 120},{MAINLINE_TRENCH_Y} L {CX + 120},{GRADE_Y}" fill="none" stroke="#BAE6FD" stroke-width="2" stroke-dasharray="6 4"/>
  {pill(CX, MAINLINE_TRENCH_Y + 25, 'MAINLINE TRENCH BED (-2\'-6")', anchor="center", font_size=12)}

  <!-- South Subline Trench Excavation (-2'-0" Depth) -->
  <path d="M {LEFT_FLUSH_X - 60},{GRADE_Y} L {LEFT_FLUSH_X - 60},{SUBLINE_TRENCH_Y} L {LEFT_DROP_X + 80},{SUBLINE_TRENCH_Y} L {LEFT_DROP_X + 80},{GRADE_Y}" fill="none" stroke="#BAE6FD" stroke-width="2" stroke-dasharray="6 4"/>
  {pill((LEFT_FLUSH_X + LEFT_DROP_X)/2, SUBLINE_TRENCH_Y + 25, 'SOUTH SUBLINE TRENCH BED (-2\'-0")', anchor="center", font_size=12)}

  <!-- North Subline Trench Excavation (-2'-0" Depth) -->
  <path d="M {RIGHT_DROP_X - 80},{GRADE_Y} L {RIGHT_DROP_X - 80},{SUBLINE_TRENCH_Y} L {RIGHT_FLUSH_X + 60},{SUBLINE_TRENCH_Y} L {RIGHT_FLUSH_X + 60},{GRADE_Y}" fill="none" stroke="#BAE6FD" stroke-width="2" stroke-dasharray="6 4"/>
  {pill((RIGHT_DROP_X + RIGHT_FLUSH_X)/2, SUBLINE_TRENCH_Y + 25, 'NORTH SUBLINE TRENCH BED (-2\'-0")', anchor="center", font_size=12)}
</g>''')

    # 5. PIPES & FITTINGS GEOMETRY
    svg.append(f'''<g id="PIPES_AND_MANIFOLD">
  <!-- BURIED 2" MAINLINE PIPE -->
  <circle cx="{CX}" cy="{PIPE_MAIN_Y}" r="32" fill="#0B2545" stroke="#FFFFFF" stroke-width="4.5"/>
  <circle cx="{CX}" cy="{PIPE_MAIN_Y}" r="22" fill="#0B2545" stroke="#BAE6FD" stroke-width="2"/>
  <circle cx="{CX}" cy="{PIPE_MAIN_Y}" r="6" fill="#FFFFFF"/>

  <!-- BURIED 2" EQUAL TEE -->
  <rect x="{CX - 28}" y="{PIPE_MAIN_Y - 45}" width="56" height="40" fill="#0B2545" stroke="#FFFFFF" stroke-width="3"/>
  <line x1="{CX - 28}" y1="{PIPE_MAIN_Y - 25}" x2="{CX + 28}" y2="{PIPE_MAIN_Y - 25}" stroke="#BAE6FD" stroke-width="1.5"/>

  <!-- 4-FOOT VERTICAL 2" PVC RISER PIPE -->
  <rect x="{CX - 22}" y="{OVERHEAD_Y}" width="44" height="{PIPE_MAIN_Y - 45 - OVERHEAD_Y}" fill="#0B2545" stroke="#FFFFFF" stroke-width="4.5"/>
  <line x1="{CX}" y1="{OVERHEAD_Y}" x2="{CX}" y2="{PIPE_MAIN_Y - 45}" stroke="#BAE6FD" stroke-width="1.5" stroke-dasharray="8 6"/>

  <!-- OVERHEAD 2" EQUAL DOUBLE-TEE -->
  <rect x="{CX - 40}" y="{OVERHEAD_Y - 35}" width="80" height="70" rx="8" fill="#0B2545" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="{CX}" cy="{OVERHEAD_Y}" r="18" fill="#FFFFFF"/>
  <circle cx="{CX}" cy="{OVERHEAD_Y}" r="8" fill="#0B2545"/>

  <!-- ==================== SOUTH WING (LEFT SIDE) ==================== -->
  <line x1="{CX - 40}" y1="{OVERHEAD_Y}" x2="{CX - 180}" y2="{OVERHEAD_Y}" stroke="#FFFFFF" stroke-width="4.5"/>

  <!-- Reducer -->
  <polygon points="{CX - 180},{OVERHEAD_Y - 26} {CX - 240},{OVERHEAD_Y - 18} {CX - 240},{OVERHEAD_Y + 18} {CX - 180},{OVERHEAD_Y + 26}" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>

  <!-- Ball Valve -->
  <rect x="{CX - 380}" y="{OVERHEAD_Y - 25}" width="140" height="50" rx="6" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>
  <polygon points="{CX - 360},{OVERHEAD_Y - 20} {CX - 260},{OVERHEAD_Y + 20} {CX - 360},{OVERHEAD_Y + 20} {CX - 260},{OVERHEAD_Y - 20}" fill="#0B2545" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="{CX - 310}" cy="{OVERHEAD_Y}" r="9" fill="#FFFFFF"/>
  <rect x="{CX - 325}" y="{OVERHEAD_Y - 60}" width="70" height="18" rx="4" fill="#FFFFFF" stroke="#0B2545" stroke-width="2"/>
  <line x1="{CX - 310}" y1="{OVERHEAD_Y - 25}" x2="{CX - 310}" y2="{OVERHEAD_Y - 50}" stroke="#FFFFFF" stroke-width="4"/>

  <!-- Horizontal Pipe to Overhead Elbow -->
  <line x1="{CX - 380}" y1="{OVERHEAD_Y}" x2="{LEFT_DROP_X}" y2="{OVERHEAD_Y}" stroke="#E0F2FE" stroke-width="3.5"/>
  <rect x="{LEFT_DROP_X - 30}" y="{OVERHEAD_Y - 30}" width="60" height="60" rx="8" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>
  <circle cx="{LEFT_DROP_X}" cy="{OVERHEAD_Y}" r="12" fill="#E0F2FE"/>

  <!-- Vertical Drop Pipe -->
  <rect x="{LEFT_DROP_X - 18}" y="{OVERHEAD_Y + 30}" width="36" height="{SUBLINE_TRENCH_Y - 40 - (OVERHEAD_Y + 30)}" fill="#0B2545" stroke="#E0F2FE" stroke-width="3.5"/>
  <line x1="{LEFT_DROP_X}" y1="{OVERHEAD_Y + 30}" x2="{LEFT_DROP_X}" y2="{SUBLINE_TRENCH_Y - 40}" stroke="#BAE6FD" stroke-width="1" stroke-dasharray="6 4"/>

  <!-- Trench Elbow -->
  <rect x="{LEFT_DROP_X - 30}" y="{SUBLINE_TRENCH_Y - 55}" width="60" height="55" rx="8" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>
  <circle cx="{LEFT_DROP_X}" cy="{SUBLINE_TRENCH_Y - 27}" r="12" fill="#E0F2FE"/>

  <!-- Subline Running South -->
  <line x1="{LEFT_DROP_X - 30}" y1="{SUBLINE_TRENCH_Y - 27}" x2="{LEFT_FLUSH_X}" y2="{SUBLINE_TRENCH_Y - 27}" stroke="#E0F2FE" stroke-width="3.5"/>

  <!-- Flush Valve South -->
  <rect x="{LEFT_FLUSH_X - 25}" y="{GRADE_Y}" width="50" height="{SUBLINE_TRENCH_Y - GRADE_Y}" fill="#0B2545" stroke="#BAE6FD" stroke-width="1.5" stroke-dasharray="6 4"/>
  <rect x="{LEFT_FLUSH_X - 35}" y="{GRADE_Y - 8}" width="70" height="16" rx="3" fill="#0B2545" stroke="#BAE6FD" stroke-width="2"/>
  <circle cx="{LEFT_FLUSH_X}" cy="{SUBLINE_TRENCH_Y - 27}" r="16" fill="#0B2545" stroke="#FFFFFF" stroke-width="2.5"/>
  <circle cx="{LEFT_FLUSH_X}" cy="{SUBLINE_TRENCH_Y - 27}" r="8" fill="#E0F2FE"/>

  <!-- ==================== NORTH WING (RIGHT SIDE) ==================== -->
  <line x1="{CX + 40}" y1="{OVERHEAD_Y}" x2="{CX + 180}" y2="{OVERHEAD_Y}" stroke="#FFFFFF" stroke-width="4.5"/>

  <!-- Reducer -->
  <polygon points="{CX + 180},{OVERHEAD_Y - 26} {CX + 240},{OVERHEAD_Y - 18} {CX + 240},{OVERHEAD_Y + 18} {CX + 180},{OVERHEAD_Y + 26}" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>

  <!-- Ball Valve -->
  <rect x="{CX + 240}" y="{OVERHEAD_Y - 25}" width="140" height="50" rx="6" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>
  <polygon points="{CX + 260},{OVERHEAD_Y - 20} {CX + 360},{OVERHEAD_Y + 20} {CX + 260},{OVERHEAD_Y + 20} {CX + 360},{OVERHEAD_Y - 20}" fill="#0B2545" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="{CX + 310}" cy="{OVERHEAD_Y}" r="9" fill="#FFFFFF"/>
  <rect x="{CX + 255}" y="{OVERHEAD_Y - 60}" width="70" height="18" rx="4" fill="#FFFFFF" stroke="#0B2545" stroke-width="2"/>
  <line x1="{CX + 310}" y1="{OVERHEAD_Y - 25}" x2="{CX + 310}" y2="{OVERHEAD_Y - 50}" stroke="#FFFFFF" stroke-width="4"/>

  <!-- Horizontal Pipe to Overhead Elbow -->
  <line x1="{CX + 380}" y1="{OVERHEAD_Y}" x2="{RIGHT_DROP_X}" y2="{OVERHEAD_Y}" stroke="#E0F2FE" stroke-width="3.5"/>
  <rect x="{RIGHT_DROP_X - 30}" y="{OVERHEAD_Y - 30}" width="60" height="60" rx="8" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>
  <circle cx="{RIGHT_DROP_X}" cy="{OVERHEAD_Y}" r="12" fill="#E0F2FE"/>

  <!-- Vertical Drop Pipe -->
  <rect x="{RIGHT_DROP_X - 18}" y="{OVERHEAD_Y + 30}" width="36" height="{SUBLINE_TRENCH_Y - 40 - (OVERHEAD_Y + 30)}" fill="#0B2545" stroke="#E0F2FE" stroke-width="3.5"/>
  <line x1="{RIGHT_DROP_X}" y1="{OVERHEAD_Y + 30}" x2="{RIGHT_DROP_X}" y2="{SUBLINE_TRENCH_Y - 40}" stroke="#BAE6FD" stroke-width="1" stroke-dasharray="6 4"/>

  <!-- Trench Elbow -->
  <rect x="{RIGHT_DROP_X - 30}" y="{SUBLINE_TRENCH_Y - 55}" width="60" height="55" rx="8" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>
  <circle cx="{RIGHT_DROP_X}" cy="{SUBLINE_TRENCH_Y - 27}" r="12" fill="#E0F2FE"/>

  <!-- Subline Running North -->
  <line x1="{RIGHT_DROP_X + 30}" y1="{SUBLINE_TRENCH_Y - 27}" x2="{RIGHT_FLUSH_X}" y2="{SUBLINE_TRENCH_Y - 27}" stroke="#E0F2FE" stroke-width="3.5"/>

  <!-- Flush Valve North -->
  <rect x="{RIGHT_FLUSH_X - 25}" y="{GRADE_Y}" width="50" height="{SUBLINE_TRENCH_Y - GRADE_Y}" fill="#0B2545" stroke="#BAE6FD" stroke-width="1.5" stroke-dasharray="6 4"/>
  <rect x="{RIGHT_FLUSH_X - 35}" y="{GRADE_Y - 8}" width="70" height="16" rx="3" fill="#0B2545" stroke="#BAE6FD" stroke-width="2"/>
  <circle cx="{RIGHT_FLUSH_X}" cy="{SUBLINE_TRENCH_Y - 27}" r="16" fill="#0B2545" stroke="#FFFFFF" stroke-width="2.5"/>
  <circle cx="{RIGHT_FLUSH_X}" cy="{SUBLINE_TRENCH_Y - 27}" r="8" fill="#E0F2FE"/>
</g>''')

    # 6. EXTERNAL ZERO-OVERLAP 1-LINE COMPACT CALLOUT COLUMNS
    # LEFT COLUMN (South Wing Components) - Anchored at X = 320 to 800
    svg.append(f'''<g id="LEFT_CALLOUT_COLUMN">
  <!-- 2"x1.5" / 2"x1.25" Reducer -->
  <line x1="{CX - 210}" y1="{OVERHEAD_Y - 20}" x2="720" y2="760" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {pill(700, 760, '2"x1.5" / 2"x1.25" Reducer', anchor="right")}

  <!-- 50mm / 40mm Ball Valve -->
  <line x1="{CX - 310}" y1="{OVERHEAD_Y}" x2="720" y2="{OVERHEAD_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {pill(700, OVERHEAD_Y, '50mm / 40mm Ball Valve', anchor="right")}

  <!-- 1.5" / 1.25" Elbow & 4\' Drop -->
  <line x1="{LEFT_DROP_X}" y1="1160" x2="720" y2="1160" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {pill(700, 1160, '1.5" / 1.25" Elbow &amp; 4\' Drop', anchor="right")}

  <!-- 1.5" / 1.25" Subline -->
  <line x1="{LEFT_DROP_X - 160}" y1="{SUBLINE_TRENCH_Y - 27}" x2="720" y2="1420" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {pill(700, 1420, '1.5" / 1.25" Subline', anchor="right")}

  <!-- 50mm / 40mm Flush Valve -->
  <line x1="{LEFT_FLUSH_X}" y1="{SUBLINE_TRENCH_Y - 27}" x2="720" y2="{SUBLINE_TRENCH_Y - 27}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {pill(700, SUBLINE_TRENCH_Y - 27, '50mm / 40mm Flush Valve', anchor="right")}
</g>''')

    # RIGHT COLUMN (Center Riser & Mainline Details) - Anchored at X = 3400
    svg.append(f'''<g id="RIGHT_CALLOUT_COLUMN">
  <!-- 2" Overhead Tee -->
  <line x1="{CX + 40}" y1="{OVERHEAD_Y - 20}" x2="3380" y2="760" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {pill(3400, 760, '2" Overhead Tee', anchor="left")}

  <!-- 4\' Vertical 2" Riser -->
  <line x1="{CX + 22}" y1="1160" x2="3380" y2="1160" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {pill(3400, 1160, '4\' Vertical 2" Riser', anchor="left")}

  <!-- 2" Buried Tee -->
  <line x1="{CX + 28}" y1="{PIPE_MAIN_Y - 25}" x2="3380" y2="1420" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {pill(3400, 1420, '2" Buried Tee', anchor="left")}

  <!-- 2" Mainline -->
  <line x1="{CX + 32}" y1="{PIPE_MAIN_Y}" x2="3380" y2="{PIPE_MAIN_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {pill(3400, PIPE_MAIN_Y, '2" Mainline', anchor="left")}

  <!-- North Flush Valve -->
  <line x1="{RIGHT_FLUSH_X}" y1="{SUBLINE_TRENCH_Y - 27}" x2="3380" y2="1820" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {pill(3400, 1820, '50mm / 40mm Flush Valve (North)', anchor="left")}
</g>''')

    # 7. ELEVATION DIMENSIONS (Waist Height & Trench Depths)
    svg.append(f'''<g id="ELEVATION_DIMENSIONS">
  <!-- Dimension: Grade Level to Overhead (+4'-0") -->
  <line x1="{CX + 90}" y1="{GRADE_Y}" x2="{CX + 90}" y2="{OVERHEAD_Y}" stroke="#BAE6FD" stroke-width="1.5" marker-start="url(#arrow_s2)" marker-end="url(#arrow_s2)"/>
  {pill(CX + 110, (GRADE_Y + OVERHEAD_Y)/2, '+4\'-0" (Overhead Waist Height)', anchor="left")}

  <!-- Dimension: Grade Level down to Subline Trench (-2'-0") -->
  <line x1="{LEFT_DROP_X + 50}" y1="{GRADE_Y}" x2="{LEFT_DROP_X + 50}" y2="{SUBLINE_TRENCH_Y}" stroke="#BAE6FD" stroke-width="1.5" marker-start="url(#arrow_s2)" marker-end="url(#arrow_s2)"/>
  {pill(LEFT_DROP_X + 70, (GRADE_Y + SUBLINE_TRENCH_Y)/2, '-2\'-0" (Subline Depth)', anchor="left")}

  <!-- Dimension: Grade Level down to Mainline Trench (-2'-6") -->
  <line x1="{CX - 90}" y1="{GRADE_Y}" x2="{CX - 90}" y2="{MAINLINE_TRENCH_Y}" stroke="#BAE6FD" stroke-width="1.5" marker-start="url(#arrow_s2)" marker-end="url(#arrow_s2)"/>
  {pill(CX - 110, (GRADE_Y + MAINLINE_TRENCH_Y)/2, '-2\'-6" (Mainline Depth)', anchor="right")}
</g>''')

    # 8. TINY SINGLE-LINE FOOTER BAR (Bug 2: Replaces the 1200x400 title block)
    svg.append('''<g id="FOOTER_BAR_S2">
  <rect x="145" y="2650" width="3910" height="45" fill="#0B2545" stroke="#FFFFFF" stroke-width="1.5"/>
  <text x="2100" y="2679" fill="#FFFFFF" font-size="16" font-weight="bold" letter-spacing="1.5" text-anchor="middle">2-ACRE MORINGA DRIP LAYOUT  |  SHEET 2: 4\' OVERHEAD RISER MANIFOLD DETAIL  |  SCALE: 1 FT = 60 PX</text>
</g>''')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Sheet 2 SVG created: {output_path}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "Riser_Manifold_Detail.svg"
    build_sheet2_svg(out_file)
