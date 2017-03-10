import unittest
from copy import deepcopy
from scrapy.http import HtmlResponse, Request, FormRequest
from datetime import datetime

from foreign_principals.spiders.foreign_principals import ForeignPrincipalsSpider
from foreign_principals.items import ForeignPrincipal

class TestSpider(unittest.TestCase):

    url = 'https://efile.fara.gov/pls/apex/f?p=171:130:0::NO:RP,130:P130_DATERANGE:N'
    links = None
    expected_items = None

    @classmethod
    def setUpClass(cls):

        cls.links = [
            'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:5945,Exhibit%20AB,AFGHANISTAN',
            'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:6065,Exhibit%20AB,AFGHANISTAN',
            'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:6335,Exhibit%20AB,ALBANIA',
            'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:6347,Exhibit%20AB,ALBANIA',
            'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:4776,Exhibit%20AB,ALGERIA',
            'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:6398,Exhibit%20AB,ANGOLA',
            'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:2244,Exhibit%20AB,ANTIGUA%20%26%20BARBUDA',
            'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:2987,Exhibit%20AB,ARUBA',
            'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:5965,Exhibit%20AB,ARUBA',
            'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:4450,Exhibit%20AB,AUSTRALIA',
            'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:1032,Exhibit%20AB,AUSTRALIA',
            'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:5041,Exhibit%20AB,AUSTRIA',
            'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:6193,Exhibit%20AB,AUSTRIA',
            'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:5916,Exhibit%20AB,AZERBAIJAN',
            'https://efile.fara.gov/pls/apex/wwv_flow.show']

        cls.expected_items = {}
        cls.expected_items[cls.links[0]] = [ForeignPrincipal (url= cls.url, country= 'AFGHANISTAN', state= None, reg_num = '5945', address= 'House #3 MRRD Road, Darul Aman, Kabul', foreign_principal= 'Transformation and Continuity, Ajmal Ghani', date= datetime(2014, 5, 5), registrant= 'Fenton Communications', exhibit_url= 'http://www.fara.gov/docs/5945-Exhibit-AB-20140505-10.pdf')]
        cls.expected_items[cls.links[1]] = [ForeignPrincipal (url= cls.url, country= 'AFGHANISTAN', state= 'VA', reg_num = '6065', address= '8105 Ainsworth Avenue, Springfield  22152', foreign_principal= 'Transformation and Continuity', date= datetime(2014, 7, 3), registrant= 'Roberti + White, LLC', exhibit_url= 'http://www.fara.gov/docs/6065-Exhibit-AB-20140703-5.pdf')]
        cls.expected_items[cls.links[2]] = [ForeignPrincipal (url= cls.url, country= 'ALBANIA', state= None, reg_num = '6335', address= 'Rr. Sami Frasheri 20/10 Tirana 20/10', foreign_principal= 'Ilir Meta, Chairman of LSI (Socialist Movement for Integration)', date= datetime(2016, 2, 24), registrant= 'Global Security and Innovative Strategies, LLC', exhibit_url= 'http://www.fara.gov/docs/6335-Exhibit-AB-20160304-4.pdf')]
        cls.expected_items[cls.links[3]] = [ForeignPrincipal (url= cls.url, country= 'ALBANIA', state= None, reg_num = '6347', address= 'Rruga e Elbasanit Vila Nr. 71, Tirana', foreign_principal= 'Albert Sino and Aurel Baci, Top Channel Shareholders', date= datetime(2016, 8, 11), registrant= 'Alexandria Group International, LLC', exhibit_url= 'http://www.fara.gov/docs/6347-Exhibit-AB-20160811-2.pdf')]
        cls.expected_items[cls.links[4]] = [ForeignPrincipal (url= cls.url, country= 'ALGERIA', state= 'DC', reg_num = '4776', address= '2118 Kalorama Road, NW, Washington  20008', foreign_principal= 'Government of the People\'s Democratic Republic of Algeria, Embassy', date= datetime(2007, 5, 25), registrant= 'Foley Hoag, LLP', exhibit_url= 'http://www.fara.gov/docs/4776-Exhibit-AB-20070525-9.pdf')]
        cls.expected_items[cls.links[5]] = [ForeignPrincipal (url= cls.url, country= 'ANGOLA', state= None, reg_num = '6398', address= '', foreign_principal= 'Movimento de Uniao Nacional (M.U.N) Angola', date= datetime(2016, 12, 1), registrant= 'Movimento de Uniao Nacional (M.U.N) Angola', exhibit_url= 'http://www.fara.gov/docs/6398-Exhibit-AB-20161201-2.pdf')]
        cls.expected_items[cls.links[6]] = [ForeignPrincipal (url= cls.url, country= 'ANTIGUA & BARBUDA', state= None, reg_num = '2244', address= 'Attorney General\'s Chambers, Government Office Complex Parliament Drive P.O. Box 118 St. Johns', foreign_principal= 'Government of Antigua and Barbuda', date= datetime(2012, 8, 24), registrant= 'Hogan Lovells US LLP', exhibit_url= 'http://www.fara.gov/docs/2244-Exhibit-AB-20140331-51.pdf')]
        cls.expected_items[cls.links[7]] = [ForeignPrincipal (url= cls.url, country= 'ARUBA', state= None, reg_num = '2987', address= 'Oranjestad', foreign_principal= 'Government of Aruba', date= datetime(1978, 12, 29), registrant= 'Aruba Tourism Authority', exhibit_url= 'http://www.fara.gov/docs/2987-Exhibit-AB-19781201-D0EE2403.pdf')]
        cls.expected_items[cls.links[8]] = [ForeignPrincipal (url= cls.url, country= 'ARUBA', state= None, reg_num = '5965', address= 'L.G. Smith Blvd. 76, Oranjestad', foreign_principal= 'Government of Aruba', date= datetime(2009, 12, 15), registrant= 'Hills Stern & Morley, LLP', exhibit_url= 'http://www.fara.gov/docs/5965-Exhibit-AB-20151221-5.pdf')]
        cls.expected_items[cls.links[9]] = [ForeignPrincipal (url= cls.url, country= 'AUSTRALIA', state= None, reg_num = '4450', address= 'Sydney', foreign_principal= 'New South Wales Tourism Commission (Government of New South Wales)', date= datetime(1990, 12, 18), registrant= 'Destination New South Wales', exhibit_url= 'http://www.fara.gov/docs/4450-Exhibit-AB-19901201-D1PNXS02.pdf')]
        cls.expected_items[cls.links[10]] = [ForeignPrincipal (url= cls.url, country= 'AUSTRALIA', state= None, reg_num = '1032', address= 'Melbourne', foreign_principal= 'Australian National Travel Association', date= datetime(1957, 6, 3), registrant= 'Tourism Australia', exhibit_url= 'http://www.fara.gov/docs/1032-Exhibit-AB-19680401-CYXK1I02.pdf')]
        
        # reusing the same reg_num and link, so we can assert if only one request is created
        cls.expected_items[cls.links[11]] = []
        cls.expected_items[cls.links[11]].append(ForeignPrincipal (url= cls.url, country= 'AUSTRIA', state= None, reg_num = '5041', address= 'Vienna', foreign_principal= 'Federal Economic Chamber of Austria (Wirtschftskammer Oesterreichs)', date= datetime(1995, 8, 17), registrant= 'Austrian Trade Commission in the U.S., Southern Region', exhibit_url= 'http://www.fara.gov/docs/5041-Exhibit-AB-19950920-DHOGQU01.pdf'))
        cls.expected_items[cls.links[11]].append(ForeignPrincipal (url= cls.url, country= 'AUSTRIA', state= 'NY', reg_num = '5041', address= 'New York', foreign_principal= 'Austrian National Tourist Office', date= datetime(1947, 10, 3), registrant= 'Austrian Tourist Office, Inc.', exhibit_url= 'http://www.fara.gov/docs/5041-Exhibit-AB-19950920-DHOGQU01.pdf'))
        
        cls.expected_items[cls.links[12]] = [ForeignPrincipal (url= cls.url, country= 'AUSTRIA', state= None, reg_num = '6193', address= 'Wiedner Hauptstrasse 63, 1045 Vienna', foreign_principal= 'Advantage Austria at the Austrian Federal Economic Chamber (WKO)', date= datetime(2013, 11, 4), registrant= 'Austrian Trade Commission, Chicago', exhibit_url= 'http://www.fara.gov/docs/6193-Exhibit-AB-20131104-1.pdf')]
        cls.expected_items[cls.links[13]] = [ForeignPrincipal (url= cls.url, country= 'AZERBAIJAN', state= 'CA', reg_num = '5916', address= '11766 Wilshire Boulevard, Suite 1410, Los Angeles  90025', foreign_principal= 'Consulate General of the Republic of Azerbaijan', date= datetime(2009, 3, 9), registrant= 'Tool Shed Group, LLC', exhibit_url= 'http://www.fara.gov/docs/5916-Exhibit-AB-20090309-1.pdf')]

    def test_parse_first_page(self):
        '''Test the parsing of the first page, asserting that all rows were scrapped and a request for the next page was returned'''
               
        parser = ForeignPrincipalsSpider()

        with open('foreign_principals/tests/first_page.html', 'r') as file:
            body = file.read().replace('\n', '')

            request = Request(url=self.url, callback=parser.parse)
            response = HtmlResponse(url=self.url, body=body, encoding='utf-8', request=request)

            for i, return_value in enumerate(parser.parse(response)):
                
                
                self.assertEqual(return_value.url, self.links[i])
                
                if i < 14:
                    self.assertEqual(type(return_value), Request)
                    self.assertEqual(return_value.method, 'GET')
                    self.assertTrue('items' in return_value.meta)
                    self.assertTrue(return_value.dont_filter)

                    for j, expected in enumerate(self.expected_items[self.links[i]]):

                       
                        item = return_value.meta['items'][j]
                        self.assertEqual(item['url'], self.url)
                        self.assertEqual(item['country'], expected['country'])
                        self.assertEqual(item['state'], expected['state'])
                        self.assertEqual(item['reg_num'], expected['reg_num'])
                        self.assertEqual(item['address'], expected['address'])
                        self.assertEqual(item['foreign_principal'], expected['foreign_principal'])
                        self.assertEqual(item['date'], expected['date'])
                        self.assertEqual(item['registrant'], expected['registrant'])
                else:
                    self.assertEqual(type(return_value), FormRequest)
                    self.assertEqual(return_value.method, 'POST')
                    self.assertEqual(return_value.body, 'p_request=APXWGT&p_instance=10454954032932&p_flow_id=171&p_flow_step_id=130&p_widget_num_return=15&p_widget_name=worksheet&p_widget_mod=ACTION&p_widget_action=PAGE&x01=80340213897823017&x02=80341508791823021&p_widget_action_mod=pgR_min_row%3D16max_rows%3D15rows_fetched%3D15'.encode())


            self.assertEqual(i, 14)      

    def test_parse_last_page(self):  
        '''Test the parsing of the last page, asserting that only the rows were scrapped and no additional requests were returned'''

        parser = ForeignPrincipalsSpider()

        with open('foreign_principals/tests/last_page.html', 'r') as file:
            body = file.read().replace('\n', '')

            request = Request(url=self.url, callback=parser.parse)
            response = HtmlResponse(url=self.url, body=body, encoding='utf-8', request=request)

            self.links = [
                'https://efile.fara.gov/pls/apex/f?p=171:200:10454954032932::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:6334,Exhibit%20AB,VIETNAM',
                'https://efile.fara.gov/pls/apex/f?p=171:200:10454954032932::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:5926,Exhibit%20AB,VIETNAM']

            for i, return_value in enumerate(parser.parse(response)):
                self.assertEqual(return_value.url, self.links[i])
                self.assertEqual(type(return_value), Request)
                self.assertEqual(return_value.method, 'GET')

            self.assertEqual(i, 1) 

    def test_parse_exhibit_url(self):
        '''Test the scrapping of the exhibit_url, asserting that all values returned were complete items to serialize'''
        parser = ForeignPrincipalsSpider()

        with open('foreign_principals/tests/exhibit_url.html', 'r') as file:
            body = file.read().replace('\n', '')
            url = 'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:5041,Exhibit%20AB,AUSTRIA'

            request = Request(url=url, callback=parser.parse)
            response = HtmlResponse(url=url, body=body, encoding='utf-8', request=request)

            response.meta['items'] =  deepcopy(self.expected_items[url])

            for i, return_value in enumerate(parser.parse_exhibit_url(response)):

                expected_item = self.expected_items[url][i]

                self.assertEqual(type(return_value), ForeignPrincipal)
                self.assertEqual(return_value['url'], expected_item['url'])
                self.assertEqual(return_value['country'], expected_item['country'])
                self.assertEqual(return_value['state'], expected_item['state'])
                self.assertEqual(return_value['reg_num'], expected_item['reg_num'])
                self.assertEqual(return_value['address'], expected_item['address'])
                self.assertEqual(return_value['foreign_principal'], expected_item['foreign_principal'])
                self.assertEqual(return_value['registrant'], expected_item['registrant'])
                self.assertEqual(return_value['exhibit_url'], expected_item['exhibit_url'])
                

            self.assertEqual(i, 1)

    def test_parse_null_exhibit_url(self):
        '''Test the scrapping when there is no exhibit_url in the page'''
        parser = ForeignPrincipalsSpider()

        with open('foreign_principals/tests/exhibit_url_null.html', 'r') as file:
            body = file.read().replace('\n', '')
            url = 'https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:5041,Exhibit%20AB,AUSTRIA'

            request = Request(url=url, callback=parser.parse)
            response = HtmlResponse(url=url, body=body, encoding='utf-8', request=request)

            response.meta['items'] =  deepcopy(self.expected_items[url])

            for i, return_value in enumerate(parser.parse_exhibit_url(response)):

                expected_item = self.expected_items[url][i]

                self.assertEqual(type(return_value), ForeignPrincipal)
                self.assertEqual(return_value['url'], expected_item['url'])
                self.assertEqual(return_value['country'], expected_item['country'])
                self.assertEqual(return_value['state'], expected_item['state'])
                self.assertEqual(return_value['reg_num'], expected_item['reg_num'])
                self.assertEqual(return_value['address'], expected_item['address'])
                self.assertEqual(return_value['foreign_principal'], expected_item['foreign_principal'])
                self.assertEqual(return_value['registrant'], expected_item['registrant'])
                self.assertEqual(return_value['exhibit_url'], None)
                

            self.assertEqual(i, 1)


if __name__ == '__main__':
    unittest.main()