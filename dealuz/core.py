"""Core functions responsible for executing DEA"""


__all__ = [
    "dea",
    "graphical_frontier",
]


import pandas as pd
from pulp import LpProblem, LpVariable, lpDot

from dealuz.definitions import DEAResult


def dea(
    tb: pd.DataFrame,
    inputs_list: list[str],
    outputs_list: list[str],
    VRS: bool = False,
    input_oriented: bool = True,
    reference_set: bool = True
) -> DEAResult:
    """Perform the multiplier Data Envelopment Analysis (DEA) for an activity table

    
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
        An object containing attributes:

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

    References
    ----------
    [1] Charnes, A.; Cooper, W. W.; Rhodes, E. "Measuring the efficiency of
    decision-making units", European Journal of Operational Research, 1978,
    https://www.sciencedirect.com/science/article/abs/pii/0377221778901388
    [2] Cooper, W. W.; Seiford, L. M.; Tone, K. "Data Envelopment Analysis: A Comprehensive
    Text with Models, Applications, References and DEA-Solver Software", Kluwer
    Academic Publishers, 2000, https://link.springer.com/book/10.1007/978-0-387-45283-8

    """

    results = []
    solutions = []

    tb = tb.copy()

    # The objective of this is to support both
    # explicit (VRS = True) and implicit (tb['VRS'])
    # scale declarations
    if VRS or 'VRS' in set(inputs_list + outputs_list):

        # For implementing VRS (BCC) model an unitary
        # column is needed so the algorithm can calculate
        # the independent variable
        tb.loc[:, 'VRS'] = 1
        if input_oriented:
            if not 'VRS' in outputs_list:
                outputs_list.append('VRS')

        else:
            if not 'VRS' in inputs_list:
                inputs_list.append('VRS')

    # Declare the columns that will be present
    # in the efficiencies (results) table
    eff_cols = ['DMU', 'INDEX']
    if reference_set:
        eff_cols.append('SET')

    # Each one of those tables is used for estimating
    # the inputs or outputs weights. Zeroing the unecessary
    # columns help in multiplying the matrices
    inp = tb.copy()
    inp[outputs_list] = 0

    out = tb.copy()
    out[inputs_list] = 0

    # Hereafter, the algorithm
    # Creating a list of variables, these are the values
    # for which the weights are generated
    variables = tb.columns.tolist()
    for dmu in tb.index:

        # The pulp package requires each round to have a name
        p_name = dmu.replace(" ", "_")

        # The pulp package have some constants for declaring
        # the sense of the problems (maximising of minimising)
        # The constants we need are 1 (minimising) and -1 (maximising)
        # When input_oriented = True the probem sense will be 1 - (1 * 2) = -1 (maximising)
        # When input_oriented = False the probem sense will be 1 - (0 * 2) = 1 (minimising)
        prob = LpProblem("DMU_" + p_name, 1 - (input_oriented * 2))

        # Declaring the variables, those for which weights are estimated
        prob_vars = LpVariable.dicts("coefficient", variables, 10e-5)
        weights = prob_vars.values()

        # Defining the objective of the problem
        objective = out if input_oriented else inp
        objective: pd.Series = objective.loc[dmu]
        objective = objective.values

        prob += (lpDot(objective, weights), p_name + "_index")

        # Defining the linearization constraint
        linear = inp if input_oriented else out
        linear: pd.Series = linear.loc[dmu]
        linear = linear.values

        prob += (lpDot(linear, weights) == 1, "linearization")

        # Each DMU have an associated constraint
        for dmu_cons in tb.index:
            in_cons: pd.Series = inp.loc[dmu_cons]
            in_cons = in_cons.values

            out_cons: pd.Series = out.loc[dmu_cons]
            out_cons = out_cons.values

            prob += (
                # Contraint
                lpDot(out_cons, weights) <= lpDot(in_cons, weights),

                # Constraint name
                dmu_cons.replace(" ", "_") + "_constraint"
            )

        # This initiates the optimiser
        prob.solve()

        # This collects all the problem weights
        solv = []
        for var in variables:

            # Getting the weight
            w = prob.variablesDict().get('coefficient_' + var.replace(' ', '_')).varValue
            
            # Checking if the weight is a number
            w = w if isinstance(w, (float, int)) else 0

            solv.append(w)

        # The objective value is the DMU efficiency value
        obj_value = round(prob.objective.value(), 5)
        dmu_res = [dmu, obj_value]

        # The reference set represents the union of DMUs
        # which are also efficient at the specific frontier
        if reference_set:
            cons_eff: pd.Series = (out @ solv) / (inp @ solv)
            ref_set = " | ".join(cons_eff[round(cons_eff, 5) == 1].index)
            dmu_res.append(ref_set)

        # Collecting the results for this turn
        results.append(dmu_res)
        solutions.append([*solv, dmu])

    # Creates two tables containing the DMUs efficiency and the weights for each DMU
    results = pd.DataFrame(results, columns=eff_cols).set_index("DMU")
    solutions = pd.DataFrame(solutions, columns=[*tb.columns, "DMU"]).set_index("DMU")

    # Collecting the parameters for this model
    model_params = {
        'VRS': VRS or 'VRS' in set(inputs_list + outputs_list),
        'inputs_list': inputs_list,
        'outputs_list': outputs_list,
        'input_oriented': input_oriented
    }

    return DEAResult(results, solutions, model_params)


def graphical_frontier(
    activity_table: pd.DataFrame,
    dea_weights: pd.DataFrame,
    inputs_list: list[str],
    outputs_list: list[str],
    VRS: bool = False,
    input_oriented: bool = True,
    **kwargs
) -> pd.DataFrame:
    """Returns a DataFrame with normalized and linearized efficient
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

    """

    activity_table = activity_table.copy()

    # Checking if activity table already has the unitary VRS column
    if VRS and (not 'VRS' in activity_table.columns):
        activity_table.loc[:, 'VRS'] = 1

    # Asserting shape equality
    assert activity_table.shape == dea_weights.shape, f'''
    Shape mismatch. Activity table of shape {activity_table.shape}
    does not match DEA solutions shape {dea_weights.shape}'''

    # The work of Bana e Costa show that we can plot the frontier graph
    # for an activity table with more than two variables if we normalise
    # the inputs and outputs values by the inputs or outputs weights
    normalization = dea_weights[inputs_list if input_oriented else outputs_list].sum(1)

    # So we can construct a two axis graph where X represents the inputs and Y, the otputs
    graph_inputs = (activity_table * dea_weights)[inputs_list].sum(1) / normalization
    graph_outputs = (activity_table * dea_weights)[outputs_list].sum(1) / normalization

    # This graph is returned as is with solely the inputs and outputs columns
    graph_data = pd.concat([graph_inputs, graph_outputs], axis=1)
    graph_data.columns = ['INPUT', 'OUTPUT']

    return graph_data
