from yul_system.types import ONES, BAD_WORD, Bit, SwitchBit, HealthBit
from yul_system.assembler.pass2 import Pass2, Cuss

class Blk2Pass2(Pass2):
    def __init__(self, mon, yul, adr_limit, m_typ_tab):
        super().__init__(mon, yul, adr_limit, m_typ_tab)

        self.d1_params = [16383.0, 16384.0, 16383]
        self.k1_maxnum = 0o77777
        self.d2_params = [268435455.0, 268435456.0, 268435455]
        self.k2_maxnum = 0o7777777777
        self.mm_params = [99.0, 16384.0, 99]
        self.vn_params = [9999.0, 16384.0, 9999]
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
            return self.implad(popo)

        return self.no_implad(popo)

    def implad(self, popo):
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

        adr_wd = [self._address, self._address]

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
                return self.add_adr_wd(popo, adr_wd)

        # Clear extension switch.
        self._yul.switch &= ~SwitchBit.EXTEND
        return self.basic_adr(popo, adr_wd)

    # Process explicit addresses for instructions or constants.
    def no_implad(self, popo):
        # Branch if instruction, not adr constant.
        b25t27m = Bit.BIT25 | Bit.BIT26 | Bit.BIT27
        if (popo.health & b25t27m) != b25t27m:
            return self.non_const(popo)

        # Branch on level of address constant.
        level = (popo.health >> 24) & 3
        b28t30m = Bit.BIT28 | Bit.BIT29 | Bit.BIT30
        adr_con_4 = 0o4000000
        if level == 0:
            # Level 0: basic address constants.
            dec_6_flag = Bit.BIT2 | Bit.BIT3
            self._word |= dec_6_flag

            # Br if ECADR, BBCON, 2FCADR, or 2(B)CADR.
            if (popo.health & b28t30m) < adr_con_4:
                # ADRES,REMADR,GENADR,FCADR,SBANK=,BNKSUM.
                self._max_adres = 0o167777
                return self.max_ad_set(popo, update_ebank=False)
            elif (popo.health & b28t30m) == adr_con_4:
                # E-addresses only for ECADR, EBANK=.
                self._max_adres = 0o3777
                return self.max_ad_set(popo, update_ebank=False)

            return self.dp_adr_con(popo)

        elif level == 1:
            # Branch for polish addr or store codes.
            if (popo.health & b28t30m) < 0o3000000:
                # FIXME
                pass

            # Rest of level 1: EBANK=, SBANK=, BNKSUM.
            self._location = ONES

            # Maybe cuss nonblank loc field.
            if popo.health & Bit.BIT8:
                self.cuss_list[43].demand = True

            # Select EBANK=, SBANK=, or BNKSUM.
            op_type = (popo.health >> 17) & 0o7
            if op_type == 0:
                # E-addresses only for ECADR, EBANK=.
                self._max_adres = 0o3777
                return self.max_ad_set(popo, update_ebank=False)

            elif op_type == 2:
                # ADRES,REMADR,GENADR,FCADR,SBANK=,BNKSUM.
                self._max_adres = 0o167777
                return self.max_ad_set(popo, update_ebank=False)

            else:
                return self.dp_adr_con(popo)

        else:
            # Level 3: special decimal constants.
            self.cuss_list[90].demand = False
            return self.mm_vn(popo)

    # Level 3 address constants: special decimal constants.
    def mm_vn(self, popo):
        # Set general MXR and delimiting asterisk.
        card = self.delimit(popo)

        # Cuss queer info in columns a la decimal.
        if popo.card[0] != ' ' and popo.card[0] != 'J':
            self.cuss_list[60].demand = True
        if popo.card[16] != ' ':
            self.cuss_list[61].demand = True
        if popo.card[23] != ' ':
            self.cuss_list[62].demand = True

        code = (popo.health >> 17) & 2
        if code == 0:
            # MM = DEC with limit of 99.
            number,_ = self.dec_const(card, *self.mm_params)
            return self.m_proc_1p(popo, number)

        else:
            # First do DEC with limit of 9999.
            number,_ = self.dec_const(card, *self.vn_params)
            # If bad word treat VN like DEC.
            if number == BAD_WORD:
                return self.m_proc_1p(popo, number)

            # Isolate verb in m_common.
            m_common = [0, 0]
            m_common[0] = int((number & ~Bit.BIT1) / 100)

            # Isolate noun in m_cmmon +1.
            m_common[1] = int(number % 100)

            # Store verb and noun as 7-bit groups.
            number = (number & Bit.BIT1) | (m_common[0] << 7) | m_common[1]

            # Finish up a la dec.
            return self.good_1p(popo, number)

    def dp_adr_con(self, popo):
        # Branch if BBCON (single precision)
        b29t30m = Bit.BIT29 | Bit.BIT30
        if (popo.health & b29t30m) > Bit.BIT30:
            # Make return go to D.P. constant proc.
            self._dp_inst = True
            # Prepare for the worst.
            self._sec_half = BAD_WORD
            self._sec_alf = '■■■■■■■■■■■■■■■■'

            # Branch if 2FCADR or BNKSUM (no er prob).
            if (popo.health & b29t30m) <= Bit.BIT29:
                self._max_adres = 0o167777
                return self.max_ad_set(popo, update_ebank=False)

        # Keep assembler's EBANK reg. up to date.
        self.ebk_loc_q(accept_temp=False)

        # May erase EBANK or SBANK conflict cuss.
        self.cuss_list[70].demand = False

        return self.set_ebcon(popo, check_oneshot=True)

    def non_const(self, popo):
        # Place quarter-code bits in instr. word.
        self._word |= (popo.health >> 12) & (Bit.BIT37 | Bit.BIT38)

        # Branch if peripheral code.
        b29t30m = Bit.BIT29 | Bit.BIT30
        if (popo.health & b29t30m) < b29t30m:
            # Set switch if this is an INDEX order.
            if popo.health & Bit.BIT27:
                self._yul.switch |= SwitchBit.CURRENT_INDEX
            else:
                self._yul.switch &= ~SwitchBit.CURRENT_INDEX

        # Isolate extracode bit of explad code.
        m_common = (popo.health << 11) & Bit.BIT17

        # Branch if ext. basic or unex. extracode.
        if m_common == (self._yul.switch & SwitchBit.EXTEND):
            # Clear extension switch.
            self._yul.switch &= ~SwitchBit.EXTEND
            return self.set_min_ad(popo, m_common)

        # Branch if extended basic code error.
        if m_common == Bit.BIT17:
            # Cuss at unextended extracode.
            self.cuss_list[36].demand = True
            return self.set_min_ad(popo, m_common)

        # Branch if not an INDEX order.
        if popo.health & Bit.BIT27:
            # Extended INDEX extends, can refer 2 any.
            popo.health &= ~(Bit.BIT29 | Bit.BIT30)
            m_common = Bit.BIT17
            return self.set_min_ad(popo, m_common)

        # Cuss any extended basic code but INDEX.
        self.cuss_list[37].demand = True
        self._yul.switch &= ~SwitchBit.EXTEND
        return self.set_min_ad(popo, m_common)

    def set_min_ad(self, popo, m_common):
        # Plant extracode flag for simulator.
        self._word |= m_common >> 10
        self._word |= m_common >> 11

        # In general, allow values down to -7777.
        self._min_adres = -0o7777

        # 4-way branch on memory type allowance.
        types = (popo.health >> 18) & 0o3

        b34t36m = (Bit.BIT34 | Bit.BIT35 | Bit.BIT36)
        if types == 0:
            # No restriction.
            self._max_adres = 0o167777

            # Branch if negative address is permitted.
            if (self._word & b34t36m) == 0o40000:
                # Negative address here would be overflow.
                self._min_adres = 0

        elif types == 1:
            # Ditto now, fixed only later.
            self._max_adres = 0o167777

        elif types == 2:
            # E-memory or indexed (quarter-code).
            self._max_adres = 0o11777

        else:
            # Peripheral code. Supply last p-code bit.
            self._word |= (popo.health >> 12) & Bit.BIT39
            # Here allow values down to -777.
            self._min_adres = -0o777
            self._max_adres = 0o777

        # If op code is double precision, add 1 to address value.
        dp_check = (popo.health >> 19) & 0o2

        # Add 00001 to double precision addresses.
        if dp_check == 0:
            # Branch if basic code and not D.P.
            b33t38m = 0o176000
            if (self._word & b33t38m) in (0o20000, 0o52000):
                self._yul.switch |= SwitchBit.DP_OPCODE

        else:
            # If not DCA, check for DCS.
            if (self._word & b34t36m) in (0o30000, 0o40000):
                self._yul.switch |= SwitchBit.DP_OPCODE

        return self.max_ad_set(popo)

    def max_ad_set(self, popo, update_ebank=True):
        # Except for EBNAK=, SBANK=, BNKSUM:
        if update_ebank or self._location >= ONES:
            # Keep assembler's EBANK reg. up to date.
            self.ebk_loc_q()

        # Translate address field.
        self.proc_adr(popo)

        # Restore min adr value.
        self._min_adres = 0

        # Cuss lack of "D" in decimal subfield.
        if popo.health & Bit.BIT9:
            self.cuss_list[1].demand = True

        # Go see if current word is polish (FIXME)

        adr_wd = [self._address, self._address]

        # Br. if meaningless or atrocious address.
        if self._address >= ONES:
            return self.rng_error(popo, adr_wd, cuss_range=False)

        # Increment address of D.P. code.
        if self._yul.switch & SwitchBit.DP_OPCODE:
            adr_wd[1] += 1

        # Branch if address size OK for this op.
        if adr_wd[0] > self._max_adres:
            return self.rng_error(popo, adr_wd, check_size=True)

        # Go process instruction if no const flag.
        b25t27m = Bit.BIT25 | Bit.BIT26 | Bit.BIT27
        if (popo.health & b25t27m) != b25t27m:
            return self.instrop(popo, adr_wd)

        # Branch if not type 0 address constant.
        if popo.health & Bit.BIT24:
            return self.adr_con_1(popo, adr_wd)

        # Select procedure for type 0 address constants.
        # May put prefix on ECADR for downlist.
        self._word |= (popo.health >> 16) & 0o74000

        # Select procedure for 1 of 8 adr consts.
        proc = (popo.health >> 18) & 0x7
        if proc == 0:
            # Adres is just like TC (except for flag).
            if self._address <= 0o3777:
                return self.basic_adr(popo, adr_wd)
            else:
                return self.adres_adr(popo, adr_wd)
        elif proc == 1:
            # Like ADRES, but must be different bank.
            return self.remadr(popo, adr_wd)
        elif proc == 2:
            # Complete address for fixed memory.
            return self.fcadr(popo, adr_wd)
        elif proc == 3:
            # Like adres, but no bank-error checks.
            return self.genadr(popo, adr_wd)
        elif proc == 4:
            # Complete address for erasable memory.
            return self.add_adr_wd(popo, adr_wd)
        elif proc == 5:
            # Both-bank constant, 5 bits and 3 bits.
            return self.bbcon(popo, adr_wd)
        elif proc == 6:
            # FCADR (for FB) followed by GENADR.
            self._sec_half = self._address
            return self._2fcadr(popo, adr_wd)
        else:
            # GENADR followed by BBCON (for BB).
            self._sec_half = self._address
            return self._2bcadr(popo, adr_wd)

    # Specific processing for 6 of the 8 type 0 address constants.
    def remadr(self, popo, adr_wd):
        # Branch if address is in erasable.
        if self._address > 0o3777:
            # Exit if address is in fixed-fixed.
            if self._address <= 0o7777:
                return self.add_adr_wd(popo, adr_wd)

            # Branch happily if loc. not in an FBANK.
            if self._location > 0o7777:
                # OK if loc. and adr. in different banks.
                if (self._location & 0o176000) == (self._address & 0o176000):
                    return self.cus_f_bank(popo, adr_wd)

            # Put subaddress in the range 2000-3777
            adr_wd[0] &= ~0o176000
            adr_wd[0] |= 0o2000
            return self.add_adr_wd(popo, adr_wd)

        # Exit if address is not in an EBANK.
        if self._address <= 0o1377:
            return self.add_adr_wd(popo, adr_wd)

        # OK if we have a pseudo EBANK. OK if loc and adr in different EBANKs.
        if (((self._ebank_reg & 0o3400) <= 0o1000) or
            ((self._address & 0o3400) != (self._ebank_reg & 0o3400))):
            # Put subaddress in the range 1400-1777
            adr_wd[0] &= ~0o3400
            adr_wd[0] |= 0o1400
            return self.add_adr_wd(popo, adr_wd)

        return self.cus_e_bank(popo, adr_wd)

    def fcadr(self, popo, adr_wd):
        # Address in erasable or fixfix illegal.
        if self._address <= 0o7777:
            return self.rng_error(popo, adr_wd)

        # Put CADR in the range 00000-77777.
        adr_wd[0] -= 0o10000

        # Branch if address isn't in a super-bank.
        if adr_wd[0] <= 0o57777:
            return self.add_adr_wd(popo, adr_wd)

        # Branch if there is no superbank setting.
        b33t35m = Bit.BIT33 | Bit.BIT34 | Bit.BIT35
        if (self._sbank_reg & b33t35m) > 0:
            # Branch to cuss superbank error.
            if (adr_wd[0] & b33t35m) != (self._sbank_reg & b33t35m):
                self.sbank_cus(adr_wd[0])

        adr_wd[0] &= ~b33t35m
        adr_wd[0] |= 0o60000
        return self.add_adr_wd(popo, adr_wd)

    def genadr(self, popo, adr_wd):
        # Branch if address is in erasable memory.
        if self._address > 0o3777:
            # All done if in fixed-fixed.
            if self._address <= 0o7777:
                return self.add_adr_wd(popo, adr_wd)

            # Put subaddress in the range 2000-3777
            adr_wd[0] &= ~0o176000
            adr_wd[0] |= 0o2000
            return self.add_adr_wd(popo, adr_wd)

        # All done if address in unswitched eras.
        if self._address <= 0o1377:
            return self.add_adr_wd(popo, adr_wd)

        adr_wd[0] &= ~0o3400
        adr_wd[0] |= 0o1400
        return self.add_adr_wd(popo, adr_wd)

    def bbcon(self, popo, adr_wd):
        # If not in fixed, should be bank number.
        if self._address <= 0o3777:
            # Address in erasable illegal here.
            if self._address >= 0o70:
                return self.rng_error(popo, adr_wd)

            # Set FB part of BBCON from bank number.
            self._address <<= 10

        elif self._address <= 0o7777:
            # No reduction needed if in fixed-fixed.
            return self.bbc_adres(popo, adr_wd, supply_sbank=True)

        else:
            self._address -= 0o10000

        # Branch if address isn't in a super-bank.
        if self._address <= 0o57777:
            return self.bbc_adres(popo, adr_wd, supply_sbank=True)

        # Branch if no 1-shot SBANK=.
        b25t27m = Bit.BIT25 | Bit.BIT26 | Bit.BIT27
        if (self._sbank_reg & b25t27m) == 0:
            # Shift address superbits to match temps.
            b28t30m = Bit.BIT28 | Bit.BIT29 | Bit.BIT30
            sec_alf = (self._address << 5) & b28t30m

            # May cuss address confl w/ 1-shot decl.
            if sec_alf != (self._sbank_reg & b28t30m):
                self.cuss_list[66].demand = True

            # Plant super-bank bits in BBCON word.
            b41t44m = Bit.BIT41 | Bit.BIT42 | Bit.BIT43 | Bit.BIT44
            self._word &= ~b41t44m
            self._word |= (self._address >> 9) & b41t44m

            # Reduce bank number to 3X.
            self._address &= ~0o160000
            self._address |= 0o60000
            return self.bbc_adres(popo, adr_wd)

        return self.bbc_adres(popo, adr_wd, supply_sbank=True)

    def bbc_adres(self, popo, adr_wd, supply_sbank=False):
        if supply_sbank:
            # Supply declared SBANK or 0 if none.
            b41t44m = Bit.BIT41 | Bit.BIT42 | Bit.BIT43 | Bit.BIT44
            self._word &= ~b41t44m
            self._word |= (self._sbank_reg >> 14) & b41t44m

        # Set FB part of BBCON from address.
        self._word &= ~0o176000
        self._word |= self._address & 0o176000

        # Insert 1-shot or established EBANK no.
        self._word |= self._ebank_reg & 0o7
        return self.gud_basic(popo, adr_wd)

    # Type 0 address constants concluded: double precision types.

    def _2fcadr(self, popo, adr_wd):
        if self._address < 0o4000:
            # Error exit if refers to erasable.
            self._sec_half = BAD_WORD
            return self.rng_error(popo, adr_wd)

        # All done if in fixed-fixed.
        if self._address <= 0o7777:
            return self.print_2pa(popo, adr_wd)

        # Put CADR in the range 00000-77777.
        adr_wd[0] -= 0o10000

        # Branch if address isn't in a super-bank.
        if (adr_wd[0] & 0o177777) > 0o57777:
            # Branch if there is no superbank setting.
            b33t35m = Bit.BIT33 | Bit.BIT34 | Bit.BIT35
            if (self._sbank_reg & b33t35m) > 0:
                # Branch to cuss superbank error.
                if (adr_wd[0] & b33t35m) != (self._sbank_reg & b33t35m):
                    self.sbank_cus(adr_wd[0])

                # Reduce bank 4X, 5X, or 6X to 3X.
                adr_wd[0] &= ~b33t35m
                adr_wd[0] |= 0o60000

        # Put GENADR in the range 2000-3777, exit.
        self._sec_half &= ~0o176000
        self._sec_half |= 0o2000
        return self.print_2pa(popo, adr_wd)

    def _2bcadr(self, popo, adr_wd):
        # Isolate bank number in BBCON word.
        self._sec_half &= ~0o1777

        # Supply declared SBANK or 0 if none.
        self._sec_half |= (self._sbank_reg >> 14) & 0o360

        # Branch if refers to erasable.
        if self._address <= 0o3777:
            # Branch if refers to an EBANK.
            if 0o1400 <= self._address:
                # Here use EBANK acording to address.
                self._sec_half |= (self._address >> 8) & 0o2007

                # Branch if there is no 1-shot declaratn.
                if (self._ebank_reg & 0o77) < 8:
                    # Otherwise check for conflict.
                    if (self._sec_half & 0o7) != (self._ebank_reg & 0o7):
                        # E(S)BANK conflict with 1-shot declare.
                        self._cuss_list[66].demand = True

                # Put GENADR in the range 1400-1777, exit.
                adr_wd[0] &= ~0o3400
                adr_wd[0] |= 0o1400
                return self.print_2pa(popo, adr_wd)

        # Branch if refers to fixed-fixed.
        elif self._address <= 0o7777:
            pass

        else:
            # Reduce bank number in BBCON word.
            self._sec_half -= 0o10000

            # Branch if address isn't in a super-bank.
            if self._sec_half > 0o57777:
                # Branch if no 1-shot SBANK=.
                if self._sbank_reg & (Bit.BIT25 | Bit.BIT26 | Bit.BIT27) == 0:
                    # Shift address superbits to match temps.
                    b28t30m = Bit.BIT28 | Bit.BIT29 | Bit.BIT30
                    sec_alf = (self._sec_half << 5) & b28t30m
                    # Maybe cuss address confl w/ 1-shot decl.
                    if sec_alf != (self._sbank_reg & b28t30m):
                        # E(S)BANK conflict with 1-shot declare.
                        self._cuss_list[66].demand = True

                # Plant super-bank bits in BBCON word.
                self._sec_half |= (self._sec_half >> 9) & 0o360

                # Reduce bank 4X, 5X, or 6X to 3X.
                self._sec_half &= ~(Bit.BIT33 | Bit.BIT34 | Bit.BIT35)
                self._sec_half |= 0o60000

            # Put GENADR in the range 2000-3777.
            adr_wd[0] &= ~0o176000
            adr_wd[0] |= 0o2000

        self._sec_half |= self._ebank_reg & 0o7
        return self.print_2pa(popo, adr_wd)

    def print_2pa(self, popo, adr_wd):
        # Branch if no minus in column 17.
        if popo.card[16] == '-':
            self._sec_half ^= 0o77777

        # Tweak and use part of 2DEC, 2OCT.
        dec6_flag = Bit.BIT2 | Bit.BIT3

        # Make printable version of low-order part
        self._sec_alf = '%05o' % self._sec_half
        self._sec_half |= dec6_flag

        # Restore it and exit.
        return self.add_adr_wd(popo, adr_wd)

    def sbank_cus(self, adr_wd):
        # Set up bank error cuss for filling in.
        self._yul.switch &= ~SwitchBit.PREVIOUS_INDEX
        self.cuss_bank()
        cuss = self.cuss_list[33]
        bank_no = adr_wd >> 13
        # Form "ADDRESS IS IN BANK SN".
        cuss.msg = cuss.msg[:19] + ('S%o' % bank_no) + cuss.msg[21:]

    def rng_error(self, popo, adr_wd, cuss_range=True, check_size=False):
        if cuss_range:
            # Branch if address too big to print.
            if (not check_size) or (adr_wd[0] < 0o170000):
                # If not atrocious, tell him what it is.
                self.cuss_list[35].demand = True
                self.prb_adres(self._address)

            # Cuss range error in address value.
            self.cuss_list[10].demand = True

        # Branch if instruction or address const.
        if (popo.health & HealthBit.CARD_TYPE_MASK) <= HealthBit.CARD_TYPE_ILLOP:
            return self.bad_basic(popo)

        # Cuss rang err in EBANK=, SBANK=, BNKSUM.
        code = (popo.health >> 18) & 0o3

        # Disposition of EBANK=, SBANK=, and BNKSUM if address is bad.
        if code == 0:
            self._line[44] = 'E■'
            self._zequaloc = True

        elif code == 1:
            self._line[44] = 'S■'
            self._zequaloc = True

        else:
            # Bad location value flag.
            popo.health |= Bit.BIT14

            # Join end of BNKSUM procedure.
            # FIXME

    def adr_con_1(self, popo, adr_wd):
        code = popo.health & (Bit.BIT28 | Bit.BIT29 | Bit.BIT30)
        if code <= 0:
            # Branch to EBANK= code.
            return self.ebank2(popo, adr_wd)

        elif code <= Bit.BIT30:
            # Branch to SBANK= code.
            return self.sbank2(popo, adr_wd)

        else:
            # Go to other bank to process BNKSUM code.
            return self.bnksum(popo, adr_wd)

    # Action of 'SBANK=' code upon assembler's S bank reg.
    def sbank2(self, popo, adr_wd):
        # Address must be in a super-bank.
        if self._address <= 0o67777:
            return self.rng_error(popo, adr_wd)

        self._address -= 0o10000

        # Set up temp. superbits, call it 1-shot.
        char5m = 0o77000000
        self._sbank_reg &= ~char5m
        self._sbank_reg |= (self._address << 5) & char5m

        # Print declared superbank no. as "SN".
        self._line[44] = 'S%o' % ((self._sbank_reg >> 18) & 0o77)

        # Exit, bypassing word processing.
        self._zequaloc = True

    # Action of 'EBANK=' code upon assembler's E bank reg.
    def ebank2(self, popo, adr_wd):
        # Branch if EBANK number implied by adr.
        if self._address < 8:
            # Use EBANK number directly.
            self._ebank_reg &= ~0o77
            self._ebank_reg |= self._address

        else:
            # Plant EBANK no. in tentative position.
            self._ebank_reg &= ~0o77
            self._ebank_reg |= (self._address >> 8) & 0o77

        # Print declared EBANK no. as "EN".
        self._line[44] = 'E%o' % (self._ebank_reg & 0o7)

        # Exit, bypassing word processing.
        self._zequaloc = True

    def bnksum(self, popo, adr_wd):
        # FIXME
        pass

    def set_ebcon(self, popo, check_oneshot=False):
        # Bypass update if 1-shot declaration.
        if check_oneshot and ((self._ebank_reg & 0o77) > 7):
            # Position current setting for BBCON fmt.
            self._ebank_reg &= ~ 0o7
            self._ebank_reg |= (self._ebank_reg >> 8) & 0o7

        # Bypass update if 1-shot declaration.
        b25t27m = Bit.BIT25 | Bit.BIT26 | Bit.BIT27
        if (self._sbank_reg & b25t27m) == Bit.BIT25:
            # Copy permanent into temporary superbits.
            b28t30m = Bit.BIT28 | Bit.BIT29 | Bit.BIT30
            self._sbank_reg &= ~b28t30m
            self._sbank_reg |= (self._sbank_reg << 5) & b28t30m

        # Select on * in op code (BBCON or 2CADR).
        if not self.cuss_list[90].demand:
            self._max_adres = 0o167777
            return self.max_ad_set(popo, update_ebank=False)

        # FIXME

    # Specific processing for basic instructions.
    def instrop(self, popo, adr_wd):
        # Supply incrementing bit for D.P. codes.
        if self._yul.switch & SwitchBit.DP_OPCODE:
            self._word |= 0o1

        # Branch if address value is positive.
        if adr_wd[0] >= 0:
            # Branch unless memory allowance = F only.
            if (popo.health & (Bit.BIT29 | Bit.BIT30)) != Bit.BIT30:
                return self.basic_adr(popo, adr_wd)

            # Branch if indeed refers to fixed.
            if self._address >= 0o4000:
                return self.basic_adr(popo, adr_wd)

            # Address in banks E4-E7 is nonsense here.
            if self._address >= 0o2000:
                return self.rng_error(popo, adr_wd)

            if self._yul.switch & SwitchBit.PREVIOUS_INDEX:
                return self.add_adr_wd(popo, adr_wd)

            self.cuss_list[35].demand = True
            self.prb_adres(self._address)
            # If not indexed, we've had it, mate.
            self.cuss_list[10].demand = True
            return self.add_adr_wd(popo, adr_wd)

        if not self._yul.switch & SwitchBit.PREVIOUS_INDEX:
            # Cuss no index before minus address.
            self.cuss_list[71].demand = True

        # Add negative address.
        self._word += adr_wd[0]

        # Set up prime for full code print.
        self._line[39] = '\''

        # Call for prime in quarter-code print.
        adr_wd[0] = 0o1000
        return self.gud_basic(popo, adr_wd)

    def add_adr_wd(self, popo, adr_wd):
        self._word += adr_wd[0]
        return self.gud_basic(popo, adr_wd)

    def basic_adr(self, popo, adr_wd):
        # Branch if address is in erasable.
        if self._address > 0o3777:
            if self._yul.switch & SwitchBit.PREVIOUS_INDEX:
                return self.adres_adr(popo, adr_wd)

            # Cuss unindexed 1/4-code reference to F.
            if self._max_adres == 0o11777:
                self.cuss_list[35].demand = True
                self.prb_adres(self._address)
                self.cuss_list[10].demand = True

            # Put misc. flag on unindexed basic instructions that refer to fixed memory.
            dec48_flg = Bit.BIT2 | Bit.BIT5
            self._word |= dec48_flg
            return self.adres_adr(popo, adr_wd)

        # Branch if address is not in an EBank.
        if adr_wd[1] <= 0o1377:
            return self.add_adr_wd(popo, adr_wd)

        # Except where instruction is indexed, cuss D.P. address that straddles Ebanks.
        if (self._yul.switch & (SwitchBit.PREVIOUS_INDEX | SwitchBit.DP_OPCODE)) == SwitchBit.DP_OPCODE:
            if (adr_wd[0] & 0o377) == 0o377:
                self.cuss_list[10].demand = True
                self.cuss_list[35].demand = True
                self.prb_adres(self._address)

                # (For D.P. address = 1377).
                if self._address <= 0o1377:
                    return self.add_adr_wd(popo, adr_wd)

        elif self._address <= 0o1377:
            return self.add_adr_wd(popo, adr_wd)

        # Forgive all if we have pseudo Ebank. Branch on E-bank error.
        if ((self._ebank_reg & 0o3400) <= 0o1000) or ((self._ebank_reg & 0o3400) == (self._address & 0o3400)) :
            # Put subaddress in the range 1400-1777
            adr_wd[0] &= ~0o3400
            adr_wd[0] |= 0o1400
            return self.add_adr_wd(popo, adr_wd)

        adr_wd[0] &= ~0o3400
        adr_wd[0] |= 0o1400
        self.cuss_bank()

        # Put Ebank number in bank error cuss.
        cuss = self.cuss_list[33]
        bank_no = self._address >> 8
        cuss.msg = cuss.msg[:19] + ('E%o' % bank_no) + cuss.msg[21:]
        return self.add_adr_wd(popo, adr_wd)

    def adres_adr(self, popo, adr_wd):
        # Exit if in fixed-fixed.
        if adr_wd[1] <= 0o7777:
            return self.add_adr_wd(popo, adr_wd)

        # Except where instruction is indexed, cuss D.P. address that straddles Fbanks.
        if (self._yul.switch & (SwitchBit.PREVIOUS_INDEX | SwitchBit.DP_OPCODE)) == SwitchBit.DP_OPCODE:
            if (adr_wd[0] & 0o1777) == 0o1777:
                self.cuss_list[10].demand = True
                self.cuss_list[35].demand = True
                self.prb_adres(self._address)

                # (For D.P. address = 7777).
                if self._address <= 0o7777:
                    return self.add_adr_wd(popo, adr_wd)

        elif self._address <= 0o7777:
            return self.add_adr_wd(popo, adr_wd)

        # Branch if location is not in an Fbank. No bank cuss on XQC ref to 2000-3777.
        if ((not (self._location <= 0o7777 or self._max_adres <= 0o11777)) and
            ((self._location & 0o176000) != (self._address & 0o176000))):
            return self.cus_f_bank(popo, adr_wd)

        # Put subaddress in range 2000-3777.
        adr_wd[0] &= ~0o176000
        adr_wd[0] |= 0o2000
        return self.add_adr_wd(popo, adr_wd)

    def cus_e_bank(self, popo, adr_wd):
        adr_wd[0] &= ~0o3400
        adr_wd[0] |= 0o1000
        cuss = self.cuss_list[33]
        bank_no = self._address >> 10
        # Put EBANK number into bank error cuss.
        cuss.msg = cuss.msg[:19] + ('E%o' % bank_no) + cuss.msg[21:]
        return self.add_adr_wd(popo, adr_wd)

    def cus_f_bank(self, popo, adr_wd):
        adr_wd[0] &= ~0o176000
        adr_wd[0] |= 0o2000
        cuss = self.cuss_list[33]
        bank_no = (self._address - 0o10000) >> 10
        # Put FBANK number into bank error cuss.
        cuss.msg = cuss.msg[:19] + ('%02o' % bank_no) + cuss.msg[21:]
        return self.add_adr_wd(popo, adr_wd)

    # Minor subroutine to cuss either type of bank error.
    def cuss_bank(self):
        # Set poison bit of bank cuss = -indexed.
        self.cuss_list[33].poison = not (self._yul.switch & SwitchBit.PREVIOUS_INDEX)
        # Call for bank error cuss.
        self.cuss_list[33].demand = True

    # When address is wrong but not atrocious, tell the man what it is.
    def prb_adres(self, address):
        # Set up address of adr cuss.
        cuss = self.cuss_list[35]
        # Branch if address is in erasable.
        if address > 0o3777:
            # Branch if address is in fixed-fixed.
            if address > 0o7777:
                # Put subaddress in the range 2000-3777.
                address -= 0o10000
                bank_no = address >> 10
                address = (address | 0o2000) & 0o3777
                # Put reduced bank no. into cuss, exit.
                cuss.msg = cuss.msg[:8] + ('=%02o,%04o' % (bank_no, address))
                return
            else:
                cuss.msg = cuss.msg[:8] + ('=%04o   ' % address)
                return
        else:
            # Branch if address is in unswitched E.
            if address > 0o1377:
                bank_no = address >> 8
                # Put subaddress in the range 1400-1777.
                address = (address | 0o1400) & 0o1777
                # Put EBank no. into cuss, exit.
                cuss.msg = cuss.msg[:8] + ('=E%o,%04o' % (bank_no, address))
                return

        cuss.msg = cuss.msg[:8] + '= %04o   ' % address

    # Printing procedures for basic instructions and address constants.
    def gud_basic(self, popo, adr_wd):
        # Branch if no minus sign in column 17.
        if popo.card[16] == '-':
            # Complement negative instruction.
            self._word ^= 0o77777

        # Put basic code address into print image.
        self._line[40] = '%04o' % (self._word & 0o7777)

        # Branch if word is an address constant.
        dec6_flag = Bit.BIT2 | Bit.BIT3

        if self._word >= dec6_flag:
            # Print first digit of constant.
            first_digit = (self._word >> 12) & 0o7
            self._line[39] = '%o' % first_digit
            return self.bc_check(popo)

        if adr_wd[0] < 0:
            return self.op_digit_m1(popo, adr_wd)

        # Branch if instruction refers 2 erasable.
        address = self._address
        if address > 0o3777:
            # Branch if refers to fixed-fixed.
            if address > 0o7777:
                # Reduce bank number. Set FBANK ref. bit.
                self._word |= Bit.BIT29 | Bit.BIT30
                address -= 0o10000

            # Align fixed bank nos. with erasable.
            address >>= 2

        # Supply bank number to pass 3 for ref ck.
        self._word |= (address << 22) & 0o770000000000
        # Store it twice to make parity ok.
        self._word |= (self._word >> 6) & 0o7700000000

        # Choose printing of straight op or other.
        return self.op_digit_m1(popo, adr_wd)

    def op_digit_m1(self, popo, adr_wd):
        if popo.health & Bit.BIT29:
            return self.op_digit(popo, adr_wd)
        else:
            return self.print_op(popo, adr_wd)

    def op_digit(self, popo, adr_wd):
        # Print second octal op digit.
        sec_digit = (self._word >> 9) & 0o7
        self._line[39] = '%o' % sec_digit

        # Branch if address value is over 777.
        if abs(adr_wd[0]) < 0o1000:
            self._line[40] = ' '
        else:
            # Insert prime if address is split.
            self._line[40] = '\''

        return self.print_op(popo, adr_wd)

    def print_op(self, popo, adr_wd):
        # Set main op digit in print.
        first_digit = (self._word >> 12) & 0o7
        self._line[38] = '%o' % first_digit

        # Move current index bit to previous.
        self._yul.switch &= ~SwitchBit.PREVIOUS_INDEX
        if self._yul.switch & SwitchBit.CURRENT_INDEX:
            self._yul.switch |= SwitchBit.PREVIOUS_INDEX
        # Clear current index bit.
        self._yul.switch &= ~SwitchBit.CURRENT_INDEX

        # Cleverly exit to naughty or bc_check.
        if self._line[43] == '■':
            return self.naughty(popo)

        return self.bc_check(popo)

    def bad_basic(self, popo):
        # Blot out bad address field.
        self._line[40] = '■■■■'

        dec_5_flag = Bit.BIT2 | Bit.BIT4
        if self._word >= dec_5_flag:
            # Blot first digit of bad constant.
            self._line[39] = '■'
            return self.naughty(popo)

        # Branch if no minu sign in column 17.
        if popo.card[16] == '-':
            # Complement good op of bad neg. instr.
            self._word ^= 0o77777

        # Choose printing of straight op or other.
        return self.print_op(popo, [0,0])

    def naughty(self, popo):
        self._word = BAD_WORD
        return self.bc_check(popo)

    def bc_check(self, popo):
        if popo.card[16] == '-':
            # Clear extension cusses if minus.
            self.cuss_list[36].demand = False
            self.cuss_list[37].demand = False
            # Clear "should-be-INDEXed" cuss if minus.
            self.cuss_list[71].demand = False
        # Cuss if neither blank nor minus in CC 17.
        elif popo.card[16] != ' ':
            self.cuss_list[61].demand = True

        if popo.card[0] == 'J':
            # Clear extension cusses if leftover.
            self.cuss_list[36].demand = False
            self.cuss_list[37].demand = False
            # Clear "should-be-INDEXed" cuss if lftvr.
            self.cuss_list[71].demand = False
        # Cuss if neither blank nor J in column 1.
        elif popo.card[0] != ' ':
            self.cuss_list[60].demand = True

        # Cuss if column 24 non-blank.
        if popo.card[23] != ' ':
            self.cuss_list[62].demand = True

        # Turn off D.P. op code switch.
        self._yul.switch &= ~SwitchBit.DP_OPCODE

        # Turn off "just-did-EBANK=" switch.
        self._ebank_reg &= ~0o77
        self._ebank_reg |= 8
        self._ebank_reg |= (self._ebank_reg >> 8) & 0o7
        # Turn off "just-did-SBANK=" switch.
        self._sbank_reg &= ~(Bit.BIT26 | Bit.BIT27)
        self._sbank_reg |= Bit.BIT25
        b28t30m = (Bit.BIT28 | Bit.BIT29 | Bit.BIT30)
        self._sbank_reg &= ~b28t30m
        self._sbank_reg |= (self._sbank_reg << 5) & b28t30m

        # Return to general procedure.
        return

    def ebk_loc_q(self, accept_temp=True):
        if accept_temp:
            # Tentatively accept EBANK declaration.
            self._ebank_reg &= ~0o3400
            self._ebank_reg |= (self._ebank_reg << 8) & 0o3400

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
        # FIXME
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

        return self.good_1p(popo, number)

    def good_1p(self, popo, number):
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
