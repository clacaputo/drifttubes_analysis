# drifttubes_analysis

## Setup

On lxplus:

```bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_98python3/x86_64-centos7-gcc10-opt/setup.sh
```

## Landau fit

```bash
find /eos/user/c/ccaputo/TestBeam_ClusterCounting/11Nov/ -type f -name "*pkl" -exec python landau_fit.py --input {} \;
```