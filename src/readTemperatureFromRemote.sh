#!/bin/bash
/usr/bin/snmpget -c public -v 1 $1 iso.3.6.1.4.1.65535.2.3.1.1.9.47.98.105.110.47.98.97.115.104 |
  /usr/bin/perl -e '<STDIN> =~ m/\"(temp1:.*?)\"/; print $1;'
exit 0;
  
