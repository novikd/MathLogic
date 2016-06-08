#!/bin/bash

RED='\033[0;31m'

NC='\033[0m' # No Color

function test {
	printf "Testing ${RED}$2${NC}\n"
	cat tests/HW4/$1correct$2.in > hw4.in
	pypy3 homework4.py
}

printf "${RED}TESTING CORRECT PROVES${NC}\n"
test "" 1
test "" 2
for i in `seq 5 15`
do
	test "" $i
done

printf "${RED}TESTING INCORRECT PROVES${NC}\n"
for i in `seq 1 11`
do
	test "in" $i
done

