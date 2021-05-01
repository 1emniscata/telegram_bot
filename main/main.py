from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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
            for i in range(30):
                rate = self.xpath_exists(f'//*[@id="currency_tbody"]/tr[{i}]/td[3]')
                bank_title = self.xpath_exists(f'//*[@id="currency_tbody"]/tr[{i}]/td[1]/span/a')
                if rate and bank_title:
                    bank = self.browser.find_element_by_xpath(
                        f'//*[@id="currency_tbody"]/tr[{i}]/td[1]/span/a').text
                    time.sleep(7)
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
            my_banks = ['Приорбанк', 'Беларусбанк', 'Белагропромбанк', 'БПС-Сбербанк']  # Only these banks is located in Osipovichi
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

            print('Курс продажи доллара в банках города Осиповичи:')
            for bank in all_rates_mine:
                print(f'{bank}: {all_rates_mine[bank]}')

            for bank in all_rates_mine:
                if all_rates_mine[bank] == min(all_rates_mine.values()):
                    result = f'Лучший курс в банке {bank}: {min(all_rates_mine.values())}'
                    len_of_separator = len(result)
                    print('-' * len_of_separator)
                    print(result)
        except NoSuchElementException as err:
            print(err)
        finally:
            self.browser.close()
            self.browser.quit()


a = Bot()
a.download_data()