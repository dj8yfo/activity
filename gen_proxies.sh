#!/bin/bash

for subprj in morphs-swap
do
	rm $subprj/proxies.txt
	while read line
	do
		echo "http://$line" >> $subprj/proxies.txt
	done < proxies.raw

	echo $subprj/proxies.txt
done
