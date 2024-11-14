from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests 
# Chrome tarayıcısını başlat
driver = webdriver.Chrome()
driver.maximize_window()
SCROLL_PAUSE_TIME = 3
for page_num in range(2,164):
    # Web sayfasını aç
    website_url = f'https://www.hepsiburada.com/apple-airpods-2-nesil-kulaklik-mv7n2tu-a-apple-turkiye-garantili-pm-HB00000KXK5C-yorumlari?sayfa={page_num}'
    driver.get(website_url)
    # Sayfa yüklenene kadar bekle
    time.sleep(SCROLL_PAUSE_TIME)
    i = 1
    # JavaScript ile sayfayı aşağı kaydırma işlemi
    while i <= 10:
        son = driver.find_element(By.XPATH, '//*[@id="hermes-voltran-comments"]/div[6]/div[3]/div[1]/div['+str(i)+']')
        # JavaScript ile sayfayı sırayla resimin olduğu yere kaydırma
        driver.execute_script("arguments[0].scrollIntoView();", son)
        # Sayfanın yüklenmesini bekle
        time.sleep(SCROLL_PAUSE_TIME)
        i += 1
    # Tüm resim etiketlerini bul
    img_tags = driver.find_elements(By.XPATH, '//*[@id="hermes-voltran-comments"]/div[6]/div[3]/div[1]/div[*]/div[2]/div[4]/div[*]/figure/picture/div/img')
    # Resimleri indir ve kaydet
    for index, img in enumerate(img_tags):
        img_url = img.get_attribute('src').replace('s/0/80', 'usercontent-images-0')
        print(img_url)
        if img_url:
            try:
                response = requests.get(img_url)
                response.raise_for_status()  # HTTP hatalarını kontrol et
                
                # Dosya adını geçerli karakterlere dönüştür
                img_name = f'image_{index}.jpeg'
                img_path = f'C:\\Users\\MSI\\OneDrive\\Masaüstü\\VS_Code\\Pyhton\\{page_num}{img_name}'
                with open(img_path, 'wb') as img_file:
                    img_file.write(response.content)
                    print(f"{page_num}{img_name} indirildi.")
            except requests.exceptions.HTTPError as errh:
                print(f"HTTP Hatası: {errh}")
            except requests.exceptions.RequestException as err:
                print(f"Hata: {err}")
# Tarayıcıyı kapat
driver.quit()