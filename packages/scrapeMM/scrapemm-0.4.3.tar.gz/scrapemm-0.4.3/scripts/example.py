from scrapemm import retrieve
import asyncio

if __name__ == "__main__":
    url = "https://x.com/Shayan86/status/1891673533601780022"
    result = asyncio.run(retrieve(url))
    if result.errors:
        print(result.errors)
    else:
        print(result.content)
