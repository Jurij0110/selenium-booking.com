from booking.booking import Booking

with Booking() as bot:
    bot.land_first_page()
    bot.change_currency(currency='VND')
    # bot.select_place_to_go(input("Where you want to go? "))
    bot.select_place_to_go('Da Nang')
    # bot.select_dates(checkin_date = input("What is the check-in date?"),
    #                  checkout_date = input("What is the check-out date?"))
    bot.select_dates(checkin_date="2025-05-02", checkout_date="2025-05-04")
    bot.select_adults(number_adults=5)
    bot.submit()
    bot.apply_filtrations()
    bot.refresh()
    # print(len(bot.report_results()))
    bot.report_results()