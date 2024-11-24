import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_job(url):
    try:
        # Fetch the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error for bad status

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract job details (LinkedIn structure)
        job_title = soup.find('h1', {'class': 'topcard__title'}).get_text(strip=True)
        company_name = soup.find('a', {'class': 'topcard__org-name-link'}).get_text(strip=True)
        location = soup.find('span', {'class': 'topcard__flavor topcard__flavor--bullet'}).get_text(strip=True)

        return {
            'Job Title': job_title,
            'Company Name': company_name,
            'Location': location,
            'URL': url
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def save_to_excel(data, filename='job_listings.xlsx'):
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to Excel: {e}")

# Main execution
if __name__ == "__main__":
    job_url = input("Enter LinkedIn job posting URL: ")
    job_data = scrape_job(job_url)
    if job_data:
        save_to_excel([job_data])