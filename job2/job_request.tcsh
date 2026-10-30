#!/bin/tcsh -f

set dir = "$HOME/job2"

if ($#argv != 1) then
    echo "Usage: job_request.tcsh command"
    exit 1
endif

set job = "$argv[1]"
if (! -f "$job") then
    echo "Command not found: $job"
    exit 1
endif

if ("$job" !~ /*) set job = "$cwd/$job"

set request_filename = "request_`date +%Y%m%d%H%M%S`_$$"
echo "$job" > "$dir/queue/.tmp_$$"
mv "$dir/queue/.tmp_$$" "$dir/queue/$request_filename.req"

echo "Requested: $request_filename"
exit 0

