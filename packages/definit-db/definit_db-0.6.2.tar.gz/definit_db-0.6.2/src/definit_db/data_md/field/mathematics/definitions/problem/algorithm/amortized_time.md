# amortized time


[amortized time](mathematics/amortized time) is a method of analyzing the [time complexity](mathematics/time_complexity) 
of a [sequence](mathematics/sequence) of [operations](mathematics/operation) by calculating the average 
cost per [operation](mathematics/operation) over the entire sequence, rather than analyzing individual operations 
in isolation. This approach is particularly useful for [algorithms](mathematics/algorithm) 
where some operations are expensive but occur infrequently, while most operations are cheap. Amortized analysis 
guarantees that the average cost per operation over any sequence remains [bounded](mathematics/bound), 
even though individual operations may occasionally be costly.

