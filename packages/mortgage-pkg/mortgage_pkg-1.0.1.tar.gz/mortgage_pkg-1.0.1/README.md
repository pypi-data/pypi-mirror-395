![CI Tests](https://github.com/lukavuko/mortgage-filter-package/workflows/CI%20Tests/badge.svg)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# The Mortgage-Filter-Package

A Python package for analyzing real estate affordability based on your financial situation. Filter properties, calculate mortgage costs, and visualize how different financial parameters affect your home buying power.

A small note: this was one of the very first things I've ever uploaded to github. It's not complicated. It's simply a first naive attempt at developing a basic Python package for processing real estate data which instantly yields information on property affordability.

**What it does:**

- Filters property datasets by affordability based on your downpayment and monthly budget
- Calculates mortgage insurance, optimal payments, and total interest costs
- Provides detailed affordability metrics for each property
- Visualizes the relationship between interest rates, payments, and costs

## Quick Links

- [PyPI Package](https://pypi.org/project/mortgage-pkg/)
- [Interactive Demo Notebook](demo/demo.ipynb)
- [Quick Start](#quick-start)
- [Documentation](#documentation)

## Installation

```bash
pip install mortgage-pkg
```

**Requirements:**

- Python >= 3.7
- pandas
- numpy

## Features

✅ **Property Filtering** - Find affordable properties from your dataset
✅ **Mortgage Calculations** - Compute interest, payments, and amortization periods
✅ **Insurance Analysis** - Calculate Canadian mortgage insurance requirements
✅ **Cost Optimization** - Determine optimal monthly payments to minimize interest
✅ **Visual Analytics** - Generate publication-quality visualizations with seaborn

## Quick Start

### Basic Usage

```python
from mortgage_filter import property_filter
import pandas as pd

# Load your property data (2 columns: name/area, price)
properties = pd.read_csv('your_properties.csv')

# Filter by affordability
affordable = property_filter(
    property_data=properties,
    downpayment=190000,
    mortgage_rate=2.8,
    max_monthly_payment=4800
)
```

### Output

The function returns a dataframe with detailed affordability metrics:

- **Price** - Listed property price
- **Minimum_Downpayment** - Legal minimum (5% of value)
- **Mortgage_Insurance** - Insurance cost when downpayment < 20%
- **Principal** - Loan amount (price - downpayment + insurance)
- **Monthly_Payment** - Optimal payment for shortest amortization
- **Shortest_Amortization** - Years to pay off with your budget
- **Total_Interest** - Cumulative interest over loan lifetime
- **Net_Cost** - Total cost (price + insurance + interest)

## Visualizations

The package includes powerful visualization capabilities. See the [interactive demo notebook](demo/demo.ipynb) for detailed examples.

### Interest Rate Impact

![Interest Rate Impact](demo/output_7_1.svg)

*How mortgage term length affects estimated interest rates*

### Monthly Payments vs Total Interest

![Monthly Payments Impact](demo/output_16_1.svg)

*How your monthly payment amount affects total interest paid over the life of the loan*

### Amortization Period Analysis

![Amortization Period](demo/output_18_1.svg)

*Relationship between monthly payments and loan duration*

### Mortgage Insurance by Downpayment

![Mortgage Insurance](demo/output_20_1.svg)

*How downpayment size affects mortgage insurance (20% threshold for Canadian mortgages)*

## Complete Demo

For a comprehensive walkthrough with all features and visualizations, see the [**Interactive Demo Notebook**](demo/demo.ipynb).

The demo covers:

- 3 real-world affordability scenarios
- 5 detailed analysis questions with visualizations
- Vancouver, BC housing data examples
- Canadian mortgage insurance rules

---

## Example: Vancouver Housing Data

```python
properties = pd.read_csv('data/vancouver_testset.csv')
properties.head()
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Area</th>
      <th>House Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Downtown & Westside</td>
      <td>3118200</td>
    </tr>
    <tr>
      <th>1</th>
      <td>West Vancouver</td>
      <td>2743600</td>
    </tr>
    <tr>
      <th>2</th>
      <td>North Vancouver</td>
      <td>1665100</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Richmond</td>
      <td>1581600</td>
    </tr>
    <tr>
      <th>4</th>
      <td>South Burnaby</td>
      <td>1564000</td>
    </tr>
  </tbody>
</table>
</div>

### Filtering Affordable Properties

```python
from mortgage_filter import property_filter

# Scenario: Unknown interest rate, specify term length
results = property_filter(
    property_data=properties,
    downpayment=190000,
    mortgage_term=15,
    max_monthly_payment=4800
)

# Output: "You can afford 5 properties from the 25 you've provided."
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Property/Area</th>
      <th>Price</th>
      <th>Minimum_Downpayment</th>
      <th>Mortgage_Insurance</th>
      <th>Principal</th>
      <th>Monthly_Payment</th>
      <th>Shortest_Amortization</th>
      <th>Total_Interest</th>
      <th>Net_Cost</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>20</th>
      <td>Pitt Meadows</td>
      <td>974800</td>
      <td>72480.0</td>
      <td>18793.83</td>
      <td>803593.83</td>
      <td>4767.48</td>
      <td>24</td>
      <td>569440.84</td>
      <td>1563034.67</td>
    </tr>
    <tr>
      <th>21</th>
      <td>North Delta</td>
      <td>972500</td>
      <td>72250.0</td>
      <td>18702.26</td>
      <td>801202.26</td>
      <td>4753.29</td>
      <td>24</td>
      <td>567746.53</td>
      <td>1558948.79</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Maple Ridge</td>
      <td>884200</td>
      <td>63420.0</td>
      <td>0.00</td>
      <td>694200.00</td>
      <td>4698.63</td>
      <td>19</td>
      <td>377088.77</td>
      <td>1261288.77</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Abbotsford</td>
      <td>873600</td>
      <td>62360.0</td>
      <td>0.00</td>
      <td>683600.00</td>
      <td>4782.72</td>
      <td>18</td>
      <td>349446.77</td>
      <td>1223046.77</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Mission</td>
      <td>726000</td>
      <td>47600.0</td>
      <td>0.00</td>
      <td>536000.00</td>
      <td>4662.46</td>
      <td>13</td>
      <td>191344.02</td>
      <td>917344.02</td>
    </tr>
  </tbody>
</table>
</div>

### We're left with what?

- We're left with all the affordable home indexes as well as:

  - the listed prices
  - the minimum downpayment (5% of value)
  - the mortgage insurance
  - the principal (price - downpayment)
  - the optimal monthly payment for the shortest amortization period (years)
  - the cumulative interst
  - the net cost
- We note there's a printed warning saying that terms must be less than or equal to 10 years (banks don't typically offer terms beyond 10 years).

  The function can handles the exception and **extrapolates from the term to interest rate function; however, this could yield misleading interest rates.**

  Lets see what the function looks like (interest as a function of term length):

```python
terms = np.arange(1, 15)
rate = [mort_rate(t) for t in terms]

plt.plot(terms, rate)
plt.xlabel('Terms'); plt.ylabel('Interest Rate as %')
plt.axvline(x = 10, linestyle='--', color = 'black')
plt.grid()

plt.savefig('output_7_1.svg', transparent = False, format = 'svg')
plt.show()
```

    Lengths greater than 10 years are not typically available.
    Terms must range from 1 to 10 years, but calculation will be performed anyway.
    Lengths greater than 10 years are not typically available.
    Terms must range from 1 to 10 years, but calculation will be performed anyway.
    Lengths greater than 10 years are not typically available.
    Terms must range from 1 to 10 years, but calculation will be performed anyway.
    Lengths greater than 10 years are not typically available.
    Terms must range from 1 to 10 years, but calculation will be performed anyway.

![png](demo/output_7_1.svg)

### Okay, now lets try using a mortgage rate of our own, say 2.8%.

```python
property_filter(property_data = properties,
                downpayment = 190000,
                mortgage_rate = 2.8,
                max_monthly_payment = 4800)
```

    You can afford 5 properties from the 25 you've provided.

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Property/Area</th>
      <th>Price</th>
      <th>Minimum_Downpayment</th>
      <th>Mortgage_Insurance</th>
      <th>Principal</th>
      <th>Monthly_Payment</th>
      <th>Shortest_Amortization</th>
      <th>Total_Interest</th>
      <th>Net_Cost</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>20</th>
      <td>Pitt Meadows</td>
      <td>974800</td>
      <td>72480.0</td>
      <td>18793.83</td>
      <td>803593.83</td>
      <td>4740.54</td>
      <td>18</td>
      <td>220350.90</td>
      <td>1213944.73</td>
    </tr>
    <tr>
      <th>21</th>
      <td>North Delta</td>
      <td>972500</td>
      <td>72250.0</td>
      <td>18702.26</td>
      <td>801202.26</td>
      <td>4726.43</td>
      <td>18</td>
      <td>219695.22</td>
      <td>1210897.48</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Maple Ridge</td>
      <td>884200</td>
      <td>63420.0</td>
      <td>0.00</td>
      <td>694200.00</td>
      <td>4727.53</td>
      <td>15</td>
      <td>156743.49</td>
      <td>1040943.49</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Abbotsford</td>
      <td>873600</td>
      <td>62360.0</td>
      <td>0.00</td>
      <td>683600.00</td>
      <td>4655.34</td>
      <td>15</td>
      <td>154350.26</td>
      <td>1027950.26</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Mission</td>
      <td>726000</td>
      <td>47600.0</td>
      <td>0.00</td>
      <td>536000.00</td>
      <td>4722.69</td>
      <td>11</td>
      <td>87383.70</td>
      <td>813383.70</td>
    </tr>
  </tbody>
</table>
</div>

### Notice how the last 4 columns have lower costs now.

- Lets try one more time with a high downpayment/low monthly payment scenario.
- Lets also assume a loan limit of **\$600,000** and **\$700,000** to see how this might affect a buying decision.

```python
property_filter(property_data = properties,
                downpayment = 500000,
                mortgage_rate = 2.8,
                max_monthly_payment = 3200,
                max_loan = 600000).head()
```

    You can afford 12 properties from the 25 you've provided.

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Property/Area</th>
      <th>Price</th>
      <th>Minimum_Downpayment</th>
      <th>Mortgage_Insurance</th>
      <th>Principal</th>
      <th>Monthly_Payment</th>
      <th>Shortest_Amortization</th>
      <th>Total_Interest</th>
      <th>Net_Cost</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>13</th>
      <td>Langley</td>
      <td>1090800</td>
      <td>218160.0</td>
      <td>0</td>
      <td>590800</td>
      <td>3103.53</td>
      <td>21</td>
      <td>191282.32</td>
      <td>1282082.32</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Cloverdale</td>
      <td>1087400</td>
      <td>217480.0</td>
      <td>0</td>
      <td>587400</td>
      <td>3199.21</td>
      <td>20</td>
      <td>180410.55</td>
      <td>1267810.55</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Central Surrey</td>
      <td>1086300</td>
      <td>217260.0</td>
      <td>0</td>
      <td>586300</td>
      <td>3193.22</td>
      <td>20</td>
      <td>180065.18</td>
      <td>1266365.18</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Ladner</td>
      <td>1042000</td>
      <td>208400.0</td>
      <td>0</td>
      <td>542000</td>
      <td>3197.35</td>
      <td>18</td>
      <td>148627.69</td>
      <td>1190627.69</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Port Coquitlam</td>
      <td>1034400</td>
      <td>206880.0</td>
      <td>0</td>
      <td>534400</td>
      <td>3152.52</td>
      <td>18</td>
      <td>146536.03</td>
      <td>1180936.03</td>
    </tr>
  </tbody>
</table>
</div>

```python
property_filter(property_data = properties,
                downpayment = 500000,
                mortgage_rate = 2.8,
                max_monthly_payment = 3200,
                max_loan = 700000).head()
```

    You can afford 14 properties from the 25 you've provided.

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Property/Area</th>
      <th>Price</th>
      <th>Minimum_Downpayment</th>
      <th>Mortgage_Insurance</th>
      <th>Principal</th>
      <th>Monthly_Payment</th>
      <th>Shortest_Amortization</th>
      <th>Total_Interest</th>
      <th>Net_Cost</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>11</th>
      <td>Tsawwassen</td>
      <td>1153300</td>
      <td>230660.0</td>
      <td>0</td>
      <td>653300</td>
      <td>3117.86</td>
      <td>24</td>
      <td>244644.99</td>
      <td>1397944.99</td>
    </tr>
    <tr>
      <th>12</th>
      <td>New Westminster</td>
      <td>1127200</td>
      <td>225440.0</td>
      <td>0</td>
      <td>627200</td>
      <td>3184.83</td>
      <td>22</td>
      <td>213587.50</td>
      <td>1340787.50</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Langley</td>
      <td>1090800</td>
      <td>218160.0</td>
      <td>0</td>
      <td>590800</td>
      <td>3103.53</td>
      <td>21</td>
      <td>191282.32</td>
      <td>1282082.32</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Cloverdale</td>
      <td>1087400</td>
      <td>217480.0</td>
      <td>0</td>
      <td>587400</td>
      <td>3199.21</td>
      <td>20</td>
      <td>180410.55</td>
      <td>1267810.55</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Central Surrey</td>
      <td>1086300</td>
      <td>217260.0</td>
      <td>0</td>
      <td>586300</td>
      <td>3193.22</td>
      <td>20</td>
      <td>180065.18</td>
      <td>1266365.18</td>
    </tr>
  </tbody>
</table>
</div>

### Note that no mortgage insurance is applied.

***In Canada, downpayments >20% of the home price do not require mortgage insurance.***

---

### If you'd like to dive deeper at one scenario in particular, base functions could be used as follows:

1. How quickly does cumulative interest increase as the mortgage rate increases?
2. How does cumulative interest change as monthly contributions increase??
3. How does the amortization period change as as monthly contributions increase?
4. What's my monthly payment on a **\$500,000** home for a 20 year amortization on 2% interest?
5. How does mortgage insurance change with downpayment?

```python
# Parameters
princ = 500000 # principal of 500k
mth_pay = 2000 # monthly payment of 2k
mort_rate = 2.0 # mortgage rate of 2%
```

```python
# Question 1

rate = np.linspace(1, 5, 20)
interest = [total_interest(princ, mortgage_rate = i, monthly_payment = mth_pay) for i in rate]

plt.plot(rate, interest)
plt.ticklabel_format(axis='y', style='plain')
plt.xlabel('Interest Rate as %'); plt.ylabel('Cumulative Interest'); plt.grid()

plt.savefig('output_15_1.svg', transparent = False, format = 'svg')
plt.show()

```

    Monthly contribution is insufficient to pay off the original Principal.

![png](demo/output_15_1.svg)

```python
# Question 2

payments = np.linspace(800, 6000, 20)
interest = [total_interest(princ, mort_rate, monthly_payment = p) for p in payments]

plt.plot(payments, interest)
plt.ticklabel_format(axis='y', style='plain')
plt.xlabel('Monthly Payment Amount'); plt.ylabel('Cumulative Interest'); plt.grid()

plt.savefig('output_16_1.svg', transparent = False, format = 'svg')
plt.show()
```

    Monthly contribution is insufficient to pay off the original Principal.

![png](demo/output_16_1.svg)

- Note that as the monthly payment increases, not only does cumulative interest decrease, but the amortization period decreases substantially but this isn't see in the plot above.
- Lets just peek at how the amortization period decreases.

```python
# Question 3

years = [optimal_monthly_payment(princ, mort_rate, max_monthly_payment = p)[1] for p in payments]

plt.plot(payments, years)
plt.xlabel('Max Monthly Payment'); plt.ylabel('Years to Pay Off'); plt.grid()

plt.savefig('output_18_1.svg', transparent = False, format = 'svg')
plt.show()
```

![png](demo/output_18_1.svg)

```python
# Question 4

monthly_payment(princ, mort_rate, amortization = 20)
```

    2529.42

```python
# Question 5
downpayment_size = np.linspace(22000, 125000, 28)
mort_ins = [mortgage_insurance(princ, d) for d in downpayment_size]

plt.plot(downpayment_size, mort_ins)
plt.xlabel('Downpayment on $500,000'); plt.ylabel('Mortgage Insurance'); plt.grid()

plt.savefig('output_20_1.svg', transparent = False, format = 'svg')
plt.show()
```

    Downpayment must be at least 5% the asset value
    Input value is too low to be legally considered.

![png](demo/output_20_1.svg)

- Notice how a message prints for downpayments less than 5% the property value (minimal downpayment).
- Also notice how at a downpayment of 20% mortgage insurance no longer applies.

---

## Documentation

All functions include detailed docstrings. Use Python's `help()` function for inline documentation:

```python
help(mortgage_filter)
```

    Help on module mortgage_filter.mortgage_filter in mortgage_filter:

    NAME
        mortgage_filter.mortgage_filter - # coding: utf-8

    FUNCTIONS
        property_filter(property_data, downpayment, mortgage_rate=None, mortgage_term=None, max_monthly_payment=None, max_loan=None)
            Given a dataframe of properties, their prices, and some basic financial information, it returns a dataframe with only the affordable properties and other affordability metrics (ie. how long it would take to pay off, monthly payments, total interest, etc.).

| Arguments                                     |
| --------------------------------------------- |
| data : dataframe                              |
| Areas/properties in column index 0 (str)      |
| Respective prices in column index 1 (numeric) |

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

| Return                            |
| --------------------------------- |
| dataframe                         |
| Properties/Areas                  |
| Prices/Average area price         |
| Minimum_Downpayment               |
| Mortgage_Insurance                |
| Principal                         |
| Monthly_Payment                   |
| Shortest_Amortization             |
| Total_Interest                    |
| Net_Cost (assuming no other fees) |

```python
help(total_interest)
```

    Help on function total_interest in module mortgage_filter.mortgage_base:

    total_interest(principal, mortgage_rate, monthly_payment)
        Returns the cumulative interest paid on a given principal, mortgage rate, and monthly payment.

| Arguments           |
| ------------------- |
| principal : numeric |

    mortgage_rate : float
            Annual mortgage rate (loan interest)

    amortization: int
            Amortization period in years (or in months if months == True)

    monthly_payment : bool
            Monthly contribution towards the principal

| Return                   |
| ------------------------ |
| float                    |
| Cumulative interest paid |

```python
help(optimal_monthly_payment)
```

    Help on function optimal_monthly_payment in module mortgage_filter.mortgage_base:

    optimal_monthly_payment(principal, mortgage_rate, max_monthly_payment)
        Returns the first amortization period which has a monthly payment
        less than your max_monthly_payment (ie. within budget). The shortest
        possible amortization period has the lowest long term interest cost.

| Arguments           |
| ------------------- |
| principal : numeric |

    mortgage_rate : float
              Annual mortgage rate (loan interest)

    max_monthly_payment: numeric
            Your max affordable monthly contribution

| Return                                       |
| -------------------------------------------- |
| list                                         |
| mp: monthly payment for a given amortization |
| i: amortization period in years              |

```python
help(mortgage_insurance)
```

---

## Key Features & Canadian Mortgage Rules

### Mortgage Insurance (CMHC)

- **Required** when downpayment < 20% of home value
- **Not required** when downpayment ≥ 20% of home value
- Insurance rates vary by loan-to-value ratio (calculated automatically)

### Interest Rate Estimation

- Estimates rates based on mortgage term length (1-10 years typical)
- Uses regression model fitted to Canadian mortgage rate data
- Terms > 10 years use extrapolation (less accurate)

### Optimization

- Calculates optimal monthly payment for shortest amortization
- Minimizes total interest paid over loan lifetime
- Respects your maximum monthly budget constraint

---

## Testing & CI/CD

- ✅ Comprehensive test suite with >95% coverage
- ✅ Automated CI testing via GitHub Actions
- ✅ Compatible with Python 3.7-3.11
- ✅ Tests run on every commit to `main`

Run tests locally:

```bash
python TEST_SUITE.py
```

---

## Contributing & Support

**Questions or feature requests?** Contact: luka.vuko@outlook.com

**Found a bug?** [Open an issue](https://github.com/lukavuko/mortgage-filter-package/issues)

**Want to contribute?** Pull requests are welcome!

---

## License

MIT License - see [LICENSE.md](LICENSE.md) for details

---

## Acknowledgments

This project was created to better understand the home buying process and associated costs. It's designed for educational purposes and personal financial planning.

**Disclaimer:** This tool provides estimates based on typical Canadian mortgage scenarios. Always consult with a qualified mortgage professional for official financial advice.
