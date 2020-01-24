import math


class Frame:

    def __str__(self):
        return self.frame_text('🙈🙉🙊', hspace=1, vspace=0)

    def __init__(self, corners, hd=' ', vd=' '):
        self.tl, self.tr = corners[0][0], corners[0][-1]
        self.bl, self.br = corners[1][0], corners[1][-1]
        if len(corners[0]) == 3:
            self.tm = corners[0][1]
            self.bm = corners[1][1]
        else:
            self.tm = ''
            self.bm = ''

        self.corners = corners

        if isinstance(hd, str):
            self.lhd = self.rhd = hd
        else:
            self.lhd, self.rhd = hd

        if not self.lhd:
            self.lhd = ' '
        if not self.rhd:
            self.rhd = ' '

        if not vd:
            vd = ' '
        self.vd = vd
        self.nh = len(self.tl) + len(self.tr) + len(self.tm)
        self.nvd = len(self.vd) * 2

    def frame_text(self, text, hspace=1, vspace=0, bg=' '):
        text_lines = text.split('\n')
        n_lines = len(text_lines) + (2*vspace) + 2
        n_char = max(map(len, text_lines)) + (2*hspace) + self.nvd

        # build our dividers
        n_hdiv = n_char-self.nh
        if n_hdiv % 2:
            n_hdiv += 1

        n_lh = n_rh = n_hdiv/2

        ldiv = self.lhd * math.ceil((n_lh/len(self.lhd)))
        rdiv = self.rhd * math.ceil((n_rh/len(self.rhd)))

        # top and bottom borders
        top = self.tl + ldiv + self.tm + rdiv + self.tr
        bottom = self.bl + ldiv + self.bm + rdiv + self.br
        n_char = max(len(top), len(bottom))

        empty_line = self.vd + bg*(n_char-self.nvd) + self.vd

        lines = [top] + [empty_line]*vspace

        # now do our lines
        for line in text_lines:
            line = line.strip()
            n_space = n_char - len(line) - self.nvd

            if n_space % 2:  # odd
                start = n_space // 2
                end = start+1
            else:
                start = end = int(n_space / 2)

            new_line = self.vd + bg*start + line + bg*end + self.vd
            lines.append(new_line)

        lines += [empty_line]*vspace
        lines.append(bottom)
        return '\n'.join(lines)
