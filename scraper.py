from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# List of domains
domains = [
    "voiceflow.com",
    "saucelabs.com",
    "inflection.io",
    "hypercontext.com",
    "stackmoxie.com",
    "tapcart.co",
    "productboard.com",
    "instapage.com",
    "tenderly.co",
    "teachable.com",
    "elastic.co",
    "astronomer.io",
    "hello.formstack.com",
    "email.nylas.com",
]

# Define the URLs of the websites
url1 = "https://dmarcly.com/tools/dmarc-checker"
url2 = "https://dmarcly.com/tools/dkim-record-checker"
url3 = "https://dmarcly.com/tools/spf-record-checker"

# Initialize the results dictionary
results = {}

# Function to perform scraping for a given domain and URL using Selenium


def scrape_domain_with_selenium(domain, url, input_id, input_placeholder, selector_id, selector_value, button_class):

    # Set up the Selenium WebDriver (you may need to adjust the path to the driver)
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Firefox()
    try:

        # Navigate to the website
        driver.get(url)

        # Find the first input box, clear it, and send the domain
        input_box1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, input_id))
        )
        input_box1.clear()
        input_box1.send_keys(domain)

        # If there is a second input box, fill it with the specified selector_value
        if selector_id:
            input_box2 = driver.find_element_by_id(selector_id)
            input_box2.clear()
            input_box2.send_keys(selector_value)

        # Click the button
        button = driver.find_element_by_class_name(button_class)
        button.click()

        # Wait for the result (you may need to adjust the waiting conditions)
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'result'))
        ).text

        # Update the results dictionary
        results[domain] = {"status": "success", "result": result}
    except Exception as e:
        results[domain] = {"status": "failure",
                           "result": f"An error occurred: {str(e)}"}
    finally:
        driver.quit()


# Loop through each domain and perform scraping
for domain in domains:
    # For the second website, use "s1" as the selector_value
    scrape_domain_with_selenium(
        domain, url1, "domain", "Domain, e.g., dmarcly.com", None, None, "check")
    scrape_domain_with_selenium(
        domain, url2, "domain", "Enter domain", "selector", "s1", "check")
    scrape_domain_with_selenium(
        domain, url3, "domain", "Domain, e.g., dmarcly.com", None, None, "check")

# Print the results
print(json.dumps(results, indent=2))

# Save the results to a JSON file
with open("scraped_results.json", "w") as file:
    json.dump(results, file, indent=2)
