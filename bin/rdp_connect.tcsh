#!/bin/tcsh -f

set result = `( bsddialog \
    --title " リモートデスクトップ接続... " \
    --insecure \
    --mixedform "リモートデスクトップ接続" 11 60 3 \
    "コンピューター：" 0 0 ""  0 18 30 255 0 \
    "ユーザー名："     1 0 ""  1 18 30 255 0 \
    "パスワード："     2 0 ""  2 18 30 255 1 \
    --output-separator " " \
    > /dev/tty ) >& /dev/stdout`

set ret = $status

if ( $ret != 0 ) then
    echo "キャンセルされました."
    exit 1
endif

set server = "$result[1]"
set user   = "$result[2]"
set passwd = "$result[3]"

printf "%s\n" "$passwd" | xfreerdp \
    /v:"$server" \
    /u:"$user" \
    /from-stdin:force \
    /size:1024x600 /sound /clipboard /cert-ignore

unset passwd
unset result
