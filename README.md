# scrapy-playwright-demo

A sample [Scrapy](https://scrapy.org)-based project containing several web crawlers. This project uses
[scrapy-playwright](https://github.com/scrapy-plugins/scrapy-playwright), a plugin integrating headless browser support
using [Playwright](http://playwright.dev) with Scrapy's web crawling capabilities.

See [Web Scraping Notes](https://brendanchen.craft.me/n42/039/web-scraping) for background regarding this repository.
To set up the project, continue reading this README.

## Getting Started

This project uses a `conda` environment for package installation. [Start by installing `conda` through Miniconda](https://docs.anaconda.com/free/miniconda/) or another method.

Verify `conda` is installed:

```plaintext
conda info
```

Then, activate the Conda environment:

```plaintext
conda env create -f env.yml
```

This will create a new environment named `scrapy-demo`, installing necessary dependencies.

Finally, activate the environment:
```plaintext
conda activate scrapy-demo
```

You'll now be able to run Scrapy. Spiders (which contain web crawling logic) are located under the `playwright_test/spiders` module. To run a spider by name:

```plaintext
scrapy crawl <spider name>
```

The spider name should match the `name` member variable of one of
the `scrapy.Spider` subclasses.

To run the spider and save the output to a file:

```
scrapy crawl <spider name> -O "[filename].jsonl"
```

This will save the output to a [JSON Lines](http://jsonlines.org/) file.

See the next section for the currently available Spiders and their arguments.

## Available Spiders

### `google_scholar_arxiv`

This spider crawls Arxiv results on Google Scholar, following links to Arxiv pages to gather more information. It returns a variety of different object types.

To run the spider with file output, use the following:
```
scrapy crawl google_scholar_arxiv -O "[filename].jsonl" -a query="[Google Scholar search query]" [-a download="1"]
```

The `download` argument is optional and solely exists if you want to download associated PDFs with papers.

### `google_scholar`

This spider crawls Google Scholar results, returning the title and link of each result.

To run the spider with file output, use the following:
```
scrapy crawl google_scholar_arxiv -O "[filename].jsonl" -a query="[Google Scholar search query]"
```

### `httpbin`

This sample code was taken from the [Scrapy Playwright repository](https://github.com/scrapy-plugins/scrapy-playwright?tab=readme-ov-file#basic-usage).

### `google`

This spider crawls Google results, returning the title of each result.

To run the spider with file output, use the following:
```
scrapy crawl google -O "[filename].jsonl" [-a query="[Google search query]"]
```

Without the -a flag, the spider searches results for "scrapy".