import scrapy


class ResultspiderSpider(scrapy.Spider):
    name = "resultspider"
    allowed_domains = ["results.elections.gov.lk"]
    start_urls = ["https://results.elections.gov.lk"]

    def parse(self, response):
        #select all parties
        party_containers = response.css("div.card.mb-3")

        for party in party_containers:
            yield{
                'party_name': party.css("h6.mb-1::text").get(),
                'vote_count': party.css("div.votes p.mb-0::text").get(),
                'vote_precentage': party.css("div.percentage p.mb-0::text").get(),
                'seats': party.css("div.seats-badge span.badge::text").get(),
            }
            
