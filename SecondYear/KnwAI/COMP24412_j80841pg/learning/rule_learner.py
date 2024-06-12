import itertools
import re
from contextlib import contextmanager
from dataclasses import dataclass, field, astuple
from typing import List, Generator, Union

from pyswip import Prolog

from learning.util import Algorithm, Examples, Dataset, Example, AlgorithmRegistry

from logging import getLogger

logger = getLogger(__name__)


@dataclass(frozen=True)
class Predicate:
    """
    Object representation of a predicate. Contains `name` which is the name of the predicate and its `arity`.
    """
    name: str
    arity: int

    def __post_init__(self):
        assert self.name[0].islower()


@dataclass(frozen=True)
class Expression:
    """
    Abstract base class representing a valid logical statement.
    """
    ...


@dataclass(frozen=True)
class Literal(Expression):
    """
    Literal: A Predicate with instantiated values for its arguments, which can be either variables or atomic values.

    Converting the literal to string will yield its syntactically valid prolog representation.
    """
    predicate: Predicate = field(hash=True)
    arguments: List[Union['Expression', str]] = field(hash=True)

    def __post_init__(self):
        """
        Make sure that the number of arguments corresponds to the predicate's arity.

        """
        assert (len(self.arguments) == self.predicate.arity,
                f"Number of arguments {len(self.arguments)} not "
                f"equal to the arity of the predicate {self.predicate.arity}")

    def __repr__(self):
        """
        Prolog representation.

        Returns: A syntactically valid prolog representation of the literal.

        """
        return f"{self.predicate.name}({','.join(str(a) for a in self.arguments)})"

    @classmethod
    def from_str(cls, string):
        """
        Generates a python object from a syntactically valid prolog representation.
        Args:
            string: Prolog representation of the literal.

        Returns: `Literal` object equivalent to the prolog representation.

        """
        predicate = get_predicate(string)
        args = get_args(string)
        return Literal(predicate, args)


def get_predicate(text: str) -> Predicate:
    """
    Returns the name and arity of a predicate from a syntactically valid prolog representation.
    Args:
        text: Text to extract the predicate from.

    Returns: Object of `Predicate` class with its corresponding name and arity.

    """
    text = str(text)
    name = text[:text.find("(")].strip()
    arity = len(re.findall("Variable", text))
    if arity == 0:
        arity = len(re.findall(",", text)) + 1
    return Predicate(name, arity)


@dataclass(frozen=True)
class Disjunction(Expression):
    """
    Represents a disjunction of horn clauses which is initially empty.
    """
    expressions: List['HornClause'] = field(default_factory=list)

    def generalize(self, expression: 'HornClause'):
        """
        Adds another horn clause to the disjunction.
        Args:
            expression: Horn clause to add

        """
        self.expressions.append(expression)

    def __repr__(self):
        """
        Returns a syntactically valid prolog representation of the horn clauses.

        Since there is no real disjunction in prolog, this is just a set of the expressions as separate statements.
        Returns:
            syntactically valid prolog representation of the contained horn clauses.

        """
        return " .\n".join(repr(e) for e in self.expressions) + ' .'


@dataclass(frozen=True)
class Conjunction(Expression):
    """
    Represents a conjunction of literals which is initially empty.
    """
    expressions: List[Expression] = field(default_factory=list)

    def specialize(self, expression: Expression):
        """
        Adds another literal to the conjunction.
        Args:
            expression: literal to add

        """
        self.expressions.append(expression)

    def __repr__(self):
        """
        Returns a syntactically valid prolog representation of the conjunction of the literals.

        Returns:
            syntactically valid prolog representation of the conjunction (comma-separated).

        """
        return " , ".join(repr(e) for e in self.expressions)


@dataclass(frozen=True)
class HornClause(Expression):
    """
    Represents a horn clause with a literal as `head` and a conjunction as `body`.
    """
    head: Expression
    body: Conjunction = field(default_factory=lambda: Conjunction())

    def get_vars(self):
        """
        Returns all variables appearing in the horn clause.

        Returns: All variables in the horn clause, according to prolog syntax, where variables are capitalised.

        """
        return re.findall(r"(?:[^\w])([A-Z]\w*)", str(self))

    def __repr__(self):
        """
        Converts to a syntactically valid prolog representation.

        Returns:
            Syntactically valid prolog representation of a horn clause in the form of
            ``head :- literal_1 , literal_2 , ... , literal_n``
            for all literals in the body.
        """
        return f"{str(self.head)} :- {' , '.join(str(e) for e in self.body.expressions)}"


def get_args(text: str) -> List[str]:
    """
    Returns the arguments of a text that is assumed to be a single literal in prolog representation.

    Args:
        text: Text to extract the arguments from. Must be valid prolog representation of a single literal.

    Returns:
        All arguments that appear in that literal.

    """
    return [x.strip() for x in re.findall(r"\(.*\)", str(text))[0][1:-1].split(",")]


@AlgorithmRegistry.register('foil')
@contextmanager
def FOIL(dataset: Dataset, recursive=False):
    f = _FOIL(dataset, recursive)
    try:
        yield f
    finally:
        f.abolish()


class _FOIL(Algorithm):
    prolog: Prolog

    def __init__(self, dataset: Dataset, recursive=False):
        super().__init__(dataset)
        logger.info("Creating prolog...")
        self.prolog = Prolog()
        self.i = 0
        self.recursive = recursive

        if dataset.kb:
            logger.debug(f"Consulting {self.dataset.kb}")
            self.prolog.consult(self.dataset.kb)

    def abolish(self):
        for p, a in (astuple(a) for a in self.get_predicates()):
            self.prolog.query(f"abolish({p}/{a})")

    def predict(self, example: Example) -> bool:
        return any(self.covers(clause=c, example=example) for c in self.hypothesis.expressions)
        
        
    def get_predicates(self) -> List[Predicate]:
        """
        This method returns all (relevant) predicates from the knowledge base.

        Returns:
            all currently known predicates in the knowledge base that was loaded from the file corresponding to the
            dataset.

        """
        file = open(self.dataset.kb, "r+")
        lines = []
        for line in file:
            # Remove the newline character at the end of the line
            line = line.strip()
            # Append the line to the list
            lines.append(line)

        predicates = []
        for x in lines:
            if x:
                predicates.append(get_predicate(x))
        predicates = list(set(predicates))
        file.close()
        return predicates


    def find_hypothesis(self) -> Disjunction:
        """
        Initiates the FOIL algorithm and returns the final disjunction from the list that is returned by
        `FOIL.foil`.

        Returns: Disjunction of horn clauses that represent the learned target relation.

        """
        positive_examples = self.dataset.positive_examples
        negative_examples = self.dataset.negative_examples

        target = Literal.from_str(self.dataset.target)

        predicates = self.get_predicates()
        assert predicates

        clauses = self.foil(positive_examples, negative_examples, predicates, target)
        return Disjunction(clauses)

    def foil(self, positive_examples: Examples, negative_examples: Examples, predicates: List[Predicate],
             target: Literal) -> List[HornClause]:
        """
        Learns a list of horn clauses from a set of positive and negative examples which as a disjunction
        represent the hypothesis inferred from the dataset.

        This method is the outer loop of the foil algorithm.

        Args:
            positive_examples: Positive examples for the target relation to be learned.
            negative_examples: Negative examples for the target relation to be learned.
            predicates: Predicates that are allowed in the bodies of the horn clauses.
            target: Signature of the target relation to be learned

        Returns:
            A list of horn clauses that as a disjunction cover all positive and none of the negative examples.

        """
        self.prolog.consult(self.dataset.kb)
        clauses = list()
        pos_ex = positive_examples
        neg_ex = negative_examples
        # print("Start:", pos_ex)
        while pos_ex:
            clause = self.new_clause(pos_ex, neg_ex, predicates, target)
            for e in pos_ex:
                bool = self.covers(clause, e)
                # print(clause)
                # print(bool)
                if not bool:
                    pos_ex.remove(e)
            # print("Change:", pos_ex)
            clauses.append(clause)
            break
        # print(clauses)
        return clauses

    def covers(self, clause: HornClause, example: Example) -> bool:
        """
        This method checks whether an example is covered by a given horn clause under the current knowledge base.
        Args:
            clause: The clause to check whether it covers the examples.
            example: The examples to check whether it is covered by the clause.

        Returns:
            True if covered, False otherwise

        """
        # print(clause)
        # print(list(self.prolog.query(str(clause.body))))
        if example in list(self.prolog.query(str(clause.body))):
            var = True
        else:
            var = False
        return var

    def new_clause(self, positive_examples: Examples, negative_examples: Examples, predicates: List[Predicate],
                   target: Literal) -> HornClause:
        """
        This method generates a new horn clause from a dataset of positive and negative examples, a target and a
        list of allowed predicates to be used in the horn clause body.

        This corresponds to the inner loop of the foil algorithm.

        Args:
            positive_examples: Positive examples of the dataset to learn the clause from.
            negative_examples: Negative examples of the dataset to learn the clause from.
            predicates: List of predicates that can be used in the clause body.
            target: Head of the clause to learn.

        Returns:
            A horn clause that covers some part of the positive examples and does not contradict any of the
            negative examples.

        """
        self.prolog.consult(self.dataset.kb)
        neg_ex = negative_examples
        pos_ex = positive_examples
        # print(pos_ex)
        clause = HornClause(target, Conjunction())
        # print("BBBB", clause)
        while neg_ex:
            candidates = self.generate_candidates(clause, predicates)
            best_literal = None
            best_gain = float('-inf')
            for lit in candidates:
                # print(lit)
                gain = self.foil_information_gain(lit, pos_ex, neg_ex)
                if gain > best_gain:
                    best_gain = gain
                    best_literal = lit
                # print(gain)
                print(best_literal)
            clause.body.specialize(best_literal)
            #print(clause)
            for x in self.prolog.query(str(best_literal)):
                for key_x, val_x in x.items():
                    pos_ex = [d for d in positive_examples if d.get(key_x) == val_x]
                    neg_ex = [d for d in negative_examples if d.get(key_x) == val_x]
        #print(clause)
        return clause

    def get_next_literal(self, candidates: List[Expression], pos_ex: Examples, neg_ex: Examples) -> Expression:
        """
        Returns the next literal with the highest information gain as computed from a given dataset of positive and
        negative examples.
        Args:
            candidates: Candidates to choose the one with the highest information gain from.
            pos_ex: Positive examples of the dataset to infer the information gain from.
            neg_ex: Negative examples of the dataset to infer the information gain from.

        Returns:
            the next literal with the highest information gain as computed
            from a given dataset of positive and negative examples.

        """

    def foil_information_gain(self, candidate: Expression, pos_ex: Examples, neg_ex: Examples) -> float:
        """
        This method calculates the information gain (as presented in the lecture) of an expression according
           to given positive and negative examples observations.

        Args:
               candidate: Attribute to infer the information gain for.
               pos_ex: Positive examples to infer the information gain from.
               neg_ex: Negative examples to infer the information gain from.

        Returns: The information gain of the given attribute according to the given observations.

        """
        from math import log2
        #print(pos_ex)
        #print(neg_ex)
        ex_pos_new = []
        ex_neg_new = []
        for ex in pos_ex:
            list = self.extend_example(ex, candidate)
            ex_pos_new += list
        for ex in neg_ex:
            list = self.extend_example(ex, candidate)
            ex_neg_new += list
        # print(ex_pos_new)
        # print(ex_neg_new)
        t = 0
        for ex in pos_ex:
            if is_represented_by(ex, ex_pos_new):
                t += 1
        #print(t)
        if len(ex_pos_new) != 0:
            ig = t * (log2(len(ex_pos_new) / (len(ex_pos_new) + len(ex_neg_new))) - log2(len(pos_ex)/(len(pos_ex) + len(neg_ex))))
        else:
            ig = t * (0 - log2(len(pos_ex)/(len(pos_ex) + len(neg_ex))))
        
        #print(ig)
        return ig
        

    def generate_candidates(self, clause: HornClause, predicates: List[Predicate]) -> Generator[Expression, None, None]:
        """
        This method generates all reasonable (as discussed in the lecture) specialisations of a horn clause
        given a list of allowed predicates.

        Args:
            clause: The clause to calculate possible specialisations for.
            predicates: Allowed predicate vocabulary to specialise the clause.

        Returns:
            All expressions that could be a reasonable specialisation of `clause`.

        """
        import itertools

        list_to_return = []
        for pred in predicates:

            variables = clause.get_vars()
            for i in range(pred.arity-1):
                variables.append(self.unique_var())
                
            vars_permutations = list(itertools.product(variables, repeat=pred.arity))
            #print(vars_permutations)

            for comb in vars_permutations:
                if any(item in clause.get_vars() for item in list(comb)):
                    literal = Literal(pred, list(comb))
                    list_to_return.append(literal)              
        
        #print(list_to_return)

        return list_to_return

    def extend_example(self, example: Example, new_expr: Expression) -> Generator[Example, None, None]:
        """
        This method extends an example with all possible substitutions subject to a given expression and the current
        knowledge base.
        Args:
            example: Example to extend.
            new_expr: Expression to extend the example with.

        Returns:
            A generator that yields all possible substitutions for a given example an an expression.

        """
        return_list = []
        for x in self.prolog.query(str(new_expr)):
            for key, value in example.items():
                if key not in x.keys():
                    x[key] = value
            # print(x)
            if all(item in x.items() for item in example.items()):
                return_list.append(x)
        # print(return_list)
        return return_list
    
    def unique_var(self) -> str:
        """
        Returns the next uniquely numbered variable to be used.

        Returns:
            the next uniquely named variable in the following format: `V_i` where `i` is a number.

        """
        var =  "V_" + str(self.i)
        self.i += 1
        return var
     


def is_represented_by(example: Example, examples: Examples) -> bool:
    """
    Checks whether a given example is represented by a list of examples.
    Args:
        example: Example to check whether it's represented.
        examples: Examples to check whether they represent the example.

    Returns:
        True, if for some `e` in `examples` for all variables (keys except target) in `example`,
        the values are equal (potential additional variables in `e` do not need to be considered). False otherwise.

    """
    # print(example)
    # print(examples)
    # print(all(item in ex.items() for ex in examples for item in example.items()))
    for dict_item in examples:
        if all(item in dict_item.items() for item in example.items()):
            return True
    return False
    
