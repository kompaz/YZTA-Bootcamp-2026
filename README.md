# EcoShield AI

EcoShield AI, finansal işlemlerde dolandırıcılık tespitini daha verimli hale getirmek için geliştirilmiş yapay zeka destekli bir fraud detection platformudur.

Proje, klasik tek aşamalı fraud detection yaklaşımı yerine iki aşamalı bir model mimarisi kullanmayı hedefler. İlk aşamada hafif bir model tüm işlemleri hızlıca tarar. İkinci aşamada ise yalnızca riskli görülen işlemler daha güçlü bir modele gönderilir. Bu yaklaşım ile hem fraud tespit performansının artırılması hem de gereksiz model çalıştırma maliyetinin azaltılması amaçlanmaktadır.

## Hedefler

- Fraud detection için baseline model geliştirmek
- Class imbalance problemini analiz etmek
- Precision, recall, F1, ROC-AUC gibi metrikleri karşılaştırmak
- İki aşamalı hafif model + ağır model mimarisi kurmak
- Riskli işlemleri dashboard üzerinde göstermek
- Model çağrı sayısı üzerinden compute-saving metriği üretmek

## Ürün Özellikleri

- Finansal işlem verileri üzerinde fraud / normal işlem analizi
- Class imbalance probleminin incelenmesi
- Precision, recall, F1-score, ROC-AUC ve PR-AUC gibi metriklerle model değerlendirme
- SMOTE, class weight ve threshold tuning gibi yöntemlerin karşılaştırılması
- Hafif model + ağır model şeklinde iki aşamalı fraud detection mimarisi
- Riskli işlemleri dashboard üzerinde gösterme
- Model çağrı sayısı üzerinden compute-saving metriği üretme

---

# Problem Tanımı

Finansal dolandırıcılık tespiti, dijital ödeme sistemleri, fintech girişimleri, bankalar ve e-ticaret ödeme altyapıları için kritik bir problemdir.

Fraud detection problemlerinde veri genellikle ciddi şekilde dengesizdir. Normal işlemler çok fazla, fraud işlemleri ise çok az sayıdadır. Bu nedenle accuracy metriği tek başına yeterli değildir.

Bu projede fraud detection problemi şu açılardan ele alınacaktır:

- Class imbalance analizi
- Baseline model geliştirme
- Precision, recall, F1-score, ROC-AUC ve PR-AUC metrikleriyle değerlendirme
- SMOTE / class weight / threshold tuning gibi yöntemlerin karşılaştırılması
- Hafif model + ağır model şeklinde iki aşamalı model mimarisi
- Compute-saving / model çağrı azaltımı metriği

---

# Hedef Kitle

- Fintech girişimleri
- Dijital ödeme sistemleri
- Bankalar
- Risk ve fraud ekipleri
- Dijital cüzdan uygulamaları
- E-ticaret ödeme altyapıları

---

# Veri Seti

İlk aşamada **Credit Card Fraud Detection** veri seti kullanılmıştır.

Target değişkeni:

- `Class = 0` → Normal işlem
- `Class = 1` → Fraud işlem

Sprint 1 kapsamında bu veri seti üzerinde EDA, class imbalance analizi ve temel veri inceleme çalışmaları yapılmıştır.

---

# Product Backlog

| No | User Story | Öncelik | Durum |
|---|---|---:|---|
| PB-1 | Kullanıcı olarak işlem verilerini sisteme yükleyebilmek istiyorum. | Yüksek | Planlandı |
| PB-2 | Sistem olarak yüklenen veriyi temizleyip model eğitimine hazır hale getirmeliyim. | Yüksek | Devam ediyor |
| PB-3 | Kullanıcı olarak fraud ve normal işlem dağılımını görebilmek istiyorum. | Yüksek | Devam ediyor |
| PB-4 | Sistem olarak baseline fraud detection modeli eğitmeliyim. | Yüksek | Planlandı |
| PB-5 | Kullanıcı olarak modelin precision, recall, F1, ROC-AUC gibi metriklerini görebilmeliyim. | Yüksek | Planlandı |
| PB-6 | Sistem olarak class imbalance problemini SMOTE veya class weight ile ele almalıyım. | Yüksek | Planlandı |
| PB-7 | Sistem olarak threshold tuning yaparak fraud yakalama performansını iyileştirmeliyim. | Yüksek | Planlandı |
| PB-8 | Sistem olarak hafif model + ağır model şeklinde iki aşamalı mimari kurmalıyım. | Yüksek | Planlandı |
| PB-9 | Kullanıcı olarak riskli işlemleri dashboard üzerinde listeleyebilmeliyim. | Yüksek | Planlandı |
| PB-10 | Kullanıcı olarak bir işlemin neden riskli görüldüğünü açıklamalı şekilde görebilmeliyim. | Orta | Planlandı |
| PB-11 | Sistem olarak compute-saving / model çağrı azaltımı metriği göstermeliyim. | Orta | Planlandı |
| PB-12 | Kullanıcı olarak demo arayüzünden örnek işlem analizi yapabilmeliyim. | Orta | Planlandı |
| PB-13 | Kullanıcı olarak model performanslarını karşılaştırmalı şekilde görebilmeliyim. | Orta | Planlandı |
| PB-14 | Sistem olarak eğitim sonucunda model dosyalarını kaydetmeliyim. | Orta | Planlandı |
| PB-15 | Proje ekibi olarak tüm geliştirme sürecini GitHub üzerinde belgelemeliyiz. | Yüksek | Devam ediyor |

## Backlog Dağıtma Mantığı

Product backlog, ürünün veri hazırlama, modelleme, değerlendirme, iki aşamalı mimari ve dashboard geliştirme ihtiyaçlarına göre oluşturulmuştur.

İlk sprintte temel veri analizi ve proje yönünün netleştirilmesine öncelik verilmiştir. Sonraki sprintlerde class imbalance yöntemleri, iki aşamalı model mimarisi, dashboard ve compute-saving metriği geliştirilecektir.

## Önceliklendirme Kriterleri

Backlog maddeleri şu kriterlere göre önceliklendirilmiştir:

- MVP için zorunlu olması
- Modelleme sürecine temel oluşturması
- Demo sırasında gösterilebilir olması
- Yapay zeka katkısını güçlendirmesi
- Ürün bütünlüğüne katkı sağlaması

---

## Sprint Amacı

Bu sprintte EcoShield AI projesinin temel kapsamını belirlemek, veri setini seçmek, ilk veri analizlerini yapmak ve fraud detection problemi için sağlam bir başlangıç altyapısı oluşturmak hedeflenmiştir.

Sprint 1’in ana odağı:

- Proje fikrinin netleşmesi
- Veri setinin seçilmesi
- Repo ve dokümantasyon düzeninin oluşturulması
- EDA yapılması
- Fraud / normal işlem dağılımının analiz edilmesi
- Class imbalance probleminin tespit edilmesi
- Sprint board ve ürün durumu çıktılarının hazırlanması

Bu sprintte model eğitimi yapılmamıştır. Train/test split, baseline modelleme, model metrikleri ve iki aşamalı mimari Sprint 2 kapsamına bırakılmıştır.

---

## Sprint 1 Backlog

Bu sprintte Product Backlog içerisinden proje fikrinin netleştirilmesi, veri setinin seçilmesi, repo/dokümantasyon düzeninin kurulması ve ilk EDA çalışmalarının yapılması hedeflenmiştir.

| No | Sprint Task | Sorumlu | Durum |
|---|---|---|---|
| SB-1 | Proje fikrinin netleştirilmesi | Tüm ekip | Tamamlandı |
| SB-2 | Proje repo yapısının oluşturulması | Developer | Tamamlandı |
| SB-3 | `docs` klasörünün ve sprint dokümanlarının hazırlanması | Developer | Tamamlandı |
| SB-4 | Kullanılacak veri setlerinin araştırılması | Tüm ekip | Tamamlandı |
| SB-5 | Credit Card Fraud Detection veri setinin seçilmesi | Tüm ekip | Tamamlandı |
| SB-6 | Veri setinin `data/raw` klasörüne eklenmesi | Developer | Tamamlandı |
| SB-7 | EDA notebook dosyasının oluşturulması | Developer | Tamamlandı |
| SB-8 | Veri setinin satır/sütun yapısının incelenmesi | Developer | Tamamlandı |
| SB-9 | Fraud / normal işlem dağılımının analiz edilmesi | Developer | Tamamlandı |
| SB-10 | Eksik değer ve duplicate kontrolü yapılması | Developer | Tamamlandı |
| SB-11 | Class distribution grafiğinin oluşturulması | Developer | Tamamlandı |
| SB-12 | Amount ve Time değişkenlerinin temel dağılım analizinin yapılması | Developer | Tamamlandı |
| SB-13 | EDA çıktılarının `assets/sprint-1` klasörüne kaydedilmesi | Developer | Tamamlandı |
| SB-14 | Sprint board ekran görüntüsünün eklenmesi | Scrum Master | Planlandı |
| SB-15 | Ürün durumu ekran görüntülerinin eklenmesi | Tüm ekip | Planlandı |

---

## Story Seçimleri ve Backlog Dağılımı

Sprint 1’de ürünün temel teknik altyapısını oluşturacak görevler seçilmiştir.

Bu sprintte öncelik, final dashboard’u veya gelişmiş modeli tamamlamak değil; veri setini anlamak, fraud detection problemini doğru tanımlamak ve modelleme öncesi veri analizini tamamlamaktır.

Bu nedenle Sprint 1’de şu işlere öncelik verilmiştir:

- Veri setinin seçilmesi
- Repo ve klasör yapısının kurulması
- EDA notebook’unun hazırlanması
- Fraud / normal işlem dağılımının incelenmesi
- Class imbalance probleminin ortaya konması
- EDA çıktılarının görsel ve metinsel olarak kaydedilmesi

Bu seçimlerin nedeni, Sprint 1’de doğrudan model geliştirmeye geçmeden önce veri setinin yapısını anlamak ve fraud detection probleminin temel karakterini ortaya koymaktır. EDA sonucunda veri setindeki class imbalance problemi netleştirilecek, bu çıktı Sprint 2’de yapılacak train/test split, baseline modelleme, SMOTE / class weight ve threshold tuning çalışmaları için temel oluşturacaktır.

---

## Sprint Board

Sprint board için aşağıdaki kolonlar kullanılacaktır:

```text
Backlog
To Do
In Progress
Review
Done
```

Sprint board üzerinde görevler bu kolonlar arasında ilerletilecektir. Her görev başlangıçta Backlog veya To Do kolonunda yer alacak, geliştirme sürecine alındığında In Progress kolonuna taşınacak, kontrol bekleyen işler Review kolonunda tutulacak ve tamamlanan işler Done kolonuna aktarılacaktır.

Sprint board ekran görüntüsü aşağıdaki klasöre eklenecektir:

```text
assets/sprint-1/sprint_board.png
```

Sprint board ekran görüntüsü eklendikten sonra aşağıdaki bağlantı aktif hale gelecektir:

![Sprint Board](/assets/sprint-1/sprint_board.png)

---

## Daily Scrum Notları

### Daily Scrum 1

**Tarih:** 23.06.2026

**Toplantı Özeti:**

İlk Scrum toplantısında ekip olarak farklı proje temaları üzerine araştırma yapılmasına karar verilmiştir. Proje fikrinin doğrudan seçilmesi yerine, önce farklı alanlardaki makaleler, veri setleri ve uygulanabilir proje örnekleri incelenerek daha sağlam bir karar verilmesi hedeflenmiştir.

Bu doğrultuda araştırma sürecinin 2-3 Temmuz tarihine kadar devam ettirilmesi önerilmiştir. Elde edilen makale, veri seti ve proje fikirleri üzerinden sıfırdan yeni bir proje oluşturulması veya birden fazla fikrin güçlü yönlerini birleştiren daha kapsamlı bir proje geliştirilmesi planlanmıştır.

**Alınan Kararlar:**

- Farklı temalar üzerinden makale ve proje araştırması yapılacak.
- Araştırma süreci 2-3 Temmuz tarihine kadar sürdürülecek.
- Bulunan kaynaklar üzerinden sıfırdan veya bileşik bir proje fikri çıkarılacak.
- Ekip için sabit bir haftalık toplantı günü belirlenecek.
- Toplantı günü ekip içinde oylama ile kararlaştırılacak.
- Gerektiği haftalarda toplantı sayısı haftada 2’ye çıkarılabilecek.

**Blocker / Risk:**

- Henüz net bir proje fikri seçilmediği için araştırma sürecinin fazla uzaması riski bulunmaktadır.
- Bu riski azaltmak için araştırma süresine tarih sınırı konulmuştur.

---

### Daily Scrum 2

**Tarih:** 01.07.2026

**Toplantı Özeti:**

İkinci Scrum toplantısında ekip genelinde ortaya konan proje fikirleri detaylı şekilde değerlendirilmiştir. Fikirlerin uygulanabilirliği, veri bulunabilirliği, yapay zeka kullanımı, ürünleşme potansiyeli ve bootcamp süresi içerisinde tamamlanabilirliği üzerine tartışılmıştır.

Mevcut fikirlerin doğrudan seçilmesi yerine, bu fikirlerden daha bütünsel ve geniş kapsamlı bir proje vizyonu çıkarılıp çıkarılamayacağı üzerine beyin fırtınası yapılmıştır. Projenin stratejik yönünü netleştirmek için elde edilen verilerin ve potansiyel veri setlerinin analiz sürecine başlanmasına karar verilmiştir.

**Alınan Kararlar:**

- Mevcut proje fikirleri uygulanabilirlik açısından karşılaştırılacak.
- Her fikir için veri seti bulunabilirliği kontrol edilecek.
- AI/modelleme tarafı güçlü olan fikirler önceliklendirilecek.
- Veri analizinden elde edilecek sonuçlar, projenin nihai yönünü belirleyecek.
- Seçilecek projenin hem teknik olarak uygulanabilir hem de ürünleşebilir olmasına dikkat edilecek.

**Blocker / Risk:**

- Bazı proje fikirleri özgün olsa da yeterli veri seti bulunamama riski taşımaktadır.
- Bu nedenle proje seçiminde veri bulunabilirliği temel kriterlerden biri olarak belirlenmiştir.

---

### Daily Scrum 3

**Tarih:** 03.07.2026

**Toplantı Özeti:**

Üçüncü Scrum toplantısında ekip olarak üzerinde durulan potansiyel projelerin veri setleri detaylı şekilde incelenmiştir. Yapılan değerlendirmelerde her proje fikri; veri bulunabilirliği, model eğitilebilirliği, metriklerin gösterilebilirliği, dashboard geliştirme potansiyeli ve bootcamp süresinde tamamlanabilirliği açısından karşılaştırılmıştır.

Bu incelemeler sonucunda ekip ortak kararıyla **EcoShield AI - Fraud Detection** projesi üzerinde çalışılmasına karar verilmiştir. Projenin finansal dolandırıcılık tespiti üzerine kurulması, veri setlerinin erişilebilir olması ve modelleme sürecinde ROC-AUC, PR-AUC, recall, precision, F1-score ve confusion matrix gibi metriklerin net şekilde gösterilebilmesi nedeniyle bu fikir ön plana çıkmıştır.

Bir sonraki toplantıda görev dağılımı yapılarak veri analizi, modelleme, dokümantasyon ve arayüz geliştirme süreçlerine başlanması kararlaştırılmıştır.

**Alınan Kararlar:**

- Proje fikri olarak **EcoShield AI - Fraud Detection** seçildi.
- İlk veri seti olarak Credit Card Fraud Detection veri setiyle başlanmasına karar verildi.
- Fraud detection probleminin class imbalance içerdiği ve bu nedenle özel metriklerle değerlendirilmesi gerektiği belirlendi.
- Sonraki toplantıda görev dağılımı yapılacak.
- İlk aşamada EDA ve proje dokümantasyonu hazırlanacak.

**Blocker / Risk:**

- Fraud detection veri setleri ciddi class imbalance içerdiği için accuracy metriği tek başına yeterli olmayacaktır.
- Projenin klasik fraud detection projesi gibi görünmemesi için iki aşamalı hafif model + ağır model mimarisi ve compute-saving yaklaşımı özellikle vurgulanacaktır.

---

## Ürün Durumu

Sprint 1 sonunda ürün henüz çalışan bir dashboard veya tamamlanmış modelleme sistemi değildir. Bu sprintte ürünün temel veri analizi ve proje planlama altyapısı oluşturulmuştur.

Bu sprint sonunda elde edilen durum:

- Proje fikri olarak EcoShield AI seçildi.
- Repo ve dokümantasyon yapısı oluşturuldu.
- Credit Card Fraud Detection veri seti seçildi.
- Veri seti projeye eklendi.
- EDA notebook oluşturuldu.
- Veri setinin satır/sütun yapısı incelendi.
- Fraud / normal işlem dağılımı analiz edildi.
- Eksik değer ve duplicate kontrolü yapıldı.
- Class imbalance problemi tespit edildi.
- Class distribution, Amount distribution ve Time distribution grafikleri oluşturuldu.
- EDA özeti `assets/sprint-1/eda_summary.txt` dosyasına kaydedildi.

Sprint 1 kapsamında oluşturulan teknik çıktılar:

```text
notebooks/01_eda.ipynb
assets/sprint-1/class_distribution.png
assets/sprint-1/amount_distribution.png
assets/sprint-1/time_distribution.png
assets/sprint-1/eda_summary.txt
```

Sprint 1 EDA çıktıları:

![Class Distribution](/assets/sprint-1/class_distribution.png)

![Amount Distribution](/assets/sprint-1/amount_distribution.png)

![Time Distribution](/assets/sprint-1/time_distribution.png)

EDA sonucunda elde edilen temel bulgular:

| Metrik | Değer |
|---|---:|
| Veri seti boyutu | 284,807 satır / 31 sütun |
| Normal işlem sayısı | 284,315 |
| Fraud işlem sayısı | 492 |
| Fraud oranı | %0.1727 |
| Eksik değer bulunan sütun sayısı | 0 |
| Duplicate satır sayısı | 1,081 |
| Normal/Fraud oranı | 577.88 |

Bu sprintte model eğitimi yapılmamıştır. Baseline modelleme, train/test split ve performans metrikleri Sprint 2’ye bırakılmıştır.

---

## Sprint Review

Sprint 1 sonunda EcoShield AI projesinin temel kapsamı belirlenmiş ve finansal dolandırıcılık tespiti problemi üzerine çalışılmasına karar verilmiştir. Ekip, farklı proje fikirlerini veri bulunabilirliği, model eğitilebilirliği, ürünleşme potansiyeli ve bootcamp süresinde tamamlanabilirlik açısından değerlendirmiştir.

Yapılan değerlendirmeler sonucunda fraud detection probleminin hem veri açısından erişilebilir hem de modelleme açısından ölçülebilir olduğu görülmüştür. Bu nedenle ilk aşamada Credit Card Fraud Detection veri setiyle başlanmasına karar verilmiştir.

Tamamlanan işler:

- Proje fikri netleştirildi.
- Hedef problem alanı belirlendi.
- Product backlog oluşturuldu.
- Sprint 1 backlog hazırlandı.
- Repo klasör yapısı oluşturuldu.
- Dokümantasyon dosyaları hazırlandı.
- Credit Card Fraud Detection veri seti seçildi.
- EDA notebook oluşturuldu.
- Veri setinin temel yapısı incelendi.
- Fraud / normal işlem dağılımı analiz edildi.
- Eksik değer ve duplicate kontrolü yapıldı.
- Class imbalance problemi tespit edildi.
- EDA çıktıları görsel ve metinsel olarak kaydedildi.

Eksik kalan / sonraki sprinte aktarılan işler:

- Train/test split yapılması
- Logistic Regression baseline modelinin eğitilmesi
- Random Forest / LightGBM gibi ikinci model denemeleri
- Confusion matrix ve model metriklerinin çıkarılması
- SMOTE ve class weight karşılaştırmaları
- Threshold tuning
- İki aşamalı hafif model + ağır model mimarisi
- Dashboard’un çalışan hale getirilmesi
- Compute-saving metriğinin hesaplanması

---

## Sprint Retrospective

### İyi Gidenler

- Proje fikri seçilmeden önce farklı temalar ve veri setleri karşılaştırıldığı için daha bilinçli bir proje seçimi yapılabildi.
- Proje fikri erken aşamada netleştirildi.
- Veri bulunabilirliği açısından uygulanabilir bir proje seçildi.
- Fraud detection problemi teknik olarak uygulanabilir bulundu.
- Repo ve dokümantasyon yapısı oluşturuldu.
- Product backlog ve sprint backlog hazırlandı.
- EDA ile veri setinin temel yapısı anlaşılmaya başlandı.

### Zorlayan Noktalar

- Fraud detection probleminin ciddi class imbalance içerdiği görüldü.
- Accuracy metriğinin bu problem için tek başına yeterli olmayacağı anlaşıldı.
- Projenin klasik fraud detection gibi görünmemesi için iki aşamalı enerji-verimli mimarinin daha net vurgulanması gerektiği fark edildi.
- IEEE-CIS Fraud Detection veri setinin daha gerçekçi fakat daha karmaşık olduğu görüldü. Bu nedenle ilk sprintte daha hızlı analiz edilebilir Credit Card Fraud Detection veri setiyle başlanmasına karar verildi.

### Bir Sonraki Sprintte İyileştirilecekler

- EDA sonucunda tespit edilen class imbalance problemi modelleme sürecinde dikkate alınacak.
- Train/test split işlemi stratified şekilde yapılacak.
- İlk baseline model olarak Logistic Regression eğitilecek.
- Accuracy yerine recall, precision, F1-score, ROC-AUC ve PR-AUC metrikleri birlikte değerlendirilecek.
- Random Forest veya LightGBM ile ikinci bir model denemesi yapılacak.
- SMOTE, class weight ve threshold tuning yöntemleri Sprint 2 kapsamında test edilecek.
- Model çıktıları dashboard’da gösterilebilecek hale getirilecek.
- Sprint board ekran görüntüsü ve ürün durumu görselleri repo’ya eklenecek.

---

## Sprint 1 Teknik Minimum Hedefler

Sprint 1 sonunda teknik olarak şu çıktıların oluşturulması hedeflenmiştir:

1. Veri seti seçildi.
2. EDA notebook oluşturuldu.
3. Veri setinin satır/sütun yapısı incelendi.
4. Fraud / normal işlem dağılımı gösterildi.
5. Eksik değer kontrolü yapıldı.
6. Duplicate kontrolü yapıldı.
7. Class distribution grafiği oluşturuldu.
8. Amount distribution grafiği oluşturuldu.
9. Time distribution grafiği oluşturuldu.
10. EDA özeti oluşturuldu.

Modelleme, train/test split ve performans metrikleri Sprint 2 kapsamına aktarılmıştır.

---

## Sprint 1 Sonuç Özeti

Sprint 1 kapsamında EcoShield AI projesinin temel yönü belirlenmiş ve finansal dolandırıcılık tespiti problemi üzerine ilerlenmesine karar verilmiştir. Bu sprintte, fraud detection probleminin veri yapısını hızlıca anlamak ve class imbalance durumunu net şekilde gözlemlemek amacıyla Credit Card Fraud Detection veri seti üzerinden ilk EDA çalışması yapılmıştır.

Credit Card Fraud Detection veri seti Sprint 1’de problem doğrulama ve hızlı EDA için kullanılmıştır. Ancak projenin sonraki aşamalarında daha gerçekçi, daha kapsamlı ve daha fazla değişken içeren IEEE-CIS Fraud Detection veri seti de denenecektir. Sprint 2’de IEEE-CIS veri setinin `train_transaction` ve `train_identity` dosyaları incelenerek preprocessing, eksik değer yönetimi, kategorik değişken dönüşümü ve modelleme sürecine uygunluğu değerlendirilecektir.

Bu sprintte elde edilen çıktılar, Sprint 2’de geliştirilecek train/test split, baseline modelleme, class imbalance yöntemleri, threshold tuning ve iki aşamalı hafif model + ağır model mimarisi için temel oluşturacaktır.