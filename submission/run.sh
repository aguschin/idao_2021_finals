set -ex
export PATH=/usr/conda/bin:"$PATH"
python generate_submission.py
ls -lh .
export timestamp=`date "+%Y%m%d_%H-%M-%S_UTC"`
[ -d "/submissions" ] && mv submission.csv /submissions/${timestamp}.csv
echo "completed"
