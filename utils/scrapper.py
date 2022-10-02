# IMPORT NECCESSARY LIB
import os
import time
from utils.formatter import format_description_text
from utils.tweet import tweet

path = os.getcwd()
default_media = path + '/blizzard.png'

def blizzard_news_scrapper(driver, WebDriverWait, By, EC):
    driver.get('https://playhearthstone.com/en-gb/news')
    wait = WebDriverWait(driver, 60)

    driver.implicitly_wait(10)

    url = None 

    all_news_links = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a.NewsListItem__ArticleListItem-sc-11gqdi2-0.ArticleListItem")))

    for new_url in all_news_links:
        tweeted = False
        with open(path +"/data/tweeted_news.txt") as f:
            for line in f:
                if line.strip() == new_url.get_attribute('href'):
                    tweeted = True
                    break
        if tweeted:
            continue  
        else: 
            with open(path +"/data/tweeted_news.txt", 'a') as f:
                f.write(new_url.get_attribute('href') + '\n')
                url = new_url.get_attribute('href')
            break

    if url == None:
        print('No new card available at the moment')        
    else:
        scrape_news(driver, wait, By, EC, url)
        driver.quit()
        print('done..............')    
   
  


def scrape_news(driver, wait, By, EC, url_link):
    driver.get(url_link)
    time.sleep(10)
    title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.heading--article span"))).text
    description = driver.find_element(By.CSS_SELECTOR, "div.detail.blog-detail p").text
    img = driver.find_element(By.CSS_SELECTOR, "div.header-image img")
    img_href = img.get_attribute('src')
    intro = '📢 News article spotted 📢'
    url = driver.current_url 
    t = f"{intro}\n\n📜{title}\n\n🌐 {url}"
    desc = format_description_text(description, len(t))

    text = f"{intro}\n\n📜 {title}\n {desc}\n\n🌐 {url}"

    print('Blizzard News...........................#####################################################')
    print(text, img_href)

    # UPLOAD TO TWITTER
    tweet(text, media = img_href)
    
    time.sleep(5)
    driver.quit() 
   

