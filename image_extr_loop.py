
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
def download_images(url, folder_path):
    # Web sayfasını indir
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Resim etiketlerini bul
    img_tags = soup.find_all('img')
    # Her resmi indir ve kaydet
    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url:
            img_url = img_url.replace('amp;', '')  # 'amp;' ifadesini kaldırma
            img_url = urljoin(url, img_url)
            try:
                response = requests.get(img_url, headers=headers)
                response.raise_for_status()  # HTTP hatalarını kontrol et
                # Dosya adını geçerli karakterlere dönüştür
                img_name = ''.join(x for x in img_url.split('/')[-1] if x.isalnum() or x in ('.', '_'))
                img_name += '.jpeg'  # Uzantıyı .jpeg olarak ayarla
                img_path = f'{folder_path}/{img_name}'
                with open(img_path, 'wb') as img_file:
                    img_file.write(response.content)
                    print(f"{img_name} indirildi.")
            except requests.exceptions.HTTPError as errh:
                print(f"HTTP Hatası: {errh}")
            except requests.exceptions.RequestException as err:
                print(f"Hata: {err}")
# Örnek kullanım
website_url = 'https://www.google.com/search?q=pizza&sca_esv=590945601&rlz=1C1GCEU_trTR996TR996&tbm=isch&sxsrf=AM9HkKmJolLCkGX81hueCIqOsdOxTaM69g:1702574857220&source=lnms&sa=X&ved=2ahUKEwjzm8XMuY-DAxVM_7sIHdp-C0sQ_AUoAnoECAUQBA&biw=1396&bih=663&dpr=1.38'
download_folder = r'C:\Users\MSI\OneDrive\Masaüstü\resim'
download_images(website_url, download_folder)

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests 
from PIL import Image
from io import BytesIO
import os
# Chrome tarayıcısını başlat
driver = webdriver.Chrome()
download_directory = 'C:\\Users\\MSI\\OneDrive\\Masaüstü\\resimsıralı\\'
if not os.path.exists(download_directory):
    os.makedirs(download_directory)
for page_number in range(2, 23):  # 2'den 22'ye kadar sayfa numaralarını döngüye al
    website_url = f'https://www.gumtree.com/search?search_category=washing-machines&search_location=london&q=washing+machine&page={page_number}'
    driver.get(website_url)
    time.sleep(2)
    SCROLL_PAUSE_TIME = 1
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    img_tags = driver.find_elements(By.TAG_NAME, 'img')
    downloaded_count = 0
    for img in img_tags:
        img_url = img.get_attribute('src')
        if img_url and 'http' in img_url:
            try:
                response = requests.get(img_url, timeout=10)
                response.raise_for_status()
                img_name = f'image_{hash(img_url)}.jpeg'
                img_path = os.path.join(download_directory, img_name)
                with open(img_path, 'wb') as img_file:
                    img_file.write(response.content)
                    print(f"{img_name} indirildi.")
                    downloaded_count += 1
                img = Image.open(BytesIO(response.content))
                if img.format != 'JPEG':
                    img = img.convert("RGB")
                    img.save(img_path, "JPEG")
                    print(f"{img_name} JPEG formatına dönüştürüldü.")
            except requests.exceptions.HTTPError as errh:
                print(f"HTTP Hatası: {errh}")
            except requests.exceptions.RequestException as err:
                print(f"Hata: {err}")
            except Exception as e:
                print(f"Beklenmeyen bir hata oluştu: {e}")
            time.sleep(1)
    print(f"Sayfa {page_number} için toplamda {downloaded_count} resim indirildi.")
driver.quit()
