#!/bin/bash
# scripts/RunMultiple.sh
#
# to be run in DACHS source top-level directory
pushd "$(dirname $0)" > /dev/null
SCRIPTPATH="$(pwd)"
popd > /dev/null

echo "Using SCRIPTPATH: '$SCRIPTPATH'"

monitorFiles="AutoMOFs05_[MLTH]???.xlsx"
dataPath="$1" # first command line argument

# check if given arg is an existing dir, set it a default otherwise
[ -d "$dataPath" ] || dataPath="$SCRIPTPATH/../tests/testData"

files="$(find "$dataPath" -maxdepth 3 -name "$monitorFiles" -type f | head -n 1)"
echo "Found the following files for processing:"
echo "$files"

for f in $files;
do
        echo "Processing '$f'…" # >> ~/raw.log 2&>1
        PYTHONPATH=src python -m dachs -l "$dataPath/AutoMOFs_Logbook_Testing.xlsx" -s0 "$dataPath/AutoMOFs05_Solution0.xlsx" -s1 "$dataPath/AutoMOFs05_Solution1.xlsx" -s "$f" -a AMSET_5
        # groupNum=`echo "$f" | awk '{split($0,a,"_"); print a[2]}'`
        # python3 processingCode/datamerge/main.py -f "$f" -C "$toProcess/mergeConfig.yaml" -o "$toProcess/merged-$groupNum.nxs" -g "20*.nxs"
        # python3 processingCode/datamerge/main.py -f "$f" -C "$toProcess/mergeConfig.yaml" -o "$toProcess/automatic.nxs" -g "20*.nxs"
        # python3 processingCode/scicatMergedDataUpload.py -f "$toProcess/merged-$groupNum.nxs"
done
