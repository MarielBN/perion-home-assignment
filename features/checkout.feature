Feature: Checkout

  Background:
    Given user is logged in as "standard_user"

  Scenario Outline: Complete checkout with CSV data
    Given there are <count> products in the cart
    When proceeding to checkout
    And entering checkout information from CSV row "<csv_row_index>"
    And reviewing the order summary
    Then item total should equal the sum of items plus tax
    When completing the order
    Then order success message should be displayed

    Examples:
      | count | csv_row_index |
      | 3       | 1   |

  Scenario: Checkout with empty cart
    Given having an empty cart
    When attempting to checkout
    Then checkout should be blocked for an empty cart
