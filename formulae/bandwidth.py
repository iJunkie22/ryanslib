from __future__ import print_function
from formulae import DiscreteVariable


class Bytes(int):
    def to_bits(self):
        return self * 8.000

    @classmethod
    def from_kb(cls, kb_value):
        return cls(kb_value * 1024.000)

    @classmethod
    def from_mb(cls, mb_value):
        return cls(mb_value * 1048576.0000)

    @classmethod
    def from_gb(cls, b_value):
        return cls(b_value * 1073741824.0000000)

    @classmethod
    def from_bits(cls, bits_value):
        return cls(bits_value / 8.000000)


class Kilobytes(float):
    def __init__(self, x):
        super(Kilobytes, self).__init__(x)

    def to_kbits(self):
        return self * 8.000

    @classmethod
    def from_b(cls, b_value):
        return cls(b_value / 1024.000)

    @classmethod
    def from_mb(cls, mb_value):
        return cls(mb_value * 1024.000)

    @classmethod
    def from_gb(cls, gb_value):
        return cls(gb_value * 1048576.0000)

    @classmethod
    def from_kbits(cls, kbits_value):
        return cls(kbits_value / 8.000000)


class Megabytes(float):
    def __init__(self, x):
        super(Megabytes, self).__init__(x)

    def to_mbits(self):
        return self * 8.000

    @classmethod
    def from_b(cls, b_value):
        return cls(b_value / 1048576.0000)

    @classmethod
    def from_kb(cls, kb_value):
        return cls(kb_value / 1024.000)

    @classmethod
    def from_gb(cls, mb_value):
        return cls(mb_value * 1024.000)

    @classmethod
    def from_mbits(cls, mbits_value):
        return cls(mbits_value / 8.000000)


class Gigabytes(float):
    def __init__(self, x):
        super(Gigabytes, self).__init__(x)

    def to_gbits(self):
        return self * 8.000

    @classmethod
    def from_b(cls, b_value):
        return cls(b_value / 1073741824.0000000)

    @classmethod
    def from_kb(cls, kb_value):
        return cls(kb_value / 1048576.0000)

    @classmethod
    def from_mb(cls, mb_value):
        return cls(mb_value / 1024.000)

    @classmethod
    def from_tb(cls, tb_value):
        return cls(tb_value * 1024.000)

    @classmethod
    def from_gbits(cls, gbits_value):
        return cls(gbits_value / 8.000000)

KB = Kilobytes
MB = Megabytes
GB = Gigabytes


# From https://en.wikipedia.org/wiki/Bit_rate#Progress_trends on Jun 14, 2016
# From https://en.wikipedia.org/wiki/IEEE_802.11#802.11n on Jun 14, 2016

WiFi_mbytes = DiscreteVariable(MB.from_mbits(54.00), MB.from_mbits(600.00), MB.from_mbits(50.00))
ThunderBolt1 = GB.from_gbits(20.00)
ThunderBolt2 = GB.from_gbits(20.00)
ThunderBolt3 = GB.from_gbits(40.00)
Bluetooth_old = MB.from_mbits(11.00)
Bluetooth41_PAL = WiFi_mbytes


