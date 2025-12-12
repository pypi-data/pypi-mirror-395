"""
A simple currency conversion library for:
USD, BDT, EUR, JPY, NPR, UZS.

Author: Your Name
"""

# 1. Dictionary to store exchange rates
#    All rates are relative to 1 USD.
EXCHANGE_RATES = {
    "USD": 1.0,     # 1 USD = 1 USD
    "BDT": 110.0,   # example: 1 USD = 110 Bangladeshi Taka
    "EUR": 0.92,    # example: 1 USD = 0.92 Euro
    "JPY": 150.0,   # example: 1 USD = 150 Japanese Yen
    "NPR": 133.0,   # example: 1 USD = 133 Nepalese Rupee
    "UZS": 12600.0  # example: 1 USD = 12,600 Uzbekistan Som
}


def get_supported_currencies():
    """
    Return a list of all supported currency codes.
    """
    return list(EXCHANGE_RATES.keys())


def is_supported_currency(code):
    """
    Check if a currency code is supported by the library.

    Parameters:
        code (str): Currency code like "USD" or "BDT".

    Returns:
        bool: True if supported, False otherwise.
    """
    return code in EXCHANGE_RATES


def convert_to_usd(amount, from_currency):
    """
    Convert from any supported currency to USD.

    Parameters:
        amount (float): Amount of money in from_currency.
        from_currency (str): Currency code of the amount.

    Returns:
        float: Equivalent amount in USD.

    Raises:
        ValueError: If the currency code is not supported
                    or the amount is negative.
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative.")

    if not is_supported_currency(from_currency):
        raise ValueError(f"Unsupported currency: {from_currency}")

    rate = EXCHANGE_RATES[from_currency]

    # Since EXCHANGE_RATES is "how much of this currency equals 1 USD",
    # to get USD, we divide by the rate.
    amount_in_usd = amount / rate
    return amount_in_usd


def convert_from_usd(amount_usd, to_currency):
    """
    Convert an amount in USD to another currency.

    Parameters:
        amount_usd (float): Amount in USD.
        to_currency (str): Target currency code.

    Returns:
        float: Equivalent amount in target currency.

    Raises:
        ValueError: If currency code is not supported
                    or the amount is negative.
    """
    if amount_usd < 0:
        raise ValueError("Amount cannot be negative.")

    if not is_supported_currency(to_currency):
        raise ValueError(f"Unsupported currency: {to_currency}")

    rate = EXCHANGE_RATES[to_currency]

    # To go from USD to another currency, multiply.
    result = amount_usd * rate
    return result


def convert(amount, from_currency, to_currency):
    """
    Convert an amount from one currency directly to another.

    Parameters:
        amount (float): Amount of money in from_currency.
        from_currency (str): Currency code to convert from.
        to_currency (str): Currency code to convert to.

    Returns:
        float: Equivalent amount in to_currency.

    Raises:
        ValueError: If any currency code is not supported
                    or the amount is negative.
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative.")

    if not is_supported_currency(from_currency):
        raise ValueError(f"Unsupported currency: {from_currency}")

    if not is_supported_currency(to_currency):
        raise ValueError(f"Unsupported currency: {to_currency}")

    # Step 1: convert from 'from_currency' to USD
    amount_in_usd = convert_to_usd(amount, from_currency)

    # Step 2: convert from USD to 'to_currency'
    converted_amount = convert_from_usd(amount_in_usd, to_currency)

    return converted_amount


def print_supported_currencies():
    """
    Print all supported currencies in a friendly way.
    """
    print("Supported currencies:")
    for code in get_supported_currencies():
        print(f"- {code}")


# Only run this interactive part when the file is executed directly,
# not when it is imported as a library.
if __name__ == "__main__":
    print("Simple Currency Converter Library Demo")
    print_supported_currencies()

    try:
        # Ask user for details
        from_code = input("Enter FROM currency code (e.g., USD): ").strip().upper()
        to_code = input("Enter TO currency code (e.g., EUR): ").strip().upper()
        amount_str = input("Enter amount: ").strip()

        amount_value = float(amount_str)

        result = convert(amount_value, from_code, to_code)
        print(f"{amount_value} {from_code} = {result:.2f} {to_code}")

    except ValueError as ve:
        print("Error:", ve)
    except Exception as e:
        print("Unexpected error:", e)



