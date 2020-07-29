import unittest
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


# This is to test "My Favourite Articles" widget
class MyFavListTests(unittest.TestCase):

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

        # articles will be added when testing
        cls.a = ['435186b5474321009db4b5b08b9a7160']
        # articles added before testing
        cls.articles = ['c85cd2519f77230088aebde8132e70c2',
                        'dcf43d75474321009db4b5b08b9a71dc',
                        '3b0fccee0a0a0b9b00d34b36ea41a43e']
        # user id
        cls.user = '1d6097281b39101064244375cc4bcbf8'

        # page links
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

        print("login successfully")

    # add dummy records before each test
    def setUp(self):
        self.add_fav_record(self.articles, self.user)

    def visit_table(self):
        if self.dr.current_url != self.table_url:
            sleep(1)
            self.dr.get(self.table_url)
            sleep(1)
            self.dr.switch_to.frame("gsft_main")

    # add records into the table
    def add_fav_record(self, articles, user):
        self.visit_table()
        for article in articles:
            self.dr.find_element_by_id('sysverb_new').click()
            self.dr.find_element_by_id('x_512628_webwidget_favourite_records.user_id').send_keys(user)
            self.dr.find_element_by_id('x_512628_webwidget_favourite_records.article_id').send_keys(article)
            self.dr.find_element_by_id('sysverb_insert_bottom').click()

    # delete records from the table
    def del_fav_record(self, articles, user):
        self.visit_table()
        for article in articles:
            self.dr.find_element_by_xpath("//a[text()='{}' and ../following-sibling::td[1]/text()='{}']".format(article, user)).click()
            self.dr.find_element_by_id('sysverb_delete_bottom').click()
            self.dr.find_element_by_id('ok_button').click()

    # visit the test page of the widget
    def visit_fav_list(self):
        if self.dr.current_url != self.fav_list_url:
            sleep(1)
            self.dr.get(self.fav_list_url)

    # check whether the table has desired records
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

    # test showing my favourite articles
    def test_1_list_show_articles(self):
        print('start testing showing favourites')
        self.check_list(self.articles)
        print('test passed')

    # test showing my favourite articles after adding and removing an article
    def test_2_add_and_del_fav_record(self):
        print('start testing showing favourites when adding and removing favourites')

        # add favourite records and check
        self.add_fav_record(self.a, self.user)
        self.check_list(self.articles + self.a)

        # remove favourite records and check
        self.del_fav_record(self.a, self.user)
        self.check_list(self.articles, self.a)

        print('test passed')

    # test showing favourite articles when others favourite articles
    def test_3_others_add_record(self):
        print('start testing showing favourite when others add favourites')
        self.add_fav_record(self.a, '111')
        self.check_list(self.articles, self.a)
        self.del_fav_record(self.a, '111')
        print('test passed')

    # add duplicate, only show 1?

    # delete dummy records after each test
    def tearDown(self):
        self.del_fav_record(self.articles, self.user)

    # quit driver
    @classmethod
    def tearDownClass(cls):
        cls.dr.quit()


if __name__ == '__main__':
    unittest.main()
