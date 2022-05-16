import requests
import pprint


class Basescraper(object):
    def __init__(self):
        '''for putting setting up interaction with the API'''
        pass

    def search(self, query):
        '''for interacting with the API and getting the data in JSON format'''
        pass

    def save_results(self, results, filename):
        '''for parsing the data in a specific format'''
        pass

    def search_engine(self):
        '''identifying which search engine corresponds with which class'''
        pass

    # def process_results(self, results):
    #   pass


class Googlescraper(Basescraper):
    def __init__(self,
                 api_key="AIzaSyAS9eKgOiroK3C1W75EUD2i0Q452NFs35k",
                 cse_engine_id="dfa6a9cd2b3cc6812"):
        '''sets up keys to use Google API
        second set of API keys we are on because I ran out of request for the first set '''
        super().__init__()
        self.API_KEY = api_key
        self.SEARCH_ENGINE_ID = cse_engine_id

    def search(self, query):
        '''asks Google API for the JSON data of the first page of search results in the specific format that google wants'''
        page = 1
        start = (page - 1) * 10 + 1
        url = f"https://www.googleapis.com/customsearch/v1?key={self.API_KEY}&cx={self.SEARCH_ENGINE_ID}&q={query}&start={start}"
        data = requests.get(url).json()
        return data

    def save_results(self, results, filename):
        '''saves data of results into a file with the name filename'''
        results_file_handle = open(filename, "w", encoding='utf-8')
        ranked_results = []
        for i, search_item in enumerate(results['items'], start=1):
            title = search_item.get("title")
            snippet = search_item.get("snippet")
            link = search_item.get("link")
            results_file_handle.write("=" * 10 + f"Result #{i}" + "=" * 10 +
                                      "\n")
            results_file_handle.write("Title:" + title + "\n")
            results_file_handle.write("Description:" + snippet + "\n")
            results_file_handle.write("URL:" + link + "\n")
            ranked_results.append({
                "Title": title,
                "Description": snippet,
                "URL": link
            })
        results_file_handle.close()
        return ranked_results

    def search_engine(self):
        '''says that the subclass being used is google'''
        return 'google'


class Bingscraper(Basescraper):
    def __init__(self, api_key='80ed6b5369ca47f8b88508924f36cd72'):
        '''sets up keys to use Bing API
        '''
        super().__init__()
        self.API_KEY = api_key

    def search(self, query):
        '''asks Bing API for the JSON data of the first page of search results in the specific format that Bing wants'''
        search_url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key": self.API_KEY}
        params = {
            "q": query,
            "textDecorations": True,
            "textFormat": "HTML",
            "answerCount": 10
        }
        # get response
        data = requests.get(search_url, headers=headers, params=params).json()
        # pprint.pprint(data)
        # print(len(data))
        return data

    def save_results(self, results, filename):
        '''saves data of results into a file with the name filename. small difference with google is that the snippet is in HTML format whereas Google's is further processed'''
        results_file_handle = open(filename, "w", encoding='utf-8')
        ranked_results = []
        for i, search_item in enumerate(results['webPages']['value'], start=1):
            title = search_item.get("name")
            snippet = search_item.get("snippet")
            link = search_item.get("url")
            results_file_handle.write("=" * 10 + f"Result #{i}" + "=" * 10 +
                                      "\n")
            results_file_handle.write("Title:" + title + "\n")
            results_file_handle.write("Description:" + snippet + "\n")
            results_file_handle.write("URL:" + link + "\n")
            ranked_results.append({
                "Title": title,
                "Description": snippet,
                "URL": link
            })
        results_file_handle.close()
        return ranked_results

    def search_engine(self):
        '''says that the subclass being used is google'''
        return 'bing'
