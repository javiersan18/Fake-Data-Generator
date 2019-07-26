CREATE TABLE IF NOT EXISTS `credit_cards_example` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner_name` varchar(100) NOT NULL,
  `iban` varchar(100) NOT NULL,
  `credit_card_number` varchar(100) NOT NULL,
  `credit_card_provider` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;