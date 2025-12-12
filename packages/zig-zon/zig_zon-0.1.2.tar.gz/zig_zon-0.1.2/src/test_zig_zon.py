#!/usr/bin/env python3

from pprint import pprint

import zig_zon
print('zig_zon module:', zig_zon)

teststr = """
.{
    .asdf = "ccc",
    .my_bool = true,
    .my_float = 1.23,
    .my_hex_int = 0xdeadbeef,
    .my_negative_int = -432_123_111,
    .my_negative_big_int = -4611686018427387904,
    .my_optional = null,
}"""

testzon = zig_zon.parse(teststr)
print('teststr:')
pprint(testzon)
pprint(zig_zon.__version__)
pprint(zig_zon.__version_str__)

assert testzon['asdf'] == "ccc"
assert testzon['my_float'] == 1.23
assert testzon['my_hex_int'] == 0xdeadbeef
assert testzon['my_negative_int'] == -432_123_111
assert testzon['my_negative_big_int'] == -4611686018427387904
assert testzon['my_optional'] == None
assert zig_zon.parse(str(2**63 - 1)) == 2**63 - 1
assert zig_zon.parse(str(2**63)) == 2**63
assert zig_zon.parse(str(2**64 - 1)) == 2**64 - 1

# print("TODO: 2**64 ==", 2**64, ", zig_zon.parse(str(2**64)) ==",
#       zig_zon.parse(str(2**64)))
# assert zig_zon.parse(str(2**64)) == str(2**64)

print('build.zig.zon:')
with open('build.zig.zon') as fd:
    pprint(zig_zon.parse(fd.read()))
