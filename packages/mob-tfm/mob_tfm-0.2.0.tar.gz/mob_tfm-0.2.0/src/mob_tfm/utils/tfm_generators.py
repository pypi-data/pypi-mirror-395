from faker import Faker
from random import randint,uniform
from random import seed as rseed

def build_faker(seed: int | None = None , optimized: bool = False) -> Faker:
    """A function to build the faker object
    Note: each call will return a factory object 
    However using the seed argument alter the global seed of faker
    """
    fake = Faker(use_weighting = not(optimized))
    if seed:
        Faker.seed(seed)
        rseed(seed)
    
    return fake
    

def gen_name(fake: Faker) -> str:
    return fake.name()

def gen_firstname(fake: Faker) -> str:
    return fake.first_name()

def gen_lastname(fake: Faker) -> str:
    return fake.last_name()

def gen_address(fake: Faker) -> str:
    "A function that always return an inline address rather that faker multi line format"
    email = fake.address()
    lines = email.split("\n")
    inline_email = " ".join(lines)
    return inline_email 

def gen_phone(fake: Faker) -> str:
    return fake.phone_number()

def gen_email(fake: Faker,safe: bool = True, domain: str | None = None) -> str:
    return fake.email(safe=safe,domain=domain)

def gen_company(fake: Faker) -> str:
    return fake.company()

def gen_company_email(fake: Faker) -> str:
    return fake.company_email()

def gen_language(fake: Faker) -> str:
    return fake.language_name()

def gen_century(fake: Faker) -> str:
    return fake.century()

def gen_city(fake: Faker) -> str:
    return fake.city()

#: Custom tfm generator/Not faker based

def gen_int(**kwargs) -> int:
    minimum = int(kwargs.get("min",0))
    maximum = int(kwargs.get("max",1))
    
    return randint(minimum, maximum)


def gen_float(**kwargs) -> float:
    
    minimum :float = float(kwargs.get("min",0.0))
    maximum :float = float(kwargs.get("max",1.0))
    # we work with the maximum so one can do float(min=10.0,max=123.45)
    maximum_str :str = str(maximum) 
    maximum_data :list[str] = maximum_str.split(".")
    precision :int = len(maximum_data[1])
    num = uniform(minimum, maximum)

    return round(num,precision)
