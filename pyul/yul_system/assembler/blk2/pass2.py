from yul_system.types import ONES, BAD_WORD, Bit, SwitchBit, HealthBit
from yul_system.assembler.pass2 import Pass2, Cuss

class Blk2Pass2(Pass2):
    def __init__(self, mon, yul, adr_limit, m_typ_tab):
        super().__init__(mon, yul, adr_limit, m_typ_tab)

        self.d1_params = [16383.0, 16384.0, 16383]
        self.k1_maxnum = 0o77777
        self.d2_params = [268435455.0, 268435456.0, 268435455]
        self.k2_maxnum = 0o7777777777
        self.con_mask = [39, 44]
        self.flag_mask = 0o7400007700000000
        self.pret_flag = 0o1000000000
        self.cons_flag = 0o2000000000
        self.misc_flag = 0o3000000000

        self._max_adres = 0
        self._ebank_reg = 0o3417
        self._sbank_reg = 0o40000000

        self.cuss_list = [
            # 0-2
            Cuss('CARD NUMBER OUT OF SEQUENCE     '),
            Cuss('NO "D" IN DECIMAL SUBFIELD      '),
            Cuss('ILLEGAL OR MIS-SPELLED OPERATION CODE   ', poison=True),

            # 3-5
            Cuss('IMPROPER LEFTOVER LOCATION FIELD FORMAT ', poison=True),
            Cuss('CONFLICT IN USE OF THIS LOCATION', poison=True),
            Cuss('LOCATION IS IN WRONG MEMORY TYPE', poison=True),

            # 6-8
            Cuss('OVERSIZE OR ILL-DEFINED LOCATION', poison=True),
            Cuss('INDEXING IS ILLEGAL HERE', poison=True),
            Cuss('ADDRESS FIELD IS MEANINGLESS    ', poison=True),

            # 9-11
            Cuss('"        " IS UNDEFINED ', poison=True),
            Cuss('RANGE ERROR IN VALUE OF ADDRESS ', poison=True),
            Cuss('IRREGULAR BUT ACCEPTABLE ADDRESS'),

            # 12-14
            Cuss('LEFTOVER WON\'T FIT IN MEMORY    ', poison=True),
            Cuss('ATTEMPT TO PREDEFINE LOCATION SYMBOL FAILED     ', poison=True),
            Cuss('"        " WON\'T FIT IN SYMBOL TABLE    ', poison=True),

            # 15-17
            Cuss('"        " WON\'T FIT IN SYMBOL TABLE    ', poison=True),
            Cuss('"        " ASSOCIATED WITH WRONG MEMORY TYPE    ', poison=True),
            Cuss('"        " ASSOCIATED WITH WRONG MEMORY TYPE    ', poison=True),

            # 18-20
            Cuss('"        " ASSOCIATED WITH CONFLICT     ', poison=True),
            Cuss('"        " ASSOCIATED WITH CONFLICT     ', poison=True),
            Cuss('"        " GIVEN OVERSIZE DEFINITION    ', poison=True),

            # 21-23
            Cuss('"        " GIVEN OVERSIZE DEFINITION    ', poison=True),
            Cuss('"        " GIVEN MULTIPLE DEFINITIONS   ', poison=True),
            Cuss('"        " GIVEN MULTIPLE DEFINITIONS   ', poison=True),

            # 24-26
            Cuss('"        " ASSOCIATED WITH MULTIPLE ERRORS      ', poison=True),
            Cuss('"        " ASSOCIATED WITH MULTIPLE ERRORS      ', poison=True),
            Cuss('"        " IS IN MISCELLANEOUS TROUBLE  ', poison=True),

            # 27-29
            Cuss('"        " IS IN MISCELLANEOUS TROUBLE  ', poison=True),
            Cuss('"        " WAS NEARLY DEFINED BY EQUALS ', poison=True),
            Cuss('ADDRESS DEPENDS ON UNKNOWN LOCATION     ', poison=True),

            # 30-32
            Cuss('"        " IS INDEFINABLY LEFTOVER      ', poison=True),
            Cuss('"        " MULTIPLY DEFINED INCLUDING NEARLY BY EQUALS  ', poison=True),
            Cuss('"        " MULTIPLY DEFINED INCLUDING BY EQUALS ', poison=True),

            # 33-35
            Cuss('ADDRESS IS IN BANK 00   ', poison=True),
            Cuss('ADDRESS IS INAPPROPRIATE FOR OP CODE    '),
            Cuss('ADDRESS         '),

            # 36-38
            Cuss('THIS INSTRUCTION SHOULD BE EXTENDED     ', poison=True),
            Cuss('THIS INSTRUCTION SHOULD NOT BE EXTENDED ', poison=True),
            Cuss('INEXACT DECIMAL-TO-BINARY CONVERSION    '),

            # 39-41
            Cuss('MORE THAN 10 DIGITS IN DECIMAL CONSTANT '),
            Cuss('RANGE ERROR IN CONSTANT FIELD   ', poison=True),
            Cuss('FRACTIONAL PART LOST BY TRUNCATION      '),

            # 42-44
            Cuss('MORE THAN 14 DIGITS IN OCTAL CONSTANT   '),
            Cuss('LOCATION FIELD SHOULD BE BLANK  '),
            Cuss('"        " WAS UNDEFINED IN PASS 1      ', poison=True),

            # 45-47
            Cuss('"        " WAS NEARLY DEFINED BY EQUALS IN PASS 1       ', poison=True),
            Cuss('LOCATION FIELD SHOULD BE SYMBOLIC       ', poison=True),
            Cuss('"        " WAS NEARLY DEFINED BY EQUALS ', poison=True),

            # 48-50
            Cuss('"        " MULTIPLY DEFINED INCLUDING NEARLY BY EQUALS  ', poison=True),
            Cuss('"        " IS INDEFINABLY LEFTOVER      ', poison=True),
            Cuss('"        " MULTIPLY DEFINED INCLUDING BY EQUALS ', poison=True),

            # 51-53
            Cuss('"        " SHOULDN\'T HAVE BEEN PREDEFINED       ', poison=True),
            Cuss('NUMERIC LOCATION FIELD IS ILLEGAL HERE  ', poison=True),
            Cuss('NO SUCH BANK OR BLOCK IN THIS MACHINE   ', poison=True),

            # 54-56
            Cuss('THIS BANK OR BLOCK IS FULL      ', poison=True),
            Cuss('ILLEGAL LOCATION FIELD FORMAT   ', poison=True),
            Cuss('CARD IGNORED BECAUSE IT\'S TOO LATE IN THE DECK  ', poison=True),

            # 57-59
            Cuss('CARD IGNORED BECAUSE IT MAKES MEMORY TABLE TOO LONG     ', poison=True),
            Cuss('NO MATCH FOUND FOR CARD NUMBER OR ACCEPTOR TEXT ', poison=True),
            Cuss('FIRST CARD NUMBER NOT LESS THAN SECOND  ', poison=True),

            # 60-62
            Cuss('QUEER INFORMATION IN COLUMN 1   '),
            Cuss('QUEER INFORMATION IN COLUMN 17  '),
            Cuss('QUEER INFORMATION IN COLUMN 24  '),

            # 63-65
            Cuss('BLANK ADDRESS FIELD EXPECTED    '),
            Cuss('ADDRESS FIELD SHOULD CONTAIN A POLISH OPERATOR  ', poison=True),
            Cuss('ERASED REGION SHOULD NOT CROSS E-BANKS  '),

            # 66-68
            Cuss('EBANK OR SBANK CONFLICT WITH 1-SHOT DECLARATION '),
            Cuss('FIRST POLISH OPERATOR ILLEGALLY INDEXED ', poison=True),
            Cuss('SECOND POLISH OPERATOR ILLEGALLY INDEXED', poison=True),

            # 69-71
            Cuss('NO MATCH FOUND FOR SECOND CARD NUMBER   ', poison=True),
            Cuss('EBANK OR SBANK CONFLICT ILLEGAL EXCEPT FOR BBCON, 2BCADR', poison=True),
            Cuss('THIS INSTRUCTION SHOULD BE INDEXED      '),

            # 72-74
            Cuss('INTERPRETIVE INSTRUCTION NOT EXPECTED   ', poison=True),
            Cuss('POLISH ADDRESS(ES) MISSING PRIOR TO THIS OP PAIR', poison=True),
            Cuss('STORE OP MUST BE NEXT OP AFTER STADR    ', poison=True),

            # 75-77
            Cuss('PUSHUP ILLEGAL BEFORE STORE OP WITHOUT STADR    ', poison=True),
            Cuss('LEFT OPCODE\'S MODE IN DISAGREES WITH MODE OUT SETTING   ', poison=True),
            Cuss('RIGHT OPCODE\'S MODE IN DISAGREES WITH MODE OUT SETTING  ', poison=True),

            # 78-80
            Cuss('ADDRESS HAS NO ASSOCIATED POLISH OPCODE ', poison=True),
            Cuss('INT OPCODE DID NOT CALL FOR INDEXING    ', poison=True),
            Cuss('INT OPCODE REQUIRES INDEXED ADDR HERE   ', poison=True),

            # 81-83
            Cuss('ADDRESS WORDS CROSS OVER BANK OR VAC AREA BOUNDARY      '),
            Cuss('INTERPRETIVE ADDR WORD OUT OF SEQUENCE  ', poison=True),
            Cuss('CAN NOT HANDLE NEG ADDRESSES WITH INDEXING HERE ', poison=True),

            # 84-86
            Cuss('D.P. CONSTANT SHOULD NOT CROSS BANKS    '),
            Cuss('ADDR MUST BE BASIC S.P. CONSTANT OR INST', poison=True),
            Cuss('POLISH WORDS REQUIRE BLANKS IN COLS 1, 17 AND 24', poison=True),

            # 87-89
            Cuss('PREVIOUS POLISH EQUATION NOT CONCLUDED PROPERLY ', poison=True),
            Cuss('POLISH PUSHUP REQUIRES NEGATIVE WORD HERE       ', poison=True),
            Cuss('POLISH ADDRESS EXPECTED HERE    ', poison=True),

            # 90-92
            Cuss('ASTERISK ILLEGAL ON THIS OP CODE', poison=True),
            Cuss('LOCATION SYMBOL IMPROPER ON STADR\'ED STORE WORD ', poison=True),
            Cuss(''),

            # 93-95
            Cuss('SUBROUTINE NAME NOT RECOGNIZED  ', poison=True),
            Cuss('MULTIPLE CALLS IN ONE PROGRAM OR SUBRO  '),
            Cuss('CONFLICT WITH EARLIER HEAD SPECIFICATION', poison=True),
        ]

    # Subroutine in pass 2 for AGC4 to form a word from an operation code and an addess (basic instruction
    # and address constants), or from two polish operator codes (polish operator words). The operation code(s)
    # and some associated information bits are taken from the health word of the current POPO item. The address is
    # obtained from the card via a general subroutine in pass 2 called PROC ADR. Implied addresses, bank errors, and
    # inappropriate addresses are checked for, and address value cussing is done.
    def m_proc_op(self, popo):
        if popo.health & Bit.BIT32:
            return self.int_op_cod(popo)

        # Insert basic op code into word.
        self._word = (popo.health >> 12) & (Bit.BIT34 | Bit.BIT35 | Bit.BIT36)

        # Maybe cuss illegal op code asterisk.
        if popo.health & Bit.BIT11:
            self.cuss_list[90].demand = True

        # Branch if no implied address.
        if popo.health & Bit.BIT31:
            # Determine addresses implied by special op codes.
            # Keep assembler's EBANK reg. up to date.
            self._max_adres = 0o167777
            self.ebk_loc_q()

            if not (popo.address_1().isspace() and popo.address_2().isspace()):
                # Mildly cuss nonblank adr fld, proceed.
                self.cuss_list[63].demand = True

            # Maybe cuss indexing of implads.
            if self._yul.switch & SwitchBit.PREVIOUS_INDEX:
                self.cuss_list[7].demand = True

            # Branch if implad is not in health word.
            if (popo.health & Bit.BIT27) == 0:
                # Supply implied address.
                self._address = (popo.health >> 18) & 0o7

                # Branch if not code 1 (here, NOOP).
                if self._word == Bit.BIT36:
                    # Form of NOOP depends on which memory.
                    if self._location < 0o4000:
                        # In E memory, NOOP = CA A
                        self._word = 0o30000
                    else:
                        # In F memory, NOOP = TCF +1
                        self._address = self._location + 1

            else:
                # Place quarter-code bits in instr. word.
                self._word |= (popo.health >> 9) & 0o6000

                # Three-way branch on bits 14,13 of word.
                b13b14 = (self._word >> 12) & 3
                if b13b14 == 0:
                    # Ed Smally's rupt is peripheral code 7.
                    self._word |= Bit.BIT39
                    self._address = 0
                elif b13b14 == 1:
                    # Three-way branch on quarters of code 5.
                    qc = (self._word >> 10) & 3
                    if qc == 0:
                        # RESUME = INDEX 17.
                        self._address = 0o17
                    elif qc == 1:
                        # Pick 1 of 2 implied addresses for DXCH.
                        if ((popo.health >> 18) & 1) == 0:
                            # DTCF = DXCH FBANK.
                            self._address = 5
                        else:
                            # DTCB = DXCH Z.
                            self._address = 6
                    else:
                        # Pick 1 of 2 implied addresses for TS.
                        if ((popo.health >> 18) & 1) == 0:
                            # OVSK = TS A.
                            self._address = 0
                        else:
                            # TCAA =  TS Z.
                            self._address = 5
                else:
                    # Two-way branch on quarters of code 2.
                    qc = (self._word >> 10) & 1
                    if qc == 0:
                        # DAS A = DDOUBL (D.P. DOUBLE).
                        self._address = 1
                    else:
                        # LXCH 7 = ZL (Zero L), QXCH 7 = ZQ.
                        self._address = 7

            # Isolate extracode bit of implad code.
            m_common = (popo.health << 8) & SwitchBit.EXTEND

            # Plant extracode flag for simulator.
            self._word |= (m_common << 10) | (m_common << 11)

            # Bit 29 places op-address print split.
            popo.health &= ~0o3000000
            popo.health |= (popo.health >> 2) & 0o3000000

            # Branch if extended basic or unex. extra.
            if (self._yul.switch & SwitchBit.EXTEND) != m_common:
                if m_common == 0:
                    # Error was unextended extracode.
                    self.cuss_list[36].demand = True
                else:
                    # Error was an extended basic code.
                    self.cuss_list[37].demand = True

            else:
                # Branch if this is the "EXTEND" code.
                if popo.health & Bit.BIT26:
                    # Set extension switch.
                    self._yul.switch |= SwitchBit.EXTEND
                    return self.add_adr_wd(popo)

            # Clear extension switch.
            self._yul.switch &= ~SwitchBit.EXTEND
            return self.basic_adr(popo)

    def add_adr_wd(self, popo):
        pass

    def basic_adr(self, popo):
        pass

    def ebk_loc_q(self):
        # Tentatively accept EBANK declaration.
        self._ebank_reg &= ~0o3400
        self._ebank_reg |= (self._ebank_reg << 8) & 0o344

        # Tentatively accept SBANK declaration.
        self._sbank_reg &= ~0o160000
        self._sbank_reg |= (self._sbank_reg >> 5) & 0o160000

        # If in fixed, go see if in superbank.
        if self._location < 0o4000:
            # Exit if location is not in an Ebank.
            if self._location <= 0o1377:
                return

            # Branch on old-Ebank-declaration bit.
            if (self._ebank_reg & 0o77) < 8:
                # Check on new permanent declaration.
                if (self._ebank_reg & 0o3400) != (self._location & 0o3400):
                    # E(S)Bank conflict with location.
                    self.cuss_list[70].demand = True

            # Force agreement and exit.
            self._ebank_reg &= ~0o3400
            self._ebank_reg |= self._location & 0o3400
            return

        # Exit if location not in a superbank.
        if self._location <= 0o67777:
            return

        # Exit if location has no value.
        if self._location >= ONES:
            return

        location = self._location - 0o10000

        # Branch on old-Sbank-declaration bits
        if (self._sbank_reg & 0o70000000) == 0:
            # Check up on new permanent declaration.
            if (self._sbank_reg & 0o160000) != (location & 0o160000):
                # E(S)Bank conflict with location.
                self.cuss_list[70].demand = True

        # Force agreement and exit.
        self._sbank_reg &= ~0o160000
        self._sbank_reg |= location & 0o160000

    def int_op_cod(self, popo):
        pass

    # Subroutine in pass 2 for BLK2 to set in print a right-hand location for such as SETLOC.
    # Puts in the bank indicator, if any. Blots out an invalid location.
    def m_ploc_is(self, location):
        if location >= ONES:
            # Blot out bad location and exit.
            self._line[42] = '■■■■'
            return

        # Branch if location is in erasable.
        if location > 0o3777:
            # Branch if location is not in a bank.
            if location > 0o7777:
                # Reduce to standard bank notation.
                location -= 0o10000
                bank_no = location >> 10

                # Set bank number in print.
                self._line[39] = '%02o,' % bank_no

                # Put subaddress in the range 2000 - 3777.
                location = (location | 0o2000) & 0o3777

        else:
            if location > 0o1377:
                # Set bank number in print.
                bank_no = location >> 8
                self._line[39] = 'E%o,' % bank_no

                # Put subaddress in the range 1400 - 1777
                location = (location | 0o1400) & 0o1777

        # Set location in print and exit.
        self._line[42] = '%04o' % location

    # Subroutine in pass 2 for BLK2 to set in print the location of an instruction or constant, with bank
    # number if any and with a notation for end of block or bank if required. Blots out location field if bad loc.
    def m_ploc_eb(self, location, popo, dp=False):
        # Branch if theres a valid location.
        if location >= ONES:
            # Blot out location field and exit.
            self._line[32] = '■■■■'
            return

        orig_loc = location
        check_end = True

        # Branch if location is in erasable.
        if location > 0o3777:
            # Branch if location begins bank or FF/2.
            if (location & 0o1777) == 0:
                self.dp_cross_q(dp)

            # Branch if location is not in a bank.
            if location > 0o7777:
                # Reduce to standard bank notation.
                location -= 0o10000
                bank_no = location >> 10

                # Set bank number in print.
                self._line[29] = '%02o,' % bank_no

                # Put subaddress in the range 2000 - 3777.
                location = (location | 0o2000) & 0o3777

        else:
            # Branch if not an ERASE card.
            if (popo.health & HealthBit.CARD_TYPE_MASK) == HealthBit.CARD_TYPE_ERASE:
                # Branch if ERASE crosses Ebank boundary.
                if (location & 0o3400) != (popo.health & 0o3400):
                    self.cuss_list[65].demand = True

            # Branch if location begins Ebank.
            if (location & 0o377) == 0:
                self.dp_cross_q(dp)

            # Branch if location is not in an Ebank.
            if location > 0o1377:
                # Set Ebank number in print.
                bank_no = location >> 8
                self._line[29] = 'E%o,' % bank_no

                # Put subaddress in the range 1400 - 1777
                location = (location | 0o1400) & 0o1777
            else:
                check_end = False

        # Branch if not end of block or bank.
        if check_end and (orig_loc & 0o1777) == 0o1777:
            # "EB" precedes such locations.
            self._line[24] = '  EB'
        else:
            midx = 0
            # Branch when memory type category found.
            while orig_loc > self._m_typ_tab[midx][1]:
                midx += 1
            # Branch if not end of minor block.
            if orig_loc == self._m_typ_tab[midx][1]:
                # Mark line "MC" for memory type change.
                self._line[24] = '  MC'

        # Set up location in print and exit.
        self._line[32] = '%04o' % location

    # Minor subroutine in pass 2 for BLK2 to cuss a double precision constant that crosses a bank boundary.
    def dp_cross_q(self, dp):
        if dp:
            self.cuss_list[84].demand = True

    # Subroutine in pass 2 for BLK2 to set up a single-precision constant in word and in print. This subroutine
    # does not care whether the word is signed or not, but demands the output of dec/oct const in number.
    def m_proc_1p(self, popo, number):
        # Branch if word is valid.
        if number == BAD_WORD:
            self._line[39] = '■■■■■'
            self._word = number
            return

        # Isolate magnitude
        self._word = number & ~(Bit.BIT1)
        if not number & Bit.BIT1:
            # Complement negative word.
            self._word ^= 0o77777

        # Set word in print.
        self._line[39] = '%05o' % self._word

        # Apply internal constant flag and exit
        dec6_flag = Bit.BIT2 | Bit.BIT3
        self._word |= dec6_flag

    # Subroutine in pass 2 for BLK2 to process a single-precision constant. Using the output of DEC CONST or
    # OCT CONST, and distinguishing between the signed and unsigned possibilities (for octal constants only),
    # sets up the high-order part in word and the low-order part in sec_half, sets the high-order part in print,
    # and sets up the low-order part in printable form in sec_alf.
    def m_proc_2p(self, popo, number, e_number):
        # Branch if constant is valid.
        if number == BAD_WORD:
            # Prepare blots for low-order part.
            sec_alf = '■■■■■'
            self._line[39] = '■■■■■'
            self._word = number
            return BAD_WORD, sec_alf

        # Branch if number is signed.
        if e_number != 0:
            # Set up unsigned constant.
            self._word = (number >> 14) & 0o37777
            common = 0o37777
        else:
            # Set up signed constant.
            self._word = (number >> 15) & 0o77777
            common = 0o77777

        # Isolate low-order part.
        sec_half = number & common

        # Branch if no minus sign.
        if not number & Bit.BIT1:
            # Complement halves of negative constant.
            self._word ^= 0o77777
            sec_half ^= 0o77777

        # Make printable version of low-order part
        sec_alf = '%05o' % sec_half

        dec6_flag = Bit.BIT2 | Bit.BIT3
        sec_half |= dec6_flag

        # Set word in print.
        self._line[39] = '%05o' % self._word

        # Apply internal constant flag and exit
        self._word |= dec6_flag

        return sec_half, sec_alf
