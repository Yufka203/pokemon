# Pokémon Discord Bot ⚔️🧙‍♂️

**Bu proje**, Discord üzerinde Pokémon temalı bir oyun botudur. Oyuncular kendi Pokémonlarını oluşturabilir, onları besleyebilir, diğer oyunculara karşı savaşabilir ve Pokémonlarının sağlık durumunu kontrol edebilirler. Çok biçimlilik (polymorphism) kullanılarak farklı Pokémon türlerine özel davranışlar eklenmiştir (örneğin, Fighter ve Wizard sınıfları).

---

## 🚀 Özellikler

- 🎮 `/go [tür]` komutuyla farklı türde Pokémon oluşturma (normal, fighter, wizard)
- 🍖 `!feed` komutuyla Pokémonunuzu besleyip sağlığını artırma
- ⚔️ `!attack @kullanıcı` komutuyla başka oyuncuların Pokémonlarına saldırma
- 📊 `!pokebilgi` komutuyla kendi Pokémonunuzun istatistiklerini görüntüleme
- ⏳ Beslenme zamanı kontrolü ile gerçekçi sağlık yenileme sistemi

---

## ⚙️ Kurulum

1. Python 3.8+ yüklü olduğundan emin olun  
2. Gerekli kütüphaneleri yükleyin:  
```bash
pip install -r requirements.txt
.env dosyanıza Discord bot tokenınızı ekleyin:
DISCORD_TOKEN=bot_tokenınız_burada

Botu çalıştırın:
python main.py

🛠️ Kullanım
/go komutuyla Pokémon oluşturun. Örnek: /go fighter

!feed komutuyla Pokémonunuzu besleyin.

!attack @rakip komutuyla savaşa girin.

!pokebilgi ile Pokémonunuzun istatistiklerini görün.

🌟 Katkıda Bulunma
Projeye katkı sağlamak, hataları bildirmek veya yeni özellikler önermek için pull request gönderebilir ya da issue açabilirsiniz. Hep birlikte daha eğlenceli hale getirelim! 💪

📜 Lisans
Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için LICENSE dosyasına bakabilirsiniz.

🧡 Teşekkürler
Projeyi kullandığınız ve desteklediğiniz için teşekkürler! Herhangi bir sorunuz veya öneriniz için benimle iletişime geçebilirsiniz.

