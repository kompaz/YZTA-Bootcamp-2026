# Sprint 1 — EcoShield AI

## Sprint Amacı

Bu sprintte EcoShield AI projesinin temel kapsamını belirlemek, veri setini seçmek, ilk veri analizlerini yapmak ve baseline fraud detection modeli için altyapı oluşturmak hedeflenmiştir.

Sprint 1’in ana odağı:

- Proje fikrinin netleşmesi
- Veri setinin seçilmesi
- EDA yapılması
- Fraud / normal işlem dağılımının analiz edilmesi
- Class imbalance probleminin tespit edilmesi
- Baseline modelleme altyapısının hazırlanması
- Sprint board ve dokümantasyon düzeninin oluşturulması

---

## Sprint 1 Backlog

| No | Sprint Task | Sorumlu | Durum |
|---|---|---|---|
| SB-1 | Proje fikrinin netleştirilmesi | Tüm ekip | Tamamlandı |
| SB-2 | Proje repo yapısının oluşturulması | Developer | Tamamlandı |
| SB-3 | `docs` klasörünün ve sprint dokümanlarının hazırlanması | Developer | Tamamlandı |
| SB-4 | Kullanılacak veri setlerinin araştırılması | Tüm ekip | Tamamlandı |
| SB-5 | Credit Card Fraud Detection veri setinin seçilmesi | Tüm ekip | Tamamlandı |
| SB-6 | Veri setinin `data/raw` klasörüne eklenmesi | Developer | Tamamlandı |
| SB-7 | EDA notebook dosyasının oluşturulması | Developer | Planlandı |
| SB-8 | Veri setinin satır/sütun yapısının incelenmesi | Developer | Planlandı |
| SB-9 | Fraud / normal işlem dağılımının analiz edilmesi | Developer | Planlandı |
| SB-10 | Eksik değer ve duplicate kontrolü yapılması | Developer | Planlandı |
| SB-11 | Class distribution grafiğinin oluşturulması | Developer | Planlandı |
| SB-12 | Train/test split hazırlığının yapılması | Developer | Planlandı |
| SB-13 | Baseline Logistic Regression modeli için notebook hazırlanması | Developer | Planlandı |
| SB-14 | Sprint board ekran görüntüsünün eklenmesi | Scrum Master | Planlandı |
| SB-15 | Ürün durumu ekran görüntülerinin eklenmesi | Tüm ekip | Planlandı |

---

## Story Seçimleri ve Backlog Dağılımı

Sprint 1’de ürünün temel teknik altyapısını oluşturacak görevler seçilmiştir.

Bu sprintte öncelik, final dashboard’u veya gelişmiş modeli tamamlamak değil; veri setini anlamak, fraud detection problemini doğru tanımlamak ve baseline modelleme için temel hazırlamaktır.

Bu nedenle Sprint 1’de şu işlere öncelik verilmiştir:

- Veri setinin seçilmesi
- Repo ve klasör yapısının kurulması
- EDA notebook’unun hazırlanması
- Fraud / normal işlem dağılımının incelenmesi
- Class imbalance probleminin ortaya konması
- Baseline modelleme için hazırlık yapılması

Bu seçimlerin nedeni, Sprint 2’de geliştirilecek SMOTE / class weight / threshold tuning ve iki aşamalı model mimarisinin sağlam bir veri analizi üzerine kurulmasıdır.

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
- İlk aşamada EDA, baseline model ve proje dokümantasyonu hazırlanacak.

**Blocker / Risk:**

- Fraud detection veri setleri ciddi class imbalance içerdiği için accuracy metriği tek başına yeterli olmayacaktır.
- Projenin klasik fraud detection projesi gibi görünmemesi için iki aşamalı hafif model + ağır model mimarisi ve compute-saving yaklaşımı özellikle vurgulanacaktır.