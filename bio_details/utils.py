from .models import Currency

def number_to_words(amount, currency_code="INR"):
    """Convert number to words using DB currency"""

    # Get currency from DB
    try:
        currency_obj = Currency.objects.get(code=currency_code)
        currency_name = currency_obj.currency_name  # India, USA
    except Currency.DoesNotExist:
        currency_name = "Rupees"

    if amount == 0:
        return f"Zero {currency_name} Only"

    amount = int(float(amount))

    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
            "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
            "Seventeen", "Eighteen", "Nineteen"]

    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    def convert_hundreds(n):
        result = ""
        if n >= 100:
            result += ones[n // 100] + " Hundred "
            n %= 100
        if n >= 20:
            result += tens[n // 10] + " "
            n %= 10
        if n > 0:
            result += ones[n] + " "
        return result

    def convert_number(num):
        result = ""

        if num >= 10000000:
            result += convert_hundreds(num // 10000000) + "Crore "
            num %= 10000000

        if num >= 100000:
            result += convert_hundreds(num // 100000) + "Lakh "
            num %= 100000

        if num >= 1000:
            result += convert_hundreds(num // 1000) + "Thousand "
            num %= 1000

        if num > 0:
            result += convert_hundreds(num)

        return result.strip()

    words = convert_number(amount)
    return f"{words} {currency_name} Only"