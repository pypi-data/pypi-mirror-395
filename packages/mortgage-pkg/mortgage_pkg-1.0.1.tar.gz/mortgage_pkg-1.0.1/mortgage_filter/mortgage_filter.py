#!/usr/bin/env python
# coding: utf-8

# # PRIMARY FILTER FUNCTION
# ### Uses base functions to compute affordability metrics.


from warnings import filterwarnings

import pandas as pd

from mortgage_filter.exceptions import *
from mortgage_filter.mortgage_base import *


def property_filter(
    property_data,
    downpayment,
    mortgage_rate=None,
    mortgage_term=None,
    max_monthly_payment=None,
    max_loan=None,
):
    """Given a dataframe of properties, their prices, and some basic financial information, it returns a dataframe with only the affordable properties and other affordability metrics (ie. how long it would take to pay off, monthly payments, total interest, etc.).

    Arguments
    ----------
    data : dataframe
        Areas/properties in column index 0 (str)
        Respective prices in column index 1 (numeric)

    downpayment : numeric
        Your maximal possible downpayment

    mortgage_rate : numeric
        Interest rate on the mortgage loan (leave empty if mortgage_term is provided)

    mortgage_term : int
        Contract length in years (1 to 10) for the mortgage interest rate.
        Only specify if you do not know what mortgage_rate to enter (leave empty if mortgage_rate provided)

    max_monthly_payment : numeric
        Your max affordable or bank limited monthly payment towards your home

    max_loan : numeric
        Max eligible loan based on your downpayment

    Return
    ------
    dataframe
        Properties/Areas
        Prices/Average area price
        Minimum_Downpayment
        Mortgage_Insurance
        Principal
        Monthly_Payment
        Shortest_Amortization
        Total_Interest
        Net_Cost (assuming no other fees)
    """

    filterwarnings("ignore")

    try:
        # is object a dataframe?
        if isinstance(property_data, pd.DataFrame) == False:
            raise FilterInputError("Dataframe object expected")
        # right number of columns?
        if len(property_data.columns) != 2:
            raise FormatError(
                "Expected two columns of type str and numeric, respectively"
            )
        # is column at index 1 (price) numeric?
        if pd.api.types.is_numeric_dtype(property_data.iloc[:, 1]) == False:
            raise TypeError("Column at index 1 (price) must be numeric")

    except FilterInputError as FIE:
        print(FIE, "\nReveived object of type:", type(property_data))
        return None
    except FormatError as FE:
        print(
            FE,
            "\nReveived dataframe with this many columns:",
            len(property_data.columns),
        )
        return None
    except TypeError as TE:
        print(TE)
        return None

    data = property_data.copy()

    # Rename columns
    data = data.set_axis(["Property/Area", "Price"], axis=1)

    # Note original input of properties
    og_prop_count = data["Property/Area"].count()

    # FILTER: Downpayment. Remove properties where minimal DP exceeds your entered DP
    data["Minimum_Downpayment"] = data.iloc[:, 1].apply(lambda x: min_downpayment(x))
    data = data[data["Minimum_Downpayment"] <= downpayment]

    # Mortgage rate. If none provided give a reasonable estimate
    if mortgage_rate == None:
        mortgage_rate = mort_rate(mortgage_term)

    # Calculate mortgage insurance (default insurance) lump sum for each property
    data["Mortgage_Insurance"] = data.loc[:, "Price"].apply(
        lambda p: mortgage_insurance(p, downpayment)
    )

    # Calculate initial principal for each property
    data["Principal"] = round(
        (data["Price"] - downpayment + data["Mortgage_Insurance"]), 2
    )

    # FILTER: Max eligible loan. Remove properties where the principal exceeds the max approved loan
    # If no max loan specified assume no limit
    if max_loan != None:
        data = data[data["Principal"] < max_loan]

    # Add two columns for monthly payment and shortest amortization period
    # These are outputs of the optimal_monthly_payment function
    temp = data.loc[:, "Principal"].apply(
        lambda principal: optimal_monthly_payment(
            principal, mortgage_rate, max_monthly_payment
        )
    )
    temp = list(zip(*temp))

    data["Monthly_Payment"] = temp[0]
    data["Shortest_Amortization"] = temp[1]

    # FILTER: Remove rows where Monthly_Payment is NaN
    data = data[data["Monthly_Payment"].notnull()]

    # Add column for the cumulative cost of interest given that amortization
    tot_int = []
    for princ, monthly_payment in data[["Principal", "Monthly_Payment"]].itertuples(
        index=False
    ):
        tot_int += [total_interest(princ, mortgage_rate, monthly_payment)]
    data["Total_Interest"] = tot_int

    # Add column for net cost of home (price + cumulative interest + mortgage insurance)
    data["Net_Cost"] = (
        data["Price"] + data["Mortgage_Insurance"] + data["Total_Interest"]
    )

    print(
        f"You can afford {data['Property/Area'].count()} properties from the {og_prop_count} you've provided."
    )
    return data
