from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time


MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_table_list')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def tearDown(self):
        self.browser.quit()



    def test_can_start_a_list_for_one_user(self):

        # User notes the page title and header mention to-do lists.
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is invited to enter new To-do item right away
        inputBox =self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputBox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # User types "Finish App" in to a text box
        inputBox.send_keys('Finish App')

        # When User hits enter, the page updates, and now the page lists "1. Finish App" in a to-do list
        inputBox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Finish App')

        # There is still a textbox for the User to enter another item. User enters "Upload to git."
        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys('Push app to git.')
        inputBox.send_keys(Keys.ENTER)

        # Page updates again, and now shows both items
        self.wait_for_row_in_list_table('1: Finish App')
        self.wait_for_row_in_list_table('2: Push app to git.')


        # User notices sites URL has changed.

        # navigating to new URL shows same to-do list.
        self.fail('Finish the tests!')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('This is a new list')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: This is a new list')

        first_list_url = self.browser.current_url
        self.assertRegex(first_list_url, '/lists/.+')

        # New User
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text= self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('This is a new list', page_text)
        self.assertNotIn('Push app to git.', page_text)

        # New Users starts List
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy Milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy Milk')

        # New List has unique URL
        second_list_url = self.browser.current_url
        self.assertRegex(second_list_url, '/lists/.+')
        self.assertNotEqual(first_list_url, second_list_url)

        # New list doesnt include first list items
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Buy Milk', page_text)
        self.assertNotIn('Push app to git.', page_text)


