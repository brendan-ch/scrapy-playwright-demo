# scrapy-playwright-demo

A sample [Scrapy](https://scrapy.org)-based project containing several web crawlers. This project uses
[scrapy-playwright](https://github.com/scrapy-plugins/scrapy-playwright), a plugin integrating headless browser support
using [Playwright](http://playwright.dev) with Scrapy's web crawling capabilities.

## Getting Started

Set up Scrapy by creating a [Python virtual environment](https://docs.python.org/3/library/venv.html) and installing dependencies.

```plaintext
python -m venv <location> && source <location>/bin/activate
pip install -r requirements.txt
```

Change the working directory to the Scrapy project `playwright_test`:

```plaintext
cd playwright_test
```

Spiders (which contain web crawling logic) are located under the
`playwright_test/playwright_test/spiders` module. To run a spider by name:

```plaintext
scrapy crawl <spider name>
```

The spider name should match the `name` member variable of one of
the `scrapy.Spider` subclasses.

To run the spider and save the output to a file:

```
scrapy crawl <spider name> -O <filename>
```

This will save the output to a [JSON Lines](http://jsonlines.org/) file.