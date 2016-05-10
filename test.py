from engines.sogouFactory import SogouFactory
from query.query_engines import AccessUrls
import sys
query = sys.argv[1]
G = SogouFactory()
urls = G.urlGenerator(query)
a = AccessUrls()
a.gtaskManager(urls,G.extractSearchResults,proxy_flag = 0,ua_flag = 1)
