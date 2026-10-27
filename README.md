# <p align="center">📂 SMART FILE ORGANIZER</p>
## <p align="center">📁 Smart File Organizer and Archiving System</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" />
  <img src="https://img.shields.io/badge/File_System-OS_&_Shutil-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<p align="center">
  <a href="#-english"><b>🇬🇧 English</b></a> · <a href="#-türkçe"><b>🇹🇷 Türkçe</b></a>
</p>

---

## 🇬🇧 English

### 📝 About the Project
**Smart File Organizer** is a lightweight and safe Windows automation tool that clears up the clutter in messy folders (such as "Downloads") with a single command. Using only Python's standard library, it sorts files into logical categories and builds a tidy archive structure.

It was built to save time by automating manual file sorting and to make better use of digital storage.

### 🌟 Key Features
* 🎯 **Smart classification:** Automatically moves files into folders by extension (Images, Documents, Videos, etc.).
* 🛡️ **Conflict handling:** If a file with the same name already exists in the target folder, it renames the file instead of deleting data (e.g. `report(1).pdf`).
* 👁️ **Confirmation step:** Lists every planned change and waits for your approval before moving anything.
* 📊 **Real-time tracking:** Reports in the terminal which file went to which category.
* ⚡ **Zero dependencies:** Works with Python's built-in modules only.

### 📁 Categories

| Category | Extensions |
| :--- | :--- |
| 🖼️ **Images** | `.jpg`, `.png`, `.gif`, `.webp`, `.svg` |
| 🎬 **Videos** | `.mp4`, `.mkv`, `.avi`, `.mov` |
| 📄 **Documents** | `.pdf`, `.docx`, `.txt`, `.xlsx`, `.pptx` |
| 💿 **Installers** | `.exe`, `.msi`, `.dmg` |
| 📦 **Archives** | `.zip`, `.rar`, `.7z`, `.tar` |
| 🎵 **Music** | `.mp3`, `.wav`, `.flac` |

### 🚀 Installation and Usage

1. **Download or clone the project:**
   ```bash
   git clone https://github.com/huseyinbaranisik/Smart_file_organizer.git
   cd Smart_file_organizer
   ```

2. **Run the program:**
   * **Option A (terminal):**
     ```bash
     python Kaynak_Kodlar/main.py
     ```
   * **Option B (batch file):** double-click `run.bat`.
   * **Option C (ready-made app):** run `Smart_file_organizar/Smart_File_Organizer.exe`.

### 🛠️ How It Works
When the program starts, it asks which folder you want to organise. After you enter the folder path:
1. It scans the files in the folder.
2. It lists which file will go to which category.
3. It waits for your confirmation (**y/n**).
4. If you confirm, it moves the files into the matching subfolders.

### 📝 License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🇹🇷 Türkçe

### 📝 Proje Hakkında
**Smart File Organizer**, düzensiz klasörlerdeki (örneğin "İndirilenler") dosya kalabalığını tek bir komutla ortadan kaldıran, hafif ve güvenli bir Windows otomasyon aracıdır. Python'un standart kütüphanelerini kullanarak dosyaları mantıksal kategorilere ayırır ve sistemli bir arşiv yapısı oluşturur.

Bu araç, manuel dosya düzenleme sürecini otomatikleştirerek zaman tasarrufu sağlamak ve dijital depolama alanlarını daha verimli kullanmak amacıyla geliştirilmiştir.

### 🌟 Temel Özellikler
* 🎯 **Akıllı Sınıflandırma:** Dosyaları uzantılarına göre (Görsel, Belge, Video vb.) otomatik olarak ilgili klasörlere taşır.
* 🛡️ **Çakışma Yönetimi:** Hedef klasörde aynı isimli bir dosya bulunması durumunda, veriyi silmek yerine otomatik olarak yeniden adlandırır (Örn: `rapor(1).pdf`).
* 👁️ **Onaylı İşlem Mekanizması:** Herhangi bir taşıma işlemi yapmadan önce yapılacak tüm değişiklikleri listeler ve kullanıcı onayı bekler.
* 📊 **Gerçek Zamanlı Takip:** Terminal üzerinden hangi dosyanın hangi kategoriye aktarıldığını anlık olarak raporlar.
* ⚡ **Sıfır Bağımlılık:** Harici bir kütüphane gerektirmeden, sadece Python'un yerleşik modülleriyle çalışır.

### 📁 Kategorizasyon Şeması

| Kategori | Uzantılar |
| :--- | :--- |
| 🖼️ **Görseller** | `.jpg`, `.png`, `.gif`, `.webp`, `.svg` |
| 🎬 **Videolar** | `.mp4`, `.mkv`, `.avi`, `.mov` |
| 📄 **Belgeler** | `.pdf`, `.docx`, `.txt`, `.xlsx`, `.pptx` |
| 💿 **Kurulum** | `.exe`, `.msi`, `.dmg` |
| 📦 **Arşivler** | `.zip`, `.rar`, `.7z`, `.tar` |
| 🎵 **Müzikler** | `.mp3`, `.wav`, `.flac` |

### 🚀 Kurulum ve Kullanım

1. **Projeyi indirin veya klonlayın:**
   ```bash
   git clone https://github.com/huseyinbaranisik/Smart_file_organizer.git
   cd Smart_file_organizer
   ```

2. **Programı çalıştırın:**
   * **Seçenek A (terminal):**
     ```bash
     python Kaynak_Kodlar/main.py
     ```
   * **Seçenek B (bat dosyası):** `run.bat` dosyasına çift tıklayın.
   * **Seçenek C (hazır uygulama):** `Smart_file_organizar/Smart_File_Organizer.exe` dosyasını çalıştırın.

### 🛠️ Nasıl Çalışır?
Program açıldığında size hangi klasörü düzenlemek istediğinizi sorar. Klasör yolunu girdikten sonra:
1. Program klasördeki dosyaları tarar.
2. Hangi dosyanın hangi kategoriye gideceğini listeler.
3. Sizden onay bekler (**y/n**).
4. Onay vermeniz durumunda dosyaları ilgili alt klasörlere taşır.

### 📝 Lisans
Bu proje MIT lisansı altındadır. Daha fazla bilgi için `LICENSE` dosyasına bakabilirsiniz.
