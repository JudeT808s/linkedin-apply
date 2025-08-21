from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import urllib.parse
import time
from config.secrets import username, password


# ==============================
# CONFIGURATION
# ==============================
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

# Map search term to CV filename
resume_map = {
    "Graduate Data Analyst": "JudeMcCreaCVD.pdf",
    "Graduate Data Scientist": "JudeMcCreaCVD.pdf",
    "Graduate React Developer": "JudeMcCreaCVD.pdf",
    "Graduate Python Developer": "JudeMcCreaCVW.pdf",
    "Graduate Front End Developer": "JudeMcCreaCVW.pdf",
    "Data Analyst": "JudeMcCreaCVD.pdf",
    "React Developer": "JudeMcCreaCVW.pdf",
    "Python Developer": "JudeMcCreaCVW.pdf",
    "Front End Developer": "JudeMcCreaCVW.pdf",
    "Web Developer": "JudeMcCreaCVW.pdf",
    "Nodejs Developer": "JudeMcCreaCVW.pdf",
}


# ==============================
# FUNCTIONS
# ==============================
def login_LN(driver, username: str, password: str):
    """
    Log into LinkedIn.
    """
    driver.get("https://www.linkedin.com/login")
    wait = WebDriverWait(driver, 15)

    try:
        wait.until(EC.presence_of_element_located((By.ID, "username")))
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        wait.until(EC.url_contains("linkedin.com/feed"))
        print("✅ Logged in successfully!")
    except Exception as e:
        print("❌ Login failed!")
        raise e


def search_and_apply(driver, term: str):
    """
    Search for jobs with the given term, open the first result,
    open Easy Apply panel, select the correct CV, click Next buttons,
    and optionally submit.
    """
    wait = WebDriverWait(driver, 15)
    encoded_term = urllib.parse.quote(term)
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_term}"
    driver.get(search_url)
    print(f"🔎 Searching for: {term}")
    time.sleep(3)

    # Step 0: Open first job

    # Step 1: Ensure Easy Apply panel is open
    try:
        panel = driver.find_element(By.CSS_SELECTOR, "div.jobs-easy-apply-modal")
        print("📌 Easy Apply panel is already open")
    except:
        try:
            easy_apply_button = driver.find_element(
                By.XPATH,
                "//button[contains(@class,'jobs-apply-button') and contains(@aria-label,'Easy')]",
            )
            easy_apply_button.click()
            print("✅ Clicked Easy Apply button")
            time.sleep(2)
        except:
            print("⚠️ Easy Apply button not found")
            return

    # Step 1.5 Click Next

    try:
        next_button = driver.find_element(
            By.XPATH, "//button[@aria-label='Continue to next step']"
        )
        driver.execute_script("arguments[0].click();", next_button)
        next_button.click()
        print("✅ Clicked Next button")
        time.sleep(2)
    except:
        print("⚠️ Next button not found")

    # Step 2: Select the correct CV
    resume_filename = resume_map.get(term, "JudeMcCreaCVW.pdf")
    resume_cards = driver.find_elements(
        By.CSS_SELECTOR, "div.jobs-document-upload-redesign-card__container"
    )
    selected = False
    for card in resume_cards:
        try:
            file_name = card.find_element(
                By.CSS_SELECTOR, "h3.jobs-document-upload-redesign-card__file-name"
            ).text.strip()
            if file_name == resume_map.get(term, "JudeMcCreaCVW.pdf"):
                # Click the label to select the radio (inputs are hidden)
                label = card.find_element(
                    By.CSS_SELECTOR,
                    "label.jobs-document-upload-redesign-card__toggle-label",
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView(true);", label
                )  # make sure it's visible
                driver.execute_script("arguments[0].click();", label)
                print(f"✅ Selected CV: '{file_name}' for job search term '{term}'")
                selected = True
                break
        except Exception as e:
            print("⚠️ Error selecting CV:", e)
            continue

    if not selected:
        print(f"⚠️ Could not find CV '{resume_map.get(term)}' for '{term}'")

        return

    # # Step 3: Click Next buttons until we reach Review/Submit
    # try:
    #     while True:
    #         next_button = wait.until(
    #             EC.element_to_be_clickable(
    #                 (By.XPATH, "//button[@aria-label='Continue to next step']")
    #             )
    #         )
    #         driver.execute_script("arguments[0].click();", next_button)
    #         print("➡️ Clicked Next")
    #         time.sleep(1)
    # except TimeoutException:
    #     print("📌 No more Next buttons found, ready to submit or finish Easy Apply")

    # try:
    #     submit_button = driver.find_element(
    #         By.XPATH, "//button[@aria-label='Submit application']"
    #     )
    #     driver.execute_script("arguments[0].click();", submit_button)
    #     print("🎉 Application submitted!")
    # except:
    #     print("⚠️ Submit button not found, manual submission may be required")

    # # Pause briefly to verify before moving to next search term
    # time.sleep(3)


# ==============================
# MAIN SCRIPT
# ==============================
if __name__ == "__main__":
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    login_LN(driver, username, password)

    # Loop through all search terms
    for term in search_terms:
        search_and_apply(driver, term)

    print("🎉 Finished all search terms")
    driver.quit()
