# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # The url we want to scrape
    url = 'https://redplanetscience.com/'

    # Call visit on our browser and pass the url we want to scrape
    browser.visit(url)

    # Create a Beautiful Soup object
    html = browser.html

    soup_news = soup(html, "html.parser")

    title = soup_news.find_all('div', class_='content_title')[0].text
    paragraph = soup_news.find_all('div', class_='article_teaser_body')[0].text

    # The url we want to scrape
    featured_image_url = 'https://spaceimages-mars.com/'

    # Call visit on our browser and pass the url we want to scrape
    browser.visit(featured_image_url)

    button_element = browser.find_by_tag("button")[1].click()

    # Return all the HTML on our page
    html = browser.html

    # Create Beautiful Soup object, pass in our html and parse with'html.parser'
    image_soup = soup(html, "html.parser")

    image_short = image_soup.find('img', class_= "fancybox-image").get("src")
    image_url = featured_image_url + image_short

    # Scrape the table containing facts about Mars
    url_facts = 'https://galaxyfacts-mars.com/'

    # Use Pandas to convert the data to a HTML table string.
    mars_data = pd.read_html(url_facts)[0]
    mars_data.columns = ["Comparison", "Mars", "Earth"]
    mars_data.set_index("Comparison", inplace = True)

    mars_data.to_html(classes="table table-striped table-bordered table-hover")

    # Obtain high-resolution images for each hemisphere of Mars from 'https://marshemispheres.com/'

    # The url we want to scrape
    url_hemi = 'https://marshemispheres.com/'

    # Call visit on our browser and pass the url we want to scrape
    browser.visit(url_hemi)

    hemi_list = []
    items = browser.find_by_css("a.product-item img")

    for item in range(len(items)):
        hemi_dict = {}
        
        
        browser.find_by_css("a.product-item img")[item].click()
        hemi_dict["title"] = browser.find_by_css("h2.title").text
        sample = browser.links.find_by_text("Sample").first
        hemi_dict["img_url"] = sample["href"]
        hemi_list.append(hemi_dict)
        browser.back()

    browser.quit()      


    scrape_dict = {
        "news_title": title,
        "news_paragraph": paragraph,
        "featured_image": image_url,
        "facts": mars_data,
        "hemispheres": hemi_list

    }

    return scrape_dict

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())