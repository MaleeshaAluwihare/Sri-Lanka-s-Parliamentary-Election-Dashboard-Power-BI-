import scrapy

class DistrictSpider(scrapy.Spider):
    name = "districtspider"
    allowed_domains = ["results.elections.gov.lk"]
    start_urls = ["https://results.elections.gov.lk"]

    def parse(self, response):
        # Extract district links
        links = response.xpath('//li[contains(@class, "nav-item nav-category")]/following-sibling::li[contains(@class, "nav-item")]')

        for link in links:
            districtlink = link.xpath('.//a[@class = "nav-link"]/@href')[1].get()
            
            if districtlink:
                # Follow each district link and pass it to parse_district
                yield response.follow(districtlink, self.parse_district)

    def parse_district(self, response):
        # Extract table rows containing party data
        rows = response.xpath('//div[contains(@class, "table-responsive")]/div[contains(@class, "wrapper") and contains(@class, "border-bottom")]')

        for row in rows:
            # Extract party name
            party_name = row.xpath('.//div[@class="ms-3"]/p[@class="mb-0 fw-bold"]/text()').get()
            
            # Extract votes
            votes = row.xpath('.//div[@class="ms-5"][1]/p[@class="mb-0 fw-bold text-end"]/text()').get()
            
            # Extract percentage
            percentage = row.xpath('.//div[@class="ms-5"][2]/p[@class="mb-0 fw-bold text-end"]/text()').get()
            
            # Extract seats
            seats = row.xpath('.//div[@class="ms-5"][3]/p[@class="mb-0 fw-bold text-left"]/text()[normalize-space()]').get().strip()

            if party_name and votes and percentage and seats:
                yield {
                    'district': response.url.split('=')[-1],
                    'party_name': party_name.strip(),
                    'votes': votes.strip(),
                    'percentage': percentage.strip(),
                    'seats': seats.strip()
                }
