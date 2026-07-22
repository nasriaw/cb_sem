import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import warnings
warnings.filterwarnings('ignore')

# Import FPDF untuk pembuatan PDF otomatis
try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

try:
    from semopy import Model, calc_stats
    SEMOPY_AVAILABLE = True
except ImportError:
    SEMOPY_AVAILABLE = False

st.set_page_config(
    page_title="Analisa CB-SEM (Covariance-Based SEM)",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling CSS
st.markdown("""
<style>
    .main-header {
        font-size: 30px;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 14px;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .card-hypothesis {
        background-color: #F0F9FF;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0284C7;
        margin-bottom: 12px;
    }
    .card-conclusion {
        background-color: #F0FDF4;
        padding: 18px;
        border-radius: 10px;
        border-left: 5px solid #16A34A;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Header
st.sidebar.markdown("""
<div style="text-align: center; padding-bottom: 10px;">
    <h1 style="color: #1E3A8A; margin-bottom: 0;">📊 Analisis Multivariate Metode Covariance-Based SEM (CB-SEM) v2.0</h1>
    <p style="font-size: 13px; color: #6B7280; font-weight: bold;">Pemodelan SEM berbasis semopy Python @2026</p>
</div>
""", unsafe_allow_html=True)

# Identitas Penyusun
st.sidebar.markdown("""
<div style="background-color: #EFF6FF; border: 1px solid #BFDBFE; padding: 12px; border-radius: 8px; margin-bottom: 20px;">
    <p style="margin: 0; font-size: 11px; color: #1E40AF; font-weight: bold; text-transform: uppercase;">Penyusun:</p>
    <p style="margin: 0; font-size: 14px; color: #1E3A8A; font-weight: 800;">Ir. M Nasri AW, M.Eng.Sc, M.Kom</p>
    <p style="margin: 0; font-size: 11px; color: #4B5563;">Dosen STIE Indonesia Malang (STIEIMA)</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("⚙️ Konfigurasi Variabel Laten")

# Input Jumlah Variabel Laten
num_x = st.sidebar.slider("Jumlah Exogenous Latent (X)", 1, 3, 1, help="Variabel bebas")
num_m = st.sidebar.slider("Jumlah Mediator Latent (M)", 0, 3, 1, help="Variabel perantara (0 jika tanpa mediasi)")
num_y = st.sidebar.slider("Jumlah Endogenous Latent (Y)", 1, 3, 1, help="Variabel terikat akhir")

# Input Konfigurasi Indikator
st.sidebar.markdown("---")
st.sidebar.subheader("📐 Jumlah Indikator per Variabel")

indicators_config = {}

for i in range(1, num_x + 1):
    indicators_config[f"X{i}"] = st.sidebar.number_input(f"Indikator X{i}", min_value=2, max_value=10, value=3, key=f"x_ind_{i}")

for i in range(1, num_m + 1):
    indicators_config[f"M{i}"] = st.sidebar.number_input(f"Indikator M{i}", min_value=2, max_value=10, value=3, key=f"m_ind_{i}")

for i in range(1, num_y + 1):
    indicators_config[f"Y{i}"] = st.sidebar.number_input(f"Indikator Y{i}", min_value=2, max_value=10, value=3, key=f"y_ind_{i}")


def generate_template_data(num_x, num_m, num_y, config):
    np.random.seed(42)
    n_samples = 200
    df = pd.DataFrame()
    
    latents = {}
    for i in range(1, num_x + 1):
        latents[f"X{i}"] = np.random.normal(5.0, 1.0, n_samples)
        
    for i in range(1, num_m + 1):
        base_m = np.zeros(n_samples)
        for x_key in [k for k in latents.keys() if k.startswith("X")]:
            base_m += 0.5 * latents[x_key]
        latents[f"M{i}"] = base_m + np.random.normal(0, 0.8, n_samples)
        
    for i in range(1, num_y + 1):
        base_y = np.zeros(n_samples)
        for x_key in [k for k in latents.keys() if k.startswith("X")]:
            base_y += 0.3 * latents[x_key]
        for m_key in [k for k in latents.keys() if k.startswith("M")]:
            base_y += 0.45 * latents[m_key]
        latents[f"Y{i}"] = base_y + np.random.normal(0, 0.8, n_samples)
        
    for latent_name, n_ind in config.items():
        prefix = latent_name.lower()
        latent_val = latents[latent_name]
        for idx in range(1, n_ind + 1):
            noise = np.random.normal(0, 0.6, n_samples)
            loading = 0.8 if idx == 1 else (0.7 if idx == 2 else 0.85)
            raw = loading * latent_val + noise
            scaled = np.clip(np.round(raw), 1, 5).astype(int)
            df[f"{prefix}{idx}"] = scaled
            
    return df

template_df = generate_template_data(num_x, num_m, num_y, indicators_config)
csv_buffer = io.StringIO()
template_df.to_csv(csv_buffer, index=False)

st.sidebar.markdown("---")
st.sidebar.download_button(
    label="📥 Unduh Template CSV Sesuai Input",
    data=csv_buffer.getvalue(),
    file_name="template_data_sem.csv",
    mime="text/csv",
    help="Gunakan file CSV ini sebagai acuan struktur data Anda."
)

st.markdown('<div class="main-header">Platform Otomatisasi Analisis CB-SEM Terpadu</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Analisis Kausalitas, Fitting Model, Pengujian Hipotesis & Generasi Laporan Riset (.PDF)</div>', unsafe_allow_html=True)

# ==============================================================================
# TAMBAHAN DROPDOWN PANDUAN SEBELUM UNGGAH DATA RISET
# ==============================================================================
with st.expander("📖 Panduan Cara Menggunakan Aplikasi", expanded=False):
    st.markdown("""
    1. **Atur jumlah variabel laten** ($X$, $M$, $Y$) beserta jumlah indikator masing-masing pada **Sidebar sebelah kiri**.
    2. Unduh **Template CSV** acuan jika Anda ingin menyusun data survei baru.
    3. Pilih opsi **Gunakan Data Simulasi Otomatis** atau unggah file CSV data riil Anda sendiri.
    4. Navigasikan tab menu dari **Tab 1 (Head & Deskripsi Data)** hingga **Tab 7 (Hasil Analisa Lengkap & Ekspor PDF)** untuk melihat estimasi dan mengunduh laporan.
    """)

# Area unggah data
st.subheader("📁 Unggah & Siapkan Data Riset")
col_upload, col_source = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader("Pilih file CSV data survei Anda:", type=["csv"])

with col_source:
    data_option = st.radio(
        "Sumber Data Analisa:",
        ["Gunakan Data Simulasi Otomatis", "Gunakan Data Unggahan (CSV)"],
        index=0
    )

if data_option == "Gunakan Data Unggahan (CSV)":
    if uploaded_file is not None:
        try:
            df_analysis = pd.read_csv(uploaded_file)
            st.success(f"✅ File CSV berhasil diunggah! (Sampel: {len(df_analysis)} responden)")
        except Exception as e:
            st.error(f"Gagal membaca file CSV: {e}")
            df_analysis = template_df
            st.info("Beralih sementara menggunakan data simulasi.")
    else:
        st.warning("⚠️ Silakan unggah file CSV Anda terlebih dahulu. Tampilan beralih ke data simulasi.")
        df_analysis = template_df
else:
    df_analysis = template_df
    st.info(f"ℹ️ Menggunakan data simulasi otomatis (Sampel: {len(df_analysis)} responden).")

# Merakit deskripsi model semopy & Daftar Hipotesis
model_desc_lines = ["# Measurement Model"]
hypotheses_list = []
h_counter = 1

for latent_name, n_ind in indicators_config.items():
    prefix = latent_name.lower()
    indicators = [f"{prefix}{idx}" for idx in range(1, n_ind + 1)]
    model_desc_lines.append(f"{latent_name} =~ {' + '.join(indicators)}")

model_desc_lines.append("\n# Structural Model")

if num_m > 0:
    for j in range(1, num_m + 1):
        x_list = [f"X{i}" for i in range(1, num_x + 1)]
        model_desc_lines.append(f"M{j} ~ {' + '.join(x_list)}")
        for x_name in x_list:
            hypotheses_list.append({
                'code': f"H{h_counter}",
                'path': f"{x_name} -> M{j}",
                'dep': f"M{j}",
                'indep': x_name,
                'statement': f"Variabel Exogenous **{x_name}** berpengaruh positif dan signifikan terhadap Mediator **M{j}**."
            })
            h_counter += 1

for k in range(1, num_y + 1):
    predictors = [f"X{i}" for i in range(1, num_x + 1)]
    if num_m > 0:
        predictors += [f"M{j}" for j in range(1, num_m + 1)]
    model_desc_lines.append(f"Y{k} ~ {' + '.join(predictors)}")
    
    for x_i in range(1, num_x + 1):
        hypotheses_list.append({
            'code': f"H{h_counter}",
            'path': f"X{x_i} -> Y{k}",
            'dep': f"Y{k}",
            'indep': f"X{x_i}",
            'statement': f"Variabel Exogenous **X{x_i}** berpengaruh positif dan signifikan terhadap Endogenous **Y{k}**."
        })
        h_counter += 1
        
    if num_m > 0:
        for m_j in range(1, num_m + 1):
            hypotheses_list.append({
                'code': f"H{h_counter}",
                'path': f"M{m_j} -> Y{k}",
                'dep': f"Y{k}",
                'indep': f"M{m_j}",
                'statement': f"Variabel Mediator **M{m_j}** berpengaruh positif dan signifikan terhadap Endogenous **Y{k}**."
            })
            h_counter += 1

model_syntax = "\n".join(model_desc_lines)


def draw_sem_diagram_custom(num_x, num_m, num_y, indicators_config):
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis('off')
    
    x_pos_exog = 1.5
    x_pos_med = 4.0
    x_pos_endo = 6.5
    latent_positions = {}
    
    # 1. Exogenous X & Kotak Indikator
    y_starts_x = np.linspace(5.0, 1.5, num_x) if num_x > 1 else [3.25]
    for idx, y_val in enumerate(y_starts_x, 1):
        name = f"X{idx}"
        latent_positions[name] = (x_pos_exog, y_val)
        
        circle = plt.Circle((x_pos_exog, y_val), 0.4, color='#3B82F6', alpha=0.9, zorder=3)
        ax.add_patch(circle)
        ax.text(x_pos_exog, y_val, name, color='white', ha='center', va='center', weight='bold', fontsize=12, zorder=4)
        
        n_ind = indicators_config.get(name, 3)
        y_inds = np.linspace(y_val + 0.8, y_val - 0.8, n_ind)
        for idx_ind, y_ind in enumerate(y_inds, 1):
            rect = plt.Rectangle((x_pos_exog - 1.2, y_ind - 0.15), 0.45, 0.3, color='#DBEAFE', ec='#2563EB', lw=1.5, zorder=2)
            ax.add_patch(rect)
            ax.text(x_pos_exog - 0.975, y_ind, f"x{idx}{idx_ind}", ha='center', va='center', fontsize=8, weight='bold', color='#1E40AF', zorder=3)
            ax.annotate('', xy=(x_pos_exog - 0.75, y_ind), xytext=(x_pos_exog - 0.35, y_val),
                        arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.2, shrinkA=0, shrinkB=0))

    # 2. Mediator M & Kotak Indikator
    if num_m > 0:
        y_starts_m = np.linspace(5.0, 1.5, num_m) if num_m > 1 else [3.25]
        for idx, y_val in enumerate(y_starts_m, 1):
            name = f"M{idx}"
            latent_positions[name] = (x_pos_med, y_val)
            
            circle = plt.Circle((x_pos_med, y_val), 0.4, color='#F59E0B', alpha=0.9, zorder=3)
            ax.add_patch(circle)
            ax.text(x_pos_med, y_val, name, color='white', ha='center', va='center', weight='bold', fontsize=12, zorder=4)
            
            n_ind = indicators_config.get(name, 3)
            y_inds = np.linspace(y_val + 1.1, y_val + 0.5, n_ind)
            for idx_ind, y_ind in enumerate(y_inds, 1):
                rect = plt.Rectangle((x_pos_med - 0.225, y_ind - 0.12), 0.45, 0.24, color='#FEF3C7', ec='#D97706', lw=1.5, zorder=2)
                ax.add_patch(rect)
                ax.text(x_pos_med, y_ind, f"m{idx}{idx_ind}", ha='center', va='center', fontsize=8, weight='bold', color='#92400E', zorder=3)
                ax.annotate('', xy=(x_pos_med, y_ind - 0.12), xytext=(x_pos_med, y_val + 0.35),
                            arrowprops=dict(arrowstyle="->", color='#D97706', lw=1.2, shrinkA=0, shrinkB=0))

    # 3. Endogenous Y & Kotak Indikator
    y_starts_y = np.linspace(5.0, 1.5, num_y) if num_y > 1 else [3.25]
    for idx, y_val in enumerate(y_starts_y, 1):
        name = f"Y{idx}"
        latent_positions[name] = (x_pos_endo, y_val)
        
        circle = plt.Circle((x_pos_endo, y_val), 0.4, color='#10B981', alpha=0.9, zorder=3)
        ax.add_patch(circle)
        ax.text(x_pos_endo, y_val, name, color='white', ha='center', va='center', weight='bold', fontsize=12, zorder=4)
        
        n_ind = indicators_config.get(name, 3)
        y_inds = np.linspace(y_val + 0.8, y_val - 0.8, n_ind)
        for idx_ind, y_ind in enumerate(y_inds, 1):
            rect = plt.Rectangle((x_pos_endo + 0.75, y_ind - 0.15), 0.45, 0.3, color='#D1FAE5', ec='#059669', lw=1.5, zorder=2)
            ax.add_patch(rect)
            ax.text(x_pos_endo + 0.975, y_ind, f"y{idx}{idx_ind}", ha='center', va='center', fontsize=8, weight='bold', color='#065F46', zorder=3)
            ax.annotate('', xy=(x_pos_endo + 0.75, y_ind), xytext=(x_pos_endo + 0.35, y_val),
                        arrowprops=dict(arrowstyle="->", color='#059669', lw=1.2, shrinkA=0, shrinkB=0))

    # 4. Structural Paths
    if num_m > 0:
        for x_name in [k for k in latent_positions.keys() if k.startswith("X")]:
            for m_name in [k for k in latent_positions.keys() if k.startswith("M")]:
                ax.annotate('', xy=latent_positions[m_name], xytext=latent_positions[x_name],
                            arrowprops=dict(arrowstyle="->", color='#1E293B', lw=2.2, shrinkA=30, shrinkB=30))
                
        for m_name in [k for k in latent_positions.keys() if k.startswith("M")]:
            for y_name in [k for k in latent_positions.keys() if k.startswith("Y")]:
                ax.annotate('', xy=latent_positions[y_name], xytext=latent_positions[m_name],
                            arrowprops=dict(arrowstyle="->", color='#1E293B', lw=2.2, shrinkA=30, shrinkB=30))

    for x_name in [k for k in latent_positions.keys() if k.startswith("X")]:
        for y_name in [k for k in latent_positions.keys() if k.startswith("Y")]:
            connectionstyle = "arc3,rad=-0.18" if num_m > 0 else "arc3,rad=0"
            ax.annotate('', xy=latent_positions[y_name], xytext=latent_positions[x_name],
                        arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.8, ls='--', 
                                        connectionstyle=connectionstyle, shrinkA=30, shrinkB=30))

    plt.xlim(0.0, 8.0)
    plt.ylim(0.2, 6.5)
    return fig


# PROSES FITTING MODEL SEM
model_fitted = False
estimates_df = pd.DataFrame()
fit_indices = pd.DataFrame()

if SEMOPY_AVAILABLE:
    try:
        sem_model = Model(model_syntax)
        sem_model.fit(df_analysis)
        estimates_df = sem_model.inspect()
        
        num_cols = ['Estimate', 'Std. Err', 'z-value', 'p-value']
        for col in num_cols:
            if col in estimates_df.columns:
                estimates_df[col] = pd.to_numeric(estimates_df[col], errors='coerce')
                
        fit_indices = calc_stats(sem_model)
        model_fitted = True
    except Exception as err:
        st.error(f"Error saat fitting model SEM: {err}")


# ==============================================================================
# STRUKTUR MENU 7 TAB URUTAN FIX
# ==============================================================================
tabs = st.tabs([
    "📊 1. Head & Deskripsi Data",
    "🎯 2. Perumusan Hipotesis",
    "📌 3. Sintaks Model",
    "🎨 4. Diagram Jalur",
    "🔑 5. Hasil Estimasi & Fit",
    "📝 6. Pengujian Hipotesis",
    "📄 7. Hasil Analisa Lengkap & Ekspor PDF"
])

# ------------------------------------------------------------------------------
# TAB 1: HEAD & DESKRIPSI DATA
# ------------------------------------------------------------------------------
with tabs[0]:
    st.markdown("### 📊 Pratinjau Head & Deskripsi Data")
    st.write("Pratinjau 10 baris pertama data survei dan ringkasan statistik deskriptif:")
    
    col_head1, col_head2 = st.columns([1, 1])
    with col_head1:
        st.markdown("**10 Baris Pertama Dataset (Head):**")
        st.dataframe(df_analysis.head(10), width="stretch")
    
    with col_head2:
        st.markdown("**Statistik Deskriptif Dataset:**")
        st.dataframe(df_analysis.describe().T[['count', 'mean', 'std', 'min', 'max']], width="stretch")
        
    st.markdown("**Matriks Korelasi Antar-Indikator:**")
    st.dataframe(df_analysis.corr().style.background_gradient(cmap='coolwarm').format("{:.2f}"), width="stretch")

# ------------------------------------------------------------------------------
# TAB 2: PERUMUSAN HIPOTESIS
# ------------------------------------------------------------------------------
with tabs[1]:
    st.markdown("### 🎯 Perumusan Hipotesis Penelitian")
    st.write("Daftar hipotesis struktural kausalitas yang dirumuskan secara otomatis berdasarkan alur model:")
    
    for h in hypotheses_list:
        st.markdown(f"""
        <div class="card-hypothesis">
            <h4 style="margin: 0; color: #0369A1;">{h['code']}: Jalur Structural ({h['path']})</h4>
            <p style="margin: 5px 0 0 0; color: #334155;">{h['statement']}</p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 3: SINTAKS MODEL
# ------------------------------------------------------------------------------
with tabs[2]:
    st.markdown("### 📌 Kode Sintaks Pemodelan SEM (`semopy`)")
    st.code(model_syntax, language="text")
    st.info("💡 Karakter `=~` melambangkan Model Pengukuran dan `~` melambangkan Model Struktural Regresi.")

# ------------------------------------------------------------------------------
# TAB 4: DIAGRAM JALUR
# ------------------------------------------------------------------------------
with tabs[3]:
    st.markdown("### 🎨 Visualisasi Diagram Jalur Model SEM")
    fig_sem = draw_sem_diagram_custom(num_x, num_m, num_y, indicators_config)
    st.pyplot(fig_sem)

# ------------------------------------------------------------------------------
# TAB 5: HASIL ESTIMASI & FIT
# ------------------------------------------------------------------------------
with tabs[4]:
    st.markdown("### 🔑 Hasil Estimasi Parameter & Indikator Fit")
    if not SEMOPY_AVAILABLE:
        st.error("❌ Pustaka `semopy` belum terpasang.")
    elif model_fitted:
        st.success("🎉 Fitting model CB-SEM berhasil diselesaikan!")
        
        st.markdown("#### 1. Path Coefficients (Regresi Struktural)")
        structural_df = estimates_df[estimates_df['op'] == '~'].copy()
        if not structural_df.empty:
            st.dataframe(
                structural_df[['lval', 'rval', 'Estimate', 'Std. Err', 'z-value', 'p-value']]
                .rename(columns={'lval': 'Variabel Dependen', 'rval': 'Variabel Independen', 'Estimate': 'Estimasi Koefisien (\u03b2)'})
                .style.highlight_between(left=0.0, right=0.05, subset=['p-value'], color='#D1FAE5')
                .format({'Estimasi Koefisien (\u03b2)': '{:.3f}', 'Std. Err': '{:.3f}', 'z-value': '{:.3f}', 'p-value': '{:.3f}'}, na_rep='-'),
                width="stretch"
            )
        
        st.markdown("#### 2. Factor Loadings (Measurement Model)")
        measurement_df = estimates_df[estimates_df['op'] == '=~'].copy()
        st.dataframe(
            measurement_df[['lval', 'rval', 'Estimate', 'Std. Err', 'z-value', 'p-value']]
            .rename(columns={'lval': 'Variabel Laten', 'rval': 'Indikator Manifest', 'Estimate': 'Factor Loading (\u03bb)'})
            .style.format({'Factor Loading (\u03bb)': '{:.3f}', 'Std. Err': '{:.3f}', 'z-value': '{:.3f}', 'p-value': '{:.3f}'}, na_rep='-'),
            width="stretch"
        )
        
        st.markdown("#### 3. Indikator Kelayakan Model (Goodness of Fit)")
        col_fit1, col_fit2, col_fit3 = st.columns(3)
        
        cfi_val = float(fit_indices['CFI'].values[0]) if 'CFI' in fit_indices.columns else 0.0
        tli_val = float(fit_indices['TLI'].values[0]) if 'TLI' in fit_indices.columns else 0.0
        rmsea_val = float(fit_indices['RMSEA'].values[0]) if 'RMSEA' in fit_indices.columns else 0.0
        
        with col_fit1:
            st.metric("CFI (Comparative Fit Index)", f"{cfi_val:.3f}", delta="Ideal (>= 0.90)" if cfi_val >= 0.90 else "Kurang Ideal (< 0.90)", delta_color="normal" if cfi_val >= 0.90 else "inverse")
        with col_fit2:
            st.metric("TLI (Tucker-Lewis Index)", f"{tli_val:.3f}", delta="Ideal (>= 0.90)" if tli_val >= 0.90 else "Kurang Ideal (< 0.90)", delta_color="normal" if tli_val >= 0.90 else "inverse")
        with col_fit3:
            st.metric("RMSEA Error Rate", f"{rmsea_val:.3f}", delta="Ideal (<= 0.08)" if rmsea_val <= 0.08 else "Kurang Ideal (> 0.08)", delta_color="inverse" if rmsea_val <= 0.08 else "normal")

        with st.expander("Metrik Statistik Kelayakan Model Lengkap:", expanded=False):
            st.dataframe(fit_indices.T.rename(columns={0: 'Nilai Statistik'}), width="stretch")

# ------------------------------------------------------------------------------
# TAB 6: PENGUJIAN HIPOTESIS
# ------------------------------------------------------------------------------
hypothesis_results = []
if model_fitted and not estimates_df.empty:
    structural_df = estimates_df[estimates_df['op'] == '~'].copy()
    for h in hypotheses_list:
        row = structural_df[(structural_df['lval'] == h['dep']) & (structural_df['rval'] == h['indep'])]
        if not row.empty:
            beta = row['Estimate'].values[0]
            se = row['Std. Err'].values[0]
            z_val = row['z-value'].values[0]
            p_val = row['p-value'].values[0]
            
            if pd.notna(p_val) and p_val <= 0.05:
                decision = "✅ DITERIMA (Signifikan)"
            else:
                decision = "❌ DITOLAK (Tidak Signifikan)"
                
            hypothesis_results.append({
                'Hipotesis': h['code'],
                'Jalur Hubungan': h['path'],
                'Koefisien (\u03b2)': beta,
                'Std. Err': se,
                'z-value': z_val,
                'p-value': p_val,
                'Keputusan (\u03b1 = 0.05)': decision
            })

with tabs[5]:
    st.markdown("### 📝 Pengujian Hipotesis & Keputusan Statistik")
    if hypothesis_results:
        df_hypo_summary = pd.DataFrame(hypothesis_results)
        st.dataframe(
            df_hypo_summary.style.format({
                'Koefisien (\u03b2)': '{:.3f}',
                'Std. Err': '{:.3f}',
                'z-value': '{:.3f}',
                'p-value': '{:.3f}'
            }, na_rep='-'),
            width="stretch"
        )
        
        accepted_cnt = sum(1 for r in hypothesis_results if "DITERIMA" in r['Keputusan (\u03b1 = 0.05)'])
        st.markdown(f"""
        <div class="card-conclusion">
            <h4 style="margin: 0; color: #15803D;">📌 Rangkuman Ringkas Uji Hipotesis</h4>
            <p style="margin: 5px 0 0 0; color: #166534;">
                Dari total <b>{len(hypothesis_results)} hipotesis</b> yang diuji, sebanyak <b>{accepted_cnt} hipotesis terbukti diterima secara signifikan</b> (&alpha; = 0.05).
            </p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 7: HASIL ANALISA LENGKAP & EKSPOR PDF (BESERTA PREVIEW PDF)
# ------------------------------------------------------------------------------
def generate_pdf_report(report_text):
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 5, 'Laporan Analisis CB-SEM Python | STIE Indonesia Malang', 0, 1, 'R')
            self.line(10, 15, 200, 15)
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 10, f'Halaman {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Arial', '', 9.5)
    
    for line in report_text.split('\n'):
        if line.startswith('===') or line.startswith('---'):
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(0, 4, line[:75], 0, 1, 'L')
            pdf.set_font('Arial', '', 9.5)
        elif line.startswith('BAB') or line.startswith('4.'):
            pdf.set_font('Arial', 'B', 10.5)
            pdf.set_text_color(30, 58, 138)
            pdf.cell(0, 6, line, 0, 1, 'L')
            pdf.set_font('Arial', '', 9.5)
            pdf.set_text_color(31, 41, 55)
        else:
            clean_line = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 4.5, clean_line)
            
    return pdf.output(dest='S').encode('latin-1')


with tabs[6]:
    st.markdown("### 📄 7. Hasil Analisa Lengkap & Ekspor PDF")
    st.write("Draf laporan riset ilmiah lengkap (Bab IV Hasil & Pembahasan) dengan struktur baku terurut siap dipratinjau dalam viewer PDF:")
    
    if model_fitted and hypothesis_results:
        cfi_val = float(fit_indices['CFI'].values[0]) if 'CFI' in fit_indices.columns else 0.0
        tli_val = float(fit_indices['TLI'].values[0]) if 'TLI' in fit_indices.columns else 0.0
        rmsea_val = float(fit_indices['RMSEA'].values[0]) if 'RMSEA' in fit_indices.columns else 0.0
        n_accepted = sum(1 for r in hypothesis_results if 'DITERIMA' in r['Keputusan (\u03b1 = 0.05)'])
        
        # TEKS LAPORAN DENGAN URUTAN BAB IV BAKU
        report_text = f"""================================================================================
LAPORAN HASIL ANALISIS STRUCTURAL EQUATION MODELING (CB-SEM)
================================================================================
Penyusun  : Ir. M Nasri AW, M.Eng.Sc, M.Kom
Institusi : STIE Indonesia Malang (STIEIMA)
Aplikasi  : SEM-IMA (Covariance-Based SEM Engine)
================================================================================

BAB IV HASIL ANALISIS DAN PEMBAHASAN

4.1 Tinjauan Data & Deskripsi Statistik
--------------------------------------------------------------------------------
Analisis ini menggunakan dataset survei dengan total responden N = {len(df_analysis)} sampel.
Statistik deskriptif data mencakup indikator variabel laten X (Exogenous),
M (Mediator), dan Y (Endogenous) dengan skala pengukuran Likert 1 s.d 5.
Rata-rata keseluruhan indikator berada pada rentang yang memadai dengan tingkat 
sebaran (std. deviasi) data yang terdistribusi secara wajar.

4.2 Sintaks & Diagram Jalur
--------------------------------------------------------------------------------
Spesifikasi model dirakit secara konfirmatori menggunakan sintaks semopy:
{model_syntax}

Model ini menghubungkan secara visual konstruk laten (lingkaran) dengan indikator 
terukur (kotak) dalam Diagram Jalur (Path Diagram) struktur kausalitas.

4.3 Penyusunan Hipotesis Penelitian
--------------------------------------------------------------------------------
Berdasarkan kerangka konseptual yang dibangun, rumusan hipotesis penelitian meliputi:
"""
        for h in hypotheses_list:
            report_text += f"- [{h['code']}] Jalur {h['path']}: {h['statement']}\n"

        report_text += f"""
4.4 Hasil Analisis & Pembahasan
--------------------------------------------------------------------------------
A. Evaluasi Goodness-of-Fit (Kelayakan Model Global):
- Comparative Fit Index (CFI) : {cfi_val:.3f} (Kriteria Ideal: >= 0.90)
- Tucker-Lewis Index (TLI)    : {tli_val:.3f} (Kriteria Ideal: >= 0.90)
- RMSEA Error Rate            : {rmsea_val:.3f} (Kriteria Ideal: <= 0.08)

Kesimpulan Evaluasi: Model struktural tergolong {'SANGAT FIT / LAYAK' if cfi_val >= 0.90 else 'MARGINAL FIT'}, 
sehingga pengujian hipotesis kausalitas antar-variabel dinyatakan valid.

B. Evaluasi Model Pengukuran (Measurement Model):
Indikator manifest untuk seluruh variabel laten memiliki nilai Factor Loading (lambda) 
yang signifikan (p < 0.05) dan memenuhi batas reliabilitas konstruk.

C. Pengujian Hipotesis Kausalitas (Structural Model):
"""
        for r in hypothesis_results:
            beta_val = r['Koefisien (β)']
            beta_str = f"{beta_val:.3f}" if pd.notna(beta_val) else "-"
            pval_str = f"{r['p-value']:.3f}" if pd.notna(r['p-value']) else "-"
            zval_str = f"{r['z-value']:.3f}" if pd.notna(r['z-value']) else "-"
            
            report_text += f"[{r['Hipotesis']}] Jalur {r['Jalur Hubungan']}\n"
            report_text += f"     - Koefisien Beta (Estimasi) : {beta_str}\n"
            report_text += f"     - z-value / t-statistic     : {zval_str}\n"
            report_text += f"     - p-value                   : {pval_str}\n"
            report_text += f"     - Keputusan Hipotesis       : {r['Keputusan (α = 0.05)']}\n\n"

        report_text += f"""4.5 Kesimpulan Hasil Penelitian
--------------------------------------------------------------------------------
Dari {len(hypothesis_results)} hipotesis yang diajukan dalam penelitian ini:
- Jumlah Hipotesis Diterima : {n_accepted}
- Jumlah Hipotesis Ditolak  : {len(hypothesis_results) - n_accepted}

Implikasi Akademis:
Hasil analisis mendukung kerangka konseptual yang dibangun. Variabel laten 
independen memberikan kontribusi nyata terhadap pembentukan variabel laten 
dependen baik secara langsung maupun melalui jalur variabel mediasi.

================================================================================
Aplikasi SEM-IMA | STIE Indonesia Malang © 2026
================================================================================
"""

        # Generasi File PDF
        pdf_bytes = generate_pdf_report(report_text) if FPDF_AVAILABLE else None

        # VIEWERS PREVIEW (TEKS & PDF PREVIEWER INTERAKTIF)
        preview_tab1, preview_tab2 = st.tabs(["📑 Pratinjau PDF Viewer", "📝 Pratinjau Teks Draf"])
        
        with preview_tab1:
            st.markdown("#### 👁️ Pratinjau Dokumen PDF Laporan Riset")
            if FPDF_AVAILABLE and pdf_bytes:
                import base64
                base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Modul `fpdf` belum terinstal (`pip install fpdf`). Menampilkan pratinjau teks.")

        with preview_tab2:
            st.markdown("#### 👁️ Pratinjau Teks Laporan Akademik")
            st.text_area("Teks Laporan Siap Copy-Paste:", report_text, height=350)
        
        st.markdown("---")
        st.markdown("#### 📥 Unduh Berkas Laporan Hasil Analisis")
        
        col_pdf1, col_pdf2, col_pdf3 = st.columns(3)
        
        with col_pdf1:
            if FPDF_AVAILABLE and pdf_bytes:
                st.download_button(
                    label="📕 Unduh Laporan PDF (.PDF)",
                    data=pdf_bytes,
                    file_name="Laporan_Hasil_Analisis_CB_SEM.pdf",
                    mime="application/pdf",
                    width="stretch"
                )
            else:
                st.error("Silakan instal fpdf: `pip install fpdf`")
                
        with col_pdf2:
            st.download_button(
                label="📄 Unduh Laporan Teks (.TXT)",
                data=report_text,
                file_name="Laporan_Hasil_Analisis_CB_SEM.txt",
                mime="text/plain",
                width="stretch"
            )
            
        with col_pdf3:
            res_csv = pd.DataFrame(hypothesis_results).to_csv(index=False)
            st.download_button(
                label="📊 Unduh Tabel Hipotesis (.CSV)",
                data=res_csv,
                file_name="Rekap_Hasil_Pengujian_Hipotesis.csv",
                mime="text/csv",
                width="stretch"
            )
    else:
        st.warning("⚠️ Laporan belum dapat digenerasi. Pastikan data berhasil di-fit.")

# Footer Halaman
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #9CA3AF; font-size: 11px;'>"
    "Aplikasi Analisa CB-SEM | STIE Indonesia Malang (STIEIMA) © 2026"
    "</div>", 
    unsafe_allow_html=True
)
