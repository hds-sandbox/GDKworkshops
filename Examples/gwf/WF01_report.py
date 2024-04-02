from gwf import Workflow

gwf = Workflow()


## A target doing FastQC on a file
gwf.target('FastQC', 
           cores=1,
           memory='8gb',
           time='00:05:00',	
           inputs=['data/SRR2584863_1.fastq.gz'], 
           outputs=['data/SRR2584863_1_fastqc.html', 
                    'data/SRR2584863_1_fastqc.zip']) << """ 
fastqc data/SRR2584863_1.fastq.gz
"""