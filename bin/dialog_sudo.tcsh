#!/bin/tcsh -f

set result = `( bsddialog \
    --insecure \
    --passwordbox "sudoのパスワードを入力してください." 9 48 \
    > /dev/tty ) >& /dev/stdout`

set ret = $status

if ( $ret != 0 ) then
    echo "キャンセルされました."
    exit 1
endif

printf "%s\n" $result | sudo -S -p "" -v
set ret = $status
unset result

if ( $ret != 0 ) then
    echo "強制終了します."
    sudo -k
    exit 1
endif

sudo chmod 770 /mnt

sudo -k
