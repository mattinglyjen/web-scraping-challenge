from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

def scrape():
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    #NASA Mars News
    titles = soup.find('div', class_="content_title")
    paragraphs = soup.find('div', class_="article_teaser_body")
    news_title = titles.text.strip()
    news_p = paragraphs.text.strip()

    #JPL Mars Space Image
    browser = Browser('chrome', **executable_path, headless=False)
    url2 = "https://spaceimages-mars.com/"
    browser.visit(url2)
    html = browser.html
    soup2 = bs(html,"html.parser")

    # print(soup.prettify())
    image=soup2.find('img',class_="headerimage fade-in").get('src')
    featured_image_url = url2+image

    #Mars Facts
    url3 = "https://galaxyfacts-mars.com/"
    mars_df = pd.read_html(url3)
    info = mars_df[0]
    info = info.append(mars_df[1])
    info.columns= info.iloc[0]
    info = info.drop(0)
    info.set_index("Mars - Earth Comparison", inplace=True)
    info_html= info.to_html()
    
    #Mars Hempisphere
    url4 = "https://marshemispheres.com/"
    html = requests.get(url4)
    soup4 = bs(html.text,"html.parser")

    hemi_img = soup4.find_all('div', {"class":["description",'itemLink product-item']})

    hemisphere_image_urls = []
    img_hold = []
    hemi_img = soup4.find_all('div', {"class":["description",'itemLink product-item']})
    for j in hemi_img:
        k = j.find('a',href=True)
        img_hold.append(k['href'])
    hemi_title = soup4.find_all('h3')
    for i in range(len(hemi_img)):
        hold = {}
        hold['title'] = hemi_title[i].text.strip()
        urlh = url4+img_hold[i]
        html = requests.get(urlh)
        souph = bs(html.text,"html.parser")
        img_dl= (souph.find('img', class_='wide-image')).get('src')
        hold['img_url']= url4+img_dl
        hemisphere_image_urls.append(hold)

    
    mars = {'news_title':news_title,
            'news_p':news_p,
            'featured_image_url':featured_image_url,
            'facts': info_html,
            'hemispheres': hemisphere_image_urls,
            
           }
    
    return mars

