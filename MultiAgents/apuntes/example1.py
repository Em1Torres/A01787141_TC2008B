
tempValues = [29,30,31,30,29,25]


def fanStatus(tv):
    fan = False
    room_temperature = 0
    for i in tv:
        room_temperature = i
        if room_temperature >= 30:
            fan = True
            print(fan)
        else:
            fan = False
            print(fan)


fanStatus(tempValues)
