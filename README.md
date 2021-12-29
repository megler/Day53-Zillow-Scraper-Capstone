# Zillow Scraper

Given a set of parameters, scrape Zillow and fill out Google Form with
gathered data. This project uses Beautiful Soup, Selenium and Google Forms.


## Usage

1. Replace `ZILLOW_URL` with your Zillow URL containing whatever search results
you're trying to gather. It doesn't have to be in an .env file. I have it there
to keep things clean. If not in an .env, then line 26 of main.py needs to be replaced
with the URL you wish to use.

2. Replace `FORM_URL` with the URL to the Google Form you wish to fill out. Again,
if not using .env, then replace with actual URL as in Step 1. You'll need to create
a Google form with short answer fields for any data you're trying to create. The
form for this code has 3 questions:
    * What's the address?
    * What's the rent?
    * What's the link?

3. If you get a captcha when you try to scrape Zillow with BS4, try changing your
header. The header in this code currently works, though no guarantee it always will.

4. The current code is set to gather price, address and URL of property. You can 
change this to anything returned in the JSON object created on line 36. To see what
is returned, run a for loop like this:

    for result in data["cat1"]["searchResults"]["listResults"]:
        print(result)

You can pick and choose what you want to data gather from there.

5. There are no unique identifying IDs, Classes, etc on Google Froms. XPATH was
used to fill in the form. Note that `driver.find_element_by` is deprecated in
Selenium. You must use `driver.find_element(By...)` formatting. 

The current Selenium4 Documentation isn't the best, but can be referred to [here](https://www.selenium.dev/selenium/docs/api/py/index.html). As with most things, Stack Overflow will guide you. Just be sure to
look at more recent SO answers vs year or older.





## License
[MIT](https://choosealicense.com/licenses/mit/)