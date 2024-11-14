from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
liste = []
for page_number in range(1, 11):  # Örnek olarak 1'den 10'a kadar sayfa numaralarını ziyaret ediyoruz
    url = f"https://www.amazon.com.tr/JBLC100SIUBLK-C100-JBL-Kulak-Kulakl%C4%B1k/product-reviews/B01DEWVZ2C/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1={page_number}"
    
    response = requests.get(url)
    html_icerigi = response.content
    soup = BeautifulSoup(html_icerigi, "html.parser")
    yorumlar = soup.find_all("span", {"data-hook": "review-body"})
    
    for yorum in yorumlar:
        yorum = (yorum.text).strip("\n").strip()
        # Gereksiz karakterleri temizleme
        yorum = re.sub(r'\s+', ' ', yorum)  # Boşlukları temizler
        yorum = re.sub(r'[^\w\s]', '', yorum)  # Özel karakterleri temizler
        # Tüm Türkçe karakterleri düzeltme
        turkce_karakterler = {'Ç': 'C', 'ç': 'c', 'Ğ': 'G', 'ğ': 'g', 'İ': 'I', 'ı': 'i', 'Ö': 'O', 'ö': 'o', 'Ş': 'S', 'ş': 's', 'Ü': 'U', 'ü': 'u'}
        for key, value in turkce_karakterler.items():
            yorum = yorum.replace(key, value)
        liste.append([yorum])
df = pd.DataFrame(liste, columns=["yorum1"])
print(df)
# CSV'ye aktarma
df.to_csv('veriler.csv', index=False, encoding='utf-8-sig')  # 'veriler.csv' adında bir CSV dosyası oluşturur
