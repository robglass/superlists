from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_table_list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

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
        self.check_for_row_in_list_table('1: Finish App')

        # There is still a textbox for the User to enter another item. User enters "Upload to git."
        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys('Push app to git.')
        inputBox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Page updates again, and now shows both items
        self.check_for_row_in_list_table('1: Finish App')
        self.check_for_row_in_list_table('2: Push app to git. ')


        # User notices sites URL has changed.

        # navigating to new URL shows same to-do list.
        self.fail('Finish the tests!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
