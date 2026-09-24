# pdf-text-remover

PDF dosyaları içinden belirli bir metni veya belirli bir fontla yazılmış tüm yazıları silmek için yazılmış küçük Python betikleri. [PyMuPDF](https://pymupdf.readthedocs.io/) kütüphanesini kullanır ve düzenlenen içeriği redaksiyon (redaction) yöntemiyle kalıcı olarak kaldırır.

## Özellikler

- **İçeriğe göre silme** — PDF içinde geçen belirli bir metni arar ve o bölgeleri redakte eder (görünmez/şeffaf hale getirir).
- **Fonta göre silme** — Belirttiğiniz font adını içeren tüm metin bloklarını PDF içerik akışından (content stream) doğrudan kaldırır.
- **Bağlantı (link) temizleme** — İsteğe bağlı olarak PDF içindeki tüm link anotasyonlarını da siler.
- **Font/metin tespit aracı** — Bir PDF'teki metinlerin hangi fontla, hangi boyutla yazıldığını ve sayfadaki görsel/çizim/anotasyon sayısını gösterir.

## Dosyalar

| Dosya | Ne işe yarar |
|---|---|
| `delete_text_from_content.py` | Girdiğiniz metni PDF'te arar, bulduğu her yeri redakte edip siler. |
| `delete_text_from_font.py` | Girdiğiniz font adını taşıyan tüm metin bloklarını PDF içerik akışından kaldırır. |
| `find_font.py` | Bir PDF'in ilk sayfasındaki görsel/çizim/anotasyon sayısını ve aratılan metnin font adı ile boyutunu gösterir (hedef font adını bulmak için kullanışlıdır). |

## Gereksinimler

- Python 3
- [PyMuPDF](https://pypi.org/project/PyMuPDF/)

Kurulum:

```bash
pip install pymupdf
```

## Kullanım

### 1. Belirli bir metni silme

```bash
python delete_text_from_content.py
```

Çalıştırdığınızda sırasıyla:
1. `Pdf name:` — işlenecek PDF dosyasının adı/yolu
2. `Target text:` — PDF içinden silinecek metin
3. `Remove links? (y/n):` — link anotasyonlarının da silinip silinmeyeceği

sorulur. Sonuç `deleted.pdf` olarak kaydedilir; her sayfada kaç eşleşme silindiği ve kaç link kaldırıldığı ekrana yazdırılır.

### 2. Belirli bir fontla yazılmış tüm metni silme

Önce hangi fontu hedefleyeceğinizi bilmiyorsanız `find_font.py` ile PDF içindeki metinlerin font adlarını görebilirsiniz:

```bash
python find_font.py
```

`Pdf:` ve `Search Text:` girildikten sonra, aranan metnin geçtiği her konumdaki font adı ve boyutu listelenir.

Font adını öğrendikten sonra:

```bash
python delete_text_from_font.py
```

Sorulan bilgiler:
1. `Pdf name:` — işlenecek PDF dosyasının adı/yolu
2. `Target font name:` — silinecek metinlerin font adı (tam eşleşme değil, adın **içinde geçmesi** yeterli)
3. `Remove links? (y/n):` — link anotasyonlarının da silinip silinmeyeceği

Sonuç yine `deleted.pdf` olarak kaydedilir; kaç sayfanın değiştiği, kaç byte'lık içerik silindiği ve kaç link kaldırıldığı raporlanır.

> **Not:** Font tabanlı silme, PDF içerik akışını (content stream) doğrudan işler; bu yöntem redaksiyona göre daha "cerrahi" olsa da PDF yapısına bağlı olarak bazı özel/karmaşık PDF'lerde beklenmedik sonuçlar verebilir. Önemli dosyalarda önce bir kopya üzerinde deneyin.

## Lisans

Bu proje [MIT lisansı](LICENSE) ile lisanslanmıştır.
