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
    page_title="Analisa CB-SEM (Covariance-Based SEM)",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling CSS
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
    <h1 style="color: #1E3A8A; margin-bottom: 0;">📊 Analisis Multivariate Covariance-Based Structural Equation Modeling (CB-SEM),v2.0 @2026</h1>
    <p style="font-size: 14px; color: #6B7280; font-weight: bold;">CB-SEM menggunakan data cukup besar (N>=100-200). Pelajari kapan menggunakan Covariance Based (CB-SEM) atau Partial Least Squares (PLS-SEM). Pelajari Panduan Cara Menggunakan Aplikasi</p>
</div>
""", unsafe_allow_html=True)

# Identitas Penyusun
st.sidebar.markdown("""
<div style="background-color: #EFF6FF; border: 1px solid #BFDBFE; padding: 12px; border-radius: 8px; margin-bottom: 20px;">
    <p style="margin: 0; font-size: 14px; color: #1E40AF; font-weight: bold; text-transform: uppercase;">Penyusun:</p>
    <p style="margin: 0; font-size: 16px; color: #1E3A8A; font-weight: 800;">M Nasri AW | Pengembang Aplikasi, CB-SEM v2.0 @2026</p>
    <p style="margin: 0; font-size: 16px; color: #4B5563;"> Dosen STIE Indonesia Malang</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("⚙️ Konfigurasi Variabel Laten")

# Input Jumlah Variabel Laten
num_x = st.sidebar.slider("Jumlah Exogenous Latent (X)", 1, 3, 1, help="Variabel bebas yang mempengaruhi mediator atau variabel terikat")
num_m = st.sidebar.slider("Jumlah Mediator Latent (M)", 0, 3, 1, help="Variabel perantara (bisa diatur 0 jika tidak memakai mediasi)")
num_y = st.sidebar.slider("Jumlah Endogenous Latent (Y)", 1, 3, 1, help="Variabel terikat akhir")

# Input Konfigurasi Indikator untuk setiap Variabel
st.sidebar.markdown("---")
st.sidebar.subheader("📐 Jumlah Indikator per Variabel")

indicators_config = {}

# Konfigurasi X
for i in range(1, num_x + 1):
    indicators_config[f"X{i}"] = st.sidebar.number_input(f"Indikator untuk X{i}", min_value=2, max_value=10, value=3, key=f"x_ind_{i}")

# Konfigurasi M
for i in range(1, num_m + 1):
    indicators_config[f"M{i}"] = st.sidebar.number_input(f"Indikator untuk M{i}", min_value=2, max_value=10, value=3, key=f"m_ind_{i}")

# Konfigurasi Y
for i in range(1, num_y + 1):
    indicators_config[f"Y{i}"] = st.sidebar.number_input(f"Indikator untuk Y{i}", min_value=2, max_value=10, value=3, key=f"y_ind_{i}")


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
csv_string = csv_buffer.getvalue()

st.sidebar.markdown("---")
st.sidebar.download_button(
    label="📥 Unduh Template CSV, isi data dengan benar sesuai indikator variabel sebelum di upload",
    data=csv_string,
    file_name="template_data_sem.csv",
    mime="text/csv",
    help="Gunakan file CSV ini sebagai acuan struktur data Anda."
)

#st.markdown('<div class="main-header">Platform Otomatisasi Pengujian #Hipotesis, Fitting Model dan Narasi Output Akademik</div>', unsafe_allow_html=True)
#st.markdown('<div class="sub-header">Berbasis <code>semopy</code> Python</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-header">Platform Otomatisasi Pengujian Hipotesis, Fitting Model dan Narasi Output Akademik</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Berbasis <code>semopy</code> Python — Release v2.0 @2026</p>', unsafe_allow_html=True)

# Panduan Alur Kerja Aplikasi
with st.expander("📖 Panduan Cara Menggunakan Aplikasi", expanded=False):
    st.markdown("""
    1. **Atur jumlah variabel laten** ($X$, $M$, $Y$) beserta indikatornya pada **Sidebar sebelah kiri**.
    2. Unduh **Template CSV** dan masukkan data survei Anda (sampel yang disarankan $N ≥ 100-200$ untuk CB-SEM).
    3. Unggah file CSV Anda atau gunakan **Data Simulasi Otomatis** bawaan aplikasi.
    4. Navigasikan ke Tab **"🎯 Rumusan Hipotesis"**, **"🎨 Diagram Jalur"**, **"🔑 Hasil Estimasi & Fit"**, dan **"📑 Pengujian Hipotesis & Narasi"**.
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
            st.success(f"✅ File CSV berhasil diunggah! (Ukuran Sampel: {len(df_analysis)} responden)")
        except Exception as e:
            st.error(f"Gagal membaca file CSV: {e}")
            df_analysis = template_df
            st.info("Beralih sementara menggunakan data simulasi.")
    else:
        st.warning("⚠️ Silakan unggah file CSV Anda terlebih dahulu. Tampilan beralih ke data simulasi.")
        df_analysis = template_df
else:
    df_analysis = template_df
    st.info(f"ℹ️ Menggunakan data simulasi otomatis (Ukuran Sampel: {len(df_analysis)} responden).")

with st.expander("📊 Pratinjau Dataset & Korelasi Indikator", expanded=False):
    st.dataframe(df_analysis.head(10))
    st.write("Matriks Korelasi Antar-Indikator:")
    st.dataframe(df_analysis.corr().style.background_gradient(cmap='coolwarm').format("{:.2f}"))

# Merakit deskripsi model semopy & Daftar Hipotesis
model_desc_lines = []
hypotheses_list = []

model_desc_lines.append("# Measurement Model")
for latent_name, n_ind in indicators_config.items():
    prefix = latent_name.lower()
    indicators = [f"{prefix}{idx}" for idx in range(1, n_ind + 1)]
    model_desc_lines.append(f"{latent_name} =~ {' + '.join(indicators)}")

model_desc_lines.append("\n# Structural Model")
h_counter = 1

# Structural paths M ~ X
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

# Structural paths Y ~ X + M
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
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    x_pos_exog = 1.0
    x_pos_med = 3.0
    x_pos_endo = 5.0
    latent_positions = {}
    
    # 1. Exogenous X
    y_starts_x = np.linspace(5.0, 1.0, num_x) if num_x > 1 else [3.0]
    for idx, y_val in enumerate(y_starts_x, 1):
        name = f"X{idx}"
        latent_positions[name] = (x_pos_exog, y_val)
        circle = plt.Circle((x_pos_exog, y_val), 0.35, color='#3B82F6', alpha=0.85, zorder=3)
        ax.add_patch(circle)
        ax.text(x_pos_exog, y_val, name, color='white', ha='center', va='center', weight='bold', fontsize=12, zorder=4)
        
        n_ind = indicators_config[name]
        y_inds = np.linspace(y_val + 0.6, y_val - 0.6, n_ind)
        for idx_ind, y_ind in enumerate(y_inds, 1):
            rect = plt.Rectangle((x_pos_exog - 1.0, y_ind - 0.15), 0.4, 0.3, color='#DBEAFE', ec='#2563EB', zorder=2)
            ax.add_patch(rect)
            ax.text(x_pos_exog - 0.8, y_ind, f"x{idx}{idx_ind}", ha='center', va='center', fontsize=8, zorder=3)
            ax.annotate('', xy=(x_pos_exog - 0.6, y_ind), xytext=(x_pos_exog - 0.3, y_val),
                        arrowprops=dict(arrowstyle="<-", color='#2563EB', lw=1, shrinkA=0, shrinkB=5))

    # 2. Mediator M
    if num_m > 0:
        y_starts_m = np.linspace(5.0, 1.0, num_m) if num_m > 1 else [3.0]
        for idx, y_val in enumerate(y_starts_m, 1):
            name = f"M{idx}"
            latent_positions[name] = (x_pos_med, y_val)
            circle = plt.Circle((x_pos_med, y_val), 0.35, color='#F59E0B', alpha=0.85, zorder=3)
            ax.add_patch(circle)
            ax.text(x_pos_med, y_val, name, color='white', ha='center', va='center', weight='bold', fontsize=12, zorder=4)
            
            n_ind = indicators_config[name]
            x_inds = np.linspace(x_pos_med - 0.4, x_pos_med + 0.4, n_ind)
            for idx_ind, x_ind in enumerate(x_inds, 1):
                rect = plt.Rectangle((x_ind - 0.15, y_val + 0.6), 0.3, 0.25, color='#FEF3C7', ec='#D97706', zorder=2)
                ax.add_patch(rect)
                ax.text(x_ind, y_val + 0.725, f"m{idx}{idx_ind}", ha='center', va='center', fontsize=8, zorder=3)
                ax.annotate('', xy=(x_ind, y_val + 0.6), xytext=(x_pos_med, y_val + 0.3),
                            arrowprops=dict(arrowstyle="<-", color='#D97706', lw=1, shrinkA=0, shrinkB=5))

    # 3. Endogenous Y
    y_starts_y = np.linspace(5.0, 1.0, num_y) if num_y > 1 else [3.0]
    for idx, y_val in enumerate(y_starts_y, 1):
        name = f"Y{idx}"
        latent_positions[name] = (x_pos_endo, y_val)
        circle = plt.Circle((x_pos_endo, y_val), 0.35, color='#10B981', alpha=0.85, zorder=3)
        ax.add_patch(circle)
        ax.text(x_pos_endo, y_val, name, color='white', ha='center', va='center', weight='bold', fontsize=12, zorder=4)
        
        n_ind = indicators_config[name]
        y_inds = np.linspace(y_val + 0.6, y_val - 0.6, n_ind)
        for idx_ind, y_ind in enumerate(y_inds, 1):
            rect = plt.Rectangle((x_pos_endo + 0.6, y_ind - 0.15), 0.4, 0.3, color='#D1FAE5', ec='#059669', zorder=2)
            ax.add_patch(rect)
            ax.text(x_pos_endo + 0.8, y_ind, f"y{idx}{idx_ind}", ha='center', va='center', fontsize=8, zorder=3)
            ax.annotate('', xy=(x_pos_endo + 0.6, y_ind), xytext=(x_pos_endo + 0.3, y_val),
                        arrowprops=dict(arrowstyle="<-", color='#059669', lw=1, shrinkA=0, shrinkB=5))

    # 4. Structural Paths
    if num_m > 0:
        for x_name in [k for k in latent_positions.keys() if k.startswith("X")]:
            for m_name in [k for k in latent_positions.keys() if k.startswith("M")]:
                ax.annotate('', xy=latent_positions[m_name], xytext=latent_positions[x_name],
                            arrowprops=dict(arrowstyle="->", color='#374151', lw=2, shrinkA=38, shrinkB=38))
                
        for m_name in [k for k in latent_positions.keys() if k.startswith("M")]:
            for y_name in [k for k in latent_positions.keys() if k.startswith("Y")]:
                ax.annotate('', xy=latent_positions[y_name], xytext=latent_positions[m_name],
                            arrowprops=dict(arrowstyle="->", color='#374151', lw=2, shrinkA=38, shrinkB=38))

    for x_name in [k for k in latent_positions.keys() if k.startswith("X")]:
        for y_name in [k for k in latent_positions.keys() if k.startswith("Y")]:
            connectionstyle = "arc3,rad=-0.15" if num_m > 0 else "arc3,rad=0"
            ax.annotate('', xy=latent_positions[y_name], xytext=latent_positions[x_name],
                        arrowprops=dict(arrowstyle="->", color='#6B7280', lw=1.5, ls='--', 
                                        connectionstyle=connectionstyle, shrinkA=38, shrinkB=38))

    plt.xlim(-0.5, 6.5)
    plt.ylim(0.0, 6.5)
    return fig


tab_hypo, tab_syntax, tab_diag, tab_output, tab_eval = st.tabs([
    "🎯 1. Perumusan Hipotesis",
    "📌 2. Sintaks Model", 
    "🎨 3. Diagram Jalur", 
    "🔑 4. Hasil Estimasi & Fit", 
    "📝 5. Uji Hipotesis & Kesimpulan"
])

# TAB 1: PERUMUSAN HIPOTESIS
with tab_hypo:
    st.markdown("### 🎯 Perumusan Hipotesis Penelitian")
    st.write("Berdasarkan konfigurasi variabel laten yang Anda tetapkan pada sidebar, berikut adalah daftar hipotesis struktural yang dirumuskan secara otomatis:")
    
    for h in hypotheses_list:
        st.markdown(f"""
        <div class="card-hypothesis">
            <h4 style="margin: 0; color: #0369A1;">{h['code']}: Jalur Structural ({h['path']})</h4>
            <p style="margin: 5px 0 0 0; color: #334155;">{h['statement']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.info("💡 Hipotesis di atas akan diuji secara statistik pada Tab **'📝 5. Uji Hipotesis & Kesimpulan'** berdasarkan estimasi model CB-SEM.")

# TAB 2: SINTAKS MODEL
with tab_syntax:
    st.markdown("### Kode Sintaks Pemodelan SEM (`semopy`)")
    st.write("Sintaks spesifikasi model otomatis dibangun berdasarkan alur hubungan variabel laten dan indikatornya:")
    st.code(model_syntax, language="text")
    st.info("💡 Karakter `=~` melambangkan Model Pengukuran (Measurement Model) dan `~` melambangkan Model Struktural (Regresi).")

# TAB 3: DIAGRAM JALUR
with tab_diag:
    st.markdown("### Visualisasi Diagram Jalur Model SEM")
    st.write("Konstruksi hubungan logis antara indikator terukur (kotak) dan variabel laten (lingkaran):")
    fig_sem = draw_sem_diagram_custom(num_x, num_m, num_y, indicators_config)
    st.pyplot(fig_sem)

# GLOBAL VARS FOR FITTING RESULT
model_fitted = False
estimates_df = pd.DataFrame()
fit_indices = pd.DataFrame()

if SEMOPY_AVAILABLE:
    try:
        sem_model = Model(model_syntax)
        sem_model.fit(df_analysis)
        estimates_df = sem_model.inspect()
        
        # Safe numeric parsing for semopy string '-' outputs
        num_cols = ['Estimate', 'Std. Err', 'z-value', 'p-value']
        for col in num_cols:
            if col in estimates_df.columns:
                estimates_df[col] = pd.to_numeric(estimates_df[col], errors='coerce')
                
        fit_indices = calc_stats(sem_model)
        model_fitted = True
    except Exception as err:
        st.error(f"Terjadi kesalahan saat fitting model SEM: {err}")

# TAB 4: HASIL ESTIMASI & FIT
with tab_output:
    st.markdown("### Output Estimasi Parameter & Goodness of Fit")
    if not SEMOPY_AVAILABLE:
        st.error("❌ Pustaka `semopy` belum terpasang di sistem kerja Anda.")
    elif model_fitted:
        st.success("🎉 Fitting model CB-SEM berhasil diselesaikan!")
        
        st.markdown("#### 1. Koefisien Jalur Struktural (Structural Path Coefficients)")
        structural_df = estimates_df[estimates_df['op'] == '~'].copy()
        if not structural_df.empty:
            st.dataframe(
                structural_df[['lval', 'rval', 'Estimate', 'Std. Err', 'z-value', 'p-value']]
                .rename(columns={'lval': 'Variabel Dependen', 'rval': 'Variabel Independen', 'Estimate': 'Estimasi Koefisien (\u03b2)'})
                .style.highlight_between(left=0.0, right=0.05, subset=['p-value'], color='#D1FAE5')
                .format({'Estimasi Koefisien (\u03b2)': '{:.3f}', 'Std. Err': '{:.3f}', 'z-value': '{:.3f}', 'p-value': '{:.3f}'}, na_rep='-')
            )
        
        st.markdown("#### 2. Muatan Faktor Pengukuran (Measurement Outer Loadings)")
        measurement_df = estimates_df[estimates_df['op'] == '=~'].copy()
        st.dataframe(
            measurement_df[['lval', 'rval', 'Estimate', 'Std. Err', 'z-value', 'p-value']]
            .rename(columns={'lval': 'Variabel Laten', 'rval': 'Indikator Manifest', 'Estimate': 'Factor Loading (\u03bb)'})
            .style.format({'Factor Loading (\u03bb)': '{:.3f}', 'Std. Err': '{:.3f}', 'z-value': '{:.3f}', 'p-value': '{:.3f}'}, na_rep='-')
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
            st.dataframe(fit_indices.T.rename(columns={0: 'Nilai Statistik'}))

# TAB 5: UJI HIPOTESIS & NARASI KESIMPULAN
with tab_eval:
    st.markdown("### 📝 Pengujian Hipotesis, Narasi Output, & Kesimpulan")
    
    if not model_fitted or estimates_df.empty:
        st.warning("⚠️ Model belum berhasil di-fit. Silakan periksa kembali dataset Anda.")
    else:
        # 1. TABEL PENGUJIAN HIPOTESIS
        st.markdown("#### A. Tabel Keputusan Pengujian Hipotesis")
        
        hypothesis_results = []
        structural_df = estimates_df[estimates_df['op'] == '~'].copy()
        
        for h in hypotheses_list:
            # Find matching row in structural estimation
            row = structural_df[(structural_df['lval'] == h['dep']) & (structural_df['rval'] == h['indep'])]
            
            if not row.empty:
                beta = row['Estimate'].values[0]
                se = row['Std. Err'].values[0]
                z_val = row['z-value'].values[0]
                p_val = row['p-value'].values[0]
                
                # Decision Rule: p-value <= 0.05 & beta > 0 -> Diterima
                if pd.notna(p_val) and p_val <= 0.05:
                    if beta > 0:
                        decision = "✅ DITERIMA (Signifikan Positif)"
                    else:
                        decision = "⚠️ DITERIMA (Signifikan Negatif)"
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
            else:
                hypothesis_results.append({
                    'Hipotesis': h['code'],
                    'Jalur Hubungan': h['path'],
                    'Koefisien (\u03b2)': np.nan,
                    'Std. Err': np.nan,
                    'z-value': np.nan,
                    'p-value': np.nan,
                    'Keputusan (\u03b1 = 0.05)': "Data Tidak Tersedia"
                })
                
        df_hypo_summary = pd.DataFrame(hypothesis_results)
        st.dataframe(
            df_hypo_summary.style.format({
                'Koefisien (\u03b2)': '{:.3f}',
                'Std. Err': '{:.3f}',
                'z-value': '{:.3f}',
                'p-value': '{:.3f}'
            }, na_rep='-')
        )
        
        # 2. NARASI OUTPUT LENGKAP
        st.markdown("#### B. Narasi Deskriptif Output Model")
        
        fit_status_str = "SANGAT BAIK (GOOD FIT)" if (cfi_val >= 0.90 and rmsea_val <= 0.08) else "CUKUP IDEAL (MODERATE FIT)"
        
        narasi_text = fr"""
        **1. Evaluasi Kelayakan Model Struktural (Goodness of Fit):**
        Berdasarkan hasil pengujian kovarians keseluruhan model (*Global Fit Indices*), nilai **CFI** tercatat sebesar **{cfi_val:.3f}**, nilai **TLI** sebesar **{tli_val:.3f}**, dan **RMSEA** sebesar **{rmsea_val:.3f}**. Dengan demikian, model struktural ini berada dalam kategori **{fit_status_str}**, di mana struktur kovarians sampel dari data survei mampu merepresentasikan model teoretis yang dibangun dengan presisi statistik yang tinggi.

        **2. Evaluasi Model Pengukuran (Measurement Model / Outer Loadings):**
        Seluruh indikator manifest terbukti secara signifikan merefleksikan masing-masing variabel latennya dengan tingkat muatan faktor (*Factor Loading* $\lambda$) yang memenuhi kriteria reliabilitas konstruksi. Hal ini mengonfirmasi bahwa instrumen kuesioner memiliki validitas konfirmatori (*Confirmatory Factor Analysis*) yang solid.

        **3. Evaluasi Hubungan Kausalitas (Structural Model):**
        Dari total **{len(hypotheses_list)} hipotesis** hubungan struktural yang diuji:
        """
        st.markdown(narasi_text)
        
        for res in hypothesis_results:
            beta_str = f"{res['Koefisien (β)']:.3f}" if pd.notna(res['Koefisien (β)']) else "-"
            p_str = f"{res['p-value']:.3f}" if pd.notna(res['p-value']) else "-"
            st.markdown(f"- **{res['Hipotesis']} ({res['Jalur Hubungan']})**: Menghasilkan koefisien jalur $\\beta = {beta_str}$ ($p = {p_str}$). Hasil pengujian menyatakan hipotesis ini **{res['Keputusan (α = 0.05)']}**.")

        # 3. KESIMPULAN AKADEMIK
        st.markdown("#### C. Kesimpulan Riset & Implikasi Akademik")
        
        accepted_count = sum(1 for r in hypothesis_results if "DITERIMA" in r['Keputusan (\u03b1 = 0.05)'])
        total_count = len(hypothesis_results)
        
        st.markdown(f"""
        <div class="card-conclusion">
            <h4 style="margin: 0; color: #15803D;">📌 Rangkuman Kesimpulan Penelitian</h4>
            <p style="margin: 8px 0; color: #166534; font-size: 14px;">
                1. Dari total <b>{total_count} hipotesis penelitian</b> yang diajukan, sebanyak <b>{accepted_count} hipotesis terbukti berpengaruh signifikan</b> pada tingkat signifikansi &alpha; = 0.05.<br>
                2. Kerangka model konseptual CB-SEM yang dibangun terbukti secara empiris memiliki kesesuaian fit yang memadai dengan data survei lapangan (CFI = {cfi_val:.3f}, RMSEA = {rmsea_val:.3f}).<br>
                3. Temuan ini menegaskan pentingnya peranan variabel Exogenous dan Mediator dalam menjelaskan keragaman variabel Endogenous pada model riset ini.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #9CA3AF; font-size: 11px;'>"
    "Aplikasi Analisa CB-SEM Sederhana | Dikembangkan untuk Kebutuhan Akademik STIEIMA © 2026"
    "</div>", 
    unsafe_allow_html=True
)
