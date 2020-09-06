#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape():
    #open browser
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)



    #Getting Title and Paragraph
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')


    content_titles = soup.find_all("li", class_="slide")
    first_slide = content_titles[0]
    title = first_slide.find('div', class_ = 'content_title')
    teaser = first_slide.find('div', class_ = 'article_teaser_body')
    news_title = title.text
    news_p = teaser.text




    #Getting Featured Picture
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    time.sleep(1)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    full_button = soup.find('a', class_ = "button fancybox")
    jpgLink = full_button["data-fancybox-href"]
    LatestMarsImage = 'https://www.jpl.nasa.gov' + jpgLink



    #Create Table and convert to html
    url = 'https://space-facts.com/mars/'
    df_list = pd.read_html(url)
    list_needed = df_list[2]
    list_needed.columns = ['Fact', 'Mars']
    html_table = list_needed.to_html(index = False)



    #Getting hi res hemisphere images
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    time.sleep(1)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    hemispheres = {}
    content_titles = soup.find_all("div", class_="item")
    original_site = 'https://astrogeology.usgs.gov/'
    for content in content_titles:
        try:
            a_tag = content.find('a')
            link = a_tag['href']
            enhanced_image = original_site + link
            description_class = content.find('div', class_ = 'description')
            description_a = description_class.find('a')
            title = description_a.find('h3').text
            hemispheres[title] = enhanced_image
        except:
            continue
    hemisphere_image_urls = []
    for title, link in hemispheres.items():
        browser.visit(link)
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        content_lists = soup.find_all("li")
        enhanced_image = content_lists[0]
        a_tag_enhanced = enhanced_image.find('a')
        enhanced_image = a_tag_enhanced['href']
        hemisphere_image = {}
        hemisphere_image["title"] = title
        hemisphere_image["image"] = enhanced_image
        hemisphere_image_urls.append(hemisphere_image)


    #Close Browser
    browser.quit()


    return_dictionary = {"articletitle": news_title,
                         "articleparagraph": news_p,
                         "featuredimage": LatestMarsImage,
                         "marstable": html_table,
                         "hemispheres": hemisphere_image_urls}
    return return_dictionary


if __name__ == '__main__':
    scraped_info = scrape()
    print(scraped_info)
