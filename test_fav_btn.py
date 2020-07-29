import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep


# This is to test the "Favourite" and "Unfavourite" buttons
class FavBtnTests(unittest.TestCase):

    dr = None

    # start driver and login to the instance
    @classmethod
    def setUpClass(cls):
        # use chrome to test
        chrome_options = webdriver.ChromeOptions()
        # enable headless mode
        chrome_options.add_argument('--headless')
        # set options
        cls.dr = webdriver.Chrome(options=chrome_options)
        # set the implicit wait time
        cls.dr.implicitly_wait(5)

        # define article id and user id
        cls.article = '207de43187032100deddb882a2e3ec7a'
        cls.user = '1d6097281b39101064244375cc4bcbf8'

        # page links
        cls.article_prefix = \
            'https://dev67438.service-now.com/sp?id=kb_article_view_new&sys_id='
        cls.table_url = \
            'https://dev67438.service-now.com/nav_to.do?uri=%2Fx_512628_webwidget_favourite_records_list.do'
        cls.article_url = cls.article_prefix + cls.article

        # login to the instance
        cls.dr.get(cls.article_url)
        cls.dr.find_element_by_id('username').send_keys('wentao.yang')
        cls.dr.find_element_by_id('password').send_keys('shoh_FLIR8raum@aul')
        cls.dr.find_element_by_name('login').click()

        print("login successfully")

    # visit the article page
    def visit_article(self):
        if self.dr.current_url != self.article_url:
            sleep(1)
            self.dr.get(self.article_url)

    # visit the favourite record table
    def visit_table(self):
        if self.dr.current_url != self.table_url:
            sleep(1)
            self.dr.get(self.table_url)
            sleep(1)
            self.dr.switch_to.frame("gsft_main")

    # test marking an article as favourite
    def test_1_add_fav(self):
        print('start testing adding favourites')

        # click the favourite button
        self.visit_article()
        self.dr.find_element_by_id('favourite').click()

        # visit table to check records
        # if not found, it will throw an exception
        self.visit_table()
        self.dr.find_element_by_xpath("//tr[td/a/text()='{}' and td/text()='{}']".format(self.article, self.user))

        print('test passed')

    # test removing an favourite article
    def test_2_remove_fav(self):
        print('start testing removing favourites')

        # click the unfavourite button
        self.visit_article()
        self.dr.find_element_by_id('unfavourite').click()

        # visit table to check records
        # not found will throw exception, which is expected
        self.visit_table()
        raised = False
        try:
            self.dr.find_element_by_xpath("//tr[td/a/text()='{}' and td/text()='{}']".format(self.article, self.user))
        except NoSuchElementException:
            raised = True
        self.assertTrue(raised, "the record still exists")

        print('test passed')

    # quit driver
    @classmethod
    def tearDownClass(cls):
        cls.dr.quit()
        print('finish')


if __name__ == '__main__':
    unittest.main()
