import flet as ft
import datetime
import search_engine_many_categories
from dateutil.relativedelta import relativedelta
import sys
#Category
CategoriesSelected = [["Zajęcia edukacyjne","Aktywność fizyczna","Twórczość i hobby","Integracja i wycieczki"], [1,1,1,1]]

#Price
MinPrice = 0
MaxPrice = 100000

#
SelectedDay = datetime.date.today() - relativedelta(months=3)
SelectedHour = 0

TypesSelected = [["Stacjonarny","Online"], [1,1]]

ActivitiesSearched = []




def print_categories_selected(categories_selected):
    print("CategoriesSelected:")
    for label, selected in zip(categories_selected[0], categories_selected[1]):
        print(f" - {label}: {'Selected' if selected == 1 else 'Not selected'}")

def main(page: ft.Page):
    page.title = "Sortuj wyniki wedlug"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def close_function(e):
        page.window.destroy()

    def open_facility(e):
        page.clean()
        back_button = ft.ElevatedButton("Wróć", on_click=go_back)
        page.add(back_button)

    def open_activity(e):
        page.clean()

        options = search_engine_many_categories.CategorieList
        checkboxes = [ft.Checkbox(label=opt, value=False) for opt in options]

        selected_text = ft.Text("")

        def on_confirm(e):


            CategoriesSelected[0] = [cb.label for cb in checkboxes]
            CategoriesSelected[1] = [1 if cb.value else 0 for cb in checkboxes]

            selected = [cb.label for cb in checkboxes if cb.value]

            page.update()

        back_button = ft.ElevatedButton("Wróc", on_click=go_back)
        confirm_button = ft.ElevatedButton("Potwierdz wybór", on_click=on_confirm)

        page.add(
            ft.Text("Wybierz jedną lub wiele kategorii:", size=30, weight="bold"),
            *checkboxes,
            confirm_button,
            selected_text,
            back_button,
        )

    def open_day(e):
        selected_text = ft.Text("")
        pickedDay = datetime.date.today()

        def pickDay(day):
            nonlocal pickedDay
            pickedDay = day
            selected_text.value = f"Wybrano dzień: {pickedDay.strftime('%Y-%m-%d')}"
            page.update()
            global SelectedDay
            SelectedDay = pickedDay

        page.clean()
        buttons = []
        today = datetime.date.today()
        for i in range(7):
            day = today + datetime.timedelta(days=i)
            # Use lambda to capture current day value in the loop
            buttons.append(ft.ElevatedButton(str(day), on_click=lambda e, d=day: pickDay(d)))
        #any day
        today + datetime.timedelta(days=i)
   #     buttons.append(ft.ElevatedButton(str(day), on_click=lambda e, d=day: pickDay(d)))
        page.add(
            ft.Text("Wybierz dzień po którym pokazać kategoire:", size=30),
            selected_text,
            ft.Row(buttons, spacing=10),
            ft.ElevatedButton("Wróc", on_click=go_back)
        )

    def open_hour(e):
        page.clean()
        selected_text = ft.Text("")
        buttons = []
        buttons1 = []
        buttons2 = []
        pickedHour = datetime.datetime.now().hour

        def pickHour(hour):
            nonlocal pickedHour
            pickedHour = hour
            selected_text.value = f"Wybrano godzine: {pickedHour}"
            page.update()
            global SelectedHour
            SelectedHour = pickedHour

        for i in range(24):
            buttons.append(ft.ElevatedButton(str(i),on_click=lambda e, h=i: pickHour(h)))

        for i in range(0, 12):
            buttons1.append(buttons[i])
        for i in range(12, 24):
            buttons2.append(buttons[i])
        page.add(
            ft.Text("Wybierz Godzine:", size=30),
            selected_text,
            ft.Row(buttons1, spacing=10),
            ft.Row(buttons2, spacing=10),
            ft.ElevatedButton("Wróc", on_click=go_back)
        )

    def open_mode(e):
        page.clean()

        options = ["Stacjonarne", "Zdalne"]
        checkboxes = [ft.Checkbox(label=opt, value=False) for opt in options]

        selected_text = ft.Text("")

        def on_confirm(e):


            TypesSelected[0] = [cb.label for cb in checkboxes]
            TypesSelected[1] = [1 if cb.value else 0 for cb in checkboxes]

            selected = [cb.label for cb in checkboxes if cb.value]

            page.update()

        back_button = ft.ElevatedButton("Wróc", on_click=go_back)
        confirm_button = ft.ElevatedButton("Potwierdz wybór", on_click=on_confirm)

        page.add(
            ft.Text("Wybierz tryb stacjonarny lub online:", size=30, weight="bold"),
            *checkboxes,
            confirm_button,
            selected_text,
            back_button,
        )

    def cena_sort(e):
        page.clean()

        min_price = ft.TextField(label="Minimalna cena", width=200, keyboard_type=ft.KeyboardType.NUMBER)
        max_price = ft.TextField(label="Maksymalna cena", width=200, keyboard_type=ft.KeyboardType.NUMBER)
        result_text = ft.Text("")

        def on_confirm(e):
            global MinPrice
            MinPrice = min_price.value.strip()
            global MaxPrice
            MaxPrice = max_price.value.strip()

            if MinPrice == "":
                MinPrice = "0"
            if MaxPrice == "":
                MaxPrice = "Brak limitu"

            result_text.value = f"Wybrano zakres cen: {MinPrice} - {MaxPrice}"
            page.update()

        confirm_button = ft.ElevatedButton("Potwierdź", on_click=on_confirm)
        back_button = ft.ElevatedButton("Wróć", on_click=go_back)

        page.add(
            ft.Text("Podaj zakres cen:", size=30, weight="bold"),
            min_price,
            max_price,
            confirm_button,
            result_text,
            back_button,
        )

    def go_back(e):
        page.clean()
        page.add(title,activity_button,facility_button, category_button,day_button,hour_button,on_off_site_button,price_button,search_button,close_button)

    def open_search(e):
        page.clean()

        results = search_engine_many_categories.SearchZajeciaByManyParameters(
            CategoriesSelected, MinPrice, MaxPrice, SelectedDay, SelectedHour, TypesSelected
        )

        # Scrollable list of buttons
        lv = ft.ListView(expand=1, spacing=8, padding=0, auto_scroll=False)

        for Activities in results:
            lv.controls.append(
                ft.ElevatedButton(
                    str(Activities.return_string()),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.all(12),
                    ),
                )
            )

        back_button = ft.ElevatedButton("Wróć", on_click=go_back)

        # Keep the back button visible below the scrollable list
        page.add(
            ft.Column(
                controls=[lv, back_button],
                expand=True,
                spacing=8,
            )
        )

        page.update()



    title = ft.Text("Sortuj wyniki według", size=40, weight="bold")
    activity_button = ft.ElevatedButton("Zajęcia", on_click=open_day)
    facility_button = ft.ElevatedButton("Ośrodek", on_click=open_facility)
    category_button = ft.ElevatedButton("Kategoria", on_click=open_activity)
    day_button = ft.ElevatedButton("Dzień", on_click=open_day)
    hour_button = ft.ElevatedButton("Godzina", on_click=open_hour)
    on_off_site_button = ft.ElevatedButton("Tryb", on_click=open_mode)
    price_button = ft.ElevatedButton("Cena", on_click=cena_sort)
    search_button = ft.ElevatedButton("wyszukaj", on_click=open_search)
    close_button = ft.ElevatedButton("wyjdz", on_click=close_function)
    page.add(title,activity_button,facility_button, category_button,day_button,hour_button,on_off_site_button,price_button,search_button,close_button)

if __name__ == "__main__":
    ft.app(target=main)
