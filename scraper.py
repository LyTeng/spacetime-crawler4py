import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
track = set()
list = []

def discardFragment(url):
    o = urlparse(url)
    unique_url = o.scheme + '//' + o.hostname #url.scheme will get 'http', url.hostname will get 'ics.uci.edu'
    return unique_url

def scraper(url, resp):
    unique_countIn = 0
    links = extract_next_links(url, resp)
    modified_Url = discardFragment(url) #call function duscardFragment to get unique_url
    if modified_Url not in track:   #If unique_url is not inside the track, we add it in
        track.add(modified_Url)
        unique_countIn += 1
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    if resp.status == 200:
        is_valid(url)
        soup = BeautifulSoup(resp.raw_response.content, "lxml")
        text = soup.get_text()         #-> use text to get tokens and frequencies
        #token = PartA.Tokenizer()
        #token_list = token.tokenize(text)
        #token_frequency = token.computeWordFrequencies(token_list)
        #token_print = token.print_sorted(token_frequency)

        for link in soup.find_all('a'):
            abs_url = urljoin(url, link.get('href')) #get the absolute url like 'http://www.example.com/xyz.html'
            list.append(abs_url)
    #elif resp.status != 200:
    return list

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise



