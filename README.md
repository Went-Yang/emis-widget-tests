# emis-widget-tests

This GitHub repository is to test 3 ServiceNow-based widgets developed by us that are related to the favorites feature. Since the automated testing framework provided by ServiceNow does not support automated testing of service portal widgets, a third-party testing framework, Selenium, was used to perform unit testing to validate the widgets we had created.

**Requirements:**

- Programming Language: Python
- Automated Testing Framework: Selenium
- Web Browser: Chrome

## How to Run Tests?

1. Make sure you have Chrome installed on your machine

2. Follow the instructions to download ChromeDriver and put its location into PATH environment variable

    https://chromedriver.chromium.org/getting-started

3. Make sure you have python 3 installed on your machine

4. Install Python module for Selenium

    ```cmd
    pip install selenium
    ```

5. Run tests

    ```cmd
    # for example
    python test_fav_btn.py
    ```

    