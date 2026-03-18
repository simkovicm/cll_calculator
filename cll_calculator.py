"""
CLL Response Assessment Calculator v3
iwCLL 2018 — světlý layout, vstupy nahoře, výstup dole
"""

import streamlit as st
from datetime import date
import json
import io

st.set_page_config(
    page_title="CLL Kalkulátor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #f5f7fa;
    color: #1a2744;
}

/* ── All input fields: white background, dark text ── */
input[type="number"],
input[type="text"],
input[type="date"],
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input,
[data-baseweb="input"] input {
    background-color: #ffffff !important;
    color: #1a2744 !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 6px !important;
    caret-color: #1a2744 !important;
}
input::placeholder { color: #94a3b8 !important; }

/* Selectbox */
[data-baseweb="select"] > div:first-child {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 6px !important;
}
[data-baseweb="select"] [data-testid="stMarkdownContainer"],
[data-baseweb="select"] div,
[data-baseweb="select"] span {
    color: #1a2744 !important;
}

/* Labels */
label, .stSelectbox label, .stNumberInput label,
.stTextInput label, .stDateInput label, .stRadio label {
    color: #374151 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}

/* Hide sidebar toggle */
[data-testid="collapsedControl"] { display: none; }
section[data-testid="stSidebar"] { display: none; }

/* ── Header ── */
.main-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #102a4c 100%);
    padding: 1.2rem 2rem; border-radius: 10px;
    margin-bottom: 1.5rem; border-left: 5px solid #3b82f6;
}
.main-header h1 { color: white; font-size: 1.5rem; font-weight: 700; margin: 0; }
.main-header p  { color: #94a3b8; margin: 0.2rem 0 0; font-size: 0.82rem; }

/* ── Cards ── */
.card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 1.2rem 1.4rem;
    margin-bottom: 1rem; box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.ct-a    { font-size:0.8rem;font-weight:700;color:#1d4ed8;border-left:4px solid #3b82f6;padding-left:10px;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:.5px; }
.ct-b    { font-size:0.8rem;font-weight:700;color:#15803d;border-left:4px solid #22c55e;padding-left:10px;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:.5px; }
.ct-warn { font-size:0.8rem;font-weight:700;color:#92400e;border-left:4px solid #f59e0b;padding-left:10px;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:.5px; }
.ct-info { font-size:0.8rem;font-weight:700;color:#1e3a5f;border-left:4px solid #102a5a;padding-left:10px;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:.5px; }

/* SPD pill */
.spd-pill { display:inline-block;border-radius:20px;padding:3px 14px;font-size:0.82rem;font-weight:600;margin-top:4px; }
.spd-green { background:#dcfce7;color:#15803d; }
.spd-red   { background:#fee2e2;color:#991b1b; }
.spd-yellow{ background:#fef9c3;color:#713f12; }

/* ── Result box ── */
.result-box { border-radius:14px;padding:2rem;text-align:center;margin:1rem 0;border:2px solid; }
.result-label { font-size:0.7rem;text-transform:uppercase;letter-spacing:3px;opacity:.7;margin-bottom:.4rem; }
.result-value { font-size:3.5rem;font-weight:800;line-height:1;margin:.3rem 0; }
.result-desc  { font-size:.85rem;line-height:1.5;margin-top:.5rem; }
.result-CR  { background:#dcfce7;border-color:#16a34a;color:#14532d; }
.result-CRi { background:#dbeafe;border-color:#2563eb;color:#1e3a8a; }
.result-PR  { background:#dbeafe;border-color:#3b82f6;color:#1e40af; }
.result-PRL { background:#f3e8ff;border-color:#9333ea;color:#581c87; }
.result-nPR { background:#e0f2fe;border-color:#0284c7;color:#0c4a6e; }
.result-SD  { background:#fefce8;border-color:#ca8a04;color:#713f12; }
.result-PD  { background:#fee2e2;border-color:#dc2626;color:#7f1d1d; }

/* Breakdown */
.bd-row { display:flex;justify-content:space-between;align-items:center;padding:7px 4px;border-bottom:1px solid #f1f5f9;font-size:.83rem; }
.bmet    { background:#dcfce7;color:#166534;padding:2px 10px;border-radius:4px;font-size:.73rem;font-weight:600; }
.bnotmet { background:#fee2e2;color:#991b1b;padding:2px 10px;border-radius:4px;font-size:.73rem;font-weight:600; }
.bwarn   { background:#fef9c3;color:#713f12;padding:2px 10px;border-radius:4px;font-size:.73rem;font-weight:600; }
.bna     { background:#f1f5f9;color:#64748b;padding:2px 10px;border-radius:4px;font-size:.73rem; }
.note-w  { background:#fef9c3;border:1px solid #fcd34d;border-radius:8px;padding:.8rem;font-size:.8rem;color:#713f12;line-height:1.6;margin-top:.5rem; }
.info-bar{ background:#eff6ff;border:1px solid #bfdbfe;border-radius:7px;padding:7px 12px;font-size:.8rem;color:#1e40af;margin-bottom:.8rem; }

/* History */
.hist-table { width:100%;border-collapse:collapse;font-size:.82rem; }
.hist-table th { background:#1e3a5f;color:white;padding:7px 10px;text-align:left; }
.hist-table td { padding:6px 10px;border-bottom:1px solid #e2e8f0; }
.hist-table tr:nth-child(even) td { background:#f8fafc; }
.chip-CR  { background:#dcfce7;color:#166534;border-radius:20px;padding:2px 10px;font-weight:700;font-size:.8rem; }
.chip-PR  { background:#dbeafe;color:#1e40af;border-radius:20px;padding:2px 10px;font-weight:700;font-size:.8rem; }
.chip-PRL { background:#f3e8ff;color:#6b21a8;border-radius:20px;padding:2px 10px;font-weight:700;font-size:.8rem; }
.chip-CRi { background:#dbeafe;color:#1e3a8a;border-radius:20px;padding:2px 10px;font-weight:700;font-size:.8rem; }
.chip-nPR { background:#e0f2fe;color:#0c4a6e;border-radius:20px;padding:2px 10px;font-weight:700;font-size:.8rem; }
.chip-SD  { background:#fefce8;color:#713f12;border-radius:20px;padding:2px 10px;font-weight:700;font-size:.8rem; }
.chip-PD  { background:#fee2e2;color:#7f1d1d;border-radius:20px;padding:2px 10px;font-weight:700;font-size:.8rem; }
</style>
""", unsafe_allow_html=True)

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

# ══════════════════════════════════════════════════════════════════════════════
#  CORE LOGIC
# ══════════════════════════════════════════════════════════════════════════════
def compute(p):
    def v(k): return p.get(k)
    baseline_spd=p.get("baseline_spd") or 0
    current_spd =p.get("current_spd")  or 0
    has_any_ln  =p.get("has_any_ln",False)
    all_nodes_small=p.get("all_nodes_small",True)
    spd_pct=None
    if has_any_ln and baseline_spd>0:
        spd_pct=(current_spd-baseline_spd)/baseline_spd*100

    is_pd,pd_r=False,[]
    if spd_pct is not None and spd_pct>=50: is_pd=True;pd_r.append("SPD vzrostlo ≥50%")
    if v("new_lesions"):  is_pd=True;pd_r.append("Nové lymfatické léze")
    if v("new_cytopenia"):is_pd=True;pd_r.append("Nová cytopenie")
    sp_b,sp_c=v("spleen_base"),v("spleen_curr")
    if sp_b and sp_c and sp_c>sp_b*1.5: is_pd=True;pd_r.append("Slezina vzrostla ≥50%")
    hb,hc=v("hgb_base"),v("hgb_curr")
    if hb and hc and (hb-hc)>=2: is_pd=True;pd_r.append("Hb poklesl ≥2 g/dL")
    pb,pc=v("plt_base"),v("plt_curr")
    if pb and pc and pc<pb*0.5: is_pd=True;pd_r.append("Trombocyty poklesly ≥50%")
    if v("marrow_key")=="increasing": is_pd=True;pd_r.append("Nárůst CLL buněk v dřeni")

    A_met=0;A_abn=0;a_items=[];lymphocytosis=False
    ln_abn=has_any_ln and baseline_spd>0
    if has_any_ln:
        if ln_abn and spd_pct is not None:
            A_abn+=1;s="met" if spd_pct<=-50 else "notmet"
            if s=="met":A_met+=1
            a_items.append(("Lymf. uzliny (SPD)",f"{spd_pct:+.1f}% (BL:{baseline_spd:.2f} cm²)",s,None))
        else:
            a_items.append(("Lymf. uzliny (SPD)",f"SPD:{current_spd:.2f} cm²","na","Bez baseline"))
    else:
        a_items.append(("Lymf. uzliny (SPD)","—","na",None))

    lb,lc=v("lymph_base"),v("lymph_curr");lb_abn=lb is not None and lb>5
    if lc is not None:
        if lb_abn:
            A_abn+=1;lp=(lb-lc)/lb*100
            if lc<4:A_met+=1;ls="met"
            elif lp>=50:A_met+=1;ls="met"
            elif lc>=5:lymphocytosis=True;ls="warn"
            else:ls="notmet"
            a_items.append(("Lymfocyty",f"{lc} ×10⁹/L",ls,None))
        elif lb is not None:
            a_items.append(("Lymfocyty",f"{lc} ×10⁹/L","na","Normální při baseline"))
        else:
            ls2="warn" if lc>=5 else "na"
            if lc>=5:lymphocytosis=True
            a_items.append(("Lymfocyty",f"{lc} ×10⁹/L",ls2,"Baseline nezadán"))
    else:
        a_items.append(("Lymfocyty","—","na",None))

    sp_abn=sp_b is not None and sp_b>=13
    if sp_c is not None:
        if sp_abn:
            A_abn+=1;spp=(sp_b-sp_c)/sp_b*100
            ss="met" if(spp>=50 or sp_c<13) else "notmet"
            if ss=="met":A_met+=1
            a_items.append(("Slezina",f"{sp_c} cm",ss,None))
        else:
            a_items.append(("Slezina",f"{sp_c} cm","na","Normální při baseline (<13 cm)"))
    else:
        a_items.append(("Slezina","—","na",None))

    lv_abn=v("liver_base_abn");lv_n=v("liver_curr_normal")
    if lv_abn:
        A_abn+=1;lvs="met" if lv_n else "notmet"
        if lvs=="met":A_met+=1
    else:lvs="na"
    a_items.append(("Játra","Normální" if lv_n else "Hepatomegalie",lvs,"Normální při baseline" if not lv_abn else None))

    cs_abn=v("const_base_abn");cs_n=v("const_curr_none")
    if cs_abn:
        A_abn+=1;css="met" if cs_n else "notmet"
        if css=="met":A_met+=1
    else:css="na" if cs_n else "notmet"
    a_items.append(("Konst. příznaky","Žádné" if cs_n else "Přítomny",css,"Nepřítomny při baseline" if not cs_abn else None))

    B_met=0;B_abn=0;b_items=[]
    pb_abn=pb is not None and pb<100
    if pc is not None:
        if pb_abn:
            B_abn+=1;pts="met" if(pc>=100 or (pc-pb)/pb*100>=50) else "notmet"
            if pts=="met":B_met+=1
        else:pts="na" if(pb is None or pc>=100) else "notmet"
        b_items.append(("Trombocyty",f"{pc} ×10⁹/L",pts,"Normální při baseline" if(pb is not None and not pb_abn) else None))
    else:
        b_items.append(("Trombocyty","—","na",None))

    hb_abn=hb is not None and hb<11
    if hc is not None:
        if hb_abn:
            B_abn+=1;hbs="met" if(hc>=11 or (hc-hb)/hb*100>=50) else "notmet"
            if hbs=="met":B_met+=1
        else:hbs="na" if(hb is None or hc>=11) else "notmet"
        b_items.append(("Hemoglobin",f"{hc} g/dL",hbs,"Normální při baseline" if(hb is not None and not hb_abn) else None))
    else:
        b_items.append(("Hemoglobin","—","na",None))

    ab,ac=v("anc_base"),v("anc_curr");ab_abn=ab is not None and ab<1500
    if ac is not None:
        if ab_abn:
            B_abn+=1;acs="met" if(ac>=1500 or (ac-ab)/ab*100>=50) else "notmet"
            if acs=="met":B_met+=1
        else:acs="na" if(ab is None or ac>=1500) else "notmet"
        b_items.append(("ANC (neutrofily)",f"{ac} ×10⁹/L",acs,"Normální při baseline" if(ab is not None and not ab_abn) else None))
    else:
        b_items.append(("ANC (neutrofily)","—","na",None))

    mk=v("marrow_key") or "not_done"
    if mk=="normal":     B_met+=1;B_abn+=1;ms="met";mn=None
    elif mk=="not_done": B_met+=1;B_abn+=1;ms="warn";mn="Nebyla provedena — počítá se jako splněno (iwCLL 2018)"
    elif mk in("cll_cells","nodules"):B_abn+=1;ms="warn";mn=None
    elif mk=="increasing":B_abn+=1;ms="notmet";mn=None
    else:ms="na";mn=None
    b_items.append(("Kostní dřeň",{"not_done":"Nebyla provedena","normal":"Normální","cll_cells":"CLL buňky/noduly","nodules":"Lymfoidní noduly","increasing":"Nárůst CLL"}.get(mk,"—"),ms,mn))

    B_all_norm=B_abn==0;total_abn=A_abn+B_abn;single=total_abn<=1
    pA_thr=1 if single else 2;pB_thr=0 if single else 1
    B_sat=B_met>=1 or B_all_norm
    pr_met=(A_met>=1 or B_met>=1) if single else(A_met>=pA_thr and B_sat)

    cr_nodes=not has_any_ln or all_nodes_small
    cr_A=cr_nodes and(sp_c is None or sp_c<13) and lv_n and cs_n and(lc is not None and lc<4)
    cr_B=(pc is not None and pc>=100) and(hc is not None and hc>=11) and(ac is not None and ac>=1500)
    cr_mk_ok=mk=="normal" and(v("marrow_pct") is None or v("marrow_pct")<30)
    cr_mk_done=mk!="not_done"

    notes=[];response="SD";desc=""
    if is_pd:
        response="PD";desc="Progresivní onemocnění — splněno ≥1 kritérium pro progresi"
        for r in pd_r:notes.append("Kritérium: "+r)
    elif cr_A and cr_B and cr_mk_ok and cr_mk_done:
        response="CR";desc="Kompletní remise — všechna kritéria A i B splněna, KD normální"
    elif cr_A and cr_B and not cr_mk_done:
        response="CR";desc="Možná CR — splněna A i B kritéria (nutno potvrdit biopsií KD)"
        notes.append("Pro potvrzení CR nutná biopsie KD: ≤30% lymfocytů, bez lymfoidních nodulů")
    elif cr_A and cr_B and mk=="nodules":
        response="nPR";desc="Nodulární parciální remise — CR v krvi, lymfoidní noduly v KD"
    elif cr_A and not(pc is not None and pc>=100 and hc is not None and hc>=11 and ac is not None and ac>=1500):
        response="CRi";desc="CR s neúplnou obnovou dřeně — splněna A kritéria, přetrvává cytopenie"
    elif pr_met and not lymphocytosis:
        response="PR"
        desc="Parciální remise — pravidlo jediného parametru" if(single and total_abn==1) else f"Parciální remise — zlepšení ≥{pA_thr} param. A a ≥1 param. B"
    elif pr_met and lymphocytosis:
        response="PR-L";desc="Parciální remise s lymfocytózou — kritéria PR splněna, redistribuce lymfocytů"
        notes.append("Lymfocytóza u inhibitorů kináz sama o sobě není PD — redistribuce (iwCLL 2018 sec. 5.3.4)")
    else:
        response="SD";desc=f"Stabilní onemocnění — nesplněna CR/PR kritéria (A:{A_met}/{A_abn}, B:{B_met}/{B_abn})"
        if A_abn==0 and B_abn==0:notes.append("Žádné parametry nebyly patologické při baseline")

    rl={"CR":"kompletní remise (CR)","CRi":"CR s neúplnou obnovou dřeně (CRi)","PR":"parciální remise (PR)",
        "PR-L":"parciální remise s lymfocytózou (PR-L)","nPR":"nodulární parciální remise (nPR)",
        "PD":"progrese onemocnění (PD)","SD":"stabilní onemocnění (SD)"}
    today_s=date.today().strftime("%-d. %-m. %Y")
    doc_parts=[f"Hodnocení odpovědi ({today_s}): Jedná se o {rl.get(response,response)}."]
    reas=[]
    if spd_pct is not None and has_any_ln:
        if spd_pct<=-50:reas.append(f"pokles SPD o {abs(spd_pct):.0f}% ({baseline_spd:.2f}→{current_spd:.2f} cm²)")
        elif spd_pct>=50:reas.append(f"nárůst SPD o {spd_pct:.0f}%")
        else:reas.append(f"změna SPD o {spd_pct:+.0f}%")
    if lc and lb_abn:
        if lc<4:reas.append(f"normalizace lymfocytů ({lb}→{lc} ×10⁹/L)")
        elif lymphocytosis:reas.append(f"redistribuční lymfocytóza ({lc} ×10⁹/L)")
    if sp_c and sp_abn:
        spp2=(sp_b-sp_c)/sp_b*100
        if spp2>=50 or sp_c<13:reas.append(f"redukce splenomegalie ({sp_b}→{sp_c} cm)")
    if lv_abn and lv_n:reas.append("normalizace hepatomegalie")
    if cs_abn and cs_n:reas.append("vymizení konstitučních příznaků")
    if pc and pb_abn and pc>=100:reas.append(f"normalizace trombocytů ({pb}→{pc} ×10⁹/L)")
    if hc and hb_abn and hc>=11:reas.append(f"normalizace hemoglobinu ({hb}→{hc} g/dL)")
    if ac and ab_abn and ac>=1500:reas.append(f"normalizace neutrofilů ({ab}→{ac} ×10⁹/L)")
    mk_d={"normal":"normální KD","cll_cells":"CLL buňky v KD","nodules":"lymfoidní noduly v KD","not_done":"KD nebyla provedena"}
    if mk in mk_d:reas.append(mk_d[mk])
    for r in pd_r:reas.append(r)
    if reas:doc_parts.append("Odůvodnění: "+", ".join(reas)+".")
    doc_parts.append("Hodnocení dle iwCLL 2018 guidelines.")

    return {"response":response,"desc":desc,"notes":notes,
            "a_items":a_items,"b_items":b_items,
            "A_met":A_met,"A_abn":A_abn,"B_met":B_met,"B_abn":B_abn,
            "pA_thr":pA_thr,"pB_thr":pB_thr,"B_all_norm":B_all_norm,"single":single,
            "doc_text":" ".join(doc_parts),
            "spd_pct":spd_pct,"baseline_spd":baseline_spd,"current_spd":current_spd}

# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="main-header">
  <h1>🩺 CLL Response Assessment Calculator</h1>
  <p>Hodnocení odpovědi na léčbu dle iwCLL 2018 Guidelines &nbsp;|&nbsp; Výsledek se aktualizuje automaticky</p>
</div>
""", unsafe_allow_html=True)

tab_input, tab_history, tab_export = st.tabs(["📋 Hodnocení", "📅 Historie", "📄 Export"])

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1
# ══════════════════════════════════════════════════════════════════════════════
with tab_input:

    # Pacient
    st.markdown('<div class="card"><div class="ct-info">👤 Pacient a studie</div>', unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    pat_id    =c1.text_input("ID / jméno pacienta",     value="", placeholder="CLL-001")
    study_name=c2.text_input("Název studie / protokolu", value="", placeholder="MAJIC")
    tp_label  =c3.text_input("Časový bod",               value="", placeholder="C3, M12...")
    eval_date =c4.date_input("Datum hodnocení", value=date.today())
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Skupina A — klinické parametry")

    # LN
    st.markdown('<div class="card"><div class="ct-a">🔵 Lymfatické uzliny — SPD</div>', unsafe_allow_html=True)
    ln_mode=st.radio("Způsob zadání",["Jednotlivé uzliny","Přímé SPD"],horizontal=True,key="ln_mode")
    baseline_spd=0.0;current_spd=0.0;has_any_ln=False;all_nodes_small=True

    if ln_mode=="Jednotlivé uzliny":
        n_nodes=st.number_input("Počet uzlin (1–6)",1,6,1,key="n_nodes")
        for i in range(int(n_nodes)):
            cols=st.columns(5)
            cols[0].markdown(f"<div style='padding-top:30px;font-size:.82rem;color:#475569;font-weight:500'>Uzlina {i+1}</div>",unsafe_allow_html=True)
            b1=cols[1].number_input("BL d₁ (cm)",0.0,step=0.1,key=f"b1_{i}",format="%.1f")
            b2=cols[2].number_input("BL d₂ (cm)",0.0,step=0.1,key=f"b2_{i}",format="%.1f")
            c1v=cols[3].number_input("Akt. d₁ (cm)",0.0,step=0.1,key=f"c1_{i}",format="%.1f")
            c2v=cols[4].number_input("Akt. d₂ (cm)",0.0,step=0.1,key=f"c2_{i}",format="%.1f")
            ppdb=b1*b2 if b1>0 and b2>0 else None
            ppdc=c1v*c2v if c1v>0 and c2v>0 else None
            if ppdb:baseline_spd+=ppdb;has_any_ln=True
            if ppdc:current_spd+=ppdc
            if c1v>1.5 or c2v>1.5:all_nodes_small=False
    else:
        cc1,cc2=st.columns(2)
        b_spd=cc1.number_input("SPD baseline (cm²)",0.0,step=0.01,key="spd_base_d",format="%.2f")
        c_spd=cc2.number_input("SPD aktuálně (cm²)",0.0,step=0.01,key="spd_curr_d",format="%.2f")
        if b_spd>0:
            has_any_ln=True;baseline_spd=b_spd;current_spd=c_spd;all_nodes_small=(c_spd==0)

    if has_any_ln and baseline_spd>0:
        pct_ln=(current_spd-baseline_spd)/baseline_spd*100
        cls="spd-green" if pct_ln<=-50 else("spd-red" if pct_ln>=50 else "spd-yellow")
        ic="🟢" if pct_ln<=-50 else("🔴" if pct_ln>=50 else "🟡")
        st.markdown(f'<span class="spd-pill {cls}">{ic} ΔSPD: {pct_ln:+.1f}% &nbsp;|&nbsp; {baseline_spd:.2f} → {current_spd:.2f} cm²</span>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    # Slezina + játra + konst + lymfocyty
    st.markdown('<div class="card"><div class="ct-a">🔵 Slezina, játra, konstituční příznaky, lymfocyty</div>',unsafe_allow_html=True)
    r1=st.columns(4)
    spleen_base =r1[0].number_input("Slezina — baseline (cm)",0.0,step=0.1,key="sp_b",format="%.1f",help="Splenomegalie ≥13 cm")
    spleen_curr =r1[1].number_input("Slezina — aktuálně (cm)",0.0,step=0.1,key="sp_c",format="%.1f")
    liver_base_abn   =r1[2].selectbox("Játra — baseline", ["Normální","Hepatomegalie"],key="lv_b")=="Hepatomegalie"
    liver_curr_normal=r1[3].selectbox("Játra — aktuálně",["Normální","Hepatomegalie"],key="lv_c")=="Normální"
    r2=st.columns(4)
    const_base_abn =r2[0].selectbox("Konst. příznaky — baseline", ["Žádné","Přítomny"],key="cs_b")=="Přítomny"
    const_curr_none=r2[1].selectbox("Konst. příznaky — aktuálně",["Žádné","Přítomny"],key="cs_c")=="Žádné"
    lymph_base=r2[2].number_input("Lymfocyty — baseline (×10⁹/L)",0.0,step=0.1,key="lb",format="%.1f",help="Lymfocytóza >5")
    lymph_curr=r2[3].number_input("Lymfocyty — aktuálně (×10⁹/L)",0.0,step=0.1,key="lc",format="%.1f")
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Skupina B — hematologické parametry")

    # CBC
    st.markdown('<div class="card"><div class="ct-b">🟢 Krevní obraz</div>',unsafe_allow_html=True)
    bc=st.columns(6)
    plt_base=bc[0].number_input("PLT — baseline (×10⁹/L)",0.0,step=1.0,key="pb",format="%.0f",help="Abnormální <100")
    plt_curr=bc[1].number_input("PLT — aktuálně",          0.0,step=1.0,key="pc",format="%.0f")
    hgb_base=bc[2].number_input("Hgb — baseline (g/dL)",  0.0,step=0.1,key="hb",format="%.1f",help="Abnormální <11")
    hgb_curr=bc[3].number_input("Hgb — aktuálně",          0.0,step=0.1,key="hc",format="%.1f")
    anc_base=bc[4].number_input("ANC — baseline (×10⁹/L)",0.0,step=1.0,key="ab",format="%.0f",help="Abnormální <1500")
    anc_curr=bc[5].number_input("ANC — aktuálně",          0.0,step=1.0,key="ac",format="%.0f")
    st.markdown('</div>',unsafe_allow_html=True)

    # Bone marrow
    st.markdown('<div class="card"><div class="ct-b">🟢 Kostní dřeň</div>',unsafe_allow_html=True)
    mc=st.columns(2)
    marrow_opts={"Nebyla provedena":"not_done","Normální":"normal",
                 "CLL buňky / B-lymfoidní noduly":"cll_cells",
                 "Lymfoidní noduly (bez CLL infiltrace)":"nodules",
                 "Nárůst CLL buněk (≥50%) v opakovaných biopsiích":"increasing"}
    marrow_sel=mc[0].selectbox("Výsledek biopsie KD",list(marrow_opts.keys()),key="marrow")
    marrow_key=marrow_opts[marrow_sel]
    marrow_pct_v=mc[1].number_input("% lymfocytů v KD (pro CR: <30%)",0,100,step=1,key="mpct")
    st.markdown('</div>',unsafe_allow_html=True)

    # New lesions
    st.markdown('<div class="card"><div class="ct-warn">⚠️ Nové léze / nová cytopenie</div>',unsafe_allow_html=True)
    wc=st.columns(2)
    new_lesions  =wc[0].selectbox("Nové lymfatické uzliny nebo extranodální léze",["Ne","Ano"],key="nl")=="Ano"
    new_cytopenia=wc[1].selectbox("Nová cytopenie nesouvisející s léčbou",         ["Ne","Ano"],key="nc")=="Ano"
    st.markdown('</div>',unsafe_allow_html=True)

    # Compute
    def _val(v): return v if v and v>0 else None

    params={
        "baseline_spd":baseline_spd,"current_spd":current_spd,
        "has_any_ln":has_any_ln,"all_nodes_small":all_nodes_small,
        "spleen_base":_val(spleen_base),"spleen_curr":_val(spleen_curr),
        "liver_base_abn":liver_base_abn,"liver_curr_normal":liver_curr_normal,
        "const_base_abn":const_base_abn,"const_curr_none":const_curr_none,
        "lymph_base":_val(lymph_base),"lymph_curr":_val(lymph_curr),
        "plt_base":_val(plt_base),"plt_curr":_val(plt_curr),
        "hgb_base":_val(hgb_base),"hgb_curr":_val(hgb_curr),
        "anc_base":_val(anc_base),"anc_curr":_val(anc_curr),
        "marrow_key":marrow_key,"marrow_pct":_val(float(marrow_pct_v)) if marrow_pct_v else None,
        "new_lesions":new_lesions,"new_cytopenia":new_cytopenia,
    }
    res=compute(params)
    st.session_state["result"]=res
    st.session_state["eval_meta"]={"pat_id":pat_id,"study":study_name,"tp":tp_label,"date":str(eval_date)}

    # ─────────────────── RESULTS ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Výsledek hodnocení")

    css_k={"CR":"CR","CRi":"CRi","PR":"PR","PR-L":"PRL","nPR":"nPR","PD":"PD","SD":"SD"}.get(res["response"],"SD")
    st.markdown(f"""
    <div class="result-box result-{css_k}">
      <div class="result-label">Hodnocení odpovědi dle iwCLL 2018</div>
      <div class="result-value">{res["response"]}</div>
      <div class="result-desc">{res["desc"]}</div>
    </div>
    """,unsafe_allow_html=True)

    with st.expander("📋 Detailní rozbor parametrů",expanded=True):
        auto=""
        if res["B_all_norm"]:auto=" <span style='color:#64748b'>(vše normální → automaticky splněno)</span>"
        st.markdown(f"""
        <div class="info-bar">
          Patologické při baseline: <b>A:{res['A_abn']} | B:{res['B_abn']}</b>
          {"&nbsp;&nbsp;<span style='color:#92400e'>⚠ Pravidlo jediného parametru</span>" if res["single"] else ""}
          &nbsp;&nbsp;|&nbsp;&nbsp;Splněná zlepšení: <b>A:{res['A_met']}/{res['A_abn']} | B:{res['B_met']}/{res['B_abn']}</b>
        </div>
        """,unsafe_allow_html=True)

        bl_map={"met":"bmet","notmet":"bnotmet","warn":"bwarn","na":"bna"}
        bl_lab={"met":"✓ Zlepšeno","notmet":"✗ Nezlepšeno","warn":"⚠ Pozor","na":"— N/A"}
        ca,cb=st.columns(2)
        with ca:
            st.markdown("**Skupina A**")
            for nm,vl,s2,note in res["a_items"]:
                nh=f'<br><small style="color:#92400e">{note}</small>' if note else ""
                st.markdown(f'<div class="bd-row"><span>{nm}{nh}</span><span><b>{vl}</b>&nbsp;<span class="{bl_map[s2]}">{bl_lab[s2]}</span></span></div>',unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:.77rem;color:#1e40af;padding:5px 0;font-weight:600'>Patologické:{res['A_abn']} | Zlepšeno:{res['A_met']} | Požadováno:{res['pA_thr']}</div>",unsafe_allow_html=True)
        with cb:
            st.markdown("**Skupina B**")
            for nm,vl,s2,note in res["b_items"]:
                nh=f'<br><small style="color:#92400e">{note}</small>' if note else ""
                st.markdown(f'<div class="bd-row"><span>{nm}{nh}</span><span><b>{vl}</b>&nbsp;<span class="{bl_map[s2]}">{bl_lab[s2]}</span></span></div>',unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:.77rem;color:#15803d;padding:5px 0;font-weight:600'>Patologické:{res['B_abn']} | Zlepšeno:{res['B_met']} | Požadováno:{res['pB_thr']}{auto}</div>",unsafe_allow_html=True)

    if res["notes"]:
        st.markdown('<div class="note-w">'+"<br><br>".join(["⚠ "+n for n in res["notes"]])+'</div>',unsafe_allow_html=True)

    st.markdown("**📝 Text pro dokumentaci**")
    st.code(res["doc_text"],language=None)

    st.markdown("")
    if st.button("💾 Uložit hodnocení do historie",type="primary"):
        entry={"date":eval_date.strftime("%-d. %-m. %Y"),"tp":tp_label or "—",
               "response":res["response"],"pat_id":pat_id or "—","study":study_name or "—",
               "spd_pct":res["spd_pct"],"lymph_curr":_val(lymph_curr),
               "plt_curr":_val(plt_curr),"hgb_curr":_val(hgb_curr),"doc_text":res["doc_text"]}
        st.session_state.history.append(entry)
        st.success(f"✅ Hodnocení {res['response']} uloženo — {eval_date.strftime('%-d. %-m. %Y')}")

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — History
# ══════════════════════════════════════════════════════════════════════════════
with tab_history:
    if not st.session_state.history:
        st.info("Zatím žádná uložená hodnocení. Klikněte na 💾 Uložit v záložce Hodnocení.")
    else:
        st.markdown(f"**Celkem uložených hodnocení: {len(st.session_state.history)}**")
        chips={"CR":"chip-CR","CRi":"chip-CRi","PR":"chip-PR","PR-L":"chip-PRL","nPR":"chip-nPR","SD":"chip-SD","PD":"chip-PD"}
        rows=""
        for i,e in enumerate(st.session_state.history):
            ch=chips.get(e["response"],"chip-SD")
            spd_s=f"{e['spd_pct']:+.1f}%" if e.get("spd_pct") is not None else "—"
            rows+=f"<tr><td>{i+1}</td><td><b>{e['date']}</b></td><td>{e['tp']}</td><td><span class='{ch}'>{e['response']}</span></td><td>{spd_s}</td><td>{e['lymph_curr'] or '—'}</td><td>{e['hgb_curr'] or '—'}</td><td>{e['plt_curr'] or '—'}</td></tr>"
        st.markdown(f'<table class="hist-table"><tr><th>#</th><th>Datum</th><th>Timepoint</th><th>Odpověď</th><th>ΔSPD</th><th>Lymfocyty</th><th>Hgb</th><th>PLT</th></tr>{rows}</table>',unsafe_allow_html=True)
        try:
            import plotly.graph_objects as go
            spd_data=[(e["date"],e["tp"],e["spd_pct"]) for e in st.session_state.history if e.get("spd_pct") is not None]
            if spd_data:
                st.markdown("#### Trend ΔSPD")
                labels=[f"{d[1]} ({d[0]})" for d in spd_data]
                vals=[d[2] for d in spd_data]
                colors=["#16a34a" if v<=-50 else("#dc2626" if v>=50 else "#ca8a04") for v in vals]
                fig=go.Figure(go.Bar(x=labels,y=vals,marker_color=colors,text=[f"{v:+.1f}%" for v in vals],textposition="outside"))
                fig.add_hline(y=-50,line_dash="dash",line_color="#16a34a",annotation_text="≥50% pokles (PR)")
                fig.add_hline(y=50, line_dash="dash",line_color="#dc2626",annotation_text="≥50% nárůst (PD)")
                fig.update_layout(yaxis_title="Změna SPD (%)",plot_bgcolor="white",paper_bgcolor="white",height=320,margin=dict(t=20,b=20))
                st.plotly_chart(fig,use_container_width=True)
            if len(st.session_state.history)>1:
                rv={"CR":6,"CRi":5,"PR":4,"PR-L":3,"nPR":4,"SD":2,"PD":1}
                rc2={"CR":"#16a34a","CRi":"#2563eb","PR":"#3b82f6","PR-L":"#9333ea","nPR":"#0284c7","SD":"#ca8a04","PD":"#dc2626"}
                rl=[f"{e['tp']} ({e['date']})" for e in st.session_state.history]
                rvv=[rv.get(e["response"],2) for e in st.session_state.history]
                rcc=[rc2.get(e["response"],"#ca8a04") for e in st.session_state.history]
                rt=[e["response"] for e in st.session_state.history]
                st.markdown("#### Vývoj odpovědi")
                fig2=go.Figure(go.Scatter(x=rl,y=rvv,mode="lines+markers+text",
                    marker=dict(color=rcc,size=16),line=dict(color="#94a3b8",width=2),
                    text=rt,textposition="top center",textfont=dict(size=12,color=rcc)))
                fig2.update_layout(yaxis=dict(tickvals=list(rv.values()),ticktext=list(rv.keys()),range=[0,7]),
                    plot_bgcolor="white",paper_bgcolor="white",height=280,margin=dict(t=20,b=20),showlegend=False)
                st.plotly_chart(fig2,use_container_width=True)
        except ImportError:
            st.caption("Pro grafy: pip install plotly")
        if st.button("🗑 Vymazat historii"):
            st.session_state.history=[];st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — Export
# ══════════════════════════════════════════════════════════════════════════════
with tab_export:
    st.markdown("### 📄 Export hodnocení")
    res2=st.session_state.get("result")
    meta=st.session_state.get("eval_meta",{})
    if not res2:
        st.info("Nejprve vyplňte parametry v záložce Hodnocení.")
    else:
        exp_type=st.radio("Formát",["DOCX (Word)","JSON"],horizontal=True)
        if exp_type=="DOCX (Word)":
            try:
                from docx import Document as DocxDoc
                from docx.shared import Pt,RGBColor,Cm
                from docx.enum.text import WD_ALIGN_PARAGRAPH
                from docx.oxml.ns import qn
                from docx.oxml import OxmlElement
                def shd(cell,hex_c):
                    tc=cell._tc;pr=tc.get_or_add_tcPr()
                    s=OxmlElement('w:shd');s.set(qn('w:val'),'clear');s.set(qn('w:color'),'auto');s.set(qn('w:fill'),hex_c);pr.append(s)
                def run(para,text,bold=False,size=11,color=None):
                    r=para.add_run(text);r.bold=bold;r.font.size=Pt(size);r.font.name="Calibri"
                    if color:r.font.color.rgb=RGBColor(*color)
                    return r
                doc=DocxDoc()
                for sec in doc.sections:
                    sec.top_margin=Cm(2);sec.bottom_margin=Cm(2);sec.left_margin=Cm(2.5);sec.right_margin=Cm(2.5)
                h=doc.add_paragraph();run(h,"CLL RESPONSE ASSESSMENT",bold=True,size=16,color=(16,42,90))
                h.alignment=WD_ALIGN_PARAGRAPH.LEFT
                pf=h._p.get_or_add_pPr();pb2=OxmlElement('w:pBdr');bt=OxmlElement('w:bottom')
                bt.set(qn('w:val'),'single');bt.set(qn('w:sz'),'4');bt.set(qn('w:space'),'1');bt.set(qn('w:color'),'102A5A')
                pb2.append(bt);pf.append(pb2)
                sub=doc.add_paragraph();run(sub,"Hodnocení odpovědi na léčbu dle iwCLL 2018 Guidelines",size=10,color=(100,100,100))
                doc.add_paragraph()
                it=doc.add_table(rows=2,cols=4);it.style='Table Grid'
                for i2,(hh,vv) in enumerate(zip(["Pacient/ID","Studie","Timepoint","Datum"],
                                                 [meta.get("pat_id","—"),meta.get("study","—"),meta.get("tp","—"),meta.get("date","—")])):
                    shd(it.rows[0].cells[i2],"102A5A");run(it.rows[0].cells[i2].paragraphs[0],hh,bold=True,size=9,color=(255,255,255))
                    run(it.rows[1].cells[i2].paragraphs[0],vv,size=10)
                doc.add_paragraph()
                rc_map={"CR":(21,128,61),"CRi":(30,58,138),"PR":(29,78,216),"PR-L":(109,40,217),"nPR":(3,105,161),"SD":(133,77,14),"PD":(185,28,28)}
                rc=rc_map.get(res2["response"],(100,100,100))
                rp=doc.add_paragraph();run(rp,f"VÝSLEDEK: {res2['response']}",bold=True,size=22,color=rc);rp.alignment=WD_ALIGN_PARAGRAPH.CENTER
                dp=doc.add_paragraph();run(dp,res2["desc"],size=11);dp.alignment=WD_ALIGN_PARAGRAPH.CENTER
                doc.add_paragraph()
                doc.add_paragraph().add_run("DETAILNÍ ROZBOR PARAMETRŮ").bold=True
                all_it=[("A",n,v,s) for n,v,s,_ in res2["a_items"]]+[("B",n,v,s) for n,v,s,_ in res2["b_items"]]
                tbl=doc.add_table(rows=1,cols=4);tbl.style='Table Grid'
                for i2,hx in enumerate(["Sk.","Parametr","Hodnota","Hodnocení"]):
                    shd(tbl.rows[0].cells[i2],"102A5A");run(tbl.rows[0].cells[i2].paragraphs[0],hx,bold=True,size=9,color=(255,255,255))
                sl={"met":"✓ Zlepšeno","notmet":"✗ Nezlepšeno","warn":"⚠ Pozor","na":"— N/A"}
                sc2={"met":(21,128,61),"notmet":(185,28,28),"warn":(133,77,14),"na":(100,100,100)}
                for idx,(grp,nm,vl,s3) in enumerate(all_it):
                    row=tbl.add_row();bg="F2F4F8" if idx%2==0 else "FFFFFF"
                    for ci in range(4):shd(row.cells[ci],bg)
                    run(row.cells[0].paragraphs[0],grp,size=10);run(row.cells[1].paragraphs[0],nm,size=10)
                    run(row.cells[2].paragraphs[0],str(vl),size=10);run(row.cells[3].paragraphs[0],sl.get(s3,"—"),size=10,color=sc2.get(s3,(100,100,100)))
                doc.add_paragraph()
                if res2["notes"]:
                    doc.add_paragraph().add_run("POZNÁMKY").bold=True
                    for n2 in res2["notes"]:doc.add_paragraph(f"⚠ {n2}",style="List Bullet")
                    doc.add_paragraph()
                doc.add_paragraph().add_run("TEXT PRO DOKUMENTACI").bold=True
                run(doc.add_paragraph(),res2["doc_text"],size=11)
                buf=io.BytesIO();doc.save(buf);buf.seek(0)
                fn=f"CLL_{(meta.get('pat_id') or 'pacient').replace(' ','_')}_{meta.get('date','')}.docx"
                st.download_button("⬇️ Stáhnout DOCX",data=buf,file_name=fn,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            except ImportError:
                st.error("Nainstalujte: pip install python-docx")
            except Exception as e:
                st.error(f"Chyba: {e}")
        else:
            ed={**meta,"response":res2["response"],"desc":res2["desc"],
                "A_met":res2["A_met"],"A_abn":res2["A_abn"],"B_met":res2["B_met"],"B_abn":res2["B_abn"],
                "notes":res2["notes"],"doc_text":res2["doc_text"],"history":st.session_state.history}
            js=json.dumps(ed,ensure_ascii=False,indent=2)
            st.download_button("⬇️ Stáhnout JSON",data=js,
                file_name=f"CLL_{meta.get('pat_id','export')}_{meta.get('date','')}.json",mime="application/json")
            st.code(js,language="json")
