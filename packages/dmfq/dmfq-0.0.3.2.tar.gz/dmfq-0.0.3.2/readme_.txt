
# 本地更新包，先不上传
    可以先不上传，本地先试用迭代一段时间，没为题，再更新上传

    更改 setup.py 里面的 version



    1. 改代码
    2. 本地打包
    3. 本地安装：


cd /home/hjy/ws/utils_sync/utils_git/dmfq
python setup.py sdist
cd /home/hjy/ws/utils_sync/utils_git/dmfq

conda activate base;        pip install dist/dmfq-0.0.3.2.tar.gz
conda activate python37;    pip install dist/dmfq-0.0.3.2.tar.gz
conda activate GI-GS;       pip install dist/dmfq-0.0.3.2.tar.gz
conda activate evllgs;      pip install dist/dmfq-0.0.3.2.tar.gz
conda activate videoinr;    pip install dist/dmfq-0.0.3.2.tar.gz
conda activate CBMNet;      pip install dist/dmfq-0.0.3.2.tar.gz
conda activate vid2e;       pip install dist/dmfq-0.0.3.2.tar.gz
conda activate gspl;        pip install dist/dmfq-0.0.3.2.tar.gz


# pipx install dist/dmfq-0.0.3.2.tar.gz  是没意义的， 应为dmfq是库，不是命令行工具CLI

# 更新完代码之后，上传pypi

    每次上传 pypi 之后，这个版本号就上传不上去了，得用新的保本号
    更改 setup.py 里面的 version, 需要跟以往上传的都不同

    twine upload dist/dmfq-0.0.3.1.tar.gz



pip install dmfq==0.0.3.1












conda activate python37;    pip install -U jupyter
conda activate videoinr;    pip install -U jupyter
conda activate CBMNet;      pip install -U jupyter
conda activate vid2e;       pip install -U jupyter
conda activate pytorch_GPU_py310;   pip install -U jupyter
conda activate pytorch_GPU;         pip install -U jupyter
conda activate pytorch_lighting;    pip install -U jupyter