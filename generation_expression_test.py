x = ['abc', 12, 'j48', '45', 43, 33, -20, -11, True, False, 11.5, 24.3, 0]
print x

# python generator expression test
result = (n for n in x if isinstance(n, int) and isinstance(n, bool) == False and (n % 2 == 0 or int(str(abs(n))[0]) % 2 == 0))

for n in result:
	print n

