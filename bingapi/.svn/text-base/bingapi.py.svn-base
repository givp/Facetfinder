import urllib2
import urllib
import simplejson
import logging

class BingException(Exception):
    pass

class Bing(object):
    def __init__(self, app_id, loglevel=logging.INFO):
        self.app_id = app_id
        self.log_filename = 'log.log'
        self.end_point = 'http://api.search.live.net/json.aspx?Appid=%s&'%app_id
        logging.basicConfig(level=loglevel,
                          format='%(asctime)s %(name)-6s %(levelname)-8s %(message)s',
                          filename=self.log_filename) 
        
        
    def talk_to_bing(self, query, sources, extra_args={}):
        logging.info('Query:%s'%query)
        logging.info('Sources:%s'%sources)
        logging.info('Other Args:%s'%extra_args)
        
        payload={}
        #payload['Appid'] = self.app_id
        payload['query'] = query
        payload['sources'] = sources
        payload.update(extra_args)
        query_string = urllib.urlencode(payload)
        final_url = self.end_point + query_string
        logging.info('final_url:%s'%final_url)
        response = urllib.urlopen(final_url)
        data = simplejson.load(response)
        if 'Errors' in data['SearchResponse']:
            logging.info('Error')
            logging.info('data:%s'%data)
            data = data['SearchResponse']
            errors_list = [el['Message'] for el in data['Errors']]
            error_text = ','.join(errors_list)
            raise BingException(error_text)
        #logging.info('data:%s'%data)
        return data
    
    def do_web_search(self, query, extra_args={}):
        return self.talk_to_bing(query, sources='web', extra_args=extra_args)
    
    def do_image_search(self, query, extra_args={}):
        return self.talk_to_bing(query, sources='image', extra_args=extra_args)
    
    def do_news_search(self, query, extra_args={}):
        return self.talk_to_bing(query, sources='news', extra_args=extra_args)
    
    def do_spell_search(self, query, extra_args={}):
        return self.talk_to_bing(query, sources='spell', extra_args=extra_args)
    
    def do_related_search(self, query, extra_args={}):
        return self.talk_to_bing(query, sources='relatedsearch', extra_args=extra_args)
    
    def do_phonebook_search(self, query, extra_args={}):
        return self.talk_to_bing(query, sources='Phonebook', extra_args=extra_args)
    
    def do_answers_search(self, query, extra_args={}):
        return self.talk_to_bing(query, sources='InstantAnswer', extra_args=extra_args)
    
    
    
        
        
        
        