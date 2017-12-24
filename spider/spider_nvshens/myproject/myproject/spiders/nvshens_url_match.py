import re


class NvshensURLMatcher():
    def __init__(self):
        self.pattern_domain = \
            re.compile("^https://www\.nvshens\.com(/)?")

        self.pattern_album_page = \
            re.compile("^https://www\.nvshens\.com/g/\d+/(\d+\.html)?$")

        self.pattern_star_page = \
            re.compile("^https://www\.nvshens\.com/girl/\d+/")

        self.pattern_tag_page = \
            re.compile("^https://www\.nvshens\.com/gallery/[a-zA-Z0-9]+/(\d+\.html)?$")

    # https://www.nvshens.com/g/19340/
    # https://www.nvshens.com/g/24928/3.html
    def match_pattern_album_page(self, url):
        return self.pattern_album_page.match(url)

    # https://www.nvshens.com/girl/25401/
    def match_pattern_star_page(self, url):
        return self.pattern_star_page.match(url)

    def match_pattern_tag_page(self, url):
        return self.pattern_tag_page.match(url)

    def match_pattern_domain(self, url):
        return self.pattern_domain.match(url)


if __name__ == '__main__':
    macher = NvshensURLMatcher()
    url = "https://www.nvshens.com/g/22808/"
    url = "https://www.nvshens.com/gallery/qizhi/"
    print(macher.match_pattern_tag_page(url))