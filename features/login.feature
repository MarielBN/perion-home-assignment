Feature: Login

Scenario Outline: Login with valid and invalid users
  Given login page is displayed
  When login is performed using "<user_name>"
  Then <then_step>

Examples:
  | user_name         | then_step                                                                 |
  | standard_user    | login should succeed                                                      |
  | locked_out_user  | login should fail with error "Epic sadface: Sorry, this user has been locked out." |
  | invalid_user     | login should fail with error "Epic sadface: Username and password do not match any user in this service" |

