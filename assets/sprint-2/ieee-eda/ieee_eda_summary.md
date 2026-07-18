# IEEE-CIS Fraud Detection — EDA Özeti

- Train transaction: 590,540 satır, 394 kolon
- Birleştirilmiş train: 590,540 satır, 436 kolon
- Normal işlem: 569,877
- Fraud işlem: 20,663
- Fraud oranı: 3.4990%
- Normal/Fraud oranı: 27.58
- Identity kapsama oranı: 24.42%
- Duplicate satır: 0
- %50 üzeri eksik kolon: 214
- %90 üzeri eksik kolon: 12

## İlk değerlendirme

- Veri seti ciddi class imbalance içermektedir.
- Accuracy tek başına yeterli değildir.
- Identity bilgisi bütün işlemlerde bulunmamaktadır.
- Eksik oranı yüksek kolonlar model denemesi yapılmadan doğrudan silinmemelidir.
- Modelleme aşamasında PR-AUC, recall, precision, F1 ve confusion matrix birlikte değerlendirilmelidir.