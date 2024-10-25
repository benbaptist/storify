import sys

from storify import Storify
from storify.model import Model

class Cookie(Model):
    def __init__(self) -> None:
        self.name = None
        self.flavor = None
        self.shape = None

class CookieJar(Model):
    def __init__(self) -> None:
        self.cookies = []

def main():
    storify = Storify(models=[Cookie, CookieJar])
    db = storify.get_db(name="cookie_db")

    if len(sys.argv) < 2:
        print("Usage: python complex_models.py <new|read>")
        return

    if sys.argv[1] == "new":

        cookie_jar = CookieJar()
        cookie = Cookie()
        cookie.name = "Chocolate Chip"  
        cookie.flavor = "Chocolate"
        cookie.shape = "Circle"
        cookie_jar.cookies.append(cookie)

        cookie = Cookie()
        cookie.name = "Sugar"
        cookie.flavor = "Vanilla"
        cookie.shape = "Square"
        cookie_jar.cookies.append(cookie)

        cookie = Cookie()
        cookie.name = "Oatmeal Raisin"
        cookie.flavor = "Raisin"
        cookie.shape = "Square"
        cookie_jar.cookies.append(cookie)

        db["cookie_jar"] = cookie_jar

        print("Saved cookie jar")
        db.flush()
    elif sys.argv[1] == "read":
        cookie_jar = db["cookie_jar"]

        for cookie in cookie_jar.cookies:
            print(f"* {cookie.name} - {cookie.flavor} - {cookie.shape}")

if __name__ == "__main__":
    main()  