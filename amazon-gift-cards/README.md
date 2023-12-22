# Amazon Gift Card Script

Script to automate the purchase of Amazon gift cards using multiple cards multiple times

## Usage

Append entries to the `cards` variable where each entry is a key-value pair:

- Key: String alias for the card (For your reference only)
- Value: Tuple of size 2 containing:
  - String with the last 4 digits of the card intended on being used (Should already be added on Amazon or else an error will be logged)
  - Number of times to purchase a gift card using this card

The `PURCHASE_AMOUNT` variable should also be changed, depending on your preferred denomination per EACH transaction/purchase