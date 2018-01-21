import re


class NvshensURLMatcher():
    def __init__(self):
        self.pattern_domain = \
            re.compile("^https://www\.nvshens\.com(/)?")

        self.pattern_star_album_list_page = \
            re.compile("^https://www\.nvshens\.com/girl/\d+/album/$")

        self.pattern_album_page = \
            re.compile("^https://www\.nvshens\.com/g/\d+/(\d+\.html)?$")

        self.pattern_star_page = \
            re.compile("^https://www\.nvshens\.com/girl/\d+/$")

        self.pattern_article_page = \
            re.compile("^https://www\.nvshens\.com/article/\d+/")

        self.pattern_tag_page_gallery = \
            re.compile("^https://www\.nvshens\.com/gallery/([a-zA-Z0-9]+/)?(\d+\.html)?$")

        self.pattern_tag_page_tag = \
            re.compile("^https://www\.nvshens\.com/tag/([a-zA-Z0-9]+/)?(\d+\.html)?$")

    # https://www.nvshens.com/g/19340/
    # https://www.nvshens.com/g/24928/3.html
    def match_pattern_album_page(self, url):
        return self.pattern_album_page.match(url)

    #https://www.nvshens.com/girl/21132/album/
    def match_pattern_star_album_list_page(self, url):
        return self.pattern_star_album_list_page.match(url)

    def match_pattern_article_page(self, url):
        return self.pattern_article_page.match(url)

    # https://www.nvshens.com/girl/25401/
    def match_pattern_star_page(self, url):
        return self.pattern_star_page.match(url)

    def match_pattern_tag_page(self, url):
        return self.pattern_tag_page_gallery.match(url) or \
                self.pattern_tag_page_tag.match(url)

    def match_pattern_domain(self, url):
        return self.pattern_domain.match(url)

    def match_pattern_extract_page(self, url):
        return self.match_pattern_domain(url) #and not self.match_pattern_article_page(url)


if __name__ == '__main__':
    matcher = NvshensURLMatcher()
    url = "https://www.nvshens.com/g/22808/"
    url = "https://www.nvshens.com/gallery/qizhi/"
    print(matcher.match_pattern_tag_page(url))

    url = "https://www.nvshens.com/girl/25401/"
    print(matcher.match_pattern_star_page(url))

    url = "https://www.nvshens.com/tag/adf/"
    print(matcher.match_pattern_tag_page(url))

    url = "https://www.nvshens.com/tag/adf/2.html"
    print(matcher.match_pattern_tag_page(url))

    url = "https://www.nvshens.com/girl/21132/album/"
    print(matcher.match_pattern_star_album_list_page(url))
