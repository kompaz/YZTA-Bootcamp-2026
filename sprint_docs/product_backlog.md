# EcoShield AI - Product Backlog

| No | User Story | Öncelik | Durum |
|---|---|---:|---|
| PB-1 | Kullanıcı olarak işlem verilerini sisteme yükleyebilmek istiyorum. | Yüksek | Planlandı |
| PB-2 | Sistem olarak yüklenen veriyi temizleyip model eğitimine hazır hale getirmeliyim. | Yüksek | Devam ediyor |
| PB-3 | Kullanıcı olarak fraud ve normal işlem dağılımını görebilmek istiyorum. | Yüksek | Devam ediyor |
| PB-4 | Sistem olarak baseline fraud detection modeli eğitmeliyim. | Yüksek | Devam ediyor |
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

---

## Backlog Dağıtma Mantığı

Product backlog, ürünün veri hazırlama, modelleme, değerlendirme, iki aşamalı mimari ve dashboard geliştirme ihtiyaçlarına göre oluşturulmuştur.

İlk sprintte temel veri analizi ve baseline modelleme görevlerine öncelik verilmiştir. Sonraki sprintlerde class imbalance yöntemleri, iki aşamalı model mimarisi, dashboard ve compute-saving metriği geliştirilecektir.

---

## Önceliklendirme Kriterleri

Backlog maddeleri şu kriterlere göre önceliklendirilmiştir:

- MVP için zorunlu olması
- Modelleme sürecine temel oluşturması
- Demo sırasında gösterilebilir olması
- Yapay zeka katkısını güçlendirmesi
- Ürün bütünlüğüne katkı sağlaması