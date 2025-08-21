from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config.secrets import username, password


# ==============================
# CONFIGURATION
# ==============================
username = username
password = password

search_terms = [
    "Graduate React Developer",
    "Graduate Data Scientist",
    "Graduate Data Analyst",
    "Graduate Python Developer",
    "Graduate Front End Developer",
    "Data Analyst",
    "React Developer",
    "Python Developer",
    "Front End Developer",
    "Web Developer",
    "Nodejs Developer",
]


# ==============================
# FUNCTIONS
# ==============================


def login_LN(driver, username: str, password: str) -> None:
    """
    Logs into LinkedIn using provided credentials.
    """
    driver.get("https://www.linkedin.com/login")
    wait = WebDriverWait(driver, 15)

    try:
        # Wait until login form loads
        wait.until(EC.presence_of_element_located((By.ID, "username")))

        # Fill login fields
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)

        # Submit login
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        # Wait for redirect to feed
        wait.until(EC.url_contains("linkedin.com/feed"))
        print("✅ Login successful!")

    except Exception as e:
        print("❌ Login failed. Check credentials.")
        raise e


def select_resume_based_on_terms(job_title: str) -> str:
    """
    Chooses which CV to use depending on job title.
    """
    if any(term.lower() in job_title.lower() for term in search_terms):
        return "JudeMcCreaCVD.pdf"
    else:
        return "JudeMcCreaCVW.pdf"


# ==============================
# MAIN SCRIPT
# ==============================
if __name__ == "__main__":
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    # Step 1: Login
    login_LN(driver, username, password)

    # Step 2: Go to a job page (replace with real LinkedIn job URL)
    job_url = "https://www.linkedin.com/jobs/view/4285735604"
    driver.get(job_url)

    time.sleep(5)

    # Step 3: Get job title
    # job_title_element = wait.until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "h1.top-card-layout__title"))
    # )
    # job_title = job_title_element.text.strip()
    # print(f"📌 Job title detected: {job_title}")

    # Click the "Easy Apply" button
    easy_apply_button = driver.find_element(
        By.XPATH,
        ".//button[contains(@class,'jobs-apply-button') and "
        "contains(@class,'artdeco-button--3') and "
        "contains(@aria-label,'Easy')]",
    )
    easy_apply_button.click()
    print("✅ Clicked Easy Apply")

    # Step 4: Choose which CV to use
    resume_filename = select_resume_based_on_terms(search_terms)
    print(f"📄 Will select resume: {resume_filename}")

    # Step 5: Find resume cards and select correct one
    resume_cards = driver.find_elements(
        By.CSS_SELECTOR, "div.jobs-document-upload-redesign-card__container"
    )

    for card in resume_cards:
        try:
            file_name = card.find_element(
                By.CSS_SELECTOR, "h3.jobs-document-upload-redesign-card__file-name"
            ).text.strip()

            if file_name == resume_filename:
                radio = card.find_element(By.CSS_SELECTOR, "input[type='radio']")
                driver.execute_script("arguments[0].click();", radio)
                print(f"✅ Selected {file_name}")
                break
        except Exception:
            continue

    # Keep browser open briefly so you can verify
    time.sleep(10)
    driver.quit()
