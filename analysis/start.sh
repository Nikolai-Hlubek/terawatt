sed "s/^b//g" /vagrant/data/$1.raw | sed "s/'//g" | sed "s/$/,/g" | sed '$s/},/}/g' | sed "1 i \[" | sed -e "\$a]" | sed 's/value":-/value":/g' | in2csv -f json > $1.csv
./analysis.r $1 $2
