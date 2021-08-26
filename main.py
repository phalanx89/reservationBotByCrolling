import configparser
from bs4 import BeautifulSoup
from restock import StockCheck
from telegram_bot import TelegramBot
from datetime import datetime
import time

# Loading config
config = configparser.ConfigParser()
config.read('config.ini')


# Initialize scraping classes
# TODO Consider function to lambda

def stockCheck(res):
    soup = BeautifulSoup(res.text, 'html.parser')
    elementToFind = soup.find("a", class_="_30d7I ")

    if elementToFind == None:
        return False

    return True

# main script
if __name__ == "__main__":
    #이학훈, 김민영, 이재익, 김병지, 손지훈, 김동훈, 최진우
    hakhunlee = 1465659915
    minyoungkim = 1760572904
    jaeiklee = 1874234225
    byungjikim = 1657705070
    jihoonson = 1530113968
    donghoonkim = 1908154690
    jinwoochoi = 1373332792

    #Date
    dateList = [20210925, 20211002, 20211009, 20211016, 20211023, 20211030]
    zelKova = 1202918454
    zelKovaRoomList = [
        3905136, 3903078, 3903080, 3903083, 3903090, 3903430, 3903444, 3903446, 3903448, 3903450, 3903451, 3903452, 3903453, 3903465, 3903466, #A
        3903520, 3903527, 3903524, 3903528, 3903529, #B
        3903480, 3903497, 3903502, 3903504, 3903506, 3903507, 3903509, 3903511, 3903514, 3903515, 3903517, 3903518, 3903519 #C
    ]

    helinoxCotOneTan = "http://www.helinoxstore.co.kr/shop/shopdetail.html?branduid=3546518&xcode=003&mcode=006&scode=&type=X&sort=manual&cur_code=003006&GfDT=bmx7W10%3D"

    urlList = []

    for date in dateList:
        for zelKovaRoom in zelKovaRoomList:
            urlList.append("https://pcmap.place.naver.com/accommodation/" + str(zelKova) + "/room/" + str(zelKovaRoom) + "?from=map&fromPanelNum=1&ts=1629963438648&checkin=" + str(date) + "&checkout=" + str(date + 1) + "&guest=2")

    userList = [hakhunlee, byungjikim, minyoungkim]
    # userList = [hakhunlee]

    bot = TelegramBot(config['TELEGRAM']['TOKEN'])

    interval_seconds = config['DEFAULT']['INTERVAL_SECONDS']

    for user in userList:
        bot.sendMessage(user, "안녕하세요 젤코바 캠핑장 주말 모니터링 시작합니다!")
        bot.sendMessage(user, str(dateList[0]) + " ~ " + str(dateList[-1]) + " 모니터링 합니다.")
        # for url in urlList:
        #     bot.sendMessage(user, "우리가 사야할 물품 링크에요. " + url)

    stockPerkList = []
    for idx, url in enumerate(urlList):
        stockPerkList.append(StockCheck("ZelkovaRoom" + str(idx + 1), url, stockCheck, "utf-8"))


    def check(checkTargetArray):
        return list(map(lambda item: item.statusChanged(), checkTargetArray))


    sendHealthCheck = False
    while True:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        cnt = 0
        for idx, stockPerk in enumerate(stockPerkList):
            returns = check([stockPerk])

            print("check[%03d] : %s"%(idx + 1, stockPerk.url))

            alerts = list(filter(lambda item: item[0], returns))

            for item in alerts:
                for user in userList:
                    # bot.sendMessage(user, "{} status has changed to {}".format(item[3].name, item[0]))
                    bot.sendMessage(user, "사이트 자리 났다!!!")
                    bot.sendMessage(user, "링크 : " + stockPerk.url)
            cnt += 1
        print(str(cnt) + "개 사이트 확인 완료")

        # health check
        currentTime = datetime.now()
        if currentTime.hour == 12 and currentTime.minute == 0:
            if not sendHealthCheck:
                for user in userList:
                    bot.sendMessage(user, "정각알리미 : 점심 맛있게 드세요!")
                sendHealthCheck = True
        elif currentTime.hour == 18 and currentTime.minute == 0:
            if not sendHealthCheck:
                for user in userList:
                    bot.sendMessage(user, "정각알리미 : 저녁 맛있게 드세요!")
                sendHealthCheck = True
        else:
            sendHealthCheck = False

        time.sleep(int(interval_seconds))