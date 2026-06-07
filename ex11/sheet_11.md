Exercise Sheet 11 - Robert Zacchia
=================



A) Applying Memoization (optional)
----------------------------------

>Apply basic hash-based memoization to `small_samples/delannoy` and benchmark your implementation. 
>
> * What level of performance improvement can you achieve, both theoretically and practically?  
> * What is the space complexity of your optimized version in terms of the parameters `x` and `y`?


The naive Delannoy approach has a time complexity of O(3^(x+y)). The theoretical improvement should be O(x*y).


B) Algorithm Tabulation (optional)
----------------------------------

> Use dynamic programming tabulation to implement the `delannoy` benchmark while only requiring `O(x)` additional space and no hashing. Benchmark this solution and compare the results to basic hash-based memoization.




