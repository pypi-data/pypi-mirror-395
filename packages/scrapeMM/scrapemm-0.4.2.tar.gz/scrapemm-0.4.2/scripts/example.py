from scrapemm import retrieve
import asyncio

if __name__ == "__main__":
    url = "https://www.awesomescreenshot.com/image/43774028?key=0de2147873b73ed468d07aeb93512c51"
    result = asyncio.run(retrieve(url))
    if result.errors:
        print(result.errors)
    else:
        print(result.content)
