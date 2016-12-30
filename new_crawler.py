from urllib.request import urlopen
from urllib.parse import urljoin,urlparse
from bs4 import BeautifulSoup


def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    #index = []
    while True:
        if len(tocrawl) == 0:
            break
        page = tocrawl.pop()
        if page not in crawled:
            new_url = gather_links(page)
            content = gather_content(page)
            print("new url is -------->>>>>>>>>>>.", new_url)
            union(tocrawl,new_url)
            crawled.append(page)
            #add_page_to_index(index,page,content)
        print (str(len(tocrawl)) + "  tocrawl list --> " + str(tocrawl))
    return crawled


def gather_links(page_url):
    html_string = ''
    url_list = []
    try:
        response = urlopen(page_url)
        if 'text/html' in response.getheader('Content-Type'):
            print("hello 123")
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8")

    except Exception as e:
        # print("Error: Page cannot be crawled")
        print(str(e))
        return "not available"
    soup = BeautifulSoup(html_string, 'html.parser')
    html_string = soup.prettify()
    a = soup.find_all('a')
    for x in a:
        print(x.get('href'))
        url = x.get('href')
        url = urljoin(HOMEPAGE, url)
        if url.find(HOMEPAGE) != -1:
            url_list.append(url)
        print("absolute url is =======", url)
        if url.find(HOMEPAGE) == -1:
            print("Ignored url is , ", url)
    print(url_list)
    print("code is")
    #print(html_string)
    return url_list

def gather_content(page_url):
    html_string = ''
    try:
        response = urlopen(page_url)
        if 'text/html' in response.getheader('Content-Type'):
            print("hello 123")
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8")

    except Exception as e:
        # print("Error: Page cannot be crawled")
        print(str(e))
        return "not available"
    soup = BeautifulSoup(html_string, 'html.parser')
    html_string = soup.prettify()
    return  html_string



def lookup_index(index,keyword):
    index_len = len(index)
    b = 0
    flag = 0
    while b < index_len:
        if keyword == index[b][0]:
            flag = 1
            break
        b = b + 1
    if flag == 1:
        return index[b][1]
    elif flag == 0:
        return "Item not found on page"

#def add_page_to_index(index,page_url,page_content):
#    page_content_list = page_content.split()
#    page_content_list_len = len(page_content_list)
#    for x in range(page_content_list_len):
#        index.append([page_content_list[x],[page_url]])
#    print("index list is -->  " + str(index))
#    return index


home = input("enter the webpage you want to crawl -- ")
HOMEPAGE = urlparse(home).scheme + "://" +urlparse(home).netloc
print("crawling - " + HOMEPAGE)
crawled = crawl_web(HOMEPAGE)
print ("crawled urls --> ", crawled)

item  = input("enter the item you want a list of - ")
get_item_list(item)
def get_item_list(item):
    url = urljoin(HOMEPAGE,item)
    html_string = ''
    try:
        response = urlopen(url)
        if 'text/html' in response.getheader('Content-Type'):
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8")

    except Exception as e:
        print(str(e))
        return "not available"
    soup = BeautifulSoup(html_string, 'html.parser')
    for i in soup.find_all('li', attrs={"class": "h-product pidloadeddefault"}):
        s = i.find("a")
        print(item + " name - "+ str(s["data-ga-title"]))
        print(item + " url - " + str(urljoin(HOMEPAGE,s["href"])))





