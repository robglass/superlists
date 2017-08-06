from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # User notes the page title and header mention to-do lists.
        self.browser.get('http://localhost:8000')
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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_table_list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1. Finish App' for row in rows),
            "New to-do item did not appear in table"
        )

        # There is still a textbox for the User to enter another item. User enters "Upload to git."
        self.fail('Finish the tests!')

        # User notices sites URL has changed.

        # navigating to new URL shows same to-do list.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
