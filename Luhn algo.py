import secrets
import string
def check_card_number(card_number):


    card_digits = []
    print(card_number)
    print(len(card_number))
    counter = 0
    sum_card_numbers = 0
    number_ = 0
    for s in range(len(card_number)-1):
        card_digits.append(int(card_number[s]))

    print(card_digits)
    while counter < len(card_digits):
        card_digits[counter] *= 2
        if card_digits[counter] > 9:
            card_digits[counter] -= 9
        counter += 2

    print(card_digits)

    while number_ < len(card_digits):
        sum_card_numbers += card_digits[number_]
        number_ += 1

    print(sum_card_numbers)
    print(card_digits[-1])
    if(sum_card_numbers + int(card_number[-1])) % 10 == 0:
        return True
    else:
        return False


a = (str(400000)+str(''.join(secrets.choice(string.digits) for x in range(10))))
print(check_card_number(a))
