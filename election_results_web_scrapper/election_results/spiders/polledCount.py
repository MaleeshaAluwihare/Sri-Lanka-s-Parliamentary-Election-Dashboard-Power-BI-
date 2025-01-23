import scrapy


class PolledcountSpider(scrapy.Spider):
    name = "polledCount"
    allowed_domains = ["results.elections.gov.lk"]
    start_urls = ["https://results.elections.gov.lk"]

    def parse(self, response):
        # Extract district links
        links = response.xpath('//li[contains(@class, "nav-item nav-category")]/following-sibling::li[contains(@class, "nav-item")]')

        for link in links:
            districtlink = link.xpath('.//a[@class = "nav-link"]/@href')[1].get()
            
            if districtlink:
                # Follow each district link and pass it to parse_district
                yield response.follow(districtlink, self.parse_table)

    def parse_table(self,response):
        rows = response.xpath("//div[contains(@class, 'table-responsive') and contains(@class, 'mt-1')]//table[contains(@class, 'table') and contains(@class, 'select-table')]//tr")

        for row in rows:
            title = row.xpath('./td[1]/p/text()').get()
            value = row.xpath('./td[2]/p/text()').get()
            percentage = row.xpath('./td[3]/p/text()').get()

            yield {
                'district': response.url.split('=')[-1],
                'title' : title.strip() if title else None,
                'value' : value.strip() if value else None,
                'percentage' : percentage.strip() if percentage else None
            }
