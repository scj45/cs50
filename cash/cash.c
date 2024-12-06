#include <cs50.h>
#include <stdio.h>

int calculate_quarters(int change);
int calculate_dimes(int change);
int calculate_nickels(int change);
int calculate_pennies(int change);

int main(void)
{
    // Prompt for change owed in cents
    int change;
    do
    {
        change = get_int("Amount of change owed, in cents: ");
    }
    while (change < 0);

    // How many quarters
    int quarters = calculate_quarters(change);
    // Subtract the value of the quarters
    change = change - (quarters * 25);

    // How many dimes
    int dimes = calculate_dimes(change);
    // Subtract the value of the dimes
    change = change - (dimes * 10);

    // How many nickels
    int nickels = calculate_nickels(change);
    // Subtract the value of the nickels
    change = change - (nickels * 5);

    // How many pennies
    int pennies = calculate_pennies(change);
    // Subtract the value of the pennies
    change = change - (pennies * 1);

    // Add up coins used
    int coins = quarters + dimes + nickels + pennies;

    // Print sum
    printf("%i\n", coins);
}

int calculate_quarters(int change)
{
    // Divide by 25c
    int quarters = 0;
    while (change >= 25)
    {
        quarters++;
        change = change - 25;
    }
    return quarters;
}

int calculate_dimes(int change)
{
    // Divide remainder by 10c
    int dimes = 0;
    while (change >= 10)
    {
        dimes++;
        change = change - 10;
    }
    return dimes;
}

int calculate_nickels(int change)
{
    // Divide remainder by 5c
    int nickels = 0;
    while (change >= 5)
    {
        nickels++;
        change = change - 5;
    }
    return nickels;
}

int calculate_pennies(int change)
{
    // Divide remainder by 1c
    int pennies = 0;
    while (change >= 1)
    {
        pennies++;
        change = change - 1;
    }
    return pennies;
}
