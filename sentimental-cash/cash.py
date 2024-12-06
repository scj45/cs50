from cs50 import get_float


while True:
    change = get_float("Change: ")  # ask user for change in dollars
    if change > 0:  # change has to be more than 0
        break


def calculate_quarters(change):
    quarters = 0
    while (change >= 25):
        quarters += 1
        change = change - 25
    return quarters


def calculate_dimes(change):
    dimes = 0
    while (change >= 10):
        dimes += 1
        change = change - 10
    return dimes


def calculate_nickels(change):
    nickels = 0
    while (change >= 5):
        nickels += 1
        change = change - 5
    return nickels


def calculate_pennies(change):
    pennies = 0
    while (change >= 1):
        pennies += 1
        change = change - 1
    return pennies


change = change * 100

quarters = calculate_quarters(change)  # how many quarters
change = change - (quarters * 25)  # subtract value of quarters

dimes = calculate_dimes(change)  # how many dimes
change = change - (dimes * 10)  # subtract value of dimes

nickels = calculate_nickels(change)  # how many nickels
change = change - (nickels * 5)  # subtract value of nickels

pennies = calculate_pennies(change)  # how many dimes
change = change - (pennies * 1)  # subtract value of dimes

coins = quarters + dimes + nickels + pennies
print(coins)
