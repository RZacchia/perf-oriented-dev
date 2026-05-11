Exercise Sheet 8 Robert Zacchia
================

A) False Sharing
----------------

> Have a look at this git PR:
> https://github.com/KhronosGroup/Vulkan-ValidationLayers/pull/5587
> 
> Explain the problem it tries to solve, and how it attempts to do so.

Overview:
False sharing happens, when a cache line contains multiple elements on which multiple threads operate on. (e.g. cache line has 64 byte). When the different threads change, the value of a variable (not the same variable) in the same cache line, the whole cache line gets rendered invalid for all other threads.

False sharing can be solved in different ways, mostly Padding and Alignment.
Padding is manually ```char padding[64]``` filling the cache line to prevent, that multiple variables lie on the same cache line/

Alignment works syntactically different, but similar with optimization flags.
Adding something like:
```c
struct alignas(64) ThreadData {
    
};
```


Instead of:
```c
struct Shared {
    int a;
    int b;
};
```

They restructure into:
```c
struct A { int a; };
struct B { int b; };
```
Before:

[ Thread A var ][ Thread B var ]  <-- same cache line
          ↑         ↑
     both cores fight over this line

After:

[ Thread A var ................. ]  <-- cache line 1
[ Thread B var ................. ]  <-- cache line 2

No more contention.

B) Data Structure Selection
---------------------------

> Search on Github for a merged pull request in a reasonably sized and popular project (>100 stars) which replaces a data structure in order to improve performance.
> Examine the use of this data structure, evaluating all the decision criteria discussed in the lecture, and report your findings.
> Do these criteria help indicate that the change in data structure would be beneficial?

For this task I chose a [pull request](https://github.com/dotnet/roslyn/pull/33840/changes#diff-e129d1317cf310702ed4d7bf9226b280d8678821615d33060c99811c0c8508f1
) for the roslyn C# compiler. 

GreenNode.cs is an immutable treenode. It is used in the CodeAnalysis library of dotnet. It is used to represent the abstract syntax tree (AST) of the code used by the compiler. It does not include parent pointers. The class has a method ```WriteTo()``` which traverses the tree, and writes text into it.

To prevent recursion this method used a ```Stack<(GreenNode node, bool leading, bool trailing)>``` in the past.
In the above mentioned pull request it was changed to ```ArrayBuilder<(GreenNode node, bool leading, bool trailing)>```.
The ```ArrayBuilder<T>``` data structure is not exposed to the public API and hence cannot be used with normal C# code.
The public equivalent would be ```ArrayPool<T>```, which works in a similar way to ```ArrayBuilder<T>```. The data structure was NOT changed because of the complexity class. and the ```ArrayBuilder<T>``` was still used as a stack logically.

The main difference between ```Stack<T>``` and ```ArrayBuilder<T>``` is that ```Stack<T>``` grows dynamically and is handled by the GC while ```ArrayBuilder<T>``` is a pooled resizable array-backed builder which prevents reallocations when new elements are added. It also needs to freed manually.

This improves the memory consumption and overhead

I made a minimal working example using [BenchmarkDotnet](https://benchmarkdotnet.org/) comparing ```ArrayPool<T>``` and ```Stack<T>```.

| Method                | Depth | Branching | Mean          | Error         | StdDev        | Median        | Ratio | RatioSD | Gen0   | Allocated | Alloc Ratio |
|---------------------- |------ |---------- |--------------:|--------------:|--------------:|--------------:|------:|--------:|-------:|----------:|------------:|
| TraverseWithStack     | 5     | 2         |      1.189 us |     0.0752 us |     0.2145 us |      1.133 us |  1.03 |    0.25 | 0.0839 |     176 B |        1.00 |
| TraverseWithArrayPool | 5     | 2         |      1.313 us |     0.1115 us |     0.3289 us |      1.262 us |  1.14 |    0.34 |      - |         - |        0.00 |
|                       |       |           |               |               |               |               |       |         |        |           |             |
| TraverseWithStack     | 5     | 4         |     26.756 us |     2.1290 us |     6.2774 us |     25.015 us |  1.05 |    0.35 | 0.1526 |     328 B |        1.00 |
| TraverseWithArrayPool | 5     | 4         |     24.307 us |     1.8132 us |     5.3179 us |     23.198 us |  0.96 |    0.31 |      - |         - |        0.00 |
|                       |       |           |               |               |               |               |       |         |        |           |             |
| TraverseWithStack     | 10    | 2         |     38.812 us |     2.2416 us |     6.3954 us |     38.518 us |  1.03 |    0.24 | 0.1221 |     328 B |        1.00 |
| TraverseWithArrayPool | 10    | 2         |     30.619 us |     0.8260 us |     2.2888 us |     29.920 us |  0.81 |    0.14 |      - |         - |        0.00 |
|                       |       |           |               |               |               |               |       |         |        |           |             |
| TraverseWithStack     | 10    | 4         | 45,307.966 us | 1,637.2179 us | 4,801.6770 us | 46,281.724 us |  1.01 |    0.16 |      - |     608 B |        1.00 |
| TraverseWithArrayPool | 10    | 4         | 53,197.742 us | 2,522.4100 us | 7,196.5782 us | 52,693.190 us |  1.19 |    0.21 |      - |         - |        0.00 |



Submission
----------
Please submit your solutions by email to peter.thoman at UIBK, using the string "[Perf2026-sheet8]" in the subject line, before the start of the next VU at the latest.  
Try not to include attachments with a total size larger than 2 MiB.
