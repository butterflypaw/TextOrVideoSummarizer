import requests 
from bs4 import BeautifulSoup 


def scrape(url):
    URL = url
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"} 
    # Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link. 

    r = requests.get(url=URL, headers=headers) 
    if r.status_code ==200:
        # print(r.content)

        soup = BeautifulSoup(r.content, 'html.parser') 
        if "404" in soup.title.string:
            print('The page indicates a 404 error')
            return None
    
    possible_selectors = [
        {'tag': 'div', 'class': 'post-content'},
        {'tag': 'div', 'class': 'article-content'},
        {'tag': 'article', 'class': None},
        {'tag': 'div', 'class': 'content'},
        {'tag': 'div', 'id': 'content'},
        {'tag': 'main', 'class': None},
        {'tag': 'div', 'class': 'blog-post'},
        {'tag': 'div', 'class': 'entry-content'},
    ]

    for selector in possible_selectors:
            if selector['class']:
                content_div = soup.find(selector['tag'], class_=selector['class'])
            else:
                content_div = soup.find(selector['tag'])

            if content_div:
                break

    if content_div:
        # Filter out unwanted tags
        for unwanted in content_div(['aside', 'button', 'footer', 'nav', 'form']):
            unwanted.decompose()
        
        # Extract text from the div
        blog_content = content_div.get_text(strip=True,separator="\n")
        return blog_content

    print('Content not found using predefined selectors')
    return None
print()
str = scrape("https://rapidfireart.com/2017/04/06/lesson-1-how-to-sketch/")
print(str)
