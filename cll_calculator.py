"""
CLL Response Assessment Calculator
Hodnocení odpovědi na léčbu dle iwCLL 2018 Guidelines
"""

import streamlit as st
from datetime import date

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CLL Kalkulátor – Hodnocení Odpovědi",
    page_icon="🩺",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main header */
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #555;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    .badge {
        background: #f0f4ff;
        border: 1px solid #c5d1f5;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.75rem;
        color: #3b5bdb;
        display: inline-block;
        margin-bottom: 1.5rem;
    }
    /* Section headers */
    .section-a {
        background: #e8f0fe;
        border-left: 4px solid #4285f4;
        padding: 6px 12px;
        font-weight: 600;
        border-radius: 0 6px 6px 0;
        color: #1a1a2e;
        font-size: 0.9rem;
    }
    .section-b {
        background: #e6f4ea;
        border-left: 4px solid #34a853;
        padding: 6px 12px;
        font-weight: 600;
        border-radius: 0 6px 6px 0;
        color: #1a1a2e;
        font-size: 0.9rem;
    }
    .section-warn {
        background: #fff3e0;
        border-left: 4px solid #ea8600;
        padding: 6px 12px;
        font-weight: 600;
        border-radius: 0 6px 6px 0;
        color: #1a1a2e;
        font-size: 0.9rem;
    }
    /* Result cards */
    .result-CR  { background:#d4edda; border:2px solid #28a745; color:#155724; }
    .result-CRi { background:#cce5ff; border:2px solid #004085; color:#004085; }
    .result-PR  { background:#cce5ff; border:2px solid #0056b3; color:#0056b3; }
    .result-PRL { background:#e2d9f3; border:2px solid #6f42c1; color:#4a2c8f; }
    .result-SD  { background:#fff3cd; border:2px solid #856404; color:#533f03; }
    .result-PD  { background:#f8d7da; border:2px solid #721c24; color:#721c24; }
    .result-box {
        border-radius: 12px;
        padding: 1.5rem 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .result-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; opacity: 0.75; }
    .result-value { font-size: 3rem; font-weight: 800; line-height: 1; margin: 0.3rem 0; }
    .result-desc  { font-size: 0.85rem; line-height: 1.5; }
    /* Doc output */
    .doc-box {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        font-family: monospace;
        font-size: 0.82rem;
        line-height: 1.7;
        color: #333;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    /* Breakdown table */
    .bd-row {
        display: flex;
        justify-content: space-between;
        padding: 6px 0;
        border-bottom: 1px solid #eee;
        font-size: 0.85rem;
    }
    .badge-met    { background:#d4edda; color:#155724; padding:2px 8px; border-radius:4px; font-size:0.75rem; }
    .badge-notmet { background:#f8d7da; color:#721c24; padding:2px 8px; border-radius:4px; font-size:0.75rem; }
    .badge-warn   { background:#fff3cd; color:#533f03; padding:2px 8px; border-radius:4px; font-size:0.75rem; }
    .badge-na     { background:#e9ecef; color:#555;    padding:2px 8px; border-radius:4px; font-size:0.75rem; }
    .note-warn {
        background: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-size: 0.82rem;
        color: #533f03;
        line-height: 1.6;
    }
    .spd-info {
        background: #f0f4ff;
        border: 1px solid #c5d1f5;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 0.82rem;
        color: #1a1a2e;
        margin-top: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">🩺 CLL Response Assessment</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Kalkulátor hodnocení odpovědi na léčbu</p>', unsafe_allow_html=True)
st.markdown('<span class="badge">📋 iwCLL 2018 Guidelines</span>', unsafe_allow_html=True)

# ── Helper functions ──────────────────────────────────────────────────────────
def nf(v, decimals=2):
    """Format number nicely."""
    if v is None:
        return "—"
    return f"{v:.{decimals}f}"

def pct_str(v):
    if v is None:
        return ""
    sign = "+" if v > 0 else ""
    return f"{sign}{v:.1f}%"

def badge_html(status, label):
    cls = {"met": "badge-met", "notmet": "badge-notmet", "warn": "badge-warn"}.get(status, "badge-na")
    icon = {"met": "✓", "notmet": "✗", "warn": "⚠", "na": "—"}.get(status, "—")
    return f'<span class="{cls}">{icon} {label}</span>'

# ═══════════════════════════════════════════════════════════════════════════════
#  SKUPINA A
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-a">📍 SKUPINA A — Klinické parametry</div>', unsafe_allow_html=True)
st.write("")

# ── Lymfatické uzliny ────────────────────────────────────────────────────────
with st.expander("🔵 Lymfatické uzliny — SPD", expanded=True):
    ln_mode = st.radio(
        "Způsob zadání",
        ["Jednotlivé uzliny (výpočet SPD)", "Přímé zadání SPD"],
        horizontal=True,
        key="ln_mode"
    )

    baseline_spd = 0.0
    current_spd = 0.0
    has_any_ln = False
    all_nodes_small = True  # for CR check: all nodes ≤1.5 cm

    if ln_mode == "Jednotlivé uzliny (výpočet SPD)":
        n_nodes = st.number_input("Počet uzlin (1–6)", min_value=1, max_value=6, value=1, step=1)
        cols_header = st.columns([2, 1, 1, 1, 1])
        cols_header[0].markdown("**Uzlina**")
        cols_header[1].markdown("**BL d₁ (cm)**")
        cols_header[2].markdown("**BL d₂ (cm)**")
        cols_header[3].markdown("**Aktuálně d₁**")
        cols_header[4].markdown("**Aktuálně d₂**")

        for i in range(int(n_nodes)):
            c = st.columns([2, 1, 1, 1, 1])
            c[0].markdown(f"Uzlina {i+1}")
            b1 = c[1].number_input("", min_value=0.0, step=0.1, key=f"b1_{i}", label_visibility="collapsed")
            b2 = c[2].number_input("", min_value=0.0, step=0.1, key=f"b2_{i}", label_visibility="collapsed")
            c1 = c[3].number_input("", min_value=0.0, step=0.1, key=f"c1_{i}", label_visibility="collapsed")
            c2 = c[4].number_input("", min_value=0.0, step=0.1, key=f"c2_{i}", label_visibility="collapsed")

            ppd_b = b1 * b2 if (b1 > 0 and b2 > 0) else None
            ppd_c = c1 * c2 if (c1 > 0 and c2 > 0) else None

            if ppd_b is not None:
                baseline_spd += ppd_b
                has_any_ln = True
            if ppd_c is not None:
                current_spd += ppd_c
            if c1 and c1 > 1.5:
                all_nodes_small = False
            if c2 and c2 > 1.5:
                all_nodes_small = False

        if has_any_ln:
            spd_pct = ((current_spd - baseline_spd) / baseline_spd * 100) if baseline_spd > 0 else None
            color = "green" if (spd_pct is not None and spd_pct <= -50) else ("red" if (spd_pct is not None and spd_pct >= 50) else "orange")
            st.markdown(f'<div class="spd-info">SPD baseline: <b>{baseline_spd:.2f} cm²</b> → aktuálně: <b>{current_spd:.2f} cm²</b> &nbsp;|&nbsp; <b style="color:{color}">{pct_str(spd_pct)} oproti baseline</b></div>', unsafe_allow_html=True)
    else:
        col1, col2 = st.columns(2)
        with col1:
            spd_base_direct = st.number_input("SPD celkem — baseline (cm²)", min_value=0.0, step=0.01, key="spd_base_d")
        with col2:
            spd_curr_direct = st.number_input("SPD celkem — aktuálně (cm²)", min_value=0.0, step=0.01, key="spd_curr_d")
        if spd_base_direct > 0:
            has_any_ln = True
            baseline_spd = spd_base_direct
            current_spd = spd_curr_direct
            spd_pct = ((current_spd - baseline_spd) / baseline_spd * 100) if baseline_spd > 0 else None
            color = "green" if (spd_pct is not None and spd_pct <= -50) else ("red" if (spd_pct is not None and spd_pct >= 50) else "orange")
            st.markdown(f'<div class="spd-info"><b style="color:{color}">{pct_str(spd_pct)} oproti baseline</b></div>', unsafe_allow_html=True)
        all_nodes_small = (current_spd == 0)

# ── Slezina a játra ──────────────────────────────────────────────────────────
with st.expander("🔵 Slezina a játra", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        spleen_base = st.number_input("Slezina — baseline (cm)", min_value=0.0, step=0.1, key="sp_base",
                                       help="Splenomegalie = ≥13 cm")
        liver_base_sel = st.selectbox("Játra — baseline", ["Normální", "Zvětšená (hepatomegalie)"], key="liv_base")
    with c2:
        spleen_curr = st.number_input("Slezina — aktuálně (cm)", min_value=0.0, step=0.1, key="sp_curr")
        liver_curr_sel = st.selectbox("Játra — aktuálně", ["Normální", "Zvětšená (hepatomegalie)"], key="liv_curr")

# ── Konstituční příznaky ──────────────────────────────────────────────────────
with st.expander("🔵 Konstituční příznaky", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        const_base_sel = st.selectbox("Baseline", ["Žádné", "Přítomny"], key="const_base")
    with c2:
        const_curr_sel = st.selectbox("Aktuálně", ["Žádné", "Přítomny"], key="const_curr")

# ── Lymfocyty ────────────────────────────────────────────────────────────────
with st.expander("🔵 Cirkulující lymfocyty", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        lymph_base_v = st.number_input("Baseline (×10⁹/L)", min_value=0.0, step=0.1, key="lym_base",
                                        help="Lymfocytóza = >5 ×10⁹/L")
    with c2:
        lymph_curr_v = st.number_input("Aktuálně (×10⁹/L)", min_value=0.0, step=0.1, key="lym_curr")

# ═══════════════════════════════════════════════════════════════════════════════
#  SKUPINA B
# ═══════════════════════════════════════════════════════════════════════════════
st.write("")
st.markdown('<div class="section-b">📍 SKUPINA B — Hematologické parametry</div>', unsafe_allow_html=True)
st.write("")

with st.expander("🟢 Krevní obraz", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        plt_base_v = st.number_input("Trombocyty — baseline (×10⁹/L)", min_value=0.0, step=1.0, key="plt_base",
                                      help="Abnormální = <100")
        plt_curr_v = st.number_input("Trombocyty — aktuálně (×10⁹/L)", min_value=0.0, step=1.0, key="plt_curr")
    with c2:
        hgb_base_v = st.number_input("Hemoglobin — baseline (g/dL)", min_value=0.0, step=0.1, key="hgb_base",
                                      help="Abnormální = <11")
        hgb_curr_v = st.number_input("Hemoglobin — aktuálně (g/dL)", min_value=0.0, step=0.1, key="hgb_curr")
    with c3:
        anc_base_v = st.number_input("ANC — baseline (×10⁹/L)", min_value=0.0, step=1.0, key="anc_base",
                                      help="Abnormální = <1500")
        anc_curr_v = st.number_input("ANC — aktuálně (×10⁹/L)", min_value=0.0, step=1.0, key="anc_curr")

with st.expander("🟢 Kostní dřeň", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        marrow_sel = st.selectbox("Výsledek biopsie", [
            "Nebyla provedena",
            "Normální (normocellular, bez CLL buněk)",
            "Přítomnost CLL buněk / B-lymfoidních nodulů",
            "Lymfoidní noduly (bez CLL infiltrace)",
            "Nárůst CLL buněk (≥50%) v opakovaných biopsiích"
        ], key="marrow")
    with c2:
        marrow_pct_v = st.number_input("% lymfocytů v dřeni", min_value=0, max_value=100, step=1, key="marrow_pct",
                                        help="Pro CR: <30%")

# ═══════════════════════════════════════════════════════════════════════════════
#  NOVÉ LÉZE
# ═══════════════════════════════════════════════════════════════════════════════
st.write("")
st.markdown('<div class="section-warn">⚠️ Nové léze / nová cytopenie</div>', unsafe_allow_html=True)
st.write("")
c1, c2 = st.columns(2)
with c1:
    new_lesions_v = st.selectbox("Nové lymfatické uzliny nebo extranodální léze", ["Ne", "Ano"], key="new_lesions")
with c2:
    new_cytopenia_v = st.selectbox("Nová cytopenie nesouvisející s léčbou", ["Ne", "Ano"], key="new_cytopenia")

# ═══════════════════════════════════════════════════════════════════════════════
#  CALCULATE BUTTON
# ═══════════════════════════════════════════════════════════════════════════════
st.write("")
calc_col, reset_col = st.columns([3, 1])
with calc_col:
    calculate = st.button("🔬 Vyhodnotit odpověď", type="primary", use_container_width=True)
with reset_col:
    if st.button("↺ Resetovat", use_container_width=True):
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
#  CALCULATION LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
if calculate:

    # Prepare values (0.0 inputs treated as "not entered" for baseline)
    def _val(v):
        return v if v > 0 else None

    spleen_base_val = _val(spleen_base)
    spleen_curr_val = _val(spleen_curr)
    lymph_base_val  = _val(lymph_base_v)
    lymph_curr_val  = _val(lymph_curr_v)
    plt_base_val    = _val(plt_base_v)
    plt_curr_val    = _val(plt_curr_v)
    hgb_base_val    = _val(hgb_base_v)
    hgb_curr_val    = _val(hgb_curr_v)
    anc_base_val    = _val(anc_base_v)
    anc_curr_val    = _val(anc_curr_v)
    marrow_pct_val  = _val(float(marrow_pct_v))

    # SPD
    spd_pct = None
    if has_any_ln and baseline_spd > 0:
        spd_pct = (current_spd - baseline_spd) / baseline_spd * 100

    # ── PD check ──────────────────────────────────────────────────────────────
    is_pd = False
    pd_reasons = []

    if spd_pct is not None and spd_pct >= 50:
        is_pd = True; pd_reasons.append("SPD vzrostlo ≥50% oproti baseline")
    if new_lesions_v == "Ano":
        is_pd = True; pd_reasons.append("Nové lymfatické léze")
    if new_cytopenia_v == "Ano":
        is_pd = True; pd_reasons.append("Nová cytopenie nesouvisející s léčbou")
    if spleen_base_val and spleen_curr_val and spleen_curr_val > spleen_base_val * 1.5:
        is_pd = True; pd_reasons.append("Slezina vzrostla ≥50%")
    if hgb_base_val and hgb_curr_val and (hgb_base_val - hgb_curr_val) >= 2:
        is_pd = True; pd_reasons.append("Hb poklesl ≥2 g/dL")
    if plt_base_val and plt_curr_val and plt_curr_val < plt_base_val * 0.5:
        is_pd = True; pd_reasons.append("Trombocyty poklesly ≥50%")
    if "Nárůst" in marrow_sel:
        is_pd = True; pd_reasons.append("Nárůst CLL buněk v kostní dřeni")

    # ── GROUP A ───────────────────────────────────────────────────────────────
    A_met = 0
    A_abnormal = 0
    a_items = []  # (name, val_str, status, note)
    lymphocytosis = False

    # LN / SPD
    ln_abnormal_at_bl = has_any_ln and baseline_spd > 0
    if has_any_ln:
        if ln_abnormal_at_bl and spd_pct is not None:
            A_abnormal += 1
            display_spd = f"{pct_str(spd_pct)} (BL SPD: {baseline_spd:.2f} cm²)"
            if spd_pct <= -50:
                A_met += 1; spd_status = "met"
            else:
                spd_status = "notmet"
            a_items.append(("Lymf. uzliny (SPD)", display_spd, spd_status, None))
        else:
            a_items.append(("Lymf. uzliny (SPD)", f"SPD aktuálně: {current_spd:.2f} cm²", "na", "Bez baseline hodnot nelze hodnotit zlepšení"))
    else:
        a_items.append(("Lymf. uzliny (SPD)", "—", "na", "Nezadáno"))

    # Lymfocyty
    lymph_base_abn = lymph_base_val is not None and lymph_base_val > 5
    if lymph_curr_val is not None:
        lym_display = f"{lymph_curr_val} ×10⁹/L"
        if lymph_base_abn:
            A_abnormal += 1
            lym_pct = (lymph_base_val - lymph_curr_val) / lymph_base_val * 100
            if lymph_curr_val < 4:
                A_met += 1; lym_status = "met"
            elif lym_pct >= 50:
                A_met += 1; lym_status = "met"
            elif lymph_curr_val >= 5:
                lymphocytosis = True; lym_status = "warn"
            else:
                lym_status = "notmet"
            a_items.append(("Lymfocyty", lym_display, lym_status, None))
        elif lymph_base_val is not None:
            lym_status = "na" if lymph_curr_val < 4 else "notmet"
            a_items.append(("Lymfocyty", lym_display, lym_status, "Normální při baseline — nezapočítává se pro PR"))
        else:
            if lymph_curr_val >= 5:
                lymphocytosis = True; lym_status = "warn"
            else:
                lym_status = "na"
            a_items.append(("Lymfocyty", lym_display, lym_status, "Baseline nezadán"))
    else:
        a_items.append(("Lymfocyty", "—", "na", "Nezadáno"))

    # Slezina
    spleen_base_abn = spleen_base_val is not None and spleen_base_val >= 13
    if spleen_curr_val is not None:
        sp_display = f"{spleen_curr_val} cm"
        if spleen_base_abn:
            A_abnormal += 1
            sp_pct = (spleen_base_val - spleen_curr_val) / spleen_base_val * 100
            if sp_pct >= 50 or spleen_curr_val < 13:
                A_met += 1; sp_status = "met"
            else:
                sp_status = "notmet"
        elif spleen_base_val is not None:
            sp_status = "na"
        else:
            sp_status = "na"
        note_sp = "Normální při baseline (<13 cm) — nezapočítává se" if (spleen_base_val is not None and not spleen_base_abn) else None
        a_items.append(("Slezina", sp_display, sp_status, note_sp))
    else:
        a_items.append(("Slezina", "—", "na", "Nezadáno"))

    # Játra
    liver_base_abn = liver_base_sel == "Zvětšená (hepatomegalie)"
    liver_curr_normal = liver_curr_sel == "Normální"
    if liver_base_abn:
        A_abnormal += 1
        if liver_curr_normal:
            A_met += 1; liv_status = "met"
        else:
            liv_status = "notmet"
    else:
        liv_status = "na"
    note_liv = "Normální při baseline — nezapočítává se" if not liver_base_abn else None
    a_items.append(("Játra", liver_curr_sel, liv_status, note_liv))

    # Konstituční příznaky
    const_base_abn = const_base_sel == "Přítomny"
    const_curr_none = const_curr_sel == "Žádné"
    if const_base_abn:
        A_abnormal += 1
        if const_curr_none:
            A_met += 1; const_status = "met"
        else:
            const_status = "notmet"
    else:
        const_status = "na" if const_curr_none else "notmet"
    note_const = "Nepřítomny při baseline — nezapočítávají se pro PR" if not const_base_abn else None
    a_items.append(("Konstituční příznaky", const_curr_sel, const_status, note_const))

    # ── GROUP B ───────────────────────────────────────────────────────────────
    B_met = 0
    B_abnormal = 0
    b_items = []

    # Trombocyty
    plt_base_abn = plt_base_val is not None and plt_base_val < 100
    if plt_curr_val is not None:
        if plt_base_abn:
            B_abnormal += 1
            plt_pct = (plt_curr_val - plt_base_val) / plt_base_val * 100
            if plt_curr_val >= 100 or plt_pct >= 50:
                B_met += 1; plt_status = "met"
            else:
                plt_status = "notmet"
        elif plt_base_val is not None:
            plt_status = "na" if plt_curr_val >= 100 else "notmet"
        else:
            plt_status = "na"
        note_plt = "Normální při baseline — nezapočítává se pro PR" if (plt_base_val is not None and not plt_base_abn) else None
        b_items.append(("Trombocyty", f"{plt_curr_val} ×10⁹/L", plt_status, note_plt))
    else:
        b_items.append(("Trombocyty", "—", "na", "Nezadáno"))

    # Hemoglobin
    hgb_base_abn = hgb_base_val is not None and hgb_base_val < 11
    if hgb_curr_val is not None:
        if hgb_base_abn:
            B_abnormal += 1
            hgb_pct = (hgb_curr_val - hgb_base_val) / hgb_base_val * 100
            if hgb_curr_val >= 11 or hgb_pct >= 50:
                B_met += 1; hgb_status = "met"
            else:
                hgb_status = "notmet"
        elif hgb_base_val is not None:
            hgb_status = "na" if hgb_curr_val >= 11 else "notmet"
        else:
            hgb_status = "na"
        note_hgb = "Normální při baseline — nezapočítává se pro PR" if (hgb_base_val is not None and not hgb_base_abn) else None
        b_items.append(("Hemoglobin", f"{hgb_curr_val} g/dL", hgb_status, note_hgb))
    else:
        b_items.append(("Hemoglobin", "—", "na", "Nezadáno"))

    # ANC
    anc_base_abn = anc_base_val is not None and anc_base_val < 1500
    if anc_curr_val is not None:
        if anc_base_abn:
            B_abnormal += 1
            anc_pct = (anc_curr_val - anc_base_val) / anc_base_val * 100
            if anc_curr_val >= 1500 or anc_pct >= 50:
                B_met += 1; anc_status = "met"
            else:
                anc_status = "notmet"
        elif anc_base_val is not None:
            anc_status = "na" if anc_curr_val >= 1500 else "notmet"
        else:
            anc_status = "na"
        note_anc = "Normální při baseline — nezapočítává se pro PR" if (anc_base_val is not None and not anc_base_abn) else None
        b_items.append(("ANC (neutrofily)", f"{anc_curr_val} ×10⁹/L", anc_status, note_anc))
    else:
        b_items.append(("ANC (neutrofily)", "—", "na", "Nezadáno"))

    # Kostní dřeň
    marrow_map = {
        "Nebyla provedena": "not_done",
        "Normální (normocellular, bez CLL buněk)": "normal",
        "Přítomnost CLL buněk / B-lymfoidních nodulů": "cll_cells",
        "Lymfoidní noduly (bez CLL infiltrace)": "nodules",
        "Nárůst CLL buněk (≥50%) v opakovaných biopsiích": "increasing"
    }
    marrow_key = marrow_map[marrow_sel]

    if marrow_key == "normal":
        B_met += 1; B_abnormal += 1; marrow_status = "met"
        note_marrow = None
    elif marrow_key == "not_done":
        B_met += 1; B_abnormal += 1; marrow_status = "warn"
        note_marrow = "Nebyla provedena — pro PR se počítá jako splněno (iwCLL 2018)"
    elif marrow_key in ("cll_cells", "nodules"):
        B_abnormal += 1; marrow_status = "warn"
        note_marrow = None
    elif marrow_key == "increasing":
        B_abnormal += 1; marrow_status = "notmet"
        note_marrow = None
    else:
        marrow_status = "na"; note_marrow = None

    b_items.append(("Kostní dřeň", marrow_sel, marrow_status, note_marrow))

    B_all_normal = B_abnormal == 0
    total_abnormal = A_abnormal + B_abnormal
    single_param_rule = total_abnormal <= 1

    pr_A_threshold = 1 if single_param_rule else 2
    pr_B_threshold = 0 if single_param_rule else 1

    B_satisfied = B_met >= 1 or B_all_normal

    # PR check
    if single_param_rule:
        pr_met = (A_met >= 1 or B_met >= 1)
    else:
        pr_met = (A_met >= pr_A_threshold) and B_satisfied

    # ── CR checks ─────────────────────────────────────────────────────────────
    cr_nodes  = not has_any_ln or all_nodes_small
    cr_spleen = spleen_curr_val is None or spleen_curr_val < 13
    cr_liver  = liver_curr_normal
    cr_const  = const_curr_none
    cr_lymph  = lymph_curr_val is not None and lymph_curr_val < 4
    cr_plt    = plt_curr_val is not None and plt_curr_val >= 100
    cr_hgb    = hgb_curr_val is not None and hgb_curr_val >= 11
    cr_anc    = anc_curr_val is not None and anc_curr_val >= 1500
    cr_marrow_normal = marrow_key == "normal" and (marrow_pct_val is None or marrow_pct_val < 30)
    cr_marrow_done   = marrow_key != "not_done"
    cr_A = cr_nodes and cr_spleen and cr_liver and cr_const and cr_lymph
    cr_B = cr_plt and cr_hgb and cr_anc

    # ── Determine response ────────────────────────────────────────────────────
    notes_list = []
    response = "SD"
    desc = ""

    if is_pd:
        response = "PD"
        desc = "Progresivní onemocnění — splněno ≥1 kritérium pro progresi"
        for r in pd_reasons:
            notes_list.append("Kritérium progrese: " + r)
    elif cr_A and cr_B and cr_marrow_normal and cr_marrow_done:
        response = "CR"
        desc = "Kompletní remise — všechna absolutní kritéria A i B splněna, kostní dřeň normální"
    elif cr_A and cr_B and not cr_marrow_done:
        response = "CR"
        desc = "Možná kompletní remise — splněna A i B kritéria (nutné potvrzení biopsií KD)"
        notes_list.append("Pro potvrzení CR je nutná biopsie kostní dřeně: ≤30% lymfocytů, bez lymfoidních nodulů")
    elif cr_A and cr_B and marrow_key == "nodules":
        response = "nPR"
        desc = "Nodulární parciální remise — kritéria CR v krvi splněna, ale přítomny lymfoidní noduly v KD"
    elif cr_A and not (cr_plt and cr_hgb and cr_anc):
        response = "CRi"
        desc = "CR s neúplnou obnovou dřeně — splněna A kritéria CR, přetrvává cytopenie (pravděpodobně léková toxicita)"
    elif pr_met and not lymphocytosis:
        response = "PR"
        if single_param_rule and total_abnormal == 1:
            desc = "Parciální remise — při pouze 1 abnormálním parametru před léčbou stačí zlepšení 1 parametru"
        else:
            desc = f"Parciální remise — zlepšení ≥{pr_A_threshold} parametrů skupiny A a ≥1 parametru skupiny B (A={A_met}, B={B_met})"
    elif pr_met and lymphocytosis:
        response = "PR-L"
        desc = f"Parciální remise s lymfocytózou — splněna kritéria PR (A: {A_met}/{pr_A_threshold}, B: {B_met}/1), lymfocyty zvýšeny redistribucí"
        notes_list.append("Lymfocytóza u inhibitorů kináz (ibrutinib aj.) sama o sobě není PD — jde o redistribuci CLL buněk z lymfoidní tkáně do krve (iwCLL 2018 sec. 5.3.4)")
    else:
        response = "SD"
        desc = f"Stabilní onemocnění — nesplněna kritéria pro CR ani PR, bez progrese (A: {A_met}/{A_abnormal}, B: {B_met}/{B_abnormal})"
        if A_abnormal == 0 and B_abnormal == 0:
            notes_list.append("Žádné parametry nebyly označeny jako patologické při baseline — zkontrolujte baseline hodnoty")

    # ── Render result ─────────────────────────────────────────────────────────
    st.write("")
    st.markdown("---")
    st.subheader("Výsledek hodnocení")

    css_key = {"CR": "CR", "CRi": "CRi", "PR": "PR", "PR-L": "PRL", "nPR": "PR", "PD": "PD", "SD": "SD"}.get(response, "SD")
    st.markdown(f"""
    <div class="result-box result-{css_key}">
        <div class="result-label">Hodnocení odpovědi na léčbu (iwCLL 2018)</div>
        <div class="result-value">{response}</div>
        <div class="result-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Breakdown ─────────────────────────────────────────────────────────────
    with st.expander("📊 Detailní rozbor parametrů", expanded=True):
        st.markdown(f"""
        <div style="background:#f0f4ff;border-radius:6px;padding:8px 12px;font-size:0.82rem;margin-bottom:0.8rem">
            Patologické parametry při baseline: <b>A: {A_abnormal} | B: {B_abnormal}</b>
            {'&nbsp; → &nbsp;<span style="color:#856404">Platí pravidlo jediného parametru</span>' if single_param_rule else ''}
            &nbsp;&nbsp;|&nbsp;&nbsp; Splněná zlepšení: <b>A: {A_met}/{A_abnormal} | B: {B_met}/{B_abnormal}</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Skupina A**")
        badge_labels = {"met": "Zlepšeno", "notmet": "Nezlepšeno", "warn": "Pozor", "na": "N/A"}
        for name, val, status, note in a_items:
            note_html = f'<br><span style="font-size:0.72rem;color:#856404">{note}</span>' if note else ""
            st.markdown(f"""
            <div class="bd-row">
                <div><b>{name}</b>{note_html}</div>
                <div style="text-align:right">{val}&nbsp;&nbsp;{badge_html(status, badge_labels.get(status,"N/A"))}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"<div style='font-size:0.78rem;color:#0056b3;padding:4px 0;font-weight:600'>Skupina A — abnormálních při BL: {A_abnormal} | zlepšeno: {A_met} | požadováno: {pr_A_threshold}</div>", unsafe_allow_html=True)

        st.markdown("**Skupina B**")
        for name, val, status, note in b_items:
            note_html = f'<br><span style="font-size:0.72rem;color:#856404">{note}</span>' if note else ""
            st.markdown(f"""
            <div class="bd-row">
                <div><b>{name}</b>{note_html}</div>
                <div style="text-align:right">{val}&nbsp;&nbsp;{badge_html(status, badge_labels.get(status,"N/A"))}</div>
            </div>
            """, unsafe_allow_html=True)

        auto_note = " <span style='color:#555'>(vše normální → B automaticky splněno)</span>" if B_all_normal else ""
        st.markdown(f"<div style='font-size:0.78rem;color:#155724;padding:4px 0;font-weight:600'>Skupina B — abnormálních při BL: {B_abnormal} | zlepšeno: {B_met} | požadováno: {pr_B_threshold}{auto_note}</div>", unsafe_allow_html=True)

    # Notes
    if notes_list:
        st.markdown('<div class="note-warn">' + "<br><br>".join(["⚠ " + n for n in notes_list]) + '</div>', unsafe_allow_html=True)

    # ── Documentation output ──────────────────────────────────────────────────
    st.write("")
    st.subheader("📝 Výstup pro dokumentaci")

    resp_labels = {
        "CR": "kompletní remise (CR)",
        "CRi": "kompletní remise s neúplnou obnovou dřeně (CRi)",
        "PR": "parciální remise (PR)",
        "PR-L": "parciální remise s lymfocytózou (PR-L)",
        "nPR": "nodulární parciální remise (nPR)",
        "PD": "progrese onemocnění (PD)",
        "SD": "stabilní onemocnění (SD)"
    }

    today_str = date.today().strftime("%-d. %-m. %Y")
    doc_parts = [f"Hodnocení odpovědi ({today_str}): Jedná se o {resp_labels.get(response, response)}."]

    reasons = []
    if spd_pct is not None and has_any_ln:
        if spd_pct <= -50:
            reasons.append(f"pokles SPD lymfatických uzlin o {abs(spd_pct):.0f}% ({baseline_spd:.2f} → {current_spd:.2f} cm²)")
        elif spd_pct >= 50:
            reasons.append(f"nárůst SPD o {spd_pct:.0f}% (progrese uzlin)")
        else:
            reasons.append(f"změna SPD o {spd_pct:+.0f}%")
    elif not has_any_ln and all_nodes_small:
        reasons.append("normalizace lymfatických uzlin (všechny LU ≤1.5 cm)")

    if lymph_curr_val is not None and lymph_base_abn:
        if lymph_curr_val < 4:
            reasons.append(f"normalizace lymfocytů ({lymph_base_val} → {lymph_curr_val} ×10⁹/L)")
        elif lymphocytosis:
            reasons.append(f"redistribuční lymfocytóza ({lymph_curr_val} ×10⁹/L)")

    if spleen_curr_val is not None and spleen_base_abn:
        sp_pct = (spleen_base_val - spleen_curr_val) / spleen_base_val * 100
        if sp_pct >= 50 or spleen_curr_val < 13:
            reasons.append(f"redukce splenomegalie ({spleen_base_val} → {spleen_curr_val} cm)")
        elif spleen_curr_val > spleen_base_val * 1.5:
            reasons.append(f"progrese splenomegalie ({spleen_base_val} → {spleen_curr_val} cm)")

    if liver_base_abn and liver_curr_normal:
        reasons.append("normalizace hepatomegalie")
    elif liver_base_abn and not liver_curr_normal:
        reasons.append("přetrvávající hepatomegalie")

    if const_base_abn and const_curr_none:
        reasons.append("vymizení konstitučních příznaků")

    if plt_curr_val is not None:
        if plt_base_abn and plt_curr_val >= 100:
            reasons.append(f"normalizace trombocytů ({plt_base_val} → {plt_curr_val} ×10⁹/L)")
        elif plt_base_abn and plt_curr_val < (plt_base_val or 0) * 0.5:
            reasons.append(f"pokles trombocytů ({plt_base_val} → {plt_curr_val} ×10⁹/L)")
        elif not plt_base_abn and plt_curr_val >= 100:
            reasons.append(f"trombocyty v normě ({plt_curr_val} ×10⁹/L)")

    if hgb_curr_val is not None:
        if hgb_base_abn and hgb_curr_val >= 11:
            reasons.append(f"normalizace hemoglobinu ({hgb_base_val} → {hgb_curr_val} g/dL)")
        elif hgb_base_val is not None and (hgb_base_val - hgb_curr_val) >= 2:
            reasons.append(f"pokles Hb ≥2 g/dL ({hgb_base_val} → {hgb_curr_val} g/dL)")
        elif not hgb_base_abn and hgb_curr_val >= 11:
            reasons.append(f"hemoglobin v normě ({hgb_curr_val} g/dL)")

    if anc_curr_val is not None:
        if anc_base_abn and anc_curr_val >= 1500:
            reasons.append(f"normalizace neutrofilů ({anc_base_val} → {anc_curr_val} ×10⁹/L)")
        elif not anc_base_abn and anc_curr_val >= 1500:
            reasons.append(f"neutrofily v normě ({anc_curr_val} ×10⁹/L)")

    marrow_doc = {
        "normal": "normální nález v kostní dřeni",
        "cll_cells": "přítomnost CLL buněk v kostní dřeni",
        "nodules": "lymfoidní noduly v kostní dřeni",
        "not_done": "biopsie kostní dřeně nebyla provedena"
    }
    if marrow_key in marrow_doc:
        reasons.append(marrow_doc[marrow_key])

    for r in pd_reasons:
        reasons.append(r)

    if reasons:
        doc_parts.append("Odůvodnění: " + ", ".join(reasons) + ".")

    doc_parts.append("Hodnocení provedeno dle iwCLL 2018 guidelines.")
    doc_text = " ".join(doc_parts)

    st.text_area("", value=doc_text, height=110, key="doc_out")
    st.caption("💡 Text zkopírujte výběrem myší nebo Ctrl+A / Ctrl+C.")
