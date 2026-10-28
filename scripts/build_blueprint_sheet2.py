import os
import sys

def build_sheet2_svg(output_path):
    svg_lines = []
    svg_lines.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4200 2800" width="4200" height="2800" style="background:#0B2545; font-family:\'Courier New\', Courier, monospace;">')
    
    # 1. DEFS & PATTERNS
    svg_lines.append('''<defs>
  <!-- Subtle Blueprint Engineering Grid -->
  <pattern id="grid10_s2" width="50" height="50" patternUnits="userSpaceOnUse">
    <path d="M 50 0 L 0 0 0 50" fill="none" stroke="rgba(255, 255, 255, 0.07)" stroke-width="1"/>
  </pattern>
  <pattern id="grid50_s2" width="250" height="250" patternUnits="userSpaceOnUse">
    <rect width="250" height="250" fill="url(#grid10_s2)" />
    <path d="M 250 0 L 0 0 0 250" fill="none" stroke="rgba(255, 255, 255, 0.16)" stroke-width="1.5"/>
  </pattern>

  <!-- Ground Hatch Pattern -->
  <pattern id="groundHatch" width="40" height="40" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
    <line x1="0" y1="0" x2="0" y2="40" stroke="#BAE6FD" stroke-width="1" opacity="0.25"/>
  </pattern>

  <!-- Markers -->
  <marker id="arrow_s2" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#BAE6FD" />
  </marker>
  <marker id="dot_s2" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6">
    <circle cx="5" cy="5" r="3.5" fill="#BAE6FD" stroke="#0B2545" stroke-width="1"/>
  </marker>
</defs>''')

    # Grid Background
    svg_lines.append('<rect width="4200" height="2800" fill="#0B2545"/>')
    svg_lines.append('<rect width="4200" height="2800" fill="url(#grid50_s2)"/>')

    # 2. ARCHITECTURAL BORDER & HEADER
    svg_lines.append('<rect x="120" y="100" width="3960" height="2600" fill="none" stroke="#FFFFFF" stroke-width="5"/>')
    svg_lines.append('<rect x="145" y="125" width="3910" height="2550" fill="none" stroke="#FFFFFF" stroke-width="2"/>')

    # Sheet Header
    svg_lines.append('''<g transform="translate(180, 190)">
  <text x="0" y="0" fill="#FFFFFF" font-size="44" font-weight="bold" letter-spacing="3">4-FOOT OVERHEAD DOUBLE-TEE RISER MANIFOLD — DETAIL CROSS-SECTION</text>
  <text x="0" y="38" fill="#BAE6FD" font-size="22" letter-spacing="1.5">SIDE-ELEVATION LOOKING EAST • WAIST-HEIGHT VALVE CONTROLS • TRENCH DROP PROFILES</text>
  <text x="0" y="70" fill="#BAE6FD" font-size="16" letter-spacing="1">APPLIES TO RISERS A1–A4 (50MM BALL VALVES) &amp; RISERS B1–B4 (40MM BALL VALVES) | SCALE: 1 FT = 60 PX</text>
</g>''')

    # Helper function for Callout Pills
    def callout_pill(x, y, text_lines, width=320, height=None, anchor="left", border_col="#BAE6FD", bg_col="#0B2545", font_size=15):
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

    # 3. ELEVATION GEOMETRY COORDINATES
    # Center X: 2100 px (exact center of 4200 canvas)
    # Finished Grade Level (0.00' Elev): Y = 1350 px
    # +4.00' Overhead Manifold: Y = 1350 - 4.0 * 120 = 870 px (Scale: 1 ft = 120 px in detail view)
    # -2.00' Subline Trench: Y = 1350 + 2.0 * 120 = 1590 px
    # -2.50' Mainline Trench: Y = 1350 + 2.5 * 120 = 1650 px
    
    CX = 2100
    GRADE_Y = 1350
    OVERHEAD_Y = 870
    SUBLINE_TRENCH_Y = 1590
    MAINLINE_TRENCH_Y = 1650
    PIPE_MAIN_Y = 1610  # Mainline pipe center

    # Outer Left Wing: X = 1300 (Elbow drop) to X = 950 (Flush valve)
    # Outer Right Wing: X = 2900 (Elbow drop) to X = 3250 (Flush valve)
    LEFT_DROP_X = 1450
    RIGHT_DROP_X = 2750
    LEFT_FLUSH_X = 1000
    RIGHT_FLUSH_X = 3200

    # 4. GROUND PROFILE & TRENCH CUT EXCAVATION
    svg_lines.append(f'''<g id="GROUND_AND_TRENCHES">
  <!-- Hatching below Grade Line -->
  <rect x="500" y="{GRADE_Y}" width="3200" height="500" fill="url(#groundHatch)" opacity="0.3"/>

  <!-- Finished Ground Level Line (0.00' Elev) -->
  <line x1="500" y1="{GRADE_Y}" x2="3700" y2="{GRADE_Y}" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="14 6"/>
  <rect x="520" y="{GRADE_Y - 34}" width="360" height="26" fill="#0B2545" stroke="#BAE6FD" stroke-width="1" rx="4"/>
  <text x="700" y="{GRADE_Y - 16}" fill="#BAE6FD" font-size="14" font-weight="bold" text-anchor="middle">FINISHED GROUND LEVEL (0.00\' ELEVATION)</text>

  <!-- Mainline Trench Excavation Profile (-2\'-6" Depth) -->
  <path d="M {CX - 120},{GRADE_Y} L {CX - 120},{MAINLINE_TRENCH_Y} L {CX + 120},{MAINLINE_TRENCH_Y} L {CX + 120},{GRADE_Y}" fill="none" stroke="#BAE6FD" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="{CX}" y="{MAINLINE_TRENCH_Y + 30}" fill="#BAE6FD" font-size="13" font-weight="bold" text-anchor="middle">MAINLINE TRENCH BED (-2\'-6" / 750MM DEPTH)</text>

  <!-- South Subline Trench Excavation (-2\'-0" Depth) -->
  <path d="M {LEFT_FLUSH_X - 60},{GRADE_Y} L {LEFT_FLUSH_X - 60},{SUBLINE_TRENCH_Y} L {LEFT_DROP_X + 80},{SUBLINE_TRENCH_Y} L {LEFT_DROP_X + 80},{GRADE_Y}" fill="none" stroke="#BAE6FD" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="{(LEFT_FLUSH_X + LEFT_DROP_X)/2}" y="{SUBLINE_TRENCH_Y + 30}" fill="#BAE6FD" font-size="13" font-weight="bold" text-anchor="middle">SOUTH SUBLINE TRENCH BED (-2\'-0" / 600MM)</text>

  <!-- North Subline Trench Excavation (-2\'-0" Depth) -->
  <path d="M {RIGHT_DROP_X - 80},{GRADE_Y} L {RIGHT_DROP_X - 80},{SUBLINE_TRENCH_Y} L {RIGHT_FLUSH_X + 60},{SUBLINE_TRENCH_Y} L {RIGHT_FLUSH_X + 60},{GRADE_Y}" fill="none" stroke="#BAE6FD" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="{(RIGHT_DROP_X + RIGHT_FLUSH_X)/2}" y="{SUBLINE_TRENCH_Y + 30}" fill="#BAE6FD" font-size="13" font-weight="bold" text-anchor="middle">NORTH SUBLINE TRENCH BED (-2\'-0" / 600MM)</text>
</g>''')

    # 5. PIPES & FITTINGS GEOMETRY
    svg_lines.append(f'''<g id="PIPES_AND_MANIFOLD">
  <!-- BURIED 2" MAINLINE PIPE (Flowing East-West through CX, PIPE_MAIN_Y) -->
  <circle cx="{CX}" cy="{PIPE_MAIN_Y}" r="32" fill="#0B2545" stroke="#FFFFFF" stroke-width="4.5"/>
  <circle cx="{CX}" cy="{PIPE_MAIN_Y}" r="22" fill="#0B2545" stroke="#BAE6FD" stroke-width="2"/>
  <circle cx="{CX}" cy="{PIPE_MAIN_Y}" r="6" fill="#FFFFFF"/>

  <!-- BURIED 2" EQUAL TEE (Pointing Vertically Upwards) -->
  <rect x="{CX - 28}" y="{PIPE_MAIN_Y - 45}" width="56" height="40" fill="#0B2545" stroke="#FFFFFF" stroke-width="3"/>
  <line x1="{CX - 28}" y1="{PIPE_MAIN_Y - 25}" x2="{CX + 28}" y2="{PIPE_MAIN_Y - 25}" stroke="#BAE6FD" stroke-width="1.5"/>

  <!-- 4-FOOT VERTICAL 2" PVC RISER PIPE (+4.0' Elev above grade) -->
  <rect x="{CX - 22}" y="{OVERHEAD_Y}" width="44" height="{PIPE_MAIN_Y - 45 - OVERHEAD_Y}" fill="#0B2545" stroke="#FFFFFF" stroke-width="4.5"/>
  <line x1="{CX}" y1="{OVERHEAD_Y}" x2="{CX}" y2="{PIPE_MAIN_Y - 45}" stroke="#BAE6FD" stroke-width="1.5" stroke-dasharray="8 6"/>

  <!-- OVERHEAD 2" EQUAL DOUBLE-TEE (AT +4.00' ELEVATION, Y = 870) -->
  <rect x="{CX - 40}" y="{OVERHEAD_Y - 35}" width="80" height="70" rx="8" fill="#0B2545" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="{CX}" cy="{OVERHEAD_Y}" r="18" fill="#FFFFFF"/>
  <circle cx="{CX}" cy="{OVERHEAD_Y}" r="8" fill="#0B2545"/>

  <!-- ==================== SOUTH WING (LEFT SIDE) ==================== -->
  <!-- Horizontal 2" Pipe from Center Tee to Reducer -->
  <line x1="{CX - 40}" y1="{OVERHEAD_Y}" x2="{CX - 180}" y2="{OVERHEAD_Y}" stroke="#FFFFFF" stroke-width="4.5"/>

  <!-- 2" x 1.5" (Plot A) / 2" x 1.25" (Plot B) Bushing Reducer -->
  <polygon points="{CX - 180},{OVERHEAD_Y - 26} {CX - 240},{OVERHEAD_Y - 18} {CX - 240},{OVERHEAD_Y + 18} {CX - 180},{OVERHEAD_Y + 26}" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>

  <!-- 50mm / 40mm Plain Ball Valve (South Wing Control) -->
  <rect x="{CX - 380}" y="{OVERHEAD_Y - 25}" width="140" height="50" rx="6" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>
  <polygon points="{CX - 360},{OVERHEAD_Y - 20} {CX - 260},{OVERHEAD_Y + 20} {CX - 360},{OVERHEAD_Y + 20} {CX - 260},{OVERHEAD_Y - 20}" fill="#0B2545" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="{CX - 310}" cy="{OVERHEAD_Y}" r="9" fill="#FFFFFF"/>
  <!-- Valve Ergonomic Lever Handle -->
  <rect x="{CX - 325}" y="{OVERHEAD_Y - 60}" width="70" height="18" rx="4" fill="#FFFFFF" stroke="#0B2545" stroke-width="2"/>
  <line x1="{CX - 310}" y1="{OVERHEAD_Y - 25}" x2="{CX - 310}" y2="{OVERHEAD_Y - 50}" stroke="#FFFFFF" stroke-width="4"/>

  <!-- Horizontal Pipe into 90° Overhead Elbow -->
  <line x1="{CX - 380}" y1="{OVERHEAD_Y}" x2="{LEFT_DROP_X}" y2="{OVERHEAD_Y}" stroke="#E0F2FE" stroke-width="3.5"/>
  <!-- 90° Overhead Elbow -->
  <rect x="{LEFT_DROP_X - 30}" y="{OVERHEAD_Y - 30}" width="60" height="60" rx="8" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>
  <circle cx="{LEFT_DROP_X}" cy="{OVERHEAD_Y}" r="12" fill="#E0F2FE"/>

  <!-- 6-FOOT VERTICAL DROP PIPE (Down into South Trench) -->
  <rect x="{LEFT_DROP_X - 18}" y="{OVERHEAD_Y + 30}" width="36" height="{SUBLINE_TRENCH_Y - 40 - (OVERHEAD_Y + 30)}" fill="#0B2545" stroke="#E0F2FE" stroke-width="3.5"/>
  <line x1="{LEFT_DROP_X}" y1="{OVERHEAD_Y + 30}" x2="{LEFT_DROP_X}" y2="{SUBLINE_TRENCH_Y - 40}" stroke="#BAE6FD" stroke-width="1" stroke-dasharray="6 4"/>

  <!-- 90° Bottom Trench Elbow -->
  <rect x="{LEFT_DROP_X - 30}" y="{SUBLINE_TRENCH_Y - 55}" width="60" height="55" rx="8" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>
  <circle cx="{LEFT_DROP_X}" cy="{SUBLINE_TRENCH_Y - 27}" r="12" fill="#E0F2FE"/>

  <!-- BURIED SUBLINE PIPE RUNNING SOUTH (-2.0' Depth) -->
  <line x1="{LEFT_DROP_X - 30}" y1="{SUBLINE_TRENCH_Y - 27}" x2="{LEFT_FLUSH_X}" y2="{SUBLINE_TRENCH_Y - 27}" stroke="#E0F2FE" stroke-width="3.5"/>

  <!-- Lateral Take-off Collar Example on Subline -->
  <rect x="{LEFT_DROP_X - 220}" y="{SUBLINE_TRENCH_Y - 45}" width="36" height="36" rx="4" fill="#0B2545" stroke="#7DD3FC" stroke-width="2"/>
  <circle cx="{LEFT_DROP_X - 202}" cy="{SUBLINE_TRENCH_Y - 27}" r="7" fill="#7DD3FC"/>
  <!-- Lateral Pipe Branching Out -->
  <line x1="{LEFT_DROP_X - 202}" y1="{SUBLINE_TRENCH_Y - 45}" x2="{LEFT_DROP_X - 202}" y2="{SUBLINE_TRENCH_Y - 85}" stroke="#7DD3FC" stroke-width="2.5"/>

  <!-- Terminal Flush Valve at South Arm End in Surface Access Sleeve -->
  <!-- 8" Surface Access PVC Pipe -->
  <rect x="{LEFT_FLUSH_X - 25}" y="{GRADE_Y}" width="50" height="{SUBLINE_TRENCH_Y - GRADE_Y}" fill="#0B2545" stroke="#BAE6FD" stroke-width="1.5" stroke-dasharray="6 4"/>
  <rect x="{LEFT_FLUSH_X - 35}" y="{GRADE_Y - 8}" width="70" height="16" rx="3" fill="#0B2545" stroke="#BAE6FD" stroke-width="2"/>
  <!-- Flush Valve Body -->
  <circle cx="{LEFT_FLUSH_X}" cy="{SUBLINE_TRENCH_Y - 27}" r="16" fill="#0B2545" stroke="#FFFFFF" stroke-width="2.5"/>
  <circle cx="{LEFT_FLUSH_X}" cy="{SUBLINE_TRENCH_Y - 27}" r="8" fill="#E0F2FE"/>


  <!-- ==================== NORTH WING (RIGHT SIDE) ==================== -->
  <!-- Horizontal 2" Pipe from Center Tee to Reducer -->
  <line x1="{CX + 40}" y1="{OVERHEAD_Y}" x2="{CX + 180}" y2="{OVERHEAD_Y}" stroke="#FFFFFF" stroke-width="4.5"/>

  <!-- 2" x 1.5" (Plot A) / 2" x 1.25" (Plot B) Bushing Reducer -->
  <polygon points="{CX + 180},{OVERHEAD_Y - 26} {CX + 240},{OVERHEAD_Y - 18} {CX + 240},{OVERHEAD_Y + 18} {CX + 180},{OVERHEAD_Y + 26}" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>

  <!-- 50mm / 40mm Plain Ball Valve (North Wing Control) -->
  <rect x="{CX + 240}" y="{OVERHEAD_Y - 25}" width="140" height="50" rx="6" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>
  <polygon points="{CX + 260},{OVERHEAD_Y - 20} {CX + 360},{OVERHEAD_Y + 20} {CX + 260},{OVERHEAD_Y + 20} {CX + 360},{OVERHEAD_Y - 20}" fill="#0B2545" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="{CX + 310}" cy="{OVERHEAD_Y}" r="9" fill="#FFFFFF"/>
  <!-- Valve Lever Handle -->
  <rect x="{CX + 255}" y="{OVERHEAD_Y - 60}" width="70" height="18" rx="4" fill="#FFFFFF" stroke="#0B2545" stroke-width="2"/>
  <line x1="{CX + 310}" y1="{OVERHEAD_Y - 25}" x2="{CX + 310}" y2="{OVERHEAD_Y - 50}" stroke="#FFFFFF" stroke-width="4"/>

  <!-- Horizontal Pipe into 90° Overhead Elbow -->
  <line x1="{CX + 380}" y1="{OVERHEAD_Y}" x2="{RIGHT_DROP_X}" y2="{OVERHEAD_Y}" stroke="#E0F2FE" stroke-width="3.5"/>
  <!-- 90° Overhead Elbow -->
  <rect x="{RIGHT_DROP_X - 30}" y="{OVERHEAD_Y - 30}" width="60" height="60" rx="8" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>
  <circle cx="{RIGHT_DROP_X}" cy="{OVERHEAD_Y}" r="12" fill="#E0F2FE"/>

  <!-- 6-FOOT VERTICAL DROP PIPE (Down into North Trench) -->
  <rect x="{RIGHT_DROP_X - 18}" y="{OVERHEAD_Y + 30}" width="36" height="{SUBLINE_TRENCH_Y - 40 - (OVERHEAD_Y + 30)}" fill="#0B2545" stroke="#E0F2FE" stroke-width="3.5"/>
  <line x1="{RIGHT_DROP_X}" y1="{OVERHEAD_Y + 30}" x2="{RIGHT_DROP_X}" y2="{SUBLINE_TRENCH_Y - 40}" stroke="#BAE6FD" stroke-width="1" stroke-dasharray="6 4"/>

  <!-- 90° Bottom Trench Elbow -->
  <rect x="{RIGHT_DROP_X - 30}" y="{SUBLINE_TRENCH_Y - 55}" width="60" height="55" rx="8" fill="#0B2545" stroke="#E0F2FE" stroke-width="3"/>
  <circle cx="{RIGHT_DROP_X}" cy="{SUBLINE_TRENCH_Y - 27}" r="12" fill="#E0F2FE"/>

  <!-- BURIED SUBLINE PIPE RUNNING NORTH (-2.0' Depth) -->
  <line x1="{RIGHT_DROP_X + 30}" y1="{SUBLINE_TRENCH_Y - 27}" x2="{RIGHT_FLUSH_X}" y2="{SUBLINE_TRENCH_Y - 27}" stroke="#E0F2FE" stroke-width="3.5"/>

  <!-- Lateral Take-off Collar Example on Subline -->
  <rect x="{RIGHT_DROP_X + 220}" y="{SUBLINE_TRENCH_Y - 45}" width="36" height="36" rx="4" fill="#0B2545" stroke="#7DD3FC" stroke-width="2"/>
  <circle cx="{RIGHT_DROP_X + 238}" cy="{SUBLINE_TRENCH_Y - 27}" r="7" fill="#7DD3FC"/>
  <!-- Lateral Pipe Branching Out -->
  <line x1="{RIGHT_DROP_X + 238}" y1="{SUBLINE_TRENCH_Y - 45}" x2="{RIGHT_DROP_X + 238}" y2="{SUBLINE_TRENCH_Y - 85}" stroke="#7DD3FC" stroke-width="2.5"/>

  <!-- Terminal Flush Valve at North Arm End -->
  <rect x="{RIGHT_FLUSH_X - 25}" y="{GRADE_Y}" width="50" height="{SUBLINE_TRENCH_Y - GRADE_Y}" fill="#0B2545" stroke="#BAE6FD" stroke-width="1.5" stroke-dasharray="6 4"/>
  <rect x="{RIGHT_FLUSH_X - 35}" y="{GRADE_Y - 8}" width="70" height="16" rx="3" fill="#0B2545" stroke="#BAE6FD" stroke-width="2"/>
  <circle cx="{RIGHT_FLUSH_X}" cy="{SUBLINE_TRENCH_Y - 27}" r="16" fill="#0B2545" stroke="#FFFFFF" stroke-width="2.5"/>
  <circle cx="{RIGHT_FLUSH_X}" cy="{SUBLINE_TRENCH_Y - 27}" r="8" fill="#E0F2FE"/>
</g>''')

    # 6. EXTERNAL ZERO-OVERLAP CALLOUT COLUMNS
    # LEFT COLUMN (South Wing Components) - Anchored at X = 750 (Right Aligned)
    svg_lines.append(f'''<g id="LEFT_CALLOUT_COLUMN">
  <!-- Callout 1: 50mm/40mm Plain Ball Valve -->
  <line x1="{CX - 310}" y1="{OVERHEAD_Y}" x2="800" y2="{OVERHEAD_Y}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {callout_pill(790, OVERHEAD_Y, [
      "PLAIN BALL VALVE (SOUTH CONTROL)",
      "PLOT A: 50MM (1.5\") | ITEM #13",
      "PLOT B: 40MM (1.25\") | ITEM #12",
      "WAIST-HEIGHT MANUAL ISOLATION"
  ], width=360, anchor="right", font_size=13)}

  <!-- Callout 2: 2\" x 1.5\" / 2\" x 1.25\" Reducer -->
  <line x1="{CX - 210}" y1="{OVERHEAD_Y - 26}" x2="800" y2="720" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {callout_pill(790, 720, [
      "PVC BUSHING REDUCER",
      "PLOT A: 2\" x 1.5\" (63x50MM)",
      "PLOT B: 2\" x 1.25\" (63x40MM)",
      "SOLVENT-WELDED TO TEE HUB"
  ], width=360, anchor="right", font_size=13)}

  <!-- Callout 3: 90° Overhead Elbow -->
  <line x1="{LEFT_DROP_X}" y1="{OVERHEAD_Y}" x2="800" y2="1020" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {callout_pill(790, 1020, [
      "90° PVC OVERHEAD ELBOW",
      "TURNS FLOW DIRECTLY DOWNWARD",
      "PLOT A: 1.5\" (50MM) | PLOT B: 1.25\" (40MM)"
  ], width=360, anchor="right", font_size=13)}

  <!-- Callout 4: 6-Foot Vertical Drop Pipe -->
  <line x1="{LEFT_DROP_X}" y1="1200" x2="800" y2="1200" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {callout_pill(790, 1200, [
      "VERTICAL DROP PIPE (6\'-0\" CUT)",
      "CONNECTS OVERHEAD MANIFOLD (+4.0\')",
      "DOWN TO TRENCH SUBLINE BED (-2.0\')"
  ], width=360, anchor="right", font_size=13)}

  <!-- Callout 5: 90° Bottom Trench Elbow -->
  <line x1="{LEFT_DROP_X}" y1="{SUBLINE_TRENCH_Y - 27}" x2="800" y2="1400" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {callout_pill(790, 1400, [
      "90° PVC TRENCH ELBOW",
      "TURNS FLOW HORIZONTALLY INTO SUBLINE",
      "BEDDED IN SIFTED SAND BEDDING"
  ], width=360, anchor="right", font_size=13)}

  <!-- Callout 6: Take-off Collar -->
  <line x1="{LEFT_DROP_X - 202}" y1="{SUBLINE_TRENCH_Y - 27}" x2="800" y2="1580" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {callout_pill(790, 1580, [
      "LATERAL TAKE-OFF COLLAR",
      "PLOT A: 50x16x2-WAY (V-CONNECTOR)",
      "PLOT B: 40x16x1-WAY TF COLLAR",
      "DRILLED 16MM HOLE + GROMMET"
  ], width=360, anchor="right", font_size=13)}

  <!-- Callout 7: Terminal Flush Valve -->
  <line x1="{LEFT_FLUSH_X}" y1="{SUBLINE_TRENCH_Y - 27}" x2="800" y2="1760" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {callout_pill(790, 1760, [
      "TERMINAL FLUSH VALVE",
      "PLOT A: 50MM FLASH VALVE (ITEM #10)",
      "PLOT B: 40MM FLUSH VALVE (ITEM #7)",
      "8\" SURFACE ACCESS SLEEVE + REMOVABLE CAP"
  ], width=360, anchor="right", font_size=13)}
</g>''')

    # RIGHT COLUMN (North Wing Components & Center Riser Details) - Anchored at X = 3450 (Left Aligned)
    svg_lines.append(f'''<g id="RIGHT_CALLOUT_COLUMN">
  <!-- Callout 1: Overhead 2" Equal Double-Tee -->
  <line x1="{CX + 40}" y1="{OVERHEAD_Y}" x2="3400" y2="720" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {callout_pill(3410, 720, [
      "OVERHEAD 2\" EQUAL DOUBLE-TEE",
      "ELEVATION: +4\'-0\" (WAIST HEIGHT)",
      "SPLITS MAINLINE NORTH &amp; SOUTH",
      "HEAVY-DUTY CLASS 2 PVC FITTING"
  ], width=360, anchor="left", font_size=13)}

  <!-- Callout 2: 4-Foot 2\" Vertical Riser Pipe -->
  <line x1="{CX + 22}" y1="1100" x2="3400" y2="1100" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {callout_pill(3410, 1100, [
      "2\" VERTICAL RISER PIPE",
      "4\'-0\" STANDPIPE ABOVE FINISHED GRADE",
      "RISES OUT OF BURIED MAINLINE TRENCH",
      "RIGID SOLVENT-WELDED JOINT"
  ], width=360, anchor="left", font_size=13)}

  <!-- Callout 3: Buried 2\" Equal Tee on Mainline -->
  <line x1="{CX + 28}" y1="{PIPE_MAIN_Y - 25}" x2="3400" y2="{PIPE_MAIN_Y - 25}" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {callout_pill(3410, PIPE_MAIN_Y - 25, [
      "BURIED 2\" EQUAL PVC TEE",
      "ELEVATION: -2\'-6\" (750MM DEPTH)",
      "BRANCH POINTS VERTICALLY (+Z AXIS)",
      "GLUED DIRECTLY INTO 2\" MAINLINE"
  ], width=360, anchor="left", font_size=13)}

  <!-- Callout 4: Buried 2\" PVC Mainline -->
  <line x1="{CX + 32}" y1="{PIPE_MAIN_Y}" x2="3400" y2="1750" stroke="#BAE6FD" stroke-width="1.2" marker-start="url(#dot_s2)"/>
  {callout_pill(3410, 1750, [
      "2\" (63MM) PVC MAINLINE (CLASS 2)",
      "DYNAMIC OPERATING PRESSURE: 2.5 KG/CM²",
      "WATER VELOCITY: 1.15 M/S (OPTIMAL)",
      "BEDDED IN SIFTED TOP SOIL / SAND"
  ], width=360, anchor="left", font_size=13)}
</g>''')

    # 7. CENTER ELEVATION DATUM MARKS & DIMENSIONS
    svg_lines.append(f'''<g id="ELEVATION_DIMENSIONS">
  <!-- Dimension: Grade Level (0.00') to Overhead Manifold (+4.00') -->
  <line x1="{CX + 90}" y1="{GRADE_Y}" x2="{CX + 90}" y2="{OVERHEAD_Y}" stroke="#BAE6FD" stroke-width="1.5" marker-start="url(#arrow_s2)" marker-end="url(#arrow_s2)"/>
  {callout_pill(CX + 105, (GRADE_Y + OVERHEAD_Y)/2, [
      "+4\'-0\" (1.22M)",
      "OVERHEAD WAIST HEIGHT"
  ], width=230, anchor="left", font_size=13)}

  <!-- Dimension: Grade Level (0.00') down to Subline Trench (-2.00') -->
  <line x1="{LEFT_DROP_X + 50}" y1="{GRADE_Y}" x2="{LEFT_DROP_X + 50}" y2="{SUBLINE_TRENCH_Y}" stroke="#BAE6FD" stroke-width="1.5" marker-start="url(#arrow_s2)" marker-end="url(#arrow_s2)"/>
  {callout_pill(LEFT_DROP_X + 65, (GRADE_Y + SUBLINE_TRENCH_Y)/2, [
      "-2\'-0\" (600MM)",
      "SUBLINE TRENCH DEPTH"
  ], width=210, anchor="left", font_size=13)}

  <!-- Dimension: Grade Level (0.00') down to Mainline Trench (-2.50') -->
  <line x1="{CX - 90}" y1="{GRADE_Y}" x2="{CX - 90}" y2="{MAINLINE_TRENCH_Y}" stroke="#BAE6FD" stroke-width="1.5" marker-start="url(#arrow_s2)" marker-end="url(#arrow_s2)"/>
  {callout_pill(CX - 105, (GRADE_Y + MAINLINE_TRENCH_Y)/2, [
      "-2\'-6\" (750MM)",
      "MAINLINE TRENCH DEPTH"
  ], width=210, anchor="right", font_size=13)}
</g>''')

    # 8. TITLE BLOCK FOR SHEET 2 (BOTTOM RIGHT)
    TB_X = 2850
    TB_Y = 2270
    TB_W = 1200
    TB_H = 400

    svg_lines.append(f'''<g id="ARCHITECTURAL_TITLE_BLOCK_S2">
  <rect x="{TB_X}" y="{TB_Y}" width="{TB_W}" height="{TB_H}" fill="#0B2545" stroke="#FFFFFF" stroke-width="3"/>
  <rect x="{TB_X + 6}" y="{TB_Y + 6}" width="{TB_W - 12}" height="{TB_H - 12}" fill="none" stroke="#BAE6FD" stroke-width="1"/>

  <!-- Dividers -->
  <line x1="{TB_X}" y1="{TB_Y + 90}" x2="{TB_X + TB_W}" y2="{TB_Y + 90}" stroke="#FFFFFF" stroke-width="2"/>
  <line x1="{TB_X}" y1="{TB_Y + 180}" x2="{TB_X + TB_W}" y2="{TB_Y + 180}" stroke="#FFFFFF" stroke-width="2"/>
  <line x1="{TB_X}" y1="{TB_Y + 280}" x2="{TB_X + TB_W}" y2="{TB_Y + 280}" stroke="#FFFFFF" stroke-width="1.5"/>

  <line x1="{TB_X + 420}" y1="{TB_Y + 90}" x2="{TB_X + 420}" y2="{TB_Y + 280}" stroke="#FFFFFF" stroke-width="1.5"/>
  <line x1="{TB_X + 800}" y1="{TB_Y + 90}" x2="{TB_X + 800}" y2="{TB_Y + 280}" stroke="#FFFFFF" stroke-width="1.5"/>
  <line x1="{TB_X + 300}" y1="{TB_Y + 280}" x2="{TB_X + 300}" y2="{TB_Y + TB_H}" stroke="#FFFFFF" stroke-width="1.5"/>
  <line x1="{TB_X + 600}" y1="{TB_Y + 280}" x2="{TB_X + 600}" y2="{TB_Y + TB_H}" stroke="#FFFFFF" stroke-width="1.5"/>
  <line x1="{TB_X + 900}" y1="{TB_Y + 280}" x2="{TB_X + 900}" y2="{TB_Y + TB_H}" stroke="#FFFFFF" stroke-width="1.5"/>

  <!-- Texts -->
  <text x="{TB_X + 25}" y="{TB_Y + 40}" fill="#BAE6FD" font-size="14" letter-spacing="2">PROJECT &amp; LOCATION:</text>
  <text x="{TB_X + 25}" y="{TB_Y + 70}" fill="#FFFFFF" font-size="24" font-weight="bold" letter-spacing="2">2-ACRE MORINGA COMMERCIAL ORCHARD DRIP SYSTEM</text>

  <text x="{TB_X + 25}" y="{TB_Y + 120}" fill="#BAE6FD" font-size="13">DRAWING TITLE:</text>
  <text x="{TB_X + 25}" y="{TB_Y + 150}" fill="#FFFFFF" font-size="18" font-weight="bold">OVERHEAD RISER DETAIL</text>

  <text x="{TB_X + 440}" y="{TB_Y + 120}" fill="#BAE6FD" font-size="13">PLOT A CONFIGURATION:</text>
  <text x="{TB_X + 440}" y="{TB_Y + 145}" fill="#FFFFFF" font-size="14" font-weight="bold">4 STATIONS (A1–A4 @ 30\' CTRS)</text>
  <text x="{TB_X + 440}" y="{TB_Y + 168}" fill="#E0F2FE" font-size="13">2x 50MM VALVES + 15\' SUBLINES</text>

  <text x="{TB_X + 820}" y="{TB_Y + 120}" fill="#BAE6FD" font-size="13">PLOT B CONFIGURATION:</text>
  <text x="{TB_X + 820}" y="{TB_Y + 145}" fill="#FFFFFF" font-size="14" font-weight="bold">4 STATIONS (B1–B4 @ 64\' CTRS)</text>
  <text x="{TB_X + 820}" y="{TB_Y + 168}" fill="#E0F2FE" font-size="13">2x 40MM VALVES + 32\' SUBLINES</text>

  <text x="{TB_X + 25}" y="{TB_Y + 210}" fill="#BAE6FD" font-size="13">OPERATIONAL HEIGHT:</text>
  <text x="{TB_X + 25}" y="{TB_Y + 235}" fill="#FFFFFF" font-size="14" font-weight="bold">+4\'-0" (1.22M) WAIST LEVEL</text>
  <text x="{TB_X + 25}" y="{TB_Y + 258}" fill="#E0F2FE" font-size="13">ERGONOMIC ROTATION ACCESS</text>

  <text x="{TB_X + 440}" y="{TB_Y + 210}" fill="#BAE6FD" font-size="13">PLUMBING SPECIFICATION:</text>
  <text x="{TB_X + 440}" y="{TB_Y + 235}" fill="#FFFFFF" font-size="14" font-weight="bold">HEAVY SOLVENT CEMENT</text>
  <text x="{TB_X + 440}" y="{TB_Y + 258}" fill="#E0F2FE" font-size="13">24-HR HYDROSTATIC CURE</text>

  <text x="{TB_X + 820}" y="{TB_Y + 210}" fill="#BAE6FD" font-size="13">TRENCH DRAINAGE:</text>
  <text x="{TB_X + 820}" y="{TB_Y + 235}" fill="#FFFFFF" font-size="14" font-weight="bold">SURFACE FLUSH SLEEVES</text>
  <text x="{TB_X + 820}" y="{TB_Y + 258}" fill="#E0F2FE" font-size="13">EASY MAINTENANCE ACCESS</text>

  <text x="{TB_X + 25}" y="{TB_Y + 310}" fill="#BAE6FD" font-size="12">SCALE:</text>
  <text x="{TB_X + 25}" y="{TB_Y + 350}" fill="#FFFFFF" font-size="18" font-weight="bold">1 FT = 120 PX</text>
  <text x="{TB_X + 25}" y="{TB_Y + 375}" fill="#BAE6FD" font-size="11">(1:10 DETAIL SCALE)</text>

  <text x="{TB_X + 320}" y="{TB_Y + 310}" fill="#BAE6FD" font-size="12">DATE / STATUS:</text>
  <text x="{TB_X + 320}" y="{TB_Y + 350}" fill="#FFFFFF" font-size="16" font-weight="bold">OCTOBER 2026</text>
  <text x="{TB_X + 320}" y="{TB_Y + 375}" fill="#E0F2FE" font-size="12">APPROVED FOR FIELD</text>

  <text x="{TB_X + 620}" y="{TB_Y + 310}" fill="#BAE6FD" font-size="12">CAD STANDARD:</text>
  <text x="{TB_X + 620}" y="{TB_Y + 350}" fill="#FFFFFF" font-size="16" font-weight="bold">IS 12786 / 4985</text>
  <text x="{TB_X + 620}" y="{TB_Y + 375}" fill="#BAE6FD" font-size="11">CROSS-SECTION DETAIL</text>

  <text x="{TB_X + 920}" y="{TB_Y + 310}" fill="#BAE6FD" font-size="12">SHEET NUMBER:</text>
  <text x="{TB_X + 920}" y="{TB_Y + 355}" fill="#FFFFFF" font-size="28" font-weight="bold">SHEET 2 OF 2</text>
</g>''')

    svg_lines.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Sheet 2 SVG created: {output_path} ({len(svg_lines)} lines)")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "Riser_Manifold_Detail.svg"
    build_sheet2_svg(out_file)
