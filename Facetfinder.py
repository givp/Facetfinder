#!/usr/bin/env python
# 
# Facetfinder
# Giv Parvaneh <giv@givp.org> for VAM 2011
#
# Usage:
# from Facetfinder import Facetfinder
#
# ff = Facetfinder()
# items = ff.get_blogs('textile')
#
#for i in items:
#	print i.url
#	print i.title
#	print i.source
#	print i.keyword
#
#
from bingapi import bingapi
import flickr
import urllib2
import simplejson as json
import feedparser
import gdata.youtube
import gdata.youtube.service

# set BING API key
BING_KEY = ''

# set Flickr API key/secret
flickr.API_KEY = ''
flickr.API_SECRET = ''


########################################################################
# Main
########################################################################
class Item():
    """ Main item model """
    
    title = None
    url = None
    source = None
    keyword = None
    
    def __init__(self, title=None, url=None, source=None, keyword=None):
        self.title = title
        self.url = url
        self.source = source
        self.keyword = keyword
    

class Facetfinder():
    """ Main search class for managing aggregation methods """
    
    all_data = []
    
    def get_flickr(self, keyword):
        """ search Flickr for keyword """
        
        if (flickr.API_KEY == ''):
            raise Exception('Flickr API key not set')
            
        if (flickr.API_SECRET == ''):
            raise Exception('Bing API secret not set')  
        
        photos = flickr.photos_search(text=keyword, per_page=20)
        urls = []

        for photo in photos:
            furl = 'http://farm%s.static.flickr.com/%s/%s_%s_s.jpg' % (photo.farm, photo.server, photo.id, photo.secret)
            url = 'http://www.flickr.com/photos/%s/%s' % (photo.owner.id, photo.id)
            urls.append(url)
            
            i = Item(title=photo.title, url=url, source='flickr', keyword=keyword)
            self.all_data.append(i)
                        
        return self.all_data
        
    def get_twitter(self, keyword):
        """ search Twitter for keyword """
        
        kw1 = urllib2.quote(keyword)
        search_url = "http://search.twitter.com/search.json?q=%s&lang=en" % (keyword)
        twitterResult = urllib2.urlopen(search_url)
        
        twitterData = json.loads(twitterResult.read())
        
        for tweet in twitterData['results']:
            url = 'http://twitter.com/%s/statuses/%s' % (tweet['from_user'], tweet['id'])
            i = Item(title=tweet['text'], url=url, source='twitter', keyword=keyword)
            self.all_data.append(i)
        
        return self.all_data

    def get_youtube(self, keyword):
        """ search Youtube for keyword """
        
        yt_service = gdata.youtube.service.YouTubeService()
        query = gdata.youtube.service.YouTubeVideoQuery()
        
        query.vq = keyword
        query.orderby = 'relevance'
        query.racy = 'exclude'
        feed = yt_service.YouTubeQuery(query)
        self.PrintVideoFeed(feed, keyword) 
        
        return self.all_data   

    def PrintVideoFeed(self, feed, keyword):
        """ Loop through YT videos """
        
        for entry in feed.entry:
            i = self.PrintEntryDetails(entry, keyword)
            self.all_data.append(i)

    def PrintEntryDetails(self, entry, keyword):
        """ Get YT video properties and insert into db """
        
        title = entry.media.title.text
        url = entry.media.player.url
        thumbUrl = entry.media.thumbnail[0].url

        i = Item(title=title, url=url, source='youtube', keyword=keyword)
        
        return i
        
    def get_news(self, keyword):
        """ search Bing News """  
        
        if (BING_KEY == ''):
            raise Exception('Bing API key not set')
        
        bing = bingapi.Bing(BING_KEY)
        newResults = bing.do_news_search(keyword.replace('_', ' ').lower())
        
        newsResultsData = newResults['SearchResponse']['News']['Results']
        
        for news in newsResultsData:
                                                
            i = Item(title=news['Title'], url=news['Url'], source='news', keyword=keyword)
            self.all_data.append(i)
            
        return self.all_data
            
    def get_blogs(self, keyword):
        """ search blogs """
        
        search_url = "http://blogsearch.google.com/blogsearch_feeds?hl=en&q=%s&ie=utf-8&num=10&output=rss" % (keyword.replace('_', ' ').lower())
        blogResult = urllib2.urlopen(search_url)
        
        blogData = feedparser.parse(blogResult.read())
            
        for entry in blogData['entries']:
            i = Item(title=entry['title'], url=entry['link'], source='blogs', keyword=keyword)
            self.all_data.append(i)
        
        return self.all_data
                
    def get_delicious(self, keyword):
        """ delicious links from tag """
        
        search_url = "http://feeds.delicious.com/v2/json/tag/%s" % (keyword.replace('_', ' ').lower())
        
        tagResult = urllib2.urlopen(search_url)
        
        deliciousData = json.loads(tagResult.read())
        
        for link in deliciousData:
            aLink = link['u']
            i = Item(title=link['d'], url=aLink, source='delicious', keyword=keyword)
            self.all_data.append(i)
            
        return self.all_data    

