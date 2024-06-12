SIZES="10000 20000 30000 40000 50000 60000 70000 80000 90000 100000 150000 200000"

QUERY_SIZES="0.75"

for SIZE in $SIZES
do

for QSIZE in $QUERY_SIZES
do

QUERY_SIZE=$( echo "$SIZE * $QSIZE/1" | bc)

echo $QUERY_SIZE

for COUNT in 1
do

     python3 python/speller_bstree.py -d data/custom/dict_${SIZE}_${QUERY_SIZE}_$COUNT -m 0 -vvv data/custom/query_${SIZE}_${QUERY_SIZE}_$COUNT

done

done

done