from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests 
# Chrome tarayıcısını başlat
driver = webdriver.Chrome()
# Web sayfasını aç
website_url = 'https://ikincielbeyazesya.istanbul/urun-kategori/2-el-camasir-makinesi/page/3/?gclid=EAIaIQobChMIvfH73Y2v_wIVrwUGAB0LtQUyEAAYAiAAEgI8WvD_BwE'
driver.get(website_url)
# Sayfa yüklenene kadar bekle
time.sleep(2)
# JavaScript ile sayfayı aşağı kaydırma işlemi
SCROLL_PAUSE_TIME = 1
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Sayfayı en aşağı kaydır
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Sayfanın yüklenmesini bekle
    time.sleep(SCROLL_PAUSE_TIME)
    # Yeni yüklenen resimleri kontrol et
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
# Tüm resim etiketlerini bul
img_tags = driver.find_elements(By.TAG_NAME, 'img')
# Resimleri indir ve kaydet
for index, img in enumerate(img_tags):
    img_url = img.get_attribute('src')
    if img_url:
        try:
            response = requests.get(img_url)
            response.raise_for_status()  # HTTP hatalarını kontrol et
            
            # Dosya adını geçerli karakterlere dönüştür
            img_name = f'image_{index}.jpeg'
            img_path = f'C:\\Users\\MSI\\OneDrive\\Masaüstü\\resim\\{img_name}'
            with open(img_path, 'wb') as img_file:
                img_file.write(response.content)
                print(f"{img_name} indirildi.")
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Hatası: {errh}")
        except requests.exceptions.RequestException as err:
            print(f"Hata: {err}")
# Tarayıcıyı kapat
driver.quit()
