#  Copyright (c) To Duc Anh 2022.
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import scrapy
import os
import json
import subprocess
import time
import pandas as pd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) "
                  "Gecko/20100101 Firefox/46.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0"
}


def is_file_empty(file_path):
    """ Check if file is empty by confirming if its size is 0 bytes"""
    return os.path.isfile(file_path) and os.path.getsize(file_path) == 0


class AutodataSpider(scrapy.Spider):
    name = 'brands_extractor'
    PREFIX = 'https://www.auto-data.net'

    def start_requests(self):
        urls = [
            'https://www.auto-data.net/en/allbrands',
        ]
        for url in urls:
            self.log('Extracting %s' %url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        car_brands = []
        container = response.xpath('//div[@class="brands"]')
        for div in container:
            link_container = div.xpath('.//a[@class="marki_blok"]')
            for link in link_container:
                url = self.PREFIX + link.xpath('@href').extract()[0]
                car_brands.append(url)

        filename = 'car_specifications/resources/cars_links.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(car_brands))
        self.log(f'Saved file {filename}')



class CarModelSpider(scrapy.Spider):
    name = 'models_extractor'
    PREFIX = 'https://www.auto-data.net'

    def start_requests(self):
        file_path = 'car_specifications/resources/cars_links.txt'
        with open(file_path, 'r', encoding='utf-8') as file:
            urls = file.readlines()
        for url in urls:
            url = url.split('\n')[0]
            time.sleep(0.2)
            yield scrapy.Request(url=url, callback=self.parse, encoding='utf-8')

    def parse(self, response):
        container = response.xpath('//ul[@class="modelite"]')
        for div in container:
            link_container = div.xpath('.//a[@class="modeli"]')
            for link in link_container:
                url = self.PREFIX + link.xpath('@href').extract()[0]
                yield {'links': url}



class CarGenerationSpider(scrapy.Spider):
    name = 'generations_extractor'
    PREFIX = 'https://www.auto-data.net'

    def start_requests(self):
        file_path = 'car_specifications/resources/car_models.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            urls = [line.get('links') for line in data]
        for url in urls:
            url = url.split('\n')[0]
            self.log(url)
            time.sleep(0.3)
            yield scrapy.Request(url=url, callback=self.parse, encoding='utf-8', headers=HEADERS)

    def parse(self, response):
        tree = response.xpath('//table[@id="generr"]/tr[starts-with(@class,"f l")]/th[1]/a/@href').extract()
        for link in tree:
            yield {'car_generations': self.PREFIX + link}


class CarGenerationYearSpider(scrapy.Spider):
    name = 'year_extractor'
    PREFIX = 'https://www.auto-data.net'

    def start_requests(self):
        file_path = 'car_specifications/resources/cars_generations.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            urls = [line.get('car_generations') for line in data]

        for url in urls:
            url = url.split('\n')[0]
            time.sleep(0.3)
            yield scrapy.Request(url=url, callback=self.parse, encoding='utf-8', headers=HEADERS)

    def parse(self, response):
        tree = response.xpath('//table[@class="carlist"]/tr[starts-with(@class,"i l")]/th[1]/a/@href').extract()
        for link in tree:
            yield {'cars_years': self.PREFIX + link}

class CarSpecsSpider(scrapy.Spider):
    name = 'cars_specs_extractor'
    PREFIX = 'https://www.auto-data.net'

    def start_requests(self):
        file_path = 'car_specifications/resources/cars_years_generations.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            urls = [line.get('cars_years') for line in data]
        for url in urls:
            url = url.split('\n')[0]
            time.sleep(0.2)
            yield scrapy.Request(url=url, callback=self.parse, encoding='utf-8', headers=HEADERS)

    def parse(self, response):
        car = {}
        table = pd.read_html(response.text)
        table = table[1].T
        data = table.to_dict()
        keys = data.keys()
        for key in keys:
            row = data.get(key)
            fields = row.get('General information')
            values = row.get('General information.1')
            car[fields] = values
        yield car

def main():
    extractor_dict = {
        'models_extractor': 'car_specifications/resources/car_models.json',
        'generations_extractor': 'car_specifications/resources/cars_generations.json',
        'year_extractor': 'car_specifications/resources/cars_years_generations.json',
        'cars_specs_extractor': 'car_specifications/resources/cars_specs.json'
    }
    for crawler, path in extractor_dict.items():
        subprocess.run(f'scrapy crawl {crawler} -o {path}')

if __name__ == '__main__':
    main()


