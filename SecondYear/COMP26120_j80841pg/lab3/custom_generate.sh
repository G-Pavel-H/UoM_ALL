SIZES="10000 20000 30000 40000 50000 60000 70000 80000 90000 100000 150000 200000"

QUERY_SIZES="0.75 1"

for SIZE in $SIZES
do

for QSIZE in $QUERY_SIZES
do

QUERY_SIZE=$( echo "$SIZE * $QSIZE/1" | bc)

echo $QUERY_SIZE

for COUNT in 1
do

     python3 generate.py data/large/henry/dict data/custom/dict_${SIZE}_${QUERY_SIZE}_$COUNT data/custom/query_${SIZE}_${QUERY_SIZE}_$COUNT $SIZE ${QUERY_SIZE} none 70


done

done

done