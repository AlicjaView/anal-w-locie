import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import os
from datetime import datetime

def get_lottery_numbers(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Znajdź pierwszy znacznik div na stronie
        data_container = soup.find('div')
        if not data_container:
            print("Nie znaleziono kontenera z danymi liczbowymi.")
            return []

        # Sprawdź, czy kontener zawiera tekst
        if not data_container.text.strip():
            print("Kontener z danymi liczbowymi jest pusty.")
            return []

        # Wykorzystaj wyrażenie regularne do znalezienia tylko liczb od 1 do 49
        numbers_match = re.findall(r'\b(?:[1-9]|[1-4]\d|50)\b', data_container.text)
        numbers = list(map(int, numbers_match))

        return numbers

    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania danych: {e}")
        return []
    except ValueError as e:
        print(f"Błąd przetwarzania danych liczbowych: {e}")
        return []

def analyze_lottery_numbers(numbers):
    total_numbers = len(numbers)

    # Analiza najczęściej wypadających liczb
    number_count = Counter(numbers)

    # Wybierz 6 najbardziej prawdopodobnych liczb
    most_probable_numbers = [number for number, _ in number_count.most_common(6)]

    return most_probable_numbers

def main():
    # Uzyskaj dzisiejszą datę
    current_date = datetime.now().strftime("%d-%m-%Y")

    # Zaktualizuj link z dzisiejszą datą
    url_strony = f"https://megalotto.pl/wyniki/lotto/losowania-od-27-Stycznia-1957-do-{current_date}"
    
    lottery_numbers = get_lottery_numbers(url_strony)

    if lottery_numbers:
        # Czyść ekran
        os.system('cls' if os.name == 'nt' else 'clear')

        most_probable_numbers = analyze_lottery_numbers(lottery_numbers)

        print("6 najbardziej prawdopodobnych liczb:")
        print(most_probable_numbers)
    else:
        print("Brak danych do analizy.")

if __name__ == "__main__":
    main()

