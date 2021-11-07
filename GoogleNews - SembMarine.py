# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 11:13:08 2020

@author: Eugene
"""
# -*- coding: utf-8 -*-
import scrapy
from datetime import date
from scrapy.loader import ItemLoader
from ScrapyTest.items import GNewsSembMarineItem
from scrapy.shell import inspect_response
from scrapy.shell import open_in_browser
from urllib.parse import urljoin

# google search specific for sembcorp marine
websites = ['https://www.google.com/search?q=sembcorp+marine&biw=1421&bih=1441&tbm=nws&sxsrf=AOaemvIrHSAYUnAPPXZE48Pr8tmmG7Wf9Q%3A1636201107994&ei=k3KGYdWVPJmI4-EPhIq7wAU&oq=sembcorp+marine&gs_l=psy-ab.3...0.0.0.1382217.0.0.0.0.0.0.0.0..0.0....0...1c..64.psy-ab..0.0.0....0.fgzKudfqfXk']

class GNewsSembMarineSpider(scrapy.Spider): 
    
    name = 'GNewsSembMarine'
    start_urls = websites
    
    # to save scraped output as json
    custom_settings = {'FEED_FORMAT': 'json',
                       'FEED_URI': 'GNewsSembMarine.json'}
    
    # use xpath to extract title, body, date published of search results. Run through a number of pages of search results using the next link.
	
    def parse(self, response):

        title = response.xpath('//div[contains (@class, "BNeawe vvjwJb AP7Wnd")]/text()').extract()
        
        body = response.xpath('//div[contains (@class, "BNeawe s3v9rd AP7Wnd")]/text()').extract()
        
        date_published = response.xpath('//span[contains (@class, "xUrNXd UMOHqf")]/text()').extract()
        
        page = response.xpath('//div[@id = "result-stats"]/text()').extract()
        
        date_published2 = []
        
        for i in range(len(date_published)):
            
            if ' · ' not in date_published[i]:
                
                date_published2.append(date_published[i])

        next_page = response.xpath('//a[@class ="nBDE1b G5eFlf"]/@href').extract()

        if "start=200" in next_page[-1]:
            print(next_page[-1])
            print(Done)        
        
        if ((next_page is not None) & ~("start=200" in next_page[-1])):
            str1 = 'https://www.google.com'
            next_page2 = str1 + next_page[-1]
            yield scrapy.Request(next_page2, callback =self.parse)

        for row in zip(title, body,date_published2):
            
            scraped_info = {
                'title': row[0],
                'body' : row[1],
                'date_published' : row[2],
                'date_extracted'  : date.today() 
                }
            
            yield scraped_info
                    
            item = GNewsSembMarineItem()
            item['title'] = row[0]
            item['body'] = row[1]
            item['date_published'] = row[2]
            item['date_extracted'] = date.today()
            
            yield item
            

	
    
 
