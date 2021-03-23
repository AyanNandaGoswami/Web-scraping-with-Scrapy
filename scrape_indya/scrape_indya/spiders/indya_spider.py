import scrapy


class IndyaSpiderSpider(scrapy.Spider):
    name = 'indya'
    start_urls = [
        'https://www.houseofindya.com/zyra/necklace-sets/cat'
    ]

    
    '''
        this 'my_parse' function is use to extract each product's decsription from the given link in 'next_page' variable, and
        after extract the description, it bundle 'product_name', 'product_price', 'product_image_link' and 'product_decsription'
        to a dict.
    '''
    def my_parse(self, response, product_name, product_price, product_image_link):
        product_description = response.css('#tab-1 p::text').extract()
        yield {
            'product_name': product_name,
            'product_price': product_price,
            'product_image_link': product_image_link,
            'product_description': product_description
        }


    def parse(self, response):
        all_li_items = response.css('ul#JsonProductList li')

        # iterate each li items and get product name, product price and the url of the product
        for item in all_li_items:
            product_name = item.css('a div.catgName p').css('::text').extract()     # get product name
            product_price = item.css('li::attr(data-price)').extract()     # get product price
            product_image_link =  item.css('a div.catgItem img::attr(data-original)').extract()     # get image link of the product

            '''
                in 'next_page' variable, here I store the link of each product's description page [like, https://www.houseofindya.com/gold-kundan-red-drop-meena-earring-necklace-set-290/iprdt]
                and from this page I extract the decsription of each product
            '''
            next_page = item.css('li::attr(data-url)').get()
 
            request = scrapy.Request(next_page, callback=self.my_parse)     # here i create a request for next_page

            '''
                pass 'product_name', 'product_price', 'product_image_link' as an argument
            '''
            request.cb_kwargs['product_name'] = product_name    
            request.cb_kwargs['product_price'] = product_price
            request.cb_kwargs['product_image_link'] = product_image_link

            yield request




