from src.tools.tools import web_search, scrape_url

# from regular import declared from src/tools/tools.py
# output = scrape_url("https://www.visitnorway.com/places-to-go/eastern-norway/oslo")
# print(output)

# second method after adding tool operator (@tool) before each tool's function in tools.py
# this method let's us invoke direclty the tool here
result = scrape_url.invoke("https://www.visitnorway.com/places-to-go/eastern-norway/oslo")
print(result)