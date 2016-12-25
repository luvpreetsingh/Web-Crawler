from urllib.request import urlopen

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    while True:
        if len(tocrawl) == 0:
            break
        page = tocrawl.pop()
        if page not in crawled:	
            union(tocrawl,get_all_links(gather_links(page)))
            crawled.append(page)
        print ("tocrawl list --> " + str(tocrawl))
    return "crawled list " + str(crawled)


def gather_links(page_url):
    html_string = ''
    try:
        response = urlopen(page_url)
        if 'text/html' in response.getheader('Content-Type'):
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8")

    except Exception as e:
        # print("Error: Page cannot be crawled")
        print(str(e))
        return "not available"
    return html_string


x = input("Enter the website you want to crawl - ")
print("crawling --> " + x)
print crawl_web(x)
