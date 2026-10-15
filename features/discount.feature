Feature: Discount Calculator
  As a customer
  I want to calculate the best discount
  So that I can pay the minimum price

  Scenario: Percent discount is better than fixed
    Given the original price is 100.0
    When I apply a percent discount of 30.0
    And I apply a fixed discount of 20.0
    Then the best final price should be 70.0

  Scenario: Fixed discount is better than percent
    Given the original price is 100.0
    When I apply a percent discount of 10.0
    And I apply a fixed discount of 50.0
    Then the best final price should be 50.0

  Scenario: Boundary values 0 and 100 percent
    Given the original price is 200.0
    When I apply a percent discount of 100.0
    And I apply a fixed discount of 0.0
    Then the best final price should be 0.0
