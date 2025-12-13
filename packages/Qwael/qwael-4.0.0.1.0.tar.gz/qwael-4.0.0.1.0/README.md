# Qwael

Qwael, Google Drive üzerinde veri yönetimini kolaylaştıran ve basit işlevleri Python ile hızlıca kullanmanıza olanak sağlayan bir kütüphanedir.  
Başlık ekleme, veri ekleme, silme, okuma ve kontrol etme gibi işlemleri tek satırda yapabilirsiniz.

## Kullanım

- Info

DRİVE.info()

- Control

DRİVE.Control(
    ID="dosya adı",
    ge="kontrol etmek istediğin metin",
    dax="başlık",
    dex_ID="metin başlığı"
    fop="onay değişkeni",
    es="drive hesap bilgileri",
    os="drive klasör id'si"
)

- give

DRİVE.give(
    dex="eklemek istediğin metin",
    dax="başlık",
    dex_ID="metin başlığı",
    fop="onay değişkeni",
    es="drive hesap bilgileri",
    os="drive klasör id'si"
)

- get

DRİVE.get(
    ID="dosya adı",
    Hup=("çekmek istediğin metinin olduğu başlığı","çekmek istediğin metin başlığı"),
    go="çekilen metinin ekleneceği değişken",
    es="drive hesap bilgileri",
    os="drive klasör id'si"
)

- delete

DRİVE.delete(
    ID="dosya adı",
    delete_header="silmek istediğin başlık",
    fop="Öney değişkeni",
    es="drive hesap bilgileri",
    os="drive klasör id'si"
)




### 🚀 Kurulum

```bash
pip install Qwael
