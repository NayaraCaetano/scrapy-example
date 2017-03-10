# Foreign Principals
This is a Scrapy project to scrape foreign principal data from https://www.fara.gov/quick-search.html (“Active Principals” link)

## Extracted data

This project extracts foreign principals data that looks like this sample:
```json
{  
   "url": "https://efile.fara.gov/pls/apex/f?p=171:130:0::NO:RP,130:P130_DATERANGE:N",
   "country": "AFGHANISTAN",
   "state": null,
   "reg_num": "5945",
   "address": "House #3 MRRD Road, Darul Aman, Kabul",
   "foreign_principal": "Transformation and Continuity, Ajmal Ghani",
   "registrant": "Fenton Communications",
   "exhibit_url": "http://www.fara.gov/docs/5945-Exhibit-AB-20140505-10.pdf",
   "$date": "2014-05-05T00:00:00Z"
}
```

## Running the spiders

You can run a spider using the `scrapy crawl` command, such as:

    $ scrapy crawl foreign_principals

The data will be save to a file named output.json

## Running the tests

    $ python -m unittest foreign_principals.tests.tests