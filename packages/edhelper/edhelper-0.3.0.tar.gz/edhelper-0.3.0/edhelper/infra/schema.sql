CREATE TABLE IF NOT EXISTS cards (
	id VARCHAR NOT NULL,
	name VARCHAR, 
	colors VARCHAR, 
	color_identity VARCHAR, 
	cmc INTEGER, 
	mana_cost VARCHAR, 
	image VARCHAR, 
	art VARCHAR, 
	legal_commanders BOOLEAN, 
	is_commander BOOLEAN, 
	price VARCHAR, 
  edhrec_rank INTEGER,
	type_line VARCHAR,
	PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS decks (
	id INTEGER NOT NULL, 
	nome VARCHAR NOT NULL, 
	last_update DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS deck_cards (
	deck_id INTEGER NOT NULL, 
	card_id VARCHAR NOT NULL, 
	quantidade INTEGER NOT NULL, 
	is_commander BOOLEAN NOT NULL, 
	PRIMARY KEY (deck_id, card_id), 
	FOREIGN KEY(deck_id) REFERENCES decks (id) ON DELETE CASCADE,
	FOREIGN KEY(card_id) REFERENCES cards (id)
);
CREATE INDEX IF NOT EXISTS ix_cards_name ON cards (name);
CREATE INDEX IF NOT EXISTS ix_cards_id ON cards (id);
CREATE INDEX IF NOT EXISTS ix_decks_nome ON decks (nome);
CREATE INDEX IF NOT EXISTS ix_decks_id ON decks (id);
PRAGMA foreign_keys = ON;
