#!/bin/tcsh -f

# 接続ディスクの取得
set disks = (`sysctl -n kern.disks`)

if ($#disks == 0) then
    echo "ディスクが見つかりません."
    exit 1
endif

# メニュー項目の作成
set items = ()

foreach disk ($disks)
    set items = ($items "$disk" "ディスク情報を表示")
end

# ディスク選択
set selected = `( bsddialog \
    --title " ディスクパーティション情報表示 " \
    --menu "情報を表示するディスクを選択してください." 0 0 0 \
    $items \
    > /dev/tty ) >& /dev/stdout`

# キャンセルされた場合
if ($#selected == 0) then
    echo "キャンセルされました."
    exit 1
endif

# パーティション情報の表示
echo ""
echo "選択したディスク: $selected[1]"
echo ""

gpart show "$selected[1]"

