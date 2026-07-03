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