input_file = open('4530.protein.links.v11.0.txt', 'r')
rows = input_file.readline()[0:]

c100 = 0
c200 = 0
c300 = 0
c400 = 0
c500 = 0
c600 = 0
c700 = 0
c800 = 0
c900 = 0
c1000 = 0
for line in input_file:
    row = line.split()
    i = row[2]
    i = float(i)
    if i < 100:
        c100 = c100 + 1
    elif 100 <= i < 200:
        c200 = c200 + 1
    elif 200 <= i < 300:
        c300 = c300 + 1
    elif 300 <= i < 400:
        c400 = c400 + 1
    elif 400 <= i < 500:
        c500 = c500 + 1
    elif 500 <= i < 600:
        c600 = c600 + 1
    elif 600 <= i < 700:
        c700 = c700 + 1
    elif 700 <= i < 800:
        c800 = c800 + 1
    elif 800 <= i < 900:
        c900 = c900 + 1
    elif 900 <= i < 1000:
        c1000 = c1000 + 1
print(c100, c200, c300, c400, c500, c600, c700, c800, c900, c1000)
print(c100 + c200 + c300 + c400 + c500 + c600 + c700 + c800 + c900 + c1000)