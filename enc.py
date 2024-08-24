s = "192.168.40.7"
l = [(255-int(i))/10 for i in s.split('.')]

[i for i in s.split('.')] #[63, 87, 215, 248]

print(l)

d = {i+1:j for i, j in enumerate("abcdefghijklmnopqrstuvwxyz")}
print(d)

enc = "".join([d[int(i)] for i in l])
rest = "".join([d[int(str(i)[-1])] for i in l])
code = "".join([i+j for i, j in zip(enc,rest)])
# print(code)

enc2, rest2 = code[::2], code[1::2]
d2 = {j:i+1 for i, j in enumerate("abcdefghijklmnopqrstuvwxyz")}
enc2_l = [d2[i] for i in enc2]
rest2_l = [d2[i] for i in rest2]
ip_l = ([(f"{i}{j}") for i, j in zip(enc2_l, rest2_l)])
ip = '.'.join([str((int(255-(float(i))))) for i in ip_l])

print(type(ip))

"192.168.40.7"

[192, 168, 40, 7]