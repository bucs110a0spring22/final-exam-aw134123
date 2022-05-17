import pprint
from masterscraper import Googlescraper, Bingscraper


def api_main():
    '''driver code for running masterscraper and saving top 10 search results from the different search engines to a file. Also combines the results by ranking and checks if there are any common URLs and if so, how they are ranked differently by each search engine.'''
    for search_term in ["dog", "cat"]:
        results_by_rank = {}
        results_by_url = {}
        results_by_search_engine = {}
        search_engines = [Googlescraper(), Bingscraper()]
        for scrape in search_engines:

            result_filename = search_term + scrape.search_engine(
            ) + "results" + ".txt"
            search_results = scrape.search(search_term)
            results = scrape.save_results(search_results, result_filename)
            results_by_search_engine[scrape.search_engine()] = results
        # populate search results by rank (results returned by search engine are ordered by rank already
        # populate search results by url
        for search_engine, results in results_by_search_engine.items():
            
            for rank, result_entry in enumerate(results):
                if rank in results_by_rank:
                    entry = results_by_rank[rank]
                else:
                    entry = {}  # stores url by search engine
                    results_by_rank[rank] = entry
                url = result_entry['URL']
                entry[search_engine] = url

                if url in results_by_url:
                    by_url_entry = results_by_url[url]
                else:
                    by_url_entry = {}  # stores ranking by search engine
                    results_by_url[url] = by_url_entry
                by_url_entry[search_engine] = rank

        # process results_by_url and filter out urls appears in all search engines
        num_of_search_engine = len(search_engines)
        results_common_url = {}
        for url, rankings_by_search_engine in results_by_url.items():
            if len(rankings_by_search_engine) == num_of_search_engine:
                results_common_url[
                    url] = rankings_by_search_engine
        #print out search result ranking, URL with ranking, and common URL for both browsers
        print(
            f'Search Results for {search_term} by Rank: \n {pprint.pformat(results_by_rank)}'
        )
        print(
            f'Search Results for {search_term} by URL: \n {pprint.pformat(results_by_url)}'
        )
        print(
            f'Search Results for {search_term} by URL that appears in both search engines: \n {pprint.pformat(results_common_url)}'
        )
        # create new files with search result ranking and common URL for both browsers "
        result_by_rank_file_handle = open(search_term + search_engine + "ranking" + ".txt", "w")
        result_by_rank_file_handle.write(pprint.pformat(results_by_rank))
        result_common_url_file_handle = open(search_term + search_engine + "commonurl" + ".txt", "w")
        result_common_url_file_handle.write(pprint.pformat(results_common_url))
        

api_main()
