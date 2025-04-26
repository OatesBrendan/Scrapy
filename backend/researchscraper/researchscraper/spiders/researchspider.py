import scrapy

class ResearchSpider(scrapy.Spider):
    name = 'research'
    start_urls = ['https://eprints.qut.edu.au/view/person/Perrin,_Dimitri.html']

    def parse(self, response):
        for product in response.css('div.ep_view_result'):
            # Get the citation span
            citation = product.css('span.citation')
            
            # Extract title - this is the link that appears right after the year
            # The year is in parentheses, e.g. "(2023)"
            title = None
            
            # First find the link that contains the title - it's the first link after the year
            title_element = citation.xpath('.//a[contains(@href, "eprints.qut.edu.au") and not(contains(@class, "creators_name"))]')
            
            if title_element:
                # Extract the text, cleaning up any HTML comments
                title_text = ''.join(title_element.xpath('.//text()').getall())
                title = title_text.strip()
                # Clean up potential HTML comments
                title = title.replace('<!--if test="article_type = \'erratum\'">Correction to: </if-->', '')
                title = title.replace('<!--if test="type = \'book_section\' and book_section_type = \'erratum\'">Correction to: </if-->', '')
                title = title.strip()
            
            # Extract URL for the paper
            url = citation.xpath('.//a[contains(@href, "eprints.qut.edu.au") and not(contains(@class, "creators_name"))]/@href').get()
            
            # Extract all authors
            authors = citation.css('span.person_name::text').getall()
            
            # Extract year
            year = product.xpath('./preceding-sibling::h2[1]/text()').get()
            
            yield {
                'title': title,
                'authors': authors,
                'url': url,
                'year': year
            }