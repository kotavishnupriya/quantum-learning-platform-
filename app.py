import streamlit as st
import pandas as pd
import json
import os
import altair as alt
from datetime import datetime
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Quantum Learning Platform",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# TYPOGRAPHY PRESETS & CUSTOM UI / STYLING INJECTION
# ============================================================

FONT_PRESETS = {
    "🚀 Quantum Cyber (Space Grotesk + Inter)": {
        "heading": "'Space Grotesk', sans-serif",
        "body": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "mono": "'JetBrains Mono', monospace"
    },
    "🌌 Futuristic Neon (Syne + Plus Jakarta)": {
        "heading": "'Syne', sans-serif",
        "body": "'Plus Jakarta Sans', sans-serif",
        "mono": "'Fira Code', monospace"
    },
    "💎 Geometric Tech (Sora + Outfit)": {
        "heading": "'Sora', sans-serif",
        "body": "'Outfit', sans-serif",
        "mono": "'JetBrains Mono', monospace"
    },
    "⚡ Hyper-Readable (Lexend + Inter)": {
        "heading": "'Lexend', sans-serif",
        "body": "'Inter', sans-serif",
        "mono": "'JetBrains Mono', monospace"
    }
}

def inject_custom_css(font_choice="🚀 Quantum Cyber (Space Grotesk + Inter)"):
    preset = FONT_PRESETS.get(font_choice, list(FONT_PRESETS.values())[0])
    h_font = preset["heading"]
    b_font = preset["body"]
    m_font = preset["mono"]

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&family=Syne:wght@500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Sora:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&family=Lexend:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Fira+Code:wght@400;500;600&display=swap');
    
    :root {{
        --bg-main: #f8fafc;
        --card-bg: #ffffff;
        --card-border: #e2e8f0;
        --card-border-hover: #cbd5e1;
        --primary: #7c3aed;
        --primary-hover: #6d28d9;
        --primary-light: #f5f3ff;
        --primary-border: #ddd6fe;
        --accent-indigo: #6366f1;
        --accent-blue: #3b82f6;
        --accent-cyan: #06b6d4;
        --accent-green: #10b981;
        --accent-amber: #f59e0b;
        --text-dark: #0f172a;
        --text-body: #334155;
        --text-muted: #64748b;
        --text-subtle: #94a3b8;
    }}

    html, body {{
        font-family: {b_font};
        color: #0f172a;
        background-color: #f8fafc !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    p, .stMarkdown p, .stMarkdown li, label, .stSelectbox, .stSlider {{
        font-family: {b_font};
        color: #334155;
        line-height: 1.65;
    }}

    h1, h2, h3, h4, h5, h6, .hero-title, .quantum-card-title, .metric-box-val {{
        font-family: {h_font} !important;
        letter-spacing: -0.025em !important;
        font-weight: 700 !important;
        color: #0f172a !important;
    }}

    code, pre, .circuit-window, .stCodeBlock {{
        font-family: {m_font} !important;
    }}

    /* Main Container */
    .stApp {{
        background: radial-gradient(circle at 85% 8%, rgba(124, 58, 237, 0.04) 0%, transparent 40%),
                    radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.03) 0%, transparent 35%),
                    #f8fafc !important;
        color: #0f172a !important;
    }}

    .main .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1380px !important;
    }}

    /* Top Navigation Bar */
    .top-header-container {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 10px 20px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02), 0 4px 12px rgba(0, 0, 0, 0.03);
    }}

    .top-search-box {{
        display: flex;
        align-items: center;
        gap: 10px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 8px 16px;
        width: 380px;
        color: #64748b;
        font-size: 0.88rem;
    }}

    .top-user-pill {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .icon-badge-btn {{
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #475569;
        font-size: 1rem;
        cursor: pointer;
        position: relative;
    }}

    .icon-badge-dot {{
        position: absolute;
        top: 6px;
        right: 6px;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #7c3aed;
    }}

    .user-profile-badge {{
        display: flex;
        align-items: center;
        gap: 10px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 9999px;
        padding: 4px 14px 4px 5px;
    }}

    .user-avatar {{
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 0.82rem;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
        box-shadow: 2px 0 12px rgba(0, 0, 0, 0.02) !important;
    }}

    section[data-testid="stSidebar"] .block-container {{
        padding: 1.5rem 1rem !important;
    }}

    .sidebar-brand-box {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 10px 18px 10px;
        margin-bottom: 8px;
        border-bottom: 1px solid #f1f5f9;
    }}

    .sidebar-brand-icon {{
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: linear-gradient(135deg, #f5f3ff, #ede9fe);
        border: 1px solid #ddd6fe;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.12);
    }}

    .sidebar-brand-title {{
        font-size: 1.15rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }}

    .sidebar-brand-subtitle {{
        font-size: 0.72rem;
        color: #7c3aed;
        font-weight: 600;
        letter-spacing: 0.02em;
    }}

    .sidebar-category-header {{
        font-size: 0.7rem;
        font-weight: 800;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 12px 10px 6px 10px;
        margin-top: 6px;
    }}

    .sidebar-promo-card {{
        background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
        border: 1px solid #ddd6fe;
        border-radius: 16px;
        padding: 18px;
        margin-top: 20px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.08);
    }}

    .promo-icon {{
        font-size: 1.8rem;
        margin-bottom: 6px;
    }}

    .promo-title {{
        font-size: 0.92rem;
        font-weight: 800;
        color: #5b21b6;
        margin-bottom: 4px;
    }}

    .promo-desc {{
        font-size: 0.76rem;
        color: #6d28d9;
        line-height: 1.4;
        margin-bottom: 12px;
    }}

    .promo-btn {{
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        color: white;
        border-radius: 10px;
        padding: 7px 14px;
        font-size: 0.78rem;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 4px 10px rgba(124, 58, 237, 0.25);
    }}

    /* Streamlit Selectbox and Radios in Sidebar */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {{
        gap: 4px;
    }}

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label {{
        padding: 8px 12px !important;
        border-radius: 10px !important;
        margin-bottom: 2px !important;
        transition: all 0.2s ease !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        color: #334155 !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
        background-color: #f1f5f9 !important;
        color: #7c3aed !important;
    }}

    /* Modern White Cards */
    .quantum-card {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px 26px;
        margin-bottom: 22px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02), 0 6px 18px rgba(0, 0, 0, 0.03);
        transition: all 0.2s ease;
    }}

    .quantum-card:hover {{
        border-color: #cbd5e1;
        box-shadow: 0 10px 25px -4px rgba(0, 0, 0, 0.06);
    }}

    .quantum-card-title {{
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 14px;
    }}

    /* Hero Banner */
    .hero-container {{
        background: linear-gradient(135deg, #ffffff 0%, #faf5ff 60%, #f3e8ff 100%);
        border: 1px solid #e9d5ff;
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.06), 0 1px 3px rgba(0, 0, 0, 0.02);
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
    }}

    .hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        border-radius: 9999px;
        background: #ede9fe;
        border: 1px solid #ddd6fe;
        color: #6d28d9;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 10px;
    }}

    .hero-title {{
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.2;
        color: #0f172a;
        margin-bottom: 8px;
    }}

    .hero-subtitle {{
        font-size: 1rem;
        color: #64748b;
        line-height: 1.6;
        max-width: 650px;
    }}

    .hero-orb-graphic {{
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, #a855f7 0%, #7c3aed 45%, #4338ca 90%);
        box-shadow: 0 12px 30px rgba(124, 58, 237, 0.35), inset -5px -5px 15px rgba(0, 0, 0, 0.2), inset 5px 5px 15px rgba(255, 255, 255, 0.4);
        position: relative;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .hero-orb-ring {{
        position: absolute;
        width: 170px;
        height: 60px;
        border: 2px solid rgba(192, 132, 252, 0.6);
        border-radius: 50%;
        transform: rotate(-25deg);
        box-shadow: 0 0 15px rgba(192, 132, 252, 0.4);
    }}

    /* Modern Metric Cards */
    .metric-box {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02), 0 4px 12px rgba(0,0,0,0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        position: relative;
    }}

    .metric-box:hover {{
        border-color: #cbd5e1;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    }}

    .metric-box-icon {{
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        margin-bottom: 12px;
    }}

    .metric-box-val {{
        font-size: 1.9rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.1;
    }}

    .metric-box-lbl {{
        color: #64748b;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 4px;
    }}

    .metric-bar-bg {{
        height: 5px;
        background: #f1f5f9;
        border-radius: 9999px;
        margin-top: 14px;
        overflow: hidden;
    }}

    .metric-bar-fill {{
        height: 100%;
        border-radius: 9999px;
    }}

    /* Timeline Stepper */
    .stepper-container {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px 10px;
        position: relative;
    }}

    .step-item {{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        position: relative;
        z-index: 2;
        width: 18%;
    }}

    .step-circle {{
        width: 42px;
        height: 42px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }}

    .step-completed {{
        background: #ede9fe;
        color: #7c3aed;
        border: 2px solid #7c3aed;
    }}

    .step-active {{
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        color: #ffffff;
        box-shadow: 0 0 0 5px rgba(124, 58, 237, 0.18), 0 4px 14px rgba(124, 58, 237, 0.35);
    }}

    .step-locked {{
        background: #f8fafc;
        color: #94a3b8;
        border: 2px solid #e2e8f0;
    }}

    .step-title {{
        font-size: 0.78rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.2;
        margin-bottom: 3px;
    }}

    .step-status {{
        font-size: 0.7rem;
        font-weight: 600;
    }}

    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 9px 22px !important;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.25) !important;
        transition: all 0.2s ease !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.38) !important;
        filter: brightness(1.04) !important;
    }}

    /* Code Block and Circuit Windows */
    .circuit-window {{
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 14px;
        overflow: hidden;
        margin: 14px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }}

    .circuit-header {{
        background: #1e293b;
        padding: 10px 16px;
        display: flex;
        align-items: center;
        gap: 7px;
        border-bottom: 1px solid #334155;
    }}

    .dot {{
        width: 11px;
        height: 11px;
        border-radius: 50%;
    }}
    .dot-red {{ background: #ef4444; }}
    .dot-yellow {{ background: #f59e0b; }}
    .dot-green {{ background: #10b981; }}

    /* Badges */
    .badge-pill {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    .badge-purple {{
        background: #f5f3ff;
        color: #7c3aed;
        border: 1px solid #ddd6fe;
    }}
    .badge-cyan {{
        background: #f0f9ff;
        color: #0284c7;
        border: 1px solid #bae6fd;
    }}
    .badge-green {{
        background: #ecfdf5;
        color: #059669;
        border: 1px solid #a7f3d0;
    }}
    .badge-amber {{
        background: #fffbeb;
        color: #d97706;
        border: 1px solid #fde68a;
    }}

    /* Interactive Action Row */
    .quick-action-item {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 16px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        margin-bottom: 10px;
        color: #0f172a;
        font-weight: 600;
        font-size: 0.88rem;
        transition: all 0.2s ease;
        text-decoration: none;
    }}

    .quick-action-item:hover {{
        background: #f5f3ff;
        border-color: #ddd6fe;
        color: #7c3aed;
        transform: translateX(3px);
    }}

    /* Learning Card item */
    .continue-module-card {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
    }}

    .continue-module-card:hover {{
        border-color: #ddd6fe;
        box-shadow: 0 6px 16px rgba(124, 58, 237, 0.08);
    }}

    /* Streamlit Alert Boxes */
    div[data-testid="stAlert"] {{
        border-radius: 14px !important;
        border: 1px solid #e2e8f0 !important;
    }}

    /* Streamlit Expanders */
    div[data-testid="stExpander"] {{
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
    }}

    /* Streamlit Dataframes */
    div[data-testid="stDataFrame"] {{
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #e2e8f0 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# APPLICATION / STORAGE CONFIGURATION
# ============================================================

APP_NAME = "Quantum Learning Platform"
DEFAULT_STORAGE = os.path.join(os.getcwd(), "quantum_cloud_storage")
os.makedirs(DEFAULT_STORAGE, exist_ok=True)

# Apply Modern Light Theme
inject_custom_css()

def render_top_header(current_title=None):
    st.markdown('<div class="top-header-container" style="display: block; padding: 10px 14px;">', unsafe_allow_html=True)
    search_query = st.text_input(
        "Search platform",
        placeholder="🔍 Search modules, quantum gates (X, H, CNOT), guided projects, simulator, glossary...",
        label_visibility="collapsed",
        key="global_search_input"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if search_query:
        query_lower = search_query.strip().lower()
        search_index = [
            ("🌱 Introduction to Quantum Computing", "🌱 Introduction to Quantum Computing", "Why quantum computing matters, linear algebra, hybrid models"),
            ("💻 Classical vs Quantum Computing", "💻 Classical vs Quantum Computing", "Bits vs Qubits, computational complexity"),
            ("🔵 What is a Qubit?", "🔵 What is a Qubit?", "Statevectors, amplitudes, Bloch sphere"),
            ("🌊 Quantum Superposition", "🌊 Quantum Superposition", "Hadamard gate, linear combinations, 50/50 probabilities"),
            ("⚙️ Quantum Gates (X, Y, Z, S, T, CNOT, SWAP)", "⚙️ Quantum Gates", "Single and multi-qubit unitary operations, phase rotations"),
            ("🔗 Quantum Entanglement", "🔗 Quantum Entanglement", "Bell states, EPR pairs, non-local quantum correlations"),
            ("📏 Quantum Measurement", "📏 Quantum Measurement", "Wavefunction collapse, Born's rule, classical bits"),
            ("🧩 Quantum Circuits", "🧩 Quantum Circuits", "Circuit wires, gate scheduling, registers"),
            ("❓ Beginner Quiz", "❓ Beginner Quiz", "10-question quantum mechanics and gates assessment"),
            ("🧪 Quantum Playground", "🧪 Quantum Playground", "Interactive circuit builder with step-by-step state inspection"),
            ("⚛️ Quantum Circuit Simulator", "⚛️ Quantum Circuit Simulator", "Full custom circuit simulator with shots slider"),
            ("🚀 Simulation Access & Playground", "🚀 Simulation Access & Playground", "Interactive sandbox for rapid experimentation"),
            ("📊 Probability Distribution", "📊 Probability Distribution", "Visual probability bar charts and measurement statistics"),
            ("🔔 Bell State Experiment", "🔔 Bell State Experiment", "Hands-on preparation of all 4 Bell states (|Φ⁺⟩, |Φ⁻⟩, |Ψ⁺⟩, |Ψ⁻⟩)"),
            ("🎲 Quantum Random Number Generator", "🎲 Quantum Random Number Generator", "Hardware-grade true randomness via quantum measurement"),
            ("🧪 Guided Quantum Projects", "🧪 Guided Quantum Projects", "Real-world guided applications and protocols"),
            ("🤖 Quantum AI / ML", "🤖 Quantum AI / ML", "Variational quantum circuits and quantum machine learning"),
            ("📖 Quantum Glossary", "📖 Quantum Glossary", "20+ student-friendly terms dictionary"),
            ("🗺️ Learning Path", "🗺️ Learning Path", "12-module structured quantum curriculum roadmap"),
            ("📊 Experiment History", "📊 Experiment History", "View and export saved quantum simulation runs"),
            ("☁️ Cloud Storage", "☁️ Experiment and Cloud Storage", "Manage JSON/CSV local experiment database")
        ]
        
        results = [m for m in search_index if query_lower in m[0].lower() or query_lower in m[2].lower()]
        if results:
            st.markdown(f"**🔍 Search Results for '{search_query}':**")
            for label, target_page, desc in results[:4]:
                r_c1, r_c2 = st.columns([3, 1])
                with r_c1:
                    st.markdown(f"**{label}** — <span style='font-size:0.85rem; color:#64748b;'>{desc}</span>", unsafe_allow_html=True)
                with r_c2:
                    if st.button("Open Module ➔", key=f"search_btn_{target_page}"):
                        navigate_to(target_page)
        else:
            st.info(f"No direct matches for '{search_query}'. Try searching: 'superposition', 'grover', 'gates', 'teleportation', 'bell', 'quiz'.")

# ============================================================
# SESSION STATE
# ============================================================

if "experiment_history" not in st.session_state:
    st.session_state.experiment_history = []

if "last_counts" not in st.session_state:
    st.session_state.last_counts = None

if "last_circuit" not in st.session_state:
    st.session_state.last_circuit = None

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_storage_path():
    path = st.session_state.get("storage_path", DEFAULT_STORAGE)
    if not path:
        path = DEFAULT_STORAGE
    os.makedirs(path, exist_ok=True)
    return path

@st.cache_resource
def get_simulator():
    return AerSimulator()

def run_circuit(circuit, shots=1000):
    """Run a circuit on the local Qiskit Aer simulator."""
    simulator = get_simulator()
    compiled = transpile(circuit, simulator)
    result = simulator.run(compiled, shots=int(shots)).result()
    return result.get_counts()

def explain_quantum_circuit(circuit, context_title=None):
    """
    Renders a comprehensive, beginner-friendly, dynamic step-by-step
    'How This Circuit Works' breakdown according to the actual quantum circuit.
    """
    if not isinstance(circuit, QuantumCircuit):
        return
    
    num_q = circuit.num_qubits
    
    # Extract operations from circuit
    ops = []
    for inst in circuit.data:
        op_name = inst.operation.name.lower()
        if op_name == "barrier":
            continue
        q_indices = [circuit.find_bit(q).index for q in inst.qubits]
        c_indices = [circuit.find_bit(c).index for c in inst.clbits] if inst.clbits else []
        ops.append((op_name, q_indices, c_indices, inst.operation))
    
    # Identify circuit patterns
    h_count_per_q = {}
    for op_name, q_idx, _, _ in ops:
        for q in q_idx:
            if op_name == 'h':
                h_count_per_q[q] = h_count_per_q.get(q, 0) + 1

    is_bb84 = (num_q == 1 and len(ops) >= 2 and ops[-1][0] == 'measure' and any(op[0] == 'h' for op in ops))
    is_bell = (num_q == 2 and len(ops) >= 2 and ops[0][0] == 'h' and ops[0][1] == [0] and ops[1][0] in ['cx', 'cnot'] and ops[1][1] == [0, 1])
    is_superposition = (num_q == 1 and len(ops) <= 2 and ops[0][0] == 'h' and ops[0][1] == [0])
    is_teleport = (num_q == 3 and any(op[0] in ['cx', 'cz'] for op in ops))
    is_grover = (num_q == 2 and any(op[0] == 'cz' for op in ops))
    is_qft = any(op[0] in ['cp', 'swap'] for op in ops)

    st.markdown("""<div class="quantum-card" style="margin-top: 14px; margin-bottom: 14px; border-left: 4px solid #7c3aed;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
            <div style="font-weight: 800; font-size: 1.12rem; color: #6d28d9;">
                🧩 How This Circuit Works
            </div>
            <span class="badge-pill badge-purple" style="font-size: 0.75rem;">Interactive Breakdown</span>
        </div>
    """, unsafe_allow_html=True)
    
    # 1. Step-by-Step Flow
    st.markdown("##### 🔄 Step-by-Step Operations")
    steps_md = []
    
    steps_md.append(f"**Step 1 — Initialize Qubits:** All {num_q} qubit wire(s) start in ground state $|0\\rangle$. System baseline: $|{'0'*num_q}\\rangle$.")
    
    step_num = 2
    seen_h = {}
    for op_name, q_idx, c_idx, op_obj in ops:
        q_str = ", ".join([f"q{i}" for i in q_idx])
        if op_name == 'h':
            q_target = q_idx[0]
            h_occurrence = seen_h.get(q_target, 0) + 1
            seen_h[q_target] = h_occurrence
            
            if h_occurrence == 1:
                steps_md.append(f"**Step {step_num} — Apply 1st Hadamard (H) on {q_str}:** Puts {q_str} into equal superposition ($|0\\rangle \\rightarrow |+\\rangle = \\frac{{|0\\rangle+|1\\rangle}}{{\\sqrt{{2}}}}$ or $|1\\rangle \\rightarrow |-\\rangle = \\frac{{|0\\rangle-|1\\rangle}}{{\\sqrt{{2}}}}$).")
            elif h_occurrence == 2:
                steps_md.append(f"**Step {step_num} — Apply 2nd Hadamard (H) on {q_str} (Basis Decoding / Interference):** Because $H \\cdot H = I$ (Hadamard is its own inverse), applying $H$ a second time creates quantum interference that reverses the superposition, rotating the $X$-basis back to the computational $Z$-basis!")
            else:
                steps_md.append(f"**Step {step_num} — Apply Hadamard (H) on {q_str}:** Rotates quantum basis between $Z$ and $X$ axes.")
        elif op_name == 'x':
            steps_md.append(f"**Step {step_num} — Apply Pauli-X (NOT) on {q_str}:** Bit-flip gate that inverts the state: $|0\\rangle \\leftrightarrow |1\\rangle$ with 100% certainty.")
        elif op_name == 'y':
            steps_md.append(f"**Step {step_num} — Apply Pauli-Y on {q_str}:** Combines bit-flip and phase-flip: $|0\\rangle \\rightarrow i|1\\rangle, |1\\rangle \\rightarrow -i|0\\rangle$.")
        elif op_name == 'z':
            steps_md.append(f"**Step {step_num} — Apply Pauli-Z on {q_str}:** Phase-flip gate. Leaves $|0\\rangle$ unchanged and applies a $180^\\circ$ ($\\pi$) phase rotation ($-1$) to state $|1\\rangle$.")
        elif op_name == 's':
            steps_md.append(f"**Step {step_num} — Apply S Phase Gate on {q_str}:** $90^\\circ$ ($\\pi/2$) phase shift on $|1\\rangle$ (multiplies $|1\\rangle$ amplitude by imaginary unit $i$).")
        elif op_name == 't':
            steps_md.append(f"**Step {step_num} — Apply T Phase Gate on {q_str}:** $45^\\circ$ ($\\pi/4$) phase shift on $|1\\rangle$ (multiplies $|1\\rangle$ amplitude by $e^{{i\\pi/4}}$).")
        elif op_name in ['cx', 'cnot']:
            ctrl = q_idx[0]
            tgt = q_idx[1]
            steps_md.append(f"**Step {step_num} — Apply CNOT (Control: q{ctrl}, Target: q{tgt}):** If q{ctrl} is $|1\\rangle$, flips q{tgt} ($|0\\rangle \\leftrightarrow |1\\rangle$). If q{ctrl} is in superposition, this creates quantum entanglement between q{ctrl} and q{tgt}.")
        elif op_name == 'cz':
            ctrl = q_idx[0]
            tgt = q_idx[1]
            steps_md.append(f"**Step {step_num} — Apply Controlled-Z (q{ctrl}, q{tgt}):** Inverts quantum phase when both qubits are in state $|11\\rangle$ (used as an oracle in Grover search).")
        elif op_name == 'swap':
            steps_md.append(f"**Step {step_num} — Apply SWAP between {q_str}:** Exchanges the quantum amplitude states between the two qubits.")
        elif op_name.startswith('r'):
            steps_md.append(f"**Step {step_num} — Apply {op_name.upper()} Rotation on {q_str}:** Rotates statevector around Bloch sphere.")
        elif op_name == 'cp':
            steps_md.append(f"**Step {step_num} — Apply Controlled Phase (CP):** Applies relative phase angle between coupled qubit components.")
        elif op_name == 'measure':
            c_target = f"c{c_idx[0]}" if c_idx else "classical register"
            steps_md.append(f"**Step {step_num} — Quantum Measurement on {q_str} $\\rightarrow$ {c_target}:** The quantum state collapses into a definite classical bit (0 or 1) based on Born rule probabilities.")
        else:
            steps_md.append(f"**Step {step_num} — Apply {op_name.upper()} on {q_str}:** Unitary transformation applied to wire.")
        step_num += 1

    for s in steps_md:
        st.markdown(f"- {s}")
    
    st.markdown("<hr style='border: none; border-top: 1px solid #ede9fe; margin: 12px 0;'>", unsafe_allow_html=True)
    
    # 2. What is happening?
    st.markdown("##### 💡 What is happening?")
    if is_bb84 and seen_h.get(0, 0) == 2:
        st.write("**BB84 Basis Matching (X-basis Encode & Decode):** Alice used the 1st H gate to encode her bit into the diagonal $X$-basis ($|-\\rangle$). Bob used the 2nd H gate to rotate the qubit from the $X$-basis back to the computational basis before measurement. Because their bases matched ($X = X$), the two Hadamard gates cancel each other out ($H \\cdot H = I$), allowing Bob to measure Alice's exact original bit with 100% fidelity!")
    elif is_bell:
        st.write("This circuit creates a maximally entangled Bell State (|Φ⁺⟩ = (|00⟩ + |11⟩)/√2). First, the H gate places qubit 0 into equal superposition. Next, the CNOT gate entangles qubit 1 with qubit 0. The two qubits become strongly correlated: measuring one immediately determines the state of the other!")
    elif is_superposition:
        st.write("This circuit demonstrates single-qubit quantum superposition. Starting from ground state |0⟩, the Hadamard gate rotates the qubit onto the equator of the Bloch sphere, creating an equal linear combination of |0⟩ and |1⟩. When measured across many shots, the counts will be approximately evenly split 50/50.")
    elif is_teleport:
        st.write("This circuit executes the Quantum Teleportation protocol. Using an entangled Bell pair shared between Alice and Bob, Alice performs a Bell-basis measurement, and Bob applies conditional quantum corrections (X and Z) to reconstruct the exact original state on his qubit.")
    elif is_grover:
        st.write("This circuit implements Grover's Search algorithm. It creates equal superposition across all items, applies an oracle that flips the phase of the marked target item, and uses a diffusion operator to amplify the target item's probability close to 100%.")
    elif is_qft:
        st.write("This circuit performs the Quantum Fourier Transform (QFT), mapping computational basis states into frequency phase components using Hadamard and controlled phase rotations.")
    else:
        st.write(f"This quantum circuit processes information step-by-step across {num_q} qubit wire(s), changing bit values and wave angles before measuring the final classical output (0 or 1).")

    # 3. Gate-by-Gate Explanation
    st.markdown("##### 🔍 Gate-by-Gate Explanation")
    gate_counts = circuit.count_ops()
    gate_bullets = []
    if 'h' in gate_counts:
        h_cnt = gate_counts['h']
        if h_cnt == 1:
            gate_bullets.append("`H` (Hadamard) ➔ Creates equal superposition ($|0\\rangle \\rightarrow \\frac{|0\\rangle+|1\\rangle}{\\sqrt{2}}$).")
        else:
            gate_bullets.append(f"`H` × {h_cnt} (Hadamard Pair / Basis Rotator) ➔ 1st H encodes into superposition/X-basis, 2nd H decodes back via interference ($H \\cdot H = I$).")
    if 'x' in gate_counts:
        gate_bullets.append("`X` (Pauli-X / NOT) ➔ Inverts bit state ($|0\\rangle \\leftrightarrow |1\\rangle$).")
    if 'y' in gate_counts:
        gate_bullets.append("`Y` (Pauli-Y) ➔ Bit-flip and phase-flip rotation.")
    if 'z' in gate_counts:
        gate_bullets.append("`Z` (Pauli-Z) ➔ $180^\\circ$ phase-flip on state $|1\\rangle$.")
    if 's' in gate_counts:
        gate_bullets.append("`S` (Phase Gate) ➔ $90^\\circ$ phase rotation on state $|1\\rangle$ ($S = \\sqrt{Z}$).")
    if 't' in gate_counts:
        gate_bullets.append("`T` (T Gate) ➔ $45^\\circ$ phase rotation on state $|1\\rangle$ ($T = \\sqrt[4]{Z}$).")
    if 'cx' in gate_counts:
        gate_bullets.append("`CNOT` (Controlled-NOT) ➔ Conditional bit-flip that creates quantum entanglement.")
    if 'cz' in gate_counts:
        gate_bullets.append("`CZ` (Controlled-Z) ➔ Phase-flips state $|11\\rangle$ for oracle marking.")
    if 'swap' in gate_counts:
        gate_bullets.append("`SWAP` ➔ Exchanges quantum states between two qubits.")
    if 'measure' in gate_counts:
        gate_bullets.append("`M` (Measurement) ➔ Collapses quantum state into classical bitstring (0 or 1).")
    
    for gb in gate_bullets:
        st.markdown(f"- {gb}")

    # 4. What result should I expect?
    st.markdown("##### 📊 What result should I expect?")
    if is_bb84 and seen_h.get(0, 0) == 2:
        st.write("Since both Alice and Bob selected the **X-basis**, the two Hadamard gates cancel each other out ($H \\cdot H = I$). Bob will measure Alice's original bit with **100% certainty** (0% error rate).")
    elif is_bell:
        st.write("You should expect approximately equal counts for **|00⟩** (~50%) and **|11⟩** (~50%). The invalid states **|01⟩** and **|10⟩** should have 0% probability because the qubits are perfectly entangled.")
    elif is_superposition:
        st.write("You should expect an approximately 50/50 split between outcome **0** (~50%) and outcome **1** (~50%). Small variations are normal due to statistical sampling of finite shots.")
    elif is_grover:
        st.write("The target marked state will appear with the dominant highest probability peak (~100%), demonstrating constructive quantum amplitude amplification.")
    else:
        st.write(f"The measurement will sample from the final {num_q}-qubit statevector distribution according to Born's probability rule $P(x) = |\\alpha_x|^2$.")

    # 5. What did I learn?
    # 5. What did I learn?
    st.markdown("##### 🎓 What did I learn?")
    if is_bb84:
        st.markdown("""
        - **Hadamard Invertibility ($H^2 = I$):** Applying Hadamard twice cancels out, turning superpositions back into definite states.
        - **Basis Rotation:** Quantum measurement in the $X$-basis is physically performed by applying an $H$ gate before standard computational $Z$-basis measurement.
        - **BB84 Security:** When bases match, bits are received perfectly; when bases differ, quantum uncertainty prevents an eavesdropper from learning the secret without creating detectable noise.
        """)
    else:
        st.markdown("""
        - **Reversibility:** Quantum gates are unitary and reversible transformations until measurement occurs.
        - **Quantum Interference:** Quantum state vectors combine constructively or destructively to amplify correct answers.
        - **Quantum Parallelism:** Superposition allows evaluating global properties of a function in fewer queries than classical computing.
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)


def circuit_diagram(circuit, show_explanation=True):
    st.markdown("""<div class="circuit-window">
        <div class="circuit-window-bar">
            <div class="circuit-window-dot" style="background: #ef4444;"></div>
            <div class="circuit-window-dot" style="background: #f59e0b;"></div>
            <div class="circuit-window-dot" style="background: #10b981;"></div>
            <span style="font-family: 'Inter', sans-serif; font-size: 0.75rem; color: #64748b; font-weight: 600; margin-left: 8px;">Quantum Circuit Wire Schematic</span>
        </div>
    """, unsafe_allow_html=True)
    st.code(str(circuit), language="text")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if show_explanation:
        explain_quantum_circuit(circuit)







def probability_table(counts, num_qubits, shots):

    states = [

        format(i, f"0{num_qubits}b")

        for i in range(2 ** num_qubits)

    ]



    rows = []

    for state in states:

        measurements = counts.get(state, 0)

        probability = measurements / shots if shots else 0

        rows.append({

            "Quantum State": state,

            "Measurements": measurements,

            "Probability": probability

        })



    return pd.DataFrame(rows)





def render_classical_measurement_output(counts, num_qubits, shots):
    """
    Renders the universal '🔢 Classical Measurement Output' section for ANY circuit execution.
    Converts actual Qiskit measurement counts into clear, dynamic classical bitstrings,
    bit-by-bit qubit breakdowns, and measurement probability tables.
    """
    if not counts:
        return

    st.markdown("""<div class="quantum-card" style="margin-top: 18px; margin-bottom: 18px; border-left: 4px solid #059669; background: #ffffff;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
            <div style="font-weight: 800; font-size: 1.15rem; color: #065f46;">
                🔢 Classical Measurement Output
            </div>
            <span class="badge-pill badge-green" style="font-size: 0.75rem;">Measured Bit Data</span>
        </div>
    """, unsafe_allow_html=True)

    # 1. Conceptual Visual Flow Box
    st.markdown("""<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 16px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #334155; text-align: center; line-height: 1.8;">
        <b>Quantum Circuit</b> &nbsp;↓&nbsp; <b>Quantum Processing</b> &nbsp;↓&nbsp; <b>Measurement</b> &nbsp;↓&nbsp; <b>Classical Bits</b> &nbsp;↓&nbsp; <span style="color: #059669; font-weight: 800;">Classical Measurement Output</span>
    </div>""", unsafe_allow_html=True)

    total_shots = shots if shots else sum(counts.values())
    sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    # Single Shot Execution Mode (shots == 1)
    if total_shots == 1:
        raw_state = list(sorted_counts.keys())[0] if sorted_counts else "0" * num_qubits
        single_state = f"{raw_state:>0{num_qubits}}" if raw_state.isdigit() else raw_state
        st.markdown(f"#### Classical Output: `{single_state}`")
        st.info("Single-shot execution performed. The quantum state collapsed into a single deterministic classical bitstring.")

        st.markdown("##### 📌 Qubit-by-Qubit Classical Bit Breakdown")
        bit_cols = st.columns(min(num_qubits, 4))
        for i in range(num_qubits):
            col_idx = i % 4
            # Qiskit bit ordering: rightmost character corresponds to Qubit 0 (little-endian)
            bit_val = single_state[len(single_state) - 1 - i] if len(single_state) > i else single_state[i]
            with bit_cols[col_idx]:
                st.markdown(f"""<div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 10px; text-align: center; margin-bottom: 8px;">
                    <div style="font-size: 0.75rem; color: #166534; font-weight: 600;">Qubit {i}</div>
                    <div style="font-size: 1.4rem; font-weight: 800; color: #059669;">{bit_val}</div>
                </div>""", unsafe_allow_html=True)

    # Multiple Shots Execution Mode (shots > 1)
    else:
        st.write("Each circuit execution (shot) produces a classical measurement result. The table below summarizes all observed measurement results:")

        # 2. Dynamic Table of Measured Classical States, Counts, and Probabilities
        table_rows = []
        for raw_state, count in sorted_counts.items():
            state = f"{raw_state:>0{num_qubits}}" if raw_state.isdigit() else raw_state
            prob_pct = (count / total_shots) * 100
            table_rows.append({
                "Classical State": state,
                "Measurements": count,
                "Probability": f"{prob_pct:.1f}%"
            })

        df_classical = pd.DataFrame(table_rows)
        st.dataframe(df_classical, use_container_width=True, hide_index=True)

        # 3. Qubit-by-Qubit Bit Breakdown for Observed States
        st.markdown("##### 📌 Qubit-by-Qubit Classical Bit Breakdown")
        for raw_state, count in sorted_counts.items():
            state = f"{raw_state:>0{num_qubits}}" if raw_state.isdigit() else raw_state
            prob_pct = (count / total_shots) * 100
            with st.expander(f"Classical State `{state}` — {count} measurements ({prob_pct:.1f}%)", expanded=(len(sorted_counts) == 1 or count == max(sorted_counts.values()))):
                q_cols = st.columns(min(num_qubits, 4))
                for i in range(num_qubits):
                    col_idx = i % 4
                    # Qiskit bit ordering: rightmost character corresponds to Qubit 0
                    bit_val = state[len(state) - 1 - i] if len(state) > i else state[i]
                    with q_cols[col_idx]:
                        st.markdown(f"""<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 14px; text-align: center; margin-bottom: 6px;">
                            <span style="font-size: 0.78rem; color: #64748b; font-weight: 600;">Qubit {i}</span> ➔ 
                            <span style="font-size: 1.2rem; font-weight: 800; color: #059669;">{bit_val}</span>
                        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def show_results(counts, num_qubits, shots):
    # Render Universal Classical Measurement Output
    render_classical_measurement_output(counts, num_qubits, shots)

    st.write("**Raw measurement counts:**", counts)

    df = probability_table(counts, num_qubits, shots)
    chart_df = df.copy()
    chart_df["Probability (%)"] = chart_df["Probability"] * 100

    st.bar_chart(
        chart_df.set_index("Quantum State")["Probability (%)"]
    )

    display_df = df.copy()
    display_df["Probability"] = (
        display_df["Probability"] * 100
    ).round(2).astype(str) + "%"

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )





def save_experiment(name, circuit, counts, qubits, shots):

    experiment = {

        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "experiment": name,

        "qubits": int(qubits),

        "shots": int(shots),

        "counts": counts,

        "circuit": str(circuit)

    }



    st.session_state.experiment_history.append(experiment)

    st.session_state.last_counts = counts

    st.session_state.last_circuit = circuit



    storage = get_storage_path()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")



    json_path = os.path.join(

        storage, f"experiment_{timestamp}.json"

    )



    csv_path = os.path.join(

        storage, "experiment_history.csv"

    )



    with open(json_path, "w", encoding="utf-8") as file:

        json.dump(experiment, file, indent=4)



    row = pd.DataFrame([{

        "Timestamp": experiment["timestamp"],

        "Experiment": experiment["experiment"],

        "Qubits": experiment["qubits"],

        "Shots": experiment["shots"],

        "Counts": str(experiment["counts"])

    }])



    if os.path.exists(csv_path):

        old = pd.read_csv(csv_path)

        final = pd.concat([old, row], ignore_index=True)

    else:

        final = row



    final.to_csv(csv_path, index=False)

    return json_path





def beginner_box(title, text):

    with st.expander(f"💡 Beginner Explanation — {title}"):

        st.write(text)





def concept_card(title, explanation):

    st.subheader(title)

    st.write(explanation)





def show_circuit_explanation(page_name):

    """Show a beginner-friendly circuit explanation appropriate to the current module."""

    explanations = {

        "🌱 Introduction to Quantum Computing": (

            "🔄 Quantum Computing Flow",

            "Input → encode into qubits → apply quantum gates → create a quantum state → measure → obtain classical output.",

            """Classical Input

      |

      v

   Qubits

      |

      v

 Quantum Gates

      |

      v

 Quantum State

      |

      v

 Measurement

      |

      v

 Classical Output"""

        ),

        "💻 Classical vs Quantum Computing": (

            "🔄 Circuit View: Classical vs Quantum",

            "A classical program changes bits with logic operations. A quantum circuit changes qubits with quantum gates and normally measures them at the end to obtain classical bits.",

            """Classical:  bit → logic operation → bit

Quantum:    qubit → quantum gate → qubit → measurement → classical bit"""

        ),

        "🔵 What is a Qubit?": (

            "🔄 Qubit Circuit",

            "A circuit begins with an initialized qubit, applies gates that transform its state, and optionally measures it. The qubit itself is the information-carrying part; the gate is the operation performed on it.",

            """q0 ── [Gate] ── M

             │        │

          quantum   classical

           state     result"""

        ),

        "🌊 Quantum Superposition": (

            "🔄 Superposition Circuit",

            "The H gate is used because it transforms |0> into an equal superposition. Measurement then samples 0 or 1 according to the resulting probabilities.",

            """q0: |0> ── H ── M

              50% 0 / 50% 1"""

        ),

        "⚙️ Quantum Gates": (

            "🔄 Gate Circuit & State Transformation",

            "A quantum gate is a reversible unitary operation placed on qubit wires. A circuit is processed left-to-right: initial state preparation (|0⟩ or |1⟩) → gate transformation (rotating amplitudes or phases) → measurement into classical bits (0 or 1). Phase shifts alter relative angles on the Bloch sphere, which become observable in measurement when combined with superposition gates.",

            """q0: |0⟩ or |1⟩ ─── [Quantum Gate (X, H, Z, S, T...)] ─── M ─── Classical Bit
                   (Transforms Amplitudes & Phases)           ↓
                                                      Measurement Result"""

        ),

        "🔗 Quantum Entanglement": (

            "🔄 Entanglement Circuit",

            "The standard beginner circuit starts with |00>, applies H to the first qubit, then CNOT to correlate the two qubits, and finally measures both.",

            """q0 ── H ──●──── M

             │

q1 ────────X──── M"""

        ),

        "📏 Quantum Measurement": (

            "🔄 Measurement Circuit",

            "Measurement is normally placed after the quantum operations. It samples the final quantum state and records a classical bit for each measured qubit.",

            """q0 ── quantum gates ── M ── classical bit

q1 ── quantum gates ── M ── classical bit"""

        ),

        "🤖 Quantum AI / ML": (

            "🔄 QML Circuit",

            "Classical features are encoded into qubits, a quantum circuit processes the encoded state, measurement produces values, and a classical ML component uses those values for learning or prediction.",

            """Features → Encoding → Quantum Circuit → Measurement → Classical ML"""

        ),

        "🧪 Guided Quantum Projects": (

            "🔄 Project Circuit Pattern",

            "Most beginner projects follow the same core pattern: initialize qubits, prepare a useful state, apply gates, measure, and let classical software interpret the result.",

            """Problem

  ↓

Qubits → Gates → Quantum State → Measurement → Classical Result → Application"""

        ),

        "🚀 Simulation Access & Playground": (

            "🔄 Simulation Playground Architecture",

            "This module allows full custom circuit construction and quick execution of guided quantum projects. Circuit flow: 1. Select Qubits (1-4) & Initial States (|0⟩/|1⟩) → 2. Apply Custom Gate Layers (H, X, Y, Z, S, T) & Entangling Operations (CNOT, SWAP, CZ) → 3. Measure Qubits → 4. Execute on Qiskit Aer Simulator → 5. Inspect Measurement Counts & Probability Distribution.",

            """Input States (|0⟩/|1⟩) ──► [Single-Qubit Gate Layers] ──► [Entangling Operations] ──► [Measurement] ──► Qiskit Aer Simulator"""

        ),

        "📊 Probability Distribution": (

            "🔄 From Circuit to Probability Distribution",

            "The circuit creates a quantum state. Repeating the same circuit for many shots produces measurement counts. Dividing each count by the total number of shots gives an estimated probability.",

            """Circuit → many shots → counts → probability calculation → chart"""

        )

    }



    if page_name in explanations:

        title, text, diagram = explanations[page_name]

        with st.expander(f"🧩 {title} — How the circuit works", expanded=False):

            st.write(text)

            st.code(diagram, language="text")

            st.info("Beginner tip: read a quantum circuit from left to right. Gates change the quantum state; measurement converts the final state into classical information.")





def run_and_save(name, circuit, qubits, shots):

    counts = run_circuit(circuit, shots)

    st.subheader("⚛️ Circuit")

    circuit_diagram(circuit)

    st.subheader("📊 Measurement Results")

    show_results(counts, qubits, shots)



    try:

        path = save_experiment(

            name, circuit, counts, qubits, shots

        )

        st.success(f"Experiment saved successfully: {path}")

    except Exception as exc:

        st.warning(f"Experiment ran, but saving failed: {exc}")



    return counts





# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown("""<div class="sidebar-brand-box">
    <div class="sidebar-brand-icon">⚛️</div>
    <div>
        <div class="sidebar-brand-title">Quantum Learning Platform</div>
        <div class="sidebar-brand-subtitle">Explore. Simulate. Master.</div>
    </div>
</div>""", unsafe_allow_html=True)

nav_sections = {
    "📖 LEARN": [
        "🏠 Dashboard / Home",
        "🗺️ Learning Path",
        "🌱 Introduction to Quantum Computing",
        "💻 Classical vs Quantum Computing",
        "🔵 What is a Qubit?",
        "🌊 Quantum Superposition",
        "⚙️ Quantum Gates",
        "🔗 Quantum Entanglement",
        "📏 Quantum Measurement",
        "🧩 Quantum Circuits",
        "❓ Beginner Quiz"
    ],
    "🔭 EXPLORE": [
        "🧪 Quantum Playground",
        "⚛️ Quantum Circuit Simulator",
        "🚀 Simulation Access & Playground",
        "📊 Probability Distribution",
        "🔔 Bell State Experiment",
        "🎲 Quantum Random Number Generator",
        "🧪 Guided Quantum Projects",
        "🤖 Quantum AI / ML",
        "📖 Quantum Glossary"
    ],
    "🛠️ TOOLS": [
        "📊 Experiment History",
        "☁️ Experiment and Cloud Storage"
    ]
}

def navigate_to(target_page):
    st.session_state["pending_page"] = target_page
    st.rerun()

# Handle any pending navigation before instantiating widgets
if "pending_page" in st.session_state:
    target = st.session_state.pop("pending_page")
    for cat_name, pages in nav_sections.items():
        if target in pages:
            st.session_state["current_category"] = cat_name
            st.session_state["current_page"] = target
            break

if "current_category" not in st.session_state:
    st.session_state["current_category"] = "📖 LEARN"
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "🏠 Dashboard / Home"

cat_list = list(nav_sections.keys())
cat_idx = cat_list.index(st.session_state["current_category"]) if st.session_state["current_category"] in cat_list else 0

category = st.sidebar.radio("Category", cat_list, index=cat_idx, label_visibility="collapsed")

if category != st.session_state["current_category"]:
    st.session_state["current_category"] = category
    st.session_state["current_page"] = nav_sections[category][0]

page_list = nav_sections[category]
page_idx = page_list.index(st.session_state["current_page"]) if st.session_state["current_page"] in page_list else 0

page = st.sidebar.selectbox("Module", page_list, index=page_idx, label_visibility="collapsed")

if page != st.session_state["current_page"]:
    st.session_state["current_page"] = page


st.sidebar.markdown("""<div style="margin-top: 24px; padding: 12px 14px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; text-align: center;">
    <div style="font-size: 0.8rem; font-weight: 700; color: #0f172a;">⚡ Qiskit Aer Simulator</div>
    <div style="font-size: 0.72rem; color: #059669; font-weight: 600;">● Local Engine Ready</div>
</div>""", unsafe_allow_html=True)

# Render Modern Top Header on All Pages
render_top_header(page)

# ============================================================
# HOME / DASHBOARD
# ============================================================

if page in ["🏠 Dashboard / Home", "🏠 Home"]:
    # 2-Column Main Dashboard Grid
    col_left, col_right = st.columns([1.65, 1.0])

    with col_left:
        # Learning Path Stepper Card
        st.markdown("""<div class="quantum-card">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
    <div class="quantum-card-title" style="margin-bottom: 0;">🗺️ Your Learning Path</div>
</div>
<div class="stepper-container">
    <div class="step-item">
        <div class="step-circle step-completed">✓</div>
        <div class="step-title">Introduction to Quantum</div>
        <div class="step-status" style="color: #059669;">● Completed</div>
    </div>
    <div style="height: 2px; flex: 1; background: #7c3aed; margin-top: -24px;"></div>
    <div class="step-item">
        <div class="step-circle step-completed">✓</div>
        <div class="step-title">Qubits and States</div>
        <div class="step-status" style="color: #059669;">● Completed</div>
    </div>
    <div style="height: 2px; flex: 1; background: #ddd6fe; margin-top: -24px;"></div>
    <div class="step-item">
        <div class="step-circle step-active">⚛️</div>
        <div class="step-title" style="color: #7c3aed;">Quantum Superposition</div>
        <div class="step-status" style="color: #7c3aed;">● In Progress</div>
    </div>
    <div style="height: 2px; flex: 1; background: #e2e8f0; margin-top: -24px;"></div>
    <div class="step-item">
        <div class="step-circle step-locked">🔒</div>
        <div class="step-title">Quantum Entanglement</div>
        <div class="step-status" style="color: #94a3b8;">Locked</div>
    </div>
    <div style="height: 2px; flex: 1; background: #e2e8f0; margin-top: -24px;"></div>
    <div class="step-item">
        <div class="step-circle step-locked">🔒</div>
        <div class="step-title">Guided Projects</div>
        <div class="step-status" style="color: #94a3b8;">Locked</div>
    </div>
</div>
</div>""", unsafe_allow_html=True)

        if st.button("🗺️ View Full Interactive Learning Path ➔", key="btn_path_nav", use_container_width=True):
            navigate_to("🗺️ Learning Path")

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # Continue Learning Card with Working Navigation Buttons
        st.markdown("""<div class="quantum-card" style="padding-bottom: 12px;">
<div class="quantum-card-title" style="margin-bottom: 14px;">📖 Continue Learning</div>
</div>""", unsafe_allow_html=True)

        c_mod1, c_mod2, c_mod3 = st.columns(3)

        with c_mod1:
            st.markdown("""<div class="continue-module-card" style="margin-bottom: 8px;">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
    <span style="font-size: 1.2rem; background: #f5f3ff; padding: 6px; border-radius: 8px; border: 1px solid #ddd6fe;">🌊</span>
    <div>
        <div style="font-weight: 700; font-size: 0.88rem; color: #0f172a;">Superposition</div>
        <div style="font-size: 0.72rem; color: #7c3aed; font-weight: 600;">Module 4 • In Progress</div>
    </div>
</div>
<div class="metric-bar-bg" style="margin-top: 6px; margin-bottom: 10px;">
    <div class="metric-bar-fill" style="width: 60%; background: #7c3aed;"></div>
</div>
</div>""", unsafe_allow_html=True)
            if st.button("▶ Continue Superposition", key="btn_nav_super", use_container_width=True):
                navigate_to("🌊 Quantum Superposition")

        with c_mod2:
            st.markdown("""<div class="continue-module-card" style="margin-bottom: 8px;">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
    <span style="font-size: 1.2rem; background: #f0f9ff; padding: 6px; border-radius: 8px; border: 1px solid #bae6fd;">⚙️</span>
    <div>
        <div style="font-weight: 700; font-size: 0.88rem; color: #0f172a;">Quantum Gates</div>
        <div style="font-size: 0.72rem; color: #64748b; font-weight: 600;">Module 5 • Next Up</div>
    </div>
</div>
<div class="metric-bar-bg" style="margin-top: 6px; margin-bottom: 10px;">
    <div class="metric-bar-fill" style="width: 0%; background: #0284c7;"></div>
</div>
</div>""", unsafe_allow_html=True)
            if st.button("▶ Start Quantum Gates", key="btn_nav_gates", use_container_width=True):
                navigate_to("⚙️ Quantum Gates")

        with c_mod3:
            st.markdown("""<div class="continue-module-card" style="margin-bottom: 8px;">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
    <span style="font-size: 1.2rem; background: #ecfdf5; padding: 6px; border-radius: 8px; border: 1px solid #a7f3d0;">🧪</span>
    <div>
        <div style="font-weight: 700; font-size: 0.88rem; color: #0f172a;">Guided Projects</div>
        <div style="font-size: 0.72rem; color: #64748b; font-weight: 600;">Hands-on Labs</div>
    </div>
</div>
<div class="metric-bar-bg" style="margin-top: 6px; margin-bottom: 10px;">
    <div class="metric-bar-fill" style="width: 0%; background: #059669;"></div>
</div>
</div>""", unsafe_allow_html=True)
            if st.button("▶ Explore Projects", key="btn_nav_projects", use_container_width=True):
                navigate_to("🧪 Guided Quantum Projects")

    with col_right:
        # Quantum Simulator Preview Card
        st.markdown("""<div class="quantum-card" style="margin-bottom: 10px;">
<div class="quantum-card-title" style="margin-bottom: 4px;">⚛️ Quantum Simulator</div>
<div style="font-size: 0.8rem; color: #64748b; margin-bottom: 12px;">Run circuits and visualize probabilities in real-time.</div>
<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; line-height: 1.8; color: #334155; margin-bottom: 12px;">
    <div><span style="font-weight: 700; color: #7c3aed;">q0 |0⟩</span> ── <span style="background: #ede9fe; color: #6d28d9; padding: 2px 7px; border-radius: 4px; font-weight: 700; border: 1px solid #ddd6fe;">H</span> ─── <span style="color: #7c3aed; font-weight: 900;">●</span> ────────── <span style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; border: 1px solid #cbd5e1; font-weight: 700;">M</span></div>
    <div><span style="font-weight: 700; color: #7c3aed;">q1 |0⟩</span> ─────────── <span style="color: #7c3aed; font-weight: 900;">┼</span> ── <span style="background: #e0f2fe; color: #0284c7; padding: 2px 7px; border-radius: 4px; font-weight: 700; border: 1px solid #bae6fd;">X</span> ───── <span style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; border: 1px solid #cbd5e1; font-weight: 700;">M</span></div>
    <div><span style="font-weight: 700; color: #7c3aed;">c2</span> ══════════════════════ <span style="color: #94a3b8; font-weight: 700;">//</span> ═</div>
</div>
</div>""", unsafe_allow_html=True)
        if st.button("🚀 Launch Quantum Simulator", key="btn_launch_sim", use_container_width=True):
            navigate_to("⚛️ Quantum Circuit Simulator")

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        # Quick Actions Card with Functional Navigation Buttons
        st.markdown("""<div class="quantum-card" style="padding-bottom: 12px;">
<div class="quantum-card-title" style="margin-bottom: 12px;">⚡ Quick Actions</div>
</div>""", unsafe_allow_html=True)

        if st.button("🧪 Quantum Playground Lab", key="btn_qa_pg", use_container_width=True):
            navigate_to("🧪 Quantum Playground")
        if st.button("🔔 Bell State Experiment", key="btn_qa_bell", use_container_width=True):
            navigate_to("🔔 Bell State Experiment")
        if st.button("📝 Take a Beginner Quiz", key="btn_qa_quiz", use_container_width=True):
            navigate_to("❓ Beginner Quiz")
        if st.button("📖 Browse Quantum Glossary", key="btn_qa_gloss", use_container_width=True):
            navigate_to("📖 Quantum Glossary")

    # Detailed Overview Card with Original Content
    st.markdown("""
    <div class="quantum-card">
        <div class="quantum-card-title">📖 Platform Overview & Architecture</div>
        <p style="color: #475569; line-height: 1.7; font-size: 0.95rem;">
        This platform is designed for a learner who may have no previous
        knowledge of quantum computing. Instead of presenting only definitions,
        each module explains the idea, the reason behind the operation, what
        happens inside a quantum circuit, what the simulator is doing, and how
        to interpret the result.
        </p>
        <p style="color: #475569; line-height: 1.7; font-size: 0.95rem;">
        The current prototype uses a local <strong>Qiskit Aer simulator</strong>. This means
        experiments can be performed without a physical quantum computer or an
        IBM Quantum account. A future version can connect the same learning
        workflow to real quantum hardware.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Recommended Learning Path Accordion/Cards
    with st.expander("🗺️ Full Recommended Learning Path (11 Modules)", expanded=False):
        learning_path = [
            ("1", "Introduction", "Understand what quantum computing is and why it is different."),
            ("2", "Classical vs Quantum", "Learn the difference between bits, qubits and processors."),
            ("3", "Qubit", "Understand |0>, |1>, amplitudes and quantum states."),
            ("4", "Superposition", "Learn how a qubit can be prepared in a combination of states."),
            ("5", "Quantum Gates", "Learn how gates change a qubit's state."),
            ("6", "Measurement", "Understand how a quantum state becomes a classical result."),
            ("7", "Circuits", "Combine gates into complete quantum algorithms."),
            ("8", "Entanglement", "Understand correlations between multiple qubits."),
            ("9", "Simulator", "Build and test your own circuits."),
            ("10", "Projects", "Apply the concepts to practical mini-projects."),
            ("11", "Quantum AI/ML", "Understand how quantum circuits can work with classical ML.")
        ]

        for number, title, description in learning_path:
            st.markdown(f"**{number}. {title}** — {description}")

    st.info("""
    **Current development stage:** classical local simulation.
    The architecture is intentionally kept separate from hardware access,
    so real IBM Quantum hardware can be added later without changing the
    beginner learning modules.
    """)




# ============================================================

# INTRODUCTION

# ============================================================



elif page == "🌱 Introduction to Quantum Computing":

    st.title("🌱 Introduction to Quantum Computing")



    st.header("What is Quantum Computing?")

    st.write("""

    Quantum computing is a computing approach based on the principles of

    quantum mechanics. Classical computers represent information with bits,

    while quantum computers use qubits.



    The important point for a beginner is that a quantum computer does not

    simply replace a normal computer. Quantum processors are especially

    interesting for certain mathematical, simulation, optimization and

    cryptographic problems. Many useful systems are expected to be hybrid:

    classical computers perform ordinary tasks while quantum processors

    handle selected quantum workloads.

    """)



    st.header("Why do we need qubits?")

    st.write("""

    A classical bit has two possible values: 0 or 1. A qubit also has two

    computational basis states, |0> and |1>, but its quantum state can be

    represented as a combination of those basis states.



    This gives quantum algorithms a different mathematical representation

    of information. Quantum gates then transform that state before

    measurement.

    """)



    st.latex(r"\lvert\psi\rangle = \alpha\lvert0\rangle + \beta\lvert1\rangle")



    st.write("""

    Here α and β are probability amplitudes. For a valid normalized state,

    the squared magnitudes of the amplitudes add to one.

    """)



    st.latex(r"|\alpha|^2 + |\beta|^2 = 1")



    st.header("🔄 The basic quantum computing process")

    st.code("""

Classical input

      |

      v

Encode information into qubits

      |

      v

Apply quantum gates

      |

      v

Create useful quantum state

      |

      v

Measure qubits

      |

      v

Classical output

""")



    st.write("""

    The simulator follows this same conceptual process. You construct a

    circuit, choose gates, optionally measure the qubits, execute the

    circuit repeatedly, and inspect the distribution of classical results.

    """)



    st.header("🌍 Potential application areas")

    applications = pd.DataFrame({

        "Area": [

            "Drug discovery",

            "Chemistry and materials",

            "Optimization",

            "Cryptography",

            "Finance",

            "Quantum machine learning",

            "Scientific simulation"

        ],

        "What researchers investigate": [

            "Molecular and drug interaction simulation",

            "Properties of molecules and materials",

            "Combinatorial and routing problems",

            "Quantum communication and security",

            "Portfolio and risk-related optimization",

            "Hybrid quantum-classical learning methods",

            "Physical systems difficult to model classically"

        ]

    })

    st.dataframe(applications, use_container_width=True, hide_index=True)



    beginner_box(

        "Start here",

        "Do not try to memorize every quantum term immediately. First understand "

        "the flow: qubit -> gate -> circuit -> measurement -> classical result. "

        "The later modules build each part of this flow separately."

    )



# ============================================================

# CLASSICAL VS QUANTUM

# ============================================================



elif page == "💻 Classical vs Quantum Computing":

    st.title("💻 Classical vs ⚛️ Quantum Computing")



    st.write("""

    Classical and quantum computers both process information, but they use

    different physical and mathematical models. A beginner should first

    understand that a qubit is not just a faster version of a bit.

    """)



    comparison = pd.DataFrame({

        "Topic": [

            "Basic information unit",

            "Possible computational basis values",

            "Operations",

            "Output",

            "Typical hardware",

            "Programming model"

        ],

        "Classical Computing": [

            "Bit",

            "0 or 1",

            "Logic gates",

            "Classical values",

            "CPU / GPU",

            "Classical algorithms"

        ],

        "Quantum Computing": [

            "Qubit",

            "|0> or |1> basis states and their combinations",

            "Quantum gates",

            "Measurement results",

            "QPU",

            "Quantum circuits / algorithms"

        ]

    })

    st.dataframe(comparison, use_container_width=True, hide_index=True)



    st.header("🧠 A useful mental model")

    st.write("""

    Imagine a classical bit as a switch whose logical state is either 0 or 1.

    A qubit is described mathematically by amplitudes. Quantum gates change

    those amplitudes and phases. When you finally measure the qubit, the

    measurement produces a classical result such as 0 or 1.

    """)



    st.latex(r"\lvert\psi\rangle = \alpha\lvert0\rangle + \beta\lvert1\rangle")



    st.header("⚠️ Important beginner point")

    st.warning("""

    A qubit should not be explained simply as "both 0 and 1 at the same time".

    That phrase is a useful informal introduction, but the precise description

    is a quantum state with amplitudes. Measurement gives one classical result.

    """)



# ============================================================

# QUBIT

# ============================================================



elif page == "🔵 What is a Qubit?":

    st.title("🔵 What is a Qubit?")



    st.write("""

    A qubit is the fundamental unit of quantum information. It is the

    quantum analogue of a classical bit, but its state is represented using

    complex probability amplitudes.

    """)



    st.header("1. Computational basis")

    st.write("""

    The two basis states are written as |0> and |1>. If a qubit is definitely

    in |0>, measurement in the computational basis produces 0. If it is

    definitely in |1>, measurement produces 1.

    """)



    st.latex(r"\lvert0\rangle,\qquad \lvert1\rangle")



    st.header("2. General single-qubit state")

    st.latex(r"\lvert\psi\rangle = \alpha\lvert0\rangle + \beta\lvert1\rangle")



    st.write("""

    α and β describe the amplitudes associated with the two basis states.

    Their squared magnitudes determine the probabilities of the two

    measurement outcomes.

    """)



    st.latex(r"P(0)=|\alpha|^2")

    st.latex(r"P(1)=|\beta|^2")

    st.latex(r"|\alpha|^2+|\beta|^2=1")



    st.header("3. What happens during measurement?")

    st.write("""

    Before measurement, the state is represented by amplitudes. When the

    computational basis is measured, the simulator samples an outcome

    according to the corresponding probabilities. After measurement, the

    application receives a classical bit string.

    """)



    beginner_box(

        "Qubit",

        "Remember this sequence: |0> and |1> are basis states; α and β are "

        "amplitudes; squared magnitudes give probabilities; measurement gives "

        "a classical result."

    )



# ============================================================

# SUPERPOSITION

# ============================================================



elif page == "🌊 Quantum Superposition":

    st.title("🌊 Quantum Superposition")



    st.write("""

    Superposition means that a quantum state can be represented as a linear

    combination of basis states. It is one of the core ideas behind quantum

    algorithms.

    """)



    st.latex(r"\lvert\psi\rangle = \alpha\lvert0\rangle+\beta\lvert1\rangle")



    st.header("🔬 What happens when we use the H gate?")

    st.write("""

    If the qubit starts in |0>, the Hadamard gate creates an equal

    superposition:



    The important learning sequence is:



    1. The qubit starts in |0>.

    2. The H gate changes its quantum state.

    3. The state becomes a combination of |0> and |1>.

    4. Measurement samples one of those outcomes.

    5. Repeating the experiment many times produces an approximately

       balanced distribution.

    """)



    st.latex(r"H\lvert0\rangle=\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}}")

    st.subheader("⚛️ Superposition Circuit")
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    circuit_diagram(qc)

    shots = st.slider("Number of measurements (shots)", 100, 5000, 1000, 100, key="super_shots")

    if st.button("🚀 Run Superposition Experiment", use_container_width=True, key="btn_run_super_exp"):
        st.subheader("📊 Measurement Results")
        counts = run_circuit(qc, shots)
        show_results(counts, 1, shots)
        try:
            path = save_experiment("Superposition", qc, counts, 1, shots)
            st.success(f"✅ Experiment simulated & saved: {path}")
        except Exception as exc:
            st.warning(f"Experiment simulated successfully: {exc}")

    beginner_box(
        "Why are results not exactly 50/50?",
        "The ideal probabilities are 50% and 50%, but a finite number of random measurements will usually not produce exactly equal counts. As the number of shots increases, the observed distribution tends to become closer to the theoretical probabilities."
    )




# ============================================================

# QUANTUM GATES

# ============================================================



elif page == "⚙️ Quantum Gates":
    st.title("⚙️ Quantum Gates")

    st.write("""
    Quantum gates are the basic building blocks of quantum circuits. 
    Just like classical logic gates change bits from 0 to 1, quantum gates transform 
    qubits by creating superposition, flipping bits, or shifting wave angles.
    """)

    show_circuit_explanation("⚙️ Quantum Gates")

    gate = st.selectbox(
        "Select a gate to learn",
        [
            "H — Superposition Gate",
            "X — Bit Flip Gate",
            "Y — Bit + Phase Flip Gate",
            "Z — Phase Flip Gate",
            "S — 90° Phase Gate",
            "T — 45° Phase Gate",
            "CNOT — Controlled Flip Gate",
            "SWAP — Swap Gate"
        ]
    )

    gate_details = {
        "H — Superposition Gate": {
            "type": "Superposition Gate",
            "purpose": "Splits a qubit into an equal 50/50 mix of 0 and 1.",
            "effect": "Turns a definite state |0⟩ or |1⟩ into a balanced combination where outcome 0 and outcome 1 are equally likely. Applying it twice returns the qubit back to its original state.",
            "measurement": "When measured, yields approximately 50% 0 and 50% 1.",
            "matrix": r"H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}",
            "step_0": r"H\lvert0\rangle = \frac{\lvert0\rangle + \lvert1\rangle}{\sqrt{2}} = \lvert+\rangle",
            "step_1": r"H\lvert1\rangle = \frac{\lvert0\rangle - \lvert1\rangle}{\sqrt{2}} = \lvert-\rangle",
            "step_explain": "Hadamard transforms computational states into superposition states. Applying H twice cancels out: H(H|0⟩) = |0⟩.",
            "example": "Start: |0⟩ → Apply H → Superposition (50/50 mix) → Measure → ~50% 0, ~50% 1"
        },

        "X — Bit Flip Gate": {
            "type": "Bit Flip Gate (Quantum NOT)",
            "purpose": "Flips a qubit from 0 to 1, or from 1 to 0.",
            "effect": "Reverses the qubit state (the direct quantum equivalent of a classical NOT switch).",
            "measurement": "Measuring |0⟩ after X yields 100% 1; measuring |1⟩ after X yields 100% 0.",
            "matrix": r"X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}",
            "step_0": r"X\lvert0\rangle = \lvert1\rangle",
            "step_1": r"X\lvert1\rangle = \lvert0\rangle",
            "step_explain": "The X gate swaps amplitudes between state |0⟩ and state |1⟩.",
            "example": "Start: |0⟩ → Apply X → |1⟩ → Measure → 1 (100%)\nStart: |1⟩ → Apply X → |0⟩ → Measure → 0 (100%)"
        },

        "Y — Bit + Phase Flip Gate": {
            "type": "Bit + Phase Flip Gate",
            "purpose": "Flips the qubit bit value while also twisting its wave phase.",
            "effect": "Combines a bit-flip (X) and a phase-flip (Z) in a single operation.",
            "measurement": "Flips measurement outcomes (0 ↔ 1) while adding a complex phase factor.",
            "matrix": r"Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}",
            "step_0": r"Y\lvert0\rangle = i\lvert1\rangle",
            "step_1": r"Y\lvert1\rangle = -i\lvert0\rangle",
            "step_explain": "Y combines both X (bit-flip) and Z (phase-flip) operations: Y = iXZ.",
            "example": "Start: |0⟩ → Apply Y → i|1⟩ → Measure → 1 (100%)\nStart: |1⟩ → Apply Y → -i|0⟩ → Measure → 0 (100%)"
        },

        "Z — Phase Flip Gate": {
            "type": "Phase Flip Gate",
            "purpose": "Leaves 0 unchanged and flips the wave sign of 1.",
            "effect": "Keeps state |0⟩ untouched, and applies a 180° phase flip (minus sign) to state |1⟩.",
            "measurement": "Direct measurement on |1⟩ still shows 1; the phase flip becomes visible when combined with superposition.",
            "matrix": r"Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}",
            "step_0": r"Z\lvert0\rangle = \lvert0\rangle",
            "step_1": r"Z\lvert1\rangle = -\lvert1\rangle",
            "step_explain": "Z multiplies the |1⟩ amplitude by -1 while leaving |0⟩ completely unchanged.",
            "example": "Start: |0⟩ → Apply Z → |0⟩ → Measure → 0 (100%)\nStart: |1⟩ → Apply Z → -|1⟩ → Measure → 1 (100%)\nInterference Test: |0⟩ → H → Z → H → Measure → 1 (100% proof of phase flip)"
        },

        "S — 90° Phase Gate": {
            "type": "90° Phase Gate",
            "purpose": "Leaves 0 unchanged and applies a 90° quarter-turn phase shift to 1.",
            "effect": "Keeps state |0⟩ untouched, and rotates the wave phase of state |1⟩ by 90°.",
            "measurement": "Two S gates applied together equal one Z gate (90° + 90° = 180° phase flip).",
            "matrix": r"S = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}",
            "step_0": r"S\lvert0\rangle = \lvert0\rangle",
            "step_1": r"S\lvert1\rangle = i\lvert1\rangle",
            "step_explain": "S acts as the square-root of Z (S × S = Z), adding a +90° (π/2) phase shift to |1⟩.",
            "example": "Start: |0⟩ → Apply S → |0⟩ → Measure → 0 (100%)\nStart: |1⟩ → Apply S → i|1⟩ → Measure → 1 (100%)\nRelationship: S² = Z"
        },

        "T — 45° Phase Gate": {
            "type": "45° Phase Gate",
            "purpose": "Leaves 0 unchanged and applies a 45° eighth-turn phase shift to 1.",
            "effect": "Keeps state |0⟩ untouched, and rotates the wave phase of state |1⟩ by 45°.",
            "measurement": "Two T gates equal one S gate (45° + 45° = 90°), and four T gates equal one Z gate.",
            "matrix": r"T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}",
            "step_0": r"T\lvert0\rangle = \lvert0\rangle",
            "step_1": r"T\lvert1\rangle = e^{i\pi/4}\lvert1\rangle",
            "step_explain": "T acts as the fourth-root of Z (T⁴ = Z), adding a +45° (π/4) phase shift to |1⟩.",
            "example": "Start: |0⟩ → Apply T → |0⟩ → Measure → 0 (100%)\nStart: |1⟩ → Apply T → e^(iπ/4)|1⟩ → Measure → 1 (100%)\nInterference Test: |0⟩ → H → T → H → Measure → ~85.35% 0 and ~14.65% 1"
        },

        "CNOT — Controlled Flip Gate": {
            "type": "Controlled Flip Gate (Two-Qubit)",
            "purpose": "Flips the second qubit (Target) if and only if the first qubit (Control) is 1.",
            "effect": "If Control is 0 → Target stays unchanged. If Control is 1 → Target flips (0 ↔ 1). If Control is in superposition, creates quantum entanglement.",
            "measurement": "Correlates the measurement outcomes of both qubits.",
            "matrix": r"\text{CNOT} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}",
            "step_0": r"\text{CNOT}\lvert00\rangle = \lvert00\rangle, \quad \text{CNOT}\lvert01\rangle = \lvert01\rangle",
            "step_1": r"\text{CNOT}\lvert10\rangle = \lvert11\rangle, \quad \text{CNOT}\lvert11\rangle = \lvert10\rangle",
            "step_explain": "Conditional operation: target is inverted only when control qubit is |1⟩.",
            "example": "Input |00⟩ → CNOT → |00⟩\nInput |10⟩ → CNOT → |11⟩\nInput |01⟩ → CNOT → |01⟩\nInput |11⟩ → CNOT → |10⟩"
        },

        "SWAP — Swap Gate": {
            "type": "Swap Gate (Two-Qubit)",
            "purpose": "Swaps the quantum states of two qubits (Q0 ↔ Q1).",
            "effect": "Moves whatever state is on Qubit 0 over to Qubit 1, and vice versa.",
            "measurement": "Exchanges the observed classical bits between the two qubit wires.",
            "matrix": r"\text{SWAP} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}",
            "step_0": r"\text{SWAP}\lvert00\rangle = \lvert00\rangle, \quad \text{SWAP}\lvert11\rangle = \lvert11\rangle",
            "step_1": r"\text{SWAP}\lvert01\rangle = \lvert10\rangle, \quad \text{SWAP}\lvert10\rangle = \lvert01\rangle",
            "step_explain": "Exchanges state amplitudes between basis states |01⟩ and |10⟩.",
            "example": "Input |01⟩ → SWAP → |10⟩\nInput |10⟩ → SWAP → |01⟩\nInput |00⟩ → SWAP → |00⟩\nInput |11⟩ → SWAP → |11⟩"
        }
    }

    details = gate_details[gate]

    st.header(f"🔎 {gate}")
    st.info(f"**🏷️ Type:** {details['type']}")
    st.write(f"**🎯 What it does:** {details['purpose']}")
    st.write(f"**🔄 Effect on Qubit:** {details['effect']}")
    st.write(f"**📊 Measurement:** {details['measurement']}")

    with st.expander("🔬 Advanced Details (Matrix & Mathematical Representation)", expanded=False):
        st.subheader("📐 Matrix Representation")
        st.latex(details["matrix"])
        st.subheader("🔬 Step-by-Step State Action")
        c_s0, c_s1 = st.columns(2)
        with c_s0:
            st.markdown("##### Action on State $\\lvert0\\rangle$")
            st.latex(details["step_0"])
        with c_s1:
            st.markdown("##### Action on State $\\lvert1\\rangle$")
            st.latex(details["step_1"])
        st.write(details["step_explain"])

    st.subheader("🔄 Beginner Execution Flow")
    st.code(details["example"], language="text")

    st.divider()



    st.subheader("🧪 Interactive Gate Simulation")

    st.write("Select the initial qubit state below to see how the circuit dynamically prepares the input before applying the gate:")



    if gate.startswith(("CNOT", "SWAP")):

        c_q0, c_q1, c_shots = st.columns(3)

        with c_q0:

            init_q0 = st.radio(

                "Q0 (Control / First) Initial State:",

                ["|0⟩", "|1⟩"],

                horizontal=True,

                key="gate_init_q0"

            )

        with c_q1:

            init_q1 = st.radio(

                "Q1 (Target / Second) Initial State:",

                ["|0⟩", "|1⟩"],

                horizontal=True,

                key="gate_init_q1"

            )

        with c_shots:

            shots = st.slider("Shots (Measurements)", 100, 5000, 1000, 100, key="gate_shots_2q")



        st.caption(f"🏁 Prepared Input State: **{init_q0[0:2]}{init_q1[1]}**")



        if st.button("🚀 Run Selected Gate", use_container_width=True):

            qc = QuantumCircuit(2, 2)

            if "|1⟩" in init_q0:

                qc.x(0)

            if "|1⟩" in init_q1:

                qc.x(1)



            if gate.startswith("CNOT"):

                qc.cx(0, 1)

            elif gate.startswith("SWAP"):

                qc.swap(0, 1)



            qc.measure([0, 1], [0, 1])

            run_and_save(gate, qc, 2, shots)

    else:

        c_init, c_shots = st.columns([1, 1])

        with c_init:

            initial_state = st.radio(

                "Select Initial Qubit State:",

                ["|0⟩ (Default Ground State)", "|1⟩ (Excited State)"],

                horizontal=True,

                key="gate_init_state_1q"

            )

        with c_shots:

            shots = st.slider("Shots (Measurements)", 100, 5000, 1000, 100, key="gate_shots_1q")



        enable_hadamard_sandwich = False

        if gate.startswith(("Z", "S", "T")):

            enable_hadamard_sandwich = st.checkbox(

                "🌈 Reveal Phase Shift via Interference (Hadamard Sandwich: H → Gate → H)",

                value=False,

                help="Applies an H gate before and after the phase gate. This turns phase shifts into measurable probability differences through quantum interference!"

            )



        st.caption(f"🏁 Prepared Input State: **{'|1⟩' if '|1⟩' in initial_state else '|0⟩'}**" + (" *(with Hadamard Interference Sandwich)*" if enable_hadamard_sandwich else ""))



        if st.button("🚀 Run Selected Gate", use_container_width=True):

            qc = QuantumCircuit(1, 1)

            if "|1⟩" in initial_state:

                qc.x(0)



            if enable_hadamard_sandwich:

                qc.h(0)



            if gate.startswith("H"):

                qc.h(0)

            elif gate.startswith("X"):

                qc.x(0)

            elif gate.startswith("Y"):

                qc.y(0)

            elif gate.startswith("Z"):

                qc.z(0)

            elif gate.startswith("S"):

                qc.s(0)

            elif gate.startswith("T"):

                qc.t(0)



            if enable_hadamard_sandwich:

                qc.h(0)



            qc.measure(0, 0)

            run_name = gate if not enable_hadamard_sandwich else f"{gate} (Interference)"

            run_and_save(run_name, qc, 1, shots)



    beginner_box(
        "Why do S and T gates keep |0⟩ as |0⟩ and only shift |1⟩?",
        "Think of phase gates like a light switch with a color filter:\n\n"
        "• If the qubit is in state |0⟩, the gate leaves it completely untouched — no change happens to |0⟩.\n"
        "• If the qubit is in state |1⟩, the gate turns a phase dial (rotates the wave angle of |1⟩).\n\n"
        "Because phase gates only change the angle of |1⟩ while leaving |0⟩ untouched, state |0⟩ stays exactly as |0⟩."
    )

    beginner_box(
        "Why are phase differences only visible in measurement after superposition?",
        "A phase shift changes the quantum wave angle of a qubit, but measuring a single qubit directly only counts 0s and 1s — it cannot see the wave angle by itself!\n\n"
        "However, when the qubit is in a superposition (a mix of 0 and 1), the phase angle controls how the 0 and 1 parts bounce off each other (interference). "
        "Putting the qubit through an H gate afterwards converts those invisible wave angles into visible, measurable percentages (like 50/50% or 85/15%)."
    )

    beginner_box(
        "How does the Hadamard Sandwich (H → Gate → H) reveal phase shifts?",
        "The 'Hadamard Sandwich' is a simple 3-step test to make invisible phase shifts visible:\n\n"
        "1. First H Gate: Splits the qubit into an equal 50/50 mix of |0⟩ and |1⟩.\n"
        "2. Phase Gate (Z, S, or T): Twists the wave angle of the |1⟩ part.\n"
        "3. Second H Gate: Combines the 0 and 1 parts back together so the twisted angle turns into measurable percentages:\n"
        "   • Z Gate (180° twist) ➔ Result is 100% state |1⟩.\n"
        "   • S Gate (90° twist) ➔ Result is 50% state |0⟩ and 50% state |1⟩.\n"
        "   • T Gate (45° twist) ➔ Result is ~85.35% state |0⟩ and ~14.65% state |1⟩.\n\n"
        "Try checking the 'Reveal Phase Shift via Interference' box during simulation to test this live!"
    )



# ============================================================

# ENTANGLEMENT

# ============================================================



elif page == "🔗 Quantum Entanglement":

    st.title("🔗 Quantum Entanglement")



    st.write("""

    Entanglement occurs when the joint quantum state of multiple qubits cannot

    be described as independent states of each qubit. The qubits must be

    considered as one combined quantum system.

    """)



    st.header("🔔 Bell state example")

    st.latex(r"\lvert\Phi^+\rangle=\frac{\lvert00\rangle+\lvert11\rangle}{\sqrt{2}}")



    st.write("""

    The Bell state above is created by starting with |00>, applying H to the

    first qubit, and then applying CNOT. The resulting state contains the

    |00> and |11> components.



    When measured in the computational basis, the results are correlated:

    if the first measurement is 0, the second is 0; if the first is 1, the

    second is 1, in the ideal circuit.

    """)



    st.code("""

Start:        |00>

                |

Apply H:       (|00> + |10>) / sqrt(2)

                |

Apply CNOT:    (|00> + |11>) / sqrt(2)

                |

Measure:       00 or 11

""")



    st.warning("""

    Entanglement does not mean that information can be sent faster than light.

    It describes correlations in the joint quantum state.

    """)



# ============================================================

# MEASUREMENT

# ============================================================



elif page == "📏 Quantum Measurement":

    st.title("📏 Quantum Measurement")



    st.write("""

    Measurement is the step that converts quantum information into a

    classical observation. A quantum circuit can contain amplitudes and

    phases, but when we measure in the computational basis, the result is

    a classical bit string.

    """)



    st.header("🔄 Measurement process")

    st.code("""

Quantum state

     |

     v

Measurement basis

     |

     v

Probability sampling

     |

     v

Classical result

     |

     v

0, 1, 00, 01, 10, 11, ...

""")



    st.write("""

    For example, if a qubit is prepared in an equal superposition, the

    theoretical probability of measuring 0 is 50% and the probability of

    measuring 1 is 50%. The simulator samples from those probabilities.

    """)



    st.header("🎯 Why do we use many shots?")

    st.write("""

    One measurement gives only one outcome. Running the same circuit many

    times allows us to estimate the probability distribution. This is why

    quantum experiments commonly use hundreds or thousands of shots.

    """)



    st.latex(r"P(x)\approx\frac{\text{number of times outcome }x\text{ is observed}}{\text{total shots}}")



    st.success("""

    In this platform, the probability chart converts the raw measurement

    counts into an easier-to-understand percentage distribution.

    """)



# ============================================================

# QUANTUM CIRCUITS

# ============================================================



elif page == "🧩 Quantum Circuits":

    st.title("🧩 Quantum Circuits")



    st.write("""

    A quantum circuit is an ordered sequence of operations on qubits.

    The horizontal wires represent qubits and the operations placed along

    the wires represent gates. Measurements connect the quantum part of

    the computation to classical output.

    """)



    st.code("""

q0 ── H ─────●──── M

             │

q1 ──────────X──── M

""")



    st.header("🔍 Read the circuit from left to right")

    steps = [

        "Qubits are initialized, normally in |0>.",

        "The H gate creates a superposition on q0.",

        "The CNOT uses q0 as a control and q1 as a target.",

        "The two-qubit state can become entangled.",

        "Measurement converts the final quantum state into classical bits."

    ]

    for i, step in enumerate(steps, 1):

        st.write(f"**Step {i}:** {step}")



    st.header("🧱 Circuit building blocks")

    blocks = pd.DataFrame({

        "Component": ["Qubit wire", "Single-qubit gate", "Controlled gate", "Measurement"],

        "Meaning": [

            "Carries the quantum state",

            "Changes one qubit",

            "Creates conditional multi-qubit operations",

            "Produces classical output"

        ]

    })

    st.dataframe(blocks, use_container_width=True, hide_index=True)



# ============================================================

# INTERACTIVE CIRCUIT SIMULATOR

# ============================================================



elif page == "⚛️ Quantum Circuit Simulator":

    st.title("⚛️ Interactive Quantum Circuit Simulator")



    st.success("""

    🟢 LOCAL SIMULATOR MODE



    This simulator uses Qiskit Aer on your computer. You can build circuits

    using H, X, Y, Z, S, T, CNOT and SWAP without requiring physical quantum

    hardware or an IBM Quantum API key.

    """)



    st.header("1️⃣ Choose circuit size")

    num_qubits = int(st.number_input(

        "Number of qubits",

        min_value=1,

        max_value=4,

        value=2,

        step=1

    ))



    shots = int(st.number_input(

        "Number of shots",

        min_value=100,

        max_value=10000,

        value=1000,

        step=100

    ))



    st.header("2️⃣ Choose a gate for each qubit")

    st.write("""

    The single-qubit choices are applied from the initial |0> state.

    You can then optionally add a two-qubit CNOT or SWAP operation.

    """)



    options = ["None", "H", "X", "Y", "Z", "S", "T"]

    selected = []



    for q in range(num_qubits):

        selected.append(

            st.selectbox(

                f"Gate for Qubit {q}",

                options,

                key=f"sim_gate_{q}"

            )

        )



    st.header("3️⃣ Add a two-qubit operation")

    two_qubit = st.selectbox(

        "Optional two-qubit operation",

        ["None", "CNOT (Q0 → Q1)", "SWAP (Q0 ↔ Q1)"]

    )



    if num_qubits < 2 and two_qubit != "None":

        st.warning("CNOT and SWAP require at least two qubits.")



    add_measurement = st.checkbox(

        "📏 Measure all qubits",

        value=True

    )



    if st.button("🚀 Build and Run Circuit", use_container_width=True):

        qc = QuantumCircuit(num_qubits, num_qubits)



        for q, gate in enumerate(selected):

            if gate == "H":

                qc.h(q)

            elif gate == "X":

                qc.x(q)

            elif gate == "Y":

                qc.y(q)

            elif gate == "Z":

                qc.z(q)

            elif gate == "S":

                qc.s(q)

            elif gate == "T":

                qc.t(q)



        if num_qubits >= 2:

            if two_qubit.startswith("CNOT"):

                qc.cx(0, 1)

            elif two_qubit.startswith("SWAP"):

                qc.swap(0, 1)



        if add_measurement:

            qc.measure(range(num_qubits), range(num_qubits))



        st.subheader("🧩 Generated Circuit")

        circuit_diagram(qc)



        if add_measurement:

            run_and_save(

                "Interactive Circuit Simulator",

                qc,

                num_qubits,

                shots

            )

        else:

            st.info("Measurements were disabled, so no count distribution is produced.")



    st.divider()

    st.header("🧠 How the simulator works")

    st.write("""

    1. You select the number of qubits.

    2. The program creates a Qiskit QuantumCircuit.

    3. The selected gates are appended to the circuit.

    4. Optional CNOT or SWAP operations are added.

    5. Measurements are added when requested.

    6. Qiskit transpiles the circuit for Aer.

    7. Aer simulates the circuit many times according to the number of shots.

    8. The resulting classical bit strings are counted.

    9. The platform converts those counts into probabilities and displays a chart.

    """)



# ============================================================

# SIMULATION ACCESS & PLAYGROUND

# ============================================================



elif page == "🚀 Simulation Access & Playground":

    st.title("🚀 Quantum Simulation Access & Playground")

    st.caption("Complete quantum circuit studio: design custom multi-qubit circuits or instantly execute pre-built guided projects with real-time Aer simulation.")



    tab_custom, tab_guided = st.tabs([

        "🎛️ Interactive Custom Playground",

        "🧪 Guided Quantum Projects Quick-Run"

    ])



    with tab_custom:

        st.subheader("🛠️ Custom Circuit Builder")

        st.write("Configure qubit counts, customize initial state vectors, construct multi-layer gate sequences, and run live simulation.")



        col_c1, col_c2, col_c3 = st.columns([1, 1, 1])

        with col_c1:

            num_qubits = st.slider("Number of Qubits", min_value=1, max_value=4, value=2, key="pg_num_qubits")

        with col_c2:

            shots = st.slider("Simulation Shots", min_value=100, max_value=5000, value=1000, step=100, key="pg_shots")

        with col_c3:

            num_layers = st.slider("Circuit Gate Depth (Steps)", min_value=1, max_value=4, value=2, key="pg_num_layers")



        st.markdown("#### 1️⃣ Initial State Preparation")

        st.write("Select the initial computational basis state for each qubit:")

        init_cols = st.columns(num_qubits)

        init_states = []

        for q in range(num_qubits):

            with init_cols[q]:

                init_val = st.radio(

                    f"Qubit {q} Init:",

                    ["|0⟩", "|1⟩"],

                    index=0,

                    horizontal=True,

                    key=f"pg_init_q_{q}"

                )

                init_states.append(init_val)



        state_str = "".join(["1" if "|1⟩" in s else "0" for s in init_states])

        st.caption(f"🏁 Overall Prepared Input State: **|{state_str}⟩**")



        st.markdown("#### 2️⃣ Single-Qubit Gate Specifications")

        gate_options = ["None", "H", "X", "Y", "Z", "S", "T"]

        layer_gates = []



        for step in range(num_layers):

            st.markdown(f"**Step {step + 1} Gates:**")

            g_cols = st.columns(num_qubits)

            step_gates = []

            for q in range(num_qubits):

                with g_cols[q]:

                    g = st.selectbox(

                        f"Q{q} Gate (Step {step + 1})",

                        gate_options,

                        index=0,

                        key=f"pg_g_s{step}_q{q}"

                    )

                    step_gates.append(g)

            layer_gates.append(step_gates)



        st.markdown("#### 3️⃣ Multi-Qubit Entangling Operations")

        multi_ops = []

        if num_qubits >= 2:

            num_two_qubit = st.selectbox(

                "Number of Two-Qubit Operations to append:",

                [0, 1, 2],

                index=1 if num_qubits >= 2 else 0,

                key="pg_num_2q_ops"

            )



            for i in range(num_two_qubit):

                c_op, c_ctrl, c_tgt = st.columns([1, 1, 1])

                with c_op:

                    op_type = st.selectbox(f"Operation #{i + 1}", ["None", "CNOT", "SWAP", "CZ"], key=f"pg_2q_op_{i}")

                with c_ctrl:

                    ctrl_q = st.selectbox(f"Control Qubit #{i + 1}", list(range(num_qubits)), index=0, key=f"pg_ctrl_{i}")

                with c_tgt:

                    tgt_q = st.selectbox(f"Target Qubit #{i + 1}", list(range(num_qubits)), index=min(1, num_qubits - 1), key=f"pg_tgt_{i}")



                if op_type != "None":

                    if ctrl_q == tgt_q:

                        st.warning(f"⚠️ Operation #{i + 1}: Control and Target qubits must be different!")

                    else:

                        multi_ops.append((op_type, ctrl_q, tgt_q))

        else:

            st.info("ℹ️ Multi-qubit operations (CNOT, SWAP, CZ) require at least 2 qubits.")



        measure_all = st.checkbox("📏 Measure All Qubits at the End", value=True, key="pg_measure_all")



        if st.button("🚀 Execute Custom Circuit on Aer Simulator", use_container_width=True, key="pg_run_custom"):

            qc = QuantumCircuit(num_qubits, num_qubits)



            # Step 1: Initial state preparation

            for q, s in enumerate(init_states):

                if "|1⟩" in s:

                    qc.x(q)



            # Step 2: Layered single-qubit gates

            for step_gates in layer_gates:

                for q, g in enumerate(step_gates):

                    if g == "H":

                        qc.h(q)

                    elif g == "X":

                        qc.x(q)

                    elif g == "Y":

                        qc.y(q)

                    elif g == "Z":

                        qc.z(q)

                    elif g == "S":

                        qc.s(q)

                    elif g == "T":

                        qc.t(q)



            # Step 3: Multi-qubit entangling operations

            for op_type, ctrl, tgt in multi_ops:

                if op_type == "CNOT":

                    qc.cx(ctrl, tgt)

                elif op_type == "SWAP":

                    qc.swap(ctrl, tgt)

                elif op_type == "CZ":

                    qc.cz(ctrl, tgt)



            # Step 4: Measurement

            if measure_all:

                qc.measure(range(num_qubits), range(num_qubits))



            st.divider()

            st.markdown("### ⚛️ Execution & Measurement Results")

            if measure_all:

                run_and_save(f"Playground ({num_qubits}Q State |{state_str}⟩)", qc, num_qubits, shots)

            else:

                st.subheader("🧩 Generated Circuit")

                circuit_diagram(qc)

                st.info("Measurements were disabled, so no count distribution is generated.")



    with tab_guided:

        st.subheader("🧪 Guided Quantum Projects — Quick Access & Execution")

        st.write("Select any pre-configured guided quantum project to inspect its quantum circuit architecture, adjust shots, and run live simulation.")



        def _build_guided_bell():

            qc = QuantumCircuit(2, 2)

            qc.h(0)

            qc.cx(0, 1)

            qc.measure([0, 1], [0, 1])

            return qc



        def _build_guided_qrng(n=3):

            qc = QuantumCircuit(n, n)

            for i in range(n):

                qc.h(i)

            qc.measure(range(n), range(n))

            return qc



        def _build_guided_bb84():
            qc = QuantumCircuit(2, 2)
            qc.x(0)
            qc.h(0)
            qc.h(1)
            qc.h(0)
            qc.measure([0, 1], [0, 1])
            return qc



        def _build_guided_qml():

            import numpy as np

            qc = QuantumCircuit(2, 2)

            qc.ry(0.75 * np.pi, 0)

            qc.ry(1.25 * np.pi, 1)

            qc.cx(0, 1)

            qc.ry(0.5 * np.pi, 0)

            qc.measure([0, 1], [0, 1])

            return qc



        def _build_guided_superdense():

            qc = QuantumCircuit(2, 2)

            qc.h(0)

            qc.cx(0, 1)

            qc.z(0)

            qc.x(0)

            qc.cx(0, 1)

            qc.h(0)

            qc.measure([0, 1], [0, 1])

            return qc



        def _build_guided_teleportation():

            qc = QuantumCircuit(3, 3)

            qc.h(0)

            qc.s(0)

            qc.h(1)

            qc.cx(1, 2)

            qc.cx(0, 1)

            qc.h(0)

            qc.measure([0, 1], [0, 1])

            qc.cx(1, 2)

            qc.cz(0, 2)

            qc.measure(2, 2)

            return qc



        guided_projects = {

            "🔔 Bell State Entanglement (|Φ⁺⟩)": {

                "qubits": 2,

                "objective": "Generate maximally entangled 2-qubit Bell state (|00⟩ + |11⟩)/√2 and observe correlated measurement outcomes.",

                "description": "Applies a Hadamard gate to Q0 to create superposition, followed by a CNOT gate with Q0 controlling Q1. Measurement produces 00 and 11 with ~50% probability each.",

                "code": """qc = QuantumCircuit(2, 2)\nqc.h(0)\nqc.cx(0, 1)\nqc.measure([0, 1], [0, 1])""",

                "builder": _build_guided_bell

            },

            "🎲 Quantum Random Number Generator (QRNG)": {

                "qubits": 3,

                "objective": "Harvest true quantum randomness via parallel qubit superposition and projective measurement.",

                "description": "Applies Hadamard (H) gates to all qubits in parallel, putting each qubit in a 50/50 superposition (|0⟩+|1⟩)/√2. Measurement generates uniformly distributed random bitstrings.",

                "code": """qc = QuantumCircuit(3, 3)\nfor i in range(3):\n    qc.h(i)\nqc.measure(range(3), range(3))""",

                "builder": _build_guided_qrng

            },

            "🔐 BB84 Quantum Key Distribution (QKD)": {

                "qubits": 2,

                "objective": "Simulate quantum key generation between Alice and Bob across complementary rectilinear (Z) and diagonal (X) bases.",

                "description": "Alice encodes secret bits into random bases (Z: |0⟩/|1⟩, X: |+⟩/|-⟩). Bob measures in independently chosen bases. When their bases match, measurement yields identical shared key bits.",

                "code": """qc = QuantumCircuit(2, 2)\n# Alice prepares Q0 in X-basis bit 1, Q1 in Z-basis bit 0\nqc.x(0)\nqc.h(0)\n# Bob measures Q0 in X-basis, Q1 in Z-basis\nqc.h(0)\nqc.measure([0, 1], [0, 1])""",

                "builder": _build_guided_bb84

            },

            "🤖 Quantum Machine Learning (QML Feature Encoding)": {

                "qubits": 2,

                "objective": "Encode continuous classical feature vectors into quantum state Hilbert space using parameterized rotation gates.",

                "description": "Classical features x₁ and x₂ are mapped to rotation angles via Ry(θ) gates, entangled with a CNOT gate, and measured to produce quantum kernel expectation values.",

                "code": """qc = QuantumCircuit(2, 2)\nimport numpy as np\nqc.ry(0.75 * np.pi, 0)  # Feature 1\nqc.ry(1.25 * np.pi, 1)  # Feature 2\nqc.cx(0, 1)            # Entangling layer\nqc.ry(0.5 * np.pi, 0)\nqc.measure([0, 1], [0, 1])""",

                "builder": _build_guided_qml

            },

            "📡 Quantum Superdense Coding": {

                "qubits": 2,

                "objective": "Transmit two classical bits of information using only one physical qubit through pre-shared quantum entanglement.",

                "description": "Alice and Bob share an entangled Bell pair. Alice encodes 2 classical bits ('11') by applying Z and X gates to her single qubit. Bob performs a Bell measurement to recover both bits.",

                "code": """qc = QuantumCircuit(2, 2)\n# 1. Prepare entangled pair\nqc.h(0)\nqc.cx(0, 1)\n# 2. Alice encodes '11' (Z then X)\nqc.z(0)\nqc.x(0)\n# 3. Bob decodes Bell state\nqc.cx(0, 1)\nqc.h(0)\nqc.measure([0, 1], [0, 1])""",

                "builder": _build_guided_superdense

            },

            "⚛️ Quantum Teleportation Protocol": {

                "qubits": 3,

                "objective": "Teleport an unknown arbitrary single-qubit quantum state from Alice to Bob using quantum entanglement and classical communication.",

                "description": "Q0 is prepared in an arbitrary quantum state |ψ⟩. Q1 and Q2 form an entangled pair shared between Alice and Bob. Alice measures Q0 and Q1 in the Bell basis, and Bob applies conditional X and Z correction gates to Q2.",

                "code": """qc = QuantumCircuit(3, 3)\n# Prepare state |ψ⟩ on Q0\nqc.h(0)\nqc.s(0)\n# Entangled resource between Q1 and Q2\nqc.h(1)\nqc.cx(1, 2)\n# Alice Bell measurement\nqc.cx(0, 1)\nqc.h(0)\nqc.measure([0, 1], [0, 1])\n# Bob correction\nqc.cx(1, 2)\nqc.cz(0, 2)\nqc.measure(2, 2)""",

                "builder": _build_guided_teleportation

            }

        }



        selected_proj = st.selectbox(

            "Select a Guided Project to Execute:",

            list(guided_projects.keys()),

            key="pg_guided_proj_select"

        )



        p_info = guided_projects[selected_proj]



        st.info(f"**🎯 Objective:** {p_info['objective']}")

        st.write(p_info["description"])



        with st.expander("📝 View Circuit Code & Instructions", expanded=False):

            st.code(p_info["code"], language="python")



        col_gp1, col_gp2 = st.columns([1, 1])

        with col_gp1:

            st.metric("Qubits Required", p_info["qubits"])

        with col_gp2:

            guided_shots = st.slider("Shots", min_value=100, max_value=5000, value=1000, step=100, key=f"pg_shots_{selected_proj}")



        if st.button("🚀 Execute Guided Project Live", use_container_width=True, key=f"pg_btn_run_{selected_proj}"):

            qc = p_info["builder"]()

            st.divider()

            run_and_save(f"Guided: {selected_proj.split(' ')[1]}", qc, p_info["qubits"], guided_shots)





# ============================================================

# PROBABILITY DISTRIBUTION

# ============================================================



elif page == "📊 Probability Distribution":

    st.title("📊 Quantum Probability Distribution")



    st.write("""

    A probability distribution tells us how frequently each possible measurement

    result is expected to occur. In a quantum experiment, the circuit determines

    the theoretical probabilities, while repeated measurements (shots) give us

    an experimental estimate of those probabilities.



    For a beginner, the most important distinction is:



    **Quantum state → theoretical probabilities → repeated measurements → counts → observed probabilities.**

    """)



    st.header("🧠 Why do we need a probability distribution?")

    st.write("""

    A single quantum measurement gives only one classical result. For example,

    measuring one qubit might give 0. That single result does not tell us the

    complete behaviour of the circuit. If we repeat the same circuit many times,

    we can count how often each result appears. Those counts form an experimental

    probability distribution.

    """)



    st.latex(r"P(x)\approx\frac{\text{count of outcome }x}{\text{total number of shots}}")



    st.header("🔬 Interactive probability experiment")

    experiment = st.selectbox(

        "Choose an example circuit",

        [

            "H on one qubit",

            "Bell State",

            "H on every qubit"

        ]

    )



    shots = st.slider("Number of shots", 100, 10000, 1000, 100, key="probability_shots")



    if experiment == "H on one qubit":

        st.write("The H gate creates approximately equal probabilities for 0 and 1 when the qubit starts in |0>.")

        qc = QuantumCircuit(1, 1)

        qc.h(0)

        qc.measure(0, 0)

        qubits = 1

    elif experiment == "Bell State":

        st.write("H creates superposition on Q0 and CNOT correlates Q1 with Q0, producing the Bell state. Ideal measurements are 00 and 11.")

        qc = QuantumCircuit(2, 2)

        qc.h(0)

        qc.cx(0, 1)

        qc.measure([0, 1], [0, 1])

        qubits = 2

    else:

        num = st.slider("Number of qubits", 1, 4, 2, key="probability_qubits")

        st.write("Each qubit receives H, so the ideal distribution is spread across all computational-basis states.")

        qc = QuantumCircuit(num, num)

        for q in range(num):

            qc.h(q)

        qc.measure(range(num), range(num))

        qubits = num



    st.subheader("🧩 Circuit used for the experiment")

    circuit_diagram(qc)



    if st.button("🚀 Run Probability Experiment", use_container_width=True):

        run_and_save("Probability Distribution - " + experiment, qc, qubits, shots)



    st.header("📈 How to read the chart")

    st.write("""

    The horizontal labels are possible classical measurement states such as 0,

    1, 00 or 11. The height of each bar represents the percentage of shots that

    produced that state. With more shots, the observed distribution usually gets

    closer to the theoretical distribution, although finite sampling still causes

    small fluctuations.

    """)



    st.header("🧪 Example")

    st.write("""

    Suppose a circuit is run for 1,000 shots and the result is 00 in 492 shots

    and 11 in 508 shots. Then the estimated probabilities are 49.2% and 50.8%.

    The ideal Bell-state probabilities are 50% and 50%, so this is a normal finite-

    sampling variation.

    """)



# ============================================================

# BELL STATE

# ============================================================



elif page == "🔔 Bell State Experiment":

    st.title("🔔 Bell State Experiment")



    st.write("""

    The Bell state experiment is one of the most useful beginner exercises

    because it combines three ideas: superposition, a controlled gate, and

    measurement.

    """)



    st.header("Step 1 — Initialize")

    st.write("Two qubits begin in the state |00>.")



    st.header("Step 2 — Apply H to Qubit 0")

    st.write("""

    H creates a superposition on the first qubit. The two-qubit state becomes

    a combination of |00> and |10>.

    """)

    st.latex(r"\lvert00\rangle\rightarrow\frac{\lvert00\rangle+\lvert10\rangle}{\sqrt{2}}")



    st.header("Step 3 — Apply CNOT")

    st.write("""

    Qubit 0 is the control and Qubit 1 is the target. The CNOT flips the

    target when the control is 1. The resulting state is the Bell state.

    """)

    st.latex(r"\frac{\lvert00\rangle+\lvert10\rangle}{\sqrt{2}}\rightarrow\frac{\lvert00\rangle+\lvert11\rangle}{\sqrt{2}}")



    st.header("Step 4 — Measure")

    st.write("""

    When measured repeatedly, the ideal circuit produces only 00 and 11.

    The exact percentages fluctuate slightly because the simulator samples

    finite numbers of shots.

    """)



    shots = st.slider("Bell-state shots", 100, 5000, 1000, 100)



    if st.button("🔔 Run Bell State Experiment", use_container_width=True):

        qc = QuantumCircuit(2, 2)

        qc.h(0)

        qc.cx(0, 1)

        qc.measure([0, 1], [0, 1])

        run_and_save("Bell State Experiment", qc, 2, shots)



# ============================================================

# QUANTUM RANDOM NUMBER GENERATOR

# ============================================================



elif page == "🎲 Quantum Random Number Generator":

    st.title("🎲 Quantum Random Number Generator")



    st.write("""

    This project demonstrates how quantum measurement can be used to obtain

    random-looking binary values. The important idea is not merely generating

    a random number; it is understanding where the randomness enters the

    quantum process.

    """)



    st.header("🔬 What happens step by step?")

    steps = [

        ("1. Initialize", "Each qubit starts in |0>."),

        ("2. Create superposition", "An H gate changes each qubit into an equal superposition."),

        ("3. Measure", "Measurement samples 0 or 1 according to the state probabilities."),

        ("4. Collect bits", "The individual measurement results form a binary string."),

        ("5. Interpret", "The binary string can be displayed as a random binary number.")

    ]



    for title, text in steps:

        st.subheader(title)

        st.write(text)



    st.latex(r"H\lvert0\rangle=\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}}")



    bits = st.slider(

        "Number of random bits",

        min_value=1,

        max_value=16,

        value=8

    )



    if st.button(

        "🎲 Generate Quantum Random Bits",

        use_container_width=True

    ):

        qc = QuantumCircuit(bits, bits)



        for q in range(bits):

            qc.h(q)



        qc.measure(range(bits), range(bits))



        counts = run_circuit(qc, 1)

        random_bits = next(iter(counts))



        st.subheader("🎯 Generated result")

        st.code(random_bits)



        st.write("""

        Each character represents one measured qubit. For example, an

        eight-bit result such as 10110010 is a classical binary string

        produced from quantum measurement outcomes.

        """)



        st.subheader("🧩 Circuit")

        circuit_diagram(qc)



        try:

            path = save_experiment(

                "Quantum Random Number Generator",

                qc,

                counts,

                bits,

                1

            )

            st.success(f"Experiment saved: {path}")

        except Exception as exc:

            st.warning(f"Saving failed: {exc}")



    beginner_box(

        "Why is the H gate used?",

        "Starting from |0>, the H gate gives equal theoretical probabilities "

        "for 0 and 1 when measured in the computational basis. Repeating this "

        "process creates a sequence of measurement outcomes that can be used "

        "as random binary data in this educational simulator."

    )



# ============================================================

# GUIDED PROJECTS

# ============================================================



elif page == "🧪 Guided Quantum Projects":

    st.title("🧪 Guided Quantum Projects")



    st.write("""

    This section turns the learning material into practical mini-projects.

    Each project explains the objective, prerequisites, workflow, quantum

    part, classical part, expected output, and possible future extension.



    The current projects are intentionally simulator-based. This is useful

    for the present prototype because students can learn and test the

    complete workflow without waiting for access to real quantum hardware.

    """)



    project = st.selectbox(

        "Choose a guided project",

        [

            "🎲 Quantum Random Number Generator",

            "🔔 Bell State Entanglement",

            "🔐 BB84 Quantum Cryptography",

            "🚗 Small Quantum Optimization",

            "🤖 Quantum Machine Learning",

            "🧪 Quantum Chemistry Simulation"

        ]

    )



    if project == "🎲 Quantum Random Number Generator":

        st.header("🎲 Project: Quantum Random Number Generator")



        st.subheader("🎯 Objective")

        st.write("""

        Build a small application that uses qubit superposition and

        measurement to generate a binary sequence.

        """)



        st.subheader("📚 Prerequisites")

        st.write("""

        Learn qubits, the H gate, superposition, measurement and basic

        probability before implementing the project.

        """)



        st.subheader("🔄 Complete workflow")

        st.code("""

User chooses number of bits

        |

        v

Create N qubits

        |

        v

Apply H to every qubit

        |

        v

Measure every qubit

        |

        v

Collect classical bit string

        |

        v

Display random result

        |

        v

Save experiment

""")



        st.subheader("🧠 What is quantum here?")

        st.write("""

        The quantum part is the preparation of the qubits and their

        measurement. The surrounding application, user interface, storage

        and display are classical software.

        """)



        st.subheader("🚀 Future improvements")

        st.write("""

        Add multiple runs, randomness statistics, frequency analysis,

        downloadable experiment reports, and later an optional real-QPU

        execution mode.

        """)



    elif project == "🔔 Bell State Entanglement":

        st.header("🔔 Project: Bell State Entanglement")



        st.subheader("🎯 Objective")

        st.write("""

        Create an entangled two-qubit state and demonstrate its measurement

        correlations.

        """)



        st.subheader("🔄 Implementation steps")

        for i, text in enumerate([

            "Create two qubits initialized to |00>.",

            "Apply H to Qubit 0.",

            "Apply CNOT with Qubit 0 as control and Qubit 1 as target.",

            "Measure both qubits.",

            "Run many shots.",

            "Display the distribution and explain why 00 and 11 dominate."

        ], 1):

            st.write(f"**Step {i}:** {text}")



        st.code("""

qc = QuantumCircuit(2, 2)

qc.h(0)

qc.cx(0, 1)

qc.measure([0, 1], [0, 1])

""", language="python")



        if st.button("🚀 Run Guided Bell Project"):

            qc = QuantumCircuit(2, 2)

            qc.h(0)

            qc.cx(0, 1)

            qc.measure([0, 1], [0, 1])

            run_and_save("Guided Bell State Project", qc, 2, 1000)



    elif project == "🔐 BB84 Quantum Cryptography":

        st.header("🔐 Project: BB84 Quantum Cryptography")



        st.subheader("🎯 Objective")

        st.write("""

        Understand the basic idea of quantum key distribution using two

        measurement bases. The goal is to learn how quantum states can be

        used to establish a shared key and how an eavesdropper can introduce

        detectable errors.

        """)



        st.subheader("🔄 Step-by-step")

        steps = [

            "Alice generates random classical bits.",

            "Alice chooses random encoding bases.",

            "Alice prepares quantum states according to those choices.",

            "Bob chooses random measurement bases.",

            "Bob measures the received states.",

            "Alice and Bob publicly compare bases, not the secret bits.",

            "They keep positions where the bases matched.",

            "A sample can be compared to estimate whether interference occurred."

        ]

        for i, text in enumerate(steps, 1):

            st.write(f"**Step {i}:** {text}")



        st.info("""

        This prototype currently teaches the workflow rather than claiming

        to implement a production-secure cryptographic system.

        """)



    elif project == "🚗 Small Quantum Optimization":

        st.header("🚗 Project: Small Quantum Optimization")



        st.subheader("🎯 Objective")

        st.write("""

        Learn how a classical optimization problem can be transformed into

        a form suitable for a quantum algorithm such as QAOA.

        """)



        st.subheader("🔄 Workflow")

        st.code("""

Real-world problem

      |

      v

Mathematical objective

      |

      v

Binary variables

      |

      v

Cost / Hamiltonian representation

      |

      v

Quantum circuit

      |

      v

Measurement samples

      |

      v

Classical evaluation and optimization

""")



        st.write("""

        A complete QAOA implementation can be added later. For the current

        platform, the important learning goal is understanding the mapping

        between the original problem, the quantum representation and the

        classical optimization loop.

        """)



    elif project == "🤖 Quantum Machine Learning":

        st.header("🤖 Project: Quantum Machine Learning")



        st.subheader("🎯 Objective")

        st.write("""

        Build a hybrid learning pipeline in which classical data is

        preprocessed by ordinary machine-learning methods and selected

        features are encoded into a quantum circuit.

        """)



        st.subheader("🔄 End-to-end workflow")

        st.code("""

Dataset

  |

  v

Cleaning

  |

  v

Feature selection

  |

  v

Scaling

  |

  v

Quantum feature encoding

  |

  v

Parameterized quantum circuit

  |

  v

Measurement

  |

  v

Classical loss / classifier

  |

  v

Prediction

""")



        st.write("""

        The important concept is hybrid computing. Classical processors

        continue to perform data loading, preprocessing and optimization,

        while quantum circuits are used as part of the feature mapping,

        kernel calculation or variational model.

        """)



    elif project == "🧪 Quantum Chemistry Simulation":

        st.header("🧪 Project: Quantum Chemistry Simulation")



        st.subheader("🎯 Objective")

        st.write("""

        Explore how a molecular problem can be converted into a quantum

        problem. Chemistry is one of the major areas where quantum

        computers are studied because molecules themselves obey quantum

        mechanics.

        """)



        st.subheader("🔄 Learning workflow")

        for i, text in enumerate([

            "Choose a small molecule.",

            "Describe its molecular geometry and electronic structure.",

            "Construct a molecular Hamiltonian.",

            "Map the Hamiltonian to qubits.",

            "Use a quantum algorithm such as VQE.",

            "Optimize circuit parameters using a classical optimizer.",

            "Estimate the energy."

        ], 1):

            st.write(f"**Step {i}:** {text}")



        st.info("""

        Chemistry libraries and a complete VQE workflow are suitable future

        extensions once the educational simulator foundation is stable.

        """)







    # ========================================================

    # HANDS-ON SIMULATION ACCESS (ADDED)

    # ========================================================

    st.divider()

    st.header("🧪 Hands-on Practice — Run This Project")

    st.write(

        "The explanation above tells you how the project works. "

        "Use the controls below to actually build and run a small version "

        "of the project on the local Qiskit Aer simulator."

    )

    st.success(

        "🟢 Simulation mode: these experiments run locally with Qiskit Aer. "

        "No IBM Quantum API key or real quantum computer is required."

    )



    guided_shots = int(st.slider(

        "Number of simulation shots",

        min_value=100,

        max_value=5000,

        value=1000,

        step=100,

        key="guided_project_shots"

    ))



    if project == "🎲 Quantum Random Number Generator":

        guided_bits = int(st.slider(

            "Number of qubits / random bits",

            min_value=1,

            max_value=8,

            value=4,

            key="guided_qrng_bits"

        ))

        st.code(

            "QuantumCircuit(n, n) → H on every qubit → Measure every qubit",

            language="text"

        )

        if st.button("▶️ Run QRNG Simulation", use_container_width=True,

                     key="guided_run_qrng"):

            qc = QuantumCircuit(guided_bits, guided_bits)

            for q in range(guided_bits):

                qc.h(q)

            qc.measure(range(guided_bits), range(guided_bits))

            run_and_save(

                "Guided Project - Quantum Random Number Generator",

                qc, guided_bits, guided_shots

            )



    elif project == "🔔 Bell State Entanglement":

        st.code(

            "q0: |0> ── H ──●── M\n"

            "                │\n"

            "q1: |0> ────────X── M",

            language="text"

        )

        if st.button("▶️ Run Bell State Simulation", use_container_width=True,

                     key="guided_run_bell"):

            qc = QuantumCircuit(2, 2)

            qc.h(0)

            qc.cx(0, 1)

            qc.measure([0, 1], [0, 1])

            run_and_save(

                "Guided Project - Bell State Entanglement",

                qc, 2, guided_shots

            )



    elif project == "🔐 BB84 Quantum Cryptography":
        st.write(
            "This is an educational one-qubit BB84 round. You can choose "
            "Alice's bit and encoding basis, then Bob's measurement basis."
        )

        with st.expander("🎯 Gate Selection Guide — Which Gates Should Be Selected?", expanded=True):
            st.markdown(r"""
            **How BB84 converts Alice & Bob choices into Quantum Gates:**
            
            | Protocol Step | Your Selection | Quantum Gate Applied | Resulting State / Action |
            | :--- | :--- | :--- | :--- |
            | **Alice Bit** | `Bit 0` | **No gate** (Qubit stays in $|0\rangle$) | Ground state $|0\rangle$ |
            | **Alice Bit** | `Bit 1` | **`X` Gate** (Pauli-X bit-flip) | Flipped to $|1\rangle$ |
            | **Alice Basis** | `Z basis` (Standard) | **No gate** | Remains in computational basis $\{|0\rangle, |1\rangle\}$ |
            | **Alice Basis** | `X basis` (Diagonal) | **`H` Gate** (Hadamard encoder) | Rotates to diagonal basis $\{|+\rangle, |-\rangle\}$ |
            | **Bob Basis** | `Z basis` (Standard) | **Direct Measurement `M`** | Measures along computational $Z$-axis |
            | **Bob Basis** | `X basis` (Diagonal) | **`H` Gate + `M`** (Basis rotator) | Rotates diagonal states back to $Z$-axis for measurement |
            """)

        c_bb1, c_bb2, c_bb3 = st.columns(3)
        with c_bb1:
            alice_bit = int(st.selectbox("Alice's bit", [0, 1], key="bb84_alice_bit"))
        with c_bb2:
            alice_basis = st.selectbox(
                "Alice's encoding basis", ["Z basis", "X basis"], key="bb84_alice_basis"
            )
        with c_bb3:
            bob_basis = st.selectbox(
                "Bob's measurement basis", ["Z basis", "X basis"], key="bb84_bob_basis"
            )

        # Dynamic live gate summary
        alice_gates = []
        if alice_bit == 1:
            alice_gates.append("`X` (Bit-flip)")
        if alice_basis == "X basis":
            alice_gates.append("`H` (X-basis Encode)")
        alice_gate_desc = " ➔ ".join(alice_gates) if alice_gates else "None (Starts |0⟩)"

        bob_gates = []
        if bob_basis == "X basis":
            bob_gates.append("`H` (X-basis Decode)")
        bob_gates.append("`M` (Measure)")
        bob_gate_desc = " ➔ ".join(bob_gates)

        st.info(f"""
        **🎯 Gates selected for this simulation:**
        - **👩 Alice's Gate(s):** {alice_gate_desc}
        - **👨 Bob's Gate(s):** {bob_gate_desc}
        - **🔒 Basis Matching:** {"🟢 **MATCHED (X = X or Z = Z)** ➔ $H \\cdot H = I$, Bob recovers Alice's bit with 100% certainty!" if alice_basis == bob_basis else "🟡 **MISMATCHED (X ≠ Z)** ➔ Quantum uncertainty yields 50/50 random output (sifted out in BB84)."}
        """)

        if st.button("▶️ Run BB84 Simulation", use_container_width=True,
                     key="guided_run_bb84"):
            qc = QuantumCircuit(1, 1)

            # Alice prepares |0>, |1>, |+>, or |->.
            if alice_bit == 1:
                qc.x(0)
            if alice_basis == "X basis":
                qc.h(0)

            # Bob changes the measurement basis when using X basis.
            if bob_basis == "X basis":
                qc.h(0)
            qc.measure(0, 0)

            counts = run_and_save(
                "Guided Project - BB84",
                qc, 1, guided_shots
            )
            if alice_basis == bob_basis:
                st.success(
                    "The bases matched. In an ideal noiseless simulation, "
                    "Bob should recover Alice's bit with certainty."
                )
            else:
                st.info(
                    "The bases were different. In BB84, this result is normally "
                    "discarded during the basis-sifting step."
                )




    elif project == "🚗 Small Quantum Optimization":

        st.write(

            "Beginner demonstration: prepare four candidate states and use a "

            "simple cost-marking circuit. This illustrates the sampling part "

            "of a quantum optimization workflow; it is not a full QAOA solver."

        )

        preferred_state = st.selectbox(

            "Choose a preferred candidate state",

            ["00", "01", "10", "11"],

            key="optimization_target"

        )



        if st.button("▶️ Run Optimization Simulation", use_container_width=True,

                     key="guided_run_optimization"):

            qc = QuantumCircuit(2, 2)

            qc.h([0, 1])



            # Mark the selected candidate with a phase flip.

            for q, bit in enumerate(reversed(preferred_state)):

                if bit == "0":

                    qc.x(q)

            qc.cz(0, 1)

            for q, bit in enumerate(reversed(preferred_state)):

                if bit == "0":

                    qc.x(q)



            qc.measure([0, 1], [0, 1])

            counts = run_and_save(

                "Guided Project - Small Quantum Optimization",

                qc, 2, guided_shots

            )

            st.info(

                f"The selected candidate was |{preferred_state}⟩. "

                "This small circuit demonstrates state marking and sampling."

            )



    elif project == "🤖 Quantum Machine Learning":

        feature_0 = float(st.slider(

            "Feature 1 angle (radians)", 0.0, 6.28, 1.57, 0.01,

            key="qml_feature_0"

        ))

        feature_1 = float(st.slider(

            "Feature 2 angle (radians)", 0.0, 6.28, 3.14, 0.01,

            key="qml_feature_1"

        ))

        st.write(

            "The two classical features are encoded as rotation angles. "

            "The circuit then entangles the encoded qubits and measures them."

        )



        if st.button("▶️ Run QML Encoding Simulation", use_container_width=True,

                     key="guided_run_qml"):

            qc = QuantumCircuit(2, 2)

            qc.ry(feature_0, 0)

            qc.ry(feature_1, 1)

            qc.cx(0, 1)

            qc.measure([0, 1], [0, 1])

            run_and_save(

                "Guided Project - Quantum Machine Learning",

                qc, 2, guided_shots

            )

            st.info(

                "This is the quantum feature-encoding stage of a hybrid QML "

                "pipeline. It is not a trained classifier yet."

            )



    elif project == "🧪 Quantum Chemistry Simulation":

        st.write(

            "Beginner demonstration of quantum state preparation for a tiny "

            "two-qubit model. A complete molecular Hamiltonian and VQE workflow "

            "can be added later."

        )

        chemistry_state = st.selectbox(

            "Prepare an example state",

            ["|00⟩", "|01⟩", "|10⟩", "|11⟩"],

            key="chemistry_state"

        )



        if st.button("▶️ Run Chemistry Simulation", use_container_width=True,

                     key="guided_run_chemistry"):

            qc = QuantumCircuit(2, 2)

            if chemistry_state in ("|01⟩", "|11⟩"):

                qc.x(0)

            if chemistry_state in ("|10⟩", "|11⟩"):

                qc.x(1)

            qc.measure([0, 1], [0, 1])

            run_and_save(

                "Guided Project - Quantum Chemistry",

                qc, 2, guided_shots

            )

            st.info(

                "The result shows the measured state prepared by the circuit. "

                "A real chemistry calculation would additionally construct a "

                "molecular Hamiltonian and optimize its energy."

            )



# ============================================================

# QUANTUM AI / ML

# ============================================================



elif page == "🤖 Quantum AI / ML":

    st.title("🤖 Quantum AI / Machine Learning")



    st.write("""

    Quantum Machine Learning (QML) combines classical machine learning with

    quantum circuits. For a beginner, the most important idea is that QML

    does not mean replacing every neural network with a quantum computer.

    Instead, quantum circuits can become one component of a hybrid pipeline.

    """)



    st.header("🔄 Typical hybrid pipeline")

    st.code("""

Classical dataset

       |

       v

Data cleaning

       |

       v

Feature scaling

       |

       v

Quantum feature map

       |

       v

Quantum circuit

       |

       v

Measurement / kernel values

       |

       v

Classical optimizer or classifier

       |

       v

Prediction

""")



    st.header("📚 Major QML concepts")

    concepts = pd.DataFrame({

        "Concept": [

            "Quantum Feature Map",

            "Quantum Kernel",

            "Variational Quantum Circuit",

            "Variational Classifier",

            "Quantum Support Vector Machine",

            "Hybrid Optimization"

        ],

        "Beginner explanation": [

            "Encodes classical numerical features into a quantum state.",

            "Uses similarities between quantum-encoded data points.",

            "A parameterized circuit whose values can be optimized.",

            "Uses a trainable quantum circuit as part of classification.",

            "Combines quantum kernels with an SVM-style classical method.",

            "Classical optimization updates parameters of a quantum circuit."

        ]

    })

    st.dataframe(concepts, use_container_width=True, hide_index=True)



    st.warning("""

    Current version: educational explanation only. A full QML training

    pipeline can be added as a separate project after the simulator and

    classical data-processing layers are stable.

    """)



# ============================================================

# EXPERIMENT HISTORY

# ============================================================



elif page == "📊 Experiment History":

    st.title("📊 Experiment History")



    st.write("""

    Every experiment executed through the main experiment modules can be

    stored locally as a JSON record and appended to a CSV history file.

    This creates a simple experiment-tracking layer for students.

    """)



    records = st.session_state.experiment_history



    csv_path = os.path.join(

        get_storage_path(), "experiment_history.csv"

    )



    if os.path.exists(csv_path):

        try:

            saved = pd.read_csv(csv_path)

            st.dataframe(saved, use_container_width=True, hide_index=True)

        except Exception as exc:

            st.warning(f"Could not read saved history: {exc}")

    elif records:

        st.dataframe(

            pd.DataFrame(records),

            use_container_width=True,

            hide_index=True

        )

    else:

        st.info("No experiments have been saved yet.")



    st.header("📁 What is recorded?")

    st.write("""

    The history can contain the experiment name, date and time, number of

    qubits, number of shots and measurement counts. The JSON record also

    stores a text representation of the circuit.

    """)



# ============================================================

# CLOUD STORAGE

# ============================================================



elif page == "☁️ Experiment and Cloud Storage":

    st.title("☁️ Experiment and Cloud Storage")



    st.write("""

    This module provides the storage layer for the learning platform.

    At the moment, the application saves experiment records locally on the

    computer. The storage design is intentionally separated from the

    learning modules so that a mounted cloud directory can be used later.

    """)



    st.header("📦 Current storage architecture")

    st.code("""

Quantum Learning Platform

          |

          v

Experiment / Project

          |

          v

Storage Manager

       /     \\

      /       \\

 JSON files   CSV history

      \\       /

       \\     /

        Storage Folder

""")



    st.header("💾 Current local storage")

    current_path = get_storage_path()

    st.code(current_path)



    st.write("""

    JSON is useful because each experiment can be stored as a structured

    record. CSV is useful for quickly opening the experiment history in

    spreadsheet software and performing simple analysis.

    """)



    st.header("☁️ Planned 64 GB cloud storage")

    st.write("""

    When the planned 64 GB cloud storage is provided, it can be mounted or

    connected to the application. The storage location can then be changed

    without redesigning the quantum learning modules.



    Suitable content includes:



    • Experiment JSON records

    • Experiment CSV history

    • Quantum datasets

    • Guided project files

    • Learning resources

    • Model files for future QML experiments

    • Generated reports

    • Circuit examples

    • Student project artifacts

    """)



    st.header("🗂️ Recommended folder structure")

    st.code("""

quantum_cloud_storage/

|

+-- experiments/

|   +-- json/

|   +-- csv/



+-- datasets/

|

+-- guided_projects/

|

+-- qml_models/

|

+-- learning_resources/

|

+-- reports/

|

+-- circuit_examples/

|

+-- student_projects/

""")



    st.header("🔧 Change storage location")

    new_path = st.text_input(

        "Storage path",

        value=current_path,

        help="For now use a folder available to this computer."

    )



    if st.button("💾 Set Storage Location", use_container_width=True):

        try:

            os.makedirs(new_path, exist_ok=True)

            st.session_state.storage_path = new_path

            st.success(

                f"Storage location updated to: {new_path}"

            )

        except Exception as exc:

            st.error(f"Could not create storage location: {exc}")



    st.info("""

    **Future cloud integration:** the application can later point this

    storage layer to the mounted 64 GB cloud location. Real IBM Quantum

    hardware access can also be added separately; cloud storage and quantum

    hardware are two different components.

    """)



# ============================================================

# BEGINNER QUIZ

# ============================================================



elif page == "❓ Beginner Quiz":

    st.title("❓ Beginner Quantum Computing Quiz")



    st.write("""

    Use this quiz after completing the introductory modules. It checks

    whether you understand the basic concepts rather than testing advanced

    mathematics.

    """)



    questions = [

        (

            "1. What is the basic unit of quantum information?",

            ["Byte", "Bit", "Qubit", "Pixel"],

            "Qubit"

        ),

        (

            "2. Which gate is commonly used to create equal superposition from |0>?",

            ["X", "H", "Z", "T"],

            "H"

        ),

        (

            "3. What does the X gate do to |0>?",

            ["Keeps it |0>", "Changes it to |1>", "Measures it", "Deletes it"],

            "Changes it to |1>"

        ),

        (

            "4. Which operation is a two-qubit controlled operation?",

            ["H", "X", "CNOT", "T"],

            "CNOT"

        ),

        (

            "5. What does measurement produce?",

            [

                "A classical result",

                "A new CPU",

                "A larger qubit",

                "A programming language"

            ],

            "A classical result"

        ),

        (

            "6. Which simulator is used in this prototype?",

            ["Aer", "Excel", "Photoshop", "PowerPoint"],

            "Aer"

        )

    ]



    score = 0

    answers = []



    for question, options, correct in questions:

        answer = st.radio(question, options, key=question)

        answers.append((answer, correct))

        if answer == correct:

            score += 1



    if st.button("📊 Submit Quiz", use_container_width=True):

        st.header(f"Your Score: {score}/{len(questions)}")



        if score == len(questions):

            st.success("🏆 Excellent! You understand the beginner concepts.")

        elif score >= len(questions) // 2:

            st.info("👍 Good progress. Review the modules and try again.")

        else:

            st.warning(

                "📚 Review Introduction, Qubit, Superposition, Gates and Measurement."

            )



        st.subheader("📖 Review")

        for i, (answer, correct) in enumerate(answers, 1):

            if answer == correct:

                st.write(f"Question {i}: ✅ Correct")

            else:

                st.write(

                    f"Question {i}: ❌ Correct answer: {correct}"

                )



# ============================================================
# 🗺️ LEARNING PATH MODULE
# ============================================================

elif page == "🗺️ Learning Path":
    st.markdown("""<div class="quantum-card">
        <div class="quantum-card-title">🗺️ Interactive Quantum Learning Roadmap</div>
        <p style="color: #475569; font-size: 0.95rem; line-height: 1.6;">
            Follow this structured, university-grade curriculum to progress from quantum mechanics fundamentals to advanced algorithms, interactive simulation, and Quantum Machine Learning.
        </p>
    </div>""", unsafe_allow_html=True)

    milestones = [
        ("1", "🌱 Introduction to Quantum Computing", "Why quantum computing matters, hybrid classical-quantum models, and linear algebra foundations.", "Completed", "#059669", "badge-green"),
        ("2", "💻 Classical vs Quantum Computing", "Bits vs qubits, deterministic logic vs quantum statevectors, computational complexity.", "Completed", "#059669", "badge-green"),
        ("3", "🔵 Qubits & Quantum States", "State representation |ψ⟩ = α|0⟩ + β|1⟩, normalization condition |α|² + |β|² = 1, Bloch sphere.", "Completed", "#059669", "badge-green"),
        ("4", "🌊 Quantum Superposition", "Hadamard gate, creating equal superpositions, phase relationships, probabilistic collapse.", "In Progress", "#7c3aed", "badge-purple"),
        ("5", "⚙️ Quantum Gates", "Single qubit unitaries (X, Y, Z, S, T) and multi-qubit entangling gates (CNOT, CZ, SWAP).", "Ready", "#0284c7", "badge-cyan"),
        ("6", "📏 Quantum Measurement", "Wavefunction collapse, Born's rule, extracting classical information, basis measurement.", "Ready", "#0284c7", "badge-cyan"),
        ("10", "🧪 Guided Quantum Projects", "Hands-on projects: QRNG, Bell inequality, Quantum Teleportation protocol.", "Interactive", "#d97706", "badge-amber"),
        ("11", "🤖 Quantum AI / Machine Learning", "Variational Quantum Classifiers (VQC), quantum feature maps, parameterized circuits.", "Advanced", "#7c3aed", "badge-purple")
    ]

    for num, title, desc, status, color, badge_cls in milestones:
        st.markdown(f"""<div class="quantum-card" style="display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; margin-bottom: 14px;">
            <div style="display: flex; align-items: flex-start; gap: 16px;">
                <div style="width: 36px; height: 36px; border-radius: 10px; background: #f5f3ff; border: 1px solid #ddd6fe; color: #7c3aed; font-weight: 800; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    {num}
                </div>
                <div>
                    <div style="font-weight: 700; font-size: 1.05rem; color: #0f172a; margin-bottom: 4px;">{title}</div>
                    <div style="font-size: 0.88rem; color: #64748b; line-height: 1.5;">{desc}</div>
                </div>
            </div>
            <div>
                <span class="badge-pill {badge_cls}">{status}</span>
            </div>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 🧪 QUANTUM PLAYGROUND & STEP-BY-STEP LAB
# ============================================================

elif page == "🧪 Quantum Playground":
    st.markdown("""<div class="quantum-card">
        <div class="quantum-card-title">🧪 Quantum Playground & Step-by-Step Lab</div>
        <p style="color: #475569; font-size: 0.95rem; line-height: 1.6;">
            Construct custom quantum circuits with single-qubit and multi-qubit gates, inspect state evolutions step-by-step, and execute live on the local Qiskit Aer simulator.
        </p>
    </div>""", unsafe_allow_html=True)

    if "playground_gates" not in st.session_state:
        st.session_state.playground_gates = []

    c_conf1, c_conf2 = st.columns([1, 1])
    with c_conf1:
        num_qubits = st.slider("Number of Qubits", 1, 4, 2, key="pg_num_qubits")
    with c_conf2:
        shots = st.slider("Number of Shots", 100, 5000, 1000, 100, key="pg_shots")

    st.markdown("### ➕ Add Gate Layer")
    g_col1, g_col2, g_col3, g_col4 = st.columns([1.2, 1.2, 1.2, 1.2])

    with g_col1:
        gate_type = st.selectbox("Gate Type", ["H (Hadamard)", "X (NOT)", "Y (Pauli-Y)", "Z (Phase Flip)", "S (Phase √Z)", "T (π/8 Phase)", "CNOT (Controlled-NOT)", "CZ (Controlled-Z)", "SWAP", "RX", "RY", "RZ"])

    with g_col2:
        target_q = st.selectbox("Target Qubit", [f"q{i}" for i in range(num_qubits)])

    with g_col3:
        if gate_type in ["CNOT (Controlled-NOT)", "CZ (Controlled-Z)", "SWAP"] and num_qubits > 1:
            ctrl_q = st.selectbox("Control / Second Qubit", [f"q{i}" for i in range(num_qubits) if f"q{i}" != target_q])
        else:
            ctrl_q = None
            st.write("*(Single qubit gate)*")

    with g_col4:
        st.write("")
        st.write("")
        if st.button("➕ Add Gate to Circuit", use_container_width=True):
            st.session_state.playground_gates.append({
                "gate": gate_type.split()[0],
                "target": int(target_q.replace("q", "")),
                "control": int(ctrl_q.replace("q", "")) if ctrl_q else None
            })
            st.rerun()

    c_act1, c_act2 = st.columns([1, 1])
    with c_act1:
        if st.button("🗑️ Clear All Gates", use_container_width=True):
            st.session_state.playground_gates = []
            st.rerun()
    with c_act2:
        if st.button("↩️ Remove Last Gate", use_container_width=True) and st.session_state.playground_gates:
            st.session_state.playground_gates.pop()
            st.rerun()

    # Build Circuit
    qc = QuantumCircuit(num_qubits, num_qubits)
    for op in st.session_state.playground_gates:
        g = op["gate"]
        t = op["target"]
        c = op["control"]
        if g == "H": qc.h(t)
        elif g == "X": qc.x(t)
        elif g == "Y": qc.y(t)
        elif g == "Z": qc.z(t)
        elif g == "S": qc.s(t)
        elif g == "T": qc.t(t)
        elif g == "CNOT" and c is not None: qc.cx(c, t)
        elif g == "CZ" and c is not None: qc.cz(c, t)
        elif g == "SWAP" and c is not None: qc.swap(c, t)
        elif g == "RX": qc.rx(1.5708, t)
        elif g == "RY": qc.ry(1.5708, t)
        elif g == "RZ": qc.rz(1.5708, t)

    qc.measure(range(num_qubits), range(num_qubits))

    st.markdown("### ⚛️ Current Circuit Diagram")
    circuit_diagram(qc)

    st.markdown(f"**Circuit Summary:** {num_qubits} Qubits • {len(st.session_state.playground_gates)} Gates Applied • {shots} Shots")

    c_run1, c_run2 = st.columns([1.2, 1.2])
    with c_run1:
        if st.button("🚀 Run Live Simulation", use_container_width=True):
            counts = run_and_save("Playground Experiment", qc, num_qubits, shots)

    with c_run2:
        with st.expander("▶ Step-by-Step State Evolution", expanded=True):
            st.write("1. **Initial State:** |0...0⟩ (all qubits initialized to ground state)")
            for step_i, op in enumerate(st.session_state.playground_gates, 1):
                g = op["gate"]
                t = op["target"]
                c = op["control"]
                if c is not None:
                    st.write(f"{step_i + 1}. **Apply {g}:** Controlled between q{c} and q{t} (creates or transforms entanglement)")
                else:
                    st.write(f"{step_i + 1}. **Apply {g}:** On qubit q{t} (transforms state vector amplitudes/phase)")
            st.write(f"{len(st.session_state.playground_gates) + 2}. **Measurement:** State collapses into classical bitstring according to Born rule probabilities.")


# ============================================================
# 📖 QUANTUM GLOSSARY MODULE
# ============================================================

elif page == "📖 Quantum Glossary":
    st.markdown("""<div class="quantum-card">
        <div class="quantum-card-title">📖 Comprehensive Quantum Computing Glossary</div>
        <p style="color: #475569; font-size: 0.95rem; line-height: 1.6;">
            A beginner-to-advanced reference index of essential quantum computing concepts, mathematical terms, and hardware architecture.
        </p>
    </div>""", unsafe_allow_html=True)

    glossary_items = [
        ("Qubit (Quantum Bit)", "The fundamental unit of quantum information. Unlike a classical bit (0 or 1), a qubit exists in a normalized linear combination (superposition) of basis states |0⟩ and |1⟩.", "Fundamentals"),
        ("Classical Bit", "The basic unit of classical computing representing a definite physical state: 0 (voltage low) or 1 (voltage high).", "Fundamentals"),
        ("Quantum Superposition", "The principle allowing a quantum system to be in a linear combination of multiple states simultaneously until measured.", "Core Mechanics"),
        ("Quantum Entanglement", "A quantum phenomenon where two or more qubits become correlated such that the quantum state of one cannot be described independently of the others.", "Core Mechanics"),
        ("Quantum Gate", "A reversible unitary mathematical transformation applied to qubits, represented as complex unitary matrices ($U^\\dagger U = I$).", "Circuits"),
        ("Quantum Measurement", "The process of observing a quantum state, causing the statevector to collapse probabilistically into a definite classical computational basis state.", "Measurement"),
        ("Probability Amplitude", "A complex number whose squared magnitude gives the probability of obtaining a specific measurement outcome ($P = |\\alpha|^2$).", "Mathematics"),
        ("Statevector", "A complex vector containing the full quantum state information of an $n$-qubit system across all $2^n$ basis dimensions.", "Mathematics"),
        ("Bloch Sphere", "A geometric representation of a single qubit state as a point on the surface of a unit sphere in three-dimensional space.", "Visualization"),
        ("Quantum Circuit", "A model for quantum computation where quantum operations and gates are sequenced along qubit wires over time.", "Circuits"),
        ("Qiskit", "An open-source software development framework created by IBM for working with quantum computers at the level of pulses, circuits, and application modules.", "Software"),
        ("Qiskit Aer", "A high-performance simulator framework for Qiskit that runs quantum circuits locally on classical CPUs/GPUs with realistic noise models.", "Software"),
        ("Quantum Teleportation", "A protocol to transmit an unknown quantum state using a shared entangled Bell pair and 2 classical bits without transferring physical matter.", "Protocols"),
        ("Superdense Coding", "A communication protocol that allows sending 2 classical bits by transmitting only 1 physical qubit using prior entanglement.", "Protocols"),
        ("Quantum Interference", "The phenomenon where probability amplitudes can add constructively (increasing likelihood) or destructively (canceling out wrong answers).", "Core Mechanics"),
        ("Decoherence", "The loss of quantum coherence caused by unwanted interactions between a quantum computer and its surrounding environment.", "Hardware"),
        ("Quantum Advantage / Supremacy", "The milestone demonstration where a programmable quantum device solves a well-defined computational problem faster than any classical supercomputer.", "Industry"),
        ("Quantum Error Correction (QEC)", "Methods used to protect quantum information from errors caused by decoherence and quantum noise by encoding logical qubits across physical qubits.", "Advanced")
    ]

    search_term = st.text_input("🔍 Search Glossary Terms:", "")

    for term, definition, tag in glossary_items:
        if not search_term or search_term.lower() in term.lower() or search_term.lower() in definition.lower():
            st.markdown(f"""<div class="quantum-card" style="margin-bottom: 12px; padding: 18px 22px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                    <div style="font-weight: 700; font-size: 1.05rem; color: #7c3aed;">{term}</div>
                    <span class="badge-pill badge-purple">{tag}</span>
                </div>
                <div style="font-size: 0.9rem; color: #334155; line-height: 1.55;">{definition}</div>
            </div>""", unsafe_allow_html=True)


# ============================================================



show_circuit_explanation(page)



# ============================================================

# FOOTER

# ============================================================



st.sidebar.divider()

st.sidebar.success("""

⚛️ Quantum Learning Platform



Local Simulator Mode



Qiskit + Qiskit Aer



Real quantum hardware can be added later.

""")

st.sidebar.caption(

    "Beginner-friendly educational prototype"

)
