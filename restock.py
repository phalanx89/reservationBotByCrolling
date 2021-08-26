import requests

class StockCheck:

    def __init__(self, name, url, checkMethod, encoding):
        self.name = name
        self.url = url
        self.checkMethod = checkMethod
        self.encoding = encoding
        self.last_status = False


    def getResponse(self):
        # TODO Pass parameters def getResponse(self, params):
        # TODO Add some error handling
        URL = self.url

        return requests.get(URL)


    def check(self):
        res = self.getResponse()

        if res.encoding != self.encoding:
            res.encoding = self.encoding

        return self.checkMethod(res)

    def statusChanged(self):
        status = self.check()

        if (self.last_status != status):
            self.last_status = status
            return (True, not (self.last_status), self.last_status, self)

        return (False, self.last_status, status, self)

    def __str__(self):
        return "{} is {}".format(self.name, self.last_status)



if __name__ == "__main__":
    def legoshopCheck(res):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(res.text, 'html.parser')
        stock_div = soup.find("p", attrs={"data-test": "product-overview-availability"})

        if stock_div == None:
            return True

        stock_result = stock_div.text

        import re

        p = re.compile('품절')
        m = p.search(stock_result)

        return True if m == None else False


    lego_friends_perk = StockCheck("Friends Central Perk"
                                   , "https://www.lego.com/ko-kr/product/central-perk-21319"
                                   , legoshopCheck, "utf-8")
    stock = lego_friends_perk.check()
    print(lego_friends_perk.name, "Available? ", stock)
    (status_changed, last_status, current_status) = lego_friends_perk.statusChanged()
    print(lego_friends_perk.name, "Status Changed? ", status_changed, ", Last Status? ", last_status,
          ", Current Status? ", current_status)
