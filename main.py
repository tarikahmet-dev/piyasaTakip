import requests

# --- TELEGRAM AYARLARI ---
TOKEN = "8608685627:AAHrJoD3PM16d6lZ5apkEH5yZ_JXXw2McH8"
CHAT_ID = "7701039624"

def altin_analist_botu():
    # Yahoo Finance JSON kaynakları
    ons_url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1m&range=1d"
    dolar_url = "https://query1.finance.yahoo.com/v8/finance/chart/USDTRY=X?interval=1m&range=1d"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        # 1. VERİLERİ ÇEK
        ons_res = requests.get(ons_url, headers=headers).json()['chart']['result'][0]['meta']
        dolar_res = requests.get(dolar_url, headers=headers).json()['chart']['result'][0]['meta']

        # 2. FİYATLARI HESAPLA (Bugün ve Dün)
        ons_simdi = ons_res['regularMarketPrice']
        ons_dun = ons_res['previousClose']
        
        dolar_simdi = dolar_res['regularMarketPrice']
        dolar_dun = dolar_res['previousClose']

        gram_simdi = (ons_simdi / 31.1035) * dolar_simdi
        gram_dun = (ons_dun / 31.1035) * dolar_dun

        # 3. DEĞİŞİMİ HESAPLA
        fark = gram_simdi - gram_dun
        yuzde_degisim = (fark / gram_dun) * 100
        durum_ikonu = "🚀" if fark > 0 else "🔻"

        # 4. OTOMATİK UZMAN YORUMU (Mantıksal Analiz)
        if yuzde_degisim > 0.5:
            yorum = "Piyasada 'güvenli liman' talebi artıyor. Yükseliş trendi korunuyor."
        elif yuzde_degisim < -0.5:
            yorum = "Kâr satışları baskın. Destek seviyeleri takip edilmeli."
        else:
            yorum = "Yatay seyir devam ediyor. Piyasalar yeni bir veri bekliyor."

        # 5. MESAJI HAZIRLA (Markdown formatında)
        mesaj_metni = (
            f"📊 *GÜNLÜK PİYASA ANALİZİ*\n"
            f"-------------------------------------\n"
            f"💰 *Gram Altın:* {gram_simdi:.2f} TL\n"
            f"{durum_ikonu} *Günlük Değişim:* {fark:+.2f} TL (%{yuzde_degisim:.2f})\n"
            f"-------------------------------------\n"
            f"🎙 *UZMAN NOTU:* {yorum}\n"
            f"-------------------------------------\n"
            f"_Veriler Yahoo Finance üzerinden anlık çekilmiştir._"
        )

        # 6. TELEGRAM'A GÖNDER
        telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": mesaj_metni,
            "parse_mode": "Markdown"
        }
        
        requests.post(telegram_url, data=payload)
        print("Analiz raporu Telegram'a başarıyla gönderildi kanka!")

    except Exception as e:
        print(f"❌ Kanka analiz yaparken hata oluştu: {e}")

# Çalıştır
altin_analist_botu()
