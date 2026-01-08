from ddgs import DDGS

class SearchTools:
    """
    Tools for searching the web.
    """
    
    @staticmethod
    def search(query, max_results=5):
        """
        Searches DuckDuckGo for the given query.
        """
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
            return results
        except Exception as e:
            return str(e)
