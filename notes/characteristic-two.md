# A nonzero solution in characteristic two

**Proved example.** On $R=M_2(\mathbb F_2)$, define

$$f(X)=g(X)=\operatorname{tr}(X)I.$$

These maps are additive and nonzero, since $f(E_{11})=I$. They satisfy

$$f(X)X^{-1}+X^2g(X^{-1})=0$$

for every invertible $X$.

## Direct proof

An invertible $2\times2$ matrix over $\mathbb F_2$ has determinant 1.
Writing $t=\operatorname{tr}(X)$, direct multiplication (or the
$2\times2$ Cayley–Hamilton identity) gives

$$X^2+tX+I=0.$$

The inverse formula gives $\operatorname{tr}(X^{-1})=t$.
If $t=0$, both map values in the identity vanish. If $t=1$, the displayed
equation gives $X^2+X+I=0$, so multiplication by $X+I$ gives $X^3=I$.
Thus $X^{-1}=X^2$ and

$$f(X)X^{-1}+X^2g(X^{-1})=X^{-1}+X^2=0.$$

This example concerns a noncommutative **matrix ring**. It is not a
counterexample on a noncommutative division ring.
