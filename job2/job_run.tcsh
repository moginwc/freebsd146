#!/bin/tcsh -f

echo "START: `date`"

set job = "$argv[1]"
set status_filename = "$argv[2]"

echo "COMMAND: $job"

tcsh -f "$job"
set return_code = $status

echo "STATUS: $return_code"
echo "END: `date`"

echo "$return_code" > "$status_filename"

exit 0
