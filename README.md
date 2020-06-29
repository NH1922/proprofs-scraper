# ProProfs Scraper

A simple scraper for ProProfs which is often used for going through quizes. 
The scraper can pull the entire quiz in the desired files using 'questions.py'.
``` python questions.py > filename'```
Bringing the answers has a dependency on selenium. This code depends on the ChromeDrivers for Selenium (https://chromedriver.chromium.org/getting-started) 

Download the chromedriver and place them in a folder named 'webdriver' inside the root directory of the repository and set the path appropriately in answers.py. Run the answers.py to get the answers for the quiz in a seperate csv. 



