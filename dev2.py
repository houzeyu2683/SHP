import time
import bs4
import os
import pandas
import tqdm
import json
import playwright.sync_api

class Agent:

    def __init__(
        self,
        display: bool,
        domain: str,
    ) -> None:
        self.display = display
        self.domain = domain
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        return

    def openBrowser(self) -> bool:
        self.playwright = playwright.sync_api.sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=not self.display,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-notifications"
            ]
        )
        self.context = self.browser.new_context(
            user_agent="Chromium",
            no_viewport=True,
            locale="zh-TW"
        )
        self.page = self.context.new_page()
        return True

    def visitHome(self) -> bool:
        self.page.goto(self.home)
        return True

    def searchHistory(
        self,
        department: int,
        city: str,
        area: str,
        year: tuple,
        month: tuple
    ) -> bool:
        frame = self.page.frame(url='https://lvr.land.moi.gov.tw/jsp/index.jsp')
        if not frame:
            frame = self.page.wait_for_selector('//frame').content_frame()

        if department == 1:
            symbol = f'//ul[@class="nav nav-pills"]/li[{department}]/a'
            button = frame.wait_for_selector(symbol)
            button.click()

            head = '//form[@id="main_form"]'
            # City
            city_selector = f'{head}/div[1]/div[1]/select'
            frame.select_option(city_selector, value=city)

            # Area
            keep = True
            while keep:
                area_selector = f'{head}/div[1]/div[2]/select'
                try:
                    frame.wait_for_selector(area_selector, timeout=5000)
                    frame.select_option(area_selector, value=area)
                    break
                except:
                    continue

            loop = [(3, 1), (3, 2), (4, 1), (4, 2)]
            for row, column in loop:
                box_selector = f'{head}/div[1]/div[{row}]/div[{column}]'
                box = frame.wait_for_selector(box_selector)
                input_element = box.query_selector('input')
                if input_element:
                    value = input_element.get_attribute('value')
                    if value == '1,2':
                        continue
                box.click()

            # Year start
            year_selector = f'{head}/div[1]/div[12]/select'
            frame.select_option(year_selector, value=f'{year[0]}')

            # Month start
            month_selector = f'{head}/div[1]/div[13]/select'
            frame.select_option(month_selector, value=f'{month[0]}')

            # Year end
            year_end_selector = f'{head}/div[1]/div[14]/select'
            frame.select_option(year_end_selector, value=f'{year[1]}')

            # Month end
            month_end_selector = f'{head}/div[1]/div[15]/select'
            frame.select_option(month_end_selector, value=f'{month[1]}')

            # Search button
            search_buttons = frame.query_selector_all('//*[text()="搜尋"]')
            if len(search_buttons) > 2:
                search_buttons[2].click()

        elif department == 2:
            symbol = f'//ul[@class="nav nav-pills"]/li[{department}]/a'
            button = frame.wait_for_selector(symbol)
            button.click()

            head = '//form[@id="main_form"]'
            # City
            city_selector = f'{head}/div[1]/div[1]/select'
            frame.select_option(city_selector, value=city)

            # Area
            keep = True
            while keep:
                area_selector = f'{head}/div[1]/div[2]/select'
                try:
                    frame.wait_for_selector(area_selector, timeout=5000)
                    frame.select_option(area_selector, value=area)
                    break
                except:
                    continue

            # Year start
            year_selector = f'{head}/div[1]/div[12]/select'
            frame.select_option(year_selector, value=f'{year[0]}')

            # Month start
            month_selector = f'{head}/div[1]/div[13]/select'
            frame.select_option(month_selector, value=f'{month[0]}')

            # Year end
            year_end_selector = f'{head}/div[1]/div[14]/select'
            frame.select_option(year_end_selector, value=f'{year[1]}')

            # Month end
            month_end_selector = f'{head}/div[1]/div[15]/select'
            frame.select_option(month_end_selector, value=f'{month[1]}')

            # Search button
            search_buttons = frame.query_selector_all('//*[text()="搜尋"]')
            if len(search_buttons) > 2:
                search_buttons[2].click()

        elif department == 3:
            symbol = f'//ul[@class="nav nav-pills"]/li[{department}]/a'
            button = frame.wait_for_selector(symbol)
            button.click()

            head = '//form[@id="main_form"]'
            # City
            city_selector = f'{head}/div[1]/div[1]/select'
            frame.select_option(city_selector, value=city)

            # Area
            keep = True
            while keep:
                area_selector = f'{head}/div[1]/div[2]/select'
                try:
                    frame.wait_for_selector(area_selector, timeout=5000)
                    frame.select_option(area_selector, value=area)
                    break
                except:
                    continue

            loop = [(3, 1), (4, 1), (4, 2)]
            for row, column in loop:
                box_selector = f'{head}/div[1]/div[{row}]/div[{column}]'
                box = frame.wait_for_selector(box_selector)
                input_element = box.query_selector('input')
                if input_element:
                    value = input_element.get_attribute('value')
                    if value == '1,2':
                        continue
                box.click()

            # Year start
            year_selector = f'{head}/div[1]/div[12]/select'
            frame.select_option(year_selector, value=f'{year[0]}')

            # Month start
            month_selector = f'{head}/div[1]/div[13]/select'
            frame.select_option(month_selector, value=f'{month[0]}')

            # Year end
            year_end_selector = f'{head}/div[1]/div[14]/select'
            frame.select_option(year_end_selector, value=f'{year[1]}')

            # Month end
            month_end_selector = f'{head}/div[1]/div[15]/select'
            frame.select_option(month_end_selector, value=f'{month[1]}')

            # Search button
            search_buttons = frame.query_selector_all('//*[text()="搜尋"]')
            if len(search_buttons) > 2:
                search_buttons[2].click()

        elif department == 4:
            symbol = f'//ul[@class="nav nav-pills"]/li[{department}]/a'
            button = frame.wait_for_selector(symbol)
            button.click()

            head = '//form[@id="main_form"]'
            # City
            city_selector = f'{head}/div[1]/div[1]/select'
            frame.select_option(city_selector, value=city)

            # Area
            keep = True
            while keep:
                area_selector = f'{head}/div[1]/div[2]/select'
                try:
                    frame.wait_for_selector(area_selector, timeout=5000)
                    frame.select_option(area_selector, value=area)
                    break
                except:
                    continue

            # Year start
            year_selector = f'{head}/div[1]/div[12]/select'
            frame.select_option(year_selector, value=f'{year[0]}')

            # Month start
            month_selector = f'{head}/div[1]/div[13]/select'
            frame.select_option(month_selector, value=f'{month[0]}')

            # Year end
            year_end_selector = f'{head}/div[1]/div[14]/select'
            frame.select_option(year_end_selector, value=f'{year[1]}')

            # Month end
            month_end_selector = f'{head}/div[1]/div[15]/select'
            frame.select_option(month_end_selector, value=f'{month[1]}')

            # Search button
            search_buttons = frame.query_selector_all('//*[text()="搜尋"]')
            if len(search_buttons) > 1:
                search_buttons[1].click()

        # Wait for loading to complete
        keep = True
        while keep:
            try:
                frame.wait_for_selector('//*[text()="載入中..."]', timeout=5000)
                time.sleep(1)
            except:
                keep = False
                break

        # Check if no data found
        no_data_elements = frame.query_selector_all('//*[text()="查無資料，請確認查詢條件是否輸入正確內容。"]')
        if no_data_elements:
            return False
        return True

    def pullCatalog(self) -> bool:
        catalog = []
        frame = self.page.frame(url='https://lvr.land.moi.gov.tw/jsp/index.jsp')
        if not frame:
            frame = self.page.frames[1] if len(self.page.frames) > 1 else self.page

        keep = True
        while keep:
            catalog.append(frame.content())
            next_button_selector = '//li[@id="price_table_next"]'
            try:
                next_button = frame.wait_for_selector(next_button_selector, timeout=5000)
                class_attr = next_button.get_attribute("class")
                if 'disabled' not in (class_attr or ''):
                    next_button.click()
                    time.sleep(1)  # Wait for page to load
                else:
                    keep = False
            except:
                keep = False

        self.catalog = catalog
        return True

    def collateCatalog(self, department: int) -> bool:
        if department == 1:
            group = []
            for content in tqdm.tqdm(self.catalog, leave=False):
                document = bs4.BeautifulSoup(content, "lxml")
                iteration = document.select("#table-item-tbody tr")
                chunk = []
                for row in iteration:
                    cell = row.find_all("td")
                    assert len(cell) == 19
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
                    chunk.append(item)
                group.extend(chunk)
            catalog = pandas.DataFrame.from_records(group)

        elif department == 2:
            group = []
            for content in tqdm.tqdm(self.catalog, leave=False):
                document = bs4.BeautifulSoup(content, "lxml")
                iteration = document.select("#table-item-tbody tr")
                chunk = []
                for row in iteration:
                    cell = row.find_all("td")
                    assert len(cell) == 20
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
                    chunk.append(item)
                group.extend(chunk)
            catalog = pandas.DataFrame.from_records(group)

        elif department == 3:
            group = []
            for content in tqdm.tqdm(self.catalog, leave=False):
                document = bs4.BeautifulSoup(content, "lxml")
                iteration = document.select("#table-item-tbody tr")
                chunk = []
                for row in iteration:
                    cell = row.find_all("td")
                    assert len(cell) == 19
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
                    chunk.append(item)
                group.extend(chunk)
            catalog = pandas.DataFrame.from_records(group)

        elif department == 4:
            group = []
            for content in tqdm.tqdm(self.catalog, leave=False):
                document = bs4.BeautifulSoup(content, "lxml")
                iteration = document.select("#table-item-tbody tr")
                chunk = []
                for row in iteration:
                    cell = row.find_all("td")
                    assert len(cell) == 17
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
                    chunk.append(item)
                group.extend(chunk)
            catalog = pandas.DataFrame.from_records(group)

        self.catalog = catalog
        return True

    def saveCatalog(self, path: str) -> bool:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.catalog.to_csv(path, index=False)
        return True

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
        if not existence:
            self.quitBrowser()
            return True
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
        return True

    def quitBrowser(self) -> bool:
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        return True

    def getDomain(self) -> dict:
        with open(self.domain, 'r') as paper:
            content = json.load(paper)
        domain = content
        return domain

    def saveScreen(self, path: str) -> bool:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.page.screenshot(path=path)
        return True

    home = 'https://lvr.land.moi.gov.tw/'

if __name__ == "__main__":
    agent = Agent(display=False, domain='./domain.json')
    domain = agent.getDomain()
    print("Domain loaded successfully!")
    print(f"Available cities: {list(domain['city'].keys())}")
    print(f"Areas for city P: {list(domain['area']['P'].keys())}")

    # Test mode - uncomment below to run full scraping
    department = 1
    year = (101, 113)  # (101, 113)
    month = (1, 12)  # (1, 12)
    folder = 'checkpoint'
    for city in domain['city'].keys():
        if city not in ['P']:
            continue
        print(city)
        for area in domain['area'][city].keys():
            if area in ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10', 'P11', 'P12', 'P13']:
                continue
            agent.launchJob(department, city, area, year, month, folder)
            print(area)