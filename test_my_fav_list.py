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
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
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
            'https://dev67438.service-now.com/sp?id=my_favourite_articles_test_page'
        cls.table_url = \
            'https://dev67438.service-now.com/nav_to.do?uri=%2Fx_512628_webwidget_favourite_records_list.do'

        # login to the instance
        cls.dr.get(cls.article_url + cls.articles[0])
        cls.dr.find_element_by_id('username').send_keys('wentao.yang')
        cls.dr.find_element_by_id('password').send_keys('shoh_FLIR8raum@aul')
        cls.dr.find_element_by_name('login').click()

    def setUp(self):
        self.add_fav_record(self.articles, self.user)

    def visit_table(self):
        if self.dr.current_url != self.table_url:
            sleep(1)
            self.dr.get(self.table_url)
            sleep(1)
            self.dr.switch_to.frame("gsft_main")

    def add_fav_record(self, articles, user):
        self.visit_table()
        for article in articles:
            self.dr.find_element_by_id('sysverb_new').click()
            self.dr.find_element_by_id('x_512628_webwidget_favourite_records.user_id').send_keys(user)
            self.dr.find_element_by_id('x_512628_webwidget_favourite_records.article_id').send_keys(article)
            self.dr.find_element_by_id('sysverb_insert_bottom').click()

    def del_fav_record(self, articles, user):
        self.visit_table()
        for article in articles:
            self.dr.find_element_by_xpath("//a[text()='{}' and ../following-sibling::td[1]/text()='{}']".format(article, user)).click()
            self.dr.find_element_by_id('sysverb_delete_bottom').click()
            self.dr.find_element_by_id('ok_button').click()

    def visit_fav_list(self):
        if self.dr.current_url != self.fav_list_url:
            sleep(1)
            self.dr.get(self.fav_list_url)

    def check_list(self, articles, exception=None):
        self.visit_fav_list()

        for article in articles:
            self.dr.find_element_by_xpath("//a[contains(@href,'{}')]".format(article))

        if exception is not None:
            raised = False
            try:
                self.check_list(exception)
            except NoSuchElementException:
                raised = True
            self.assertTrue(raised, 'still can see the article in my fav list')

    def test_1_list_show_articles(self):
        self.check_list(self.articles)

    # add or remove an article, update
    def test_2_add_and_del_fav_record(self):
        self.add_fav_record(self.a, self.user)
        self.check_list(self.articles + self.a)

        self.del_fav_record(self.a, self.user)
        self.check_list(self.articles, self.a)

    # others add, not influenced
    def test_3_others_add_record(self):
        self.add_fav_record(self.a, '111')
        self.check_list(self.articles, self.a)
        self.del_fav_record(self.a, '111')

    # add duplicate, only show 1?

    def tearDown(self):
        self.del_fav_record(self.articles, self.user)

    @classmethod
    def tearDownClass(cls):
        cls.dr.quit()


if __name__ == '__main__':
    unittest.main()
