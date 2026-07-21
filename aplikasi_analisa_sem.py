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
    page_title="Analisa Covariance Based Structural Equation Modeling (CB-SEM) ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk memperindah tampilan dashboard
st.markdown("""
<style>
    .main-header {
        font-size: 36px;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 16px;
        color: #4B5563;
        margin-bottom: 25px;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    .card {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #2563EB;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header Sidebar
st.sidebar.markdown("""
<div style="text-align: center; padding-bottom: 15px;">
    <h1 style="color: #1E3A8A; margin-bottom: 0;">📊 Analisa Struktural Equation Modeling (SEM), berbasis CB-SEM (Covariance-Based SEM). Menggunakan SEMOPY Python</h1>
    <p style="font-size: 14px; color: #6B7280; font-weight: bold;">CB-SEM menggunakan data cukup besar (N>=200). Pelajari kapan menggunakan Covariance Based (CB-SEM) atau Partial Least Squares (PLS-SEM). Pelajari Panduan Cara Menggunakan Aplikasi</p>
</div>
""", unsafe_allow_html=True)

# Identitas Penyusun
st.sidebar.markdown("""
<div style="background-color: #EFF6FF; border: 1px solid #BFDBFE; padding: 12px; border-radius: 8px; margin-bottom: 20px;">
    <p style="margin: 0; font-size: 16px; color: #1E40AF; font-weight: bold; text-transform: uppercase;">Penyusun:</p>
    <p style="margin: 0; font-size: 16px; color: #1E3A8A; font-weight: 800;">M Nasri AW | Dosen STIEIMA</p>
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
    
    # Generate latent scores
    latents = {}
    # Generate X latents
    for i in range(1, num_x + 1):
        latents[f"X{i}"] = np.random.normal(5.0, 1.0, n_samples)
        
    # Generate M latents
    for i in range(1, num_m + 1):
        # M dipengaruhi oleh kombinasi semua X
        base_m = np.zeros(n_samples)
        for x_key in [k for k in latents.keys() if k.startswith("X")]:
            base_m += 0.5 * latents[x_key]
        latents[f"M{i}"] = base_m + np.random.normal(0, 0.8, n_samples)
        
    # Generate Y latents
    for i in range(1, num_y + 1):
        # Y dipengaruhi oleh kombinasi semua X dan M
        base_y = np.zeros(n_samples)
        for x_key in [k for k in latents.keys() if k.startswith("X")]:
            base_y += 0.25 * latents[x_key]
        for m_key in [k for k in latents.keys() if k.startswith("M")]:
            base_y += 0.5 * latents[m_key]
        latents[f"Y{i}"] = base_y + np.random.normal(0, 0.8, n_samples)
        
    # Generate Indicators based on config
    for latent_name, n_ind in config.items():
        prefix = latent_name.lower()
        latent_val = latents[latent_name]
        for idx in range(1, n_ind + 1):
            noise = np.random.normal(0, 0.6, n_samples)
            loading = 0.8 if idx == 1 else (0.7 if idx == 2 else 0.85)
            raw = loading * latent_val + noise
            # Standard Likert Scale 1-5
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


st.markdown('<div class="main-header">Platform Interaktif untuk Menghitung Estimasi Parameter dan Jalur Struktural Variabel Laten</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Harap membaca panduan dan menyiapkan data input (Upload) format *.csv dengan benar atau menggunakan Data Simulasi Otomatis</div>', unsafe_allow_html=True)

# Panduan Alur Kerja Aplikasi
with st.expander("📖 Panduan Cara Menggunakan Aplikasi", expanded=False):
    st.markdown("""
    1. **Atur jumlah variabel laten** ($X$, $M$, $Y$) beserta jumlah indikator masing-masing pada **Sidebar sebelah kiri**.
    2. Tekan tombol **Download Template CSV Sesuai Input** untuk mengunduh struktur data kosong yang sudah disesuaikan.
    3. Masukkan data survei riil Anda ke template CSV tersebut, atau gunakan **data simulasi bawaan** langsung untuk menguji coba.
    4. Unggah file CSV Anda pada menu unggah di bawah ini untuk melihat estimasi model secara real-time.
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

# Memproses data berdasarkan opsi yang dipilih
if data_option == "Gunakan Data Unggahan (CSV)":
    if uploaded_file is not None:
        try:
            df_analysis = pd.read_csv(uploaded_file)
            st.success("✅ File CSV berhasil diunggah!")
        except Exception as e:
            st.error(f"Gagal membaca file CSV: {e}")
            df_analysis = template_df
            st.info("Beralih sementara menggunakan data simulasi karena error unggahan.")
    else:
        st.warning("⚠️ Silakan unggah file CSV Anda terlebih dahulu. Sementara kami tampilkan data simulasi di bawah.")
        df_analysis = template_df
else:
    df_analysis = template_df
    st.info("ℹ️ Saat ini menggunakan data simulasi otomatis sesuai konfigurasi parameter Anda.")

# Tampilkan preview data
with st.expander("📊 Pratinjau Dataset & Korelasi (10 Baris Pertama)", expanded=False):
    st.dataframe(df_analysis.head(10))
    st.write("Matriks Korelasi Antar-Indikator:")
    st.dataframe(df_analysis.corr().style.background_gradient(cmap='coolwarm').format("{:.2f}"))


# Merakit deskripsi model semopy
model_desc_lines = []

model_desc_lines.append("# Measurement Model")
for latent_name, n_ind in indicators_config.items():
    prefix = latent_name.lower()
    indicators = [f"{prefix}{idx}" for idx in range(1, n_ind + 1)]
    model_desc_lines.append(f"{latent_name} =~ {' + '.join(indicators)}")

model_desc_lines.append("\n# Structural Model")
# M dipengaruhi oleh semua X
if num_m > 0:
    x_list = [f"X{i}" for i in range(1, num_x + 1)]
    for j in range(1, num_m + 1):
        model_desc_lines.append(f"M{j} ~ {' + '.join(x_list)}")

# Y dipengaruhi oleh semua X dan M
for k in range(1, num_y + 1):
    predictors = [f"X{i}" for i in range(1, num_x + 1)]
    if num_m > 0:
        predictors += [f"M{j}" for j in range(1, num_m + 1)]
    model_desc_lines.append(f"Y{k} ~ {' + '.join(predictors)}")

model_syntax = "\n".join(model_desc_lines)


def draw_sem_diagram_custom(num_x, num_m, num_y, indicators_config):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    # Posisi koordinat x untuk tiap lapisan
    x_pos_exog = 1.0
    x_pos_med = 3.0
    x_pos_endo = 5.0
    
    # Simpan titik koordinat variabel laten
    latent_positions = {}
    
    # 1. Gambar Exogenous Latent X
    y_starts_x = np.linspace(5.0, 1.0, num_x) if num_x > 1 else [3.0]
    for idx, y_val in enumerate(y_starts_x, 1):
        name = f"X{idx}"
        latent_positions[name] = (x_pos_exog, y_val)
        # Gambar Lingkaran Laten
        circle = plt.Circle((x_pos_exog, y_val), 0.35, color='#3B82F6', alpha=0.85, zorder=3)
        ax.add_patch(circle)
        ax.text(x_pos_exog, y_val, name, color='white', ha='center', va='center', weight='bold', fontsize=12, zorder=4)
        
        # Gambar Kotak Indikator (di sebelah kiri X)
        n_ind = indicators_config[name]
        y_inds = np.linspace(y_val + 0.6, y_val - 0.6, n_ind)
        for idx_ind, y_ind in enumerate(y_inds, 1):
            rect = plt.Rectangle((x_pos_exog - 1.0, y_ind - 0.15), 0.4, 0.3, color='#DBEAFE', ec='#2563EB', zorder=2)
            ax.add_patch(rect)
            ax.text(x_pos_exog - 0.8, y_ind, f"x{idx}{idx_ind}", ha='center', va='center', fontsize=8, zorder=3)
            # Garis penghubung loading factor
            ax.annotate('', xy=(x_pos_exog - 0.6, y_ind), xytext=(x_pos_exog - 0.3, y_val),
                        arrowprops=dict(arrowstyle="<-", color='#2563EB', lw=1, shrinkA=0, shrinkB=5))

    # 2. Gambar Mediator Latent M (jika ada)
    if num_m > 0:
        y_starts_m = np.linspace(5.0, 1.0, num_m) if num_m > 1 else [3.0]
        for idx, y_val in enumerate(y_starts_m, 1):
            name = f"M{idx}"
            latent_positions[name] = (x_pos_med, y_val)
            # Gambar Lingkaran Laten
            circle = plt.Circle((x_pos_med, y_val), 0.35, color='#F59E0B', alpha=0.85, zorder=3)
            ax.add_patch(circle)
            ax.text(x_pos_med, y_val, name, color='white', ha='center', va='center', weight='bold', fontsize=12, zorder=4)
            
            # Gambar Kotak Indikator (di atas atau bawah M)
            n_ind = indicators_config[name]
            x_inds = np.linspace(x_pos_med - 0.4, x_pos_med + 0.4, n_ind)
            for idx_ind, x_ind in enumerate(x_inds, 1):
                rect = plt.Rectangle((x_ind - 0.15, y_val + 0.6), 0.3, 0.25, color='#FEF3C7', ec='#D97706', zorder=2)
                ax.add_patch(rect)
                ax.text(x_ind, y_val + 0.725, f"m{idx}{idx_ind}", ha='center', va='center', fontsize=8, zorder=3)
                # Garis penghubung loading factor
                ax.annotate('', xy=(x_ind, y_val + 0.6), xytext=(x_pos_med, y_val + 0.3),
                            arrowprops=dict(arrowstyle="<-", color='#D97706', lw=1, shrinkA=0, shrinkB=5))

    # 3. Gambar Endogenous Latent Y
    y_starts_y = np.linspace(5.0, 1.0, num_y) if num_y > 1 else [3.0]
    for idx, y_val in enumerate(y_starts_y, 1):
        name = f"Y{idx}"
        latent_positions[name] = (x_pos_endo, y_val)
        # Gambar Lingkaran Laten
        circle = plt.Circle((x_pos_endo, y_val), 0.35, color='#10B981', alpha=0.85, zorder=3)
        ax.add_patch(circle)
        ax.text(x_pos_endo, y_val, name, color='white', ha='center', va='center', weight='bold', fontsize=12, zorder=4)
        
        # Gambar Kotak Indikator (di sebelah kanan Y)
        n_ind = indicators_config[name]
        y_inds = np.linspace(y_val + 0.6, y_val - 0.6, n_ind)
        for idx_ind, y_ind in enumerate(y_inds, 1):
            rect = plt.Rectangle((x_pos_endo + 0.6, y_ind - 0.15), 0.4, 0.3, color='#D1FAE5', ec='#059669', zorder=2)
            ax.add_patch(rect)
            ax.text(x_pos_endo + 0.8, y_ind, f"y{idx}{idx_ind}", ha='center', va='center', fontsize=8, zorder=3)
            # Garis penghubung loading factor
            ax.annotate('', xy=(x_pos_endo + 0.6, y_ind), xytext=(x_pos_endo + 0.3, y_val),
                        arrowprops=dict(arrowstyle="<-", color='#059669', lw=1, shrinkA=0, shrinkB=5))

    # 4. Gambar Garis Hubungan Struktural (Jalur Koefisien)
    # Hubungan X -> M
    if num_m > 0:
        for x_name in [k for k in latent_positions.keys() if k.startswith("X")]:
            for m_name in [k for k in latent_positions.keys() if k.startswith("M")]:
                ax.annotate('', xy=latent_positions[m_name], xytext=latent_positions[x_name],
                            arrowprops=dict(arrowstyle="->", color='#374151', lw=2, shrinkA=38, shrinkB=38))
                
        # Hubungan M -> Y
        for m_name in [k for k in latent_positions.keys() if k.startswith("M")]:
            for y_name in [k for k in latent_positions.keys() if k.startswith("Y")]:
                ax.annotate('', xy=latent_positions[y_name], xytext=latent_positions[m_name],
                            arrowprops=dict(arrowstyle="->", color='#374151', lw=2, shrinkA=38, shrinkB=38))

    # Hubungan Langsung X -> Y
    for x_name in [k for k in latent_positions.keys() if k.startswith("X")]:
        for y_name in [k for k in latent_positions.keys() if k.startswith("Y")]:
            # Jika ada mediator, buat jalurnya agak melengkung ke bawah agar tidak bertumpuk
            connectionstyle = "arc3,rad=-0.15" if num_m > 0 else "arc3,rad=0"
            ax.annotate('', xy=latent_positions[y_name], xytext=latent_positions[x_name],
                        arrowprops=dict(arrowstyle="->", color='#6B7280', lw=1.5, ls='--', 
                                        connectionstyle=connectionstyle, shrinkA=38, shrinkB=38))

    plt.xlim(-0.5, 6.5)
    plt.ylim(0.0, 6.5)
    return fig


tab_desc, tab_diag, tab_output = st.tabs(["📌 Sintaks Model", "🎨 Visualisasi Diagram Jalur", "🔑 Hasil Estimasi & Fit"])

with tab_desc:
    st.markdown("### Kode Sintaks Konfigurasi SEM (`semopy`)")
    st.write("Sintaks ini dibuat secara otomatis berdasarkan konfigurasi jumlah variabel laten di sidebar.")
    st.code(model_syntax, language="text")
    st.info("💡 Karakter `=~` menunjukkan hubungan pengukuran (Measurement) sedangkan `~` melambangkan hubungan struktural (Regresi).")

with tab_diag:
    st.markdown("### Diagram Jalur Konstruksi Model SEM")
    st.write("Skema hubungan logis antara indikator terukur (kotak) dengan konstruk laten (lingkaran):")
    
    # Render diagram
    fig_sem = draw_sem_diagram_custom(num_x, num_m, num_y, indicators_config)
    st.pyplot(fig_sem)

with tab_output:
    st.markdown("### Output Hasil Analisis Statistik")
    
    if not SEMOPY_AVAILABLE:
        st.error("❌ Pustaka `semopy` belum terpasang di sistem lingkungan kerja Anda.")
        st.info("Silakan jalankan instalasi terlebih dahulu dengan perintah: `pip install semopy` di terminal Anda.")
    else:
        # Menjalankan fitting model semopy
        try:
            with st.spinner("Sedang memproses perhitungan model SEM..."):
                # Inisialisasi Model
                sem_model = Model(model_syntax)
                # Proses Fitting menggunakan dataset
                sem_model.fit(df_analysis)
                # Menghasilkan estimasi parameter
                estimates_df = sem_model.inspect()
                
                # --- [FIX UTAMA] KONVERSI STRING/CHAR NON-NUMERIK MENJADI FLOAT/NaN ---
                num_cols = ['Estimate', 'Std. Err', 'z-value', 'p-value']
                for col in num_cols:
                    if col in estimates_df.columns:
                        estimates_df[col] = pd.to_numeric(estimates_df[col], errors='coerce')
                
                # Kalkulasi statistik kelayakan model
                fit_indices = calc_stats(sem_model)
                
            st.success("🎉 Analisis model SEM berhasil diselesaikan dengan sukses!")
            
            # Tampilan hasil koefisien regresi
            st.markdown("#### 1. Koefisien Jalur Struktural (Path Coefficients)")
            structural_df = estimates_df[estimates_df['op'] == '~'].copy()
            if not structural_df.empty:
                st.dataframe(
                    structural_df[['lval', 'rval', 'Estimate', 'Std. Err', 'z-value', 'p-value']]
                    .rename(columns={'lval': 'Variabel Dependen', 'rval': 'Variabel Independen', 'Estimate': 'Estimasi Koefisien'})
                    .style.highlight_between(left=0.0, right=0.05, subset=['p-value'], color='#D1FAE5')
                    .format({'Estimasi Koefisien': '{:.3f}', 'Std. Err': '{:.3f}', 'z-value': '{:.3f}', 'p-value': '{:.3f}'}, na_rep='-')
                )
            else:
                st.write("Tidak ada jalur struktural regresi terdefinisi.")
                
            # Tampilan hasil Measurement Model
            st.markdown("#### 2. Muatan Faktor Pengukuran (Measurement Loadings)")
            measurement_df = estimates_df[estimates_df['op'] == '=~'].copy()
            st.dataframe(
                measurement_df[['lval', 'rval', 'Estimate', 'Std. Err', 'z-value', 'p-value']]
                .rename(columns={'lval': 'Variabel Laten', 'rval': 'Indikator Manifest', 'Estimate': 'Factor Loading'})
                .style.format({'Factor Loading': '{:.3f}', 'Std. Err': '{:.3f}', 'z-value': '{:.3f}', 'p-value': '{:.3f}'}, na_rep='-')
            )
            
            # Tampilan Kelayakan Model
            st.markdown("#### 3. Indikator Kelayakan Model (Goodness of Fit)")
            col_fit1, col_fit2, col_fit3 = st.columns(3)
            
            # Mengambil metrik utama jika tersedia
            cfi_val = float(fit_indices['CFI'].values[0]) if 'CFI' in fit_indices.columns else 0.0
            tli_val = float(fit_indices['TLI'].values[0]) if 'TLI' in fit_indices.columns else 0.0
            rmsea_val = float(fit_indices['RMSEA'].values[0]) if 'RMSEA' in fit_indices.columns else 0.0
            
            with col_fit1:
                st.metric(
                    label="Comparative Fit Index (CFI)", 
                    value=f"{cfi_val:.3f}", 
                    delta="Ideal (>= 0.90)" if cfi_val >= 0.90 else "Kurang Ideal (< 0.90)",
                    delta_color="normal" if cfi_val >= 0.90 else "inverse"
                )
            with col_fit2:
                st.metric(
                    label="Tucker-Lewis Index (TLI)", 
                    value=f"{tli_val:.3f}", 
                    delta="Ideal (>= 0.90)" if tli_val >= 0.90 else "Kurang Ideal (< 0.90)",
                    delta_color="normal" if tli_val >= 0.90 else "inverse"
                )
            with col_fit3:
                st.metric(
                    label="RMSEA Error Rate", 
                    value=f"{rmsea_val:.3f}", 
                    delta="Ideal (<= 0.08)" if rmsea_val <= 0.08 else "Kurang Ideal (> 0.08)",
                    delta_color="inverse" if rmsea_val <= 0.08 else "normal"
                )
                
            # Menampilkan detail metrik lainnya
            with st.expander("Metrik Statistik Kelayakan Model Lengkap:", expanded=False):
                st.dataframe(fit_indices.T.rename(columns={0: 'Nilai Statistik'}))
                
        except Exception as err:
            st.error(f"Terjadi kesalahan saat fitting model: {err}")
            st.info("Silakan periksa kembali apakah nama kolom di file CSV Anda sudah sesuai persis dengan sintaks indikator.")

# Footer Halaman
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #9CA3AF; font-size: 11px;'>"
    "Aplikasi Template Analisa SEM Sederhana | Dikembangkan untuk Kebutuhan Akademik STIEIMA © 2026"
    "</div>", 
    unsafe_allow_html=True
)