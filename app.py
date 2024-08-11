from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import os
import time
from selenium.common.exceptions import StaleElementReferenceException

app = Flask(__name__)

# Get the Firefox profile path and geckodriver path from environment variables
PROFILE_PATHS = {
    "default-release": os.getenv("FIREFOX_PROFILE_DEFAULT_RELEASE", ""),
    "default": os.getenv("FIREFOX_PROFILE_DEFAULT", "")
}

GECKODRIVER_PATH = os.getenv("GECKODRIVER_PATH", "")

# This global driver will be used across both endpoints
driver = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_login', methods=['POST'])
def start_login():
    global driver
    data = request.json
    profile_key = data.get('profile_key')

    if not profile_key:
        return jsonify({'error': 'Profile key is required'}), 400

    profile_path = PROFILE_PATHS.get(profile_key)
    if not profile_path:
        return jsonify({'error': f"Profile '{profile_key}' not found"}), 400

    # Set up Selenium WebDriver to use Firefox with the specified path to geckodriver
    service = Service(GECKODRIVER_PATH)
    
    # Set up Firefox options to use the selected profile
    options = Options()
    options.set_preference("profile", profile_path)
    
    # Initialize the WebDriver
    driver = webdriver.Firefox(service=service, options=options)
    
    # Go to Twitter login page and wait for the user to log in
    driver.get("https://twitter.com/login")
    
    return jsonify({'status': 'Browser opened, please log in.'})

@app.route('/continue_search', methods=['POST'])
def continue_search():
    global driver
    data = request.json
    name = data.get('name')
    negative_words = data.get('negative_words', [])

    if not name or not negative_words:
        return jsonify({'error': 'Missing required fields'}), 400
    
    results = []

    try:
        for word in negative_words:
            # Construct the query URL with the name and one negative word
            query = f'"{name}" AND "{word}"'
            
            url = f"https://twitter.com/search?q={query}&src=typed_query"
            print(f"Searching Twitter for: {url}")
            
            # Load the Twitter search page
            driver.get(url)
            
            # Wait for the search results to load
            time.sleep(5)
            
            # Click on the "Latest" tab using XPath to locate the element
            latest_tab = driver.find_element(By.XPATH, "//a[contains(@href, 'f=live')]")
            latest_tab.click()
            
            # Wait for the "Latest" tweets to load
            time.sleep(5)
            
            # Get the list of tweets
            tweets = driver.find_elements(By.CSS_SELECTOR, 'article div[lang]')
    
            if not tweets:
                results.append(f"No tweets found for the combination: '{name}' and '{word}'.")
                continue

            # Interact with each tweet
            for i in range(len(tweets)):
                retries = 3  # Number of retries for each tweet
                while retries > 0:
                    try:
                        # Re-locate the tweet element
                        tweet = driver.find_elements(By.CSS_SELECTOR, 'article div[lang]')[i]
                        tweet.click()  # Click on the tweet to open it
                        time.sleep(2)  # Wait for the tweet to fully load
                        tweet_text = tweet.text
                        if word.lower() in tweet_text.lower():
                            results.append("SUS!!!!!!")
                            results.append(f"Tweet: {tweet_text}")
                        else:
                            results.append(f"No SUS activity found in this tweet for '{name}' and '{word}'.")
                        
                        # Optionally, close the tweet overlay or return to the search results
                        driver.back()  # Navigate back to the search results
                        time.sleep(2)  # Wait for the page to return to the search results
                        break  # Exit retry loop if successful
                    except StaleElementReferenceException:
                        print(f"Stale element reference for tweet {i}, retrying...")
                        retries -= 1
                        if retries == 0:
                            results.append(f"Could not click on tweet {i} after multiple retries due to stale element reference.")
    
    finally:
        # Close the browser
        driver.quit()
    
    return jsonify({'results': results})

if __name__ == "__main__":
    app.run(debug=True)
