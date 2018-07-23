# WebPageStatusCheck Web App
A web app that reads a list of urls and displays their current status.

The app reads a list of urls in JSON format, checks their current status and displays that information in a web app. The list must be named checkurls.json; an example is provided.

The current status of each url is checked every 60 seconds. The app is multithreaded and loads 8 urls concurrently. These are utilised until all updates are complete for that checking cycle.

## Donations

BTC: 39ZxvxsssJ86doV4C3iFxRoABENyhh481J
XMR: 46oVELZ92Qr1b9hF92xUp7aJp628sLY66XPTVmhuxEo8SWPWVZJHHWk5ZNDqTEGa18ceoNns2putcVfqzAAH5Qz1RLypdqn