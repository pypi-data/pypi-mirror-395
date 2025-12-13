#!/usr/bin/env python
# coding: utf-8

from mortgage_filter.mortgage_base import *

import unittest

class Test_base_functions(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        ## Import dependencies
        from numpy import nan, linspace
        print('!!! Class setup for Test(Test_base_functions) !!!')
    
    def setUp(self):
        ## Test values
        self.downpayment = [0, 0, 0, 200000, 150000, 50000]
        self.max_monthly_payment = np.linspace(1500, 11000, 4)
        self.principal = 600000
        self.mortgage_rate = 2.6
        self.price = ['4000000', -400000, 0, 400000, 800000, 1200000]
        self.term = [-1, 0.5, 1, 5.5, 10, 12]
        self.amortization_years = [1, 8, 16, 24]
        self.amortization_months = [12, 96, 192, 288]
        print('~~~ start test ~~~')
        
        
    def test_min_downpayment(self):
        self.expected = [None, None, 0, 20000, 55000, 240000]
        for i in range(6):
            self.assertEqual(min_downpayment(self.price[i]), self.expected[i])   
        
    def test_mort_rate(self):
        self.expected = [1.736, 1.672, 1.668, 2.005, 3.018, 3.686]
        for i in range(6):
            self.assertEqual(mort_rate(self.term[i]), self.expected[i])
        
    def test_mortgage_insurance(self):
        self.expected = [None, None, None, 0, 16026.85, None]
        for i in range(6):
            self.assertEqual(mortgage_insurance(self.price[i], self.downpayment[i]), self.expected[i])
    
    def test_monthly_payment(self):
        self.expected = [50706.96, 6929.26, 3823.27, 2802.68]
        for i in range(4):
            self.assertEqual(monthly_payment(self.principal, self.mortgage_rate, self.amortization_years[i], months = False),
                             self.expected[i])
            self.assertEqual(monthly_payment(self.principal, self.mortgage_rate, self.amortization_months[i], months = True),
                             self.expected[i])
        
    def test_optimal_monthly_payment(self):
        self.expected = [[np.nan, np.nan], [4536.83, 13], [7820.28, 7], [10674.89, 5]]
        for i in range(4):
            self.assertEqual(optimal_monthly_payment(self.principal, self.mortgage_rate, self.max_monthly_payment[i]),
                             self.expected[i])

    def test_total_interest(self):
        self.expected = [796440.43, 104031.41, 56784.2, 39211.53]
        for i in range(4):
            self.assertEqual(total_interest(self.principal, self.mortgage_rate, self.max_monthly_payment[i]),
                             self.expected[i])
        
        ## handling test for insufficient monthly income leading to infinitely large interest
        self.assertIsNone(total_interest(self.principal, self.mortgage_rate, 100), None)
        
            
    def tearDown(self):
        print('~~~ complete ~~~')  
        
    @classmethod
    def tearDownClass(cls):
        print('!!! Class teardown for Test(Test_base_functions) !!!\n\n\n')


#unittest.main(argv=[''], verbosity=2, exit=False)