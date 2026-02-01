Feature: Products

  Background:
    Given user is logged in as "standard_user"

  Scenario: Product listing is displayed with valid data
    Then product listing should be visible
    And all product names should be non-empty
    And all product prices should be greater than 0

  Scenario Outline: Sort by price
    When sorting products by "<sort_option>"
    Then product prices should be sorted <direction>

    Examples:
      | sort_option            | direction  |
      | Price (low to high)    | ascending  |
      | Price (high to low)    | descending |
