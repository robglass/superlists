from selenium import webdriver
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
        self.fail('Finish the test!')

        # User is invited to enter new To-do item right away

        # User types "Finish App" in to a text box

        # When User hits enter, the page updates, and now the page lists "1. Finish App" in a to-do list

        # There is still a textbox for the User to enter another item. User enters "Upload to git."

        # User notices sites URL has changed.

        # navigating to new URL shows same to-do list.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
