from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    # return the list of requirement
    requirement_lst:List[str] = []
    try:
        with open("requirements.txt","r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement!= "-e .":
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirement.txt not found")
    
    return requirement_lst 


#Test
#print(get_requirements())

setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Vaibhav',
    author_email='vaibhav09170@gmail.com',
    packages=find_packages(),
    install_requires= get_requirements()
)