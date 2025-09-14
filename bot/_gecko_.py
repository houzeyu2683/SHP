import core
import json
import tqdm
import bs4
import pandas
import os

class Gecko(core.Browser):

    def __init__(self, display: bool) -> None:
        self.display = display
        return

    def readScope(self, path: str) -> bool:
        with open(path, 'r') as paper:
            content = json.load(paper)
            pass
        self.scope = content
        return(True)

    def selectDepartment(
        self, 
        tunnel: str, 
    ) -> bool:
        # Switch Frame
        command = (self.rule.XPATH, '//frame')
        element = self.client.find_element(*command)
        self.client.switch_to.frame(element)
        # Select Department
        symbol = f'//ul[@class="nav nav-pills"]/li[{tunnel}]/a'
        command = (self.rule.XPATH, symbol)
        button = self.event(self.client, 5).until(
            self.condition.presence_of_element_located(command)
        )
        button.click()
        if(tunnel=="1"):
            head = '//form[@id="main_form"]'
            loop = [(3, 1), (3, 2), (4, 1), (4, 2)]
            for row, column in loop:
                command = (
                    self.rule.XPATH, 
                    f'{head}/div[1]/div[{row}]/div[{column}]'
                )
                box = self.event(self.client, 5).until(
                    self.condition.presence_of_element_located(command)
                )
                value = box.find_element(
                    self.rule.XPATH, 'input'
                ).get_attribute('value')
                if(value=='1,2'): continue
                box.click()
                continue
            _ = loop
            self.department = self.scope['department'][tunnel]
            return(True)
        if(tunnel=="3"):
            head = '//form[@id="main_form"]'
            loop = [(3, 1), (4, 1), (4, 2)]
            for row, column in loop:
                command = (
                    self.rule.XPATH, 
                    f'{head}/div[1]/div[{row}]/div[{column}]'
                )
                box = self.event(self.client, 5).until(
                    self.condition.presence_of_element_located(command)
                )
                value = box.find_element(
                    self.rule.XPATH, 'input'
                ).get_attribute('value')
                if(value=='1,2'): continue
                box.click()
                continue
            _ = loop
            self.department = self.scope['department'][tunnel]
            return(True)
        self.department = self.scope['department'][tunnel]
        return(True)

    def selectLocation(self, city: str, area: str) -> bool:
        # Select City
        head = '//form[@id="main_form"]'
        command = (self.rule.XPATH, f'{head}/div[1]/div[1]/select')
        node = self.event(self.client, 5).until(
            self.condition.presence_of_element_located(command)
        )
        selection = self.selection(node)
        selection.select_by_value(city)
        # Select Area
        keep = True
        while(keep):
            command = (self.rule.XPATH, f'{head}/div[1]/div[2]/select')
            try:
                node = self.event(self.client, 5).until(
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
        _ = keep
        self.location = (
            self.scope['city'][city], 
            self.scope['area'][city][area]
        )
        return(True)

    def selectDate(
        self, 
        interval: tuple
    ) -> bool:
        head = '//form[@id="main_form"]'
        year, month = interval[0]
        if(True):
            # Year
            command = (self.rule.XPATH, f'{head}/div[1]/div[12]/select')
            node = self.event(self.client, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{year}')
            # month
            command = (self.rule.XPATH, f'{head}/div[1]/div[13]/select')
            node = self.event(self.client, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{month}')
            pass
        year, month = interval[1]
        if(True):
            # Year
            command = (self.rule.XPATH, f'{head}/div[1]/div[14]/select')
            node = self.event(self.client, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{year}')
            # Month
            command = (self.rule.XPATH, f'{head}/div[1]/div[15]/select')
            node = self.event(self.client, 5).until(
                self.condition.presence_of_element_located(command)
            )
            self.selection(node).select_by_value(f'{month}')
            pass
        self.date = interval[1]
        return(True)
    
    def startRetrieval(self) -> bool:
        command = (self.rule.XPATH, '//*[text()="搜尋"]')
        element = self.event(self.client, 5).until(
            self.condition.presence_of_all_elements_located(command)
        )
        button = element[1] if(self.department=='建案查詢') else element[2]
        button.click()
        keep = True
        while(keep):
            command = (self.rule.XPATH, '//*[text()="載入中..."]')
            try:
                element = self.event(self.client, 5).until(
                    self.condition.presence_of_element_located(command)
                )
                pass
            except:
                keep = False
                break
            keep = True
            continue
        _ = keep
        command = (
            self.rule.XPATH, 
            '//*[text()="查無資料，請確認查詢條件是否輸入正確內容。"]'
        )
        element = self.client.find_elements(*command)
        if(element!=[]):
            self.retrieval = 0
            return(True)
        self.retrieval = 1
        return(True)

    def pullPagination(self) -> bool:
        pagination = []
        keep = True
        while(keep):
            pagination += [self.client.page_source]
            symbol = '//li[@id="price_table_next"]'
            command = (self.rule.XPATH, symbol)
            element = self.event(self.client, 5).until(
                self.condition.presence_of_element_located(command)
            )
            if('disabled' not in element.get_attribute("class")): 
                element.click()
                continue
            keep = False
            continue
        _ = keep
        self.pagination = pagination
        return(True)

    def collateInformation(self) -> bool:
        if(self.department=="property_sales"):
            group = []
            for content in tqdm.tqdm(self.information, leave=False):
                document = bs4.BeautifulSoup(content, "lxml")
                iteration = document.select("#table-item-tbody tr")
                chunk = []
                for row in iteration:
                    cell = row.find_all("td")
                    assert len(cell)==19
                    item = {
                        'location_or_address': cell[0].get_text(strip=True),
                        'community_short_name': cell[1].get_text(strip=True),
                        'total_price_10k': cell[2].get_text(strip=True),
                        'transaction_date': cell[3].get_text(strip=True),
                        'unit_price_per_ping': cell[4].get_text(strip=True),
                        'total_area': cell[5].get_text(strip=True),
                        'main_building_ratio': cell[6].get_text(strip=True),
                        'building_type': cell[7].get_text(strip=True),
                        'building_age': cell[8].get_text(strip=True),
                        'floor_and_total_floors': cell[9].get_text(strip=True),
                        'primary_use': cell[10].get_text(strip=True),
                        'transaction_target': cell[11].get_text(strip=True),
                        'layout': cell[12].get_text(strip=True),
                        'parking': cell[13].get_text(strip=True),
                        'management_organization': cell[14].get_text(strip=True),
                        'elevator': cell[15].get_text(strip=True),
                        'transaction_history': cell[16].get_text(strip=True),
                        'function': cell[17].get_text(strip=True),
                        'remarks': cell[18].get_text(strip=True)
                    }
                    chunk += [item]
                    continue
                group += chunk
                continue
            information = pandas.DataFrame.from_records(group)
            pass
        elif(self.department=="property_rentals"):
            group = []
            for content in tqdm.tqdm(self.information, leave=False):
                document = bs4.BeautifulSoup(content, "lxml")
                iteration = document.select("#table-item-tbody tr")
                chunk = []
                for row in iteration:
                    cell = row.find_all("td")
                    assert len(cell)==20
                    item = {
                        'location_or_address': cell[0].get_text(strip=True),
                        'community_short_name': cell[1].get_text(strip=True),
                        'total_price_10k': cell[2].get_text(strip=True),
                        'contract_date': cell[3].get_text(strip=True),
                        'unit_price_per_ping': cell[4].get_text(strip=True),
                        'total_area': cell[5].get_text(strip=True),
                        'building_type': cell[6].get_text(strip=True),
                        'rental_type': cell[7].get_text(strip=True),
                        'building_age': cell[8].get_text(strip=True),
                        'floor_and_total_floors': cell[9].get_text(strip=True),
                        'primary_use': cell[10].get_text(strip=True),
                        'rental_target': cell[11].get_text(strip=True),
                        'parking_rental_total': cell[12].get_text(strip=True),
                        'management_organization': cell[13].get_text(strip=True),
                        'manager': cell[14].get_text(strip=True),
                        'rental_period': cell[15].get_text(strip=True),
                        'elevator': cell[16].get_text(strip=True),
                        'transaction_details': cell[17].get_text(strip=True),
                        'function': cell[18].get_text(strip=True),
                        'remarks': cell[19].get_text(strip=True)
                    }
                    chunk += [item]
                    continue
                group += chunk
                continue
            information = pandas.DataFrame.from_records(group)
            pass
        elif(self.department=='pre_sale_listings'):
            group = []
            for content in tqdm.tqdm(self.information, leave=False):
                document = bs4.BeautifulSoup(content, "lxml")
                iteration = document.select("#table-item-tbody tr")
                chunk = []
                for row in iteration:
                    cell = row.find_all("td")
                    assert len(cell)==19
                    item = {
                        'building_address': cell[0].get_text(strip=True),          # 建物坐落
                        'building_number': cell[1].get_text(strip=True),           # 棟及號
                        'project_name': cell[2].get_text(strip=True),              # 建案名稱
                        'total_price_10k': cell[3].get_text(strip=True),           # 總價(萬元)
                        'transaction_date': cell[4].get_text(strip=True),          # 交易日期
                        'unit_price_per_ping': cell[5].get_text(strip=True),       # 單價(坪)
                        'total_area_ping': cell[6].get_text(strip=True),           # 總面積 (坪)
                        'main_building_ratio': cell[7].get_text(strip=True),       # 主建物佔比
                        'building_type': cell[8].get_text(strip=True),             # 型態
                        'floor_and_total_floors': cell[9].get_text(strip=True),    # 樓別與樓高
                        'transaction_target': cell[10].get_text(strip=True),       # 交易標的
                        'layout': cell[11].get_text(strip=True),                   # 建物格局
                        'parking_total_10k': cell[12].get_text(strip=True),        # 車位總價(萬元)
                        'primary_use': cell[13].get_text(strip=True),              # 主要用途
                        'main_material': cell[14].get_text(strip=True),            # 主要建材
                        'contract_termination': cell[15].get_text(strip=True),     # 解約情形
                        'transaction_details': cell[16].get_text(strip=True),      # 交易明細
                        'function': cell[17].get_text(strip=True),                 # 功能
                        'remarks': cell[18].get_text(strip=True),                  # 備註
                    }
                    chunk += [item]
                    continue
                group += chunk
                continue
            information = pandas.DataFrame.from_records(group)
            pass
        elif(self.department=='construction_projects'):
            group = []
            for content in tqdm.tqdm(self.information, leave=False):
                document = bs4.BeautifulSoup(content, "lxml")
                iteration = document.select("#table-item-tbody tr")
                chunk = []
                for row in iteration:
                    cell = row.find_all("td")
                    assert len(cell)==17
                    item = {
                        'project_name': cell[0].get_text(strip=True),                     # 建案名稱
                        'street_address': cell[1].get_text(strip=True),                   # 坐落街道
                        'builder': cell[2].get_text(strip=True),                          # 起造人
                        'floors_units': cell[3].get_text(strip=True),                     # 層棟戶數
                        'zoning': cell[4].get_text(strip=True),                            # 使用分區
                        'primary_use': cell[5].get_text(strip=True),                       # 主要用途
                        'main_material': cell[6].get_text(strip=True),                     # 主要建材
                        'registration_period': cell[7].get_text(strip=True),               # 申報備查期間
                        'self_sales_period': cell[8].get_text(strip=True),                 # 自銷售期間
                        'agency_sales_period': cell[9].get_text(strip=True),               # 代銷售期間
                        'site_location': cell[10].get_text(strip=True),                    # 坐落基地
                        'building_permit_issue_date': cell[11].get_text(strip=True),       # 建照核發日期
                        'building_permit_number': cell[12].get_text(strip=True),           # 建造執照
                        'first_registration_date': cell[13].get_text(strip=True),          # 完成建物第一次登記日期
                        'details': cell[14].get_text(strip=True),                           # 詳細內容
                        'function': cell[15].get_text(strip=True),                          # 功能
                        'remarks': cell[16].get_text(strip=True),                           # 備註
                    }
                    chunk += [item]
                    continue
                group += chunk
                continue
            information = pandas.DataFrame.from_records(group)
            pass
        self.information = information
        return(True)

    def saveInformation(self, path: str) -> bool:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.information.to_csv(path, index=False)
        return(True)

    pass

