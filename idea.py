from playwright.sync_api import sync_playwright
import csv
import re

def get_employee_count(linkedin_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(linkedin_url)
        page.wait_for_load_state()
        try:
            employee_count_element = page.query_selector('.face-pile__cta')
            employee_count_text = employee_count_element.inner_text()
            # Regular expression pattern explanation:
            # \d{1,3}       Matches one to three digits (e.g., 5, 123, 987)
            # (?:,\d{3})*   Matches zero or more occurrences of a comma followed by
            #               three digits (e.g., ,000, ,456, ,789)
            # (?=\s*employee)   Positive lookahead to ensure that "employee" is present after the digits
            employee_count_match = re.search(r'(\d{1,3}(?:,\d{3})*)(?=\s*employee)', employee_count_text)
            employee_count = employee_count_match.group(1).replace(',', '') if employee_count_match else None
        except:
            employee_count = None

        context.close()
        browser.close()

    return employee_count


def retrieve_employee_counts(csv_file):
    employee_counts = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            company_name, linkedin_url = row
            print(f"Extracting Employee Count for {company_name}")
            employee_count = get_employee_count(linkedin_url)
            employee_counts.append([company_name, employee_count])

    return employee_counts


def write_employee_counts(csv_file, employee_counts):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "Employee Count"])
        writer.writerows(employee_counts)


def generate_linkedin_url(company_name):
    return f"https://www.linkedin.com/company/{company_name.lower().replace(' ', '-')}/"


def generate_linkedin_urls(csv_file):
    linkedin_urls = []

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            company_name = row[0]
            linkedin_url = generate_linkedin_url(company_name)
            linkedin_urls.append([company_name, linkedin_url])

    return linkedin_urls


def write_linkedin_urls(csv_file, linkedin_urls):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "LinkedIn URL"])
        writer.writerows(linkedin_urls)


input_csv = "company_data.csv"
urls_csv = "company_links.csv"

linkedin_urls = generate_linkedin_urls(input_csv)
write_linkedin_urls(urls_csv, linkedin_urls)

employee_counts = retrieve_employee_counts(urls_csv)
write_employee_counts(input_csv, employee_counts)

print("Data Scraped and added to company_data.csv.")