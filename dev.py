import time
import bs4
import os
import pandas
import tqdm
import json
import multiprocessing
import selenium.webdriver.chrome.options
import selenium.webdriver.common.by
import selenium.webdriver.support.expected_conditions
import selenium.webdriver.support.ui
import selenium.webdriver.support

class Agent:

    def __init__(
        self, 
        display: bool, 
        domain: str,
    ) -> None:
        self.display = display
        self.domain = domain
        return

    def openBrowser(self) -> bool:
        option = selenium.webdriver.chrome.options.Options()
        option.add_argument("--disable-blink-features=AutomationControlled")
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_argument("--disable-notifications")
        option.add_argument("user-agent=Chromium")
        if(not self.display):
            option.add_argument("--headless")  # 如需顯示瀏覽器畫面可註解此行
            pass
        browser = selenium.webdriver.Chrome(options=option)
        self.browser = browser
        return(True)

    def visitHome(self) -> bool:
        self.browser.get(self.home)
        return(True)

    def searchHistory(
        self, 
        department: int, 
        city: str, 
        area: str, 
        year: tuple, 
        month: tuple
    ) -> bool:
        command = (self.rule.XPATH, '//frame')
        element = self.browser.find_element(*command)
        self.browser.switch_to.frame(element)
        if(department==1):
            symbol = f'//ul[@class="nav nav-pills"]/li[{department}]/a'
            command = (self.rule.XPATH, symbol)
            button = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            button.click()
            # print("【訊息】：選擇買賣查詢部門")
            head = '//form[@id="main_form"]'
            # City
            command = (self.rule.XPATH, f'{head}/div[1]/div[1]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            selection = self.selection(node)
            selection.select_by_value(city)
            # print(f"【訊息】：選擇{}縣市")
            # Area
            keep = True
            while(keep):
                command = (self.rule.XPATH, f'{head}/div[1]/div[2]/select')
                try:
                    node = self.event(self.browser, 5).until(
                        self.condition.presence_of_element_located(command)
                    )
                    selection = self.selection(node)
                    selection.select_by_value(area) # 太快會錯
                    pass
                except:
                    _ = node
                    _ = selection
                    continue
                keep = False
                continue
            loop = [(3, 1), (3, 2), (4, 1), (4, 2)]
            for row, column in loop:
                command = (
                    self.rule.XPATH, 
                    f'{head}/div[1]/div[{row}]/div[{column}]'
                )
                box = self.event(self.browser, 5).until(
                    self.condition.presence_of_element_located(command)
                )
                value = box.find_element(
                    self.rule.XPATH, 'input'
                ).get_attribute('value')
                if(value=='1,2'): continue
                box.click()
                continue
            _ = loop
            # Year
            command = (self.rule.XPATH, f'{head}/div[1]/div[12]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{year[0]}')
            # month
            command = (self.rule.XPATH, f'{head}/div[1]/div[13]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{month[0]}')
            #
            command = (self.rule.XPATH, f'{head}/div[1]/div[14]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{year[1]}')
            #
            command = (self.rule.XPATH, f'{head}/div[1]/div[15]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{month[1]}')
            #
            command = (self.rule.XPATH, '//*[text()="搜尋"]')
            element = self.event(self.browser, 5).until(
                self.condition.presence_of_all_elements_located(command)
            )
            button = element[2]
            button.click()
            pass
        if(department==2):
            symbol = f'//ul[@class="nav nav-pills"]/li[{department}]/a'
            command = (self.rule.XPATH, symbol)
            button = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            button.click()
            # print("【訊息】：選擇買賣查詢部門")
            head = '//form[@id="main_form"]'
            # City
            command = (self.rule.XPATH, f'{head}/div[1]/div[1]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            selection = self.selection(node)
            selection.select_by_value(city)
            # print(f"【訊息】：選擇{}縣市")
            # Area
            keep = True
            while(keep):
                command = (self.rule.XPATH, f'{head}/div[1]/div[2]/select')
                try:
                    node = self.event(self.browser, 5).until(
                        self.condition.presence_of_element_located(command)
                    )
                    selection = self.selection(node)
                    selection.select_by_value(area) # 太快會錯
                    pass
                except:
                    _ = node
                    _ = selection
                    continue
                keep = False
                continue
            # Year
            command = (self.rule.XPATH, f'{head}/div[1]/div[12]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{year[0]}')
            # month
            command = (self.rule.XPATH, f'{head}/div[1]/div[13]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{month[0]}')
            #
            command = (self.rule.XPATH, f'{head}/div[1]/div[14]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{year[1]}')
            #
            command = (self.rule.XPATH, f'{head}/div[1]/div[15]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{month[1]}')
            #
            command = (self.rule.XPATH, '//*[text()="搜尋"]')
            element = self.event(self.browser, 5).until(
                self.condition.presence_of_all_elements_located(command)
            )
            button = element[2]
            button.click()
            pass
        if(department==3):
            symbol = f'//ul[@class="nav nav-pills"]/li[{department}]/a'
            command = (self.rule.XPATH, symbol)
            button = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            button.click()
            # print("【訊息】：選擇買賣查詢部門")
            head = '//form[@id="main_form"]'
            # City
            command = (self.rule.XPATH, f'{head}/div[1]/div[1]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            selection = self.selection(node)
            selection.select_by_value(city)
            # print(f"【訊息】：選擇{}縣市")
            # Area
            keep = True
            while(keep):
                command = (self.rule.XPATH, f'{head}/div[1]/div[2]/select')
                try:
                    node = self.event(self.browser, 5).until(
                        self.condition.presence_of_element_located(command)
                    )
                    selection = self.selection(node)
                    selection.select_by_value(area) # 太快會錯
                    pass
                except:
                    _ = node
                    _ = selection
                    continue
                keep = False
                continue
            loop = [(3, 1), (4, 1), (4, 2)]
            for row, column in loop:
                command = (
                    self.rule.XPATH, 
                    f'{head}/div[1]/div[{row}]/div[{column}]'
                )
                box = self.event(self.browser, 5).until(
                    self.condition.presence_of_element_located(command)
                )
                value = box.find_element(
                    self.rule.XPATH, 'input'
                ).get_attribute('value')
                if(value=='1,2'): continue
                box.click()
                continue
            _ = loop
            # Year
            command = (self.rule.XPATH, f'{head}/div[1]/div[12]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{year[0]}')
            # month
            command = (self.rule.XPATH, f'{head}/div[1]/div[13]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{month[0]}')
            #
            command = (self.rule.XPATH, f'{head}/div[1]/div[14]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{year[1]}')
            #
            command = (self.rule.XPATH, f'{head}/div[1]/div[15]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{month[1]}')
            #
            command = (self.rule.XPATH, '//*[text()="搜尋"]')
            element = self.event(self.browser, 5).until(
                self.condition.presence_of_all_elements_located(command)
            )
            button = element[2]
            button.click()
            pass
        if(department==4):
            symbol = f'//ul[@class="nav nav-pills"]/li[{department}]/a'
            command = (self.rule.XPATH, symbol)
            button = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            button.click()
            # print("【訊息】：選擇買賣查詢部門")
            head = '//form[@id="main_form"]'
            # City
            command = (self.rule.XPATH, f'{head}/div[1]/div[1]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            selection = self.selection(node)
            selection.select_by_value(city)
            # print(f"【訊息】：選擇{}縣市")
            # Area
            keep = True
            while(keep):
                command = (self.rule.XPATH, f'{head}/div[1]/div[2]/select')
                try:
                    node = self.event(self.browser, 5).until(
                        self.condition.presence_of_element_located(command)
                    )
                    selection = self.selection(node)
                    selection.select_by_value(area) # 太快會錯
                    pass
                except:
                    _ = node
                    _ = selection
                    continue
                keep = False
                continue
            # Year
            command = (self.rule.XPATH, f'{head}/div[1]/div[12]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{year[0]}')
            # month
            command = (self.rule.XPATH, f'{head}/div[1]/div[13]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{month[0]}')
            #
            command = (self.rule.XPATH, f'{head}/div[1]/div[14]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{year[1]}')
            #
            command = (self.rule.XPATH, f'{head}/div[1]/div[15]/select')
            node = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{month[1]}')
            #
            command = (self.rule.XPATH, '//*[text()="搜尋"]')
            element = self.event(self.browser, 5).until(
                self.condition.presence_of_all_elements_located(command)
            )
            button = element[1]
            button.click()
            pass
        keep = True
        while(keep):
            command = (self.rule.XPATH, '//*[text()="載入中..."]')
            try:
                element = self.event(self.browser, 5).until(
                    self.condition.presence_of_element_located(command)
                )
                pass
            except:
                keep = False
                break
            time.sleep(1)
            # print("載入中...", end='\r')
            continue
        # print("載入完成...")
        command = (
            self.rule.XPATH, 
            '//*[text()="查無資料，請確認查詢條件是否輸入正確內容。"]'
        )
        element = self.browser.find_elements(*command)
        if(element!=[]): return(False)
        return(True)

    def pullCatalog(self) -> bool:
        catalog = []
        keep = True
        while(keep):
            catalog += [self.browser.page_source]
            symbol = '//li[@id="price_table_next"]'
            command = (self.rule.XPATH, symbol)
            element = self.event(self.browser, 5).until(
                self.condition.presence_of_element_located(command)
            )
            if('disabled' not in element.get_attribute("class")): 
                element.click()
                continue
            keep = False
            continue
        self.catalog = catalog
        return(True)

    def collateCatalog(self, department: int) -> bool:
        if(department==1):
            group = []
            for content in tqdm.tqdm(self.catalog, leave=False):
                document = bs4.BeautifulSoup(content, "lxml")
                iteration = document.select("#table-item-tbody tr")
                chunk = []
                for row in iteration:
                    cell = row.find_all("td")
                    assert len(cell)==19
                    item = {
                        '地段位置或門牌': cell[0].get_text(strip=True),
                        '社區簡稱': cell[1].get_text(strip=True),
                        '總價（萬元）': cell[2].get_text(strip=True),
                        '交易日期': cell[3].get_text(strip=True),
                        '單價（每坪）': cell[4].get_text(strip=True),
                        '總面積': cell[5].get_text(strip=True),
                        '主建物佔比': cell[6].get_text(strip=True),
                        '建築型態': cell[7].get_text(strip=True),
                        '屋齡': cell[8].get_text(strip=True),
                        '樓別與樓高': cell[9].get_text(strip=True),
                        '主要用途': cell[10].get_text(strip=True),
                        '交易標的': cell[11].get_text(strip=True),
                        '建物格局': cell[12].get_text(strip=True),
                        '車位': cell[13].get_text(strip=True),
                        '管理組織': cell[14].get_text(strip=True),
                        '電梯': cell[15].get_text(strip=True),
                        '交易紀錄與歷次轉移': cell[16].get_text(strip=True),
                        '功能': cell[17].get_text(strip=True),
                        '備註': cell[18].get_text(strip=True)
                    }
                    chunk += [item]
                    continue
                group += chunk
                continue
            catalog = pandas.DataFrame.from_records(group)
            pass
        elif(department==2):
            group = []
            for content in tqdm.tqdm(self.catalog, leave=False):
                document = bs4.BeautifulSoup(content, "lxml")
                iteration = document.select("#table-item-tbody tr")
                chunk = []
                for row in iteration:
                    cell = row.find_all("td")
                    assert len(cell)==20
                    item = {
                        '地段位置或門牌': cell[0].get_text(strip=True),
                        '社區簡稱': cell[1].get_text(strip=True),
                        '總價（萬元）': cell[2].get_text(strip=True),
                        '訂約日期': cell[3].get_text(strip=True),
                        '單價（每坪）': cell[4].get_text(strip=True),
                        '總面積': cell[5].get_text(strip=True),
                        '建築型態': cell[6].get_text(strip=True),
                        '出租型態': cell[7].get_text(strip=True),
                        '屋齡': cell[8].get_text(strip=True),
                        '樓別與樓高': cell[9].get_text(strip=True),
                        '主要用途': cell[10].get_text(strip=True),
                        '租賃標的': cell[11].get_text(strip=True),
                        '車位租賃總價': cell[12].get_text(strip=True),
                        '管理組織': cell[13].get_text(strip=True),
                        '管理員': cell[14].get_text(strip=True),
                        '租賃期間': cell[15].get_text(strip=True),
                        '有無電梯': cell[16].get_text(strip=True),
                        '交易明細': cell[17].get_text(strip=True),
                        '功能': cell[18].get_text(strip=True),
                        '備註': cell[19].get_text(strip=True)
                    }
                    chunk += [item]
                    continue
                group += chunk
                continue
            catalog = pandas.DataFrame.from_records(group)
            pass
        elif(department==3):
            group = []
            for content in tqdm.tqdm(self.catalog, leave=False):
                document = bs4.BeautifulSoup(content, "lxml")
                iteration = document.select("#table-item-tbody tr")
                chunk = []
                for row in iteration:
                    cell = row.find_all("td")
                    assert len(cell)==19
                    item = {
                        '建物坐落': cell[0].get_text(strip=True),
                        '棟及號': cell[1].get_text(strip=True),
                        '建案名稱': cell[2].get_text(strip=True),
                        '總價(萬元)': cell[3].get_text(strip=True),
                        '交易日期': cell[4].get_text(strip=True),
                        '單價(坪)': cell[5].get_text(strip=True),
                        '總面積 (坪)': cell[6].get_text(strip=True),
                        '主建物佔比': cell[7].get_text(strip=True),
                        '型態': cell[8].get_text(strip=True),
                        '樓別與樓高': cell[9].get_text(strip=True),
                        '交易標的': cell[10].get_text(strip=True),
                        '建物格局': cell[11].get_text(strip=True),
                        '車位總價(萬元)': cell[12].get_text(strip=True),
                        '主要用途': cell[13].get_text(strip=True),
                        '主要建材': cell[14].get_text(strip=True),
                        '解約情形': cell[15].get_text(strip=True),
                        '交易明細': cell[16].get_text(strip=True),
                        '功能': cell[17].get_text(strip=True),
                        '備註': cell[18].get_text(strip=True),
                    }
                    chunk += [item]
                    continue
                group += chunk
                continue
            catalog = pandas.DataFrame.from_records(group)
            pass
        elif(department==4):
            group = []
            for content in tqdm.tqdm(self.catalog, leave=False):
                document = bs4.BeautifulSoup(content, "lxml")
                iteration = document.select("#table-item-tbody tr")
                chunk = []
                for row in iteration:
                    cell = row.find_all("td")
                    assert len(cell)==17
                    item = {
                        '建案名稱': cell[0].get_text(strip=True),
                        '坐落街道': cell[1].get_text(strip=True),
                        '起造人': cell[2].get_text(strip=True),
                        '層棟戶數': cell[3].get_text(strip=True),
                        '使用分區': cell[4].get_text(strip=True),
                        '主要用途': cell[5].get_text(strip=True),
                        '主要建材': cell[6].get_text(strip=True),
                        '申報備查期間': cell[7].get_text(strip=True),
                        '自銷售期間': cell[8].get_text(strip=True),
                        '代銷售期間': cell[9].get_text(strip=True),
                        '坐落基地': cell[10].get_text(strip=True),
                        '建照核發日期': cell[11].get_text(strip=True),
                        '建造執照': cell[12].get_text(strip=True),
                        '完成建物第一次登記日期': cell[13].get_text(strip=True),
                        '詳細內容': cell[14].get_text(strip=True),
                        '功能': cell[15].get_text(strip=True),
                        '備註': cell[16].get_text(strip=True),
                    }
                    chunk += [item]
                    continue
                group += chunk
                continue
            catalog = pandas.DataFrame.from_records(group)
            pass
        self.catalog = catalog
        return(True)

    def saveCatalog(self, path: str) -> bool:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.catalog.to_csv(path, index=False)
        return(True)

    def launchJob(
        self,
        department: int, 
        city: str, 
        area: str, 
        year: tuple, 
        month: tuple,
        folder: str
    ) -> bool:
        self.openBrowser()
        self.visitHome()
        existence = self.searchHistory(department, city, area, year, month)
        if(not existence): 
            self.quitBrowser()
            return(True)
        self.pullCatalog()
        self.collateCatalog(department)
        self.quitBrowser()
        archive = f"{year[0]}{month[0]}-{year[1]}{month[1]}.csv"
        path = os.path.join(
            folder,
            str(department), 
            city, 
            area, 
            archive
        )
        self.saveCatalog(path)
        return(True)

    def quitBrowser(self) -> bool:
        self.browser.quit()
        return(True)

    def getDomain(self) -> dict:
        with open(self.domain, 'r') as paper:
            content = json.load(paper)
            pass
        domain = content
        return(domain)

    def saveScreen(self, path: str) -> bool:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.browser.save_screenshot(path)
        return(True)

    home = 'https://lvr.land.moi.gov.tw/'
    rule = selenium.webdriver.common.by.By
    event = selenium.webdriver.support.ui.WebDriverWait
    condition = selenium.webdriver.support.expected_conditions
    selection = selenium.webdriver.support.ui.Select
    pass

agent = Agent(display=False, domain='./domain.json')
domain = agent.getDomain()
department = 1
year = (101, 113)#(101, 113)
month = (1, 12)#(1, 12)
folder = 'checkpoint'
for city in domain['city']:
    if(city not in ['P']): continue 
    #     print(city, 'skip')
    #     continue
    print(city)
    for area in domain['area'][city]:
        if(area in ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10', 'P11', 'P12', 'P13']): continue
        agent.launchJob(department, city, area, year, month, folder)
        print(area)
        continue
    continue
