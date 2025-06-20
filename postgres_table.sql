CREATE TABLE pbl_reinsurers (
	lei VARCHAR(50),
	osnazwa VARCHAR(150),
	centrkrajkod VARCHAR(5),
	centrkrajnazwa VARCHAR(100),
	osadrmiejsc VARCHAR(100),
	a_grupkap INT,
	lei_s VARCHAR(50),
	nazwa_s VARCHAR(150),
	krajkod_s VARCHAR(5),
	kodp_s VARCHAR(10),
	direct_parent VARCHAR(50), -- same as LEI
	ultimate_parent VARCHAR(50),
	record_ts TIMESTAMP DEFAULT current_timestamp
	-- CHECK (kodp_s LIKE '__-___') -- this only works for Polish postal codes
);