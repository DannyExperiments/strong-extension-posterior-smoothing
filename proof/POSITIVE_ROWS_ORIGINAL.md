# Q432 appendix: strictly positive rational kernels

This strengthens the already delivered general finite-state HMM hardness proof, not the fixed-alphabet result. Use its 3-CNF gap: with A=m+n, L=1/4, H=3/4, d=H−L, YES attains t=AH/(AH+nL), while NO is at most b=max{(AH−d)/(AH−d+nL), AH/(AH+nL+d)}. Set g=t−b>0 (a rational of polynomial bit length). Use (t+b)/2 as threshold.

For each initial or conditional row p, replace its row polytope K by (1−e)K+e u where u is uniform on the whole row alphabet, e=g/128. This affine bijection preserves separate specification. Apply it to each vertex or substitute p=(p'−e u)/(1−e) in an H-description, with polynomial encoding overhead. All probabilities are strictly positive. In the base reduction choose all otherwise unused final emission rows to have success probability 1/2. Thus final success lies in [1/4,3/4] given each final state in both models and evidence remains ≥1/4 uniformly.

For corresponding precise laws, couple the initial draw, two transitions and final emission by using the original row whenever histories agree except when the smoothing coin succeeds. The chance of any relevant difference is at most 4e; unobserved earlier emissions can be integrated out. For Q the query event and E the evidence, let a=P(Q∩E), v=P(E), a',v' the smoothed quantities. Then
|a/v−a'/v'| ≤ (|a−a'|+(a'/v')|v'−v|)/v ≤ 8·4e=g/4.
Taking maximum over corresponding factorizing laws (unchanged by their convex hull for a conditional ratio) proves that YES remains strictly above the new threshold and NO strictly below. This gives strict-positive hardness with three time steps, one binary observation and uniformly positive evidence, but permits input-dependent probabilities arbitrarily close to zero. No additional problem count.

The [manuscript](../paper/manuscript.pdf) gives the stronger fixed-half signed-score formulation and credits the earlier general positivity perturbation method.
