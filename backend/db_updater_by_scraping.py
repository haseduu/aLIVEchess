from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import schedule
import time
import datetime
def scrape_chess_players_selenium():
    url = "https://2700chess.com/"
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        print(f"Successfully loaded the webpage. Current URL: {driver.current_url}")
        
        wait = WebDriverWait(driver, 1)
        table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "list")))
        
        leaders = table.find_elements(By.CLASS_NAME, "leaders")
        top_ten = table.find_elements(By.CLASS_NAME, "top_ten")
        all_lines = table.find_elements(By.CLASS_NAME, "all_lines")
        print(f"Found {len(leaders) + len(top_ten) + len(all_lines)} player rows")
        
        data = []
        for player in leaders + top_ten + all_lines:
            try:
                rank = player.find_element(By.CLASS_NAME, "live_standard_pos").text.strip()
                name = player.find_element(By.CLASS_NAME, "name").find_element(By.TAG_NAME, "a").text.strip()
                nationality = player.find_element(By.CLASS_NAME, "country").find_element(By.CLASS_NAME, "flag").get_attribute("title")
                rating = player.find_element(By.CLASS_NAME, "live_standard_rating").find_element(By.TAG_NAME, "strong").text.strip()
                
                data.append({
                    "rank": rank,
                    "name": name,
                    "nationality": nationality,
                    "rating": rating
                })
            except Exception as e:
                print(f"Error parsing player data: {e}")
                print("Player row HTML:")
                print(player.get_attribute('outerHTML'))

        return data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
    finally:
        driver.quit()

def update_db():
    if load_dotenv(".env"):
        url = os.getenv("url_mongo")
        mongo = MongoClient(url)
    all_items = mongo.db.chess_players.find({}, {"_id": 0})
    all_items = list(all_items)
    if len(all_items) == 0:
        data = scrape_chess_players_selenium()
        mongo.db.chess_players.insert_many(data)
        return True
    else:
        mongo.db.chess_players.delete_many({})
    return update_db()

run_time = datetime.time(hour=9, minute=0, second=0)
schedule.every().day.at(str(run_time)).do(update_db)
# Example usage
if __name__ == "__main__":
    update_db()
    while True:
        schedule.run_pending()
        time.sleep(1)
    