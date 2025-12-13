from pathlib import Path
from typing import Generator
from typing import Callable
from mob_tfm.exceptions import InvalidColumnFormat,UnknownConverter,ImpossibleRowConvertion
from .utils import is_valid_str,echo


CONVERTERS : dict[str, Callable] = {
    "int": int,
    "float": float
}

def get_file_generator(file_path: Path) -> Generator[tuple[str,...],None,None]:
        """
        a function that returns a generator,

        each next() call on the generator return a csv file content under a tuple of strings

        Note: this function SHOULD be only called after checking that the path exist and point to a csv file
        """
        with open(file_path,"r") as file:
            for line in file:
                clean_line = line.strip()
                values = clean_line.split(",")
                clean_values = tuple(map(lambda x: x.strip(),values))
                yield clean_values

def parse_csv_columns(columns: tuple[str,...]) -> tuple[tuple[str,...],tuple[Callable,...]] :
    """
    A function that cleans the types definition from a column string and return them as the following tuple

    input: `('name','age:int','job','salary:float')`

    ```
    (
        ('name','age','job','salary'),
        (str,int,str,float)
    )
    """
    columns_names = []
    converters = []
    for i in range(len(columns)):

        if ":" not in columns[i]:
            columns_names.append(columns[i].strip())
            converters.append(str)
            continue
        
        column_data = columns[i].split(":")
        columns_names.append(column_data[0].strip())
        
        if not is_valid_str(column_data[1]):
            raise InvalidColumnFormat(f"The column number {i} contains ':' but doesn't have any value after")
        
        converter_name = column_data[1].strip()
        converter = CONVERTERS.get(converter_name)
        if converter is None:
            raise UnknownConverter(f"The provided converter on column {i} ({converter_name}) is unknown")
        
        converters.append(converter)

    return (tuple(columns_names), tuple(converters))

            
def convert_row(row: tuple[str,...],converters: tuple[Callable,...]) -> tuple[object,...]:
    row_len = len(row)
    converter_len = len(converters)
    if row_len != converter_len:
        raise ImpossibleRowConvertion(f"row and converters are of different length.\nrow length ==> {row_len}\nconverter length ==> {converter_len} ")
    
    output_list = []
    
    for i in range(row_len):
        data = row[i]
        converter = converters[i]
        converted_data = converter(data)
        output_list.append(converted_data)
    
    output = tuple(output_list)
    return output