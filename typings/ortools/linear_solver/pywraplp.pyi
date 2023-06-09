"""
This type stub file was generated by pyright.
"""


from typing import Any
from ortools.linear_solver.linear_solver_natural_api import VariableExpr

class Solver:
    r"""
    This mathematical programming (MP) solver class is the main class
    though which users build and solve problems.
    """
    thisown = ...
    CLP_LINEAR_PROGRAMMING = ...
    GLPK_LINEAR_PROGRAMMING = ...
    GLOP_LINEAR_PROGRAMMING = ...
    PDLP_LINEAR_PROGRAMMING = ...
    SCIP_MIXED_INTEGER_PROGRAMMING = ...
    GLPK_MIXED_INTEGER_PROGRAMMING = ...
    CBC_MIXED_INTEGER_PROGRAMMING = ...
    GUROBI_LINEAR_PROGRAMMING = ...
    GUROBI_MIXED_INTEGER_PROGRAMMING = ...
    CPLEX_LINEAR_PROGRAMMING = ...
    CPLEX_MIXED_INTEGER_PROGRAMMING = ...
    XPRESS_LINEAR_PROGRAMMING = ...
    XPRESS_MIXED_INTEGER_PROGRAMMING = ...
    BOP_INTEGER_PROGRAMMING = ...
    SAT_INTEGER_PROGRAMMING = ...

    def __init__(self, name: str, problem_type: str) -> None:
        r""" Create a solver with the given name and underlying solver backend."""
        ...

    __swig_destroy__ = ...

    @staticmethod
    def CreateSolver(solver_id: str) -> 'Solver' | None:
        r"""
        Recommended factory method to create a MPSolver instance, especially in
        non C++ languages.

        It returns a newly created solver instance if successful, or a nullptr
        otherwise. This can occur if the relevant interface is not linked in, or if
        a needed license is not accessible for commercial solvers.

        Ownership of the solver is passed on to the caller of this method.
        It will accept both string names of the OptimizationProblemType enum, as
        well as a short version (i.e. "SCIP_MIXED_INTEGER_PROGRAMMING" or "SCIP").

        solver_id is case insensitive, and the following names are supported:
          - CLP_LINEAR_PROGRAMMING or CLP
          - CBC_MIXED_INTEGER_PROGRAMMING or CBC
          - GLOP_LINEAR_PROGRAMMING or GLOP
          - BOP_INTEGER_PROGRAMMING or BOP
          - SAT_INTEGER_PROGRAMMING or SAT or CP_SAT
          - SCIP_MIXED_INTEGER_PROGRAMMING or SCIP
          - GUROBI_LINEAR_PROGRAMMING or GUROBI_LP
          - GUROBI_MIXED_INTEGER_PROGRAMMING or GUROBI or GUROBI_MIP
          - CPLEX_LINEAR_PROGRAMMING or CPLEX_LP
          - CPLEX_MIXED_INTEGER_PROGRAMMING or CPLEX or CPLEX_MIP
          - XPRESS_LINEAR_PROGRAMMING or XPRESS_LP
          - XPRESS_MIXED_INTEGER_PROGRAMMING or XPRESS or XPRESS_MIP
          - GLPK_LINEAR_PROGRAMMING or GLPK_LP
          - GLPK_MIXED_INTEGER_PROGRAMMING or GLPK or GLPK_MIP
        """
        ...

    @staticmethod
    def SupportsProblemType(problem_type: str) -> bool:
        r"""
        Whether the given problem type is supported (this will depend on the
        targets that you linked).
        """
        ...

    def Clear(self) -> None:
        r"""
        Clears the objective (including the optimization direction), all variables
        and constraints. All the other properties of the MPSolver (like the time
        limit) are kept untouched.
        """
        ...

    def NumVariables(self) -> int:
        r""" Returns the number of variables."""
        ...

    def variables(self) -> list['Variable']:
        r"""
        Returns the array of variables handled by the MPSolver. (They are listed in
        the order in which they were created.)
        """
        ...

    def variable(self, index: int) -> 'Variable':
        r"""Returns the variable at position index."""
        ...

    def LookupVariable(self, var_name: str) -> 'Variable':
        r"""
        Looks up a variable by name, and returns nullptr if it does not exist. The
        first call has a O(n) complexity, as the variable name index is lazily
        created upon first use. Will crash if variable names are not unique.
        """
        ...

    def Var(self, lb: float, ub: float, integer: bool, name: str) -> 'Variable':
        r"""
        Creates a variable with the given bounds, integrality requirement and
        name. Bounds can be finite or +/- MPSolver::infinity(). The MPSolver owns
        the variable (i.e. the returned pointer is borrowed). Variable names are
        optional. If you give an empty name, name() will auto-generate one for you
        upon request.
        """
        ...

    def NumVar(self, lb: float, ub: float, name: str) -> 'Variable':
        r""" Creates a continuous variable."""
        ...

    def IntVar(self, lb: float, ub: float, name: str) -> 'Variable':
        r""" Creates an integer variable."""
        ...

    def BoolVar(self, name: str) -> 'Variable':
        r""" Creates a boolean variable."""
        ...

    def NumConstraints(self) -> int:
        r""" Returns the number of constraints."""
        ...

    def constraints(self) -> list['Constraint']:
        r"""
        Returns the array of constraints handled by the MPSolver.

        They are listed in the order in which they were created.
        """
        ...

    def constraint(self, index: int) -> 'Constraint':
        r""" Returns the constraint at the given index."""
        ...

    def LookupConstraint(self, constraint_name: str) -> 'Constraint':
        r"""
         Looks up a constraint by name, and returns nullptr if it does not exist.

        The first call has a O(n) complexity, as the constraint name index is
        lazily created upon first use. Will crash if constraint names are not
        unique.
        """
        ...

    def Constraint(self, *args) -> 'Constraint':
        r"""
        *Overload 1:*

        Creates a linear constraint with given bounds.

        Bounds can be finite or +/- MPSolver::infinity(). The MPSolver class
        assumes ownership of the constraint.

        :rtype: :py:class:`MPConstraint`
        :return: a pointer to the newly created constraint.

        |

        *Overload 2:*
         Creates a constraint with -infinity and +infinity bounds.

        |

        *Overload 3:*
         Creates a named constraint with given bounds.

        |

        *Overload 4:*
         Creates a named constraint with -infinity and +infinity bounds.
        """
        ...

    def Objective(self) -> 'Objective':
        r""" Returns the mutable objective object."""
        ...

    OPTIMAL = ...
    FEASIBLE = ...
    INFEASIBLE = ...
    UNBOUNDED = ...
    ABNORMAL = ...
    MODEL_INVALID = ...
    NOT_SOLVED = ...

    def Solve(self, *args: Any) -> Any:
        r"""
        *Overload 1:*
        Solves the problem using the default parameter values.

        |

        *Overload 2:*
        Solves the problem using the specified parameter values.
        """
        ...

    def ComputeConstraintActivities(self) -> list[float]:
        r"""
        Advanced usage: compute the "activities" of all constraints, which are the
        sums of their linear terms. The activities are returned in the same order
        as constraints(), which is the order in which constraints were added; but
        you can also use MPConstraint::index() to get a constraint's index.
        """
        ...

    def VerifySolution(self, tolerance: float, log_errors: bool) -> bool:
        r"""
        Advanced usage: Verifies the *correctness* of the solution.

        It verifies that all variables must be within their domains, all
        constraints must be satisfied, and the reported objective value must be
        accurate.

        Usage:
        - This can only be called after Solve() was called.
        - "tolerance" is interpreted as an absolute error threshold.
        - For the objective value only, if the absolute error is too large,
          the tolerance is interpreted as a relative error threshold instead.
        - If "log_errors" is true, every single violation will be logged.
        - If "tolerance" is negative, it will be set to infinity().

        Most users should just set the --verify_solution flag and not bother using
        this method directly.
        """
        ...

    def InterruptSolve(self) -> bool:
        r"""
         Interrupts the Solve() execution to terminate processing if possible.

        If the underlying interface supports interruption; it does that and returns
        true regardless of whether there's an ongoing Solve() or not. The Solve()
        call may still linger for a while depending on the conditions.  If
        interruption is not supported; returns false and does nothing.
        MPSolver::SolverTypeSupportsInterruption can be used to check if
        interruption is supported for a given solver type.
        """
        ...

    def FillSolutionResponseProto(self, response: "operations_research::MPSolutionResponse *") -> None:
        r""" Encodes the current solution in a solution response protocol buffer."""
        ...

    @staticmethod
    def SolveWithProto(model_request: "operations_research::MPModelRequest const &", response: "operations_research::MPSolutionResponse *", interrupt: "std::atomic< bool > *" = ...) -> "operations_research::MPSolutionResponse *":
        r"""
        Solves the model encoded by a MPModelRequest protocol buffer and fills the
        solution encoded as a MPSolutionResponse. The solve is stopped prematurely
        if interrupt is non-null at set to true during (or before) solving.
        Interruption is only supported if SolverTypeSupportsInterruption() returns
        true for the requested solver. Passing a non-null interruption with any
        other solver type immediately returns an MPSOLVER_INCOMPATIBLE_OPTIONS
        error.

        Note(user): This attempts to first use `DirectlySolveProto()` (if
        implemented). Consequently, this most likely does *not* override any of
        the default parameters of the underlying solver. This behavior *differs*
        from `MPSolver::Solve()` which by default sets the feasibility tolerance
        and the gap limit (as of 2020/02/11, to 1e-7 and 0.0001, respectively).
        """
        ...

    def ExportModelToProto(self, output_model: "operations_research::MPModelProto *") -> None:
        r""" Exports model to protocol buffer."""
        ...

    def SetSolverSpecificParametersAsString(self, parameters: str) -> bool:
        r"""
        Advanced usage: pass solver specific parameters in text format.

        The format is solver-specific and is the same as the corresponding solver
        configuration file format. Returns true if the operation was successful.
        """
        ...

    FREE = ...
    AT_LOWER_BOUND = ...
    AT_UPPER_BOUND = ...
    FIXED_VALUE = ...
    BASIC = ...

    @staticmethod
    def infinity() -> float:
        r"""
        Infinity.

        You can use -MPSolver::infinity() for negative infinity.
        """
        ...

    def EnableOutput(self) -> None:
        r""" Enables solver logging."""
        ...

    def SuppressOutput(self) -> None:
        r""" Suppresses solver logging."""
        ...

    def iterations(self) -> int:
        r""" Returns the number of simplex iterations."""
        ...

    def nodes(self) -> int:
        r"""
        Returns the number of branch-and-bound nodes evaluated during the solve.

        Only available for discrete problems.
        """
        ...

    def ComputeExactConditionNumber(self) -> float:
        r"""
         Advanced usage: computes the exact condition number of the current scaled
        basis: L1norm(B) * L1norm(inverse(B)), where B is the scaled basis.

        This method requires that a basis exists: it should be called after Solve.
        It is only available for continuous problems. It is implemented for GLPK
        but not CLP because CLP does not provide the API for doing it.

        The condition number measures how well the constraint matrix is conditioned
        and can be used to predict whether numerical issues will arise during the
        solve: the model is declared infeasible whereas it is feasible (or
        vice-versa), the solution obtained is not optimal or violates some
        constraints, the resolution is slow because of repeated singularities.

        The rule of thumb to interpret the condition number kappa is:
          - o kappa <= 1e7: virtually no chance of numerical issues
          - o 1e7 < kappa <= 1e10: small chance of numerical issues
          - o 1e10 < kappa <= 1e13: medium chance of numerical issues
          - o kappa > 1e13: high chance of numerical issues

        The computation of the condition number depends on the quality of the LU
        decomposition, so it is not very accurate when the matrix is ill
        conditioned.
        """
        ...

    def NextSolution(self) -> bool:
        r"""
        Some solvers (MIP only, not LP) can produce multiple solutions to the
        problem. Returns true when another solution is available, and updates the
        'Variable'* objects to make the new solution queryable. Call only after
        calling solve.

        The optimality properties of the additional solutions found, and whether or
        not the solver computes them ahead of time or when NextSolution() is called
        is solver specific.

        As of 2020-02-10, only Gurobi and SCIP support NextSolution(), see
        linear_solver_interfaces_test for an example of how to configure these
        solvers for multiple solutions. Other solvers return false unconditionally.
        """
        ...

    def set_time_limit(self, time_limit_milliseconds: int) -> None:
        ...

    def wall_time(self) -> int:
        ...

    def LoadModelFromProto(self, input_model: "operations_research::MPModelProto const &") -> str:
        ...

    def LoadModelFromProtoWithUniqueNamesOrDie(self, input_model: "operations_research::MPModelProto const &") -> str:
        ...

    def LoadSolutionFromProto(self, *args) -> bool:
        ...

    def ExportModelAsLpFormat(self, obfuscated: bool) -> str:
        ...

    def ExportModelAsMpsFormat(self, fixed_format: bool, obfuscated: bool) -> str:
        ...

    def SetHint(self, variables: "std::vector< operations_research::'Variable' * > const &", values: "std::vector< float > const &") -> None:
        r"""
        Set a hint for solution.

        If a feasible or almost-feasible solution to the problem is already known,
        it may be helpful to pass it to the solver so that it can be used. A
        solver that supports this feature will try to use this information to
        create its initial feasible solution.

        Note that it may not always be faster to give a hint like this to the
        solver. There is also no guarantee that the solver will use this hint or
        try to return a solution "close" to this assignment in case of multiple
        optimal solutions.
        """
        ...

    def SetNumThreads(self, num_theads: int) -> bool:
        r""" Sets the number of threads to be used by the solver."""
        ...

    def Add(self, constraint: 'VariableExpr' | bool, name: str = ...) -> None:
        ...

    def Sum(self, expr_array):  # -> SumArray:
        ...

    def RowConstraint(self, *args):
        ...

    def Minimize(self, expr):  # -> None:
        ...

    def Maximize(self, expr):  # -> None:
        ...

    @staticmethod
    def Infinity() -> float:
        ...

    def SetTimeLimit(self, x: int) -> None:
        ...

    def WallTime(self) -> int:
        ...

    def Iterations(self) -> int:
        ...


def Solver_CreateSolver(solver_id: str) -> "operations_research::MPSolver *":
    r"""
    Recommended factory method to create a MPSolver instance, especially in
    non C++ languages.

    It returns a newly created solver instance if successful, or a nullptr
    otherwise. This can occur if the relevant interface is not linked in, or if
    a needed license is not accessible for commercial solvers.

    Ownership of the solver is passed on to the caller of this method.
    It will accept both string names of the OptimizationProblemType enum, as
    well as a short version (i.e. "SCIP_MIXED_INTEGER_PROGRAMMING" or "SCIP").

    solver_id is case insensitive, and the following names are supported:
      - CLP_LINEAR_PROGRAMMING or CLP
      - CBC_MIXED_INTEGER_PROGRAMMING or CBC
      - GLOP_LINEAR_PROGRAMMING or GLOP
      - BOP_INTEGER_PROGRAMMING or BOP
      - SAT_INTEGER_PROGRAMMING or SAT or CP_SAT
      - SCIP_MIXED_INTEGER_PROGRAMMING or SCIP
      - GUROBI_LINEAR_PROGRAMMING or GUROBI_LP
      - GUROBI_MIXED_INTEGER_PROGRAMMING or GUROBI or GUROBI_MIP
      - CPLEX_LINEAR_PROGRAMMING or CPLEX_LP
      - CPLEX_MIXED_INTEGER_PROGRAMMING or CPLEX or CPLEX_MIP
      - XPRESS_LINEAR_PROGRAMMING or XPRESS_LP
      - XPRESS_MIXED_INTEGER_PROGRAMMING or XPRESS or XPRESS_MIP
      - GLPK_LINEAR_PROGRAMMING or GLPK_LP
      - GLPK_MIXED_INTEGER_PROGRAMMING or GLPK or GLPK_MIP
    """
    ...


def Solver_SupportsProblemType(problem_type: str) -> bool:
    r"""
    Whether the given problem type is supported (this will depend on the
    targets that you linked).
    """
    ...


def Solver_SolveWithProto(model_request: "operations_research::MPModelRequest const &", response: "operations_research::MPSolutionResponse *", interrupt: "std::atomic< bool > *" = ...) -> "operations_research::MPSolutionResponse *":
    r"""
    Solves the model encoded by a MPModelRequest protocol buffer and fills the
    solution encoded as a MPSolutionResponse. The solve is stopped prematurely
    if interrupt is non-null at set to true during (or before) solving.
    Interruption is only supported if SolverTypeSupportsInterruption() returns
    true for the requested solver. Passing a non-null interruption with any
    other solver type immediately returns an MPSOLVER_INCOMPATIBLE_OPTIONS
    error.

    Note(user): This attempts to first use `DirectlySolveProto()` (if
    implemented). Consequently, this most likely does *not* override any of
    the default parameters of the underlying solver. This behavior *differs*
    from `MPSolver::Solve()` which by default sets the feasibility tolerance
    and the gap limit (as of 2020/02/11, to 1e-7 and 0.0001, respectively).
    """
    ...


def Solver_infinity() -> float:
    r"""
    Infinity.

    You can use -MPSolver::infinity() for negative infinity.
    """
    ...


def Solver_Infinity() -> float:
    ...


class Objective:
    r""" A class to express a linear objective."""
    thisown = ...

    def Clear(self) -> None:
        r"""
         Clears the offset, all variables and coefficients, and the optimization
        direction.
        """
        ...

    def SetCoefficient(self, var: 'Variable', coeff: float) -> None:
        r"""
        Sets the coefficient of the variable in the objective.

        If the variable does not belong to the solver, the function just returns,
        or crashes in non-opt mode.
        """
        ...

    def GetCoefficient(self, var: 'Variable') -> float:
        r"""
         Gets the coefficient of a given variable in the objective

        It returns 0 if the variable does not appear in the objective).
        """
        ...

    def SetOffset(self, value: float) -> None:
        r""" Sets the constant term in the objective."""
        ...

    def offset(self) -> float:
        r""" Gets the constant term in the objective."""
        ...

    def SetOptimizationDirection(self, maximize: bool) -> None:
        r""" Sets the optimization direction (maximize: true or minimize: false)."""
        ...

    def SetMinimization(self) -> None:
        r""" Sets the optimization direction to minimize."""
        ...

    def SetMaximization(self) -> None:
        r""" Sets the optimization direction to maximize."""
        ...

    def maximization(self) -> bool:
        r""" Is the optimization direction set to maximize?"""
        ...

    def minimization(self) -> bool:
        r""" Is the optimization direction set to minimize?"""
        ...

    def Value(self) -> float:
        r"""
        Returns the objective value of the best solution found so far.

        It is the optimal objective value if the problem has been solved to
        optimality.

        Note: the objective value may be slightly different than what you could
        compute yourself using ``'Variable'::solution_value();`` please use the
        --verify_solution flag to gain confidence about the numerical stability of
        your solution.
        """
        ...

    def BestBound(self) -> float:
        r"""
        Returns the best objective bound.

        In case of minimization, it is a lower bound on the objective value of the
        optimal integer solution. Only available for discrete problems.
        """
        ...

    def Offset(self) -> float:
        ...

    __swig_destroy__ = ...


class Variable:
    r""" The class for variables of a Mathematical Programming (MP) model."""
    thisown = ...

    def name(self) -> str:
        r""" Returns the name of the variable."""
        ...

    def SetInteger(self, integer: bool) -> None:
        r""" Sets the integrality requirement of the variable."""
        ...

    def integer(self) -> bool:
        r""" Returns the integrality requirement of the variable."""
        ...

    def solution_value(self) -> float:
        r"""
        Returns the value of the variable in the current solution.

        If the variable is integer, then the value will always be an integer (the
        underlying solver handles floating-point values only, but this function
        automatically rounds it to the nearest integer; see: man 3 round).
        """
        ...

    def index(self) -> int:
        r""" Returns the index of the variable in the MPSolver::variables_."""
        ...

    def lb(self) -> float:
        r""" Returns the lower bound."""
        ...

    def ub(self) -> float:
        r""" Returns the upper bound."""
        ...

    def SetBounds(self, lb: float, ub: float) -> None:
        r""" Sets both the lower and upper bounds."""
        ...

    def reduced_cost(self) -> float:
        r"""
        Advanced usage: returns the reduced cost of the variable in the current
        solution (only available for continuous problems).
        """
        ...

    def basis_status(self) -> Any:
        r"""
        Advanced usage: returns the basis status of the variable in the current
        solution (only available for continuous problems).

        See also: MPSolver::BasisStatus.
        """
        ...

    def branching_priority(self) -> int:
        r"""
        Advanced usage: Certain MIP solvers (e.g. Gurobi or SCIP) allow you to set
        a per-variable priority for determining which variable to branch on.

        A value of 0 is treated as default, and is equivalent to not setting the
        branching priority. The solver looks first to branch on fractional
        variables in higher priority levels. As of 2019-05, only Gurobi and SCIP
        support setting branching priority; all other solvers will simply ignore
        this annotation.
        """
        ...

    def SetBranchingPriority(self, priority: int) -> None:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def SolutionValue(self) -> float:
        ...

    def Integer(self) -> bool:
        ...

    def Lb(self) -> float:
        ...

    def Ub(self) -> float:
        ...

    def SetLb(self, x: float) -> None:
        ...

    def SetUb(self, x: float) -> None:
        ...

    def ReducedCost(self) -> float:
        ...

    def __add__(self, other: Any) -> VariableExpr: ...
    def __radd__(self, other: Any) -> VariableExpr: ...
    def __sub__(self, other: Any) -> VariableExpr: ...
    def __mul__(self, other: Any) -> VariableExpr: ...
    def __floordiv__(self, other: Any) -> VariableExpr: ...
    def __truediv__(self, other: Any) -> VariableExpr: ...
    def __rshift__(self, other: Any) -> VariableExpr: ...
    def __lshift__(self, other: Any) -> VariableExpr: ...
    def __and__(self, other: Any) -> VariableExpr: ...
    def __or__(self, other: Any) -> VariableExpr: ...
    def __xor__(self, other: Any) -> VariableExpr: ...
    def __eq__(self, other: Any) -> VariableExpr: ...
    def __lt__(self, other: Any) -> VariableExpr: ...
    def __gt__(self, other: Any) -> VariableExpr: ...
    def __le__(self, other: Any) -> VariableExpr: ...
    def __ge__(self, other: Any) -> VariableExpr: ...
    def __ne__(self, other: Any) -> VariableExpr: ...
    def __isub__(self, other: Any) -> VariableExpr: ...
    def __iadd__(self, other: Any) -> VariableExpr: ...
    def __imul__(self, other: Any) -> VariableExpr: ...
    def __idiv__(self, other: Any) -> VariableExpr: ...
    def __ifloordiv__(self, other: Any) -> VariableExpr: ...
    def __imod__(self, other: Any) -> VariableExpr: ...
    def __ipow__(self, other: Any) -> VariableExpr: ...
    def __irshift__(self, other: Any) -> VariableExpr: ...
    def __ilshift__(self, other: Any) -> VariableExpr: ...
    def __iand__(self, other: Any) -> VariableExpr: ...
    def __ior__(self, other: Any) -> VariableExpr: ...
    def __ixor__(self, other: Any) -> VariableExpr: ...
    def __neg__(self) -> VariableExpr: ...
    def __pos__(self) -> VariableExpr: ...
    def __invert__(self) -> VariableExpr: ...
    def __int__(self) -> VariableExpr: ...
    def Solution_Value(self) -> float: ...

    __swig_destroy__ = ...


class Constraint:
    r"""
    The class for constraints of a Mathematical Programming (MP) model.

    A constraint is represented as a linear equation or inequality.
    """
    thisown = ...

    def __init__(self, *args, **kwargs) -> None:
        ...

    __repr__ = ...

    def name(self) -> str:
        r""" Returns the name of the constraint."""
        ...

    def Clear(self) -> None:
        r""" Clears all variables and coefficients. Does not clear the bounds."""
        ...

    def SetCoefficient(self, var: Variable, coeff: float) -> None:
        r"""
        Sets the coefficient of the variable on the constraint.

        If the variable does not belong to the solver, the function just returns,
        or crashes in non-opt mode.
        """
        ...

    def GetCoefficient(self, var: Variable) -> float:
        r"""
        Gets the coefficient of a given variable on the constraint (which is 0 if
        the variable does not appear in the constraint).
        """
        ...

    def lb(self) -> float:
        r""" Returns the lower bound."""
        ...

    def ub(self) -> float:
        r""" Returns the upper bound."""
        ...

    def SetBounds(self, lb: float, ub: float) -> None:
        r""" Sets both the lower and upper bounds."""
        ...

    def set_is_lazy(self, laziness: bool) -> None:
        r"""
        Advanced usage: sets the constraint "laziness".

        **This is only supported for SCIP and has no effect on other
        solvers.**

        When **laziness** is true, the constraint is only considered by the Linear
        Programming solver if its current solution violates the constraint. In this
        case, the constraint is definitively added to the problem. This may be
        useful in some MIP problems, and may have a dramatic impact on performance.

        For more info see: http://tinyurl.com/lazy-constraints.
        """
        ...

    def index(self) -> int:
        r""" Returns the index of the constraint in the MPSolver::constraints_."""
        ...

    def dual_value(self) -> float:
        r"""
        Advanced usage: returns the dual value of the constraint in the current
        solution (only available for continuous problems).
        """
        ...

    def basis_status(self) -> "operations_research::MPSolver::BasisStatus":
        r"""
        Advanced usage: returns the basis status of the constraint.

        It is only available for continuous problems).

        Note that if a constraint "linear_expression in [lb, ub]" is transformed
        into "linear_expression + slack = 0" with slack in [-ub, -lb], then this
        status is the same as the status of the slack variable with AT_UPPER_BOUND
        and AT_LOWER_BOUND swapped.

        See also: MPSolver::BasisStatus.
        """
        ...

    def Lb(self) -> float:
        ...

    def Ub(self) -> float:
        ...

    def SetLb(self, x: float) -> None:
        ...

    def SetUb(self, x: float) -> None:
        ...

    def DualValue(self) -> float:
        ...

    __swig_destroy__ = ...


class MPSolverParameters:
    r"""
    This class stores parameter settings for LP and MIP solvers. Some parameters
    are marked as advanced: do not change their values unless you know what you
    are doing!

    For developers: how to add a new parameter:
    - Add the new Foo parameter in the floatParam or IntegerParam enum.
    - If it is a categorical param, add a FooValues enum.
    - Decide if the wrapper should define a default value for it: yes
      if it controls the properties of the solution (example:
      tolerances) or if it consistently improves performance, no
      otherwise. If yes, define kDefaultFoo.
    - Add a foo_value_ member and, if no default value is defined, a
      foo_is_default_ member.
    - Add code to handle Foo in Set...Param, Reset...Param,
      Get...Param, Reset and the constructor.
    - In class MPSolverInterface, add a virtual method SetFoo, add it
      to SetCommonParameters or SetMIPParameters, and implement it for
      each solver. Sometimes, parameters need to be implemented
      differently, see for example the INCREMENTALITY implementation.
    - Add a test in linear_solver_test.cc.

    TODO(user): store the parameter values in a protocol buffer
    instead. We need to figure out how to deal with the subtleties of
    the default values.
    """
    thisown = ...
    __repr__ = ...
    RELATIVE_MIP_GAP = ...
    PRIMAL_TOLERANCE = ...
    DUAL_TOLERANCE = ...
    PRESOLVE = ...
    LP_ALGORITHM = ...
    INCREMENTALITY = ...
    SCALING = ...
    PRESOLVE_OFF = ...
    PRESOLVE_ON = ...
    DUAL = ...
    PRIMAL = ...
    BARRIER = ...
    INCREMENTALITY_OFF = ...
    INCREMENTALITY_ON = ...
    SCALING_OFF = ...
    SCALING_ON = ...

    def __init__(self) -> None:
        r""" The constructor sets all parameters to their default value."""
        ...

    def SetfloatParam(self, param: "operations_research::MPSolverParameters::floatParam", value: float) -> None:
        r""" Sets a float parameter to a specific value."""
        ...

    def SetIntegerParam(self, param: "operations_research::MPSolverParameters::IntegerParam", value: int) -> None:
        r""" Sets a integer parameter to a specific value."""
        ...

    def GetfloatParam(self, param: "operations_research::MPSolverParameters::floatParam") -> float:
        r""" Returns the value of a float parameter."""
        ...

    def GetIntegerParam(self, param: "operations_research::MPSolverParameters::IntegerParam") -> int:
        r""" Returns the value of an integer parameter."""
        ...

    __swig_destroy__ = ...


cvar = ...


class ModelExportOptions:
    r""" Export options."""
    thisown = ...
    __repr__ = ...

    def __init__(self) -> None:
        ...

    __swig_destroy__ = ...


def ExportModelAsLpFormat(*args) -> str:
    ...


def ExportModelAsMpsFormat(*args) -> str:
    ...


def FindErrorInModelProto(input_model: "operations_research::MPModelProto const &") -> str:
    ...


def setup_variable_operator(opname):  # -> None:
    ...
