import requests
from bs4 import BeautifulSoup
import smtplib
import datetime as dt

email = "Your Email Address"
passw = "Password"
url = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"  # any amazon product url
headers = {
    "Accept-Language": "en-GB,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
}
is_price = False
while not is_price:
    now = dt.datetime.now()
    time = int(now.strftime("%H"))
    if time == 7:  # can change time from here...Time Format Hour 00-23
        response = requests.get(url, headers=headers)
        web_content = response.text
        soup = BeautifulSoup(web_content, "html.parser")
        item_price = soup.find(name="span", class_="a-offscreen")
        item_title = soup.find(name="span", class_="productTitle")
        item_price_as_float = float(item_price.getText().strip("$"))

        if item_price_as_float < 200:    # set target price here
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=email, password=passw)
                connection.sendmail(from_addr=email,
                                    to_addrs=email,
                                    msg=f"subject:Price Alert\n\n{item_title}"
                                        f"is now ${item_price_as_float}\n {url}")
            is_price = True
