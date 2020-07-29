import unittest
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class MyTestCase(unittest.TestCase):

    dr = None

    @classmethod
    def setUpClass(cls):
        # enable headless mode
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        cls.dr = webdriver.Chrome(options=chrome_options)
        cls.dr.implicitly_wait(5)

        # define article id and user id
        cls.a = ['435186b5474321009db4b5b08b9a7160']
        cls.articles = ['c85cd2519f77230088aebde8132e70c2',
                        'dcf43d75474321009db4b5b08b9a71dc',
                        '3b0fccee0a0a0b9b00d34b36ea41a43e']
        cls.user = '1d6097281b39101064244375cc4bcbf8'
        cls.article_url = \
            'https://dev67438.service-now.com/sp?id=kb_article_view_new&sys_id='
        cls.fav_list_url = \
            'https://dev67438.service-now.com/sp?id=most_favourite_articles_test_page'
        cls.table_url = \
            'https://dev67438.service-now.com/nav_to.do?uri=%2Fx_512628_webwidget_favourite_records_list.do'

        # login to the instance
        cls.dr.get(cls.fav_list_url)
        cls.dr.find_element_by_id('username').send_keys('wentao.yang')
        cls.dr.find_element_by_id('password').send_keys('shoh_FLIR8raum@aul')
        cls.dr.find_element_by_name('login').click()

    def setUp(self):
        self.visit_fav_table()
        self.add_fav_record(self.articles, '111')
        self.add_fav_record(self.articles[0:2], '222')
        self.add_fav_record(self.articles[0:1], '333')

    def visit_fav_table(self):
        if self.dr.current_url != self.table_url:
            sleep(1)
            self.dr.get(self.table_url)
            sleep(1)
            self.dr.switch_to.frame("gsft_main")

    def add_fav_record(self, articles, user):
        for article in articles:
            self.dr.find_element_by_id('sysverb_new').click()
            self.dr.find_element_by_id('x_512628_webwidget_favourite_records.user_id').send_keys(user)
            self.dr.find_element_by_id('x_512628_webwidget_favourite_records.article_id').send_keys(article)
            self.dr.find_element_by_id('sysverb_insert_bottom').click()

    def visit_and_add_fav_record(self, articles, user):
        self.visit_fav_table()
        self.add_fav_record(articles, user)

    def del_fav_record(self, articles, user):
        for article in articles:
            self.dr.find_element_by_xpath("//a[text()='{}' and ../following-sibling::td[1]/text()='{}']".format(article, user)).click()
            self.dr.find_element_by_id('sysverb_delete_bottom').click()
            self.dr.find_element_by_id('ok_button').click()

    def visit_and_del_fav_record(self, articles, user):
        self.visit_fav_table()
        self.del_fav_record(articles, user)

    def visit_fav_list(self):
        if self.dr.current_url != self.fav_list_url:
            sleep(1)
            self.dr.get(self.fav_list_url)

    def check_list(self, articles):
        self.visit_fav_list()

        def build_list_string(articles):
            if len(articles) <= 0:
                return ""

            s = "//li[a[contains(@href, '{}')]".format(articles[0])
            if len(articles) > 1:
                for i in range(1, len(articles)):
                    s += " and following-sibling::li[{}][a[contains(@href, '{}')]]".format(i, articles[i])
            s += ']'
            return s

        self.dr.find_element_by_xpath(build_list_string(articles))

    def check_no_articles(self, articles):
        # no other articles
        self.visit_fav_list()
        if articles is not None:
            found = False
            for i in articles:
                try:
                    self.dr.find_element_by_xpath("//li[a[contains(@href, '{}')]]".format(i))
                    found = True
                except NoSuchElementException:
                    pass
            self.assertFalse(found, 'still found')

    def test_1_check_list(self):
        self.check_list(self.articles)

    def test_2_add_and_del_fav_article(self):
        l = self.articles + self.a
        self.visit_and_add_fav_record(l, '444')
        self.check_list(l)
        self.visit_and_del_fav_record(l, '444')
        self.check_list(self.articles)
        self.check_no_articles(self.a)

    def tearDown(self):
        self.visit_fav_table()
        self.del_fav_record(self.articles, '111')
        self.del_fav_record(self.articles[0:2], '222')
        self.del_fav_record(self.articles[0:1], '333')

    @classmethod
    def tearDownClass(cls):
        cls.dr.quit()


if __name__ == '__main__':
    unittest.main()
