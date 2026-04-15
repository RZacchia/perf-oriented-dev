According to the documentation of gcc 12.2.0 the following flags are different between o2 and o3 verified .
  https://gcc.gnu.org/onlinedocs/gcc-12.2.0/gcc/Optimize-Options.html

> -fgcse-after-reload <br>
> -fipa-cp-clone <br>
> -floop-interchange  <br>
> -floop-unroll-and-jam  <br>
> -fpeel-loops  <br>
> -fpredictive-commoning  <br>
> -fsplit-loops  <br>
> -fsplit-paths  <br>
> -ftree-loop-distribution  <br>
> -ftree-partial-pre  <br>
> -funswitch-loops  <br>
> -fvect-cost-model= very cheap -> dynamic  <br>
> -fversion-loops-for-strides <br>


```
mmul: default (S=1000)
nbody: M=400, others default
qap: chr15c.dat
delannoy: 13

npb_bt: W
ssca: 15
```
fvect-cost-model=dynamic
