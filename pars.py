import requests
from bs4 import BeautifulSoup
import csv

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_html(url):
    try:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        return r.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return None

def norm_find(s):
    if not s:
        return "0"
    return s.split(" ")[0].replace(",", "").replace("(", "").strip()

def save_to_csv(data_list):
    with open("plugins.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "URL", "Rating Count"])
        
        for item in data_list:
            writer.writerow((item["name"], item["url"], item["rating"]))

def get_data(html):
    if not html:
        return []
        
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.find_all("section")
    if len(sections) < 3:
        print("Не удалось найти нужную секцию с плагинами")
        return []

    popular_section = sections[2]
    plugins = popular_section.find_all("li")
    
    results = []
    for plugin in plugins:
        try:
            name_tag = plugin.find("h3")
            if not name_tag: continue
            
            name = name_tag.text.strip()
            url = name_tag.find("a").get("href")
            
            rating_tag = plugin.find("span", class_="rating-count")
            r_text = rating_tag.text if rating_tag else "0"
            rating = norm_find(r_text)
            
            results.append({
                "name": name,
                "url": url,
                "rating": rating
            })
        except AttributeError:
            continue
            
    return results

def main():
    url = "https://wordpress.org/plugins/"
    print("Начинаю парсинг...")
    
    html = get_html(url)
    data = get_data(html)
    
    if data:
        save_to_csv(data)
        print(f"Готово! Сохранено плагинов: {len(data)}")
    else:
        print("Данные не найдены.")

if __name__ == '__main__':
    main()