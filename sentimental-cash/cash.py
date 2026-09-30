from cs50 import get_float

# Ask for change owed
while True:
    dollars = get_float("Change owed: ")
    if dollars > 0:
        break

# Rounding cents & dollars
dollars = round(dollars * 100)

# Calculate the number of all coins to give the customer
quarters = 0
while dollars >= 25:
    dollars = dollars - 25
    quarters += 1

dimes = 0
while dollars >= 10:
    dollars = dollars - 10
    dimes += 1

nickels = 0
while dollars >= 5:
    dollars = dollars - 5
    nickels += 1

pennies = 0
while dollars >= 1:
    dollars = dollars - 1
    pennies += 1

# Coins total
total_coins = quarters + dimes + nickels + pennies

# Print total amount of coins
print(total_coins)