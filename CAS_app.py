import flet as ft
import pandas as pd
import requests
import re
import search_by_many_parameters
import sys
from flet_lottie import Lottie
from geopy.distance import geodesic
import subprocess

def geocode_address(address):
    if "kraków" not in address.lower():
        address = address + ", Kraków"

    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    try:
        response = requests.get(url, params=params, headers={"User-Agent": "CAS-Distance-App"})
        data = response.json()
        if data:
            display_name = data[0].get("display_name", "").lower()
            if "kraków" in display_name:
                return float(data[0]["lat"]), float(data[0]["lon"])
            else:
                return None, None
    except Exception as e:
        print("Błąd geokodowania:", e)
    return None, None

def search_view(page: ft.Page):
    df = pd.read_excel("CAS_data.xlsx", sheet_name="Classes")

    lista_wynikow = ft.ListView(expand=1, spacing=6, padding=10)

    info_text = ft.Text(
        "Wpisz nazwę interesujących Cię zajęć i pokażemy wszystkie dostępne terminy we wszystkich ośrodkach.\n\n"
        "Skorzystaj z przycisku “sortowanie”, aby dostosować wyniki wyszukiwania według lokalizacji, dnia, godziny oraz innych.\n\n"
        "Jeśli chcesz zobaczyć wszystkie zajęcia wraz z terminami dla danego ośrodka - nie wpisuj niczego, jedynie zaznacz odpowiedni ośrodek, klikając przycisk “sortowanie”.",
        color=ft.Colors.BLACK54,
        size=14,
    )

    def open_sorting(e):
        print("Open Sorting:")
        subprocess.Popen(
            [sys.executable, "search_by_many_parameters.py"],
            creationflags=subprocess.CREATE_NEW_CONSOLE  # Launch in new terminal window
        )



    sort_button = ft.ElevatedButton("⚙️ Sortowanie", on_click=open_sorting)

    def aktualizuj_wyniki(e):
        tekst = pole.value.strip().lower()
        lista_wynikow.controls.clear()

        if len(tekst) >= 1:
            pattern = rf'\b{re.escape(tekst)}'
            wyniki = df[df['Nazwa'].str.lower().str.contains(pattern, regex=True)]
            if not wyniki.empty:
                for nazwa in wyniki['Nazwa']:
                    lista_wynikow.controls.append(ft.Text(nazwa))
            else:
                lista_wynikow.controls.append(ft.Text("❌ Brak pasujących wyników"))
        else:
            lista_wynikow.controls.append(ft.Text("ℹ️ Wpisz co najmniej 1 literę"))

        page.update()


    pole = ft.TextField(
        label="🔍 Wpisz nazwę zajęć",
        hint_text="np. 'joga', 'gimnastyka', 'wolontariat'",
        on_change=aktualizuj_wyniki,
        expand=True,
        width=400,
    )

    lista_wynikow.controls.append(info_text)

    content = ft.Column([
        ft.Row(
            controls=[sort_button],
            alignment=ft.MainAxisAlignment.END,
            expand=True,
        ),
        pole,
        lista_wynikow
    ], expand=True, scroll="auto")

    return ft.View(
        "/search",
        [
            ft.AppBar(
                title=ft.Text("Wyszukiwarka zajęć"),
                leading=ft.TextButton("⬅", on_click=lambda e: page.go("/")),
                bgcolor=ft.Colors.SURFACE,
            ),
            content,
        ]
    )

def lista_view(page: ft.Page):
    import pandas as pd
    import re
    import flet as ft

    df = pd.read_excel("CAS_data.xlsx", sheet_name="Classes")
    df["Opis"] = df["Opis"].fillna("")

    opisy_zajec = {
        "Kurs historii sztuki": "Poznaj fascynujący świat sztuki od starożytności po współczesność. Naucz się rozpoznawać style i techniki artystyczne. Spotkania pełne inspirujących przykładów i ciekawostek. Doskonała okazja, by rozwijać pasję i poszerzać wiedzę.",
        "Aqua aerobic ": "Ćwiczenia w wodzie, które wzmacniają mięśnie i poprawiają kondycję bez nadmiernego obciążenia stawów. Idealne dla osób w każdym wieku, szczególnie tych dbających o zdrowie i mobilność. Zajęcia łączą przyjemność z efektywnym treningiem. Poprawiają krążenie i samopoczucie.",
        "Wycieczka jednodniowa do Muszyny": "Spędź aktywny dzień na zwiedzaniu malowniczej Muszyny i jej okolic. To doskonała okazja do poznania historii, kultury i przyrody regionu. Wspólna podróż sprzyja integracji i relaksowi na świeżym powietrzu. Zadbaj o swoje ciało i umysł w miłym towarzystwie.",
        "Joga dla seniorow": "Łagodne ćwiczenia rozciągające i wzmacniające ciało, dostosowane do potrzeb seniorów. Pomagają poprawić równowagę, elastyczność i relaksację. Zajęcia prowadzone w spokojnej, przyjaznej atmosferze. Doskonały sposób na poprawę zdrowia i samopoczucia.",
        "Gry stolikowe/planszowe": "Spotkania przy grach towarzyskich, które rozwijają logiczne myślenie i integrują uczestników. Poznasz nowe gry oraz przypomnisz sobie klasyki planszówek. Zabawa i rozmowy tworzą przyjemną atmosferę. Idealne na spędzenie czasu z innymi i ćwiczenie umysłu.",
        "Zajęcia sportowo-ruchowe": "Proste ćwiczenia poprawiające koordynację, równowagę i ogólną sprawność fizyczną. Dedykowane osobom chcącym utrzymać dobrą kondycję i zdrowie. Zajęcia dostosowane do indywidualnych możliwości uczestników. Zwiększają energię i pomagają zapobiegać kontuzjom.",
        "J. angielski – poziom podstawowy": "Podstawowe lekcje języka angielskiego skupiające się na codziennej komunikacji. Nauczysz się przydatnych zwrotów i prostych struktur gramatycznych. Zajęcia prowadzone w przyjaznej atmosferze, sprzyjającej nauce. Otwórz drzwi do podróży i nowych znajomości.",
        "Nowe technologie": "Dowiedz się, jak efektywnie korzystać ze smartfonów, komputerów i internetu. Poznasz praktyczne porady i przydatne aplikacje ułatwiające codzienne życie. Zajęcia prowadzone krok po kroku, dostosowane do potrzeb początkujących. Zyskaj pewność w cyfrowym świecie.",
        "Wolontariat": "Zaangażuj się w działania na rzecz lokalnej społeczności i pomagaj innym. To szansa na poznanie ciekawych ludzi i zdobycie nowych doświadczeń. Rozwijaj swoje umiejętności interpersonalne i organizacyjne. Poczuj satysfakcję z niesienia pomocy.",
        "Gimanstyka rehabilitacyjna": "Bezpieczne ćwiczenia mające na celu poprawę sprawności i łagodzenie dolegliwości. Pomagają wzmocnić mięśnie i zwiększyć zakres ruchu. Zajęcia prowadzone pod okiem doświadczonych instruktorów. Idealne wsparcie w procesie rehabilitacji.",
        "Zajęcia plastyczne z elementami rękodzieła": "Twórz własnoręcznie piękne prace i rozwijaj kreatywność. Poznasz różnorodne techniki artystyczne i rękodzielnicze. Zajęcia sprzyjają relaksowi i integracji uczestników. Doskonały sposób na wyrażenie siebie poprzez sztukę.",
        "Gimnastyka": "Łagodne ćwiczenia ruchowe poprawiające kondycję i samopoczucie. Dostosowane do różnych poziomów sprawności uczestników. Pomagają zwiększyć energię i poprawić elastyczność ciała. Spędź aktywnie czas w miłej atmosferze.",
        "Kurs obsługi smartfonów": "Naucz się obsługi smartfona od podstaw i korzystaj z jego możliwości. Poznasz praktyczne funkcje i przydatne aplikacje. Zajęcia prowadzone krok po kroku, dostosowane do potrzeb początkujących. Ułatw sobie kontakt z rodziną i światem.",
        "Gry stolikowe, brydż": "Spotkania dla miłośników gier planszowych i brydża, rozwijające strategiczne myślenie. Poznasz zasady i strategie gier, które pobudzają umysł. Czas spędzony w dobrym towarzystwie i przyjemnej atmosferze. Doskonały sposób na ćwiczenie koncentracji i pamięci.",
    }

    pole = ft.TextField(
        label="🔍 Wpisz nazwę zajęć",
        hint_text="np. 'joga', 'gimnastyka', 'wolontariat'",
        width=400,
    )

    lista_zajec = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=15,
        width=400,
        height=500,
        scroll="auto",
    )

    def pokaz_opis(nazwa):
        opis = opisy_zajec.get(nazwa, "Brak opisu dla tych zajęć.")


        df_cas = pd.read_excel("CAS_data.xlsx", sheet_name="CAS_OpenData")
        df_zajecia = df[df["Nazwa"] == nazwa]

        dostepnosc = df_zajecia.merge(
            df_cas, left_on="Id_CAS", right_on="Lp", how="left", suffixes=("_zajecia", "_cas")
        )

        lista_dostepnosci = []
        if dostepnosc.empty:
            lista_dostepnosci.append(ft.Text("❌ Brak dostępnych zajęć w CAS."))
        else:
            for _, row in dostepnosc.iterrows():
                cas_info = ft.Column(
                    [
                        ft.Text(f"🏠 {row['Nazwa_cas']}", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(row.get("Adres", "Adres niedostępny"), size=14, color=ft.Colors.GREY_700),
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START,
                )

                cas_container = ft.Container(
                    content=ft.Row(
                        controls=[cas_info],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=10,
                    margin=ft.margin.symmetric(vertical=5),
                    border_radius=10,
                    bgcolor=ft.Colors.SURFACE,
                    border=ft.border.all(2, ft.Colors.BLUE_900),
                    expand=True,
                )

                lista_dostepnosci.append(cas_container)

        page.views.append(
            ft.View(
                "/opis",
                controls=[
                    ft.AppBar(
                        title=ft.Text("Szczegóły zajęć"),
                        leading=ft.TextButton("⬅", on_click=lambda _: page.go("/lista")),
                    ),
                    ft.Column([
                        ft.Text(nazwa, size=24, weight=ft.FontWeight.BOLD),
                        ft.Text(opis, size=16),
                        ft.Divider(),
                        ft.Text("Dostępność zajęć", size=20, weight=ft.FontWeight.BOLD),
                        ft.Column(lista_dostepnosci, spacing=10, scroll="auto")
                    ], spacing=20, expand=True, scroll="auto")
                ]
            )
        )
        page.go("/opis")

    def render_lista(df_filtered):
        lista_zajec.controls.clear()
        if df_filtered.empty:
            lista_zajec.controls.append(ft.Text("❌ Brak pasujących wyników"))
        else:
            for kat, grupa in df_filtered.groupby("Kategoria"):
                lista_zajec.controls.append(ft.Text(kat, size=20, weight=ft.FontWeight.BOLD))
                unik = set()
                for _, r in grupa.iterrows():
                    if r["Nazwa"] not in unik:
                        unik.add(r["Nazwa"])
                        lista_zajec.controls.append(
                            ft.TextButton(
                                r["Nazwa"],
                                on_click=lambda e, nazwa=r["Nazwa"]: pokaz_opis(nazwa),
                                style=ft.ButtonStyle(color=ft.Colors.BLUE_700),
                            )
                        )

    def pokaz_wszystkie():
        render_lista(df)

    def aktualizuj(e):
        fraza = pole.value.strip().lower()
        if len(fraza) >= 1:
            pattern = rf"\b{re.escape(fraza)}"
            wyniki = df[
                df["Nazwa"].str.lower().str.contains(pattern, regex=True) |
                df["Kategoria"].str.lower().str.contains(pattern, regex=True)
            ]
            render_lista(wyniki)
        else:
            pokaz_wszystkie()
        page.update()

    pole.on_change = aktualizuj

    pokaz_wszystkie()

    return ft.View(
        "/lista",
        controls=[
            ft.AppBar(
                title=ft.Text("Lista oferowanych zajęć"),
                leading=ft.TextButton("⬅", on_click=lambda e: page.go("/")),
            ),
            ft.Column([
                pole,
                lista_zajec,
            ], expand=True,
               alignment=ft.MainAxisAlignment.START,
               horizontal_alignment=ft.CrossAxisAlignment.START),
        ]
    )

def cas_view(page: ft.Page):
    df_coords = pd.read_excel("CAS_wspolrzedne2.xlsx")
    df_info = pd.read_csv("CAS_Otwarte_Dane.csv")
    df_merged = pd.merge(df_coords, df_info[["Lp", "Nazwa"]], on="Lp", how="left")

    # Animacja Lottie:
    animation = Lottie(
        "https://lottie.host/60990b8f-4ee9-460f-94ed-c8be8d382394/qAxulYH8FG.json",
        width=300,
        height=300,
        repeat=True,
        animate=True,
    )
    animation_container = ft.Container(
        content=animation,
        width=300,
        height=300,
        padding=5,
        border=ft.border.all(1, ft.Colors.BLACK12),
        border_radius=10,
    )

    address_input = ft.TextField(label="🔍 Podaj swój adres", width=400, expand=True)
    results_column = ft.Column(scroll="auto", expand=True)

    def show_all_cas():
        results_column.controls.clear()
        for i, row in enumerate(df_merged.itertuples(), start=1):
            number_text = ft.Text(f"{i}", width=20)
            cas_info = ft.Column([
                ft.Text(row.Nazwa, size=18, weight=ft.FontWeight.W_500),
                ft.Text(getattr(row, "Adres_uzyty", ""), size=14, color=ft.Colors.BLACK54),
            ], spacing=4, expand=True)

            cas_container = ft.Container(
                content=ft.Row(
                    controls=[number_text, cas_info],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=10,
                margin=ft.margin.symmetric(vertical=5),
                border_radius=10,
                bgcolor=ft.Colors.SURFACE,
                border=ft.border.all(2, ft.Colors.BLUE_900),
                expand=True,
            )
            results_column.controls.append(cas_container)

        page.update()

    def find_cas(e):
        results_column.controls.clear()
        user_address = address_input.value.strip()

        if not user_address:
            results_column.controls.append(ft.Text("❌ Podaj adres!", color="red"))
            page.update()
            return

        lat_user, lon_user = geocode_address(user_address)

        if lat_user is None or lon_user is None:
            results_column.controls.append(ft.Text("❌ Nie udało się pobrać współrzędnych.", color="red"))
            page.update()
            return

        results = []
        for row in df_merged.itertuples():
            lat_cas = getattr(row, "Latitude", None)
            lon_cas = getattr(row, "Longitude", None)

            if pd.notna(lat_cas) and pd.notna(lon_cas):
                distance_m = geodesic((lat_user, lon_user), (lat_cas, lon_cas)).meters
            else:
                distance_m = None

            results.append({
                "Lp": row.Lp,
                "Nazwa": row.Nazwa,
                "Adres_uzyty": getattr(row, "Adres_uzyty", ""),
                "Distance_m": distance_m
            })

        results_df = pd.DataFrame(results)
        results_df = results_df.dropna(subset=["Distance_m"]).sort_values(by="Distance_m")

        if results_df.empty:
            results_column.controls.append(ft.Text("❌ Brak wyników do wyświetlenia.", color="red"))
        else:
            for i, row in enumerate(results_df.itertuples(), start=1):
                number_text = ft.Text(f"{i}", width=20)
                cas_info = ft.Column([
                    ft.Text(row.Nazwa, size=18, weight=ft.FontWeight.W_500),
                    ft.Text(row.Adres_uzyty, size=14, color=ft.Colors.BLACK54),
                    ft.Text(f"Odległość {round(row.Distance_m, 1)} m", size=12, color=ft.Colors.BLACK45),
                ], spacing=4, expand=True)

                cas_container = ft.Container(
                    content=ft.Row(
                        controls=[number_text, cas_info],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=10,
                    margin=ft.margin.symmetric(vertical=5),
                    border_radius=10,
                    bgcolor=ft.Colors.SURFACE,
                    border=ft.border.all(2, ft.Colors.BLUE_900),
                    expand=True,
                )
                results_column.controls.append(cas_container)

        page.update()

    search_button = ft.ElevatedButton("Znajdź CAS", on_click=find_cas)

    input_row = ft.Row(
        controls=[address_input, search_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        expand=True,
    )

    content = ft.Column([
        ft.Row([animation_container], alignment=ft.MainAxisAlignment.CENTER),
        input_row,
        ft.Divider(),
        results_column,
        ft.Divider(),
    ], expand=True, scroll="auto")

    show_all_cas()

    return ft.View(
        "/cas",
        [
            ft.AppBar(
                title=ft.Text("Centra Aktywności Seniora"),
                leading=ft.TextButton("⬅", on_click=lambda e: page.go("/")),
                bgcolor=ft.Colors.SURFACE,
            ),
            content
        ]
    )


def main(page: ft.Page):
    page.title = "Centrum Aktywności Seniora"
    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(e):
        if page.route == "/":
            page.views.clear()
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            expand=True,
                            controls=[
                                ft.Column(
                                    [
                                        ft.Image(src="logo.png", width=200, height=200),
                                        ft.ElevatedButton(
                                            content=ft.Column([
                                                ft.Text("Wyszukaj zajęcia", size=18, weight=ft.FontWeight.BOLD),
                                                ft.Text(
                                                    "Wyszukaj zajęcia we wszystkich ośrodkach aktywności seniora w Krakowie",
                                                    size=12, color=ft.Colors.BLACK54),
                                            ],
                                                spacing=2,
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            width=300,
                                            height=90,
                                            on_click=lambda e: page.go("/zajecia"),
                                        ),
                                        ft.ElevatedButton(
                                            content=ft.Column([
                                                ft.Text("Lista oferowanych zajęć", size=18, weight=ft.FontWeight.BOLD),
                                                ft.Text("Pokaż listę wszystkich oferowanych zajęć",
                                                        size=12, color=ft.Colors.BLACK54),
                                            ],
                                                spacing=2,
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            width=300,
                                            height=90,
                                            on_click=lambda e: page.go("/lista"),
                                        ),
                                        ft.ElevatedButton(
                                            content=ft.Column([
                                                ft.Text("Centra Aktywności Seniora", size=18, weight=ft.FontWeight.BOLD),
                                                ft.Text("Pokaż listę wszystkich placówek w Krakowie",
                                                        size=12, color=ft.Colors.BLACK54),
                                            ],
                                                spacing=2,
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            width=300,
                                            height=90,
                                            on_click=lambda e: page.go("/cas"),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=25,
                                )
                            ]
                        )
                    ],
                )
            )
        elif page.route == "/cas":
            page.views.clear()
            page.views.append(cas_view(page))
        elif page.route == "/zajecia":
            page.views.clear()
            page.views.append(search_view(page))
        elif page.route == "/lista":
            page.views.clear()
            page.views.append(lista_view(page))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


ft.app(target=main)