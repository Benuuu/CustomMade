import re
import string
import bitly_api

class CustomMadeFilter():    
    def __init__(self,
                dirty_words=["Big Box", "Generic", "Commodity",
                             "Mass Market"],
                brand_correct={"consumer": "Buyer",
                               "maker": "Maker", "subscriber": "Maker",
                               "Custom Made": "CustomMade", "customade": "CustomMade",
                               "admin": "Dashboard", "back end": "Dashboard",
                               "conback": "Buyer Dashboard",
                               "subback": "Maker Dashboard",
                               }
                    ):
                
                self.dirty_words = dirty_words
                self.dirty_word_regexes = self.generate_dirty_regex(dirty_words)
                self.brand_correct = brand_correct
                self.brand_correct_regexes = self.generate_brand_correct_regex(brand_correct)
                self.url_matcher = re.compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^%s\s]|/)))')
                self.bitly_conn = bitly_api.Connection(access_token='213b35f5a8d3ab35958df62d5584aed7829d124f')
                
    """
    Match regardless of case (not just upper vs. lower, but also off cases
    like CamelCase, hyphenated-cased, and underscored_case).
    """    
    def __ignore_case_regexes(self, lst):
        regexes = []
        for s in lst:
            regexes.append(re.compile(string.replace(s, " ", "[ _-]?"), re.IGNORECASE))
        return regexes

    def generate_dirty_regex(self, dirty_words):
        all_caps_pattern = re.compile(r'\b[A-Z]{2,}\b')
        
        regexes = self.__ignore_case_regexes(dirty_words)
        regexes.append(all_caps_pattern)

        return regexes
    
    # Making the assumption that we want to match it similarly to dirty words
    def generate_brand_correct_regex(self, brand_correct):
        bc_keys = brand_correct.keys()
        bc_new_keys = self.__ignore_case_regexes(bc_keys)
        bc_new_dict = {}
        
        for i in xrange(len(bc_keys)):
            bc_new_dict[bc_new_keys[i]] = brand_correct[bc_keys[i]]
        
        return bc_new_dict

    def contains_dirty(self, text):
        for r in self.dirty_word_regexes:
            if re.search(r, text):
                return True
        return False
    
    def brand_correct_text(self, text):
        for k,v in self.brand_correct_regexes.iteritems():
            text = re.sub(k, v, text)
        return text

    def __bitly_url(self, urlmatch):
        url = urlmatch.group(0)
        if not url.startswith('http'):
            url = 'http://%s' % url
        return self.bitly_conn.shorten(url)['url']
    
    def shorten_urls(self, text):
        return re.sub(self.url_matcher, self.__bitly_url, text)
        
