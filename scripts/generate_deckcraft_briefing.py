import os
import sys
import json
import subprocess

def create_presentation(out_dir):
    pptx_path = os.path.join(out_dir, "Irrigation_Execution_Briefing.pptx")
    pdf_path = os.path.join(out_dir, "Irrigation_Execution_Briefing.pdf")

    deckcraft_cli = r"C:\Program Files\DeckCraft\deckcraft-cli.exe"

    slides = [
        {
            "layout": "title",
            "title": "2-Acre Moringa Drip Irrigation",
            "body": "Stage-by-Stage Engineering Execution Briefing\nAuthor: ArtCraft Suite (DeckCraft & CADCraft)\nProject Scope: Solar Borewell Head, 2\" Mainline, 8 Risers, 56 Laterals"
        },
        {
            "layout": "titleAndContent",
            "title": "Stage 1: Borewell Head & 2\" Mainline Routing",
            "body": "• Solar Borewell Head Unit at (590, 20): 5 HP pump delivery with 2\" NRV, Gate Valve, and 2\" T-Type Filter.\n• Northward Mainline (80'-0\"): 2\" PVC Class 2 from Borewell to Corner Tee (590, 100).\n• Westward Mainline (90'-0\"): From Corner Tee to Tee A (500, 100) — Plot A Center Entry.\n• Inter-Plot Mainline (215'-0\"): Runs West from Tee A under Plot A & 25ft buffer road to Tee B (285, 100).\n• Trench Depth: Minimum 2'-6\" deep with 2\" sand bed and 24-hr solvent cement cure."
        },
        {
            "layout": "titleAndContent",
            "title": "Stage 2: Plot A Risers & 24 Inline Trenches (PKM-1)",
            "body": "• Center Mainline: Runs North 145'-0\" from Tee A to End Cap (500, 245).\n• 4 Overhead Riser Stations: A1 (30'), A2 (60'), A3 (90'), A4 (120') with 4ft double-tee manifold.\n• Subline Network: 1.5\" (50mm) PVC running 15ft South and 15ft North from each station (8 arms = 120 ft total).\n• 24 Active Trenches: Spaced 5ft apart with 50x16x2-way take-off collars (V-connectors).\n• Laterals: 16x4x40 Inline Pipe (2,926m total) running 195ft East and 195ft West for 3,000 PKM-1 trees."
        },
        {
            "layout": "titleAndContent",
            "title": "Stage 3: Plot B Risers & 32 Online Rows (Bhagya)",
            "body": "• East-Boundary Mainline: Runs North 240'-0\" from Tee B along Plot B edge to End Cap (285, 340).\n• 4 Overhead Riser Stations: B1 (24'), B2 (88'), B3 (152'), B4 (216') with 2\"x1.25\" reducers.\n• Subline Network: 1.25\" (40mm) PVC running 32ft South and 32ft North from each station (8 arms = 256 ft total).\n• 32 Active Rows: Spaced 8ft apart with 40x16x1-way TF collars pointing West only.\n• Plain Pipe & Punching: 16mm Plain Pipe (1,610m) with 768 Tunning Drippers punched every 7ft (750 trees)."
        },
        {
            "layout": "titleAndContent",
            "title": "Stage 4: Systematic Flushing & Pressure Testing",
            "body": "• Phase A — Mainline Flush: Open 2\" end caps at (500, 245) and (285, 340) for 5 mins to clear construction sand.\n• Phase B — Subline Flush: Close mainline; open all 16 flush valves (50mm & 40mm) until discharge runs clear.\n• Phase C — Lateral Flush: Remove all 80 lateral endcaps (48 in Plot A + 32 in Plot B) for 3 mins.\n• Phase D — Pressure Test: Hold 2.5 kg/cm² test pressure for 60 mins; verify zero joint weeping and uniform emitter discharge."
        },
        {
            "layout": "titleAndContent",
            "title": "Stage 5: Commissioning, Flow Audit & Handover",
            "body": "• Emitter Uniformity Audit: Catch-can sampling across 20 points per zone; target Christiansen Uniformity > 92%.\n• Daily Irrigation Regimen: Plot A (3,000 plants @ 4 LPH = 12,000 LPH); Plot B (750 plants @ 35 LPH = 26,250 LPH peak).\n• Zone Rotation: Rotate irrigation between Zone 2 and Zone 3 to balance solar pump curve throughout peak sunlight hours.\n• Maintenance Protocol: Daily filter purge, weekly disc washing, monthly flush valve blow-out."
        }
    ]

    cmd_args = [deckcraft_cli, "run"]
    for s in slides:
        cmd_args.extend(["--cmd", "slide.new=" + json.dumps(s)])
    cmd_args.extend(["--save", pptx_path])

    res = subprocess.run(cmd_args, capture_output=True, text=True)
    if res.returncode != 0:
        print("DeckCraft run failed:", res.stderr)
        return False
    print(f"Presentation saved: {pptx_path}")

    # Convert to PDF
    res2 = subprocess.run([deckcraft_cli, "convert", pptx_path, pdf_path], capture_output=True, text=True)
    if res2.returncode != 0:
        print("DeckCraft convert failed:", res2.stderr)
        return False
    print(f"Presentation converted to PDF: {pdf_path}")
    return True

if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    create_presentation(out_dir)
