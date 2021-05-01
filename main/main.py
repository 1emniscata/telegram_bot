from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from auth_data import token
import telebot
import time


class Bot:

    def __init__(self):
        self.browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

    def xpath_exists(self, xpath):

        browser = self.browser
        try:
            browser.find_element_by_xpath(xpath)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def download_data(self):
        try:
            self.browser.get('https://myfin.by/currency/osipovichi?sort=usd_sell.desc')
            time.sleep(5)
            for i in range(1):
                self.browser.execute_script('window.scroll(0, document.body.scrollHeight);')
            time.sleep(5)
            # sell_rate = self.browser.find_element_by_xpath(
            #     '//*[@id="currency_tbody"]/tr[14]/td[3]').text
            time.sleep(15)
            # best_bank = self.browser.find_element_by_xpath(
            #     '//*[@id="currency_tbody"]/tr[14]/td[1]/span/a').text
            # '//*[@id="currency_tbody"]/tr[1]/td[1]').text
            # '//*[@id="currency_tbody"]/tr[1]/td[1]/span[1]/a')
            # links = self.browser.find_elements_by_tag_name('a')
            # items = [item.get_attribute('href') for item in links]
            # print(items)
            '//*[@id="currency_tbody"]/tr[3]/td[3]'
            '//*[@id="currency_tbody"]/tr[5]/td[3]'
            '//*[@id="adfox_157433254170785471"]/td[3]'  # Nembo
            ''
            '//*[@id="currency_tbody"]/tr[4]/td[3]'   # Priorbank
            '//*[@id="currency_tbody"]/tr[6]/td[3]'   # Belarusbank
            '//*[@id="currency_tbody"]/tr[8]/td[3]'   # Belagro
            '//*[@id="currency_tbody"]/tr[10]/td[3]'  # BPS

            '//*[@id="currency_tbody"]/tr[7]/td[3]'
            '//*[@id="currency_tbody"]/tr[7]/td[1]/span/a'  # Priorbank
            '//*[@id="currency_tbody"]/tr[9]/td[3]'
            '//*[@id="currency_tbody"]/tr[9]/td[1]/span/a'  # Belarusbank
            '//*[@id="currency_tbody"]/tr[12]/td[3]'
            '//*[@id="currency_tbody"]/tr[12]/td[1]/span/a'  # Belagro
            '//*[@id="currency_tbody"]/tr[14]/td[3]'
            '//*[@id="currency_tbody"]/tr[14]/td[1]/span/a'  # BPS

            all_rates = {}
            for i in range(20):
                rate = self.xpath_exists(f'//*[@id="currency_tbody"]/tr[{i}]/td[3]')
                bank_title = self.xpath_exists(f'//*[@id="currency_tbody"]/tr[{i}]/td[1]/span/a')
                if rate and bank_title:
                    bank = self.browser.find_element_by_xpath(
                        f'//*[@id="currency_tbody"]/tr[{i}]/td[1]/span/a').text
                    time.sleep(6)
                    all_rates[bank] = self.browser.find_element_by_xpath(
                        f'//*[@id="currency_tbody"]/tr[{i}]/td[3]').text
            # for i in range(12):
            #     print(self.xpath_exists(f'//*[@id="currency_tbody"]/tr[{i}]/td[3]'))
            #     # bank = self.browser.find_element_by_xpath(
            #     #                 f'//*[@id="currency_tbody"]/tr[{i}]/td[1]/span/a')
            #     print(self.xpath_exists(f'//*[@id="currency_tbody"]/tr[{i}]/td[1]/span/a'))
            #     # print(bank)
            #     print('It was operation №', i)
            # time.sleep(5)

            # print(best_bank)
            # print(sell_rate)
            # print(f'Банк с лучшим курсом продажи: {best_bank}.\nЛучший курс: {sell_rate}.')
            banks = list(all_rates.keys())
            rates = list(all_rates.values())
            my_banks = ['Приорбанк', 'Беларусбанк', 'Белагропромбанк', 'БПС-Сбербанк']  # Banks is located in Osipovichi
            all_rates_mine = {}
            for i in range(len(banks)):
                if banks[i] in my_banks:
                    all_rates_mine[banks[i]] = rates[i]  # Rates only for local banks
            '''
            print('Курс продажи доллара:')
            for i in range(len(banks)):
                if banks[i] in my_banks:
                    # print(f'Банк: {banks[i]}, курс: {rates[i]}')
                    print(f'{banks[i]}: {rates[i]}')
                    best_rate = 100
                    # print(f'Лучший курс: {min(rates)}')
            # print('Min value:', min(all_rates.values()))
            '''

            message = ''
            print('Курс продажи доллара в банках города Осиповичи:')
            message += 'Курс продажи доллара в банках города Осиповичи:\n'
            for bank in all_rates_mine:
                print(f'{bank}: {all_rates_mine[bank]}')
                message += f'{bank}: {all_rates_mine[bank]}\n'

            for bank in all_rates_mine:
                if all_rates_mine[bank] == min(all_rates_mine.values()):
                    result = f'Лучший курс в банке {bank}: {min(all_rates_mine.values())}'
                    len_of_separator = len(result)
                    print('-' * len_of_separator)
                    print(result)
                    message += '-' * len_of_separator + '\n' + result
            return message
        except NoSuchElementException as err:
            print(err)
        finally:
            self.browser.close()
            self.browser.quit()

    def telegram_bot(self, tg_token):
        bot = telebot.TeleBot(tg_token)

        total_message = self.download_data()

        @bot.message_handler(commands=['start'])
        def start(message):
            msg = 'Привет! Это Telegram бот для показа лучшего курса продажи доллара в Осиповичах.'
            bot.send_message(message.chat.id, msg)

        @bot.message_handler(content_types=["text"])
        def send_info(message):
            if message.text.lower() == 'show':
                try:
                    # self.download_data()
                    bot.send_message(message.chat.id, total_message)
                except Exception as err:
                    print(err)
                    bot.send_message(message.chat.id, 'Что-то пошло не так')
            else:
                print('По-моему, ты набрала неправильную команду')

        bot.polling()


a = Bot()
# a.download_data()
a.telegram_bot(token)
