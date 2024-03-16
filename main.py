import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

def configure_webdriver(open_browser, download_dir):
    options = webdriver.ChromeOptions()

    if not open_browser:
        options.add_argument("--headless")

    prefs = {"download.default_directory": download_dir}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )
    return driver


def download_tiktok_video(urls, filename, path):
    driver = configure_webdriver(True, path)
    for url in urls:
        try :
            driver.get("https://snaptik.app/")
            input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "link-input"))
            )
            input.send_keys(url)
            btn = driver.find_element(By.CLASS_NAME, "button-go")
            btn.click()
            btn = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "download-file"))
            )
            btn.click()
            time.sleep(5)
        except:
            pass    
    driver.quit()


def getPath(name):
    path = os.path.join("E:\\Freelance Dev Projects\\tiktok\\videos", name)
    return path


def read_csv_files(directory):
    if not os.path.isdir(directory):
        print(f"The directory '{directory}' does not exist.")
        return

    csv_files = [file for file in os.listdir(directory) if file.endswith(".csv")]
    for csv_file in csv_files:
        file_path = os.path.join(directory, csv_file)
        print(f"Reading file: {file_path}")

        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            urls = [row[0] for row in reader]
            urls.pop(0)
            urls = [item for item in urls if item != ""]
            filtered_urls = [entry for entry in urls if "photo" not in entry.lower()]
            download_tiktok_video(
                filtered_urls,
                "video.mp4",
                getPath(os.path.basename(file_path)).split(".")[0],
            )


directory_path = "E:\\Freelance Dev Projects\\tiktok\\userCSVs"
read_csv_files(directory_path)
