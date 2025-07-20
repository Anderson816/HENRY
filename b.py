import time, re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

def create_browser():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return uc.Chrome(options=options)

def get_temp_mail(driver):
    print("🌐 Fetching temp mail...")
    driver.get("https://temp-mail.org/en/")
    time.sleep(5)
    email_element = driver.find_element(By.XPATH, '//div[@class="emailbox-input-wrapper"]//input')
    return email_element.get_attribute("value")

def github_signup(driver, email, username, password):
    print("🛠 Creating GitHub account...")
    driver.get("https://github.com/signup")
    time.sleep(5)

    # Fill email first
    email_box = driver.find_element(By.ID, "email")
    email_box.send_keys(email)
    email_box.send_keys(Keys.RETURN)
    time.sleep(4)

    # Enter username
    username_box = driver.find_element(By.ID, "login")
    username_box.send_keys(username)
    username_box.send_keys(Keys.RETURN)
    time.sleep(4)

    # Enter password
    pwd_box = driver.find_element(By.ID, "password")
    pwd_box.send_keys(password)
    pwd_box.send_keys(Keys.RETURN)
    time.sleep(4)

    # Opt out of newsletter
    try:
        no_newsletter = driver.find_element(By.XPATH, '//button[contains(text(), "Continue")]')
        no_newsletter.click()
        time.sleep(2)
    except:
        pass

    # Wait for code input
    print("📨 Waiting for 6-digit email code...")

def wait_for_code(driver):
    driver.get("https://temp-mail.org/en/")
    time.sleep(10)
    print("📬 Checking inbox...")
    try:
        email_link = driver.find_element(By.XPATH, '//ul[@class="mail-list"]/li[1]')
        email_link.click()
        time.sleep(3)
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
        body = driver.find_element(By.TAG_NAME, "body").text
        code = re.findall(r"\b\d{6}\b", body)[0]
        driver.switch_to.default_content()
        print(f"✅ Code received: {code}")
        return code
    except Exception as e:
        print("❌ Error getting code:", e)
        return None

def submit_code(driver, code):
    try:
        code_input = driver.find_element(By.ID, "otp")
        code_input.send_keys(code)
        code_input.send_keys(Keys.RETURN)
        print("🎉 GitHub account verified!")
    except Exception as e:
        print("❌ Could not submit code:", e)

if __name__ == "__main__":
    driver = create_browser()

    # Generate random username & password
    import random, string
    def r(n): return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

    USERNAME = "gh" + r(6)
    PASSWORD = r(12)
    EMAIL = get_temp_mail(driver)

    github_signup(driver, EMAIL, USERNAME, PASSWORD)
    time.sleep(15)
    CODE = wait_for_code(driver)
    if CODE:
        submit_code(driver, CODE)

    print(f"\n🔐 Account created:\nEmail: {EMAIL}\nUsername: {USERNAME}\nPassword: {PASSWORD}")
    time.sleep(10)
    driver.quit()
