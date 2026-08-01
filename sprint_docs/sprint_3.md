# Sprint 3 — EcoShield AI

## Sprint Amacı

Sprint 3 kapsamında, Sprint 2 sonunda belirlenen ortak deney protokolü ihtiyacının giderilmesi ve EcoShield AI projesinin çalışan bir ürün prototipi olarak tamamlanması hedeflenmiştir.

Bu sprintin ana hedefleri şunlardır:

- Tüm modeller için ortak train/validation/test ayrımı oluşturmak
- Preprocessing işlemlerini yalnızca train splitine fit etmek
- Hafif ve ağır modelleri aynı veri protokolü üzerinde karşılaştırmak
- Threshold seçimini yalnızca validation splitinde yapmak
- Cascade ve tekil ağır model yaklaşımlarını adil biçimde karşılaştırmak
- Final modeli test splitinde yalnızca bir kez değerlendirmek
- Seçilen modeli Streamlit arayüzüne entegre etmek
- Tek işlem, toplu CSV ve açıklanabilirlik özelliklerini tamamlamak
- Model tahmin katmanını FastAPI servisi olarak Streamlit arayüzünden ayırmak
- FastAPI ve Streamlit servislerini Docker Compose ile birlikte çalıştırmak
- Proje dokümantasyonunu ve final ürün demosunu hazırlamak

Sprint 2’de deneysel olarak ele alınan hafif model + ağır model cascade yaklaşımı bu sprintte ortak split üzerinde kurulmuş ve ölçülmüştür. Ancak cascade yaklaşımı, final test sonuçlarında tekil **CatBoost D8 Balanced** modelinin gerisinde kaldığı için final ürün mimarisi olarak seçilmemiştir.

Final ürün, tüm işlemleri doğrudan CatBoost D8 Balanced modeliyle değerlendiren tek aşamalı bir karar destek prototipi olarak tamamlanmıştır.

---

## Sprint İçinde Tamamlanması Tahmin Edilen Puan

**100 puan**

## Puan Tamamlama Mantığı

Sprint 3 iş yükü; ortak veri protokolü, model karşılaştırmaları, threshold tuning, cascade deneyi, tekil ağır model optimizasyonu, final test değerlendirmesi, Streamlit entegrasyonu ve final dokümantasyonu dikkate alınarak 100 puan üzerinden değerlendirilmiştir.

| Görev Grubu | Puan |
|---|---:|
| Ortak split ve preprocessing pipeline | 15 |
| Hafif model karşılaştırması | 10 |
| Ağır model karşılaştırması | 10 |
| Threshold tuning | 10 |
| Cascade pipeline ve trade-off analizi | 10 |
| Tekil ağır model optimizasyonu | 15 |
| Final test karşılaştırması | 10 |
| Streamlit prototipi ve açıklanabilirlik | 10 |
| FastAPI ve Docker Compose entegrasyonu | 5 |
| Sprint dokümantasyonu ve final video hazırlığı | 5 |
| **Toplam** | **100** |

---

## Sprint 3 Backlog

| No | Sprint Task | Durum |
|---|---|---|
| SB3-1 | Ortak train/validation/test indekslerinin oluşturulması | Tamamlandı |
| SB3-2 | Transaction ve identity tablolarının `TransactionID` üzerinden left join ile birleştirilmesi | Tamamlandı |
| SB3-3 | Preprocessing işlemlerinin yalnızca train splitine fit edilmesi | Tamamlandı |
| SB3-4 | Modele özel preprocessing cache yapısının hazırlanması | Tamamlandı |
| SB3-5 | Hafif modellerin ortak validation splitinde karşılaştırılması | Tamamlandı |
| SB3-6 | Ağır modellerin ortak validation splitinde karşılaştırılması | Tamamlandı |
| SB3-7 | Threshold tuning işlemlerinin yalnızca validation splitinde yapılması | Tamamlandı |
| SB3-8 | Cascade pipeline adaylarının kurulması ve yönlendirme oranlarının ölçülmesi | Tamamlandı |
| SB3-9 | Cascade yaklaşımının tekil modellerle validation üzerinde karşılaştırılması | Tamamlandı |
| SB3-10 | Ağır modellerin hafif model filtresi olmadan tüm train verisi üzerinde optimize edilmesi | Tamamlandı |
| SB3-11 | Final model adayı olarak CatBoost D8 Balanced modelinin seçilmesi | Tamamlandı |
| SB3-12 | Cascade ve tekil CatBoost modelinin kilitli test splitinde bir kez karşılaştırılması | Tamamlandı |
| SB3-13 | Final test metrikleri, confusion matrix ve PR/ROC eğrilerinin kaydedilmesi | Tamamlandı |
| SB3-14 | Streamlit karar destek prototipinin hazırlanması | Tamamlandı |
| SB3-15 | Tek işlem ve toplu CSV tahmin özelliklerinin eklenmesi | Tamamlandı |
| SB3-16 | CatBoost SHAP açıklanabilirlik ekranının eklenmesi | Tamamlandı |
| SB3-17 | Model performansı ve teknik mimari ekranlarının hazırlanması | Tamamlandı |
| SB3-18 | FastAPI model servisinin ve health, model-info, predict ve explain endpointlerinin hazırlanması | Tamamlandı |
| SB3-19 | Streamlit tahmin akışının FastAPI servisine bağlanması | Tamamlandı |
| SB3-20 | FastAPI ve Streamlit servislerinin Docker Compose ile container hâline getirilmesi | Tamamlandı |
| SB3-21 | Sprint 3 dokümantasyonunun hazırlanması | Tamamlandı |
| SB3-22 | Üç dakikayı geçmeyen final ürün demo videosunun hazırlanması | Video çekimi bekleniyor |
| SB3-23 | Videonun YouTube'a liste dışı yüklenmesi ve bağlantısının doğrulanması | Video çekimi bekleniyor |

---

## Backlog Düzeni ve Story Seçimleri

Sprint 3’te öncelik, Sprint 2’de birbirinden farklı split ve preprocessing yöntemleriyle yürütülen model denemelerini ortak bir değerlendirme protokolüne taşımaya verilmiştir.

Bu doğrultuda:

- Tüm model ailelerinde aynı train, validation ve test indeksleri kullanılmıştır.
- Preprocessing yalnızca train splitine fit edilmiştir.
- Resampling kullanılacaksa yalnızca train splitine uygulanması kuralı korunmuştur.
- Validation spliti model, parametre ve threshold seçimi için kullanılmıştır.
- Test spliti geliştirme sürecinden izole edilmiş ve yalnızca final karşılaştırmada açılmıştır.
- Accuracy ana seçim metriği olarak kullanılmamıştır.
- Precision, recall, F1, ROC-AUC, PR-AUC, false positive, false negative, eğitim süresi ve inference süresi birlikte değerlendirilmiştir.

Sprint 2’de projenin özgün mimari adayı olarak belirlenen cascade yaklaşımı korunmuş ve gerçek bir deney olarak uygulanmıştır. Bunun yanında, hafif model filtresi olmadan doğrudan tüm işlemleri değerlendiren tekil ağır modeller de optimize edilmiştir.

Bu seçim sayesinde cascade yaklaşımının yalnızca teorik avantajı değil, gerçek validation ve test performansı da tekil model yaklaşımıyla karşılaştırılmıştır.

---

## Daily Scrum Notları

### Daily Scrum 1

**Tarih:** 01.08.2026

**Toplantı Gündemi:**

Sprint 3 kapsamında tek bir Daily Scrum toplantısı yapılacaktır. Toplantıda EcoShield AI projesinin tamamlanmış hali ekip tarafından incelenecek, final Streamlit prototipinin çalışan akışları kontrol edilecek ve teslim için hazırlanacak üç dakikalık tanıtım videosunun içeriği planlanacaktır.

Toplantının ana gündem maddeleri:

- Streamlit uygulamasının tamamlanmış halinin incelenmesi
- Tek işlem tahmin akışının kontrol edilmesi
- Yüksek, düşük ve sınırda risk demo profillerinin test edilmesi
- Toplu CSV tahmin akışının kontrol edilmesi
- SHAP açıklanabilirlik ekranının incelenmesi
- Final model performansı ve teknik mimari ekranının kontrol edilmesi
- FastAPI health, model-info, predict ve explain endpointlerinin kontrol edilmesi
- Streamlit arayüzünün tahminleri FastAPI üzerinden aldığının doğrulanması
- Docker Compose ile API ve Streamlit containerlarının birlikte çalıştığının kontrol edilmesi
- Cascade yaklaşımından neden vazgeçildiğinin video anlatımında nasıl açıklanacağının belirlenmesi
- Video için konuşma ve ekran kaydı akışının oluşturulması
- Video anlatımının ekip üyeleri arasında paylaştırılması
- Video kaydının yatay formatta ve en fazla üç dakika olacak şekilde hazırlanması
- YouTube liste dışı yükleme ve teslim bağlantısının kontrol edilmesi

**Toplantıda Kontrol Edilecek Final Kararlar:**

- Final modelin CatBoost D8 Balanced olarak sunulması
- Validation’da seçilen `0.400815` threshold değerinin sabit tutulması
- Cascade mimarisinin tamamlanmış bir deney olarak anlatılması, ancak final ürün mimarisi olarak gösterilmemesi
- Final test sonucuna göre model veya threshold’un yeniden değiştirilmemesi
- Streamlit uygulamasının otomatik finansal karar sistemi değil, açıklanabilir bir karar destek prototipi olarak tanıtılması
- Projede kullanılan FastAPI ve Docker mimarisinin kısa ve anlaşılır biçimde gösterilmesi
- Projede kullanılmayan RAG, vektör veritabanı veya agent mimarilerinin kullanılmış gibi anlatılmaması

**Riskler:**

- Video süresinin üç dakikayı aşması
- Teknik ayrıntılara fazla zaman ayrılması ve ürün demosunun geri planda kalması
- Ekran kaydı sırasında model dosyası veya uygulama bağımlılıkları nedeniyle hata oluşması
- Video içerisinde cascade yaklaşımının yanlışlıkla final mimari gibi anlatılması
- YouTube bağlantısının erişime kapalı kalması

**Toplantı Sonrası Eklenecekler:**

- Uygulama incelemesinde tespit edilen son düzeltmeler
- Kesin video görev dağılımı
- Kayıt ve kurgu sorumluları
- Alınan nihai kararlar
- Video tamamlandığında YouTube liste dışı bağlantısı

---

## Sprint Board Update

Sprint 3 board’unda görevler aşağıdaki kolonlar üzerinden takip edilmiştir:

```text
Backlog
To Do
In Progress
Review
Done
```

Sprint 3 sonunda ortak split, preprocessing pipeline, hafif ve ağır model karşılaştırmaları, threshold tuning, cascade deneyi, tekil ağır model optimizasyonu, final test karşılaştırması, Streamlit ürün prototipi, FastAPI model servisi ve Docker Compose entegrasyonu tamamlanmıştır.

Final video çekimi ve YouTube bağlantısının eklenmesi teslim öncesinde tamamlanacak işler olarak bırakılmıştır.

Sprint board ekran görüntüsü aşağıdaki konuma eklenecektir:

```text
assets/sprint-3/sprint_board.png
```

Ekran görüntüsü repository’ye eklendikten sonra bu bölüme bağlanacaktır.

---

## Ürün Durumu

Sprint 3 sonunda EcoShield AI, deneysel modelleme çalışmasından çalışan bir fraud risk karar destek prototipine dönüştürülmüştür.

Final ürün:

- IEEE-CIS verisi için hazırlanmış ortak feature şemasını kullanır.
- Final model olarak CatBoost D8 Balanced modelini kullanır.
- Validation splitinde seçilen sabit threshold ile karar üretir.
- Tek işlem için fraud olasılığı ve inceleme sinyali gösterir.
- Transaction ve identity CSV dosyalarını `TransactionID` üzerinden left join ile birleştirebilir.
- Büyük CSV dosyalarında toplu ve parçalı tahmin yapabilir.
- Uzun işlemlerde ilerleme, işlenen satır, geçen süre ve ETA bilgisi gösterir.
- CatBoost SHAP ile tek işlem tahminini açıklayabilir.
- Tahmin ve açıklama isteklerini FastAPI model servisi üzerinden gerçekleştirir.
- Streamlit ve FastAPI servislerini ayrı containerlar olarak çalıştırır.
- Docker Compose ile iki servisi tek komutla ayağa kaldırabilir.
- Final test metriklerini ve karşılaştırma grafiklerini gösterir.
- Tahmin sonuçlarını CSV olarak dışarı aktarabilir.

Ürün otomatik finansal karar veren bir sistem değildir. Üretilen sonuçlar fraud ekipleri için manuel inceleme ve önceliklendirme sinyali olarak tasarlanmıştır.

### Final Streamlit Prototipi

Streamlit ekran görüntüleri aşağıdaki klasöre eklenecektir:

```text
assets/sprint-3/
├── streamlit_home.png
├── high_risk_prediction.png
├── low_risk_prediction.png
├── shap_explanation.png
├── batch_prediction.png
└── model_performance.png
```

---

## Teknik Çalışmalar

### Ortak Split ve Veri Sızıntısı Koruması

IEEE-CIS train verisi ortak train, validation ve test splitlerine ayrılmıştır. Oluşturulan indeksler kaydedilmiş ve bütün model deneylerinde aynı indeksler kullanılmıştır.

Veri protokolü:

```text
Train      → preprocessing fit + model eğitimi
Validation → model, parametre ve threshold seçimi
Test       → yalnızca final değerlendirme
```

Test spliti, model veya threshold seçimi için kullanılmamıştır. Preprocessing validation veya test verisine fit edilmemiştir.

### Ortak Preprocessing ve Modele Özel Cache Yapısı

Tek bir veri protokolü korunurken model ailelerinin ihtiyaçlarına uygun cache profilleri hazırlanmıştır:

- Linear modeller için ölçeklenmiş ve encode edilmiş sparse matrisler
- scikit-learn tree modelleri için uygun sayısal temsiller
- LightGBM için native kategorik veri profili
- CatBoost için native kategorik veri profili

Bu yapı, pahalı preprocessing işlemlerinin her notebookta yeniden çalıştırılmasını önlemiş ve bütün modellerin aynı satırları kullanmasını sağlamıştır.

### Hafif Model Karşılaştırması

Hafif model ailesinde aşağıdaki adaylar ortak validation splitinde karşılaştırılmıştır:

- Logistic Regression
- Decision Tree
- Small Random Forest
- Small LightGBM

Bu aşamada test verisi yüklenmemiş ve kesin model seçimi yapılmamıştır. Sonuçlar threshold tuning ve cascade adaylarının oluşturulması için validation tahminleri olarak kaydedilmiştir.

### Ağır Model Karşılaştırması

Ağır model ailesinde aşağıdaki adaylar değerlendirilmiştir:

- Heavy Random Forest
- XGBoost
- Heavy LightGBM
- Heavy CatBoost

Modeller ortak split üzerinde eğitilmiş; precision, recall, F1, ROC-AUC, PR-AUC, eğitim süresi, inference süresi, RAM kullanımı ve model boyutu birlikte raporlanmıştır.

### Threshold Tuning

Threshold tuning yalnızca validation splitinde gerçekleştirilmiştir.

Fraud detection problemi için minimum recall hedefi korunurken precision ve F1 değerlerini iyileştiren threshold noktaları araştırılmıştır. Seçilen threshold değerleri sonraki aşamalarda sabit tutulmuş ve test sonuçlarına göre değiştirilmemiştir.

### Cascade Pipeline Deneyi

Cascade sisteminde hafif model bütün işlemleri taramış, belirlenen yönlendirme threshold’unu geçen işlemler ağır modele gönderilmiştir.

Değerlendirilen temel kombinasyonlar:

- Logistic Regression → Heavy CatBoost
- Logistic Regression → XGBoost
- Small Random Forest → Heavy CatBoost
- Small Random Forest → XGBoost

Validation sonuçlarında minimum recall hedefi sağlanmış olsa da en iyi F1 değerlerine ulaşmak için işlemlerin önemli bir bölümünün ağır modele yönlendirilmesi gerekmiştir.

Bu durum, cascade yaklaşımının beklenen compute-saving avantajını sınırlamıştır. Ayrıca hafif model aşamasında elenen fraud işlemlerin ağır model tarafından geri kazanılamaması sistemin yapısal bir riski olarak değerlendirilmiştir.

### Tekil Ağır Model Optimizasyonu

Cascade sonucunun ardından ağır modeller, hafif model filtresi olmadan bütün train verisi üzerinde optimize edilmiştir.

XGBoost ve CatBoost için farklı:

- Derinlik
- Class weight
- Regularization
- Ağaç sayısı
- Öğrenme oranı

yapılandırmaları karşılaştırılmıştır.

Validation sonuçlarında **CatBoost D8 Balanced**, PR-AUC ve minimum recall altında elde edilen F1 dengesi nedeniyle final tekil model adayı olarak seçilmiştir.

### Cascade Mimarisinden Vazgeçme Kararı

Cascade yaklaşımı projenin başlangıçtaki temel mimari hipotezlerinden biridir. Sprint 3’te bu hipotez gerçek bir pipeline olarak uygulanmış, threshold ve yönlendirme oranları ölçülmüş ve tekil model yaklaşımıyla karşılaştırılmıştır.

Ancak deneyler sonucunda:

1. Yüksek fraud recall değerini korumak için işlemlerin büyük bölümü ağır modele yönlendirilmiştir.
2. Yönlendirme oranının yükselmesi cascade yapısının hesaplama avantajını azaltmıştır.
3. Hafif aşamada elenen fraud işlemler ağır model tarafından geri kazanılamamıştır.
4. Tekil CatBoost modeli daha yüksek precision ve F1 sağlamıştır.
5. Tekil CatBoost modeli final testte daha yüksek PR-AUC ve ROC-AUC üretmiştir.
6. Tekil CatBoost modeli daha az false positive oluşturmuştur.

Bu nedenle cascade yaklaşımı teknik deney ve karşılaştırma çıktısı olarak korunmuş; ancak final ürün mimarisi sadeleştirilerek tüm işlemleri doğrudan CatBoost D8 Balanced modeliyle değerlendiren tek aşamalı yapıya geçilmiştir.

Bu karar başlangıçtaki planın gerekçesiz biçimde terk edilmesi değil, validation ve final test sonuçlarına dayalı bir mimari seçimdir.

### Final Test Karşılaştırması

Validation aşamasında seçilen cascade pipeline ve CatBoost D8 Balanced modeli kilitli test splitinde yalnızca bir kez değerlendirilmiştir.

| Yaklaşım | Precision | Recall | F1 | PR-AUC | ROC-AUC | False Positive | False Negative |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cascade | 0.3634 | 0.9032 | 0.5183 | 0.84 | 0.97 | 4.903 | 300 |
| CatBoost D8 Balanced | **0.4319** | 0.8971 | **0.5831** | **0.8596** | **0.9763** | **3.657** | 319 |

Cascade yaklaşımı 19 ek fraud işlemi yakalamış; ancak bunun karşılığında 1.246 daha fazla normal işlemi fraud olarak işaretlemiştir.

CatBoost D8 Balanced:

- Precision değerini yaklaşık 6,85 yüzde puan artırmıştır.
- F1 değerini yaklaşık 6,48 yüzde puan artırmıştır.
- False positive sayısını 4.903’ten 3.657’ye düşürmüştür.
- Recall değerinde yalnızca yaklaşık 0,61 yüzde puan düşüş yaşamıştır.

Bu trade-off, final ürün için CatBoost D8 Balanced modelinin daha dengeli ve operasyonel olarak daha verimli olduğunu göstermiştir.

### Final Model ve Threshold

Final ürün yapılandırması:

```text
Model: CatBoost D8 Balanced
Threshold: 0.400815
Feature sayısı: 423
Karar türü: Fraud inceleme sinyali / Normal akış
```

Threshold validation splitinde seçilmiş ve Streamlit uygulamasında sabitlenmiştir. Uygulama içerisinde threshold tuning yapılmamaktadır.

### Streamlit Ürün Prototipi

Streamlit prototipinde aşağıdaki özellikler tamamlanmıştır:

- Gerçek test cache’inden hazırlanmış yüksek, düşük ve sınırda risk demo işlemleri
- JSON ile tek işlem tahmini
- Transaction ve identity CSV dosyalarıyla toplu tahmin
- Fraud olasılığı ve sabit threshold gösterimi
- Risk seviyesi ve manuel inceleme önerisi
- CatBoost SHAP açıklanabilirliği
- En etkili feature grafiği ve tablosu
- Final model performans metrikleri
- Final confusion matrix ve PR/ROC eğrileri
- Tahmin sonuçlarını CSV olarak indirme
- Oturumu temizleme

### FastAPI Model Servisi

Streamlit arayüzü ile model çıkarım katmanı birbirinden ayrılmıştır. Model yükleme, feature hazırlama, tahmin ve açıklanabilirlik işlemleri FastAPI servisine taşınmıştır.

Serviste bulunan temel endpointler:

- `GET /health`: Servisin ve modelin çalışır durumda olduğunu kontrol eder.
- `GET /model-info`: Final model, threshold ve feature şeması bilgilerini döndürür.
- `POST /predict`: Tek işlem veya toplu işlem için fraud olasılığı ve karar üretir.
- `POST /explain`: Seçilen işlem için SHAP tabanlı açıklama üretir.

Streamlit uygulaması model dosyasını doğrudan çalıştırmak yerine FastAPI servisine HTTP/JSON isteği gönderir. Böylece kullanıcı arayüzü ve model servisi bağımsız olarak geliştirilebilir, test edilebilir ve ölçeklenebilir hâle getirilmiştir.

### Docker Compose Entegrasyonu

FastAPI ve Streamlit servisleri Docker containerları hâline getirilmiş ve `docker-compose.yml` üzerinden birlikte yönetilmiştir.

Docker Compose yapısı:

- `ecoshield-api`: FastAPI ve CatBoost inference servisi
- `ecoshield-streamlit`: Kullanıcı arayüzü

Streamlit containerı API servisi sağlıklı duruma geldikten sonra başlatılır. Model dosyası 100 MB sınırını aşabileceği için Git repository’ye veya Docker image içine eklenmemiş; yerel `models` klasöründen container içine salt okunur volume olarak bağlanmıştır.

Bu yapı sayesinde servislerin bağımlılıkları standartlaştırılmış, uygulamanın farklı ortamlarda aynı yapılandırmayla çalıştırılması kolaylaştırılmıştır.

### Teknik Mimari

```text
Kullanıcı
   │
   ▼
Streamlit arayüzü
   │ HTTP / JSON
   ▼
FastAPI model servisi
   │
   ├── Feature şeması ve veri tipi kontrolü
   ├── TransactionID üzerinden veri birleştirme
   ├── CatBoost D8 Balanced
   ├── Sabit validation threshold
   └── SHAP açıklaması
   │
   ▼
Tahmin ve karar destek çıktısı
```

---

## Final Ürün Demo Videosu

Final teslim kapsamında ürünün en fazla üç dakikalık ve yatay formatta canlı demo videosu hazırlanacaktır. Video henüz çekilmediği için bu dokümana görsel, zaman çizelgesi veya YouTube bağlantısı eklenmemiştir.

Videoda fraud detection problemi, hedef kullanıcı, Streamlit üzerinden çalışan ürün akışı, SHAP açıklaması, cascade yaklaşımından tekil CatBoost modeline geçiş, FastAPI–Docker mimarisi ve final model sonuçları kısa biçimde anlatılacaktır. Kurulum adımlarına, kod satırlarına ve projede kullanılmayan teknolojilere zaman ayrılmayacaktır.

---

## Sprint Review

Sprint 3 kapsamında EcoShield AI projesinin ortak değerlendirme protokolü ve final ürün prototipi tamamlanmıştır.

Sprint sonunda:

- Bütün modeller ortak train/validation/test splitinde karşılaştırılmıştır.
- Preprocessing yalnızca train splitine fit edilmiştir.
- Modele özel cache profilleri hazırlanmıştır.
- Hafif ve ağır model karşılaştırmaları tamamlanmıştır.
- Threshold tuning yalnızca validation splitinde gerçekleştirilmiştir.
- Cascade pipeline uygulanmış ve yönlendirme trade-off’u ölçülmüştür.
- Tekil ağır modeller hafif model filtresi olmadan optimize edilmiştir.
- CatBoost D8 Balanced final model adayı olarak seçilmiştir.
- Cascade ve tekil model kilitli test splitinde bir kez karşılaştırılmıştır.
- Test sonucuna göre yeniden model veya threshold seçimi yapılmamıştır.
- CatBoost D8 Balanced final ürün modeli olarak sabitlenmiştir.
- Streamlit karar destek prototipi hazırlanmıştır.
- Tek işlem, toplu CSV, SHAP ve model performansı ekranları tamamlanmıştır.
- Model tahmin ve açıklama katmanı FastAPI servisine ayrılmıştır.
- Streamlit arayüzü FastAPI servisine HTTP/JSON üzerinden bağlanmıştır.
- FastAPI ve Streamlit servisleri Docker Compose ile birlikte çalıştırılmıştır.

Başlangıçta hedeflenen cascade mimarisi teknik olarak uygulanmış ancak final test karşılaştırması sonucunda ürün mimarisi olarak seçilmemiştir. Proje, deney sonuçlarına göre daha sade ve daha dengeli tekil CatBoost mimarisine geçirilmiştir.

---

## Sprint Retrospective

### İyi Gidenler

- Sprint 2’de tespit edilen ortak split ve preprocessing problemi giderildi.
- Bütün model aileleri karşılaştırılabilir bir protokol altında yeniden değerlendirildi.
- Veri sızıntısını önleyen train/validation/test kuralları uygulandı.
- Test verisi final değerlendirmeye kadar izole edildi.
- Cascade yaklaşımı yalnızca fikir seviyesinde bırakılmayıp gerçek pipeline olarak uygulandı.
- Başlangıç hipotezine bağlı kalmak yerine deney sonuçlarına göre mimari karar verildi.
- CatBoost D8 Balanced ile yüksek recall korunurken precision ve F1 iyileştirildi.
- False positive sayısı cascade yaklaşıma göre azaltıldı.
- Model çıktıları çalışan bir Streamlit karar destek prototipine dönüştürüldü.
- SHAP ile tek işlem seviyesinde açıklanabilirlik sağlandı.
- Streamlit ile model servisi FastAPI üzerinden ayrıştırıldı.
- Docker Compose ile iki servisli, tekrar çalıştırılabilir ürün mimarisi kuruldu.
- Uzun işlemlerde ilerleme ve süre bilgisi görünür hale getirildi.

### Zorlayan Noktalar

- IEEE-CIS veri setinin 423 feature içeren geniş yapısı bellek ve preprocessing maliyetini artırdı.
- Farklı model aileleri için ortak fakat uygun veri temsilleri hazırlamak ek geliştirme gerektirdi.
- Logistic Regression eğitimi sparse veri üzerinde uzun sürdü ve convergence uyarıları oluşturdu.
- Recall hedefi yükseltildiğinde precision ve false positive sayısında belirgin trade-off oluştu.
- Cascade sisteminde yüksek recall için ağır modele yönlendirme oranının beklenenden yüksek olduğu görüldü.
- Model dosyası GitHub’ın normal dosya boyutu sınırını aştığı için repository’ye eklenemedi.
- Streamlit uygulamasında yüzlerce feature içeren tek işlem girdisini kullanıcı dostu biçimde sunmak zorlayıcı oldu.

### Proje Sonrası İyileştirilebilecekler

- Model artifact’i için Git LFS, release asset veya harici model registry kullanılabilir.
- API endpointleri için otomatik unit ve integration testleri eklenebilir.
- Container image boyutu multi-stage build ile küçültülebilir.
- Model dosyası bir model registry veya object storage üzerinden yönetilebilir.
- Veri drift ve model drift izleme bileşenleri eklenebilir.
- SHAP hesaplamaları önbelleğe alınarak açıklama süresi azaltılabilir.
- Kullanıcı girdileri için domain doğrulama ve feature validation katmanı geliştirilebilir.
- Batch inference işlemleri kuyruk tabanlı arka plan görevlerine taşınabilir.
- Zamana dayalı out-of-time validation ile model dayanıklılığı ayrıca ölçülebilir.
- Precision ve recall maliyetleri gerçek operasyonel maliyetlerle ağırlıklandırılabilir.
- Model kalibrasyonu ve farklı risk segmentleri ayrı bir validation protokolüyle incelenebilir.
- Üretim ortamı için kimlik doğrulama, loglama, audit trail ve erişim kontrolü eklenebilir.

---

## Sprint 3 Sonuç Özeti

Sprint 3 kapsamında EcoShield AI projesi ortak veri protokolü, karşılaştırılabilir model deneyleri, final model seçimi ve çalışan ürün arayüzüyle tamamlanmıştır.

Ortak train/validation/test splitleri oluşturulmuş, preprocessing işlemleri yalnızca train verisine fit edilmiş ve model aileleri kendi ihtiyaçlarına uygun cache profilleriyle aynı satırlar üzerinde değerlendirilmiştir. Hafif ve ağır model karşılaştırmaları, threshold tuning, cascade pipeline ve tekil ağır model optimizasyonu tamamlanmıştır.

Projenin başlangıçtaki temel hipotezi olan hafif model + ağır model cascade yaklaşımı gerçek bir pipeline olarak uygulanmış ve ölçülmüştür. Ancak yüksek recall değerini korumak için işlemlerin büyük bölümünün ağır modele yönlendirilmesi, hafif aşamada kaçırılan fraud işlemlerin geri kazanılamaması ve final testte daha fazla false positive üretilmesi nedeniyle cascade final ürün mimarisi olarak seçilmemiştir.

Final testte CatBoost D8 Balanced modeli, cascade yaklaşıma göre daha yüksek precision, F1, PR-AUC ve ROC-AUC üretmiş; false positive sayısını 4.903’ten 3.657’ye düşürmüştür. Recall değerindeki sınırlı düşüşe karşılık daha dengeli bir operasyonel sonuç sağladığı için final model olarak seçilmiştir.

Seçilen model Streamlit arayüzüne entegre edilmiş; tek işlem tahmini, toplu CSV analizi, fraud olasılığı, sabit threshold, risk sinyali, SHAP açıklanabilirliği, model performansı ve sonuç indirme özellikleri tamamlanmıştır.

Son ürünleştirme aşamasında model inference katmanı FastAPI servisine ayrılmış, Streamlit arayüzü tahmin ve açıklama isteklerini HTTP/JSON üzerinden bu servise gönderecek şekilde düzenlenmiştir. FastAPI ve Streamlit servisleri Docker Compose ile iki ayrı container olarak çalıştırılmıştır. Böylece proje yalnızca notebook ve yerel arayüz seviyesinde kalmamış, servis tabanlı ve tekrar çalıştırılabilir bir ürün mimarisine taşınmıştır.

EcoShield AI, otomatik finansal karar veren bir sistem değil; fintech, ödeme ve fraud ekiplerinin riskli işlemleri önceliklendirmesine yardımcı olan açıklanabilir bir karar destek prototipi olarak tamamlanmıştır.
