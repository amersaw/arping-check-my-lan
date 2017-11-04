# after downloadig the manuf db from wireshark website
# https://www.wireshark.org/tools/oui-lookup.html
# applying this script will fix the comment fild so it can be accessable
# using the get_comment or the get_all method

f = open ('manuf', 'r')
lines = f.readlines()
for i in range(len(lines)):
  parts = lines[i].split('\t')
  if len(parts) == 3:
    parts[2] = '#' + parts[2]
    lines[i] = str.join('\t',parts)

f.close()
f = open('manuf2','w')
f.writelines(lines)
f.close()
