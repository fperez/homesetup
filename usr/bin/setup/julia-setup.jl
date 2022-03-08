#!/usr/bin/env julia
# Configure and setup Julia installation

# Add most needed packages

using Pkg

# Set up basic Python support first using Conda defaults

ENV["PYTHON"] = "/Users/fperez/local/conda/bin/python"
Pkg.add("PyCall")
Pkg.build("PyCall")  # The rebuild seems necessary for conda integration

# Julia kernels for Jupyter and plotting
Pkg.add(["IJulia", "PyPlot" ])


# Scientific Machine Learning packages needed to reproduce results shown in
# Universal Differential equations paper - https://arxiv.org/abs/2001.04385
Pkg.add(["OrdinaryDiffEq", "ModelingToolkit", "DataDrivenDiffEq",
         "LinearAlgebra", "DiffEqSensitivity", "Optim", "DiffEqFlux",
         "Flux", "Plots"])
