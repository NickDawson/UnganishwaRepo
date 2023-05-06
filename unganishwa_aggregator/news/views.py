import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
#from news.models import News

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SourceSerializer, HeadlineSerializer

from .models import Source, Headline

# import tweepy

requests.packages.urllib3.disable_warnings()

#Getting news from Millard Ayo

millard_top_stories = requests.get("https://millardayo.com/")
millard_soup = BeautifulSoup(millard_top_stories.content, 'html5lib')

millard_headings = millard_soup.find_all('a')[1]['href']

millard_headings = millard_headings[0:-13] #Removing footers

millard_news = []

#for th in millard_headings:
#    millard_news.append(th.text)


# Getting Issa Michuzi News
issa_blog = requests.get("https://issamichuzi.blogspot.com/")
issa_soup = BeautifulSoup(issa_blog.content, 'html5lib')
issa_headings = issa_soup.find_all("div", {"class": "posttitle"})
issa_news = []

for hth in issa_headings:
    issa_news.append(hth.text)


def index(req):
    return render(req, 'news/index.html', {'millard_news':millard_news, 'issa_news': issa_news})

# Create your views here.
'''
def scrape(request):
    News.objects.all().delete()
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = "https://millardayo.com/category/top-stories/"
    content = session.get(url).content
    soup = BeautifulSoup(content, "html.parser")
    News = soup.find_all('div', {"class":"p-featured ratio-v1"})
    for article in News:
        main = article.find_all('a', href=True)
        linkx = article.find('a', {"class":"p-flink"})
        link=linkx['href']
        imgx=main[0].find('img',src=True)
        image_src=imgx['featured-img wp-post-image'].split(" ")[-4]
        titlex = article.find('h2', {"class":"entry-title"})
        title = titlex.text
        new_headline = News()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = image_src
        new_headline.save()
    return redirect("../")


def news_list(request):
    headlines = News.objects.all()[::-1]
    context = {
        'object_list': headlines,
    }
    return render(request, "news/home.html", context)




class GetDataAPI(APIView):

    def get(self, request, category='latest', *args, **kwargs):
        sources = Source.objects.filter(source_category=category)
        if not sources:
            data = {
                'success':False,
                'msg':'There\'s no sources matching your category',
            }
            return Response(data)
        else:
            serializer = SourceSerializer(sources, many=True)
            return Response(serializer.data)


class SearchAPI(APIView):

    def get(self, request, query, *args, **kwargs):
        headlines = Headline.objects.filter(title__contains=query)
        if not headlines:
            data = {
                'success':False,
                'msg': 'There\'s no headlines matching your keyword',
            }
            return Response(data)
        else:
            serializer = HeadlineSerializer(headlines, many=True)
            return Response(serializer.data)


def get_all(request, category='latest'):
    news_all = []
    for source in Source.objects.filter(source_category=category):
        source_name = source.source_name
        source_link = source.source_link
        update_datetime = source.updated_datetime
        news_list = Headline.objects.filter(source=source)

        news_count = len(news_list)
        if news_count > 5:
            dict = {'source': source_name,
                    'source_url': source_link,
                    'news_count': news_count,
                    'update_datetime': update_datetime,
                    'top_news': news_list[:5],
                    'news_list': news_list[5:]}
            
        else:
            dict = {'source': source_name,
                    'source_url': source_link,
                    'news_count': news_count,
                    'update_datetime': update_datetime,
                    'news_list': news_list}

        news_all.append(dict)
    return render(request, 'news/news.html', {'news_all': news_all})


def sync_now(request):
    Source.objects.all().delete()
    scrap_all_latest()
    return redirect('/')
    


def search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        news_all = []
        for source in Source.objects.all():
            source_name = source.source_name
            source_link = source.source_link
            update_datetime = source.updated_datetime
            news_list = Headline.objects.filter(source=source, title__contains=query)

            news_count = len(news_list)
            if news_count > 5:
                dict = {'source': source_name,
                        'source_url': source_link,
                        'news_count': news_count,
                        'update_datetime': update_datetime,
                        'top_news': news_list[:5],
                        'news_list': news_list[5:]}

            else:
                dict = {'source': source_name,
                        'source_url': source_link,
                        'news_count': news_count,
                        'update_datetime': update_datetime,
                        'news_list': news_list}

            news_all.append(dict)
        return render(request, 'news/news.html', {'news_all': news_all, 'query': query})

    else:
        get_all(request, 'latest')


def scrap_all_latest():
    news_all = [scrap_bbc(), scrap_millard_ayo(), scrap_issa_michuzi()]
    save_all(news_all, 'latest')

'''
'''
def scrap_all_politics():
    news_all = [scrap_bbc_politics(), scrap_millard_ayo_politics(), scrap_issa_michuzi_politics()]
    save_all(news_all, 'politics')


def scrap_all_business():
    news_all = [scrap_bbc_business(), scrap_millard_ayo_business(), scrap_issa_michuzi_business()]
    save_all(news_all, 'business')
'''
#We shall add more categories here
'''
def save_all(news_all, category):
    for source in news_all:
        if source.get('success') and len(source.get('news_list')) > 0:
            print('Successfully Scrapped: ' + source.get('source'))
            source_obj, created = Source.objects.get_or_create(
                source_name=source.get('source'),
                source_link=source.get('source_url'),
                source_category=category
            )
            if created:
                for news in source.get('news_list'):
                    obj, created = Headline.objects.get_or_create(
                        source=source_obj,
                        title=news.title,
                        link=news.link
                    )
        else:
            print('Failed Scrapping: ' + source.get('source'))


def scrap_bbc():
    session = requests.session()
    session.headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    url = 'https://www.bbc.com/swahili'
    content = session.get(url, verify=False).content
    try:
        soup = BeautifulSoup(content, 'lxml', from_encoding="utf8")

        rows = soup.select('.bbc-z3myq8 ea6by782 h3')
        news_list = []
        for i in rows:
            if i.find('span', {'class': 'bbc-1fxtbkn ecljyjm0'}) and i.find('a'):
                title = i.find_all('span', {'class': 'bbc-1fxtbkn ecljyjm0'})[0].text.strip
                link = i.find_all('a')[0]['href']
                if not link.startswith(url):
                    link = url + link
                news_list.append(Headline(title=title, link=link))

        return {'success': True, 'source': 'BBC Swahili', 'source_url': url, 'news_list': news_list}
    except:
        return {'success': False, 'source': 'BBC Swahili', 'source_url': url}


def scrap_millard_ayo():
    session = requests.session()
    session.headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    url = 'https://millardayo.com/'
    content = session.get(url, verify=False).content
    try:
        soup = BeautifulSoup(content, 'lxml', from_encoding="utf-8")

        rows = soup.select('.p-flink')
        news_list = []
        for i in rows:
            if i.find('a'):
                title = i.find_all('a')[1].text.replace('"', '').strip
                link = i.find_all('a')[1]['href']
                if not link.startswith(url):
                    link = url + link
                news_list.append(Headline(title=title, link=link))

        return {'success': True, 'source': 'Millard-Ayo', 'source_url':url, 'news_list': news_list}

    except:
        return {'success': False, 'source': 'Millard-Ayo', 'source_url':url}


def scrap_issa_michuzi():
    session = requests.session()
    session.headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    url = 'https://issamichuzi.blogspot.com'
    content = session.get(url, verify=False).content
    try:
        soup = BeautifulSoup(content, 'lxml', from_encoding="utf-8")

        rows = soup.select('.post-title entry-title')
        news_list = []
        for i in rows:
            if i.find('a'):
                title = i.find_all('a')[1].text.replace('"', '').strip
                link = i.find_all('a')[1]['href']
                if not link.startswith(url):
                    link = url + link
                news_list.append(Headline(title=title, link=link))

        return {'success': True, 'source': 'Issa-Michuzi', 'source_url': url, 'news_list': news_list}

    except:
        return {'success': False, 'source': 'Issa-Michuzi', 'source_url': url}

'''