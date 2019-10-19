# import src.Decoder

class HashInstructions():
    def __init__(self, decoder):
        self.decoder = decoder

        self._instructions_hash_table = [self.decoder.brk] * 256

        # ADC
        self._instructions_hash_table[int('69', 16)] = self.decoder.adc_immediate
        self._instructions_hash_table[int('65', 16)] = self.decoder.adc_zero_page
        self._instructions_hash_table[int('75', 16)] = self.decoder.adc_zero_page_x
        self._instructions_hash_table[int('6D', 16)] = self.decoder.adc_absolute
        self._instructions_hash_table[int('7D', 16)] = self.decoder.adc_absolute_x
        self._instructions_hash_table[int('79', 16)] = self.decoder.adc_absolute_y
        self._instructions_hash_table[int('61', 16)] = self.decoder.adc_indirect_x
        self._instructions_hash_table[int('71', 16)] = self.decoder.adc_indirect_y

    
    def __getitem__(self, instruction_number):
        return self._instructions_hash_table[instruction_number]
