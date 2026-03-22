# Exercise 03 - Robert Zacchia

## Task 1 gprof

To enable instrumentation of the programs I had to add the flags -pg to compilation and linking the CMakeList.txt

```
  add_compile_options(-Wall -Wextra -Wno-unknown-pragmas -Wno-unused-parameter -pg)
  set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -pg")
```
https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html


>-p
>--profile
>-fprofile
>-pg
>
>    Generate extra code to write profile information suitable for the analysis prof (for -p, --profile, and -fprofile) or gprof (for -pg). You must use this option when compiling the source files you want data about, and you must also use it when linking.
>
>    You can use the function attribute no_instrument_function to suppress profiling of individual functions when compiling with these options. See Common Attributes.

After execution the instrumented program we can output the sampling results into a text file.

```bash
./npb_bt_b
mv gmon.out gmon_b.out
gprof ./npb_bt_b gmon_b.out > profile_b.txt
```

Differences between _a and _b on lcc3.


The main difference between local and lcc3 execution were the overall execution time. I could not find sufficient variations in percentage of the different functions between the two systems to warrant further analysis:





## Task 2 Tracy