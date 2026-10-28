# The Julia side of `somegraphspy`: the helpers its wrappers call, and the precompilation of the calls Python makes.
#
# Python always loads `PythonCall` before anything else, so this loads it first too, and is precompiled the same way.
# Its workload runs `somegraphspy.workloads.run_workload()` from Python, so this package caches the code those calls
# compile, and a session does not compile it again.
module SomeGraphsPy

using PythonCall
using PrecompileTools

import SomeGraphs
import SomeGraphs.Common.Hclust
import SomeGraphs.Common.OrderedDict

# The code this caches depends on the Python code of `somegraphspy`, which runs the workload. Julia only knows of its
# own sources, so this tells it to compile again when any of those files changes.
const SOMEGRAPHSPY_DIRECTORY = joinpath(@__DIR__, "..", "..", "..")
for name in readdir(SOMEGRAPHSPY_DIRECTORY)
    if endswith(name, ".py")
        include_dependency(joinpath(SOMEGRAPHSPY_DIRECTORY, name); track_content = true)
    end
end

function pyconvert_rule_jl_object(::Type{T}, x::Py) where {T}
    return PythonCall.pyconvert_return(pyconvert(T, x.jl_obj))
end

# Build a vector of pairs of values, whose element type Julia infers from the (already converted) vectors. A list of
# Python tuples would arrive as a ``PyList{Any}``, which Julia can't convert to a vector of tuples.
function _tuples_vector(firsts::AbstractVector, seconds::AbstractVector)::AbstractVector
    return [(first, second) for (first, second) in zip(firsts, seconds)]
end

# Re-infer the element type of a vector whose entries are already Julia values. This turns the ``Vector{Any}`` we get
# for a list of arrays or of objects into a properly typed vector.
function _typed_vector(items::AbstractVector)::AbstractVector
    return [item for item in items]
end

# Classify an array by what its entries are, to pick the matching Python representation.
function _array_kind(array::AbstractArray)::String
    element_type = eltype(array)
    if element_type <: Real
        return "numbers"
    elseif element_type <: AbstractString
        return "strings"
    else
        return "other"
    end
end

# Run a Python visitor over the sinks. A Python callable is not a Julia ``Function``, so it is wrapped in one.
function _visit_data_sinks(visitor::Py, sinks::Any)::Nothing
    return SomeGraphs.visit_data_sinks(sink -> (visitor(sink); nothing), sinks)
end

function _visit_configuration_sinks(visitor::Py, sinks::Any)::Nothing
    return SomeGraphs.visit_configuration_sinks(sink -> (visitor(sink); nothing), sinks)
end

function _visit_graph_parts(visitor::Py, target::Any)::Nothing
    return SomeGraphs.visit_graph_parts(part -> (visitor(part); nothing), target)
end

# A tree from a SciPy linkage matrix. Each row of it is a merge, ``[left, right, height, count]``. Its node indices are
# 0-based, with the leaves first and each merge numbered after them. The matrix does not say which linkage built the
# tree, so that is ``:unknown``.
function _hclust_from_linkage(linkage::AbstractMatrix{<:Real})::Hclust
    n_merges = size(linkage, 1)
    n_leaves = n_merges + 1
    merges = Matrix{Int}(undef, n_merges, 2)
    for merge_index in 1:n_merges
        for column in 1:2
            node = Int(linkage[merge_index, column])
            merges[merge_index, column] = node < n_leaves ? -(node + 1) : node - n_leaves + 1
        end
    end
    return Hclust(merges, Float64.(linkage[:, 3]), _walked_leaves(merges), :unknown)
end

# The leaves of a tree from its root, left subtree first, which is its order. This walks rather than recurses, since a
# tree of many leaves may be as deep as it is wide.
function _walked_leaves(merges::AbstractMatrix{<:Integer})::Vector{Int}
    n_merges = size(merges, 1)
    if n_merges == 0
        return [1]
    end
    order = Int[]
    pending = [n_merges]
    while !isempty(pending)
        node = pop!(pending)
        if node < 0
            push!(order, -node)
        else
            push!(pending, merges[node, 2])
            push!(pending, merges[node, 1])
        end
    end
    return order
end

# The SciPy linkage matrix of a tree (see ``_hclust_from_linkage``).
function _linkage_from_hclust(clusters::Hclust)::Matrix{Float64}
    n_merges = size(clusters.merges, 1)
    n_leaves = n_merges + 1
    linkage = Matrix{Float64}(undef, n_merges, 4)
    count_per_merge = Vector{Int}(undef, n_merges)
    for merge_index in 1:n_merges
        count = 0
        for column in 1:2
            node = clusters.merges[merge_index, column]
            if node < 0
                linkage[merge_index, column] = -node - 1
                count += 1
            else
                linkage[merge_index, column] = node - 1 + n_leaves
                count += count_per_merge[node]
            end
        end
        count_per_merge[merge_index] = count
        linkage[merge_index, 3] = clusters.heights[merge_index]
        linkage[merge_index, 4] = count
    end
    return linkage
end

# The conversion rule is registered at load time, since a precompiled package does not keep the side effects of its
# top level.
function __init__()::Nothing
    PythonCall.pyconvert_add_rule("somegraphspy.julia_import:JlObject", Any, pyconvert_rule_jl_object)
    return nothing
end

# Whether the Python that `PythonCall` runs imports the `somegraphspy` this package belongs to. A precompilation started
# from plain Julia gets whatever Python `PythonCall` finds, which may lack `somegraphspy`, or have a version of it
# without this package beside it. A directory named `somegraphspy` in the working directory is also found, as a
# namespace with no origin.
function is_matching_somegraphspy()::Bool
    spec = pyimport("importlib.util").find_spec("somegraphspy")
    if pyis(spec, pybuiltins.None) || pyis(spec.origin, pybuiltins.None)
        return false
    end
    project_path = joinpath(dirname(pyconvert(String, spec.origin)), "julia", "SomeGraphsPy", "Project.toml")
    return isfile(project_path) && occursin("uuid = \"$(Base.PkgId(SomeGraphsPy).uuid)\"", read(project_path, String))
end

@compile_workload begin
    __init__()
    if !is_matching_somegraphspy()
        error(
            "SomeGraphsPy could not be precompiled: the Python that PythonCall runs ($(PythonCall.C.CTX.exe_path)) " *
            "does not import the somegraphspy that SomeGraphsPy belongs to.\n" *
            "This is harmless: SomeGraphsPy will be precompiled the first time you import somegraphspy from Python.\n" *
            "To do it now, run: python -c \"import somegraphspy\" (with the Python where somegraphspy is installed).",
        )
    end
    # While this is precompiled, `somegraphspy` cannot import it into Julia's `Main`, so it is handed over here instead.
    pysetattr(pyimport("builtins"), "_somegraphspy_glue", Py(SomeGraphsPy))
    pyexec("from somegraphspy.workloads import run_workload\nrun_workload()", pydict())
end

end  # module
