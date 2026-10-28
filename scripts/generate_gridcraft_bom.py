import os
import sys
import json
import subprocess

def build_gridcraft_script(jsonl_path, xlsx_path):
    commands = []

    def cmd(name, params=None):
        if params is None:
            return {"command": name}
        return {"command": name, "params": params}

    # 1. New File
    commands.append(cmd("file.new"))
    commands.append(cmd("sheet.rename", {"name": "Master_BOM"}))

    # Sheet 1: Master_BOM
    master_headers = [
        ["2-ACRE MORINGA DRIP IRRIGATION PROJECT — MASTER BILL OF MATERIALS (BOM) & COST SCHEDULE"],
        ["Client: 2-Acre Moringa Commercial Orchard | Standard: IS 12786 / IS 4985 | Date: October 2026"],
        [],
        ["Item #", "Category", "Item Description & Specification", "Unit", "Ordered Qty", "Planned Usage", "Spare Qty", "Unit Rate (INR)", "Total Amount (INR)", "Application / Location"]
    ]

    master_rows = [
        # PVC Pipes & Fittings
        [1, "PVC Pipes", "2\" (63mm) PVC Pipe Class 2 (6 kg/cm2, 20ft length)", "Length", 45, 37, "=E5-F5", 420.00, "=E5*H5", "Zone 1 Mainline network (730 ft used)"],
        [2, "PVC Fittings", "2\" PVC 90° Elbow", "Nos", 30, 18, "=E6-F6", 45.00, "=E6*H6", "Mainline routing & riser manifold bends"],
        [3, "PVC Fittings", "2\" PVC Equal Tee", "Nos", 30, 12, "=E7-F7", 55.00, "=E7*H7", "Borewell, Corner, Tee A, Tee B & 8 Risers"],
        [4, "PVC Fittings", "2\" PVC Collar / Coupler", "Nos", 10, 6, "=E8-F8", 30.00, "=E8*H8", "Pipe length joins in trenches"],
        [5, "PVC Fittings", "2\" PVC End Cap", "Nos", 10, 6, "=E9-F9", 35.00, "=E9*H9", "Stubs (Borewell S, Corner E, Tee B W) & mainline ends"],
        [6, "PVC Fittings", "2\" PVC Gate Valve (Header)", "Nos", 10, 2, "=E10-F10", 350.00, "=E10*H10", "Borewell delivery & field isolation"],
        [7, "PVC Pipes", "1.5\" (50mm) PVC Pipe Class 2 (20ft length)", "Length", 10, 8, "=E11-F11", 310.00, "=E11*H11", "Plot A sublines & vertical riser drops (152 ft)"],
        [8, "PVC Fittings", "1.5\" PVC 90° Elbow", "Nos", 40, 16, "=E12-F12", 32.00, "=E12*H12", "Plot A 4 overhead risers (4 per station)"],
        [9, "PVC Fittings", "1.5\" PVC Equal Tee", "Nos", 50, 8, "=E13-F13", 38.00, "=E13*H13", "Plot A subline branch junctions"],
        [10, "PVC Fittings", "1.5\" PVC Collar", "Nos", 5, 4, "=E14-F14", 22.00, "=E14*H14", "Plot A subline joins"],
        [11, "PVC Pipes", "1.25\" (40mm) PVC Pipe Class 2 (20ft length)", "Length", 15, 14, "=E15-F15", 240.00, "=E15*H15", "Plot B sublines & vertical riser drops (288 ft)"],
        [12, "PVC Fittings", "1.25\" PVC 90° Elbow", "Nos", 30, 16, "=E16-F16", 25.00, "=E16*H16", "Plot B 4 overhead risers (4 per station)"],
        [13, "PVC Fittings", "1.25\" PVC Equal Tee", "Nos", 40, 8, "=E17-F17", 30.00, "=E17*H17", "Plot B subline branch junctions"],
        [14, "PVC Fittings", "1.25\" PVC Collar", "Nos", 5, 4, "=E18-F18", 18.00, "=E18*H18", "Plot B subline joins"],
        [15, "Consumables", "PVC Solvent Cement (Heavy Duty 3L: 2L in 1/2L + 1L in 1/4L)", "Liters", 3, 2.5, "=E19-F19", 480.00, "=E19*H19", "All solvent-welded joints across 2 acres"],
        [16, "Consumables", "Teflon Thread Seal Tape (12mm x 10m roll)", "Nos", 5, 4, "=E20-F20", 20.00, "=E20*H20", "Threaded filter, gauge & valve connections"],
        [17, "Consumables", "Hacksaw Blades (Bi-metal 12\")", "Nos", 4, 4, "=E21-F21", 25.00, "=E21*H21", "Field cutting of PVC pipes & laterals"],

        # Drip Invoice Items
        [18, "Drip Invoice #1", "16mm Plain Lateral Pipe", "Mtrs", 2000, 1610, "=E22-F22", 7.25, "=E22*H22", "Plot B (32 rows x 165 ft) — 390m reserve"],
        [19, "Drip Invoice #2", "Tunning Dripper (P) (Adjustable 0-70 LPH)", "Nos", 800, 768, "=E23-F23", 4.00, "=E23*H23", "Plot B (24 drippers/row x 32 rows = 768)"],
        [20, "Drip Invoice #3", "Punching Tool (3mm precision punch)", "Nos", 5, 5, "=E24-F24", 10.00, "=E24*H24", "Field crew tools for punching dripper holes"],
        [21, "Drip Invoice #4", "16mm Endcap (Figure-8 / End plug)", "Nos", 110, 80, "=E25-F25", 2.00, "=E25*H25", "48 in Plot A + 32 in Plot B (30 spares)"],
        [22, "Drip Invoice #5", "16mm Lateral Connector (Straight joiner)", "Nos", 40, 10, "=E26-F26", 2.00, "=E26*H26", "Lateral line repair and emergency joining"],
        [23, "Drip Invoice #6", "40x16x1Way TF Coller (Take-off collar West)", "Nos", 35, 32, "=E27-F27", 25.00, "=E27*H27", "Plot B row connections into 40mm subline"],
        [24, "Drip Invoice #7", "40mm Flush Valve", "Nos", 8, 8, "=E28-F28", 30.00, "=E28*H28", "Plot B subline terminal flush points (8 arms)"],
        [25, "Drip Invoice #8", "16x4x40 Inline Pipe (4 LPH @ 40cm drippers)", "Mtrs", 3000, 2926, "=E29-F29", 5.50, "=E29*H29", "Plot A (24 trenches x 390 ft) — 74m reserve"],
        [26, "Drip Invoice #9", "50x16x2 Way Take of Coller (V-connector)", "Nos", 25, 24, "=E30-F30", 30.00, "=E30*H30", "Plot A trench connections (East & West)"],
        [27, "Drip Invoice #10", "50mm Flash Valve (Flush Valve)", "Nos", 8, 8, "=E31-F31", 40.00, "=E31*H31", "Plot A subline terminal flush points (8 arms)"],
        [28, "Drip Invoice #11", "2\" Filter 'T' Type (Disc/Screen Filter)", "Nos", 1, 1, "=E32-F32", 2750.00, "=E32*H32", "Zone 1 Solar Borewell head filtration unit"],
        [29, "Drip Invoice #12", "40mm Plain Ball Valve (1.25\" control valve)", "Nos", 8, 8, "=E33-F33", 130.00, "=E33*H33", "Plot B overhead risers (2 per station x 4)"],
        [30, "Drip Invoice #13", "50mm Plain Ball Valve (1.5\" control valve)", "Nos", 8, 8, "=E34-F34", 210.00, "=E34*H34", "Plot A overhead risers (2 per station x 4)"]
    ]

    master_summary = [
        [],
        ["", "", "SUBTOTAL: PVC PIPES, FITTINGS & CONSUMABLES", "", "", "", "", "", "=SUM(I5:I21)", "17 PVC Inventory Line Items"],
        ["", "", "SUBTOTAL: DRIP IRRIGATION INVOICE ITEMS", "", "", "", "", "", "=SUM(I22:I34)", "13 Drip Commercial Invoice Line Items"],
        ["", "", "TOTAL MATERIAL COST (BEFORE TAX)", "", "", "", "", "", "=I36+I37", "Ex-Factory Material Total"],
        ["", "", "CGST (9%)", "", "", "", "", "", "=0.09*I38", "Central Goods and Services Tax"],
        ["", "", "SGST (9%)", "", "", "", "", "", "=0.09*I38", "State Goods and Services Tax"],
        ["", "", "GRAND TOTAL PROJECT MATERIAL INVOICE", "", "", "", "", "", "=I38+I39+I40", "Full Project Procurement Value (INR)"]
    ]

    all_master = master_headers + master_rows + master_summary
    commands.append(cmd("range.setValues", {"range": "A1", "values": all_master}))

    # Sheet 2: Zone_Allocation
    commands.append(cmd("home.insertSheet", {"name": "Zone_Allocation"}))
    zone_rows = [
        ["ZONE-WISE MATERIAL & HYDRAULIC ALLOCATION MATRIX"],
        ["Detailed breakdown of pipe footage, fittings, and tree counts per hydraulic zone"],
        [],
        ["Zone ID", "Zone Name & Crop", "Target Area", "Mainline Feed", "Riser Stations", "Subline Size & Run", "Laterals & Emitters", "Plant Count", "Allocated Valves & Fittings"],
        ["Zone 1", "Solar Borewell & Mainline Network", "Infrastructure", "2\" Class 2 (730 ft)", "N/A (Header)", "None", "None", 0, "1x 2\" Filter 'T', 2x 2\" Gate Valves, 1x 2\" NRV, 4x 2\" Tees, 4x 2\" End Caps"],
        ["Zone 2", "Plot A: East Field (PKM-1 Moringa)", "1.0 Acre (390x130 ft)", "2\" Center (145 ft)", "4 Overhead (A1-A4 @ 30' spacing)", "1.5\" (50mm) x 120 ft total", "16x4x40 Inline (2,926m across 24 trenches)", 3000, "8x 50mm Ball Valves, 8x 50mm Flush Valves, 24x 50x16x2-Way Collars, 48x 16mm Caps"],
        ["Zone 3", "Plot B: West Field (Bhagya Moringa)", "1.0 Acre (165x260 ft)", "2\" Boundary (240 ft)", "4 Overhead (B1-B4 @ 64' spacing)", "1.25\" (40mm) x 256 ft total", "16mm Plain (1,610m across 32 rows)", 750, "8x 40mm Ball Valves, 8x 40mm Flush Valves, 32x 40x16x1-Way Collars, 768 Drippers, 32x Caps"],
        [],
        ["TOTALS", "2-Acre Moringa Commercial Farm", "2.0 Acres", "1,115 ft Total Mainline", "8 Riser Stations", "376 ft Buried Sublines", "4,536m Drip Laterals Installed", 3750, "16 Ball Valves, 16 Flush Valves, 56 Collars, 80 Caps, 768 Drippers"]
    ]
    commands.append(cmd("range.setValues", {"range": "A1", "values": zone_rows}))

    # Sheet 3: Riser_and_Trench_Schedule
    commands.append(cmd("home.insertSheet", {"name": "Riser_and_Trench_Schedule"}))
    schedule_rows = [
        ["FIELD EXECUTION SCHEDULE: RISER TAPE MEASURES & PIPE CUT-LIST"],
        ["Exact field dimensions from reference origins for excavation, plumbing, and riser assembly"],
        [],
        ["Station Code", "Reference Origin", "Tape Measure Offset (ft)", "Global CAD (X, Y)", "Zone / Subline Arm", "Trench / Row Spacing", "Covered Range (Y)", "Pipe Cut Lengths Required"],
        ["Tee A", "Plot A Center Entry", 0.0, "(500, 100)", "Plot A Center Mainline Start", "Mainline Entry", "Y = 100", "215 ft West from Tee B; 90 ft East from Corner"],
        ["Riser A1", "Tee A (500, 100)", 30.0, "(500, 130)", "Plot A Arms 1 & 2", "5 ft Trench Spacing", "Y = 115 to 145", "1x 4ft 2\" Riser; 2x 4ft 1.5\" Drops; 2x 15ft 1.5\" Sublines"],
        ["Riser A2", "Tee A (500, 100)", 60.0, "(500, 160)", "Plot A Arms 3 & 4", "5 ft Trench Spacing", "Y = 145 to 175", "1x 4ft 2\" Riser; 2x 4ft 1.5\" Drops; 2x 15ft 1.5\" Sublines"],
        ["Riser A3", "Tee A (500, 100)", 90.0, "(500, 190)", "Plot A Arms 5 & 6", "5 ft Trench Spacing", "Y = 175 to 205", "1x 4ft 2\" Riser; 2x 4ft 1.5\" Drops; 2x 15ft 1.5\" Sublines"],
        ["Riser A4", "Tee A (500, 100)", 120.0, "(500, 220)", "Plot A Arms 7 & 8", "5 ft Trench Spacing", "Y = 205 to 235", "1x 4ft 2\" Riser; 2x 4ft 1.5\" Drops; 2x 15ft 1.5\" Sublines"],
        ["End Cap A", "Tee A (500, 100)", 145.0, "(500, 245)", "Plot A Mainline Terminal", "Terminal End", "Y = 245", "1x 2\" End Cap on 25ft mainline tail past Riser A4"],
        [],
        ["Tee B", "Plot B Entry Corner", 0.0, "(285, 100)", "Plot B East Boundary Start", "Mainline Entry", "Y = 100", "Connected to Tee A via 215 ft 2\" pipe"],
        ["Riser B1", "Tee B (285, 100)", 24.0, "(285, 124)", "Plot B Arms 1 & 2", "8 ft Row Spacing", "Y = 92 to 156", "1x 4ft 2\" Riser; 2x 4ft 1.25\" Drops; 2x 32ft 1.25\" Sublines"],
        ["Riser B2", "Tee B (285, 100)", 88.0, "(285, 188)", "Plot B Arms 3 & 4", "8 ft Row Spacing", "Y = 156 to 220", "1x 4ft 2\" Riser; 2x 4ft 1.25\" Drops; 2x 32ft 1.25\" Sublines"],
        ["Riser B3", "Tee B (285, 100)", 152.0, "(285, 252)", "Plot B Arms 5 & 6", "8 ft Row Spacing", "Y = 220 to 284", "1x 4ft 2\" Riser; 2x 4ft 1.25\" Drops; 2x 32ft 1.25\" Sublines"],
        ["Riser B4", "Tee B (285, 100)", 216.0, "(285, 316)", "Plot B Arms 7 & 8", "8 ft Row Spacing", "Y = 284 to 348", "1x 4ft 2\" Riser; 2x 4ft 1.25\" Drops; 2x 32ft 1.25\" Sublines"],
        ["End Cap B", "Tee B (285, 100)", 240.0, "(285, 340)", "Plot B Mainline Terminal", "Terminal End", "Y = 340", "1x 2\" End Cap on 24ft mainline tail past Riser B4"]
    ]
    commands.append(cmd("range.setValues", {"range": "A1", "values": schedule_rows}))

    # Save command
    commands.append(cmd("file.saveAs", {"path": xlsx_path.replace("\\", "/")}))

    # Write jsonl
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for c in commands:
            f.write(json.dumps(c) + "\n")
    print(f"GridCraft JSONL script created: {jsonl_path} ({len(commands)} steps)")

if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    script_file = os.path.join(out_dir, "build_bom.jsonl")
    excel_file = os.path.join(out_dir, "Moringa_Irrigation_BOM_and_Schedule.xlsx")
    build_gridcraft_script(script_file, excel_file)
