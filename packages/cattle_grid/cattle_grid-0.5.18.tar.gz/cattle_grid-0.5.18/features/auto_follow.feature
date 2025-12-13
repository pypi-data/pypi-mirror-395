Feature: Automatically accepts followers

    Background:
        Given A new user called "Alice"
        And A new user called "Bob"
        And "Alice" automatically accepts followers

    Scenario:
        When "Bob" follows auto-following "Alice"
        Then The "followers" collection of "Alice" contains "Bob"
        And The "following" collection of "Bob" contains "Alice"