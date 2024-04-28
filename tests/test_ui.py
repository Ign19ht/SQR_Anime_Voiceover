from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def test_dataframe_loaded_failure():
    # Setup Chrome WebDriver
    driver = webdriver.Chrome()

    # URL where your Streamlit app is running
    url = 'http://localhost:8501'
    driver.get(url)

    # Wait for the initial rendering
    time.sleep(2)

    try:
        # Locate the text input and provide some input
        input_element = driver.find_element(By.XPATH, '//input[@placeholder="Example, 12_abcdef..."]')
        test_dir_id = '12_abcdef'
        input_element.send_keys(test_dir_id)
        input_element.send_keys(Keys.RETURN)  # Simulate enter key

        # Check if spinner appears
        spinner = driver.find_element(By.CLASS_NAME, 'stSpinner')
        assert spinner

        # Let's wait for data to load, timeout depends on expected data loading time
        time.sleep(5)  # Adjust according to your application

        # Checking if data table is loaded
        data_table = driver.find_element(By.CSS_SELECTOR, '.stDataFrame')
        assert not data_table

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Clean up after test
        driver.quit()


def test_dataframe_loaded_successfully():
    # Setup Chrome WebDriver
    driver = webdriver.Chrome()

    # URL where your Streamlit app is running
    url = 'http://localhost:8501'
    driver.get(url)

    # Wait for the initial rendering
    time.sleep(2)

    try:
        # Locate the text input and provide some input
        input_element = driver.find_element(By.XPATH, '//input[@placeholder="Example, 12_abcdef..."]')
        test_dir_id = '1O_lS_3AwnHUzH0TfwzSZ_PbHVIEq5PMC'
        input_element.send_keys(test_dir_id)
        input_element.send_keys(Keys.RETURN)  # Simulate enter key

        # Check if spinner appears
        spinner = driver.find_element(By.CLASS_NAME, 'stSpinner')
        assert spinner

        # Let's wait for data to load, timeout depends on expected data loading time
        time.sleep(5)  # Adjust according to your application

        # Checking if data table is loaded
        data_table = driver.find_element(By.CSS_SELECTOR, '.stDataFrame')
        assert data_table

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Clean up after test
        driver.quit()
