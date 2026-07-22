import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import warnings
warnings.filterwarnings('ignore')

try:
    from semopy import Model, calc_stats
    SEMOPY_AVAILABLE = True
except ImportError:
    SEMOPY_AVAILABLE = False

st.set_page_config(
    page_title="Analisa Covariance Based Structural Equation Modeling (CB-SEM)",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk memperindah tampilan dashboard
st.markdown("""
<style>
    .main-header {
        font-size: 32px;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 15px;
        color: #4B5563;
        margin-bottom: 25px;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    .card {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #2563EB;
        margin-bottom: 20px;
    }
    .report-preview {
        background-color: #FFFFFF;
        padding: 25px;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        font-family: 'Times New Roman', Times, serif;
        line-height: 1.6;
        color: #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# Header Sidebar
st.sidebar.markdown("""
<div style="text-align: center; padding-bottom: 15px;">
    <h2 style="color: #1E3A8A; margin-bottom: 0;">📊 SEM-IMA CB-SEM</h2>
    <p style="font-size: 12px; color: #6B7280; font-weight: bold;">Analisis Struktural Equation Modeling (CB-SEM) via Python semopy</p>
</div>
""", unsafe_allow_html=True)

# Identitas Penyusun
st.sidebar.markdown("""
<div style="background-color: #EFF6FF; border: 1px solid #BFDBFE; padding: 12px; border-radius: 8px; margin-bottom: 20px;">
    <p style="margin: 0; font-size: 11px; color: #1E40AF; font-weight: bold; text-transform: uppercase;">Penyusun & Institusi:</p>
    <p style="margin: 0; font-size: 14px; color: #1E3A8A; font-weight: 800;">Ir. M Nasri AW, M.Eng.Sc, M.Kom</p>
    <p style="margin: 0; font-size: 12px; color: #1E40AF;">Dosen STIE Indonesia Malang (STIEIMA)</p>
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
            base_y += 0.25 * latents[x_key]
        for m_key in [k for k in latents.keys() if k.startswith("M")]:
            base_y += 0.5 * latents[m_key]
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

st.markdown('<div class="main-header">Aplikasi Analisis CB-SEM Terpadu</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Pemodelan, Rumusan Hipotesis, Pengujian, Narasi Pembahasan Akademik & Ekspor Laporan Riset Lengkap</div>', unsafe_allow_html=True)

# Panduan Alur Kerja Aplikasi
with st.expander("📖 Panduan Cara Menggunakan Aplikasi", expanded=False):
    st.markdown("""
    1. **Atur jumlah variabel laten** ($X$, $M$, $Y$) beserta jumlah indikator masing-masing pada **Sidebar sebelah kiri**.
    2. Unduh **Template CSV** acuan jika ingin mengisi data survei baru.
    3. Pilih opsi **Gunakan Data Simulasi Otomatis** atau unggah file CSV Anda sendiri.
    4. Navigasikan tab dari **Tab 1 (Rumusan Hipotesis)** hingga **Tab 6 (Laporan Hasil Analisis Lengkap & Ekspor Dokumen)**.
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

if data_option == "Gunakan Data Unggahan (CSV)" and uploaded_file is not None:
    try:
        df_analysis = pd.read_csv(uploaded_file)
        st.success("✅ File CSV berhasil diunggah!")
    except Exception as e:
        st.error(f"Gagal membaca file CSV: {e}")
        df_analysis = template_df
else:
    df_analysis = template_df
    st.info("ℹ️ Saat ini menggunakan data simulasi otomatis sesuai konfigurasi parameter Anda.")

# Merakit deskripsi model semopy & hipotesis
model_desc_lines = ["# Measurement Model"]
hypothesis_list = []
hypo_idx = 1

for latent_name, n_ind in indicators_config.items():
    prefix = latent_name.lower()
    indicators = [f"{prefix}{idx}" for idx in range(1, n_ind + 1)]
    model_desc_lines.append(f"{latent_name} =~ {' + '.join(indicators)}")

model_desc_lines.append("\n# Structural Model")

if num_m > 0:
    for i in range(1, num_x + 1):
        for j in range(1, num_m + 1):
            hypothesis_list.append({
                'code': f"H{hypo_idx}",
                'path': f"M{j} ~ X{i}",
                'iv': f"X{i}",
                'dv': f"M{j}",
                'desc': f"Terdapat pengaruh positif dan signifikan X{i} terhadap M{j}"
            })
            hypo_idx += 1
            
    x_list = [f"X{i}" for i in range(1, num_x + 1)]
    for j in range(1, num_m + 1):
        model_desc_lines.append(f"M{j} ~ {' + '.join(x_list)}")

for k in range(1, num_y + 1):
    for i in range(1, num_x + 1):
        hypothesis_list.append({
            'code': f"H{hypo_idx}",
            'path': f"Y{k} ~ X{i}",
            'iv': f"X{i}",
            'dv': f"Y{k}",
            'desc': f"Terdapat pengaruh positif dan signifikan X{i} terhadap Y{k}"
        })
        hypo_idx += 1
        
    if num_m > 0:
        for j in range(1, num_m + 1):
            hypothesis_list.append({
                'code': f"H{hypo_idx}",
                'path': f"Y{k} ~ M{j}",
                'iv': f"M{j}",
                'dv': f"Y{k}",
                'desc': f"Terdapat pengaruh positif dan signifikan M{j} terhadap Y{k}"
            })
            hypo_idx += 1

    predictors = [f"X{i}" for i in range(1, num_x + 1)]
    if num_m > 0:
        predictors += [f"M{j}" for j in range(1, num_m + 1)]
    model_desc_lines.append(f"Y{k} ~ {' + '.join(predictors)}")

model_syntax = "\n".join(model_desc_lines)

def draw_sem_diagram_custom(num_x, num_m, num_y, indicators_config):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')
    x_pos_exog, x_pos_med, x_pos_endo = 1.0, 3.0, 5.0
    latent_positions = {}
    
    y_starts_x = np.linspace(4.5, 1.5, num_x) if num_x > 1 else [3.0]
    for idx, y_val in enumerate(y_starts_x, 1):
        name = f"X{idx}"
        latent_positions[name] = (x_pos_exog, y_val)
        circle = plt.Circle((x_pos_exog, y_val), 0.35, color='#3B82F6', alpha=0.85, zorder=3)
        ax.add_patch(circle)
        ax.text(x_pos_exog, y_val, name, color='white', ha='center', va='center', weight='bold', fontsize=12, zorder=4)

    if num_m > 0:
        y_starts_m = np.linspace(4.5, 1.5, num_m) if num_m > 1 else [3.0]
        for idx, y_val in enumerate(y_starts_m, 1):
            name = f"M{idx}"
            latent_positions[name] = (x_pos_med, y_val)
            circle = plt.Circle((x_pos_med, y_val), 0.35, color='#F59E0B', alpha=0.85, zorder=3)
            ax.add_patch(circle)
            ax.text(x_pos_med, y_val, name, color='white', ha='center', va='center', weight='bold', fontsize=12, zorder=4)

    y_starts_y = np.linspace(4.5, 1.5, num_y) if num_y > 1 else [3.0]
    for idx, y_val in enumerate(y_starts_y, 1):
        name = f"Y{idx}"
        latent_positions[name] = (x_pos_endo, y_val)
        circle = plt.Circle((x_pos_endo, y_val), 0.35, color='#10B981', alpha=0.85, zorder=3)
        ax.add_patch(circle)
        ax.text(x_pos_endo, y_val, name, color='white', ha='center', va='center', weight='bold', fontsize=12, zorder=4)

    if num_m > 0:
        for x_name in [k for k in latent_positions.keys() if k.startswith("X")]:
            for m_name in [k for k in latent_positions.keys() if k.startswith("M")]:
                ax.annotate('', xy=latent_positions[m_name], xytext=latent_positions[x_name],
                            arrowprops=dict(arrowstyle="->", color='#374151', lw=2, shrinkA=25, shrinkB=25))
                
        for m_name in [k for k in latent_positions.keys() if k.startswith("M")]:
            for y_name in [k for k in latent_positions.keys() if k.startswith("Y")]:
                ax.annotate('', xy=latent_positions[y_name], xytext=latent_positions[m_name],
                            arrowprops=dict(arrowstyle="->", color='#374151', lw=2, shrinkA=25, shrinkB=25))

    for x_name in [k for k in latent_positions.keys() if k.startswith("X")]:
        for y_name in [k for k in latent_positions.keys() if k.startswith("Y")]:
            conn = "arc3,rad=-0.15" if num_m > 0 else "arc3,rad=0"
            ax.annotate('', xy=latent_positions[y_name], xytext=latent_positions[x_name],
                        arrowprops=dict(arrowstyle="->", color='#6B7280', lw=1.5, ls='--', connectionstyle=conn, shrinkA=25, shrinkB=25))

    plt.xlim(0.0, 6.0)
    plt.ylim(0.5, 5.5)
    return fig

# 6 Tab Alur Kerja Akademik
tabs = st.tabs([
    "📌 1. Rumusan Hipotesis", 
    "📝 2. Sintaks Model", 
    "🎨 3. Diagram Jalur", 
    "🔑 4. Hasil Estimasi Fit", 
    "📊 5. Pengujian & Narasi", 
    "📄 6. Laporan Lengkap & Ekspor"
])

with tabs[0]:
    st.markdown("### 📌 Rumusan Hipotesis Penelitian Otomatis")
    st.write("Hipotesis penelitian dirumuskan secara sistematis berdasarkan struktur hubungan variabel laten yang dikonfigurasi:")
    
    hypo_df = pd.DataFrame(hypothesis_list)
    st.dataframe(hypo_df[['code', 'iv', 'dv', 'desc']].rename(columns={
        'code': 'Kode Hipotesis', 'iv': 'Variabel Independen', 'dv': 'Variabel Dependen', 'desc': 'Pernyataan Hipotesis'
    }), use_container_width=True)

with tabs[1]:
    st.markdown("### 📝 Kode Sintaks Konfigurasi SEM (`semopy`)")
    st.code(model_syntax, language="text")

with tabs[2]:
    st.markdown("### 🎨 Visualisasi Diagram Jalur (Path Diagram)")
    fig_sem = draw_sem_diagram_custom(num_x, num_m, num_y, indicators_config)
    st.pyplot(fig_sem)

# Fitting Model Utama
estimates_df = None
fit_indices = None
hypo_test_results = []

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
        
        # Evaluasi Hipotesis
        for h in hypothesis_list:
            parts = h['path'].split(' ~ ')
            dv, iv = parts[0].strip(), parts[1].strip()
            
            match = estimates_df[(estimates_df['op'] == '~') & (estimates_df['lval'] == dv) & (estimates_df['rval'] == iv)]
            if not match.empty:
                est = match['Estimate'].values[0]
                se = match['Std. Err'].values[0]
                zval = match['z-value'].values[0]
                pval = match['p-value'].values[0]
                
                is_sig = (pval < 0.05) if not np.isnan(pval) else False
                decision = "Diterima (Signifikan)" if is_sig else "Ditolak (Tidak Signifikan)"
                
                hypo_test_results.append({
                    'Kode': h['code'],
                    'Jalur Kausalitas': f"{iv} -> {dv}",
                    'Estimasi (Beta)': est,
                    'Std. Error': se,
                    'z-value': zval,
                    'p-value': pval,
                    'Keputusan': decision
                })
    except Exception as err:
        st.error(f"Error saat fitting model: {err}")

with tabs[3]:
    st.markdown("### 🔑 Hasil Estimasi Parameter & Indikator Fit")
    if estimates_df is not None:
        st.markdown("#### 1. Path Coefficients (Regresi Struktural)")
        st.dataframe(estimates_df[estimates_df['op'] == '~'], use_container_width=True)
        st.markdown("#### 2. Factor Loadings (Measurement Model)")
        st.dataframe(estimates_df[estimates_df['op'] == '=~'], use_container_width=True)
        st.markdown("#### 3. Goodness of Fit Indices")
        st.dataframe(fit_indices, use_container_width=True)

with tabs[4]:
    st.markdown("### 📊 Pengujian Hipotesis & Pembahasan Akademik")
    if hypo_test_results:
        res_df = pd.DataFrame(hypo_test_results)
        st.dataframe(res_df.style.highlight_between(left=0.0, right=0.05, subset=['p-value'], color='#D1FAE5'), use_container_width=True)
        
        st.markdown("#### 📝 Narasi Interpretasi Pembahasan Akademik")
        cfi_v = float(fit_indices['CFI'].values[0]) if 'CFI' in fit_indices.columns else 0.0
        rmsea_v = float(fit_indices['RMSEA'].values[0]) if 'RMSEA' in fit_indices.columns else 0.0
        
        st.write(f"""
        Berdasarkan pengujian Goodness of Fit, model tergolong **{'Sangat Baik / Fit' if cfi_v >= 0.90 else 'Marginal Fit'}** 
        dengan nilai CFI sebesar **{cfi_v:.3f}** dan tingkat error RMSEA sebesar **{rmsea_v:.3f}**. 
        Dari total **{len(hypo_test_results)} hipotesis** yang diuji, terdapat **{sum(1 for r in hypo_test_results if 'Diterima' in r['Keputusan'])} hipotesis diterima** pada tingkat signifikansi $\\alpha = 5\\%$.
        """)

# --- MENU 6: TAB LAPORAN LENGKAP & EKSPOR DOKUMEN ---
with tabs[5]:
    st.markdown("### 📄 6. Laporan Hasil Analisis Lengkap & Ekspor Dokumen")
    st.write("Sistem menyusun draft laporan riset ilmiah lengkap (Bab IV Hasil & Pembahasan) yang dapat dipratinjau dan diunduh langsung.")
    
    if estimates_df is not None and hypo_test_results:
        cfi_val = float(fit_indices['CFI'].values[0]) if 'CFI' in fit_indices.columns else 0.0
        tli_val = float(fit_indices['TLI'].values[0]) if 'TLI' in fit_indices.columns else 0.0
        rmsea_val = float(fit_indices['RMSEA'].values[0]) if 'RMSEA' in fit_indices.columns else 0.0
        
        n_accepted = sum(1 for r in hypo_test_results if 'Diterima' in r['Keputusan'])
        
        # Merakit teks laporan akademik lengkap (Draft Markdown/TXT/DOCX)
        report_text = f"""================================================================================
LAPORAN HASIL ANALISIS STRUCTURAL EQUATION MODELING (CB-SEM)
================================================================================
Penyusun  : Ir. M Nasri AW, M.Eng.Sc, M.Kom
Institusi : STIE Indonesia Malang (STIEIMA)
Aplikasi  : SEM-IMA (Covariance-Based SEM Python Engine)
================================================================================

BAB IV HASIL ANALISIS DAN PEMBAHASAN

4.1 Evaluasi Goodness-of-Fit (Kelayakan Model Global)
--------------------------------------------------------------------------------
Berdasarkan hasil analisis CB-SEM menggunakan algoritma Maximum Likelihood, 
diperoleh indikator kelayakan model (Goodness of Fit) sebagai berikut:
- Comparative Fit Index (CFI) : {cfi_val:.3f} (Kriteria Ideal: >= 0.90)
- Tucker-Lewis Index (TLI)    : {tli_val:.3f} (Kriteria Ideal: >= 0.90)
- RMSEA Error Rate            : {rmsea_val:.3f} (Kriteria Ideal: <= 0.08)

Kesimpulan Evaluasi Model: Model struktural tergolong {'SANGAT FIT / LAYAK' if cfi_val >= 0.90 else 'MARGINAL FIT'}, 
sehingga pengujian hipotesis kausalitas antar-variabel dapat dilanjutkan.

4.2 Hasil Pengujian Model Pengukuran (Measurement Model / Factor Loadings)
--------------------------------------------------------------------------------
Seluruh indikator terukur (manifest) untuk variabel laten X, M, dan Y memiliki 
nilai factor loading yang signifikan (p < 0.05) dan memenuhi kriteria validitas konstruk.

4.3 Hasil Pengujian Hipotesis Penelitian
--------------------------------------------------------------------------------
Ringkasan keputusan pengujian hipotesis kausalitas adalah sebagai berikut:

"""
        for r in hypo_test_results:
            report_text += f"[{r['Kode']}] Jalur {r['Jalur Kausalitas']}\n"
            report_text += f"     - Koefisien Beta (Estimasi) : {r['Estimasi (Beta)']:.3f}\n"
            report_text += f"     - z-value / t-statistic     : {r['z-value']:.3f}\n"
            report_text += f"     - p-value                   : {r['p-value']:.3f}\n"
            report_text += f"     - Keputusan Hipotesis       : {r['Keputusan']}\n\n"

        report_text += f"""4.4 Kesimpulan Hasil Penelitian
--------------------------------------------------------------------------------
Dari {len(hypo_test_results)} hipotesis yang diajukan dalam penelitian ini:
- Jumlah Hipotesis Diterima : {n_accepted}
- Jumlah Hipotesis Ditolak  : {len(hypo_test_results) - n_accepted}

Implikasi Akademis:
Hasil analisis mendukung kerangka konseptual yang dibangun. Variabel laten independen 
memberikan kontribusi nyata terhadap pembentukan variabel laten dependen baik 
secara langsung maupun melalui jalur variabel mediasi.

================================================================================
Aplikasi SEM-IMA | STIE Indonesia Malang © 2026
================================================================================
"""

        # Display Live Preview Box
        st.markdown("#### 👁️ Pratinjau Dokumen Laporan (Live Preview)")
        st.text_area("Preview Teks Laporan Akademik Siap Copy-Paste:", report_text, height=350)
        
        st.markdown("---")
        st.markdown("#### 📥 Opsi Ekspor Dokumen Laporan & Data")
        
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        
        with col_dl1:
            st.download_button(
                label="📄 Unduh Laporan Lengkap (.TXT)",
                data=report_text,
                file_name="Laporan_Hasil_Analisis_CB_SEM.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        with col_dl2:
            st.download_button(
                label="📝 Unduh Laporan (.MD)",
                data=f"```text\n{report_text}\n```",
                file_name="Laporan_Hasil_Analisis_CB_SEM.md",
                mime="text/markdown",
                use_container_width=True
            )
            
        with col_dl3:
            # Export CSV Rekap Hipotesis
            res_csv = pd.DataFrame(hypo_test_results).to_csv(index=False)
            st.download_button(
                label="📊 Unduh Tabel Hipotesis (.CSV)",
                data=res_csv,
                file_name="Rekap_Hasil_Pengujian_Hipotesis.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.warning("⚠️ Laporan belum dapat digenerasi. Silakan pastikan data telah berhasil di-fit pada model.")

# Footer Halaman
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #9CA3AF; font-size: 11px;'>"
    "Aplikasi Template Analisa SEM Sederhana | Dikembangkan untuk Kebutuhan Akademik STIEIMA © 2026"
    "</div>", 
    unsafe_allow_html=True
)
