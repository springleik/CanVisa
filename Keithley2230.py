# compose tree to describe object dictionary
# assume all instrument readings are four-byte floats
theTree = {
	0x1000: {
		0x00: {0x40: 0, 'size': 4}
	},
	0x6001: {
		0x00: {0x40: 5},
		0x01: {0x40: 'INST:SEL CH1;:SOUR:VOLT?', 0x23: 'INST:SEL CH1;:SOUR:VOLT'},
		0x02: {0x40: 'INST:SEL CH1;:SOUR:CURR?', 0x23: 'INST:SEL CH1;:SOUR:CURR'},
		0x03: {0x40: 'FETCH:VOLT? CH1'},
		0x04: {0x40: 'FETCH:CURR? CH1'},
		0x05: {0x40: 'FETCH:POW? CH1'}
	},
	0x6002: {
		0x00: {0x40: 5},
		0x01: {0x40: 'INST:SEL CH2;:SOUR:VOLT?', 0x23: 'INST:SEL CH2;:SOUR:VOLT'},
		0x02: {0x40: 'INST:SEL CH2;:SOUR:CURR?', 0x23: 'INST:SEL CH2;:SOUR:CURR'},
		0x03: {0x40: 'FETCH:VOLT? CH2'},
		0x04: {0x40: 'FETCH:CURR? CH2'},
		0x05: {0x40: 'FETCH:POW? CH2'}
	},
	0x6003: {
		0x00: {0x40: 5},
		0x01: {0x40: 'INST:SEL CH3;:SOUR:VOLT?', 0x23: 'INST:SEL CH3;:SOUR:VOLT'},
		0x02: {0x40: 'INST:SEL CH3;:SOUR:CURR?', 0x23: 'INST:SEL CH3;:SOUR:CURR'},
		0x03: {0x40: 'FETCH:VOLT? CH3'},
		0x04: {0x40: 'FETCH:CURR? CH3'},
		0x05: {0x40: 'FETCH:POW? CH3'}
	}
}
