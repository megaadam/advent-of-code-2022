from util import readlines

# to copy-paste test-data into respective def test():
# e.g.

lines = readlines()

print("\n\ndef test():")
print("    lines = [")
for line in lines:
    print(f"    '{line}',",)

print('    ]')
