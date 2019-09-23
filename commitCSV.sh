git log --pretty="format:%ai,%an,%s,%h" --before=$1 2>&1 | tee ../meta/mvp.txt
