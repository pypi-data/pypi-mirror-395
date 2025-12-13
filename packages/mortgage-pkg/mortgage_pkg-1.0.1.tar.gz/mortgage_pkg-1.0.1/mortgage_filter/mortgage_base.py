#!/usr/bin/env python
# coding: utf-8

# # BASE FUNCTIONS
# ### Functions for:
# - minimum down payment
# - mortgage rate by term
# - mortgage insurance
# - monthly payments
# - optimal monthly payment
# - total interest

# In[1]:

import numpy as np

from mortgage_filter.exceptions import *


def min_downpayment(price):
    """Returns the minimum downpayment required for a real estate
    price defined by the Financial Consumer Agency of Canada.
    (https://www.canada.ca/en/financial-consumer-agency/services/mortgages/down-payment.html)

    Arguments
    ----------
    price : numeric
        Property price or avereage area property price

    Return
    ------
    float
        minimum downpayment
    """
    try:
        if price < 0:
            print("Invalid price")
            return None
        elif price < 500000:
            return price * 0.05
        elif price < 1000000:
            return 500000 * 0.05 + (price - 500000) * 0.1
        return price * 0.2

    except TypeError:
        print("Invalid price input. Must be of type numeric")
        return None


def mort_rate(term):
    """If no mortgage rate is specified this function can be used to
    return an estimated mortgage rate based on a regression fit (R^2 = 0.926)
    on average Canadian mortgage rates for possible term lengths.
    (https://www.superbrokers.ca/tools/mortgage-rates-comparison/)

    Arguments
    ----------
    term : int
        contract length in years (from 1 to 10 years)

    Return
    ------
    float
        interest rate
    """
    try:
        x = term
        if x < 1:
            raise TermError
        elif x > 10:
            raise TermError(
                "Lengths greater than 10 years are not typically available."
            )
        elif isinstance(x, float):
            print(
                "Warning: Term lengths are typically in whole years not fractions of years."
            )
        return round((0.0167 * x**2 - 0.0337 * x + 1.6851), 3)

    except TermError as TE:
        print(
            f"{TE} \nTerms must range from 1 to 10 years, but calculation will be performed anyway."
        )
        return round((0.0167 * x**2 - 0.0337 * x + 1.6851), 3)


def mortgage_insurance(price, downpayment):
    """Returns the cost of mortgage insurance.

    Insurance rates are calculated from loan to asset price ratio.
    Rates are applied to the loan to generate a lump sum amount that's
    then added to the principal of the loan to give mortgage insurance.

    Arguments
    ----------
    price : numeric
        Property price

    downpayment : int or float
        Downpayment on property

    Return
    ------
    float
        Mortgage insurance
    """
    try:
        DP_proportion = downpayment / price

        # if downpayment more than 20% of the house price no mortgage insurance required.
        if DP_proportion >= 0.2:
            return 0
        elif DP_proportion < 0.05:
            raise MinimalDPError("Downpayment must be at least 5% the asset value")

        loan_to_price = (price - downpayment) / price
        x = loan_to_price

        # loan to price ratio determines insurance rate
        insurance_rate = (
            2924.5 * x**4 - 9340.3 * x**3 + 11116 * x**2 - 5830.8 * x + 1137.1
        ) / 100

        # mortgage insurance is a % applied to the mortgage amount (price - downpayment)
        return round(((price - downpayment) * insurance_rate), 2)

    except TypeError:
        print("Bad entry type. Received:", type(price), type(downpayment))
        return None
    except MinimalDPError as PE:
        print(PE, "\nInput value is too low to be legally considered.")
        return None
    except ZeroDivisionError:
        print("Price cannot be zero.")
        return None


def monthly_payment(principal, mortgage_rate, amortization, months=False):
    """Returns the monthly payment required to meet the given amortization period.
    Assumes payments occur on a monthly basis.

    Arguments
    ----------
    principal : numeric

    mortgage_rate : float
        Annual mortgage rate (loan interest)

    amortization: int
        Amortization period in years (or in months if months == True)

    months : bool
        (Optional) if True, amortization period is interpreted in months (default = False)

    Return
    ------
    float
        monthly payment
    """

    R = mortgage_rate / 100 / 12 + 1  ## monthly interest rate

    if months == True:
        n = amortization  ## if specified in months, amortization = the number of payments
    else:
        n = (
            amortization * 12
        )  ## convert amortization in years to the number of monthly payments

    monthly_contribution = principal * ((R**n) * (1 - R) / (1 - R**n))

    return round(monthly_contribution, 2)


def optimal_monthly_payment(principal, mortgage_rate, max_monthly_payment):
    """Returns the first amortization period which has a monthly payment
    less than your max_monthly_payment (ie. within budget). The shortest
    possible amortization period has the lowest long term interest cost.

    Arguments
    ----------
    principal : numeric

    mortgage_rate : float
          Annual mortgage rate (loan interest)

    max_monthly_payment: numeric
        Your max affordable monthly contribution

    Return
    ------
    list
        mp: monthly payment for a given amortization
        i: amortization period in years
    """
    try:
        for i in range(1, 26):
            mp = monthly_payment(principal, mortgage_rate, i, months=False)
            if mp <= max_monthly_payment:
                return [mp, i]
        return [np.nan, np.nan]

    except TypeError:
        print(
            "Bad entry type. Received:",
            type(principal),
            type(mortgage_rate),
            type(max_monthly_payment),
        )
        return None


def total_interest(principal, mortgage_rate, monthly_payment):
    """Returns the cumulative interest paid on a given principal, mortgage rate, and monthly payment.

    Arguments
    ----------
    principal : numeric

    mortgage_rate : float
        Annual mortgage rate (loan interest)

    amortization: int
        Amortization period in years (or in months if months == True)

    monthly_payment : bool
        Monthly contribution towards the principal

    Return
    ------
    float
        Cumulative interest paid
    """
    try:
        R = mortgage_rate / 1200  ## monthly interest rate
        CumInterest = 0

        i = principal * R
        new_p = principal + i - monthly_payment

        while new_p > 0:
            CumInterest += i
            i = new_p * R
            new_p = new_p + i - monthly_payment

            if new_p >= new_p - i + monthly_payment:
                print(
                    "Monthly contribution is insufficient to pay off the original Principal."
                )
                return None

        return round(CumInterest, 2)

    except TypeError:
        print(
            "Bad entry type. Received:",
            type(principal),
            type(mortgage_rate),
            type(monthly_payment),
        )
        return None
