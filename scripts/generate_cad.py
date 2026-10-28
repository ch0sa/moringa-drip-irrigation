import os
import sys

def write_master_dxf(filename):
    lines = []
    
    # Helper to add entity records
    entities = []
    
    def add_line(layer, x1, y1, x2, y2, linetype="BYLAYER"):
        entities.append(f"""0
LINE
8
{layer}
6
{linetype}
10
{x1:.3f}
20
{y1:.3f}
30
0.0
11
{x2:.3f}
21
{y2:.3f}
31
0.0""")

    def add_circle(layer, cx, cy, radius):
        entities.append(f"""0
CIRCLE
8
{layer}
10
{cx:.3f}
20
{cy:.3f}
30
0.0
40
{radius:.3f}""")

    def add_text(layer, text, x, y, height=2.5, rotation=0.0):
        entities.append(f"""0
TEXT
8
{layer}
10
{x:.3f}
20
{y:.3f}
30
0.0
40
{height:.3f}
50
{rotation:.1f}
1
{text}""")

    def add_valve(layer, x, y, size=3.0, horizontal=True):
        # Draw bowtie valve symbol
        if horizontal:
            add_line(layer, x - size, y - size*0.5, x + size, y + size*0.5)
            add_line(layer, x - size, y + size*0.5, x + size, y - size*0.5)
            add_line(layer, x - size, y - size*0.5, x - size, y + size*0.5)
            add_line(layer, x + size, y - size*0.5, x + size, y + size*0.5)
            add_circle(layer, x, y, size*0.25)
        else:
            add_line(layer, x - size*0.5, y - size, x + size*0.5, y + size)
            add_line(layer, x + size*0.5, y - size, x - size*0.5, y + size)
            add_line(layer, x - size*0.5, y - size, x + size*0.5, y - size)
            add_line(layer, x - size*0.5, y + size, x + size*0.5, y + size)
            add_circle(layer, x, y, size*0.25)

    def add_cap(layer, x, y, size=2.0, orientation="W"):
        # Draw end cap perpendicular tick mark
        if orientation in ("W", "E"):
            add_line(layer, x, y - size, x, y + size)
        else:
            add_line(layer, x - size, y, x + size, y)

    # 1. FIELD BOUNDARIES
    # Plot A boundary
    add_line("08_DIMENSIONS_ANNOTATIONS", 305, 110, 695, 110, "DASHED")
    add_line("08_DIMENSIONS_ANNOTATIONS", 695, 110, 695, 240, "DASHED")
    add_line("08_DIMENSIONS_ANNOTATIONS", 695, 240, 305, 240, "DASHED")
    add_line("08_DIMENSIONS_ANNOTATIONS", 305, 240, 305, 110, "DASHED")
    add_text("08_DIMENSIONS_ANNOTATIONS", "PLOT A BOUNDARY: PKM-1 MORINGA (1 ACRE | 3ft x 5ft | 3,000 PLANTS)", 310, 244, 3.5)

    # Plot B boundary
    add_line("08_DIMENSIONS_ANNOTATIONS", 120, 88, 285, 88, "DASHED")
    add_line("08_DIMENSIONS_ANNOTATIONS", 285, 88, 285, 352, "DASHED")
    add_line("08_DIMENSIONS_ANNOTATIONS", 285, 352, 120, 352, "DASHED")
    add_line("08_DIMENSIONS_ANNOTATIONS", 120, 352, 120, 88, "DASHED")
    add_text("08_DIMENSIONS_ANNOTATIONS", "PLOT B BOUNDARY: BHAGYA MORINGA (1 ACRE | 7ft x 8ft | 750 PLANTS)", 125, 356, 3.5)

    # Buffer zone label
    add_text("08_DIMENSIONS_ANNOTATIONS", "BUFFER ROADWAY (20 FT GAP)", 288, 50, 2.2, 90.0)

    # 2. ZONE 1: BOREWELL & 2" MAINLINE
    # Solar Borewell at (590, 20)
    add_circle("01_BOREWELL_HEAD", 590, 20, 4.0)
    add_circle("01_BOREWELL_HEAD", 590, 20, 2.0)
    # Solar array representation
    add_line("01_BOREWELL_HEAD", 596, 12, 616, 12)
    add_line("01_BOREWELL_HEAD", 616, 12, 616, 28)
    add_line("01_BOREWELL_HEAD", 616, 28, 596, 28)
    add_line("01_BOREWELL_HEAD", 596, 28, 596, 12)
    add_text("01_BOREWELL_HEAD", "SOLAR PV ARRAY (5 HP)", 598, 20, 2.0)
    add_text("01_BOREWELL_HEAD", "BOREWELL HEAD (590, 20)", 570, 14, 2.5)

    # Borewell Tee at (590, 20)
    # South stub capped at (590, 18)
    add_line("02_MAINLINE_2IN_63MM", 590, 20, 590, 18)
    add_cap("07_RISER_VALVES_FITTINGS", 590, 18, 2.0, "S")
    add_text("07_RISER_VALVES_FITTINGS", "2\" End Cap", 593, 17, 1.8)

    # Head unit inline components along North line
    add_valve("01_BOREWELL_HEAD", 590, 30, 2.5, False)
    add_text("01_BOREWELL_HEAD", "2\" NRV", 594, 29, 2.0)
    add_valve("01_BOREWELL_HEAD", 590, 42, 2.5, False)
    add_text("01_BOREWELL_HEAD", "2\" Gate Valve", 594, 41, 2.0)
    # 2" Filter T Type
    add_circle("01_BOREWELL_HEAD", 590, 54, 3.5)
    add_line("01_BOREWELL_HEAD", 590, 54, 596, 54)
    add_circle("01_BOREWELL_HEAD", 596, 54, 2.0)
    add_text("01_BOREWELL_HEAD", "2\" Filter 'T' Type (Disc/Screen)", 598, 53, 2.2)

    # Mainline: Borewell (590, 20) North 80' to Corner Tee (590, 100)
    add_line("02_MAINLINE_2IN_63MM", 590, 20, 590, 100)
    add_text("08_DIMENSIONS_ANNOTATIONS", "80'-0\" (2\" PVC Class 2 / 63mm Mainline)", 592, 70, 2.2, 90.0)

    # Corner Tee at (590, 100)
    # East stub capped at (592, 100)
    add_line("02_MAINLINE_2IN_63MM", 590, 100, 592, 100)
    add_cap("07_RISER_VALVES_FITTINGS", 592, 100, 2.0, "E")
    add_text("07_RISER_VALVES_FITTINGS", "2\" End Cap", 594, 98, 1.8)
    add_circle("07_RISER_VALVES_FITTINGS", 590, 100, 1.5)
    add_text("07_RISER_VALVES_FITTINGS", "2\" Corner Tee (590, 100)", 570, 104, 2.2)

    # Mainline: Corner Tee West 90' to Tee A (500, 100)
    add_line("02_MAINLINE_2IN_63MM", 590, 100, 500, 100)
    add_text("08_DIMENSIONS_ANNOTATIONS", "90'-0\" (2\" PVC Class 2)", 530, 94, 2.2)

    # Tee A at (500, 100)
    add_circle("07_RISER_VALVES_FITTINGS", 500, 100, 2.0)
    add_text("07_RISER_VALVES_FITTINGS", "TEE A (500, 100) - PLOT A CENTER ENTRY", 450, 88, 2.8)

    # Mainline: Tee A West 215' to Tee B (285, 100)
    add_line("02_MAINLINE_2IN_63MM", 500, 100, 285, 100)
    add_text("08_DIMENSIONS_ANNOTATIONS", "215'-0\" (2\" Mainline Under Plot A & Buffer Zone)", 350, 94, 2.2)

    # Tee B at (285, 100)
    add_circle("07_RISER_VALVES_FITTINGS", 285, 100, 2.0)
    add_text("07_RISER_VALVES_FITTINGS", "TEE B (285, 100) - PLOT B ENTRY", 210, 82, 2.8)
    # West stub capped at (283, 100)
    add_line("02_MAINLINE_2IN_63MM", 285, 100, 283, 100)
    add_cap("07_RISER_VALVES_FITTINGS", 283, 100, 2.0, "W")
    add_text("07_RISER_VALVES_FITTINGS", "2\" End Cap", 260, 98, 1.8)

    # 3. ZONE 2: PLOT A CENTER MAINLINE & RISERS
    # Plot A Centerline 2" Mainline: (500, 100) to (500, 245) = 145 ft total
    add_line("02_MAINLINE_2IN_63MM", 500, 100, 500, 245)
    add_cap("07_RISER_VALVES_FITTINGS", 500, 245, 2.0, "N")
    add_text("07_RISER_VALVES_FITTINGS", "2\" Mainline End Cap (500, 245)", 504, 244, 2.0)
    add_text("08_DIMENSIONS_ANNOTATIONS", "145'-0\" CENTER MAINLINE (2\" PVC)", 502, 110, 2.2, 90.0)

    # 4 Overhead Riser Stations on Plot A: A1(130), A2(160), A3(190), A4(220)
    riser_a_y = [130, 160, 190, 220]
    for idx, ry in enumerate(riser_a_y):
        name = f"RISER A{idx+1}"
        # Riser station symbol (concentric circles for vertical riser + overhead tee)
        add_circle("07_RISER_VALVES_FITTINGS", 500, ry, 2.5)
        add_circle("07_RISER_VALVES_FITTINGS", 500, ry, 1.2)
        add_text("07_RISER_VALVES_FITTINGS", f"{name} (500, {ry})", 504, ry + 2, 2.2)
        add_text("07_RISER_VALVES_FITTINGS", "[4ft Double-Tee Riser + 2x 50mm Ball Valves]", 504, ry - 2, 1.8)

        # 1.5" Sublines: 15 ft South and 15 ft North
        # South subline
        add_line("03_SUBLINE_1.5IN_50MM_PLOTA", 500, ry, 500, ry - 15)
        add_valve("07_RISER_VALVES_FITTINGS", 500, ry - 15, 1.8, False)
        add_text("07_RISER_VALVES_FITTINGS", "50mm Flush Valve", 503, ry - 15, 1.6)

        # North subline
        add_line("03_SUBLINE_1.5IN_50MM_PLOTA", 500, ry, 500, ry + 15)
        add_valve("07_RISER_VALVES_FITTINGS", 500, ry + 15, 1.8, False)
        add_text("07_RISER_VALVES_FITTINGS", "50mm Flush Valve", 503, ry + 15, 1.6)

    # Plot A 24 Inline Trenches (spaced every 5 ft along Y = 117.5 to 232.5)
    trench_y = [
        117.5, 122.5, 127.5, # A1-South
        132.5, 137.5, 142.5, # A1-North
        147.5, 152.5, 157.5, # A2-South
        162.5, 167.5, 172.5, # A2-North
        177.5, 182.5, 187.5, # A3-South
        192.5, 197.5, 202.5, # A3-North
        207.5, 212.5, 217.5, # A4-South
        222.5, 227.5, 232.5  # A4-North
    ]

    for t_idx, ty in enumerate(trench_y):
        # Laterals West to 305 and East to 695 (390 ft total per trench)
        add_line("05_LATERALS_16MM_INLINE_PLOTA", 305, ty, 695, ty, "DASHED")
        
        # 50x16x2-way collar (V-connector) at center (500, ty)
        add_circle("07_RISER_VALVES_FITTINGS", 500, ty, 0.8)
        
        # End caps at ends
        add_cap("07_RISER_VALVES_FITTINGS", 305, ty, 1.2, "W")
        add_cap("07_RISER_VALVES_FITTINGS", 695, ty, 1.2, "E")

        # Label some trenches
        if t_idx in (0, 11, 23):
            add_text("05_LATERALS_16MM_INLINE_PLOTA", f"Trench #{t_idx+1}: 16x4x40 Inline (390' L | 125 plants/side)", 515, ty + 0.8, 1.6)

    add_text("05_LATERALS_16MM_INLINE_PLOTA", "24 TRENCHES @ 5'-0\" SPACING (3,000 PLANTS TOTAL)", 600, 242, 2.5)

    # 4. ZONE 3: PLOT B BOUNDARY MAINLINE & RISERS
    # Plot B East-Boundary Mainline: (285, 100) to (285, 340) = 240 ft total
    add_line("02_MAINLINE_2IN_63MM", 285, 100, 285, 340)
    add_cap("07_RISER_VALVES_FITTINGS", 285, 340, 2.0, "N")
    add_text("07_RISER_VALVES_FITTINGS", "2\" Mainline End Cap (285, 340)", 289, 340, 2.0)
    add_text("08_DIMENSIONS_ANNOTATIONS", "240'-0\" EAST BOUNDARY MAINLINE (2\" PVC)", 281, 105, 2.2, 90.0)

    # 4 Overhead Riser Stations on Plot B: B1(124), B2(188), B3(252), B4(316)
    riser_b_y = [124, 188, 252, 316]
    for idx, ry in enumerate(riser_b_y):
        name = f"RISER B{idx+1}"
        add_circle("07_RISER_VALVES_FITTINGS", 285, ry, 2.5)
        add_circle("07_RISER_VALVES_FITTINGS", 285, ry, 1.2)
        add_text("07_RISER_VALVES_FITTINGS", f"{name} (285, {ry})", 289, ry + 2, 2.2)
        add_text("07_RISER_VALVES_FITTINGS", "[4ft Riser + 2x 40mm Ball Valves]", 289, ry - 2, 1.8)

        # 1.25" Sublines: 32 ft South and 32 ft North
        # South subline
        add_line("04_SUBLINE_1.25IN_40MM_PLOTB", 285, ry, 285, ry - 32)
        add_valve("07_RISER_VALVES_FITTINGS", 285, ry - 32, 1.8, False)
        add_text("07_RISER_VALVES_FITTINGS", "40mm Flush Valve", 289, ry - 32, 1.6)

        # North subline
        add_line("04_SUBLINE_1.25IN_40MM_PLOTB", 285, ry, 285, ry + 32)
        add_valve("07_RISER_VALVES_FITTINGS", 285, ry + 32, 1.8, False)
        add_text("07_RISER_VALVES_FITTINGS", "40mm Flush Valve", 289, ry + 32, 1.6)

    # Plot B 32 Online Rows (spaced every 8 ft along Y = 96 to 344)
    row_b_y = [
        96, 104, 112, 120,   # B1-South
        128, 136, 144, 152,  # B1-North
        160, 168, 176, 184,  # B2-South
        192, 200, 208, 216,  # B2-North
        224, 232, 240, 248,  # B3-South
        256, 264, 272, 280,  # B3-North
        288, 296, 304, 312,  # B4-South
        320, 328, 336, 344   # B4-North
    ]

    for r_idx, ry in enumerate(row_b_y):
        # Plain 16mm Pipe runs WEST only: from 285 to 120 (165 ft)
        add_line("06_LATERALS_16MM_ONLINE_PLOTB", 120, ry, 285, ry)
        
        # 40x16x1-way collar at (285, ry)
        add_circle("07_RISER_VALVES_FITTINGS", 285, ry, 0.8)
        
        # End cap at West end (120, ry)
        add_cap("07_RISER_VALVES_FITTINGS", 120, ry, 1.2, "W")

        # Represent punched tunning drippers every 7 ft
        for px in range(120 + 7, 285, 28): # show every 4th dripper for clean drawing
            add_circle("06_LATERALS_16MM_ONLINE_PLOTB", px, ry, 0.4)

        if r_idx in (0, 15, 31):
            add_text("06_LATERALS_16MM_ONLINE_PLOTB", f"Row #{r_idx+1}: 16mm Plain (165' L | 24 Drippers @ 7' Grid)", 130, ry + 1.2, 1.6)

    add_text("06_LATERALS_16MM_ONLINE_PLOTB", "32 ROWS @ 8'-0\" SPACING (750 PLANTS TOTAL)", 130, 348, 2.5)

    # 5. NORTH ARROW & COMPASS
    nx, ny = 660, 50
    add_circle("08_DIMENSIONS_ANNOTATIONS", nx, ny, 12.0)
    add_line("08_DIMENSIONS_ANNOTATIONS", nx, ny - 10, nx, ny + 10)
    add_line("08_DIMENSIONS_ANNOTATIONS", nx - 10, ny, nx + 10, ny)
    add_line("08_DIMENSIONS_ANNOTATIONS", nx, ny + 10, nx - 3, ny + 5)
    add_line("08_DIMENSIONS_ANNOTATIONS", nx, ny + 10, nx + 3, ny + 5)
    add_text("08_DIMENSIONS_ANNOTATIONS", "N", nx - 1.5, ny + 12, 4.0)
    add_text("08_DIMENSIONS_ANNOTATIONS", "E", nx + 12, ny - 1.5, 3.0)
    add_text("08_DIMENSIONS_ANNOTATIONS", "S", nx - 1.5, ny - 16, 3.0)
    add_text("08_DIMENSIONS_ANNOTATIONS", "W", nx - 16, ny - 1.5, 3.0)

    # 6. TITLE BLOCK & LEGEND (CAD SHEET 1)
    # Border
    bx1, by1 = 80, 0
    bx2, by2 = 720, 380
    add_line("00_BORDER_TITLEBLOCK", bx1, by1, bx2, by1)
    add_line("00_BORDER_TITLEBLOCK", bx2, by1, bx2, by2)
    add_line("00_BORDER_TITLEBLOCK", bx2, by2, bx1, by2)
    add_line("00_BORDER_TITLEBLOCK", bx1, by2, bx1, by1)

    # Title block inner box
    add_line("00_BORDER_TITLEBLOCK", 420, 10, 710, 10)
    add_line("00_BORDER_TITLEBLOCK", 710, 10, 710, 75)
    add_line("00_BORDER_TITLEBLOCK", 710, 75, 420, 75)
    add_line("00_BORDER_TITLEBLOCK", 420, 75, 420, 10)
    add_line("00_BORDER_TITLEBLOCK", 420, 48, 710, 48)

    add_text("08_DIMENSIONS_ANNOTATIONS", "AGRICULTURAL DRIP IRRIGATION ENGINEERING MASTER BLUEPRINT", 425, 64, 3.2)
    add_text("08_DIMENSIONS_ANNOTATIONS", "PROJECT: 2-ACRE MORINGA COMMERCIAL ORCHARD", 425, 54, 2.5)
    add_text("08_DIMENSIONS_ANNOTATIONS", "ZONE 1: 5HP Solar Borewell & 2\" (63mm) Mainline Network", 425, 38, 2.0)
    add_text("08_DIMENSIONS_ANNOTATIONS", "ZONE 2: Plot A (1 Acre PKM-1, 3x5ft, 24 Inline Trenches, 3,000 Plants)", 425, 30, 2.0)
    add_text("08_DIMENSIONS_ANNOTATIONS", "ZONE 3: Plot B (1 Acre Bhagya, 7x8ft, 32 Online Rows, 750 Plants)", 425, 22, 2.0)
    add_text("08_DIMENSIONS_ANNOTATIONS", "SCALE: 1 CAD Unit = 1 Foot | SHEET 1 OF 2 | REV: 1.0 (APPROVED)", 425, 14, 2.0)

    # Compile DXF
    dxf_header = """0
SECTION
2
HEADER
9
$ACADVER
1
AC1015
9
$INSUNITS
70
2
0
ENDSEC
0
SECTION
2
TABLES
0
TABLE
2
LTYPE
70
2
0
LTYPE
2
CONTINUOUS
70
0
3
Solid line
72
65
73
0
40
0.0
0
LTYPE
2
DASHED
70
0
3
Dashed __ __ __
72
65
73
2
40
4.0
49
3.0
49
-1.0
0
ENDTAB
0
TABLE
2
LAYER
70
9
0
LAYER
2
00_BORDER_TITLEBLOCK
70
0
62
8
6
CONTINUOUS
0
LAYER
2
01_BOREWELL_HEAD
70
0
62
7
6
CONTINUOUS
0
LAYER
2
02_MAINLINE_2IN_63MM
70
0
62
5
6
CONTINUOUS
0
LAYER
2
03_SUBLINE_1.5IN_50MM_PLOTA
70
0
62
3
6
CONTINUOUS
0
LAYER
2
04_SUBLINE_1.25IN_40MM_PLOTB
70
0
62
30
6
CONTINUOUS
0
LAYER
2
05_LATERALS_16MM_INLINE_PLOTA
70
0
62
4
6
DASHED
0
LAYER
2
06_LATERALS_16MM_ONLINE_PLOTB
70
0
62
6
6
CONTINUOUS
0
LAYER
2
07_RISER_VALVES_FITTINGS
70
0
62
1
6
CONTINUOUS
0
LAYER
2
08_DIMENSIONS_ANNOTATIONS
70
0
62
2
6
CONTINUOUS
0
ENDTAB
0
ENDSEC
0
SECTION
2
BLOCKS
0
ENDSEC
0
SECTION
2
ENTITIES
"""
    dxf_footer = """0
ENDSEC
0
EOF"""

    full_dxf = dxf_header + "\n".join(entities) + "\n" + dxf_footer
    with open(filename, "w") as f:
        f.write(full_dxf)
    print(f"Master DXF created: {filename} ({len(entities)} entities)")

def write_riser_detail_dxf(filename):
    entities = []

    def add_line(layer, x1, y1, x2, y2, linetype="BYLAYER"):
        entities.append(f"""0
LINE
8
{layer}
6
{linetype}
10
{x1:.3f}
20
{y1:.3f}
30
0.0
11
{x2:.3f}
21
{y2:.3f}
31
0.0""")

    def add_circle(layer, cx, cy, radius):
        entities.append(f"""0
CIRCLE
8
{layer}
10
{cx:.3f}
20
{cy:.3f}
30
0.0
40
{radius:.3f}""")

    def add_text(layer, text, x, y, height=0.25, rotation=0.0):
        entities.append(f"""0
TEXT
8
{layer}
10
{x:.3f}
20
{y:.3f}
30
0.0
40
{height:.3f}
50
{rotation:.1f}
1
{text}""")

    # Side Elevation Cross-Section: 1 CAD Unit = 1 Foot
    # Y = 0.0 is Finished Ground Level (FGL)
    # Trench bottom is Y = -2.5 (mainline) and Y = -2.0 (subline)
    # Overhead riser goes up to Y = +4.0

    # 1. GROUND PROFILE & TRENCH CUTS
    add_line("08_DIMENSIONS_ANNOTATIONS", -15.0, 0.0, 15.0, 0.0, "DASHED")
    add_text("08_DIMENSIONS_ANNOTATIONS", "FINISHED GROUND LEVEL (ELEV. 0.00')", -14.5, 0.2, 0.35)

    # Mainline Trench Profile: Center trench (-1.5 to +1.5, depth -2.5)
    add_line("08_DIMENSIONS_ANNOTATIONS", -1.5, 0.0, -1.5, -2.5)
    add_line("08_DIMENSIONS_ANNOTATIONS", -1.5, -2.5, 1.5, -2.5)
    add_line("08_DIMENSIONS_ANNOTATIONS", 1.5, -2.5, 1.5, 0.0)
    add_text("08_DIMENSIONS_ANNOTATIONS", "MAINLINE TRENCH (-2.5' DEPTH)", -1.4, -2.8, 0.3)

    # Subline Trenches North & South (-2.0' depth)
    add_line("08_DIMENSIONS_ANNOTATIONS", -12.0, 0.0, -12.0, -2.0)
    add_line("08_DIMENSIONS_ANNOTATIONS", -12.0, -2.0, -2.0, -2.0)
    add_line("08_DIMENSIONS_ANNOTATIONS", -2.0, -2.0, -2.0, 0.0)
    add_text("08_DIMENSIONS_ANNOTATIONS", "SOUTH SUBLINE TRENCH (-2.0' DEPTH)", -11.5, -2.3, 0.3)

    add_line("08_DIMENSIONS_ANNOTATIONS", 2.0, 0.0, 2.0, -2.0)
    add_line("08_DIMENSIONS_ANNOTATIONS", 2.0, -2.0, 12.0, -2.0)
    add_line("08_DIMENSIONS_ANNOTATIONS", 12.0, -2.0, 12.0, 0.0)
    add_text("08_DIMENSIONS_ANNOTATIONS", "NORTH SUBLINE TRENCH (-2.0' DEPTH)", 2.5, -2.3, 0.3)

    # 2. BURIED 2" MAINLINE & TEE
    # Mainline pipe running into page at (0, -2.2)
    add_circle("02_MAINLINE_2IN_63MM", 0.0, -2.2, 0.25)
    add_text("02_MAINLINE_2IN_63MM", "2\" Mainline Pipe (Flows through)", 0.4, -2.2, 0.25)

    # Buried 2" Tee branch pointing UP
    add_line("02_MAINLINE_2IN_63MM", -0.2, -2.2, -0.2, -1.7)
    add_line("02_MAINLINE_2IN_63MM", 0.2, -2.2, 0.2, -1.7)

    # 3. 2" VERTICAL PVC RISER PIPE (+4.0' above ground)
    add_line("02_MAINLINE_2IN_63MM", -0.18, -1.7, -0.18, 4.0)
    add_line("02_MAINLINE_2IN_63MM", 0.18, -1.7, 0.18, 4.0)
    add_text("02_MAINLINE_2IN_63MM", "2\" Vertical Riser Pipe (4'-0\" above grade)", 0.3, 2.0, 0.3)

    # 4. OVERHEAD 2" DOUBLE-TEE at +4.0'
    add_circle("07_RISER_VALVES_FITTINGS", 0.0, 4.0, 0.35)
    add_text("07_RISER_VALVES_FITTINGS", "2\" Overhead Double Tee (+4.00' Elev.)", -3.5, 4.6, 0.35)

    # 5. SOUTH BRANCH (LEFT)
    # Horizontal run left
    add_line("07_RISER_VALVES_FITTINGS", 0.0, 4.15, -2.5, 4.15)
    add_line("07_RISER_VALVES_FITTINGS", 0.0, 3.85, -2.5, 3.85)

    # Reducer (2" to 1.5" for Plot A / 2" to 1.25" for Plot B)
    add_line("07_RISER_VALVES_FITTINGS", -0.8, 4.25, -1.2, 4.1)
    add_line("07_RISER_VALVES_FITTINGS", -0.8, 3.75, -1.2, 3.9)
    add_text("07_RISER_VALVES_FITTINGS", "2\"x1.5\" Reducer", -1.8, 4.35, 0.25)

    # 50mm Plain Ball Valve (with handle)
    add_line("07_RISER_VALVES_FITTINGS", -1.6, 4.25, -2.2, 3.75)
    add_line("07_RISER_VALVES_FITTINGS", -1.6, 3.75, -2.2, 4.25)
    add_circle("07_RISER_VALVES_FITTINGS", -1.9, 4.0, 0.1)
    add_line("07_RISER_VALVES_FITTINGS", -1.9, 4.0, -1.9, 4.6)
    add_line("07_RISER_VALVES_FITTINGS", -1.9, 4.6, -2.5, 4.6)
    add_text("07_RISER_VALVES_FITTINGS", "50mm Plain Ball Valve (South Control)", -4.5, 5.0, 0.28)

    # South 90 Elbow turning DOWN at -2.5
    add_circle("07_RISER_VALVES_FITTINGS", -2.5, 4.0, 0.2)
    # Vertical Drop Pipe (4ft drop from +4.0 down to -1.8)
    add_line("03_SUBLINE_1.5IN_50MM_PLOTA", -2.6, 4.0, -2.6, -1.8)
    add_line("03_SUBLINE_1.5IN_50MM_PLOTA", -2.4, 4.0, -2.4, -1.8)
    add_text("03_SUBLINE_1.5IN_50MM_PLOTA", "1.5\" Vertical Drop Pipe (6.0' total drop)", -4.8, 1.0, 0.28)

    # South 90 Elbow turning HORIZONTAL at -1.8 into trench
    add_circle("07_RISER_VALVES_FITTINGS", -2.5, -1.8, 0.2)
    # Buried Subline running South
    add_line("03_SUBLINE_1.5IN_50MM_PLOTA", -2.5, -1.7, -11.0, -1.7)
    add_line("03_SUBLINE_1.5IN_50MM_PLOTA", -2.5, -1.9, -11.0, -1.9)
    add_text("03_SUBLINE_1.5IN_50MM_PLOTA", "Buried 1.5\" (50mm) Subline Arm (15ft South)", -9.5, -1.4, 0.28)

    # Flush Valve at terminal end (-11.0, -1.8)
    add_circle("07_RISER_VALVES_FITTINGS", -11.0, -1.8, 0.3)
    add_line("07_RISER_VALVES_FITTINGS", -11.0, -1.8, -11.0, 0.2)
    add_text("07_RISER_VALVES_FITTINGS", "50mm Flush Valve in Valve Box", -13.5, 0.5, 0.28)

    # 6. NORTH BRANCH (RIGHT)
    # Horizontal run right
    add_line("07_RISER_VALVES_FITTINGS", 0.0, 4.15, 2.5, 4.15)
    add_line("07_RISER_VALVES_FITTINGS", 0.0, 3.85, 2.5, 3.85)

    # Reducer
    add_line("07_RISER_VALVES_FITTINGS", 0.8, 4.25, 1.2, 4.1)
    add_line("07_RISER_VALVES_FITTINGS", 0.8, 3.75, 1.2, 3.9)
    add_text("07_RISER_VALVES_FITTINGS", "2\"x1.5\" Reducer", 0.6, 4.35, 0.25)

    # 50mm Plain Ball Valve (with handle)
    add_line("07_RISER_VALVES_FITTINGS", 1.6, 4.25, 2.2, 3.75)
    add_line("07_RISER_VALVES_FITTINGS", 1.6, 3.75, 2.2, 4.25)
    add_circle("07_RISER_VALVES_FITTINGS", 1.9, 4.0, 0.1)
    add_line("07_RISER_VALVES_FITTINGS", 1.9, 4.0, 1.9, 4.6)
    add_line("07_RISER_VALVES_FITTINGS", 1.9, 4.6, 2.5, 4.6)
    add_text("07_RISER_VALVES_FITTINGS", "50mm Plain Ball Valve (North Control)", 1.2, 5.0, 0.28)

    # North 90 Elbow turning DOWN at +2.5
    add_circle("07_RISER_VALVES_FITTINGS", 2.5, 4.0, 0.2)
    # Vertical Drop Pipe
    add_line("03_SUBLINE_1.5IN_50MM_PLOTA", 2.4, 4.0, 2.4, -1.8)
    add_line("03_SUBLINE_1.5IN_50MM_PLOTA", 2.6, 4.0, 2.6, -1.8)
    add_text("03_SUBLINE_1.5IN_50MM_PLOTA", "1.5\" Vertical Drop Pipe", 2.8, 1.0, 0.28)

    # North 90 Elbow turning HORIZONTAL at -1.8 into trench
    add_circle("07_RISER_VALVES_FITTINGS", 2.5, -1.8, 0.2)
    # Buried Subline running North
    add_line("03_SUBLINE_1.5IN_50MM_PLOTA", 2.5, -1.7, 11.0, -1.7)
    add_line("03_SUBLINE_1.5IN_50MM_PLOTA", 2.5, -1.9, 11.0, -1.9)
    add_text("03_SUBLINE_1.5IN_50MM_PLOTA", "Buried 1.5\" (50mm) Subline Arm (15ft North)", 3.2, -1.4, 0.28)

    # Flush Valve at terminal end (11.0, -1.8)
    add_circle("07_RISER_VALVES_FITTINGS", 11.0, -1.8, 0.3)
    add_line("07_RISER_VALVES_FITTINGS", 11.0, -1.8, 11.0, 0.2)
    add_text("07_RISER_VALVES_FITTINGS", "50mm Flush Valve in Valve Box", 9.0, 0.5, 0.28)

    # 7. ELEVATION CALLOUTS & DIMENSIONS
    add_line("08_DIMENSIONS_ANNOTATIONS", -4.0, 0.0, -4.0, 4.0)
    add_line("08_DIMENSIONS_ANNOTATIONS", -4.3, 4.0, -3.7, 4.0)
    add_line("08_DIMENSIONS_ANNOTATIONS", -4.3, 0.0, -3.7, 0.0)
    add_text("08_DIMENSIONS_ANNOTATIONS", "+4'-0\" OVERHEAD WAIST HEIGHT", -8.5, 3.7, 0.3)

    add_line("08_DIMENSIONS_ANNOTATIONS", -4.0, 0.0, -4.0, -2.5)
    add_line("08_DIMENSIONS_ANNOTATIONS", -4.3, -2.5, -3.7, -2.5)
    add_text("08_DIMENSIONS_ANNOTATIONS", "-2'-6\" TRENCH DEPTH", -8.0, -2.6, 0.3)

    # Detail Title Block
    add_text("08_DIMENSIONS_ANNOTATIONS", "DETAIL VIEW: 4-FOOT OVERHEAD DOUBLE-TEE RISER MANIFOLD", -10.0, 6.2, 0.45)
    add_text("08_DIMENSIONS_ANNOTATIONS", "ELEVATION CROSS-SECTION LOOKING EAST | SHEET 2 OF 2", -10.0, 5.7, 0.32)
    add_text("08_DIMENSIONS_ANNOTATIONS", "NOTE: APPLIES TO RISERS A1-A4 (50mm) AND B1-B4 (40mm with 2\"x1.25\" Reducer)", -10.0, 5.3, 0.25)

    dxf_header = """0
SECTION
2
HEADER
9
$ACADVER
1
AC1015
9
$INSUNITS
70
2
0
ENDSEC
0
SECTION
2
TABLES
0
TABLE
2
LTYPE
70
2
0
LTYPE
2
CONTINUOUS
70
0
3
Solid line
72
65
73
0
40
0.0
0
LTYPE
2
DASHED
70
0
3
Dashed __ __ __
72
65
73
2
40
2.0
49
1.5
49
-0.5
0
ENDTAB
0
TABLE
2
LAYER
70
7
0
LAYER
2
00_BORDER_TITLEBLOCK
70
0
62
8
6
CONTINUOUS
0
LAYER
2
02_MAINLINE_2IN_63MM
70
0
62
5
6
CONTINUOUS
0
LAYER
2
03_SUBLINE_1.5IN_50MM_PLOTA
70
0
62
3
6
CONTINUOUS
0
LAYER
2
04_SUBLINE_1.25IN_40MM_PLOTB
70
0
62
30
6
CONTINUOUS
0
LAYER
2
07_RISER_VALVES_FITTINGS
70
0
62
1
6
CONTINUOUS
0
LAYER
2
08_DIMENSIONS_ANNOTATIONS
70
0
62
2
6
CONTINUOUS
0
ENDTAB
0
ENDSEC
0
SECTION
2
BLOCKS
0
ENDSEC
0
SECTION
2
ENTITIES
"""
    dxf_footer = """0
ENDSEC
0
EOF"""

    full_dxf = dxf_header + "\n".join(entities) + "\n" + dxf_footer
    with open(filename, "w") as f:
        f.write(full_dxf)
    print(f"Riser Detail DXF created: {filename} ({len(entities)} entities)")

if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    master_dxf = os.path.join(out_dir, "Moringa_2Acre_Irrigation_Master.dxf")
    detail_dxf = os.path.join(out_dir, "Riser_Manifold_Detail.dxf")
    write_master_dxf(master_dxf)
    write_riser_detail_dxf(detail_dxf)
