# fotoboot-project

<div align="center">

# FotoBoot Project

**FotoBoot adalah platform modern untuk mengelola foto secara cepat, rapi, dan efisien.**  
Project ini dirancang untuk membantu pengguna dalam mengunggah, menyimpan, mengorganisasi, dan menampilkan foto dalam satu sistem yang sederhana namun powerful.

</div>

---

## ✨ Tentang Project

FotoBoot Project adalah aplikasi photobooth berbasis Python yang menggunakan kamera laptop untuk mengambil foto, menyusun hasilnya menjadi photo strip, dan menyimpannya ke dalam folder lokal. Project ini cocok untuk penggunaan rumahan, event kecil, atau sebagai fondasi pengembangan aplikasi photobooth yang lebih profesional.

Aplikasi ini dibuat dengan antarmuka **Tkinter** dan pemrosesan gambar menggunakan **OpenCV** serta **Pillow**. Dengan tampilan yang sederhana namun interaktif, pengguna bisa memilih slot foto, mengganti template, mengatur nama event, dan menyimpan hasil strip foto dengan mudah.

---

## 🚀 Fitur Utama

- Menampilkan live camera preview.
- Mengambil 3 foto dalam satu sesi.
- Menampilkan countdown sebelum foto diambil.
- Memilih slot foto untuk retake.
- Mengganti template tampilan strip.
- Menambahkan nama event secara dinamis.
- Menyimpan hasil photo strip ke folder `strip/`.
- Preview hasil akhir sebelum disimpan.

---

## 🎨 Template yang Tersedia

Project ini sudah menyediakan beberapa template strip foto:

- **Clean** — tampilan minimalis dan bersih.
- **Dark** — tampilan gelap yang elegan.
- **Warm** — nuansa hangat dan lembut.

Template ini membuat hasil photo strip terlihat lebih menarik dan bisa disesuaikan dengan tema acara.

---

## 🧩 Penjelasan Kode

### 1. Setup Kamera
Bagian awal script membuka kamera menggunakan `cv2.VideoCapture(0)`.  
Kalau kamera tidak bisa dibuka dengan mode DirectShow, script mencoba lagi dengan mode default. Jika tetap gagal, program akan berhenti dengan error karena kamera adalah komponen utama aplikasi.

### 2. Struktur Folder
Folder `strip/` dibuat otomatis untuk menyimpan hasil foto strip.  
Ini memastikan file hasil capture tidak bercampur dengan file utama project.

### 3. Template Desain
Variabel `TEMPLATES` berisi beberapa gaya tampilan strip seperti `clean`, `dark`, dan `warm`.  
Setiap template punya warna background, warna judul, warna footer, dan warna border yang berbeda.

### 4. Fungsi Konversi Gambar
Fungsi `cv_to_tk()` mengubah frame OpenCV menjadi format yang bisa ditampilkan di Tkinter.  
Fungsi `capture_frame()` mengambil gambar dari kamera dan membaliknya secara horizontal agar hasil tampilan lebih natural seperti cermin.

### 5. Efek Frame Foto
Fungsi `add_frame()` menambahkan border dekoratif pada foto.  
Ini membuat hasil foto terlihat lebih profesional dan seperti photo booth sungguhan.

### 6. Thumbnail Preview
Fungsi `make_thumb()` membuat versi kecil dari foto untuk ditampilkan pada slot-slot preview.  
Kalau slot masih kosong, aplikasi akan menampilkan placeholder bertuliskan “Empty”.

### 7. Membuat Photo Strip
Fungsi `make_strip()` adalah inti dari project ini.  
Di sini tiga foto digabung menjadi satu strip vertikal lengkap dengan nama event, tanggal, template aktif, border, dan pesan penutup.

### 8. Countdown Animasi
Fungsi `show_countdown()` menampilkan jendela fullscreen dengan hitungan mundur 3, 2, 1 sebelum kamera mengambil gambar.  
Efek ini membuat pengalaman capture terasa lebih hidup dan interaktif.

### 9. Update UI
Fungsi `update_thumbnails()`, `show_strip_preview()`, dan `update_final_preview()` bertugas memperbarui tampilan slot kecil dan preview hasil akhir.  
Bagian ini menjaga agar tampilan aplikasi selalu sinkron dengan foto yang sudah diambil.

### 10. Aksi Utama
- `set_slot()` untuk memilih slot foto aktif.
- `set_template()` untuk mengganti tema strip.
- `ask_event()` untuk mengubah nama event.
- `do_capture_session()` untuk mengambil 3 foto sekaligus.
- `do_retake()` untuk mengambil ulang foto di slot tertentu.
- `do_save()` untuk menyimpan hasil strip.
- `do_quit()` untuk keluar dari aplikasi.

### 11. Refresh Kamera
Fungsi `refresh_camera()` dijalankan terus-menerus menggunakan `root.after(30, refresh_camera)`.  
Ini membuat preview kamera tetap hidup dan responsif selama aplikasi berjalan.

---

## 🛠️ Teknologi yang Digunakan

- **Python**
- **OpenCV**
- **Tkinter**
- **NumPy**
- **Pillow**

---

## 📁 Output
Hasil foto strip akan disimpan di folder:

```bash
strip/
```

Format file yang disimpan adalah:

```bash
YYYYMMDD_HHMMSS.jpg
```

---

## 💡 Catatan

Project ini masih bisa dikembangkan lebih lanjut, misalnya dengan:
- menambah efek animasi yang lebih halus,
- menambahkan template custom,
- menyimpan hasil ke cloud,
- menambahkan filter foto,
- membuat versi web atau desktop yang lebih modern.

---

## 📸 Kesimpulan

FotoBoot Project adalah fondasi yang bagus untuk aplikasi photobooth modern.  
Dengan kombinasi kamera live, countdown, template strip, dan penyimpanan otomatis, project ini sudah punya alur kerja yang jelas, rapi, dan menyenangkan untuk digunakan.
