# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from crawler.items import AllocineItem

URL = 'http://www.allocine.fr/salle/cinemas-pres-de-113315/?page={page}'

class AllocineSpider(scrapy.Spider):
    name = "allocine"
    allowed_domains = ["allocine.fr"]
    start_urls = (
        'http://www.allocine.fr/salle/cinemas-pres-de-113315/',
    )

    def start_requests(self):
        for index in range(0,19):
            yield scrapy.Request(URL.format(page=index))


    def parse(self, response):
        if response.status  == 404:
            raise CloseSpider("The page doesn't exist")

        theater_bloc_list = response.css(".theaterblock")
        theater_name_list = theater_bloc_list.css(".titlebar h2 a::text").extract()
        theater_adress_list = theater_bloc_list.css(".theaterblock .lighten::text").extract()

        for i in range(0, len(theater_bloc_list)):

            movies_playing = theater_bloc_list[i].css(".j_w .underline::text").extract()
            movies_times_list = theater_bloc_list[i].css(".times ul")

            for x in range(0,len(movies_playing)):
                times = movies_times_list[x].css("li em::attr(data-times)").extract()
                datetimes = movies_times_list[x].css("li em::attr(data-datetime)").extract()

                for y in range(0, len(times)):
                    item = AllocineItem()
                    item['date'] = datetimes[y]
                    item['cinema_name'] = theater_name_list[i]
                    item['cinema_adress'] = theater_adress_list[i]
                    item['movie_name'] = movies_playing[x]

                    time = times[y]
                    bad_char = '[]"'
                    for char in bad_char:
                        time = time.replace(char, '')

                    start, duration, end = time.split(',')
                    item['movie_start'] = start
                    item['movie_end'] = end
                    yield item
