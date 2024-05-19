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
scrapy crawl <spider name> -O <filename>
```

This will save the output to a [JSON Lines](http://jsonlines.org/) file.