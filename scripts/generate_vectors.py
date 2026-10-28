import os
import sys

def create_exploded_view_svg(filepath):
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 950" width="1400" height="950" style="background:#0f172a; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;">
  <defs>
    <linearGradient id="pvcBlue" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1e3a8a"/>
      <stop offset="30%" stop-color="#3b82f6"/>
      <stop offset="70%" stop-color="#60a5fa"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>
    <linearGradient id="pvcGreen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#064e3b"/>
      <stop offset="30%" stop-color="#10b981"/>
      <stop offset="70%" stop-color="#34d399"/>
      <stop offset="100%" stop-color="#047857"/>
    </linearGradient>
    <linearGradient id="pvcOrange" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7c2d12"/>
      <stop offset="30%" stop-color="#f97316"/>
      <stop offset="70%" stop-color="#fb923c"/>
      <stop offset="100%" stop-color="#c2410c"/>
    </linearGradient>
    <linearGradient id="valveRed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#b91c1c"/>
      <stop offset="50%" stop-color="#ef4444"/>
      <stop offset="100%" stop-color="#991b1b"/>
    </linearGradient>
    <linearGradient id="groundGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#78350f" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#451a03" stop-opacity="0.6"/>
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- TITLE BLOCK -->
  <rect x="40" y="30" width="1320" height="90" rx="12" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <text x="70" y="70" fill="#38bdf8" font-size="26" font-weight="bold" letter-spacing="1">4-FOOT OVERHEAD DOUBLE-TEE RISER MANIFOLD</text>
  <text x="70" y="100" fill="#94a3b8" font-size="15">ENGINEERING ISOMETRIC &amp; EXPLODED ASSEMBLY VIEW — ARTCRAFT VECTORCRAFT SPECIFICATION</text>
  <rect x="1100" y="48" width="230" height="54" rx="8" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
  <text x="1115" y="72" fill="#38bdf8" font-size="13" font-weight="bold">WAIST-HEIGHT MANIFOLD</text>
  <text x="1115" y="92" fill="#e2e8f0" font-size="12">Elevation: +4'-0" (1.22m)</text>

  <!-- GROUND GRADE LINE -->
  <rect x="60" y="520" width="1280" height="380" fill="url(#groundGrad)"/>
  <line x1="60" y1="520" x2="1340" y2="520" stroke="#f59e0b" stroke-width="3" stroke-dasharray="10 5"/>
  <text x="80" y="510" fill="#fbbf24" font-size="14" font-weight="bold">▲ FINISHED GROUND LEVEL (GRADE 0.00')</text>
  <text x="80" y="545" fill="#f59e0b" font-size="13">▼ BURIED TRENCH ZONE (-2'-0" Sublines / -2'-6" Mainline)</text>

  <!-- CENTRAL VERTICAL AXIS (EXPLODED PIPELINE) -->
  <!-- 1. Buried 2" Mainline Pipe -->
  <g transform="translate(680, 800)" filter="url(#shadow)">
    <rect x="-240" y="-18" width="480" height="36" rx="6" fill="url(#pvcBlue)" stroke="#60a5fa" stroke-width="1.5"/>
    <text x="0" y="6" fill="#ffffff" font-size="15" font-weight="bold" text-anchor="middle">2" (63mm) PVC MAINLINE (CLASS 2)</text>
    <text x="0" y="28" fill="#93c5fd" font-size="12" text-anchor="middle">Flow Velocity: 1.15 m/s | Trench Depth: 2'-6"</text>
  </g>

  <!-- 2. Buried 2" Tee (Exploded Up) -->
  <g transform="translate(680, 710)" filter="url(#shadow)">
    <path d="M-30,-20 L30,-20 L30,-5 L20,-5 L20,20 L-20,20 L-20,-5 L-30,-5 Z" fill="#2563eb" stroke="#93c5fd" stroke-width="2"/>
    <circle cx="0" cy="-5" r="14" fill="#1d4ed8"/>
    <text x="60" y="0" fill="#38bdf8" font-size="14" font-weight="bold">① BURIED 2" PVC EQUAL TEE</text>
    <text x="60" y="20" fill="#94a3b8" font-size="12">Glued into mainline pointing vertically (+Z)</text>
    <line x1="45" y1="0" x2="15" y2="-5" stroke="#38bdf8" stroke-width="1.5"/>
  </g>

  <!-- 3. Vertical 2" Riser Pipe -->
  <g transform="translate(680, 520)" filter="url(#shadow)">
    <rect x="-16" y="-140" width="32" height="260" rx="4" fill="url(#pvcBlue)" stroke="#60a5fa" stroke-width="1.5"/>
    <text x="50" y="-30" fill="#38bdf8" font-size="14" font-weight="bold">② 4-FOOT VERTICAL 2" PVC RISER</text>
    <text x="50" y="-10" fill="#94a3b8" font-size="12">Elevates water from buried trench (-2.5')</text>
    <text x="50" y="10" fill="#94a3b8" font-size="12">to waist height (+4.0') for ergonomic operation</text>
    <line x1="40" y1="-20" x2="20" y2="-20" stroke="#38bdf8" stroke-width="1.5"/>
  </g>

  <!-- 4. Overhead 2" Double-Tee Manifold at +4.0' -->
  <g transform="translate(680, 290)" filter="url(#shadow)">
    <!-- Central Tee Body -->
    <rect x="-35" y="-25" width="70" height="50" rx="8" fill="#1d4ed8" stroke="#93c5fd" stroke-width="2.5"/>
    <circle cx="0" cy="0" r="18" fill="#3b82f6"/>
    <text x="0" y="6" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">2" TEE</text>
    <text x="0" y="-45" fill="#38bdf8" font-size="16" font-weight="bold" text-anchor="middle">③ OVERHEAD 2" SPLIT TEE (+4.0' ELEV.)</text>
    <text x="0" y="-28" fill="#cbd5e1" font-size="12" text-anchor="middle">Splits Mainline Flow into South &amp; North Sublines</text>
  </g>

  <!-- 5. SOUTH WING (LEFT SIDE) - PLOT A (50mm / 1.5") -->
  <g transform="translate(480, 290)" filter="url(#shadow)">
    <!-- Reducer: 2" to 1.5" -->
    <polygon points="120,-18 70,-14 70,14 120,18" fill="#2563eb" stroke="#93c5fd" stroke-width="2"/>
    <text x="95" y="-28" fill="#38bdf8" font-size="12" text-anchor="middle">2"x1.5" Reducer</text>

    <!-- 50mm Plain Ball Valve -->
    <rect x="-25" y="-20" width="70" height="40" rx="6" fill="#334155" stroke="#64748b" stroke-width="2"/>
    <!-- Red valve handle -->
    <rect x="-10" y="-42" width="40" height="16" rx="4" fill="url(#valveRed)" stroke="#fca5a5" stroke-width="1.5"/>
    <circle cx="10" cy="-20" r="6" fill="#dc2626"/>
    <text x="10" y="6" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">50mm VALVE</text>
    <text x="10" y="-52" fill="#ef4444" font-size="13" font-weight="bold" text-anchor="middle">④ 50mm BALL VALVE</text>

    <!-- 90 Degree Elbow Down -->
    <rect x="-95" y="-20" width="50" height="40" rx="6" fill="#1d4ed8" stroke="#93c5fd" stroke-width="2"/>
    <circle cx="-70" cy="0" r="12" fill="#3b82f6"/>
    <text x="-70" y="-28" fill="#38bdf8" font-size="12" text-anchor="middle">1.5" Elbow</text>

    <!-- Vertical Drop Pipe into South Trench -->
    <rect x="-82" y="30" width="24" height="380" rx="4" fill="url(#pvcGreen)" stroke="#34d399" stroke-width="1.5"/>
    <text x="-95" y="220" fill="#34d399" font-size="13" font-weight="bold" text-anchor="end">⑤ 1.5" VERTICAL DROP (6 FT)</text>
    <line x1="-90" y1="215" x2="-80" y2="215" stroke="#34d399" stroke-width="1.5"/>

    <!-- Bottom Elbow in Trench -->
    <g transform="translate(-70, 430)">
      <rect x="-25" y="-15" width="40" height="35" rx="6" fill="#047857" stroke="#34d399" stroke-width="2"/>
      <circle cx="-5" cy="2" r="10" fill="#10b981"/>
      <text x="-35" y="5" fill="#34d399" font-size="12" text-anchor="end">1.5" Elbow</text>
      <!-- Subline Arm South -->
      <rect x="-250" y="-12" width="225" height="24" rx="4" fill="url(#pvcGreen)" stroke="#34d399" stroke-width="1.5"/>
      <text x="-140" y="5" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">1.5" (50mm) SUBLINE (15 FT SOUTH)</text>

      <!-- Flush Valve on South Arm -->
      <g transform="translate(-250, 0)">
        <circle cx="0" cy="0" r="14" fill="url(#valveRed)" stroke="#fca5a5" stroke-width="1.5"/>
        <line x1="0" y1="-14" x2="0" y2="-50" stroke="#f87171" stroke-width="2"/>
        <rect x="-25" y="-70" width="50" height="20" rx="4" fill="#991b1b" stroke="#f87171" stroke-width="1.5"/>
        <text x="0" y="-56" fill="#fef2f2" font-size="10" font-weight="bold" text-anchor="middle">FLUSH</text>
        <text x="-35" y="-20" fill="#f87171" font-size="12" font-weight="bold" text-anchor="end">⑥ 50mm FLUSH VALVE</text>
      </g>
    </g>
  </g>

  <!-- 6. NORTH WING (RIGHT SIDE) - PLOT B (40mm / 1.25") -->
  <g transform="translate(880, 290)" filter="url(#shadow)">
    <!-- Reducer: 2" to 1.25" -->
    <polygon points="-120,-18 -70,-12 -70,12 -120,18" fill="#2563eb" stroke="#93c5fd" stroke-width="2"/>
    <text x="-95" y="-28" fill="#38bdf8" font-size="12" text-anchor="middle">2"x1.25" Reducer</text>

    <!-- 40mm Plain Ball Valve -->
    <rect x="-45" y="-18" width="65" height="36" rx="6" fill="#334155" stroke="#64748b" stroke-width="2"/>
    <!-- Red valve handle -->
    <rect x="-30" y="-38" width="36" height="14" rx="4" fill="url(#valveRed)" stroke="#fca5a5" stroke-width="1.5"/>
    <circle cx="-12" cy="-18" r="5" fill="#dc2626"/>
    <text x="-12" y="6" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">40mm VALVE</text>
    <text x="-12" y="-48" fill="#ef4444" font-size="13" font-weight="bold" text-anchor="middle">④ 40mm BALL VALVE</text>

    <!-- 90 Degree Elbow Down -->
    <rect x="45" y="-18" width="45" height="36" rx="6" fill="#1d4ed8" stroke="#93c5fd" stroke-width="2"/>
    <circle cx="68" cy="0" r="10" fill="#3b82f6"/>
    <text x="68" y="-28" fill="#38bdf8" font-size="12" text-anchor="middle">1.25" Elbow</text>

    <!-- Vertical Drop Pipe into North Trench -->
    <rect x="58" y="30" width="20" height="380" rx="4" fill="url(#pvcOrange)" stroke="#fb923c" stroke-width="1.5"/>
    <text x="95" y="220" fill="#fb923c" font-size="13" font-weight="bold" text-anchor="start">⑤ 1.25" VERTICAL DROP (6 FT)</text>
    <line x1="80" y1="215" x2="90" y2="215" stroke="#fb923c" stroke-width="1.5"/>

    <!-- Bottom Elbow in Trench -->
    <g transform="translate(68, 430)">
      <rect x="-15" y="-12" width="35" height="30" rx="6" fill="#c2410c" stroke="#fb923c" stroke-width="2"/>
      <circle cx="2" cy="3" r="8" fill="#ea580c"/>
      <text x="35" y="5" fill="#fb923c" font-size="12" text-anchor="start">1.25" Elbow</text>
      <!-- Subline Arm North -->
      <rect x="25" y="-10" width="270" height="20" rx="4" fill="url(#pvcOrange)" stroke="#fb923c" stroke-width="1.5"/>
      <text x="160" y="5" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">1.25" (40mm) SUBLINE (32 FT NORTH)</text>

      <!-- Flush Valve on North Arm -->
      <g transform="translate(295, 0)">
        <circle cx="0" cy="0" r="12" fill="url(#valveRed)" stroke="#fca5a5" stroke-width="1.5"/>
        <line x1="0" y1="-12" x2="0" y2="-50" stroke="#f87171" stroke-width="2"/>
        <rect x="-25" y="-70" width="50" height="20" rx="4" fill="#991b1b" stroke="#f87171" stroke-width="1.5"/>
        <text x="0" y="-56" fill="#fef2f2" font-size="10" font-weight="bold" text-anchor="middle">FLUSH</text>
        <text x="35" y="-20" fill="#f87171" font-size="12" font-weight="bold" text-anchor="start">⑥ 40mm FLUSH VALVE</text>
      </g>
    </g>
  </g>

  <!-- SUMMARY INFO CARDS AT BOTTOM -->
  <g transform="translate(60, 860)">
    <rect x="0" y="0" width="600" height="65" rx="8" fill="#1e293b" stroke="#047857" stroke-width="1.5"/>
    <text x="20" y="26" fill="#34d399" font-size="14" font-weight="bold">PLOT A CONFIGURATION (EAST FIELD — PKM-1)</text>
    <text x="20" y="48" fill="#94a3b8" font-size="12">50mm Plain Ball Valves (8 nos) • 50x16x2-Way Collars (24 nos) • 16x4x40 Inline (2,926m)</text>
  </g>
  <g transform="translate(740, 860)">
    <rect x="0" y="0" width="600" height="65" rx="8" fill="#1e293b" stroke="#c2410c" stroke-width="1.5"/>
    <text x="20" y="26" fill="#fb923c" font-size="14" font-weight="bold">PLOT B CONFIGURATION (WEST FIELD — BHAGYA)</text>
    <text x="20" y="48" fill="#94a3b8" font-size="12">40mm Plain Ball Valves (8 nos) • 40x16x1-Way Collars (32 nos) • 16mm Plain + Drippers (1,610m)</text>
  </g>
</svg>
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Exploded View SVG created: {filepath}")

def create_lateral_takeoff_svg(filepath):
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 950" width="1400" height="950" style="background:#0b1329; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;">
  <defs>
    <linearGradient id="pvc50" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#047857"/>
      <stop offset="40%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#064e3b"/>
    </linearGradient>
    <linearGradient id="pvc40" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#c2410c"/>
      <stop offset="40%" stop-color="#f97316"/>
      <stop offset="100%" stop-color="#7c2d12"/>
    </linearGradient>
    <linearGradient id="lldpeBlack" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="40%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <filter id="glow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
  </defs>

  <!-- TITLE BLOCK -->
  <rect x="40" y="30" width="1320" height="85" rx="12" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <text x="70" y="68" fill="#38bdf8" font-size="24" font-weight="bold">LATERAL TAKE-OFF &amp; DRIP EMITTER ENGINEERING DETAILS</text>
  <text x="70" y="96" fill="#94a3b8" font-size="14">COMPARATIVE CROSS-SECTIONS: PLOT A (2-WAY INLINE) VS. PLOT B (1-WAY ONLINE TUNNING DRIPPER)</text>

  <!-- LEFT PANEL: PLOT A (50x16x2-WAY TAKE-OFF) -->
  <g transform="translate(60, 145)">
    <rect x="0" y="0" width="620" height="740" rx="12" fill="#132238" stroke="#10b981" stroke-width="2" filter="url(#glow)"/>
    <rect x="0" y="0" width="620" height="50" rx="12" fill="#064e3b"/>
    <text x="310" y="32" fill="#ffffff" font-size="16" font-weight="bold" text-anchor="middle">PLOT A: 50x16x2-WAY TAKE-OFF COLLAR (V-CONNECTOR)</text>

    <!-- Subline pipe (50mm / 1.5") Cross section -->
    <g transform="translate(310, 260)">
      <circle cx="0" cy="0" r="85" fill="url(#pvc50)" stroke="#6ee7b7" stroke-width="3"/>
      <circle cx="0" cy="0" r="70" fill="#0f172a" stroke="#047857" stroke-width="2"/>
      <text x="0" y="-5" fill="#34d399" font-size="18" font-weight="bold" text-anchor="middle">50mm (1.5") PVC</text>
      <text x="0" y="20" fill="#a7f3d0" font-size="13" text-anchor="middle">Buried Subline Arm</text>

      <!-- Drilled hole at top (16mm hole with grommet) -->
      <rect x="-16" y="-87" width="32" height="17" rx="3" fill="#000000" stroke="#facc15" stroke-width="2"/>
      <text x="0" y="-100" fill="#facc15" font-size="12" font-weight="bold" text-anchor="middle">16mm Precision Drill + Rubber Grommet</text>

      <!-- 50x16x2-Way Collar Saddle (Clamps around pipe) -->
      <path d="M-85,-20 A95,95 0 0,1 85,-20 L95,-10 A105,105 0 0,0 -95,-10 Z" fill="#0284c7" stroke="#38bdf8" stroke-width="1.5"/>
      <rect x="-18" y="-120" width="36" height="35" rx="4" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>

      <!-- 2-Way V-Split Outlets (East & West) -->
      <!-- West Outlet (Left) -->
      <path d="M-12,-115 L-90,-180 L-100,-170 L-18,-105 Z" fill="#0369a1" stroke="#38bdf8" stroke-width="1.5"/>
      <rect x="-240" y="-195" width="150" height="24" rx="4" fill="url(#lldpeBlack)" stroke="#38bdf8" stroke-width="2"/>
      <text x="-165" y="-178" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">16mm Inline (West 195')</text>

      <!-- East Outlet (Right) -->
      <path d="M12,-115 L90,-180 L100,-170 L18,-105 Z" fill="#0369a1" stroke="#38bdf8" stroke-width="1.5"/>
      <rect x="90" y="-195" width="150" height="24" rx="4" fill="url(#lldpeBlack)" stroke="#38bdf8" stroke-width="2"/>
      <text x="165" y="-178" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">16mm Inline (East 195')</text>
    </g>

    <!-- INLINE DRIPPER CUTAWAY -->
    <g transform="translate(310, 480)">
      <rect x="-260" y="0" width="520" height="90" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
      <text x="-240" y="28" fill="#38bdf8" font-size="14" font-weight="bold">16x4x40 INLINE DRIP TUBE INTERNAL STRUCTURE</text>
      <!-- Pipe outer -->
      <rect x="-240" y="42" width="480" height="34" rx="4" fill="#020617" stroke="#475569" stroke-width="1.5"/>
      <!-- Built-in Cylindrical Labyrinth Dripper -->
      <rect x="-60" y="46" width="120" height="26" rx="3" fill="#0284c7" stroke="#38bdf8" stroke-width="1.5"/>
      <line x1="-50" y1="59" x2="50" y2="59" stroke="#93c5fd" stroke-width="2" stroke-dasharray="4 3"/>
      <!-- Water exit hole -->
      <circle cx="0" cy="42" r="3" fill="#38bdf8"/>
      <!-- Water drops -->
      <circle cx="0" cy="30" r="3" fill="#60a5fa"/>
      <circle cx="0" cy="18" r="4" fill="#93c5fd"/>
      <text x="75" y="64" fill="#e2e8f0" font-size="11">4 LPH Emitter @ 40cm</text>
      <text x="-240" y="64" fill="#94a3b8" font-size="11">Turbulent Flow Labyrinth</text>
    </g>

    <!-- SPECS TABLE -->
    <g transform="translate(40, 600)">
      <text x="0" y="0" fill="#10b981" font-size="14" font-weight="bold">KEY SPECIFICATIONS &amp; QUANTITIES:</text>
      <text x="0" y="24" fill="#cbd5e1" font-size="13">• Collar Model: 50x16x2 Way Take of Coller (Item #9) — 24 used (1 spare)</text>
      <text x="0" y="46" fill="#cbd5e1" font-size="13">• Drip Pipe: 16x4x40 Inline Pipe (Item #8) — 2,926m used (3,000m roll ordered)</text>
      <text x="0" y="68" fill="#cbd5e1" font-size="13">• Spacing: 5 ft between trenches • 40cm dripper spacing • 3 ft plant spacing</text>
      <text x="0" y="90" fill="#cbd5e1" font-size="13">• End Fittings: 16mm Endcap (Item #4) — 48 nos used (24 West + 24 East)</text>
      <text x="0" y="112" fill="#34d399" font-size="13" font-weight="bold">• Total Plants Fed: 3,000 PKM-1 Moringa trees</text>
    </g>
  </g>

  <!-- RIGHT PANEL: PLOT B (40x16x1-WAY TAKE-OFF) -->
  <g transform="translate(720, 145)">
    <rect x="0" y="0" width="620" height="740" rx="12" fill="#1c1917" stroke="#f97316" stroke-width="2" filter="url(#glow)"/>
    <rect x="0" y="0" width="620" height="50" rx="12" fill="#7c2d12"/>
    <text x="310" y="32" fill="#ffffff" font-size="16" font-weight="bold" text-anchor="middle">PLOT B: 40x16x1-WAY TAKE-OFF COLLAR &amp; ON-LINE DRIPPER</text>

    <!-- Subline pipe (40mm / 1.25") Cross section -->
    <g transform="translate(420, 260)">
      <circle cx="0" cy="0" r="70" fill="url(#pvc40)" stroke="#fdba74" stroke-width="3"/>
      <circle cx="0" cy="0" r="56" fill="#0f172a" stroke="#c2410c" stroke-width="2"/>
      <text x="0" y="-5" fill="#fb923c" font-size="17" font-weight="bold" text-anchor="middle">40mm (1.25") PVC</text>
      <text x="0" y="18" fill="#fed7aa" font-size="12" text-anchor="middle">Buried Subline Arm</text>

      <!-- 40x16x1-Way Collar Clamp -->
      <path d="M-70,-15 A78,78 0 0,1 70,-15 L80,-5 A88,88 0 0,0 -80,-5 Z" fill="#ea580c" stroke="#fdba74" stroke-width="1.5"/>

      <!-- 1-Way Takeoff Outlet pointing WEST ONLY (to the left) -->
      <rect x="-140" y="-15" width="80" height="30" rx="4" fill="#c2410c" stroke="#fdba74" stroke-width="2"/>
      <text x="-100" y="-22" fill="#facc15" font-size="11" font-weight="bold" text-anchor="middle">40x16x1-Way TF Collar</text>

      <!-- 16mm Plain Pipe Running West -->
      <rect x="-350" y="-12" width="210" height="24" rx="4" fill="url(#lldpeBlack)" stroke="#fb923c" stroke-width="2"/>
      <text x="-245" y="4" fill="#fed7aa" font-size="12" font-weight="bold" text-anchor="middle">16mm Plain Pipe (West 165')</text>
    </g>

    <!-- PUNCHING TOOL & TUNNING DRIPPER ASSEMBLY DETAIL -->
    <g transform="translate(310, 480)">
      <rect x="-260" y="0" width="520" height="90" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
      <text x="-240" y="28" fill="#fb923c" font-size="14" font-weight="bold">ON-SITE PUNCHING &amp; TUNNING DRIPPER (P) INSTALLATION</text>
      
      <!-- 16mm Plain Pipe Section -->
      <rect x="-240" y="42" width="480" height="34" rx="4" fill="#020617" stroke="#475569" stroke-width="1.5"/>
      
      <!-- Punched On-line Tunning Dripper -->
      <g transform="translate(0, 42)">
        <!-- Barb inserted into pipe -->
        <polygon points="-4,0 4,0 2,12 -2,12" fill="#f59e0b"/>
        <!-- Dripper body -->
        <rect x="-14" y="-26" width="28" height="26" rx="4" fill="#ea580c" stroke="#fdba74" stroke-width="1.5"/>
        <circle cx="0" cy="-13" r="6" fill="#facc15"/>
        <text x="25" y="-10" fill="#facc15" font-size="11" font-weight="bold">Tunning Dripper (P)</text>
        <text x="25" y="6" fill="#fed7aa" font-size="10">Adjustable 0-70 LPH @ 7 ft spacing</text>
      </g>

      <!-- Punching Tool representation -->
      <g transform="translate(-160, 42)">
        <rect x="-6" y="-30" width="12" height="25" rx="2" fill="#3b82f6" stroke="#93c5fd" stroke-width="1"/>
        <polygon points="-3,-5 3,-5 0,0" fill="#e2e8f0"/>
        <text x="0" y="-35" fill="#93c5fd" font-size="10" text-anchor="middle">Punch Tool</text>
      </g>
    </g>

    <!-- SPECS TABLE -->
    <g transform="translate(40, 600)">
      <text x="0" y="0" fill="#f97316" font-size="14" font-weight="bold">KEY SPECIFICATIONS &amp; QUANTITIES:</text>
      <text x="0" y="24" fill="#cbd5e1" font-size="13">• Collar Model: 40x16x1Way TF Coller (Item #6) — 32 used (3 spare)</text>
      <text x="0" y="46" fill="#cbd5e1" font-size="13">• Plain Pipe: 16mm Pipe Mtrs (Item #1) — 1,610m used (2,000m roll ordered)</text>
      <text x="0" y="68" fill="#cbd5e1" font-size="13">• Drippers: Tunning Dripper (P) (Item #2) — 768 used (800 nos ordered / 32 spare)</text>
      <text x="0" y="90" fill="#cbd5e1" font-size="13">• Punching: 3mm Hole via Punching Tool (Item #3) — 5 tools for field crew</text>
      <text x="0" y="112" fill="#fb923c" font-size="13" font-weight="bold">• Total Plants Fed: 750 Bhagya Moringa trees (7x8ft commercial grid)</text>
    </g>
  </g>
</svg>
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Lateral Takeoff SVG created: {filepath}")

if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    f1 = os.path.join(out_dir, "Riser_Manifold_Exploded_View.svg")
    f2 = os.path.join(out_dir, "Lateral_Takeoff_Details.svg")
    create_exploded_view_svg(f1)
    create_lateral_takeoff_svg(f2)
