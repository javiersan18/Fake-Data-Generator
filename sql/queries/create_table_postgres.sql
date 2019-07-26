CREATE TABLE IF NOT EXISTS credit_cards_example (
  id SERIAL PRIMARY KEY,
  owner_name char(100) NOT NULL,
  iban char(100) NOT NULL,
  credit_card_number char(100) NOT NULL,
  credit_card_provider char(100) NOT NULL
);