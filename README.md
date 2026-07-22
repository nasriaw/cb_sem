# 📊 Analisis Multivariate Metode Covariance-Based SEM (CB-SEM) v2.0
> **Platform Interaktif Analisis Structural Equation Modeling (SEM) Berbasis Python & Streamlit**

Developed for Academic and Research Purposes at **STIE Indonesia Malang (STIEIMA)**.

---

## 📌 Identitas Penyusun
* **Penyusun**: Ir. M Nasri AW, M.Eng.Sc, M.Kom | Dosen Aplikom STatistika
* **Institusi**: STIE Indonesia Malang (STIEIMA)
* **Lisensi**: Open Source / Academic Free Use

---

## 🎯 Gambaran Umum Aplikasi
**SEM-IMA** adalah aplikasi web interaktif yang dikembangkan menggunakan **Streamlit** dan pustaka **`semopy`** untuk memfasilitasi pengolahan data **Structural Equation Modeling (SEM)** secara cepat, otomatis, dan akurat. 

Aplikasi ini secara otomatis merakit sintaks pemodelan, menggenerasi diagram jalur (*path diagram*), menghitung koefisien jalur struktural, muatan faktor (*loading factors*), serta menampilkan indikator kelayakan model (*Goodness-of-Fit*) secara *real-time*.

---

## 🔬 Metodologi: CB-SEM vs PLS-SEM

Aplikasi ini menggunakan pendekatan **CB-SEM (Covariance-Based Structural Equation Modeling)** melalui *engine* `semopy`. 

### Mengapa CB-SEM?
CB-SEM bertujuan untuk mengonfirmasi model teoritis dengan menguji seberapa baik matriks kovarians yang diperkirakan oleh model dapat mendekati matriks kovarians dari data sampel.

### Tabel Perbandingan Metodologis:

| Parameter | CB-SEM (Digunakan di Aplikasi Ini) | PLS-SEM (Partial Least Squares) |
| :--- | :--- | :--- |
| **Tujuan Analisis** | Konfirmasi Teori (*Confirmatory*) | Prediksi / Eksplorasi Teori (*Exploratory*) |
| **Pustaka Python** | `semopy` | `csemi`, `plspm` |
| **Software Pembanding** | AMOS, LISREL, EQS, R (`lavaan`) | SmartPLS, WarpPLS |
| **Metrik Kelayakan** | CFI, TLI, RMSEA, Chi-Square | $R^2$, $f^2$, $Q^2$, HTMT, Bootstrapping |
| **Asumsi Data** | Membutuhkan distribusi normal multivariat | Bebas distribusi (*non-parametric*) |
| **Ukuran Sampel** | Disarankan sampel sedang–besar ($N \ge 100-200$) | Fleksibel untuk sampel kecil ($N < 100$) |

---

## 📐 Standar Evaluasi Kelayakan Model (Goodness-of-Fit)

Hasil analisis pada menu **Hasil Estimasi & Fit** dapat dievaluasi menggunakan ambang batas (*cut-off value*) standar berikut:

| Indikator Fit | Nama Metrik | Cut-off Value (Kriteria Ideal) | Keterangan |
| :--- | :--- | :--- | :--- |
| **CFI** | *Comparative Fit Index* | $\ge 0.90$ (Sangat Baik $\ge 0.95$) | Mengukur perbandingan model yang diestimasi dengan model nol. |
| **TLI** | *Tucker-Lewis Index* | $\ge 0.90$ (Sangat Baik $\ge 0.95$) | Mengukur indeks kesesuaian relatif yang mengoreksi kompleksitas model. |
| **RMSEA** | *Root Mean Square Error of Approximation* | $\le 0.08$ (Sangat Baik $\le 0.05$) | Mengukur tingkat kesalahan estimasi model terhadap populasi. |

---

## 🚀 Fitur Utama Aplikasi

1. **Konfigurasi Variabel Laten Dinamis**:
   * Bebas mengatur jumlah Variabel Bebas/Exogenous ($X$), Mediator ($M$), dan Terikat/Endogenous ($Y$).
   * Bebas menentukan jumlah indikator terukur (*manifest variables*) untuk setiap konstruk laten.
2. **Dynamic Template Data Generator**:
   * Dapat mengunduh template file CSV acuan yang secara otomatis disesuaikan dengan konfigurasi variabel yang dipilih pengguna.
3. **Visualisasi Diagram Jalur (Path Diagram)**:
   * Diagram interaktif berbasis `matplotlib` yang menggambarkan hubungan antara variabel laten (lingkaran) dan indikatornya (kotak).
4. **Pembersihan Data Otomatis & Pemformatan Rapi**:
   * Dilengkapi penanganan *error handling* (`pd.to_numeric`) untuk mengantisipasi nilai string/terkunci dari `semopy`.
5. **Output Hasil Lengkap**:
   * Koefisien Jalur Struktural (Regresi) lengkap dengan nilai $z$-value dan $p$-value.
   * *Factor Loadings* untuk model pengukuran (*Measurement Model*).
   * Dashboard *Goodness of Fit* interaktif.

---

## 💻 Petunjuk Instalasi & Penggunaan Lokal

### 1. Prasyarat System
Pastikan Python 3.8 atau versi yang lebih baru telah terpasang di komputer Anda.

### 2. Instalasi Dependensi
Buka Terminal / Command Prompt, lalu jalankan perintah berikut:

```bash
pip install streamlit semopy pandas numpy matplotlib
```

Atau jika menggunakan file `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Menjalankan Aplikasi
Jalankan aplikasi Streamlit dengan perintah:

```bash
streamlit run aplikasi_analisa_sem.py
```

Browser default Anda akan terbuka secara otomatis di alamat `http://localhost:8501`.

---

## 📄 Struktur File Proyek

```
.
├── aplikasi_analisa_sem.py   # Kode utama aplikasi web Streamlit
├── requirements.txt          # Daftar dependensi modul Python
└── README.md                 # Dokumentasi lengkap aplikasi
```

---

## ✉️ Kontak & Dukungan
Untuk pertanyaan akademik, diskusi metodologi, atau saran pengembangan aplikasi, silakan menghubungi:
* **Penyusun**: Ir. M Nasri AW, M.Eng.Sc, M.Kom
* **Institusi**: STIE Indonesia Malang (STIEIMA)
