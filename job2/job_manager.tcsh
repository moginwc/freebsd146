#!/bin/tcsh -f

set dir = "$HOME/job2"
set max = 3
set nonomatch

while (1)
    set busy = 0

    @ slot = 1
    while ($slot <= $max)

        if (-e "$dir/state/slot${slot}_completed.stat") then
            rm -f "$dir/state/slot${slot}_running.stat" \
                  "$dir/state/slot${slot}_completed.stat"
        endif

        if (-e "$dir/state/slot${slot}_running.stat") then
            @ busy++
		endif

        @ slot++
    end

    if ($busy < $max) then
        foreach req ($dir/queue/request_*.req)
            if (-f "$req" && $busy < $max) then
                set slot = 1
                while ($slot <= $max)
                    if (! -e "$dir/state/slot${slot}_running.stat") break
                    @ slot++
                end

                if ($slot <= $max) then
                    set job = "`cat "$req"`"

                    tcsh -f "$dir/bin/job_run.tcsh" "$job" \
                        "$dir/state/slot${slot}_completed.stat" \
                        >& "$dir/logs/${req:t:r}.log" &

                    echo $! > "$dir/state/slot${slot}_running.stat"
                    rm -f "$req"
                    @ busy++
                endif
            endif
        end
    endif

    sleep 1
end

