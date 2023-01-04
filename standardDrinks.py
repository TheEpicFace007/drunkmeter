def calculate_standard_drink(abv, volume, gender, weight=70, height=170):
    """
    Calculate the number of standard drink in a drink according to the WHO
    """
    return round(abv * volume / 1000, 2)
