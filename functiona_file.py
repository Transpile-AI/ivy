# manupulation.py
jax.numpy.histogram(
    a, 
    bins=10, 
    range=None, 
    density=False, 
    weights=None, 
    cumulative=False)

Return Tuple[Array, Array]
       hist (array)
       bin_edges (length(hist)+1)

# Generate some random data
data = jax_histogram.random.normal(size=1000)

# Compute the histogram with 10 bins
hist, bin_edges = jax_histogram.histogram(data, bins=10)

# backend

def jax_histogram(self: np.Array, 
    /, 
    *,
    input: Optional[int, str, bins, int],
    name: Optional[np.array[int]], 
    weight: Optional[Union[density[bool]] = True,
    data: Optional[Union[weights]] = None,
    normed: Optional [normed[bool]] = None
    step: Optional[Union[range(float,float)] = None, 
    buckets: Optional[np.array[float(name.min()), float(name.max)]], 
    description: Optional[np.Array[str],np.Array[bin] = 10],
    ) -> ivy.Array:

    Return jax_histogramTuple
        ([Array, Array]
        hist (array)
        bin_edges (length(hist)+1)
        )
