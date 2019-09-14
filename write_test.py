with open('test.nes', 'wb') as bin_file:
    # LDA $0008
    bin_file.write(b'\xAD')
    bin_file.write(b'\x00')
    bin_file.write(b'\x08')

    # ADC $12
    bin_file.write(b'\x69')
    bin_file.write(b'\x12')

    # STA ($09), X
    bin_file.write(b'\x81')
    bin_file.write(b'\x09')

    # BRK
    bin_file.write(b'\x00')

    # MEM 8~9
    bin_file.write(b'\xdf')
    bin_file.write(b'\x08')
