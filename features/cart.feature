Feature: Cart

  Background:
    Given user is logged in as "standard_user"

  Scenario Outline: Add products and remove some
    When adding <count> products to the cart
    Then cart badge should show <count> items
    When opening the cart
    And removing the product at position <position_to_remove> from the cart
    Then cart should have <remaining> items
    And the removed product should not be in the cart
    And the cart should contain only the other products

    Examples:
      | count | position_to_remove | remaining |
      | 3     | 1                  | 2         |
