from engines.googleFactory import GoogleFactory
from query.query_engines import AccessUrls
query = 'apple'
G = GoogleFactory()
urls = G.urlGenerator(query)
a = AccessUrls()
a.gtaskManager(urls,G.extractSearchResults,proxy_flag = 1,ua_flag = 1)
