import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
yorumlar_listesi = []
unique_comments = set()  # Yorumları saklamak için bir set
def log(log_text):
    log_text = " ➾ " + log_text
    print(log_text)
    log_file = open("trendyol14_yorumbotu.csv", "a", encoding='utf-8')
    log_file.write(log_text + "\n")
    log_file.close()
    
def clean_text(text):
    cleaned_text = re.sub(r'[^\w\s]', '', text)  # Sadece harf, rakam, boşluk ve alt çizgiyi koru
    return cleaned_text
global_delay = 0.5
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
urun_url = input("Ürün URL'sini girin: ")
try:
    driver.get(urun_url + "/yorumlar")
    time.sleep(5)
    while True:
        try:
            # Scroll işlemi sonrası yüklenen yorumları çekmek için bekleme
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="rating-and-review-app"]//p')))
            yorumlar = driver.find_elements("xpath", '//*[@id="rating-and-review-app"]//p')
            for yorum in yorumlar:
                cleaned_yorum = clean_text(yorum.text)
                if cleaned_yorum not in unique_comments:
                    yorumlar_listesi.append(cleaned_yorum)
                    unique_comments.add(cleaned_yorum)
                    log('Yorum: ' + cleaned_yorum)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(global_delay)
        except Exception as e:
            log('Hata: ' + str(e))
            log('Tüm yorumlar alındı.')
            break
except Exception as e:
    log('Hata: ' + str(e))
    log('Program sonlandı')
    driver.quit()
    exit()
driver.quit()
