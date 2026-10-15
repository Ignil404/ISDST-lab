from pytest_bdd import scenarios, given, when, then, parsers
from main import best_discount

scenarios("../discount.feature")


@given(parsers.parse("the original price is {price:f}"), target_fixture="price")
def given_price(price):
    return price


@when(
    parsers.parse("I apply a percent discount of {percent:f}"), target_fixture="percent"
)
def given_percent(percent):
    return percent


@when(
    parsers.parse("I apply a fixed discount of {amount:f}"),
    target_fixture="final_price",
)
def given_amount(price, percent, amount):
    return best_discount(price, percent, amount)


@then(parsers.parse("the best final price should be {expected:f}"))
def check_final_price(final_price, expected):
    assert final_price == expected