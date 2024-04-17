# markerfinder-euk

## This is a variation on the regular markerfinder script that can recover the three different eukaryotic RNAP variants

The original markerfinder script was written to provide a simple automated tool for recovering highly-conserved bacterial and archaeal marker genes and generating concatenated alignments that could then be used in phylogenetic inference (see https://github.com/faylward/markerfinder). 

Eukaryotes have multiple versions of RNAP, and so the initial version of markerfinder could not predict them and put them in a concatenated alignment. This tool what therefore modified to provide this workflow. 

Tool usage is the same as with markerfinder. The following example workflow will generate concatenated RNAP alignments for analyis of bacteria, archaea, viruses, and eukaryotes. 

First, predict RNAP subunits in the set of eukaryotic genomes (protein files) in eukprot_test. This uses hmmsearch to compare the proteins in these files to the allRNAP.hmm HMMs.

> python markerfinder_v2.py -i eukprot_test -n eukprot_test_out -c -m euk-rnap

Then do the same thing with the bacterial, archaeal, or viral proteins, using the regular RNAP HMMs. 

>python markerfinder_v2.py -i prokprot_test -n prokprot_test_out -c

Then, the outputs of both searches can be combined and aligned to get the final alignments. Note that the "merge_and_align.py" script requires muscle5 in your PATH, and it is called with the muscle5.1.linux_intel64 binary that can be found here: https://www.drive5.com/muscle/  

> python merge_and_align.py prokprot_test_out_alignments/ eukprot_test_out_alignments/ merged_alignments

 You should have two alignments in the merged_alignments folder, called COG0085 (beta subunit) and COG0086 (beta prime subunit). The individual eukaryotic versions will have the RNAP version in their name in the FASTA definition lines (i.e. >3075.RNAPII_COG0086 3075.RNAPII_RNAPIIbprime.copy1)
