# ✨ Kadın Giyim Yorumlarından Tavsiye Tahmini (Recommendation Prediction System)

Bu proje, gerçek bir e-ticaret platformundan alınmış **23.486 müşteri yorumunu** kullanarak bir ürünün **tavsiye edilip edilmeyeceğini (0/1)** tahmin eden makine öğrenmesi sistemidir.

Doğal dil işleme (NLP), özellik mühendisliği, kategorik veri işleme ve ensemble modellerin gücünü bir araya getirerek **0.974 ROC AUC** gibi üst seviye bir başarı elde edilmiştir.

---
## Dataset Kaynağı
- [Women's E-Commerce Clothing Reviews - Kaggle](https://www.kaggle.com/datasets/mexwell/womens-e-commerce-clothing-reviews)
---

## 🎯 Model Performansı

| Metrik                       | Sonuç              |
| ---------------------------- |--------------------|
| **ROC AUC**                  | **0.974**          |
| **Accuracy**                 | **0.9391**         |
| **F1-Score (Recommended=1)** | **0.939**          |
| Confusion Matrix             | Aşağıdaki grafikte |

<img src="images/full_presentation_report.png" width="100%"/>

Bu skorlar, modelin gerçek dünyadaki kullanıcı tavsiye davranışını yüksek doğrulukla yakaladığını gösterir.

---

## 📦 Veri Seti: *Women’s Clothing E-Commerce Reviews*

* **23.486 satır**
* **10 özellik + yorum metni**
* Gerçek müşteri yorumları (anonimleştirilmiş)
* Amaç: **Recommended IND (0 = önerilmedi, 1 = önerildi)**

### İçerik:

| Değişken                | Açıklama                                      |
| ----------------------- | --------------------------------------------- |
| Clothing ID             | Ürünün kategorik ID'si                        |
| Age                     | Kullanıcı yaşı                                |
| Title                   | Yorum başlığı                                 |
| Review Text             | Yorum metni                                   |
| Rating                  | Ürün puanı (1–5)                              |
| Recommended IND         | Tavsiye durumu (hedef değişken)               |
| Positive Feedback Count | Yorumun kaç kişi tarafından yararlı bulunduğu |
| Division Name           | Üst ürün kategorisi                           |
| Department Name         | Departman                                     |
| Class Name              | Ürün türü (Dresses, Pants, Intimates vb.)     |

---

## 🧠 Neden Bu Model?

Aşağıdaki üst seviye pipeline ile çok yönlü bir yaklaşım benimsendi:

| Bileşen                                 | Sebep                                                              |
| --------------------------------------- | ------------------------------------------------------------------ |
| **Soft Voting Ensemble**                | Logistic Regression, Random Forest ve SVM’in güçlerini birleştirir |
| **TF-IDF + Truncated SVD**              | Metni 5000 → 100 boyuta indirerek hız + performans artışı sağlar   |
| **Custom `ReviewFeatures` Transformer** | Yorum uzunluğu, ünlem sayısı gibi duygu sinyallerini modele ekler  |
| **Pipeline + GridSearchCV**             | Tam otomatik veri işleme + en iyi hiperparametreler                |

### 🔍 `ReviewFeatures` Neden Bu Kadar Etkili?

Aşağıdaki sinyaller F1 skorunda **%2 artış** sağladı:

* Uzun yorum → daha düşünülmüş → daha çok tavsiye
* Çok “!” → duygusal ton yüksek → çoğu olumlu
* Kısa başlık → genelde olumsuz ("Küçük geldi", "Beğenmedim")

Bu nedenle yorumun yapısal özellikleri, metnin kendisi kadar değerli.

---

## 🛠️ Kullanım

### 1️⃣ Modeli Eğit

```bash
python main.py train
```

### 2️⃣ Konsolda Etkileşimli Tahmin

```bash
python main.py predict
```

### 3️⃣ CSV Dosyasından Toplu Tahmin

```bash
python main.py predict-batch data/new_reviews.csv
```

---

## 📁 Proje Yapısı

```
womens-clothing-recommender/
├── src/
│   ├── data/preprocessing.py          # Veri temizleme & preprocessor
│   ├── models/ensemble.py             # VotingClassifier setup
│   └── features/review_features.py    # Custom NLP feature transformer
├── scripts/
│   ├── train.py
│   ├── predict.py
│   └── batch_predict.py
├── images/                 # Model çıktıları (ROC, CM, rapor)
├── dataset/                # Ham ve işlenmiş veri
├── models/                 # Kaydedilmiş ML modelleri
│   └── best_recommendation_model.pkl
├── config.py
├── main.py
└── requirements.txt
```

---

## 📥 Gereksinimler

Python 3.10+ önerilir.

```bash
pip install -r requirements.txt
```

---

## 📜 Lisans

MIT License

---

## 👤 Author

**Celil Vural**
🔗 [https://linkedin.com/in/celil-v-92945325b](https://linkedin.com/in/celil-v-92945325b)

---

## 💬 Katkı

Pull request’ler memnuniyetle karşılanır!
Hatalar, öneriler veya iyileştirmeler için issue açabilirsiniz.

---
