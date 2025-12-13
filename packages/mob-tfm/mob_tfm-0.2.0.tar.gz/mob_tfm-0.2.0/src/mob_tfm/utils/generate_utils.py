import ast,sys
from dataclasses import dataclass
from typing import Callable, TypeAlias
from mob_tfm.exceptions import *
from mob_tfm.utils.tfm_generators import *
from mob_tfm.utils.utils import clean_str, is_valid_str,echo

tfm_generator: TypeAlias = Callable[...,object]

@dataclass
class column:
    """
    Ths Official tfm class for generated values
    
    `alias`:
        represent the text of the mariadb/sql column
    
    `tfm_generator`:
        the associated tfm_generator to run
        
    `args`:
        the arguments to use when running `tfm_generator`,
        the first fake parameter in all tfm_generators shouldn't be include not included
    """
    alias: str
    generator: tfm_generator
    args: dict

    def __str__(self):
        return f"column(alias='{self.alias}', generator={self.generator.__name__}, args={self.args})"
    
    def __repr__(self):
        return self.__str__()

GENERATORS = {
    "name": gen_name,
    "firstname": gen_firstname,
    "lastname": gen_lastname,
    "address": gen_address,
    "phone": gen_phone,
    "email": gen_email,
    "company": gen_company,
    "company_email": gen_company_email,
    "lang":gen_language,
    "century":gen_century,
    "int": gen_int,
    "float": gen_float
}

def build_columns(text: str) -> tuple[column]:
    """
    build a tuple of tfm columns from a space separated string.
    Example:

        `Student_name:name() Student_address:address(country='ES', city='Madrid')`
    returns:

        (column("Student_name", gen_name, {}),
        
         column("Student_address", gen_address, {'country':'ES', 'city':'Madrid'}))
    
    Note:
        in case of error the function will log the error and exit the program
    """
    entry = text.split()
    columns = []
    try:
        for i in range(len(entry)):
            column = build_column(entry[i])
            columns.append(column)
        return tuple(columns)
    except Exception as error:
        echo(f"unable to build Column {i+1}:\n{error}", "error")
        sys.exit(1)


def build_column(text: str) -> column:
    """
    Build a tfm column from a formatted string.
    
    The format is as follows:
    
        '<column_name>:<tfm_generator>([arg1=val1,arg2=val2])'
    
    in case a the generator will be use without any arguments the the format should be:
        
        '<column_name>':<tfm_generator>()'
        
    """
    if not(is_valid_str(text)):
        raise InvalidColumnFormat("Invalid Format, the input string is empty")
    
    elements = text.split(":")
    column_name = clean_str(elements[0])
    
    if len(elements) != 2:
        raise InvalidColumnFormat("Invalid Format, missing or too many ':' characters")
    
    generator_expr = clean_str(elements[1])
    generator, generator_args = parse_generator(generator_expr)
    
    return column(column_name, generator, generator_args)
    

def parse_generator(expr: str) -> tuple[tfm_generator, dict]:
    """
    a function that evaluate a string into a the (tfm_generator, arguments_dict) tuple

    Note: the arguments dict doesn't include the `fake` argument since it's always provided when calling the tfm_generator
    
    the format of the expression must be:
        '<tfm_generator>([arg1=val1,arg2=val2])

    Example:

        input: "address(country='ES', city='Madrid')"

        output: (gen_address, {'country':'ES', 'city':'Madrid'})
    """
    tree = ast.parse(expr, mode='eval')
    node = tree.body
    
    if not isinstance(node, ast.Call): # Not a function call
        raise ValueError("The generator expression is not a function call")
    
    generator_name = node.func.id # type: ignore
    generator = get_generator(generator_name)
    arguments = {}
    for keyword in node.keywords:
        arg_name = keyword.arg
        arg_value = ast.literal_eval(keyword.value)
        arguments[arg_name] = arg_value
    return (generator, arguments)
        

def get_generator(name: str) -> tfm_generator:
    """
    a function that return the matching tfm generator, raise UnknownGenerator if not found
    """
    
    found_generator = GENERATORS.get(name, None)
    if found_generator is None:
        raise UnknownGenerator(f"'{name}' is not a known tfm generator")
    return found_generator



def run_column_generator(generator: tfm_generator,fake:Faker,**args) -> object:
    """
    return the result of running a tfm_generator with the provided arguments
    """
    args["fake"] = fake
    return generator(**args)

def make_insert_value(fake:Faker, columns: tuple[column]) -> tuple:
    data = []
    for column in columns:
        generator_result = run_column_generator(column.generator,fake ,**column.args)
        data.append(generator_result)
        
    return tuple(data)



