def calculate_standard_drink(abv, volume):
    """
    Calculate the number of standard drink in a drink according to the WHO
    """
    return round(abv * volume / 1000, 2)
