# 📊 Aplikasi SEM-IMA: Analisis Structural Equation Modeling (CB-SEM)
> **Platform Interaktif Analisis Structural Equation Modeling (CB-SEM) Berbasis Python & Streamlit**

Developed for Academic and Research Purposes at **STIE Indonesia Malang (STIEIMA)**.

---

## 📌 Identitas Penyusun
* **Penyusun**: Ir. M Nasri AW, M.Eng.Sc, M.Kom | Dosen Aplikom Statistik
* **Institusi**: STIE Indonesia Malang (STIEIMA)
* **Lisensi**: Open Source / Academic Free Use

---

## 🎯 Gambaran Umum Aplikasi
**SEM-IMA** adalah platform web interaktif berbasis **Streamlit** dan pustaka **`semopy`** yang dirancang untuk mengolah data **Covariance-Based Structural Equation Modeling (CB-SEM)** secara otomatis, cepat, dan presisi. 

Aplikasi ini tidak hanya merakit sintaks pemodelan dan menggenerasi diagram jalur (*path diagram*) beserta kotak indikatornya, melainkan juga secara otomatis **merumuskan hipotesis penelitian**, melakukan **pengujian hipotesis dinamis**, menyusun **narasi interpretasi output akademik Bab IV**, menyediakan **Viewer / Preview PDF Interaktif**, dan mengekspor dokumen laporan riset lengkap secara *real-time*.

---

## 🔬 Metodologi: CB-SEM vs PLS-SEM

Aplikasi ini beroperasi menggunakan pendekatan **CB-SEM (Covariance-Based Structural Equation Modeling)** dengan *engine* `semopy`.

### Mengapa CB-SEM?
CB-SEM bertujuan untuk mengonfirmasi model teoritis (*confirmatory*) dengan menguji seberapa dekat matriks kovarians yang diestimasi oleh model terhadap matriks kovarians sampel data riil.

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

Hasil analisis kelayakan model (*Global Fit Indices*) dievaluasi menggunakan kriteria ambang batas (*cut-off value*) baku berikut:

| Indikator Fit | Nama Metrik | Cut-off Value (Kriteria Ideal) | Keterangan Evaluasi |
| :--- | :--- | :--- | :--- |
| **CFI** | *Comparative Fit Index* | $\ge 0.90$ (Sangat Baik $\ge 0.95$) | Perbandingan model estimasi terhadap model nol. |
| **TLI** | *Tucker-Lewis Index* | $\ge 0.90$ (Sangat Baik $\ge 0.95$) | Indeks kesesuaian relatif terkoreksi kompleksitas. |
| **RMSEA** | *Root Mean Square Error of Approximation* | $\le 0.08$ (Sangat Baik $\le 0.05$) | Tingkat kesalahan estimasi model ke populasi. |

---

## 🚀 Modul & Fitur Alur Kerja Akademik (7 Tab Terpadu)

Aplikasi ini menyusun alur kerja analisis riset ke dalam **7 Tab Utama** yang tersusun secara sistematis:

### 1. ⚙️ Konfigurasi Sidebar & Dropdown Panduan
* **Panduan Penggunaan**: Dropdown interaktif (`st.expander`) panduan alur penggunaan aplikasi.
* **Konfigurasi Variabel Laten**: Slider dinamis untuk menentukan jumlah Exogenous ($X$), Mediator ($M$), dan Endogenous ($Y$).
* **Konfigurasi Indikator**: Pengaturan jumlah indikator per variabel laten.
* **Template CSV Generator**: Otomatisasi pengunduhan template data CSV yang presisi sesuai konfigurasi input.

### 2. 📊 Tab 1: Head & Deskripsi Data
* **Data Head Preview**: Menampilkan 10 baris pertama data sampel survei.
* **Statistik Deskriptif**: Menghitung *count, mean, std. deviasi, min, max* untuk setiap indikator.
* **Matriks Korelasi**: Visualisasi matriks korelasi antar-indikator dengan *gradient heatmap*.

### 3. 🎯 Tab 2: Perumusan Hipotesis
* **Autogenerate Hipotesis**: Perumusan otomatis hipotesis kausalitas ($H_1, H_2, \dots$) melingkupi jalur langsung maupun mediasi.

### 4. 📌 Tab 3: Sintaks Model `semopy`
* **Automated Lavaan Syntax**: Generasi sintaks konfirmatori (`=~` untuk model pengukuran dan `~` untuk model struktural).

### 5. 🎨 Tab 4: Diagram Jalur (Path Diagram)
* **Visualisasi Komplit**: Render diagram interaktif berbasis `matplotlib` yang menampilkan lingkaran variabel laten, panah kausalitas, serta **kotak indikator terukur ($x, m, y$)** secara presisi sesuai jumlah indikator data.

### 6. 🔑 Tab 5: Hasil Estimasi & Fit
* **Structural Path Coefficients**: Nilai koefisien regresi ($\beta$), *Std. Error*, $z$-value, dan $p$-value.
* **Measurement Outer Loadings**: Nilai *factor loading* ($\lambda$) untuk menguji validitas indikator terukur.
* **Goodness-of-Fit Dashboard**: Metric cards evaluasi kesesuaian model (CFI, TLI, RMSEA).

### 7. 📝 Tab 6: Pengujian Hipotesis
* **Tabel Uji Hipotesis**: Ringkasan statistik keputusan hipotesis (**Diterima / Ditolak** pada $\alpha = 0.05$).
* **Rangkuman Ringkas**: *Card summary* total hipotesis yang terbukti signifikan.

### 8. 📄 Tab 7: Hasil Analisa Lengkap & Ekspor PDF
* **Sistematika Bab IV Baku**: Draf laporan riset ilmiah terurut secara sistematis:
  1. *4.1 Tinjauan Data & Deskripsi Statistik*
  2. *4.2 Sintaks & Diagram Jalur*
  3. *4.3 Penyusunan Hipotesis Penelitian*
  4. *4.4 Hasil Analisis & Pembahasan*
  5. *4.5 Kesimpulan Hasil Penelitian*
* **Interactive PDF Viewer**: *Embedded IFrame PDF Previewer* yang memungkinkan peneliti memeriksa dokumen laporan secara langsung di browser sebelum diunduh.
* **Multi-Format Export**: Tombol unduh laporan lengkap versi **.PDF**, **.TXT**, dan **.CSV** (rekapitulasi tabel hipotesis).

---

## 💻 Petunjuk Instalasi & Penggunaan Lokal

### 1. Prasyarat Sistem
Pastikan Python 3.8 atau versi yang lebih baru telah terpasang di komputer Anda.

### 2. Instalasi Dependensi Modul
Buka Terminal / Command Prompt, lalu jalankan perintah berikut:

```bash
pip install streamlit semopy pandas numpy matplotlib fpdf
