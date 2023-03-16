from booking.booking import Booking

with Booking() as bot:
    bot.land_first_page()
    bot.change_currency(currency = "VND")
    bot.select_place_to_go("Vung Tau")
    bot.select_dates(check_in_date="2023-03-29", check_out_date="2023-03-30")
    bot.select_adults(count=2)
    bot.click_search()

    bot.report_results()
