import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep


class MyTestCase(unittest.TestCase):

    dr = None

    @classmethod
    def setUpClass(cls):
        # enable headless mode
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        cls.dr = webdriver.Chrome(options=chrome_options)
        cls.dr.implicitly_wait(5)

        # define article id and user id
        cls.article = '207de43187032100deddb882a2e3ec7a'
        cls.user = '1d6097281b39101064244375cc4bcbf8'
        cls.article_url = \
            'https://dev67438.service-now.com/sp?id=kb_article_view_new&sys_id='
        cls.table_url = \
            'https://dev67438.service-now.com/nav_to.do?uri=%2Fx_512628_webwidget_favourite_records_list.do'

        # login to the instance
        cls.dr.get(cls.article_url + cls.article)
        cls.dr.find_element_by_id('username').send_keys('wentao.yang')
        cls.dr.find_element_by_id('password').send_keys('shoh_FLIR8raum@aul')
        cls.dr.find_element_by_name('login').click()
        sleep(1)

    def visit_table(self):
        if self.dr.current_url != self.table_url:
            sleep(1)
            self.dr.get(self.table_url)
            sleep(1)
            self.dr.switch_to.frame("gsft_main")

    # test the feature of marking an article as favourite
    def test_1_add_fav(self):
        self.dr.find_element_by_id('favourite').click()
        self.visit_table()
        # if not found, throws exceptions
        self.dr.find_element_by_xpath("//tr[td/a/text()='{}' and td/text()='{}']".format(self.article, self.user))

    # test the feature of removing an favourite article
    def test_2_remove_fav(self):
        self.dr.find_element_by_id('unfavourite').click()
        self.visit_table()

        raised = False
        try:
            self.dr.find_element_by_xpath("//tr[td/a/text()='{}' and td/text()='{}']".format(self.article, self.user))
        except NoSuchElementException:
            raised = True
        self.assertTrue(raised, "the record still exists")

    @classmethod
    def tearDownClass(cls):
        cls.dr.quit()


if __name__ == '__main__':
    unittest.main()
