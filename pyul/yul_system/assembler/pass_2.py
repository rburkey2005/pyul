from yul_system.types import ALPHABET, SwitchBit, HealthBit, Bit

class Cuss:
    def __init__(self, msg, poison=False):
        self.msg = msg
        self.poison = poison
        self.requested = False

class Line:
    def __init__(self, text=' '*120, spacing=0):
        self.spacing = spacing
        self.text = text

class Pass2:
    def __init__(self, mon, yul, adr_limit):
        self._mon = mon
        self._yul = yul
        self._adr_limit = adr_limit
        self._def_xform = 0o31111615554
        self._marker = '*'
        self._lin_count = 0
        self._page_no = 0
        self._user_page = 0
        self._line = Line()
        self._old_line = Line()
        self._user_log = Line(' '*81 + 'USER\'S OWN PAGE NO.' + 20*' ', spacing=2)
        self._card_typs = [
            (self.end_of,      2),
            (self.modify,      3),
            (self.end_error,   2),
            (self.card_no,     3),
            (self.accept,      2),
            (self.delete,      3),
            (self.remarks,     2),
            (self.disaster,    0),
            (self.no_loc_sym,  2),
            (self.memory,      3),
            (self.instruct,    2),
            (self.illegop,     2),
            (self.decimal,     0),
            (self.octal,       0),
            (self.equals,      3),
            (self.setloc,      3),
            (self.erase,       3),
            (self._2octal,     0),
            (self._2decimal,   0),
            (self.block,       3),
            (self.head_tail,   3),
            (self.too_late,    3),
            (self.subro,       3),
            (self.instruct_p1, 3),
            (self.even,        3),
            (self.count,       3),
            (self.segnum,      3),
        ]

    def pass_2(self):
        for popo in self._yul.popos:
            card_type = popo.health & HealthBit.CARD_TYPE_MASK

            # Clear location symbol switch.
            self._equaloc = 0

            # Branch if last card wasnt remarks
            if self._yul.switch & SwitchBit.LAST_REM:
                self._yul.switch &= ~SwitchBit.LAST_REM
                # Branch if this card isnt right print.
                if card_type == HealthBit.CARD_TYPE_RIGHTP:
                    # Branch if line unaffected by this rev.
                    if popo.marked:
                        self._old_line.text = self._old_line.text[:7] + self._marker + self._old_line.text[8:]
                        self._marker = '*'

                    self.send_sypt(popo.card)

                    # Set right print remarks in print.
                    self._old_line.text = self._old_line.text[:80] + popo.card[8:48]

                    # Branch if no right print cardno error.
                    if not popo.health & Bit.BIT7:
                        self.cusser()
                        continue

                    # Make up card number error note.
                    self._line.text = self._line.text[:88] + self.cuss_list[0].msg
                    if self.cuss_list[0].requested:
                        self.rem_cn_err(popo)
                        continue

                    # If 1st cuss of page, left end of blots.
                    self.go_num_cus()
                    self.count_cus(6)
                    continue
            else:
                if self.cuss_list[0].requested:
                    self.rem_cn_err(popo)

            # Procedure when last card was not left print remarks.
            # Set up columns 1-7.
            self._line.text = popo.card[:7] + self._line.text[7:]

            # Branch if line affected by this revision
            if popo.marked:
                self._line.text = self._line.text[:7] + self._marker + self._line.text[8:]
                self._marker = '*'

            # Maybe cuss card number sequence error.
            if popo.health & Bit.BIT7:
                self.cuss_list[0].requested = True

            # Branch if card is not right print
            if card_type == HealthBit.CARD_TYPE_RIGHTP:
                # Print under 1st half of remarks field.
                self._line.text = self._line.text[:80] + popo.card[8:48]
                # Make right print a continuation card.
                self._line.text = 'C' + self._line.text[1:]
                self.no_loc_sym(popo)
                continue

            vert_format = ord(popo.card[7]) & 0xF
            if vert_format == 8:
                # Maybe set up skip bit.
                self._line.spacing |= Bit.BIT1
            else:
                # Maybe set up space count.
                self._line.spacing |= vert_format

            # Set up columns 9-80.
            self._line.text = self._line.text[:48] + popo.card[8:]

            # Turn off leftover switch.
            self._yul.switch &= ~SwitchBit.LEFTOVER

            # Set up branches on card type.
            own_proc, ternary_key = self._card_typs[card_type // Bit.BIT6]

            # Use ternary key to check whether columns 1, 17, and 24 contain
            # queer information.
            if ternary_key == 3 or (ternary_key == 0 and popo.card[0] != 'J'):
                if popo.card[0] != ' ':
                    self.cuss_list[60].requested = True
                if popo.card[16] != ' ':
                    self.cuss_list[61].requested = True
                if popo.card[23] != ' ':
                    self.cuss_list[62].requested = True

            own_proc(popo)

        return self.end_pass_2()

    def rem_cn_err(self, popo):
        pass

    def end_pass_2(self):
        pass

    def end_of(self, popo):
        pass

    def modify(self, popo):
        pass

    def end_error(self, popo):
        pass

    def card_no(self, popo):
        pass

    def accept(self, popo):
        pass

    def delete(self, popo):
        pass

    # Procedure in pass 2 for remarks cards. Postpones cussing to check for a right print card.
    def remarks(self, popo):
        # Move remark 5 words left. Fill out line with blanks.
        self._line.text = self._line.text[:8] + self._line.text[48:] + 40*' '
        # Signal that last was remarks, print.
        self._yul.switch |= SwitchBit.LAST_REM
        self.print_lin()
        self.send_sypt(popo)

    def disaster(self, popo):
        pass

    def no_loc_sym(self, popo):
        pass

    def memory(self, popo):
        pass

    def instruct(self, popo):
        pass

    def illegop(self, popo):
        pass

    def decimal(self, popo):
        pass

    def octal(self, popo):
        pass

    def equals(self, popo):
        pass

    def setloc(self, popo):
        pass

    def erase(self, popo):
        pass

    def _2octal(self, popo):
        pass

    def _2decimal(self, popo):
        pass

    def block(self, popo):
        pass

    def head_tail(self, popo):
        pass

    def too_late(self, popo):
        pass

    def subro(self, popo):
        pass

    def instruct_p1(self, popo):
        pass

    def even(self, popo):
        pass

    def count(self, popo):
        pass

    def segnum(self, popo):
        pass

    def send_sypt(self, card):
        pass

    def go_num_cus(self):
        pass

    def count_cus(self, offset):
        pass

    def cusser(self):
        pass

    def print_lin(self):
        # New line ages suddenly.
        old_line = self._old_line
        self._old_line = self._line

        if self._line.text[0] == 'L':
            if self._line.spacing <= 1:
                # Change log card SP1 to SP2.
                self._line.spacing = 2

            # Erase any special flag at end of loglin.
            self._user_log.text = self._user_log.text[:116] + ' '*4

            # Lose any right print on log card.
            self._yul.switch &= ~SwitchBit.LAST_REM

            # Always start page number at 1.
            self._user_log.text = self._user_log.text[:100] + '   1' + self._user_log.text[104:]

            # Keep log line for page subheads.
            self._user_log.text = self._line.text[:80] + self._user_log.text[80:]

            # Set up "USER'S OWN PAGE NO."
            self._user_page = 1
            self._line.text = self._line.text[:80] + self._user_log.text[80:]

            # Branch unless printing is suppressed.
            if self._yul.switch & SwitchBit.PRINT:
                return self.prin_skip(old_line)

            # Exit at once if page head is owed.
            if self._yul.switch & SwitchBit.OWE_HEADS:
                return self.print_old()

            # Print E and owe heads if E is owed.
            if old_line.text[0] == 'E':
                self._yul.switch |= SwitchBit.OWE_HEADS
                return self.endoform(old_line, False)

            # If nothing is owed, we're in mid-page. So print blank line(s) to
            # get to E-O-F.
            self._yul.switch |= SwitchBit.OWE_HEADS
            return self.endoform(old_line, True)

        # Make card number look helpful by suppressing at most two zeros.
        # From right to left (columns 7 and 6).
        if self._line.text[6] == '0':
            self._line.text = self._line.text[:6] + ' ' + self._line.text[7:]
            if self._line.text[5] == '0':
                self._line.text = self._line.text[:5] + ' ' + self._line.text[6:]

        # Branch unless printing is suppressed.
        if not self._yul.switch & SwitchBit.PRINT:
            # Branch unless owe a cuss or cussed line.
            if self._line.text[0] == 'E':
                # Single-space any line preceding E-line.
                old_line.spacing = 1
                self._line.spacing = 2

                # Branch if we owe heads.
                if self._yul.switch & SwitchBit.OWE_HEADS:
                    return self.page_unit(old_line)

                self._yul.switch &= ~SwitchBit.OWE_HEADS

                # Add to line count from last line.
                self._lin_count += old.spacing & ~Bit.BIT1
                return self.print_old(old_line)

            # Exit at once if nor this nor last was E.
            if old_line.text[0] != 'E':
                return self.print_old()

            # Add to line count from last line.
            self._lin_count += old_line.spacing & ~Bit.BIT1

            # Back to normal print.
            if self._lin_count <= self._yul.n_lines:
                return self.print_old(old_line)

            self._yul.switch |= SwitchBit.OWE_HEADS
            return self.endoform(old_line, False)

        # Unless immediately following a log card, skip to head of form before ..P.. card.
        if self._line.text[0] == 'P' and old_line.text[0] != 'L':
            return self.prin_skip(old_line)

        # Branch unless A-line after C-line.
        if self._line.text[0] == 'A':
            if old_line.text[0] != 'C':
                return self.ask_skip(old_line)

            # Maybe copy 2nd loc and word of DP const.
            self._line.text = self._line.text[:8] + old_line.text[8:48] + self._line.text[48:]

            # Absorb it into A-line if it was.
            if not self._line.text[40:48].isspace():
                return self.print_old()

        # Branch if not pass 2 error/warning line or continuation line.
        if not self._line.text[0] in 'EC':
            return self.ask_skip(old_line)

        if self._lin_count != self._yul.n_lines:
            # Keep "E" and "C" lines on same page.
            self._lin_count -= 1

        # Branch if last line is already skip.
        if old_line.spacing & Bit.BIT1:
            # Move last lines skip to this E-line.
            self._line.spacing = Bit.BIT1

        # Branch if last line is SP1.
        elif old_line.spacing <= 1:
            # Make last line SP1.
            old_line.spacing = 1

        else:
            # If not, space this line 1 less.
            self._line.spacing -= 1

        # Make last line SP1.
        old_line.spacing = 1
        return self.ask_skip(old_line, False)

    def ask_skip(self, old_line, check_skip=True):
        # Branch if last line is skip.
        if check_skip and old_line.spacing & Bit.BIT1:
            return self.prin_skip(old_line)

        # Add to line count from last line.
        self._lin_count += old_line.spacing

        # Branch to normal print.
        if self._lin_count <= self._yul.n_lines:
            return self.print_old(old_line)

        return self.prin_skip(old_line)

    def prin_skip(self, old_line, check_cusses=True):
        # "Branch" if any cusses on this page.
        if check_cusses and not self._yul.switch & SwitchBit.CUSSES_ON_PAGE:
            # Skip after last line at end of page.
            old_line.spacing = Bit.BIT1
            return self.dpaginat(old_line)

        # Set up SP2 and record it in line count.
        old_line.spacing = 2
        self._lin_count += old_line.spacing

        # Branch if more copies should be done.
        if self._yul.n_copies > 0:
            self.copy_prt5()

        self._mon.phi_print(old_line.text, old_line.spacing)

        # Turn off cusses-on-this-page flag.
        self._yul.switch &= ~SwitchBit.CUSSES_ON_PAGE

        # Branch if not yet at end of form.
        if self._lin_count <= self._yul.n_lines:
            # Go to end of form by blank lines w/ SP2.
            old_line.text = ' '*120
            return self.prin_skip(old_line, check_cusses=False)

        # Prepare a wham for last line of page.
        old_line.spacing = Bit.BIT1
        old_line.text = '■'*120
        return self.dpaginat(old_line)

    def dpaginat(self, old_line):
        # FIXME: what does DEPAGIN8 do?
        # if self._yul.n_copies > 0:
        #     self.copy_prt5()
        #self._mon.phi_print('', spacing=Bit.BIT1)

        if self._yul.n_copies > 0:
            self.copy_prt5()

        self._mon.phi_print(old_line.text, spacing=old_line.spacing)

        return self.page_unit(old_line)

    # Printing of page head and subhead (loc), and detail lines.

    def page_unit(self, old_line):
        self._page_no += 1
        # Put page number alpha in page head.
        self._yul.page_head = self._yul.page_head[:116] + ('%4d' % self._page_no)

        return self.print_hed(old_line)

    def print_hed(self, old_line):
        if self._yul.n_copies > 0:
            self.copy_prt5()
        self._mon.phi_print(self._yul.page_head, spacing=3)
        # Reset line count to 3.
        self._lin_count = 3

        # Finish up and exit if no log.
        if self._user_page > 0:
            # Go to print if not new log.
            if self._user_page != 1:
                # Put page no. in alpha in page subhead.
                self._user_log.text = self._user_log.text[:100] + ('%4d' % self._user_page) + self._user_log.text[104:]

            # Print log line now if heads are owed.
            elif not self._yul.switch & SwitchBit.OWE_HEADS:
                # Advance page no. for next use of log.
                self._user_page = 2
                return self.print_old()

            if self._yul.n_copies > 0:
                self.copy_prt5()

            # Print log line and double space.
            self._mon.phi_print(self._user_log.text, spacing=self._user_log.spacing)
            self._user_page += 1

            # Accordingly set line count to 5.
            self._lin_count += self._user_log.spacing

        # Exit now unless heads were owed.
        if not self._yul.switch & SwitchBit.OWE_HEADS:
            return self.print_old()

        # Now heads are paid up, print a cussed L.
        self._yul.switch &= ~SwitchBit.OWE_HEADS

        # Add to line count from last line.
        self._lin_count += old.spacing & ~Bit.BIT1
        return self.print_old(old_line)

    def endoform(self, old_line, check_cusses):
        if check_cusses and not self._yul.switch & SwitchBit.CUSSES_ON_PAGE:
            # Branch if more copies should be done.
            if self._yul.n_copies > 0:
                self.copy_prt5()

            # FIXME: DEPAGIN8

            # Print last line, skip, and owe heads.
            old_line.spacing = Bit.BIT1
            return self.print_old(old_line)

        self._yul.switch &= ~SwitchBit.CUSSES_ON_PAGE

        # Set up SP2 and record it in line count.
        old_line.spacing = 2
        self._lin_count += old_line.spacing

        if self._yul.n_copies > 0:
            self.copy_prt5()

        self.phi_print(old_line.text, old_line.spacing)

        if self._lin_count <= self._yul.n_lines:
            old_line.text = ' '*120
            return self.endoform(old_line, False)

    def print_old(self, old_line=None):
        if old_line is not None:
            if self._yul.n_copies != 0:
                self.copy_prt5()

            self._mon.phi_print(old_line.text, old_line.spacing)

        # Old line discovers fountain of youth. And moreover is made clean again.
        self._line = Line()

    def copy_prt5(self):
        pass

    def pass_1p5(self):
        # print('\nSYMBOL TABLE:')
        # print('-------------')
        # syms = sorted(self._yul.sym_thr.keys(), key=lambda sym: [ALPHABET.index(c) for c in sym])
        # for sym in syms:
        #     s = self._yul.sym_thr[sym]
        #     print('%-8s: %04o (%x)' % (sym, s.value, s.health))
        #     if s.definer is not None:
        #         print('  - Defined by: %s' % s.definer)
        #     if len(s.definees) > 0:
        #         print('  - Defines:    %s' % ', '.join(s.definees))

        # FIXME: resolve leftovers

        self.resolvem()
        self.assy_typ_q()

    def resolvem(self):
        for sym_name, symbol in self._yul.sym_thr.items():
            # If not nearly defined, seek another.
            if symbol.health > 0x0 and symbol.health < 0x3:
                self.def_test(symbol)

    def def_test(self, symbol):
        # Mark definer thread.
        symbol.analyzer = 1

        # Fetch symbol health code.
        definer = self._yul.sym_thr[symbol.definer]
        # "Branch" if symbol has no valid defin.
        undefined = (self._def_xform >> (16 + definer.health)) & 0x1

        if not undefined:
            # Fetch first-definee thread, go define.
            self.definem(definer)
        elif definer.analyzer:
            # Vicious circle if marked.
            self.voidem(definer)
        elif definer.health > 0x0 and definer.health < 0x3:
            # Continue definer search.
            self.def_test(definer)
        else:
            # Branch if symbol is undefinable.
            self.voidem(definer)

    def voidem(self, definer):
        # Void a definer thread.
        definer.health = 0
        definer.analyzer = 2
        for definee in definer.definees:
            def_symbol = self._yul.sym_thr[definee]

            if def_symbol.analyzer != 2:
                self.voidem(def_symbol)

    def definem(self, definer):
        for definee in definer.definees:
            def_symbol = self._yul.sym_thr[definee]

            # Reconstitute signed modifier.
            def_symbol.value += definer.value
            if def_symbol.value < 0 or def_symbol.value > self.adr_limit:
                if def_symbol.health == 0x1:
                    # Nearly def becomes oversize defined.
                    def_symbol.health = 0x8
                else:
                    # Mult near def becomes mult oversize def.
                    def_symbol.health = 0xB
            else:
                if def_symbol.health == 0x1:
                    # Nearly defined becomes defined by =.
                    def_symbol.health = 0x3
                else:
                    # Mult nearly def becomes mult def by =.
                    def_symbol.health = 0x4

            self.definem(def_symbol)

    def assy_typ_q(self):
        if not self._yul.switch & SwitchBit.REPRINT:
            return self.real_assy()

        # FIXME: handle revisions and bad merges

    # Assembly of a new program or subroutine, or a well-merged revision or version. Clean out the
    # delete list and refurbish the lists of threads to subsidiary subroutines.
    def real_assy(self):
        # FIXME: handle deletes?
        # FIXME: create files, update metadata
        return self.inish_p2()

    # Initializing procedure for pass 2.
    def inish_p2(self):
        # Turn on print switch for main part.
        self._yul.switch |= SwitchBit.PRINT

        # Initialize count of word records.
        self._n_word_recs = 0
        self._yul.switch &= ~SwitchBit.LAST_REM

        self._err_pages = 0

        return self.pass_2()
