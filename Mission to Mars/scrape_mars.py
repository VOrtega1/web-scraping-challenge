#dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time as tm

def init_browser():
    executable_path = {'executable_path': 'c:\\Program Files\\chromdriver_win32\\chromedriver'}
    browser = Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    mysoup = bs(html, "html.parser")
    tm.sleep(10)
    news_title = mysoup.find("li", class_="slide").find("div", class_="content_title").text
    news_p = mysoup.find("li", class_="slide").find("div", class_="article_teaser_body").text

    #use Pandas to scrape the table 
    table_url = 'https://space-facts.com/mars/'
    space_facts = pd.read_html(table_url)
    space_facts_df = space_facts[0]
    space_facts_df.columns = ["Description", "Mars"]
    space_facts_table = space_facts_df.set_index("Description")
    space_facts_table

    #Use Pandas to convert the data to a HTML table string
    space_facts_table_html = space_facts_table.to_html()
    space_html = space_facts_table_html.replace('\n', ' ')
    space_html 

    #set browser
    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astro_url)
    astro_html = browser.html
    astro_soup = bs(astro_html, "html.parser")
    # Set up bucket
    astro_imgs_url = []

    # Base image url
    base_img_url = "https://astrogeology.usgs.gov/"

    # Set up soup
    astros = astro_soup.find_all('div', class_='item')

# Setting up loop to get title and url
    for astro in astros:
        title = astro.find('h3').text
        
        browser.click_link_by_partial_text("Hemisphere Enhanced")
        jpg_html = browser.html
        jpg_soup = bs(jpg_html, "html.parser")
        jpgs_url = jpg_soup.find('img', class_='wide-image')['src']
        
        images_url = base_img_url+jpgs_url
        astro_imgs_url.append({"title": title, "img_url": images_url})
        astro_imgs_url
        browser.quit()
# Display final dictionary

    mars_dict={
        "Mars_news_headline": news_title,
        "Mars_News_Tease": news_p,
        "Featured_Mars_Image": "N/A",
        "Mars_Facts": space_html,
        "Mars_Hemispheres": astro_imgs_url,
    }
    return mars_dict

if __name__ == "__main__":
    data = scrape()
    print(data)
