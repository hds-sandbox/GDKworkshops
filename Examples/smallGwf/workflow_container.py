from gwf import *
from gwf.executors import Conda
from gwf.executors import Singularity

#The conda env you want to use.
#You can also give a path to the environment

conda_env = Conda("seqkitEnv")
sing_cont = Singularity("./seqkit:2.10.0")

## Create a workflow object
# this will contain settings which are global across all blocks
# of the workflow (templates below), unless for a specific
# template you specify a setting inside the dictionary "options"
gwf = Workflow( )

## Templates
# the generic structure of each block of your pipeline

def split(infile, parts):
    inputs  = [infile]
    outputs = [f"gwf_splitted/part{number:>03}.fq" for number in range(1, parts + 1)]
    options = {"cores": 1, "memory": "4g", "walltime": "05:00:00"}
    spec = f"""
    seqkit split2 -O gwf_splitted --by-part {parts} --by-part-prefix part {infile}
    """
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec, executor=conda_env)


def table(infile):
    inputs  = [infile]
    outputs = [f"{infile}.fx2tab.tsv"]
    options = {"cores": 1, "memory": "1g", "walltime": "02:00:00"}
    spec = f"""
    seqkit fx2tab -n -l -C A -C C -C G -C T -C N -g -G -s {infile} >{outputs[0]}
    """
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec, executor=sing_cont)


def combine(infiles, outfile):
    inputs  = infiles
    outputs = [outfile]
    options = {"cores": 1, "memory": "1g", "walltime": "01:00:00"}
    spec = f"""
    cat {' '.join(infiles)} > {outfile}
    """
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)



## Create targets
# here you run the python code which applies
# the targets to the explicit scenario you want
# to fulfill with your pipeline

parts=10 # split input file in 10 parts

# 1. Split specific file
T1 = gwf.target_from_template("split", split(infile="data.fq", parts=parts))

# 2. Tabulate each chunk
seqkit_output_files = []
for i, infile in enumerate(T1.outputs):
   T2 = gwf.target_from_template(f"table_{i}", table(infile  = infile))
   seqkit_output_files.append(T2.outputs[0])

# 3. Combine results from each chunk.
gwf.target_from_template("combine",
    combine(
        infiles = seqkit_output_files,
        outfile = "gwf_combined.fx2tab.tsv",
    )
)