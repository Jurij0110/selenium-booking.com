from booking.booking import Booking

with Booking() as bot:
    bot.land_first_page()
    bot.change_currency(currency='VND')
    bot.select_place_to_go('New York')
    bot.select_dates(checkin_date="2025-05-02",checkout_date="2025-05-04")
    bot.select_adults(number_adults=5)
    bot.submit()
    bot.apply_filtrations()
    bot.refresh()
    # print(len(bot.report_results()))
    bot.report_results()