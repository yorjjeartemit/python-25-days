import requests
from bs4 import BeautifulSoup
import datetime
def get_weather(city_name):
    q=f"weather+{city_name}"
    url=f"https://api.duckduckgo.com/?q={q}&format=json"
    r=requests.get(url).json()
    try:
        w_text=r['relatedtopics'][0]['text']
        return w_text
    except (IndexError,KeyError):
        return "no weather found"
def get_sunset(city):
    c=city.lower().replace(" ","-")
    url=f"https://www.timeanddate.com/sun/ukraine/{c}"
    r=requests.get(url)
    s=BeautifulSoup(r.text,"html.parser")
    try:
        tab=s.find("table",{"class":"tb-wt"})
        row=tab.find_all("tr")[1]
        cell=row.find_all("td")[1].text
        return cell
    except Exception:
        return "no sunset time"
def get_imdb(movie):
    q=f"{movie} imdb"
    url=f"https://duckduckgo.com/html/?q={q.replace(' ','+')}"
    r=requests.get(url).text
    s=BeautifulSoup(r,"html.parser")
    imdb_link=None
    for a in s.select("a.result__a"):
        href=a.get("href")
        if "imdb.com/title" in href:
            imdb_link=href
            break
    if not imdb_link:
        return "imdb not found"
    rr=requests.get(imdb_link).text
    ss=BeautifulSoup(rr,"html.parser")
    rate=ss.find("span",{"class":"sc-7ab21ed2-1 jGRxWM"})
    if rate:
        return f"{movie} imdb rate: {rate.text}"
    return "rate not found"
def get_news():
    url="https://duckduckgo.com/html/?q=news"
    r=requests.get(url).text
    s=BeautifulSoup(r,"html.parser")
    news_list=[]
    for a in s.select(".result__a")[:5]:
        tit=a.text
        link=a['href']
        news_list.append((tit,link))
    return news_list
def get_usd_uah():
    url="https://api.duckduckgo.com/?q=usd+to+uah&format=json"
    r=requests.get(url).json()
    try:
        info=r['relatedtopics'][0]['text']
        return info
    except (IndexError,KeyError):
        return "rate not found"
def get_quote():
    url="https://duckduckgo.com/html/?q=random+quote+goodreads"
    r=requests.get(url).text
    s=BeautifulSoup(r,"html.parser")
    quote_url=None
    for a in s.select("a.result__a"):
        if "goodreads.com/quotes" in a['href']:
            quote_url=a['href']
            break
    if not quote_url:
        return "quote not found"
    rq=requests.get(quote_url).text
    sq=BeautifulSoup(rq,"html.parser")
    quote=sq.find("div",{"class":"quoteText"})
    if quote:
        return quote.text.strip().split("\n")[0].strip()
    return "quote not found"
def get_btc():
    url="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    r=requests.get(url).json()
    return f"bitcoin price: ${r['bitcoin']['usd']}"
def get_meteo(lat,lon):
    url=f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    r=requests.get(url).json()
    try:
        t=r['current_weather']['temperature']
        return f"temp now: {t}°c"
    except KeyError:
        return "no weather"
def get_day(date_str):
    d=datetime.datetime.strptime(date_str,"%Y-%m-%d")
    return d.strftime("%A")
def get_suggs(q):
    url=f"https://duckduckgo.com/ac/?q={q}"
    r=requests.get(url).json()
    return [i['phrase'] for i in r]
if __name__=="__main__":
    print("1 погода kyiv:",get_weather("kyiv"))
    print("2 захід сонця kyiv:",get_sunset("kyiv"))
    print("3 imdb inception:",get_imdb("inception"))
    print("4 новини:")
    for t,l in get_news():
        print("-",t,l)
    print("5 usd to uah:",get_usd_uah())
    print("6 цитата:",get_quote())
    print("7 btc price:",get_btc())
    print("8 meteo kyiv:",get_meteo(50.45,30.52))
    print("9 день тижня 2025-08-09:",get_day("2025-08-09"))
    print("10 подсказки python:",get_suggs("python"))