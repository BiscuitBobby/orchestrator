import pickle
import threading
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from langchain.document_loaders import AsyncChromiumLoader, AsyncHtmlLoader
from langchain.document_transformers import BeautifulSoupTransformer, Html2TextTransformer

references = []
text = ''

def scrape_dynamic(url = "https://www.google.com/"):
    global text
    driver = webdriver.Firefox()
    driver.get(url)

    # this is just to ensure that the page is loaded
    time.sleep(5)

    html = driver.page_source

    # this renders the JS code and stores all the information in static HTML code.

    # Now, we could simply apply bs4 to html variable
    soup = BeautifulSoup(html, "html.parser")

    #print(soup)
    text += str(soup)

    driver.close()
    return soup
def scrape_html(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            # Get the HTML content
            html_content = response.text
            return html_content
        else:
            print(f"Error: Unable to fetch data from {url}. Status code: {response.status_code}")
            return None

    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


def soap_scrape(url):
    loader = AsyncChromiumLoader([url])
    html = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        html, tags_to_extract=["p", "li", "div", "a", "div", "ul", "script"]
    )
    print(docs_transformed)
    with open('pickle', 'wb') as file:
        pickle.dump(docs_transformed, file)


def data_extraction(url):
    global references
    data = scrape_html(url)
    thread = threading.Thread(target=scrape_dynamic, args=(url,))
    references.append(data)
    thread.start()
    return thread


def scrape_google_search(query, num_pages=5):
    print('initializing...')
    info = []
    # Use Firefox as the webdriver
    driver = webdriver.Firefox()
    print('searching')
    try:
        for page_num in range(num_pages):
            url = f"https://www.google.com/search?q={query}&start={page_num * 10}"
            driver.get(url)

            # Extract search results from the current page
            search_results = driver.find_elements("css selector", 'div.tF2Cxc')

            # Extract data from each search result
            for result in search_results:
                description = ''
                title_element = result.find_element("css selector", 'h3')
                title = title_element.text

                url_element = result.find_element("css selector", 'a')
                url = url_element.get_attribute('href')

                description_element = result.find_element("css selector", 'div')
                description = f"{description}\n{description_element.text}"

                print(f"Title: {title}")
                print(f"URL: {url}")
                print(f"DESCRIPTION: {description}")
                references.append(f"Title: {title}, URL: {url}, DESCRIPTION: {description}")

                # Extract additional data if needed
            info.append(references)

            # Scrape the next page if there are more results
            if page_num < num_pages:
                # Wait for the "Next" button to be clickable
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'pnnext'))
                )
                next_button.click()

    except Exception as e:
        print(f"error: {e}")

    finally:
        print(info)
        # Close the driver after all the pages have been processed
        driver.quit()

        with open('data.txt', 'w') as x:
            with open('data.txt', 'a') as y:
                for i in info:
                    for j in i:
                        y.write(str(j))

# Example usage
#query = "What is a nebula"
#scrape_google_search(query)
scrape_google_search("what is a nebula")