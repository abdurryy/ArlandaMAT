import cloudscraper
from datetime import datetime
from bs4 import BeautifulSoup

class ArlandaMAT():
    def __init__(self) -> None:
        self.req = cloudscraper.create_scraper()
        return None
    
    def remove_breaks(self, obj : list) -> list:
        n = []
        for x in obj:
            n.append([x for x in [o for o in x.split("\n")] if x != ""])
        return n

    def get_menus(self) -> list:
        r = self.req.get("https://mpi.mashie.com/public/app/Sigtuna%20Kommun/425457e0")
        bs = BeautifulSoup(r.text, "html.parser")
        p = [str(x.text) for x in bs.find_all("div",{"class":"panel panel-default app-default"})]
        try:p.append(bs.find_all("div",{"class":"panel panel-primary"})[0].text)
        except:pass
        obj = self.remove_breaks(p)
        return obj
    
    def get_day(self, day : str) -> list or None:
        ma = [("Januari", "jan"), ("Februari", "feb"), ("Mars", "mar"), ("April", "apr"), ("Maj", "maj"), ("Juni", "jun"), ("Juli", "jul"), ("Augusti", "aug"), ("September", "sep"), ("Oktober", "okt"), ("November", "nov"), ("December", "dec")]
        m = day.split(" ")[1]
        d = day.split(" ")[0]
        try: m = [x[1] for x in ma if m.lower() in x[0].lower() or m.lower() == x[0].lower()][0]
        except:return None
        try: 
            d=int(d)
            day = f"{d} {m}"
            if len(day.split(" ")[0]) == 1:
                day = f"0{day.split(' ')[0]} {m}"
        except:
            return None
        for menu in self.get_menus():
            if menu[0].lower() == day.lower():
                return menu
        return None
    
    def get_search(self, smeal : str) -> list or None:
        meals = []
        for menu in self.get_menus():
            b = [meal for meal in [menu[3],menu[5]] if smeal.lower() in meal.lower() or smeal.lower() == meal.lower()][0] if len([meal for meal in [menu[3],menu[5]] if smeal.lower() in meal.lower() or smeal.lower() == meal.lower()]) > 0 else None
            if b != None:
                meals.append([menu[0], menu[1], b])
        return meals if len(meals) > 0 else None

    def get_today(self) -> list:
        day = datetime.now().strftime("%d %B")
        ma = [("January", "jan"), ("February", "feb"), ("March", "mar"), ("April", "apr"), ("May", "maj"), ("June", "jun"), ("July", "jul"), ("August", "aug"), ("September", "sep"), ("October", "okt"), ("November", "nov"), ("December", "dec")]
        d = day.split(" ")[0]
        m = [x[1] for x in ma if day.split(" ")[1].lower() in x[0].lower() or day.split(" ")[1].lower() == x[0].lower()][0]
        day = f"{d} {m}"
        if len(day.split(" ")[0]) == 1:
            day = f"0{day.split(' ')[0]} {m}"
        return self.get_day(day)
print(ArlandaMAT().get_today())
print(ArlandaMAT().get_day("20 mar"))