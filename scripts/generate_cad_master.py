import os
import sys

def write_master_dxf(filename):
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

    # 1. FIELD BOUNDARIES
    # Plot A boundary
    add_line("08_DIMENSIONS_ANNOTATIONS", 305, 115, 695, 115, "DASHED")
    add_line("08_DIMENSIONS_ANNOTATIONS", 695, 115, 695, 235, "DASHED")
    add_line("08_DIMENSIONS_ANNOTATIONS", 695, 235, 305, 235, "DASHED")
    add_line("08_DIMENSIONS_ANNOTATIONS", 305, 235, 305, 115, "DASHED")
    add_text("08_DIMENSIONS_ANNOTATIONS", "PLOT A: PKM-1 MORINGA (1 ACRE | 3ft x 5ft | 3,000 TREES)", 310, 240, 3.5)

    # Plot B boundary (STARTS AT Y=124, 24 FT NORTH OF TEE B)
    add_line("08_DIMENSIONS_ANNOTATIONS", 120, 124, 285, 124, "DASHED")
    add_line("08_DIMENSIONS_ANNOTATIONS", 285, 124, 285, 380, "DASHED")
    add_line("08_DIMENSIONS_ANNOTATIONS", 285, 380, 120, 380, "DASHED")
    add_line("08_DIMENSIONS_ANNOTATIONS", 120, 380, 120, 124, "DASHED")
    add_text("08_DIMENSIONS_ANNOTATIONS", "PLOT B: BHAGYA MORINGA (1 ACRE | 7ft x 8ft | 750 TREES | STARTS 24FT NORTH)", 125, 385, 3.5)

    # 2. BOREWELL & MAINLINE
    add_circle("01_BOREWELL_HEAD", 590, 20, 4.0)
    add_circle("01_BOREWELL_HEAD", 590, 20, 2.0)
    add_text("01_BOREWELL_HEAD", "5HP SOLAR BOREWELL HEAD (590, 20)", 560, 14, 2.5)

    # South stub capped
    add_line("02_MAINLINE_2IN_63MM", 590, 20, 590, 18)
    add_line("07_RISER_VALVES_FITTINGS", 588, 18, 592, 18)

    # Mainline North 80 ft to Corner Tee
    add_line("02_MAINLINE_2IN_63MM", 590, 20, 590, 100)
    add_text("08_DIMENSIONS_ANNOTATIONS", "80'-0\" (2\" PVC CLASS 2)", 592, 60, 2.2, 90.0)

    # Corner Tee (590, 100) with East stub capped
    add_circle("07_RISER_VALVES_FITTINGS", 590, 100, 2.0)
    add_line("02_MAINLINE_2IN_63MM", 590, 100, 592, 100)
    add_line("07_RISER_VALVES_FITTINGS", 592, 98, 592, 102)

    # West 90 ft to Tee A (500, 100)
    add_line("02_MAINLINE_2IN_63MM", 590, 100, 500, 100)
    add_text("08_DIMENSIONS_ANNOTATIONS", "90'-0\" (2\" PVC CLASS 2)", 535, 94, 2.2)

    # Tee A at (500, 100)
    add_circle("07_RISER_VALVES_FITTINGS", 500, 100, 2.0)
    add_text("07_RISER_VALVES_FITTINGS", "TEE A (500, 100)", 480, 88, 2.5)

    # West 215 ft to Tee B (285, 100)
    add_line("02_MAINLINE_2IN_63MM", 500, 100, 285, 100)
    add_text("08_DIMENSIONS_ANNOTATIONS", "215'-0\" (2\" MAINLINE UNDER PLOT A & ROADWAY)", 330, 94, 2.2)

    # Tee B at (285, 100) with West stub capped
    add_circle("07_RISER_VALVES_FITTINGS", 285, 100, 2.0)
    add_line("02_MAINLINE_2IN_63MM", 285, 100, 283, 100)
    add_line("07_RISER_VALVES_FITTINGS", 283, 98, 283, 102)
    add_text("07_RISER_VALVES_FITTINGS", "TEE B (285, 100)", 250, 88, 2.5)

    # 3. PLOT B 2" MAINLINE & FIXED TERMINATION AT RISER B4
    # 24 ft Bare ground run North: from Tee B (285, 100) to Y=124
    add_line("02_MAINLINE_2IN_63MM", 285, 100, 285, 124)
    add_text("08_DIMENSIONS_ANNOTATIONS", "24'-0\" BARE GROUND (NO ROWS)", 287, 110, 1.8, 90.0)

    # 2" Mainline runs North from Y=124 to Riser B4 at Y=348 (offset 248 ft North of Tee B)
    # AND TERMINATES AT RISER B4!
    add_line("02_MAINLINE_2IN_63MM", 285, 124, 285, 348)
    add_line("07_RISER_VALVES_FITTINGS", 283, 348, 287, 348)
    add_text("07_RISER_VALVES_FITTINGS", "2\" MAINLINE TERMINATES AT RISER B4 (2\" END CAP)", 289, 348, 2.2)

    # Above Riser B4, ONLY 1.25" Subline continues 32 ft North to Y=380
    add_line("04_SUBLINE_1.25IN_40MM_PLOTB", 285, 348, 285, 380)
    add_circle("07_RISER_VALVES_FITTINGS", 285, 380, 1.5)
    add_text("07_RISER_VALVES_FITTINGS", "40mm Flush Valve (Top Terminal)", 289, 380, 1.8)

    # Subline 1.25" full run from Y=124 to Y=380 (256 ft total)
    add_line("04_SUBLINE_1.25IN_40MM_PLOTB", 285, 124, 285, 348)
    add_circle("07_RISER_VALVES_FITTINGS", 285, 124, 1.5)
    add_text("07_RISER_VALVES_FITTINGS", "40mm Flush Valve (Bottom Terminal)", 289, 124, 1.8)

    # 4 Risers on Plot B (B1 at 156, B2 at 220, B3 at 284, B4 at 348)
    for ry, rname in [(156, "RISER B1"), (220, "RISER B2"), (284, "RISER B3"), (348, "RISER B4")]:
        add_circle("07_RISER_VALVES_FITTINGS", 285, ry, 2.5)
        add_circle("07_RISER_VALVES_FITTINGS", 285, ry, 1.2)
        add_text("07_RISER_VALVES_FITTINGS", f"{rname} (Y={ry}')", 289, ry + 2, 2.0)

    # Plot B 32 Rows (Westward only, 165 ft run from 285 to 120)
    for r in range(32):
        row_y = 128 + r * 8  # 32 rows spaced 8 ft apart
        add_line("06_LATERALS_16MM_ONLINE_PLOTB", 120, row_y, 285, row_y)
        add_circle("07_RISER_VALVES_FITTINGS", 285, row_y, 0.8)
        add_line("07_RISER_VALVES_FITTINGS", 120, row_y - 1, 120, row_y + 1)

    # 4. PLOT A CENTER MAINLINE & RISERS
    # Mainline runs North 145 ft from (500, 100) to (500, 245)
    add_line("02_MAINLINE_2IN_63MM", 500, 100, 500, 245)
    add_line("07_RISER_VALVES_FITTINGS", 498, 245, 502, 245)
    add_text("07_RISER_VALVES_FITTINGS", "2\" MAINLINE END CAP (500, 245)", 504, 245, 2.0)

    # 1.5" Sublines from Y=115 to Y=235 (120 ft total)
    add_line("03_SUBLINE_1.5IN_50MM_PLOTA", 500, 115, 500, 235)
    add_circle("07_RISER_VALVES_FITTINGS", 500, 115, 1.5)
    add_circle("07_RISER_VALVES_FITTINGS", 500, 235, 1.5)

    # 4 Risers on Plot A (A1 at 130, A2 at 160, A3 at 190, A4 at 220)
    for ry, rname in [(130, "RISER A1"), (160, "RISER A2"), (190, "RISER A3"), (220, "RISER A4")]:
        add_circle("07_RISER_VALVES_FITTINGS", 500, ry, 2.5)
        add_circle("07_RISER_VALVES_FITTINGS", 500, ry, 1.2)
        add_text("07_RISER_VALVES_FITTINGS", f"{rname} (Y={ry}')", 504, ry + 2, 2.0)

    # Plot A 24 Trenches (East & West 195 ft: X=305 to 695)
    for t in range(24):
        ty = 117.5 + t * 5
        add_line("05_LATERALS_16MM_INLINE_PLOTA", 305, ty, 695, ty)
        add_circle("07_RISER_VALVES_FITTINGS", 500, ty, 0.8)
        add_line("07_RISER_VALVES_FITTINGS", 305, ty - 1, 305, ty + 1)
        add_line("07_RISER_VALVES_FITTINGS", 695, ty - 1, 695, ty + 1)

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
7
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
7
6
CONTINUOUS
0
LAYER
2
03_SUBLINE_1.5IN_50MM_PLOTA
70
0
62
4
6
CONTINUOUS
0
LAYER
2
04_SUBLINE_1.25IN_40MM_PLOTB
70
0
62
4
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
CONTINUOUS
0
LAYER
2
06_LATERALS_16MM_ONLINE_PLOTB
70
0
62
4
6
CONTINUOUS
0
LAYER
2
07_RISER_VALVES_FITTINGS
70
0
62
7
6
CONTINUOUS
0
LAYER
2
08_DIMENSIONS_ANNOTATIONS
70
0
62
4
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

    with open(filename, "w") as f:
        f.write(dxf_header + "\n".join(entities) + "\n" + dxf_footer)
    print(f"Master DXF created: {filename}")

if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    master_dxf = os.path.join(out_dir, "Moringa_2Acre_Irrigation_Master.dxf")
    write_master_dxf(master_dxf)
