# Basit Hashing Algoritması

Bu algoritma, 256 bit'lik bir state başlatır ve girdinin her bir baytı üzerinde çalışarak bu durumu karıştırır. İşlem, `XOR`, `toplama`, `çarpma` ve `rotl` (bitsel sola döndürme) gibi bir dizi bitsel işlemi içerir. Son olarak, ek karıştırma turları uygulanır ve nihai durum 32 baytlık bir onaltılık (hexadecimal) dize olarak döndürülür.

## Örnek kullanım

```Python
from hash import chain_hash_64

text="Hello World"
hash=chain_hash_64(text)

print(f"Hash: {hash}")
```
