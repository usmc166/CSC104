from decimal import Decimal, ROUND_HALF_UP


def money(value):
    """Return a currency value rounded to the nearest cent."""
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def monthly_payment(principal, annual_rate, years):
    """Calculate the fixed monthly payment for a standard amortized loan."""
    principal = Decimal(str(principal))
    annual_rate = Decimal(str(annual_rate))
    years = Decimal(str(years))

    if principal <= 0:
        raise ValueError("Principal must be greater than zero.")
    if years <= 0:
        raise ValueError("Years must be greater than zero.")

    monthly_rate = annual_rate / Decimal("100") / Decimal("12")
    total_payments = years * Decimal("12")

    if monthly_rate == 0:
        return principal / total_payments

    return (
        principal
        * (monthly_rate * ((1 + monthly_rate) ** total_payments))
        / (((1 + monthly_rate) ** total_payments) - 1)
    )


def total_paid(principal, annual_rate, years):
    """Return the total amount paid over the life of the loan."""
    payment = monthly_payment(principal, annual_rate, years)
    return payment * (Decimal(str(years)) * Decimal("12"))


def total_interest(principal, annual_rate, years):
    """Return the total interest paid for the loan."""
    return total_paid(principal, annual_rate, years) - Decimal(str(principal))


def loan_summary(principal, annual_rate, years):
    """Return a dictionary containing the main loan figures."""
    principal = Decimal(str(principal))
    annual_rate = Decimal(str(annual_rate))
    years = Decimal(str(years))

    payment = monthly_payment(principal, annual_rate, years)
    total = total_paid(principal, annual_rate, years)
    interest = total - principal

    return {
        "principal": money(principal),
        "annual_rate": annual_rate,
        "years": years,
        "monthly_payment": money(payment),
        "total_paid": money(total),
        "total_interest": money(interest),
    }


def payment_schedule(principal, annual_rate, years):
    """Return a list of monthly payment details for each month of the loan."""
    principal = Decimal(str(principal))
    annual_rate = Decimal(str(annual_rate))
    years = Decimal(str(years))

    monthly_rate = annual_rate / Decimal("100") / Decimal("12")
    payment_amount = monthly_payment(principal, annual_rate, years)
    remaining_balance = principal
    schedule = []

    total_months = int(years * 12)

    for month in range(1, total_months + 1):
        interest_paid = remaining_balance * monthly_rate
        principal_paid = payment_amount - interest_paid

        if principal_paid > remaining_balance:
            principal_paid = remaining_balance
            payment_amount = remaining_balance + interest_paid

        remaining_balance -= principal_paid

        if remaining_balance < 0:
            remaining_balance = Decimal("0.00")

        schedule.append(
            {
                "month": month,
                "balance_before": money(remaining_balance + principal_paid),
                "payment": money(payment_amount),
                "interest": money(interest_paid),
                "principal": money(principal_paid),
                "balance_after": money(remaining_balance),
            }
        )

        if remaining_balance == 0:
            break

    return schedule


def yearly_summary(principal, annual_rate, years):
    """Return a year-by-year breakdown of the loan's payments."""
    schedule = payment_schedule(principal, annual_rate, years)
    yearly_rows = []

    total_years = int(Decimal(str(years)))

    for year in range(1, total_years + 1):
        start_index = (year - 1) * 12
        end_index = min(start_index + 12, len(schedule))
        year_schedule = schedule[start_index:end_index]

        if not year_schedule:
            break

        beginning_balance = year_schedule[0]["balance_before"]
        ending_balance = year_schedule[-1]["balance_after"]
        annual_paid = sum(item["payment"] for item in year_schedule)
        annual_interest = sum(item["interest"] for item in year_schedule)
        annual_principal = sum(item["principal"] for item in year_schedule)

        yearly_rows.append(
            {
                "year": year,
                "beginning_balance": money(beginning_balance),
                "ending_balance": money(ending_balance),
                "total_paid": money(annual_paid),
                "interest_paid": money(annual_interest),
                "principal_paid": money(annual_principal),
            }
        )

    return yearly_rows


def main():
    principal = 250000
    annual_rate = 6.5
    years = 30

    summary = loan_summary(principal, annual_rate, years)
    schedule = payment_schedule(principal, annual_rate, years)
    yearly = yearly_summary(principal, annual_rate, years)

    print("Loan Summary")
    print("-" * 40)
    print(f"Principal: ${summary['principal']:,.2f}")
    print(f"Annual Rate: {summary['annual_rate']}%")
    print(f"Years: {summary['years']}")
    print(f"Monthly Payment: ${summary['monthly_payment']:,.2f}")
    print(f"Total Paid: ${summary['total_paid']:,.2f}")
    print(f"Total Interest: ${summary['total_interest']:,.2f}")
    print()

    print("First 3 Payments")
    print("-" * 40)
    for month in schedule[:3]:
        print(
            f"Month {month['month']}: "
            f"Payment=${month['payment']:,.2f}, "
            f"Interest=${month['interest']:,.2f}, "
            f"Principal=${month['principal']:,.2f}, "
            f"Balance=${month['balance_after']:,.2f}"
        )

    print()
    print("Yearly Summary")
    print("-" * 40)
    for row in yearly[:3]:
        print(
            f"Year {row['year']}: "
            f"Paid=${row['total_paid']:,.2f}, "
            f"Interest=${row['interest_paid']:,.2f}, "
            f"Principal=${row['principal_paid']:,.2f}, "
            f"Ending Balance=${row['ending_balance']:,.2f}"
        )


if __name__ == "__main__":
    main()
