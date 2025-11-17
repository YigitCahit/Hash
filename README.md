# Basit Hashing Araçları

Bu depo, özel bir 256 bit durum kullanan `chain_hash_64` fonksiyonunu ve bu fonksiyonun üstüne kurulu yardımcı araçları içerir. Algoritma, girdinin her baytını `XOR`, toplama, çarpma ve `rotl` (bitsel sola döndürme) işlemleriyle karıştırır, ardından 32 baytlık bir hexadecimal çıktı üretir.

## Python içinden kullanım

```python
from hash import chain_hash_64

text = "Hello World"
digest = chain_hash_64(text)

print(f"Hash: {digest}")
```

## Komut satırı yardımcıları

Depoda iki küçük CLI bulunuyor:

- `app.py`: Konsola girilen metnin hash değerini üretir.
- `file_hash.py`: Belirtilen dosyanın hash değerini hesaplar.

Çalıştırmak için:

```powershell
python app.py
python file_hash.py
```

## Blockchain benzeri metin zinciri

`text_chain.py`, her metin girdisini bir önceki bloğun hash'i ile birbirine bağlayarak basit bir zincir dosyası (`text_chain.json`) tutar. Zincirdeki her blok şu alanları içerir:

- `index`: Sıra numarası
- `timestamp`: UTC ISO zaman damgası
- `text`: Saklanmak istenen metin
- `prev_hash`: Bir önceki bloğun hash değeri
- `hash`: Bloğun kendi hash değeri (metin + metadata üzerinden hesaplanır)

Desteklenen alt komutlar:

```powershell
python text_chain.py reset    # Yeni genesis bloğu oluştur
python text_chain.py add "Merhaba dünya"  # Zincire yeni metin ekle
python text_chain.py list     # Zincirdeki blokları sırayla göster
python text_chain.py verify   # Zincir bütünlüğünü kontrol et
```

`reset` komutu zinciri sıfırlar, `add` zincirin sonuna yeni bir blok ekler, `list` özet bir çıktı verir, `verify` ise hash ve `prev_hash` alanlarını yeniden hesaplayarak zincirin bozulmadığını doğrular.
