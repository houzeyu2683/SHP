import playwright.sync_api

with playwright.sync_api.sync_playwright() as connection:
    client = connection.chromium.launch(headless=False)
    context = client.new_context(
        user_agent="Mozilla/5.0",
        no_viewport=True,
        locale="zh-TW",
        # geolocation={"latitude": 25.0478, "longitude": 121.5319},
        # permissions=["geolocation"]
    )
    page = context.new_page()
    page.goto("https://lvr.land.moi.gov.tw/")
    frame = page.frame(url='https://lvr.land.moi.gov.tw/jsp/index.jsp')
    index = 1
    button = frame.wait_for_selector(
        f'xpath=//*[@id="pills-tab"]/li[{index}]'
    )
    button.click()
    if(index==1):
        city = 'C'
        area = 'C02'
        frame.select_option('xpath=//*[@id="p_city"]', value=city)
        frame.select_option('xpath=//*[@id="p_town"]', value=area)
        if(True):
            section = '//*[@id="main_form"]/div[1]/div[3]'
            box = frame.locator(f'{section}/div[1]/label')
            if(box.is_checked()==False): box.click()
            box = frame.locator(f'{section}/div[2]/label')
            if(box.is_checked()==False): box.click()
            pass
        if(True):
            section = '//*[@id="main_form"]/div[1]/div[4]'
            box = frame.locator(f'{section}/div[1]/label')
            if(box.is_checked()==False): box.click()
            box = frame.locator(f'{section}/div[2]/label')
            if(box.is_checked()==False): box.click()
            pass
        year = '101' # 114
        frame.select_option('xpath=//*[@id="p_startY"]', value=year)
        month = '1' # 12
        frame.select_option('xpath=//*[@id="p_startM"]', value=month)
        year = '112' # 114
        frame.select_option('xpath=//*[@id="p_endY"]', value=year)
        month = '2' # 12
        frame.select_option('xpath=//*[@id="p_endM"]', value=month)
        
        block = "form-group mt-0 form-check-inline qry_general"
        element = frame.locator(f'//div[@class="{block}"]')
        button = element.locator('div, font').first

        button.click()
        print('next')
        pass

    client.close()
    pass



