import scrapy
import logging

from collections import defaultdict
from datetime import datetime
from foreign_principals.items import ForeignPrincipal


def strip(str):
    if str:
        return str.replace('\xa0', ' ').strip()
    else:
        return None


class ForeignPrincipalsSpider(scrapy.Spider):

    name = "foreign_principals"
    start_urls = ['https://efile.fara.gov/pls/apex/f?p=171:130:0::NO:RP,130:P130_DATERANGE:N']
    allowed_domains = ["efile.fara.gov"]

    def parse(self, response):

        country = None
        count = 0

        data = defaultdict(list)

        page = response.xpath('//td[@class="pagination"]/span/text()').extract_first()
       
        logging.info("Scrapping rows {}".format(page))

        hasNext = response.xpath('//img[@title="Next"]').extract_first() is not None

        # First, scrap all rows saving them to the following dictionary
        # {
        #   'view_url1' : [ForeignPrincipalItem1, ForeignPrincipalItem2],
        #   'view_url2' : [ForeignPrincipalItem3]
        #    ...
        # }
        # This will save a few requests if the exhibit_url are located in the same URL for more than one principal (in the same page!)
        for tr in response.xpath('//table[@class="apexir_WORKSHEET_DATA"]//tr'):

            
            c = tr.xpath('./th[contains(text(), "Country/Location")]/span/text()').extract_first()           
            if c is not None:  
                country = c

            else:
                
                address     = ", ".join([strip(s) for s in tr.xpath('./td[contains(@headers, "ADDRESS_1")]//text()').extract()])
                
                name        = strip(tr.xpath('./td[contains(@headers, "FP_NAME")]/text()').extract_first())
                state       = strip(tr.xpath('./td[contains(@headers, "STATE")]/text()').extract_first())
                registrant  = strip(tr.xpath('./td[contains(@headers, "REGISTRANT_NAME")]/text()').extract_first())
                reg_num     = strip(tr.xpath('./td[contains(@headers, "REG_NUMBER")]/text()').extract_first())
                reg_date    = strip(tr.xpath('./td[contains(@headers, "REG_DATE")]/text()').extract_first())

                if reg_num is not None:

                    item = ForeignPrincipal (
                        url= response.url,
                        country= country,
                        state= state,
                        reg_num= reg_num,
                        address= address,
                        foreign_principal= name,
                        date= datetime.strptime(reg_date, "%m/%d/%Y"),
                        registrant= registrant
                    )

                    link = tr.xpath('./td[contains(@headers, "LINK")]/a/@href').extract_first()
                    link = response.urljoin(link)

                    data[link].append(item)

                    count += 1

        # Sanity-check if 15 principals were found (except in the last page)
        if hasNext and count < 15:
            logging.warning('Less than 15 items were extracted from the page {}'.format(page))

        # Second, request all view_url that needs to be crawled to scrape the exhibit_url and save the items
        for view_url, items in data.items():

            # dont_filter = True is necessary because the same exhibit_url could be located in different pages
            # in this case, the URL is requested again
            req = scrapy.Request(view_url, callback=self.parse_exhibit_url, dont_filter=True) 
            req.meta['items'] =  items
            yield req 


        # Finally, check if there is another page to crawl       
        if hasNext:

            if 'params' not in response.meta:
                params = {
                    'p_request' : 'APXWGT',
                    'p_instance' : response.xpath('//input[@id="pInstance"]/@value').extract_first(),
                    'p_flow_id' : response.xpath('//input[@id="pFlowId"]/@value').extract_first(),
                    'p_flow_step_id' : response.xpath('//input[@id="pFlowStepId"]/@value').extract_first(),
                    'p_widget_num_return' : '15',
                    'p_widget_name' : 'worksheet',
                    'p_widget_mod' : 'ACTION',
                    'p_widget_action' : 'PAGE',
                    'x01': response.xpath('//input[@id="apexir_WORKSHEET_ID"]/@value').extract_first(),
                    'x02': response.xpath('//input[@id="apexir_REPORT_ID"]/@value').extract_first()
                }
            else:
                params = response.meta['params']
            

            next_page = "https://efile.fara.gov/pls/apex/wwv_flow.show"

            s = response.xpath('(//td[@class="pagination"]/span/a/@href)[last()]').extract_first()
            p_widget_action_mod = s[s.find("('") + 2 : s.find("')")]
            params['p_widget_action_mod'] = p_widget_action_mod

            req = scrapy.FormRequest(next_page, method="POST", formdata=params, callback=self.parse)
            req.meta['params'] = params
        
            yield req
    
    def parse_exhibit_url(self, response):
        items = response.meta['items']
        exhibit_url = response.xpath('(//td[@headers="DOCLINK"])[1]//@href').extract_first()
        for item in items:
            item['exhibit_url'] = exhibit_url
            yield item

            


        