# Fruit Ninja Image Recognition
Ini adalah program Python yang dapat memainkan game populer **Fruit Ninja** dengan menggunakan pengenalan gambar.

# Bagaimana cara kerjanya?
Program ini bekerja dengan mengambil tangkapan layar permainan, dan mengambil sampel beberapa titik dari tangkapan layar untuk mencoba menemukan buah dan bom. Kemudian dari sana, beberapa transformasi dilakukan pada data untuk mencoba dan menghapus hal-hal yang kontraproduktif (seperti buah duplikat di wilayah kecil), dan kemudian program ini mengiris buah yang berada di lokasi yang aman (untuk menghindari bom) Metode untuk mencapai hal ini adalah dengan menggunakan `YOLOv8`, dan melatihnya dengan dataset buah dan bom khusus dari permainan.

------------------------

# Dependencies

- Pyautogui
- Pillow
- Opencv-python
- Numpy
- Mss
- Keyboard
------------------------

## Melatih model

Kita akan menggunakan gabungan dua dataset buah-buahan dan bom dari roboflow, kreditnya ada di file .txt di folder dataset.

Kami menggunakan file 'train.ipynb' untuk melatih model, dan model 'best.pt' disimpan di folder 'runs/detect/train*/weight'.
 - Model saat ini adalah file 'runs/detect/train232/weights/best3.pt'.

Gambar berikut ini menunjukkan sekumpulan prediksi dari model 'best3.pt':

![image](runs/detect/train232/val_batch2_pred.jpg)

Kita dapat melihat bahwa parameter conf harus diatur pada nilai yang tinggi untuk menghindari prediksi yang tidak perlu pada buah yang dipotong.

![image](git_images/gameplay_short_best3.gif)

------------------------

Translated with DeepL.com (free version)