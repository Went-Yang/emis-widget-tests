import unittest
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException


# This is to test "My Favourite Articles" widget
class MyFavListTests(unittest.TestCase):
    dr = None

    # start driver and login to the instance
    @classmethod
    def setUpClass(cls):
        # use chrome to test
        chrome_options = webdriver.ChromeOptions()
        # enable headless mode
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # set options
        cls.dr = webdriver.Chrome(options=chrome_options)
        # set the implicit wait time
        cls.dr.implicitly_wait(3)
        cls.retry_time = 3

        # articles will be added when testing
        cls.a = ['435186b5474321009db4b5b08b9a7160']
        # articles added before testing
        cls.articles = ['c85cd2519f77230088aebde8132e70c2',
                        'dcf43d75474321009db4b5b08b9a71dc']
        # user id
        cls.user = '1d6097281b39101064244375cc4bcbf8'

        # page links
        cls.article_url = \
            'https://dev67438.service-now.com/sp?id=kb_article_view_new&sys_id='
        cls.fav_list_url = \
            'https://dev67438.service-now.com/sp?id=my_favourite_articles_test_page'

        # login to the instance
        print("login")
        for _ in range(cls.retry_time):
            try:
                cls.dr.get(cls.article_url + cls.articles[0])
                cls.dr.find_element_by_id('username').send_keys('wentao.yang')
                cls.dr.find_element_by_id('password').send_keys('shoh_FLIR8raum@aul')
                cls.dr.find_element_by_name('login').click()
                sleep(3)
                break
            except:
                continue

    # add dummy records before each test
    def setUp(self):
        print('add dummy records')
        self.del_all_record()
        self.add_fav_record(self.articles, self.user)

    # visit the test page of the widget
    def visit_fav_list(self):
        if self.dr.current_url != self.fav_list_url:
            self.dr.get(self.fav_list_url)
            sleep(3)

    # visit the favourite record table
    def visit_table(self):
        url = 'https://dev67438.service-now.com/nav_to.do?uri=%2Fx_512628_webwidget_favourite_records_list.do'
        if self.dr.current_url != url:
            # retry
            for _ in range(self.retry_time):
                try:
                    self.dr.get(url)
                    sleep(3)
                    self.dr.switch_to.frame("gsft_main")
                    break
                except (UnexpectedAlertPresentException, TimeoutException):
                    continue

    # add records into the table
    def add_fav_record(self, articles, user):
        for article in articles:
            for _ in range(self.retry_time):
                try:
                    self.visit_table()
                    self.dr.find_element_by_id('sysverb_new').click()
                    sleep(1)
                    self.dr.find_element_by_id('x_512628_webwidget_favourite_records.user_id').send_keys(user)
                    self.dr.find_element_by_id('x_512628_webwidget_favourite_records.article_id').send_keys(article)
                    self.dr.find_element_by_id('sysverb_insert_bottom').click()
                    sleep(1)
                    break
                except:
                    continue

    # delete records from the table
    def del_fav_record(self, articles, user):
        for article in articles:
            for _ in range(self.retry_time):
                try:
                    self.visit_table()
                    self.dr.find_element_by_xpath(
                        "//a[text()='{}' and ../following-sibling::td[1]/text()='{}']".format(article, user)).click()
                    self.dr.find_element_by_id('sysverb_delete_bottom').click()
                    self.dr.find_element_by_id('ok_button').click()
                    sleep(1)
                    break
                except:
                    continue

    # delete all the records
    def del_all_record(self):
        for _ in range(self.retry_time):
            try:
                url = 'https://dev67438.service-now.com/nav_to.do?uri=%2Fsys_db_object.do%3Fsys_id%3D385e11941b0e501064244375cc4bcb0c%26sysparm_record_target%3Dsys_db_object%26sysparm_record_row%3D1%26sysparm_record_rows%3D2430%26sysparm_record_list%3Dsys_update_nameISNOTEMPTY%5Elabel%3E%3Dfavourite%5EORDERBYlabel'
                self.dr.get(url)
                sleep(3)
                self.dr.switch_to.frame('gsft_main')
                self.dr.find_element_by_id('delete_all_records').click()
                sleep(1)
                self.dr.switch_to.alert.send_keys('delete')
                self.dr.switch_to.alert.accept()
                sleep(2)
                self.dr.switch_to.alert.accept()
                break
            except:
                continue

    # check whether the table has desired records
    def check_list(self, articles, exception=None):
        for article in articles:
            for _ in range(self.retry_time):
                try:
                    self.visit_fav_list()
                    self.dr.find_element_by_xpath("//a[contains(@href,'{}')]".format(article))
                    break
                except:
                    continue

        if exception is not None:
            raised = 0
            for article in exception:
                try:
                    self.dr.find_element_by_xpath("//a[contains(@href,'{}')]".format(article))
                except:
                    raised += 1
            self.assertEqual(len(exception), raised, 'still can see the article in my fav list')

    # test showing my favourite articles
    def test_1_list_show_articles(self):
        print('Test1: showing favourites')
        self.check_list(self.articles)

    # test showing my favourite articles after adding and removing an article
    def test_2_add_and_del_fav_record(self):
        print('Test2: showing favourites when adding and removing favourites')

        # add favourite records and check
        self.add_fav_record(self.a, self.user)
        self.check_list(self.articles + self.a)

        # remove favourite records and check
        self.del_fav_record(self.a, self.user)
        self.check_list(self.articles, self.a)

    # test showing favourite articles when others favourite articles
    def test_3_others_add_record(self):
        print('Test3: showing favourite when others add favourites')
        self.add_fav_record(self.a, '111')
        self.check_list(self.articles, self.a)
        self.del_fav_record(self.a, '111')

    # delete dummy records after each test
    def tearDown(self):
        print('remove dummy records')
        self.del_all_record()

    # quit driver
    @classmethod
    def tearDownClass(cls):
        cls.dr.quit()


if __name__ == '__main__':
    unittest.main()
