import asyncio
from scraper.main import main

if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)