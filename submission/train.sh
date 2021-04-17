set -ex
export PATH=/usr/conda/bin:"$PATH"
python train_model.py
ls -lh .
export timestamp=`date "+%Y%m%d_%H-%M-%S_UTC"`
echo ${timestamp}.tar.gz > archive_name
[ -d "/submissions" ] && tar -zcvf /submissions/${timestamp}.tar.gz --exclude='data' *
echo "trained"
