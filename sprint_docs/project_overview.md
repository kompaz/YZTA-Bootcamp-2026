# EcoShield AI - Project Overview

## Proje Tanımı

EcoShield AI, finansal işlemlerde dolandırıcılık tespitini daha verimli hale getirmek için geliştirilmiş iki aşamalı yapay zeka destekli fraud detection platformudur.

Sistem, tüm işlemleri doğrudan ağır modellerden geçirmek yerine önce hafif bir modelle ön eleme yapar. Sadece şüpheli işlemler ikinci aşamadaki daha güçlü modele gönderilir. Böylece hem fraud tespiti yapılır hem de gereksiz model çalıştırma maliyeti azaltılır.

---

## Problem Tanımı

Finansal dolandırıcılık tespiti, dijital ödeme sistemleri, fintech girişimleri, bankalar ve e-ticaret ödeme altyapıları için kritik bir problemdir.

Fraud detection problemlerinde veri genellikle ciddi şekilde dengesizdir. Normal işlemler çok fazla, fraud işlemler ise çok az sayıdadır. Bu nedenle accuracy metriği tek başına yeterli değildir.

Bu projede fraud detection problemi şu açılardan ele alınacaktır:

- Class imbalance analizi
- Baseline model geliştirme
- Precision, recall, F1, ROC-AUC ve PR-AUC metrikleriyle değerlendirme
- SMOTE / class weight / threshold tuning gibi yöntemlerin karşılaştırılması
- Hafif model + ağır model şeklinde iki aşamalı model mimarisi
- Compute-saving / model çağrı azaltımı metriği

---

## Hedef Kitle

- Fintech girişimleri
- Dijital ödeme sistemleri
- Bankalar
- Risk ve fraud ekipleri
- Dijital cüzdan uygulamaları
- E-ticaret ödeme altyapıları

---

## Kullanılacak Veri Seti

İlk aşamada Credit Card Fraud Detection veri seti kullanılacaktır.

Target değişkeni:

- `Class = 0` → Normal işlem
- `Class = 1` → Fraud işlem

Bu veri seti üzerinde EDA, preprocessing, baseline modelleme ve class imbalance analizleri yapılacaktır.

---

## Önerilen Modelleme Yaklaşımı

Proje iki aşamalı bir fraud detection mimarisi üzerine kurulacaktır.

### 1. Aşama: Hafif Model

Tüm işlemleri hızlıca tarayan düşük maliyetli model.

Olası modeller:

- Logistic Regression
- Decision Tree
- Random Forest küçük versiyon
- LightGBM küçük versiyon

### 2. Aşama: Ağır Model

Sadece şüpheli işlemleri detaylı analiz eden daha güçlü model.

Olası modeller:

- XGBoost
- LightGBM
- CatBoost
- Random Forest
- Autoencoder

---

## Başarı Metrikleri

Bu projede accuracy tek başına yeterli görülmeyecektir. Aşağıdaki metrikler birlikte değerlendirilecektir:

- Precision
- Recall
- F1-score
- ROC-AUC
- PR-AUC
- Confusion Matrix
- False Positive / False Negative analizi
- Model çağrı azaltımı oranı
- Tahmini compute-saving oranı

---

## MVP Kapsamı

Bootcamp sürecinde hedeflenen MVP şunları içerecektir:

- Veri yükleme ve temel analiz
- Fraud / normal işlem dağılımı gösterimi
- Baseline model sonuçları
- Class imbalance yöntemlerinin karşılaştırılması
- İki aşamalı model mimarisi
- Riskli işlemleri gösteren dashboard
- Model metriklerini gösteren arayüz
- Compute-saving metriği