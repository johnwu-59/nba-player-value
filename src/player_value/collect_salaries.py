"""Parse player salary records from a manually saved Spotrac HTML page."""
from pathlib import Path
from bs4 import BeautifulSoup
import csv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
HTML_PATH = PROJECT_ROOT / "data" / "raw" / "spotrac_base_salary_2025_26.html"


if __name__ == "__main__":
    html = HTML_PATH.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    rows = soup.find_all("li", class_="list-group-item")
    salaries = []
    for row in rows:
        name_element = row.select_one('a.link[href*="/redirect/player/"]')
        salary_element = row.find("span", class_="medium")

        if name_element is None or salary_element is None:
            continue

        player_id = name_element["href"].rstrip("/").rsplit("/", 1)[-1]
        player_name = name_element.get_text(strip=True)
        salary_text = salary_element.get_text(strip=True)
        base_salary = int(salary_text.replace("$", "").replace(",", ""))

        salaries.append({
            "player_id": player_id,
            "name": player_name,
            "base_salary": base_salary
        })

    output_path = PROJECT_ROOT / "data" / "processed" / "spotrac_base_salary_2025_26.csv"
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["player_id", "name", "base_salary"])
        writer.writeheader()
        writer.writerows(salaries)








