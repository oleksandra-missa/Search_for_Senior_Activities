import requests
from bs4 import BeautifulSoup
import re
import io
import pandas as pd
from pdfminer.high_level import extract_text

BASE_URL = "https://dlaseniora.krakow.pl/278715,artykul,centra-aktywnosci-seniorow.html"
DOMAIN = "https://dlaseniora.krakow.pl"

res = requests.get(BASE_URL)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")

# listy na dane
results = []

# 1. Znajdź linki do podstron CAS wraz z nazwami
cas_entries = []
for a in soup.find_all("a", href=True):
    if "/centra_aktywnosci_seniorow/" in a['href']:
        link = a['href']
        if not link.startswith("http"):
            link = DOMAIN + link
        cas_name = a.get_text(strip=True).replace("\n", " ")
        cas_entries.append((cas_name, link))

print(f"Znaleziono {len(cas_entries)} podstron CAS")

# 2. Odwiedź każdą podstronę CAS i pobierz tylko ostatni PDF
for cas_name, cas_url in cas_entries:
    try:
        print(f"\nSprawdzam: {cas_name} ({cas_url})")
        page = requests.get(cas_url)
        page.raise_for_status()
        soup_cas = BeautifulSoup(page.text, "html.parser")

        pdfs = [a['href'] for a in soup_cas.find_all("a", href=True) if "zalacznik" in a['href']]

        if not pdfs:
            print("Brak PDF na tej stronie")
            continue

        # wybieramy ostatni link PDF
        last_pdf = pdfs[-1]
        if not last_pdf.startswith("http"):
            last_pdf = "https://plikimpi.krakow.pl" + last_pdf

        print(f"Pobieram ostatni PDF: {last_pdf}")
        pdf_data = requests.get(last_pdf).content
        text = extract_text(io.BytesIO(pdf_data))

        found_emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
        if found_emails:
            for email in found_emails:
                results.append({"CAS_name": cas_name, "Email": email})
            print("Znalezione e-maile:", found_emails)
        else:
            print("Brak adresów e-mail w tym PDF")

    except Exception as e:
        print(f"Błąd przy {cas_url}: {e}")

# 3. Zapis do Excela
if results:
    df = pd.DataFrame(results)
    df.to_excel("CAS_emails.xlsx", index=False)
    print("\n✅ Zapisano wyniki do pliku CAS_emails.xlsx")
else:
    print("\n⚠️ Nie znaleziono żadnych adresów e-mail")