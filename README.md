# WebPageStatusCheck Web App
A web app that reads a list of urls and displays their current status.

The app reads a list of urls in JSON format, checks their current status and displays that information in a web page. The list is named checkurls.json bu default (can be changed in settings.py); an example is provided.

The current status of each url is checked every 60 seconds (interval can be changed in settings.py). The app is multithreaded and loads 8 urls concurrently. These are utilised until all updates are complete for that checking cycle.

If one of the urls gives a timeout it may initially take 60 seconds for the web server to load.