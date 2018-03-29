def map_element_to_colour(element:str):
    if element.lower() == "power":
        return 0xff0000
    elif element.lower() == "speed":
        return 0x00ff00
    elif element.lower() == "magic":
        return 0x0000ff
