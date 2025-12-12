Examples
========

Getting a backend
------------------
::
    
    from pcss_qapi import AuthorizationService
    from pcss_qapi.orca import OrcaProvider

    AuthorizationService.login()

    provider = OrcaProvider()

    backend = provider.least_busy()

TBI sampling
------------------

::

    backend: OrcaBackend = ...

    tbi = backend.get_tbi()

    samples = tbi.sample(input_state=[1, 0], theta_list=[np.pi/4], n_samples=10)


PTLayer inference
------------------

::

    import torch
    
    backend: OrcaBackend = ...

    ptlayer = backend.get_ptlayer(in_features=2)
    output = ptlayer(torch.tensor([[1.0,-1.0]],dtype=torch.float32))

Binary Bosonic Solver training
------------------

::

    backend: OrcaBackend = ...

    objective = lambda sample_array: -sample_array[0] #"optimize" for the first qumode to be a 1

    bbs = backend.get_bbs(pb_dim = 4, objective = objective_function)
    
    bbs.solve(updates=20, print_frequency=2)

    best_energy = bbs.best_cost
    solution = bbs.best_solution
