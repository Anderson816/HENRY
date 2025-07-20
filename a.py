import time, json, random, string, re
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By

def random_username():
    return "gh" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

USERNAME = random_username()
PASSWORD = "Str0ngP@ssw0rd123!"
EMAIL = None  # Will be fetched from temp-mail

def create_browser():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")  # For VPS
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return uc.Chrome(options=options)

def get_temp_mail(driver):
    print("🌐 Fetching temp mail address...")
    driver.get("https://temp-mail.org/en/")
    time.sleep(5)
    email_input = driver.find_element(By.ID, "mail")
    temp_email = email_input.get_attribute("value")
    print(f"📨 Temp email: {temp_email}")
    return temp_email

def github_signup(driver, email):
    print(f"🚀 Creating GitHub account: {USERNAME}")
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://github.com/join")
    time.sleep(4)

    driver.find_element(By.ID, "user_login").send_keys(USERNAME)
    driver.find_element(By.ID, "user_email").send_keys(email)
    driver.find_element(By.ID, "user_password").send_keys(PASSWORD)
    time.sleep(1)

    driver.find_element(By.XPATH, "//button[contains(text(),'Continue')]").click()
    time.sleep(6)

    print("📥 Waiting for GitHub email...")
    driver.switch_to.window(driver.window_handles[0])
    for _ in range(60):
        time.sleep(3)
        driver.refresh()
        try:
            inbox_list = driver.find_elements(By.CSS_SELECTOR, ".inbox-dataList li")
            for mail in inbox_list:
                if "GitHub" in mail.text:
                    mail.click()
                    time.sleep(3)
                    iframe = driver.find_element(By.ID, "iframeMail")
                    driver.switch_to.frame(iframe)
                    body = driver.find_element(By.TAG_NAME, "body").text
                    driver.switch_to.default_content()
                    match = re.search(r"\b\d{6}\b", body)
                    if match:
                        code = match.group(0)
                        print(f"✅ GitHub code received: {code}")
                        driver.switch_to.window(driver.window_handles[1])
                        driver.find_element(By.ID, "email-verification-code-input").send_keys(code)
                        driver.find_element(By.XPATH, "//button[contains(text(),'Verify')]").click()
                        time.sleep(5)
                        return True
        except Exception:
            continue
    print("❌ GitHub email code not found.")
    return False

def github_login(driver):
    print("🔐 Logging into GitHub...")
    driver.get("https://github.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "login_field").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "commit").click()
    time.sleep(3)

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
    except Exception:
        pass
    print("✅ Railway account created and logged in!")

def save_cookies(driver):
    cookies = driver.get_cookies()
    with open("cookies.json", "w") as f:
        json.dump(cookies, f)
    print("💾 Cookies saved to cookies.json")

if __name__ == "__main__":
    driver = create_browser()
    EMAIL = get_temp_mail(driver)

    if github_signup(driver, EMAIL):
        github_login(driver)
        railway_signup(driver)
        save_cookies(driver)
    else:
        print("❌ GitHub signup failed.")

    driver.quit()
