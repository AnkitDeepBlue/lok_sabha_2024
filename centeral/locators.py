from selenium.webdriver.common.by import By

STATE_DROPDOWN_ID = (By.ID, "ctl00_ContentPlaceHolder1_Result1_ddlState")
CONSTITUENCY_DROPDOWN_ID = (By.ID, "ctl00_ContentPlaceHolder1_Result1_ddlState")
winner_candidate = (By.XPATH, "(//*[@class='col-md-4 col-12'])[1]//div")
looser_candidate = (By.XPATH, "(//*[@class='col-md-4 col-12'])[2]//div")

complete_stats= (By.XPATH, "//*[@class='parent-wrap cardTble']")