# drifttubes_analysis

## Setup

On lxplus:

```bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_98python3/x86_64-centos7-gcc10-opt/setup.sh
```
**Compile decoder**

```bash
g++ -std=c++17 -I`root-config --incdir` -L`root-config --libdir` `root-config --libs` `root-config --cflags` read_binary_comp.C -o decode.exe
```

## Landau fit

```bash
find /eos/user/c/ccaputo/TestBeam_ClusterCounting/11Nov/ -type f -name "*pkl" -exec python landau_fit.py --input {} \;
```
