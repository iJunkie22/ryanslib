#!/bin/bash
sq="'"
rcode=$(cat "$2" | (grep -n -m1 -e "$1") | cut -d ':' -f1);

exit $rcode
