from gwf import *
from gwf.executors import Conda

## Create a workflow object
# this will contain settings which are global across all blocks
# of the workflow (templates below), unless for a specific
# template you specify a setting inside the dictionary "options"
gwf = Workflow( )

## Templates
# the generic structure of each block of your pipeline

# This first template needs to know the input file name and the desired output file name
# Inside it you can see the parameters needed to run the command, and the command itself 
# as part of `spec` - Note the commands are written in a bash command line syntax.
def renameFile(inputName, outputName):
    inputs  = [inputName]
    outputs = [outputName]
    options = {"cores": 1, "memory": "1g", "walltime": "00:01:00"}
    spec = f"""
        cp {inputName} {outputName}
    """
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


def zipFile(inputName):
    inputs  = [inputName]
    outputs = [f"{inputName}.gz"]
    options = {"cores": 1, "memory": "4g", "walltime": "00:10:00"}
    spec = f"""
        gzip -k {inputName}
    """
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


## Create targets
# here you run the python code which applies
# the templates to the explicit scenario you want
# to fulfill with your pipeline

# 1. Rename data.txt
# Each target needs a unique name (here "target_rename")
# The variable defined by `target_rename = ` contains the 
# Information of the target for any later use if necessary
target_rename = gwf.target_from_template("target_rename", 
                                         renameFile(inputName="data.txt", 
                                                    outputName="samples.txt")
                                        )

# 2. Zip samples.txt
target_gzip = gwf.target_from_template("target_gzip", 
                                         zipFile(inputName="samples.txt")
                                        )