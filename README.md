# dealuz

**dealuz** is a short and simple package that aims to implement Data Envelopment Analysis (DEA) in python language

# Package Documentation

As stated: short and simple. The whole package is composed of two modules: `definitions` and `core`:

## `core`

At the package's core reside two functions:

### dea

Perform the multiplier Data Envelopment Analysis (DEA) for an activity table

Parameters
----------
tb : pd.DataFrame
    DataFrame which indices are DMUs and columns are features
    representing inputs and outputs

inputs_list : list
    List of features that constitute the inputs. If `VRS = True`
    and `input_oriented = False` a column `VRS` is added to this list

outputs_list : list
    List of features that constitute the outputs. If `VRS =
    input_oriented = True` a column `VRS` is added to this list

VRS : bool, default = False
    A boolean variable that define if the model assume variable
    returns to scale. The default value suposes the model assume
    constant returns to scale (CRS)

input_oriented : bool, default = True
    A boolean variable that define the model orientation. The
    default value suposes an input-oriented model. If False, it
    suposes an output-oriented model

reference_set : bool, default = True
    Defines if the efficiencies result shall contain the efficient
    reference set for each DMU. Default behavior is to include the
    `SET` column in efficiencies DataFrame

Returns
-------
res : DEAResult
    The result object, which is better defined in the definitions section

References
----------
[1] Charnes, A.; Cooper, W. W.; Rhodes, E. "Measuring the efficiency of decision-making units", European Journal of Operational Research, 1978, https://www.sciencedirect.com/science/article/abs/pii/0377221778901388
[2] Cooper, W. W.; Seiford, L. M.; Tone, K. "Data Envelopment Analysis: A Comprehensive Text with Models, Applications, References and DEA-Solver Software", Kluwer Academic Publishers, 2000, https://link.springer.com/book/10.1007/978-0-387-45283-8

### graphical_frontier

Returns a DataFrame with normalized and linearized efficient
frontier for DMUs, as proposed by Bana e Costa et al. (2016)
                                                                              
                                                                              
Parameters
----------
activity_table : (n, k) | (n, k - 1) shaped pd.DataFrame
    DataFrame which indices are DMUs and columns are features
    representing inputs and outputs. If `VRS = True` and `not
    'VRS' in activity_table.columns` then a column `VRS = 1`
    is added to the Dataframe. Afer adding (or not) the `VRS`
    column, it must have the same shape as `dea_weights` DataFrame
                                                                              
dea_weights : (n, k) shaped pd.DataFrame
    Dataframe of DEA weights solutions, as the one yielded by
    `dea` function. It must have the same shape as `activity_table`
    after adding (or not) the `VRS` column
                                                                              
inputs_list : list
    List of features that constitute the model's inputs. If
    `VRS = True` and `input_oriented = False` this list may
    contain the `VRS` variable
                                                                              
outputs_list : list
    List of features that constitute the model's outputs. If
    `VRS = input_oriented = True` this list may contain the
    `VRS` variable
                                                                              
VRS : bool, default = False
    A boolean variable that define if the model assume variable
    returns to scale. The default value, `VRS = False` suposes
    the model assume constant returns to scale (CRS). If `VRS =
    True` and `not 'VRS' in activity_table.columns` then a `VRS
    = 1` columns is added to `activity_table` 
                                                                              
input_oriented : bool, default = True
    A boolean variable that define the model orientation. The
    default value suposes an input-oriented model. If False, it
    suposes an output-oriented model
                                                                              
Returns
-------
graph_data : (n, 2) shaped pd.DataFrame
    A DataFrame containing `INPUT` and `OUTPUT` coordinates, for
    each index DMU, relative to an identity function efficiency
    frontier
                                                                              
References
----------
[1] Bana e Costa, C. A.; Soares de Mello, J. C. C. B.; Meza, L. A. "A new
approach to the bi-dimensional representation of the DEA efficient frontier
with multiple inputs and outputs", European Journal of Operational Research,
2016, https://www.sciencedirect.com/science/article/abs/pii/S0377221716303320

## `definitions`

This module is composed of one `DEAResult` object

### DEAResult

Initializes a result object that is returned by core estimator functions
                                                                            
                                                                            
Parameters
----------
efficiencies : pd.DataFrame
    A DataFrame which indices are DMUs and columns are the
    efficiency score (the DEA objective function value) and,
    if `reference_set = True`, the `SET` reference of efficient
    DMUs for each DMU
                                                                            
weights : pd.DataFrame
    A DataFrame with the weights yielded by each DMU problem
    in DEA. The indices represent the DMUs and the columns
    the variables used by the model
                                                                            
model_params : dict
    A dict containing the params used for the model. This dict
    can be used to run similar models and contain the following
    keys:
        input_oriented : bool
            Boolean value that defines if model assume constant
            returns to scale (CRS) if `VRS = False`, else it
            assumes variable returns to scale (VRS) `VRS = True`
        inputs_list : list
            List of features that constitute the model's input.
            Containing the `VRS` column if the model is output-
            oriented and assume variable returns to scale
        outputs_list : list
            List of features that constitute the model's output.
            Containing the `VRS` column if the model is input-
            oriented and assume variable returns to scale
        input_oriented : bool
            Boolean value that define an input-oriented model.
            If False, defines an output-oriented model

# References

This are some references used to produce this package

* [1] Charnes, A.; Cooper, W. W.; Rhodes, E. "Measuring the efficiency of decision-making units", European Journal of Operational Research, 1978, https://www.sciencedirect.com/science/article/abs/pii/0377221778901388
* [2] Cooper, W. W.; Seiford, L. M.; Tone, K. "Data Envelopment Analysis: A Comprehensive Text with Models, Applications, References and DEA-Solver Software", Kluwer Academic Publishers, 2000, https://link.springer.com/book/10.1007/978-0-387-45283-8
* [3] Bana e Costa, C. A.; Soares de Mello, J. C. C. B.; Meza, L. A. "A new approach to the bi-dimensional representation of the DEA efficient frontier with multiple inputs and outputs", European Journal of Operational Research, 2016, https://www.sciencedirect.com/science/article/abs/pii/S0377221716303320
