import time
import json
import random
import string
import re

import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By

def generate_username():
    return "user" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

USERNAME = generate_username()
PASSWORD = "StrongP@ssw0rd123"
EMAIL = None  # to be filled after scraping from temp-mail.org

# === Init Selenium ===
def create_browser():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    return uc.Chrome(options=options)

# === Get Temp Mail ===
def get_temp_mail(driver):
    driver.get("https://temp-mail.org/en/")
    time.sleep(5)
    email_elem = driver.find_element(By.ID, "mail")
    email = email_elem.get_attribute("value")
    print(f"📨 Temp mail: {email}")
    return email

# === Wait for GitHub email and extract 6-digit code ===
def wait_for_github_email(driver):
    print("📥 Waiting for GitHub email...")
    for _ in range(60):  # Wait up to 2 minutes
        time.sleep(3)
        driver.refresh()
        time.sleep(3)
        try:
            emails = driver.find_elements(By.CSS_SELECTOR, ".inbox-dataList li")
            for mail in emails:
                if "GitHub" in mail.text:
                    mail.click()
                    time.sleep(3)
                    body_frame = driver.find_element(By.ID, "iframeMail")
                    driver.switch_to.frame(body_frame)
                    body_text = driver.find_element(By.TAG_NAME, "body").text
                    driver.switch_to.default_content()
                    match = re.search(r"\b\d{6}\b", body_text)
                    if match:
                        code = match.group(0)
                        print(f"✅ Verification code: {code}")
                        return code
        except Exception as e:
            pass
    print("❌ Timeout: GitHub email not received.")
    return None

# === GitHub Signup ===
def github_signup(driver, email):
    print(f"\n🚀 Signing up GitHub as {USERNAME}")
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://github.com/join")
    time.sleep(4)

    driver.find_element(By.ID, "user_login").send_keys(USERNAME)
    driver.find_element(By.ID, "user_email").send_keys(email)
    driver.find_element(By.ID, "user_password").send_keys(PASSWORD)
    time.sleep(1)

    driver.find_element(By.XPATH, "//button[contains(text(),'Continue')]").click()
    time.sleep(5)

    code = wait_for_github_email(driver.switch_to.window(driver.window_handles[0]) or driver)
    if not code:
        driver.quit()
        return False

    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(By.ID, "email-verification-code-input").send_keys(code)
    driver.find_element(By.XPATH, "//button[contains(text(),'Verify')]").click()
    time.sleep(5)
    print("✅ GitHub account created & verified")
    return True

# === Railway Signup ===
def railway_signup(driver):
    print("🚉 Signing into Railway with GitHub...")
    driver.get("https://railway.app/login")
    time.sleep(3)
    driver.find_element(By.XPATH, "//button[contains(text(),'Continue with GitHub')]").click()
    time.sleep(6)

    try:
        if "Authorize Railway" in driver.page_source:
            driver.find_element(By.NAME, "authorize").click()
            time.sleep(3)
    except:
        pass

    print("✅ Railway account created and logged in!")

# === Save Cookies ===
def save_cookies(driver):
    cookies = driver.get_cookies()
    with open("cookies.json", "w") as f:
        json.dump(cookies, f)
    print("💾 Cookies saved to cookies.json")

# === Main ===
if __name__ == "__main__":
    driver = create_browser()
    EMAIL = get_temp_mail(driver)

    success = github_signup(driver, EMAIL)
    if success:
        driver.get("https://github.com/login")
        time.sleep(3)
        railway_signup(driver)
        save_cookies(driver)

    driver.quit()
