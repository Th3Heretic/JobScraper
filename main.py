from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time


def scrape_job_firefox(url):
    # Set up Firefox options for lightweight operation
    options = Options()
    options.headless = True  # Set to True for headless mode (no browser window)

    # Initialize Firefox WebDriver
    driver = webdriver.Firefox(service=Service(), options=options)
    driver.get(url)
    time.sleep(3)  # Allow page to load

    try:
        # Extract job details
        job_title = driver.find_element(By.CSS_SELECTOR, 'h1.topcard__title').text
        company_name = driver.find_element(By.CSS_SELECTOR, 'a.topcard__org-name-link').text
        location = driver.find_element(By.CSS_SELECTOR, 'span.topcard__flavor--bullet').text

        return {
            'Job Title': job_title,
            'Company Name': company_name,
            'Location': location,
            'URL': url
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
    finally:
        driver.quit()


def save_to_excel(data, filename='job_listings.xlsx'):
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to Excel: {e}")


# Main execution
if __name__ == "__main__":
    job_url = input("Enter the LinkedIn job posting URL: ")
    job_data = scrape_job_firefox(job_url)
    if job_data:
        save_to_excel([job_data])