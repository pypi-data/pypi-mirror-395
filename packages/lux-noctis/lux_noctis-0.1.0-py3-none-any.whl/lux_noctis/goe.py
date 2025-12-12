import gzip
import shutil
from io import BytesIO, StringIO

import Bio.UniProt.GOA as GOA
import pandas as pd
import requests
from goatools import obo_parser
from goatools.go_enrichment import GOEnrichmentStudy


def download_go_files():
    """Downloads the latest versions of the GOA and OBO files."""
    gaf_link = "http://geneontology.org/gene-associations/goa_human.gaf.gz"
    gaf_filename = "goa_human.gaf"
    obo_link = "http://purl.obolibrary.org/obo/go/go-basic.obo"
    obo_filename = "go-basic.obo"

    # Download and gunzip the GAF file
    with open(gaf_filename, "wb") as gaf_fout:
        with gzip.open(
            BytesIO(requests.get(gaf_link).content), "rb"
        ) as gaf_fin:
            shutil.copyfileobj(gaf_fin, gaf_fout)

    # Download the OBO file
    with open(obo_filename, "wb") as obo_fout:
        obo_fout.write(requests.get(obo_link).content)


class Go:
    def __init__(
        self, gaf_filename, obo_filename, alpha=0.01, method="bonferroni"
    ):
        """Initializes a Go object.

        Params:
        - gaf_filename: the name of the GAF file to load
        - obo_filename: the name of the OBO file to load
        - alpha: the significance value to use for GO enrichment analysis
        - method: the method to use for p-value correction
                  ["bonferroni", "sidak", "holm", "fdr"] or
                  more if statsmodels is installed

        NOTES:
        - The population is set to all proteins in the GAF file by default and
           should be changed if needed via set_population()
        """
        self.gaf_filename = gaf_filename
        self.obo_filename = obo_filename
        self.alpha = alpha
        self.method = method
        self.assoc = None
        self.go = None
        self.load_go_ontologies()
        self.pop = self.assoc.keys()  # We use all proteins as population
        self.g = GOEnrichmentStudy(
            pop=self.pop,
            assoc=self.assoc,
            obo_dag=self.go,
            propagate_counts=True,
            alpha=self.alpha,
            methods=[self.method],
        )
        self.go_results = None
        self.go_results_df = None

    def load_go_ontologies(self):
        """Loads GAF and OBO gene ontologies in gaf_file_name and obo_filename.

        Sets:
        - self.assoc and self.go with assoc being protein to GO term
          associations and go being GODAG.
        """
        with open(self.gaf_filename, "rt") as gaf_fin:
            gaf_funcs = {}  # Initialise the dictionary of functions
            # Iterate on each function using Bio.UniProt.GOA library.
            for entry in GOA.gafiterator(gaf_fin):
                uniprot_id = entry.pop("DB_Object_ID")
                gaf_funcs[uniprot_id] = entry
        # Dictionary of UniProt IDs (keys) and GO annotations (values)
        self.assoc = {}
        for x in gaf_funcs:
            if x not in self.assoc:
                self.assoc[x] = set()
            self.assoc[x].add(str(gaf_funcs[x]["GO_ID"]))
        self.go = obo_parser.GODag(self.obo_filename)

    def set_population(self, population):
        """Sets the population to run GO enrichment analysis on.

        Params:
        - population: a list of protein IDs to set as the population
        """
        self.pop = population
        self.g = GOEnrichmentStudy(
            pop=self.pop,
            assoc=self.assoc,
            obo_dag=self.go,
            propagate_counts=True,
            alpha=self.alpha,
            methods=[self.method],
        )

    def run_go_enrichment(self, study):
        """Runs GO enrichment analysis on study.

        Params:
        - study: a list of protein IDs to run GO enrichment analysis on

        Sets:
        - self.go_results: the results of the GO enrichment analysis
        - self.go_results_df: a DataFrame containing the results of the GO
        """
        if len(study):
            self.go_results = self.g.run_study(study)
            with StringIO() as fout:
                self.g.prt_tsv(prt=fout, goea_results=self.go_results)
                fout.seek(0)
                self.go_results_df = pd.read_csv(fout, sep="\t")
        else:
            # If the list of proteins is empty don't try to run the analysis
            self.go_results = None
            self.go_results_df = None

    def run_go_enrichment_on_top_table(
            self, top_table, up=True, top_table_p_cutoff=0.01, top_table_fc_cutoff=0,
            extra_entries=[]
    ):
        """Runs GO enrichment analysis on the top_table results from limma
        eBayes analysis.

        Params:
        - top_table: a DataFrame containing the results of the limma eBayes
                     analysis
        - up: whether to run GO enrichment analysis on upregulated genes (True)
              or downregulated genes (False)
        - top_table_p-cutoff: the p-value cutoff to use for the top_table
        - top_table_fc_cutoff: the fold change cutoff to use for the top_table
        - extra_entries: list of extra entries to include in the study regardless of cutoffs

        Sets:
        - self.population: to all entries in top_table
        - self.go_results: the results of the GO enrichment analysis
        - self.go_results_df: a DataFrame containing the results of the GO
        """
        self.set_population(top_table["Entry"])
        if up:
            study = top_table[
                (top_table["adj_p"] < top_table_p_cutoff)
                & (top_table["mean_log2_fc"] > top_table_fc_cutoff)
            ]["Entry"]
        else:
            study = top_table[
                (top_table["adj_p"] < top_table_p_cutoff)
                & (top_table["mean_log2_fc"] < -top_table_fc_cutoff)
            ]["Entry"]
        study = pd.concat([study, pd.Series(extra_entries)]).unique()
        self.run_go_enrichment(study)
