import unittest
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from test_fav_btn import del_all_record, visit_table
from test_my_fav_list import add_fav_record, del_fav_record


# This is to test "Most Favourite Articles" widget
class MostFavListTests(unittest.TestCase):

    dr = None

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

        # define article id and user id
        cls.a = ['435186b5474321009db4b5b08b9a7160']
        cls.articles = ['c85cd2519f77230088aebde8132e70c2',
                        'dcf43d75474321009db4b5b08b9a71dc']
        cls.user = '1d6097281b39101064244375cc4bcbf8'
        cls.article_url = \
            'https://dev67438.service-now.com/sp?id=kb_article_view_new&sys_id='
        cls.fav_list_url = \
            'https://dev67438.service-now.com/sp?id=most_favourite_articles_test_page'

        # login to the instance
        print("login")
        for _ in range(cls.retry_time):
            try:
                cls.dr.get(cls.fav_list_url)
                cls.dr.find_element_by_id('username').send_keys('wentao.yang')
                cls.dr.find_element_by_id('password').send_keys('shoh_FLIR8raum@aul')
                cls.dr.find_element_by_name('login').click()
                sleep(3)
                break
            except:
                continue

    def setUp(self):
        print('add dummy records')
        del_all_record(self.dr, self.retry_time)
        visit_table(self.dr, self.retry_time)
        add_fav_record(self.dr, self.articles, '111', self.retry_time)
        add_fav_record(self.dr, self.articles[0:1], '222', self.retry_time)

    def visit_fav_list(self):
        if self.dr.current_url != self.fav_list_url:
            self.dr.get(self.fav_list_url)
            sleep(3)

    def visit_and_add_fav_record(self, articles, user):
        visit_table(self.dr, self.retry_time)
        add_fav_record(self.dr, articles, user, self.retry_time)

    def visit_and_del_fav_record(self, articles, user):
        visit_table(self.dr, self.retry_time)
        del_fav_record(self.dr, articles, user, self.retry_time)

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
        print('Test1: showing most favourites')
        self.check_list(self.articles)

    def test_2_add_and_del_fav_article(self):
        print('Test2: showing most favourites after adding and removing')
        l = self.articles + self.a
        self.visit_and_add_fav_record(l, '333')
        self.check_list(l)
        self.visit_and_del_fav_record(l, '333')
        self.check_list(self.articles)
        self.check_no_articles(self.a)

    def tearDown(self):
        print('remove dummy records')
        del_all_record(self.dr, self.retry_time)

    @classmethod
    def tearDownClass(cls):
        cls.dr.quit()


if __name__ == '__main__':
    unittest.main()
