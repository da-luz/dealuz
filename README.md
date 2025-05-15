# dealuz

**dealuz** is a short and simple package that aims to implement Data Envelopment Analysis (DEA) in python language

## Why this package, what does it do?

This package is built to deal with the main concerns when applying a DEA model: inputs and outputs, returns to scale,
model objective (output and input oriented) and reference sets

The **Data Envelopment Analysis is a diagnostic tool that generates efficiency indexes** for Decision Making Units based
on their Activity. Those indexes are computed primarily based on the **ratio of inputs and outputs of each DMU activity**,
the results, the performance of a DMU in a closed section of time. A practical example is a paper selling company that
want to assess their branches performance based on the ratio between office meetings (as input) and sales performed (as
output)

If one assumes that to each office meeting the sales grow by a fixed and proportional amount, that one is assuming a
**Constant Returns to Scale** model where **each change in the number of meetings** turns into a **proportional change in the
sales amount**. On the other hand if a change in the number of meetings **does not causes a proportional change** in the
sales, one may assume a **Variable Returns to Scale**

Now let's evaluate the company's goal. If the office meetings are the social fuel our sellers crave or the company
has not yet conquered the whole market share and is not willing to reduce the number of meetings, one other may use
an **Output Oriented model** that evaluates the branches on their capability of **maximising sales**. However if the company
is facing the scarcity of time or has already conquered the whole market share, thus having no motivation to expand
in sales, one other may use the **Input Oriented** model that focus on the branch capability of **minimising their meetings**

In the end (if you've done everything right) there may be some inneficient branhces; that's okay, the main purpose of
DEA is not evaluate acceptable levels of activity but to evaluate, between similar branches, which one of they exceeds
expectations. So, if Scranton branch, is deemed as efficient in despite of Utica, Stamford and Nashua, the Scraton branch
sets a new standard for the other branches to follow and the **other branches are evaluated in comparison to the effcient
branch; this is the reference set** for the DEA models

## What is included?

This package includes two DEA related functions:

* [`dealuz.dea`](src/dealuz/core.py) which performs the multiplier Data Envelopment Analysis[^2][^3][^4] for an activity table; and
* [`dealuz.graphical_frontier`](src/dealuz/core.py)based on the work of Bana e Costa et al.[^1] which presents a graphical way
to visualize DEA results

For those OOP lovers, the package also has a [`dealuz.DEAResult`](src/dealuz/definitions.py) object that is returned by `dealuz.dea`
and can be also passed to `dealuz.graphical_frontier`

## References

[^1]: Bana e Costa, C. A.; Soares de Mello, J. C. C. B.; Meza, L. A. "A new approach to the bi-dimensional representation of the DEA
efficient frontier with multiple inputs and outputs", European Journal of Operational Research, 2016,
https://www.sciencedirect.com/science/article/abs/pii/S0377221716303320
[^2]: Banker, R. D.; Charnes, A.; Cooper, W. W. "Some models for estimating techincal and scale ineficiencies in Data Envelopment
Analysis", Management Science, 1984, https://www.jstor.org/stable/2631725?origin=JSTOR-pdf
[^3]: Charnes, A.; Cooper, W. W.; Rhodes, E. "Measuring the efficiency of decision-making units", European Journal of Operational
Research, 1978, https://www.sciencedirect.com/science/article/abs/pii/0377221778901388
[^4]: Cooper, W. W.; Seiford, L. M.; Tone, K. "Data Envelopment Analysis: A Comprehensive Text with Models, Applications, References
and DEA-Solver Software", Kluwer Academic Publishers, 2000, https://link.springer.com/book/10.1007/978-0-387-45283-8
