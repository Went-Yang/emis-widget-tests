import unittest
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException, TimeoutException


# visit the favourite record table
def visit_table(dr, retry_time):
    url = 'https://dev67438.service-now.com/nav_to.do?uri=%2Fx_512628_webwidget_favourite_records_list.do'
    if dr.current_url != url:
        # retry
        for _ in range(retry_time):
            try:
                dr.get(url)
                sleep(3)
                dr.switch_to.frame("gsft_main")
                break
            except (UnexpectedAlertPresentException, TimeoutException):
                continue


# delete all the records
def del_all_record(dr, retry_time):
    for _ in range(retry_time):
        try:
            url = 'https://dev67438.service-now.com/nav_to.do?uri=%2Fsys_db_object.do%3Fsys_id%3D385e11941b0e501064244375cc4bcb0c%26sysparm_record_target%3Dsys_db_object%26sysparm_record_row%3D1%26sysparm_record_rows%3D2430%26sysparm_record_list%3Dsys_update_nameISNOTEMPTY%5Elabel%3E%3Dfavourite%5EORDERBYlabel'
            dr.get(url)
            sleep(3)
            dr.switch_to.frame('gsft_main')
            dr.find_element_by_id('delete_all_records').click()
            sleep(1)
            dr.switch_to.alert.send_keys('delete')
            dr.switch_to.alert.accept()
            sleep(2)
            dr.switch_to.alert.accept()
            break
        except:
            continue


# This is to test the "Favourite" and "Unfavourite" buttons
class FavBtnTests(unittest.TestCase):

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
        cls.dr.implicitly_wait(5)
        cls.retry_time = 3

        # define article id and user id
        cls.article = '207de43187032100deddb882a2e3ec7a'
        cls.user = '1d6097281b39101064244375cc4bcbf8'

        # page links
        cls.article_prefix = \
            'https://dev67438.service-now.com/sp?id=kb_article_view_new&sys_id='
        cls.article_url = cls.article_prefix + cls.article

        # login to the instance
        print("login")
        for _ in range(cls.retry_time):
            try:
                cls.dr.get(cls.article_url)
                cls.dr.find_element_by_id('username').send_keys('wentao.yang')
                cls.dr.find_element_by_id('password').send_keys('shoh_FLIR8raum@aul')
                cls.dr.find_element_by_name('login').click()
                sleep(3)
                break
            except:
                continue

    def setUp(self):
        del_all_record(self.dr, self.retry_time)

    # visit the article page
    def visit_article(self):
        if self.dr.current_url != self.article_url:
            self.dr.get(self.article_url)
            sleep(3)

    # test marking an article as favourite
    def test_1_add_fav(self):
        print('Test1: add favourites')

        # click the favourite button
        self.visit_article()
        self.dr.find_element_by_id('favourite').click()

        # visit table to check records
        # if not found, it will throw an exception
        visit_table(self.dr, self.retry_time)
        self.dr.find_element_by_xpath("//tr[td/a/text()='{}' and td/text()='{}']".format(self.article, self.user))

    # test removing an favourite article
    def test_2_remove_fav(self):
        print('Test2: remove favourites')

        # click the favourite button
        self.visit_article()
        self.dr.find_element_by_id('favourite').click()

        # visit table to check records
        # if not found, it will throw an exception
        visit_table(self.dr, self.retry_time)
        self.dr.find_element_by_xpath("//tr[td/a/text()='{}' and td/text()='{}']".format(self.article, self.user))

        # click the unfavourite button
        self.visit_article()
        self.dr.find_element_by_id('unfavourite').click()

        # visit table to check records
        # not found will throw exception, which is expected
        visit_table(self.dr, self.retry_time)
        raised = False
        try:
            self.dr.find_element_by_xpath("//tr[td/a/text()='{}' and td/text()='{}']".format(self.article, self.user))
        except NoSuchElementException:
            raised = True
        self.assertTrue(raised, "the record still exists")

    def tearDown(self):
        del_all_record(self.dr, self.retry_time)

    # quit driver
    @classmethod
    def tearDownClass(cls):
        cls.dr.quit()


if __name__ == '__main__':
    unittest.main()
