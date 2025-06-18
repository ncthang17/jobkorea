import pandas as pd
from bs4 import BeautifulSoup
from requests import get
from urllib.parse import quote
import time
import random

def extract_key_fields(detail_soup):
    """
    Extracts only the needed fields from the detailed info table.
    """
    field_map = {
        "자본금": "",
        "매출액": "",
        "대표자": "",
        "설립일": ""
    }

    rows = detail_soup.select("div.company-infomation-row.basic-infomation table tr.field")

    for row in rows:
        ths = row.select("th.field-label")
        tds = row.select("td.field-value")

        for th, td in zip(ths, tds):
            label = th.get_text(strip=True)
            if label in field_map:
                value_container = td.select_one("div.value") or td.select_one("div.values div.value")
                field_map[label] = value_container.get_text(strip=True) if value_container else ""

    return field_map


def get_jobkorea_data(corp_name_list, page_no=1):
    """
    Main scraping function for given list of company names.
    Skips companies with less than 3 metadata spans.
    """
    jobkorea_data = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    total = len(corp_name_list)
    for idx, corp_name in enumerate(corp_name_list, start=1):
        print(f"[{idx}/{total}] Processing: {corp_name}")

        encoded_name = quote(corp_name)
        url = f"https://www.jobkorea.co.kr/Search/?stext={encoded_name}&tabType=corp&Page_No={page_no}"

        try:
            response = get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"[ERROR] Failed to fetch {url}")
                continue
        except Exception as e:
            print(f"[EXCEPTION] Error fetching {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        containers = soup.find_all(
            "div",
            class_="Flex_display_flex__i0l0hl2 Flex_direction_row__i0l0hl3 Flex_justify_space-between__i0l0hlf",
        )

        for container in containers:
            inner_flex = container.find(
                "div",
                class_="Flex_display_flex__i0l0hl2 Flex_gap_space12__i0l0hls Flex_direction_row__i0l0hl3",
            )
            if not inner_flex:
                continue

            spans = inner_flex.find_all("span", class_="Typography_variant_size14__344nw27")

            if len(spans) < 3:
                print("  → Skipped: Not enough metadata.")
                continue

            corp_type = corp_location = corp_industry = ""
            if len(spans) == 3:
                corp_type, corp_location, corp_industry = [s.get_text(strip=True) for s in spans]
            elif len(spans) == 4:
                corp_type, corp_location, corp_industry = spans[1].get_text(strip=True), spans[2].get_text(strip=True), spans[3].get_text(strip=True)

            capital = sales = ceo = foundation_date = ""

            parent = container.find_parent(
                "div", class_="Flex_display_flex__i0l0hl2 Flex_gap_space4__i0l0hly Flex_direction_column__i0l0hl4"
            )
            a_tag = parent.find("a", href=True) if parent else None

            if a_tag:
                try:
                    detail_response = get(a_tag['href'], headers=headers, timeout=10)
                    detail_soup = BeautifulSoup(detail_response.text, "html.parser")
                    fields = extract_key_fields(detail_soup)
                    capital = fields["자본금"]
                    sales = fields["매출액"]
                    ceo = fields["대표자"]
                    foundation_date = fields["설립일"]
                except Exception as e:
                    print(f"  [EXCEPTION] Failed to parse detail page: {e}")

            jobkorea_data.append({
                "기업명": corp_name,
                "기업형태": corp_type,
                "지역": corp_location,
                "업종": corp_industry,
                "자본금": capital,
                "매출액": sales,
                "대표자": ceo,
                "설립일": foundation_date
            })

        time.sleep(random.uniform(2.5, 4.0))

    return pd.DataFrame(jobkorea_data)


if __name__ == "__main__":
    corp_name_list = ["지일", "삼성전자", "LG화학", "가짜기업명"]
    result_df = get_jobkorea_data(corp_name_list)

    result_df.to_csv("jobkorea_data_clean.csv", index=False, encoding="utf-8-sig")
    print("\n✅ Data collection complete. Sample:")
    print(result_df.head())