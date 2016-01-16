awk '/\/closeio.html/ && $2 !~ /^127./ && $2 !~ /^::1/ {a[$2]++;}END{for (i in a)print i,a[i];}' log.txt | sort -k2 -r
