# dependencies
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import requests
from pprint import pprint



def scrape():

    # NASA MARS NEWS
    URL1 = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    URL2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    driver = webdriver.Firefox()

    driver.get(URL1)
    html_text = driver.page_source

    soup = BeautifulSoup(html_text, "html.parser")

    latest_news_title = soup.find("div", class_="content_title").text
    latest_news_title

    latest_news_p = soup.find("div", class_="article_teaser_body").text
    latest_news_p

    # JPL Mars Space Images - Featured Image

    driver.get(URL2)
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, "html.parser")

    mars_img_ref_path = soup.find("footer").a.attrs
    mars_img_ref_path

    feat_mars_img_url = "https://www.jpl.nasa.gov" + mars_img_ref_path["data-fancybox-href"]
    feat_mars_img_url

    # MARS WEATHER
    MARS_WEATHER_URL = "https://twitter.com/marswxreport?lang=en"

    html_text = requests.get(MARS_WEATHER_URL).text
    soup = BeautifulSoup(html_text, "html.parser")

    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather

    # MARS FACTS
    MARS_FACTS_URL = "https://space-facts.com/mars/"

    mars_facts_df = pd.read_html(MARS_FACTS_URL)[0]

    mars_facts_df.columns = ["Description", "Values"]
    mars_facts_df.set_index("Description").to_dict(orient = "records")
    mars_facts = mars_facts_df.to_html()
    mars_facts

    # Mars Hemispheres
    MARS_HEMI_URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    driver.get(MARS_HEMI_URL)
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, "html.parser")

    hemisphere_name = [e.text.strip("Enhanced") for e in soup.find_all("h3")]
    hemisphere_name

    path_to_full_img = [e.a["href"] for e in soup.find_all("div", class_="description")]
    path_to_full_img

    FULL_IMG_LINK = []
    for e in range(len(path_to_full_img)):
        FULL_IMG_LINK.append("https://astrogeology.usgs.gov" + path_to_full_img[e])

    FULL_IMG_LINK

    image_url = []
    for e in range(len(FULL_IMG_LINK)):
        driver.get(FULL_IMG_LINK[e])
        html_text = driver.page_source
        soup = BeautifulSoup(html_text, "html.parser")
        
        
        image_url.append("https://astrogeology.usgs.gov" + soup.find_all("img", class_="wide-image")[0]["src"])
        
    image_url

    hemisphere_image = []
    for e in range(len(hemisphere_name)):
        hemisphere_dict = {}
        hemisphere_dict["title"] = hemisphere_name[e]
        hemisphere_dict["url"] = image_url[e]
        
        hemisphere_image.append(hemisphere_dict)
        
    hemisphere_image

    mars_data = {
        "news_title": latest_news_title,
        "news_snippet": latest_news_p,
        "featured_img_url": feat_mars_img_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemispheres": hemisphere_image
    }


    return mars_data