from fetchBlotter import fetch
from settings import settings

blotFetcher = fetch()
settings = settings()


dispatchIds = blotFetcher.fetchDispatchIds()

for dispatchId in dispatchIds:
    details = blotFetcher.fetchDispatchDetails(dispatchId)
    outputStr = 'Dispatch ID: %s | Message: %s' % (dispatchId, details)
    print(outputStr)