''' fitting several polymorphs at a time
could wrap several fit objects

how do i organise files?
    difflets
    data_textom - needs to be only one actually. if peaks overlap they go together
    peak_regions (baseline regions will be common)
    crystal.py


optimizer
    this one should be given just a loss function and a gradient, which i can put together in multifit, that works with a
    combined list of coefficients

load_opt might be hard

visualization (basically all functions that depend on fit)
    all functions should be preserved if there is several, i could just make the fit object a list
    and then functions get an argument that choses the polymorph, with default 0

results
    this is maybe hard, need to label everything with the polymorph number?

'''