import base64
import gzip
import io
import os
import re
import shutil
import warnings
from datetime import date
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import seaborn as sns
import seaborn.objects as so
from dousatsu import feature_preprocessing, feature_visualization
from plotly.subplots import make_subplots
from pyteomics.mass.unimod import Unimod
from rpy2 import robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from scipy import stats
from sklearn.pipeline import Pipeline
from upsetplot import from_indicators, plot


def download_surfy():
    """Downloads the latest version of the surfy file, extracts UniProt IDs,
    and saves them to a file.

    Output:
        surfy.txt: a file containing the UniProt IDs of the surfy proteins
    """
    surfy_link = "https://wlab.ethz.ch/surfaceome/table_S3_surfaceome.xlsx"
    surfy_filename = "surfy.txt"

    # Download surfy and store in pandas DataFrame
    surfy_df = pd.read_excel(
        surfy_link, sheet_name="in silico surfaceome only", header=1
    )
    surfy_set = set(surfy_df["Uniprot ID"].tolist())

    # Save surfy IDs to file
    with open(surfy_filename, "w") as fout:
        for surfy_id in surfy_set:
            fout.write(surfy_id + "\n")


def download_uniprot_annotation():
    """Downloads the latest version of the uniprot annotation file and saves it
    to a file.

    NOTE: This function is only for human proteins.

    Output:
        uniprot_annotation_YYYY-MM-DD.tsv: the uniprot annotation file
    """
    api_link = (
        "https://rest.uniprot.org/uniprotkb/stream?compressed=true"
        "&fields=accession%2Cprotein_name%2Ccc_function%2Cgene_names%2Cgo_c"
        "&format=tsv&query=%28%28proteome%3AUP000005640%29%29"
    )
    uniprot_annotation_filename = "uniprot_annotation_{}.tsv".format(
        date.today()
    )

    # Download uniprot annotation gunzip and save to file
    with open(uniprot_annotation_filename, "wb") as fout:
        with gzip.open(BytesIO(requests.get(api_link).content), "rb") as fin:
            shutil.copyfileobj(fin, fout)


class LuxFragPipeProtein:
    """The main class for the Lux package.

    This class is used to load and process data from FragPipe.

    Attributes:
        combined_protein_filename (str): Path to the FragPipe combined protein
            file (i.e. combined_protein.tsv).
        experiment_annotation_filename (str): Path to the FragPipe experiment
            annotation file (experiment_annotation.tsv)).
        uniprot_annotation_filename (str): Path to the uniprot annotation file.
            Can be downloaded via download_uniprot_annotation().
            (for human see: https://www.uniprot.org/uniprotkb?query=%28proteome%3AUP000005640%29)
        surfy_filename (str): Path to the surfy file.
            Can be downloaded via download_surfy().
            (column 2 from "in silico surfaceome only" page of https://wlab.ethz.ch/surfaceome/table_S3_surfaceome.xlsx)
        abundance_type (str): Abundance type to use. Must be one of:
            - "Spectral Count"
            - "Intensity" <- default for IonQuant DDA
            - "MaxLFQ"
            - "diann" <- default for DIANN DIA
        workflow_type (str): Workflow type to use. Must be one of:
            - "iq_dda": FragPipe DDA workflow with IonQuant based MS1 quantification.
            - "diann_dia": FragPipe DIA workflow with DIANN based quantification.
        quantile_threshold (float): Quantile threshold for removing proteins
            with low abundance values. Default is 0.
        min_peptide_count (int): Minimum number of peptides per protein.
            Default is 1.
        log_transform_abundance (bool): Whether to log10 transform abundance
            values. Default is True.
        intensity_label (str): Label for the abundance type used in plots.
        classes_palette_type (str): Color palette to use for classes. Default
            is pastel.
        classes_palette (dict): Dictionary of classes and colors. Set by
            load_experiment_annotation().
        experiment_annotation (pd.DataFrame): The experiment annotation file as
            a pd.DataFrame. Set by load_experiment_annotation().
            Index: sample (with selected abundance_type appended
                   (e.g. sample_Intensity)
            Columns: file, sample_name, class, replicate
        combined_protein (pd.DataFrame): The combined protein file as a
            pd.DataFrame. Set by load_combined_protein(). Note that other
            methods may modify this DataFrame.
            The following pre-processing is applied:
                - Only the requested abundance type is loaded.
                - Proteins with less than the minimum peptide count are removed.
                - Proteins with max abundance value less than the median of
                  self.quantile_threshold abundance across all samples are removed.
                - 0 values are replaced with NaN.
                - Proteins with only NaN values are removed.
                - Abundance values are log10 transformed according to
                  self.log_transform_abundance.
            Index: Protein ID
            Columns: [sample_abundance_type_1, sample_abundance_type_2, ...]
        uniprot_annotation (pd.DataFrame): The uniprot annotation file as a
            pd.DataFrame. Set by load_uniprot_annotation().
            Index: #
            Columns: Entry, Protein names, Function [CC], Gene Names,
                     Gene Ontology (cellular component), is_uniprot_membrane
        surfy_proteins (set): The surfy file as a set of proteins. Set by
            load_surfy().
        top_table (pd.DataFrame): The top table as a pd.DataFrame. Set by the
            limma_ttest() method.
            Index: #
            Columns: Entry, mean_log2_fc, ave_expr, t, p_val, adj_p, B,
                     -log10(adj_p), Protein names, Function [CC], Gene Names,
                     Gene Ontology (cellular component), is_uniprot_membrane,
                     is_surfy
        singularities_class1 (pd.DataFrame): The singularities for class 1 as a
            pd.DataFrame (i.e. proteins unique to class1). Set by the
            limma_ttest() method.
            NOTE: These proteins must be present in each replicate of class1.
            Index: sample (with selected abundance_type appended
                     (e.g. sample_Intensity)
            Columns: [protein1, protein2, ...]
        singularities_class2 (pd.DataFrame): The singularities for class 2 as a
            pd.DataFrame (i.e. proteins unique to class2). Set by the
            limma_ttest() method.
            NOTE: These proteins must be present in each replicate of class2.
            Index: sample (with selected abundance_type appended
                     (e.g. sample_Intensity)
            Columns: [protein1, protein2, ...]
    """  # noqa E501

    def __init__(
        self,
        input_folder,
        uniprot_annotation_filename,
        surfy_filename,
        quantile_threshold=0,
        min_peptide_count=1,
        log_transform_abundance=True,
        classes_palette_type="pastel",
        abundance_type=None,
        keep_peptidoforms=False,
        reduce_to_labels=False,
        debug=False,
        class_label1=None,
        class_label2=None,
        drop_samples=None,
    ):
        """Initialize the class."""
        self.debug = debug  # Set to True to enable debug mode
        if self.debug:
            self.debug_file = open("lux_debug.txt", "w")
            self.debug_file.write(
                f"Debug mode enabled. Debug file created at {date.today()}\n"
            )
        self.input_folder = input_folder
        self.combined_protein_filename = (
            ""  # Set by get_combined_protein_loader()
        )
        self.keep_peptidoforms = keep_peptidoforms
        self.combined_peptide_filename = (
            ""  # Set by get_combined_peptide_loader()
        )
        self.experiment_annotation_filename = (
            ""  # Set by get_experiment_annotation_loader()
        )
        self.uniprot_annotation_filename = uniprot_annotation_filename
        self.surfy_filename = surfy_filename
        self.cspa_filename = ""  # Not yet implemented
        self.workflow_type = self.get_workflow_type()
        if abundance_type is None:
            self.abundance_type = self.get_abundance_type()
        else:
            if abundance_type not in [
                "Spectral Count",
                "Intensity",
                "MaxLFQ",
                "diann",
            ]:
                raise ValueError(
                    "abundance_type must be one of: "
                    "'Spectral Count', 'Intensity', 'MaxLFQ', 'diann'"
                )
            if self.workflow_type == "iq_dda" and abundance_type == "diann":
                raise ValueError(
                    "abundance_type 'diann' is not supported for workflow_type "
                    "'iq_dda'"
                )
            if self.workflow_type == "diann_dia" and abundance_type != "diann":
                raise ValueError(
                    "abundance_type must be 'diann' for workflow_type "
                    "'diann_dia'"
                )
            self.abundance_type = abundance_type
        self.quantile_threshold = quantile_threshold
        self.min_peptide_count = min_peptide_count
        self.log_transform_abundance = log_transform_abundance
        if self.log_transform_abundance:
            self.intensity_label = "log10(feature intensity)"
        else:
            self.intensity_label = "feature intensity"
        self.reduce_to_labels = reduce_to_labels
        self.class_label1 = class_label1
        self.class_label2 = class_label2
        self.drop_samples = drop_samples
        self.classes_palette_type = classes_palette_type
        self.classes_palette = None  # Set by load_experiment_annotation()
        sns.set_palette(self.classes_palette_type)
        self.experiment_annotation = self.load_experiment_annotation()
        self.combined_peptide = self.load_combined_peptide()
        self.combined_protein = self.load_combined_protein()
        self.uniprot_annotation = self.load_uniprot_annotation()
        self.surfy_proteins = self.load_surfy()
        self.top_table = None
        self.singularities_class1 = None
        self.singularities_class2 = None

    def close(self):
        """Closes the debug file if it was opened."""
        if self.debug_file:
            self.debug_file.close()

    def get_workflow_type(self):
        """Check in fragpipe.workflow file for workflow type.

        Returns:
        workflow_type (str): Workflow type to use. Must be one of:
            - "iq_dda": FragPipe DDA workflow with IonQuant based MS1
                        quantification.
            - "diann_dia": FragPipe DIA workflow with DIANN based
                           quantification.
        """
        workflow_filename = self.input_folder + "/fragpipe.workflow"
        if not os.path.isfile(workflow_filename):
            raise FileNotFoundError(f"File not found: {workflow_filename}")
        # Set workflow type to:
        # - iq_dda if diann.run-dia-nn=false
        # - diann_dia if diann.run-dia-nn=true
        with open(workflow_filename, "r") as f:
            for line in f:
                if "diann.run-dia-nn" in line:
                    if "false" in line:
                        return "iq_dda"
                    elif "true" in line:
                        return "diann_dia"
                    else:
                        raise ValueError(
                            f"Unknown diann.run-dia-nn value: {line.strip()}"
                        )
        raise ValueError(f"diann.run-dia-nn not found in {workflow_filename}")

    def get_abundance_type(self):
        """Set default abundance type depending on workflow_type.

        We set the default abundance type to the following:
        - "Intensity" for iq_dda
        - "diann" for diann_dia
        """
        if self.workflow_type == "iq_dda":
            return "Intensity"
        elif self.workflow_type == "diann_dia":
            return "diann"
        else:
            raise ValueError(f"Unknown workflow_type: {self.workflow_type}")

    def get_experiment_annotation_loader(self):
        """Returns the correct experiment annotation loader depending on
        workflow_type.

        Returns:
        load_experiment_annotation (function): Function to load the
            experiment annotation file.
        """
        if self.workflow_type == "iq_dda":
            self.experiment_annotation_filename = (
                self.input_folder + "/experiment_annotation.tsv"
            )
            # Raise error if file  doesn't exist
            if not os.path.isfile(self.experiment_annotation_filename):
                raise FileNotFoundError(
                    f"File not found: {self.experiment_annotation_filename}"
                )
            return self.load_experiment_annotation_iq_dda
        elif self.workflow_type == "diann_dia":
            self.experiment_annotation_filename = (
                self.input_folder + "/experiment_annotation.tsv"
            )
            if not os.path.isfile(self.experiment_annotation_filename):
                raise FileNotFoundError(
                    f"File not found: {self.experiment_annotation_filename}"
                )
            return self.load_experiment_annotation_diann_dia
        else:
            raise ValueError(f"Unknown workflow_type: {self.workflow_type}")

    def load_experiment_annotation(self):
        """Load FragPipe experiment annotation file."""
        experiment_annotation_loader = self.get_experiment_annotation_loader()
        return experiment_annotation_loader()

    def load_experiment_annotation_iq_dda(self):
        """Load FragPipe experiment annotation file.

        Loads the content of the experiment annotation file as a pd.DataFrame.
        - The sample names are appended with the abundance_type specified
          at initialization.
        - Modified sample names as set as the index.
        - The condition column is renamed to class.

        Sets the classes_palette attribute as a dictionary of classes and
        colors.

        Returns:
            pd.DataFrame: The experiment annotation file as a pd.DataFrame.
        """
        experiment_annotation = pd.read_csv(
            self.experiment_annotation_filename, sep="\t"
        )
        if self.reduce_to_labels:
            # Limit to conditions that match self.class_label1 and
            # self.class_label2

            # Make sure class_label1 and class_label2 are set
            if self.class_label1 is None or self.class_label2 is None:
                raise ValueError(
                    "class_label1 and class_label2 must be set "
                    "to reduce to labels"
                )
            experiment_annotation = experiment_annotation[
                (experiment_annotation["condition"] == self.class_label1)
                | (experiment_annotation["condition"] == self.class_label2)
            ]
        # Drop samples from self.drop_samples list
        if self.drop_samples is not None:
            experiment_annotation = experiment_annotation[
                ~experiment_annotation["sample"].isin(self.drop_samples)
            ]
        experiment_annotation["sample"] = (
            experiment_annotation["sample"] + " " + self.abundance_type
        )
        experiment_annotation.set_index("sample", inplace=True)
        experiment_annotation.rename(
            columns={"condition": "class"}, inplace=True
        )
        # Set color palette for classes as a dictionary
        self.classes_palette = dict(
            zip(
                experiment_annotation["class"].unique(),
                sns.color_palette(
                    self.classes_palette_type,
                    len(experiment_annotation["class"].unique()),
                ).as_hex(),
            )
        )
        return experiment_annotation

    def load_experiment_annotation_diann_dia(self):
        """Load FragPipe experiment annotation file.

        Loads the content of the experiment annotation file as a pd.DataFrame.
        - The sample names are appended with the abundance_type specified
          at initialization.
        - Modified sample names as set as the index.
        - The condition column is renamed to class.

        Sets the classes_palette attribute as a dictionary of classes and
        colors.

        Returns:
            pd.DataFrame: The experiment annotation file as a pd.DataFrame.
        """
        experiment_annotation = pd.read_csv(
            self.experiment_annotation_filename, sep="\t"
        )
        if self.reduce_to_labels:
            # Limit to conditions that match self.class_label1 and
            # self.class_label2

            # Make sure class_label1 and class_label2 are set
            if self.class_label1 is None or self.class_label2 is None:
                raise ValueError(
                    "class_label1 and class_label2 must be set "
                    "to reduce to labels"
                )
            experiment_annotation = experiment_annotation[
                (experiment_annotation["condition"] == self.class_label1)
                | (experiment_annotation["condition"] == self.class_label2)
            ]
        # Drop samples from self.drop_samples list
        if self.drop_samples is not None:
            experiment_annotation = experiment_annotation[
                ~experiment_annotation["sample"].isin(self.drop_samples)
            ]
        experiment_annotation["sample"] = (
            experiment_annotation["sample_name"] + " " + self.abundance_type
        )
        experiment_annotation.set_index("sample", inplace=True)
        experiment_annotation.rename(
            columns={"condition": "class"}, inplace=True
        )
        # Set color palette for classes as a dictionary
        self.classes_palette = dict(
            zip(
                experiment_annotation["class"].unique(),
                sns.color_palette(
                    self.classes_palette_type,
                    len(experiment_annotation["class"].unique()),
                ).as_hex(),
            )
        )
        return experiment_annotation

    def get_combined_protein_loader(self):
        """Returns the correct combined protein loader depending on
        workflow_type.

        Returns:
        load_combined_protein (function): Function to load the
            combined protein file.
        """
        if self.workflow_type == "iq_dda":
            self.combined_protein_filename = (
                self.input_folder + "/combined_protein.tsv"
            )
            if not os.path.isfile(self.combined_protein_filename):
                raise FileNotFoundError(
                    f"File not found: {self.combined_protein_filename}"
                )
            return self.load_combined_protein_iq_dda
        elif self.workflow_type == "diann_dia":
            # Older versions used to save under diann-output folder
            # Newer under dia-quant-output
            # Check which one exists
            if os.path.isdir(self.input_folder + "/dia-quant-output"):
                self.combined_protein_filename = (
                    self.input_folder + "/dia-quant-output/report.pg_matrix.tsv"
                )
            else:
                self.combined_protein_filename = (
                    self.input_folder + "/diann-output/report.pg_matrix.tsv"
                )
            if not os.path.isfile(self.combined_protein_filename):
                raise FileNotFoundError(
                    f"File not found: {self.combined_protein_filename}"
                )
            return self.load_combined_protein_diann_dia
        else:
            raise ValueError(f"Unknown workflow_type: {self.workflow_type}")

    def load_combined_protein(self):
        """Load FragPipe experiment annotation file."""
        combined_protein_loader = self.get_combined_protein_loader()
        return combined_protein_loader()

    def load_combined_protein_iq_dda(self):
        """Load FragPipe combined protein file.

        Loads the content of the combined protein file as a pd.DataFrame and
        performs the following pre-processing:
        - Only the requested abundance type is loaded.
        - Proteins with less than the minimum peptide count are removed.
          This is meant as a way to remove proteins with low evidence and possibly
          unreliable quantification.
        - Proteins with max abundance value less than the median of
          self.quantile_threshold abundance across all samples are removed.
          This is meant as a quick way to remove consistently low abundance proteins.
        - 0 values are replaced with NaN.
        - Proteins with only NaN values are removed.
        - Abundance values are log10 transformed according to
          self.log_transform_abundance.

        Returns:
            pd.DataFrame: The combined protein file as a pd.DataFrame.
                 Index: Protein ID
                 Columns: [sample_abundance_type_1, sample_abundance_type_2,
                           ...]
        """
        # If reduce_to_labels only load samples that match, which in this case
        # is the same as self.experiment_annotation["sample_name"]
        combined_protein_columns = ["Protein ID", "Combined Total Peptides"] + [
            sample + " " + self.abundance_type
            for sample in self.experiment_annotation["sample_name"]
        ]
        combined_protein = pd.read_csv(
            self.combined_protein_filename,
            sep="\t",
            usecols=combined_protein_columns,
            index_col="Protein ID",
        )
        # If reduce_to_labels or drop_samples we need to recalculate
        # "Combined Total Peptides".  Based on self.combined_peptide
        if self.reduce_to_labels or self.drop_samples:
            tot_peptide_counts = (
                self.combined_peptide.groupby("Protein ID")
                .count()
                .transpose()
                .sum()
            )
            # Match by Protein ID and replace "Combined Total
            # Peptides"
            combined_protein["Combined Total Peptides"] = tot_peptide_counts
        # DEBUG save proteins we are about to remove to file
        if self.debug:
            removed_proteins = combined_protein[
                combined_protein["Combined Total Peptides"]
                < self.min_peptide_count
            ]
            if not removed_proteins.empty:
                self.debug_file.write(
                    f"Removed {len(removed_proteins)} proteins with less than "
                    f"{self.min_peptide_count} peptides.\n"
                )
                self.debug_file.write(
                    ", ".join(removed_proteins.index.tolist()) + "\n"
                )
        combined_protein = combined_protein[
            combined_protein["Combined Total Peptides"]
            >= self.min_peptide_count
        ]
        combined_protein.drop("Combined Total Peptides", axis=1, inplace=True)
        # DEBUG save proteins we are about to remove to file
        if self.debug:
            removed_proteins = combined_protein[
                combined_protein.transpose().max()
                <= combined_protein.quantile(self.quantile_threshold).median()
            ]
            if not removed_proteins.empty:
                self.debug_file.write(
                    f"Removed {len(removed_proteins)} proteins with "
                    f"max abundance value less than the median of "
                    f"quantile {self.quantile_threshold}.\n"
                )
                self.debug_file.write(
                    ", ".join(removed_proteins.index.tolist()) + "\n"
                )
        combined_protein = combined_protein[
            combined_protein.transpose().max()
            > combined_protein.quantile(self.quantile_threshold).median()
        ]
        combined_protein.replace(0, np.nan, inplace=True)
        combined_protein.dropna(inplace=True, how="all", axis=0)
        if self.log_transform_abundance:
            combined_protein = np.log10(combined_protein)
        return combined_protein

    def load_combined_protein_diann_dia(self):
        """Load FragPipe combined protein file.

        Loads the content of the combined protein file as a pd.DataFrame and
        performs the following pre-processing:
        - Proteins with less than the minimum peptide count are removed.
          This is meant as a way to remove proteins with low evidence and possibly
          unreliable quantification.        
        - Proteins with max abundance value less than the median of
          self.quantile_threshold abundance across all samples are removed.
          This is meant as a quick way to remove consistently low abundance proteins.        
        - 0 values are replaced with NaN.
        - Proteins with only NaN values are removed.
        - Abundance values are log10 transformed according to
          self.log_transform_abundance.

        Returns:
            pd.DataFrame: The combined protein file as a pd.DataFrame.
                 Index: Protein ID
                 Columns: [sample_1, sample_2,
                           ...]
        """
        # If reduce_to_labels only load samples that match, which in this case
        # is the same as self.experiment_annotation["file"]
        combined_protein_columns = ["Protein.Group"] + [
            ms_file for ms_file in self.experiment_annotation["file"]
        ]
        combined_protein = pd.read_csv(
            self.combined_protein_filename,
            sep="\t",
            usecols=combined_protein_columns,
            index_col="Protein.Group",
        )
        combined_protein.index.name = "Protein ID"

        # Rename columns from file to sample_name
        combined_protein.rename(
            columns=dict(
                zip(
                    self.experiment_annotation["file"],
                    self.experiment_annotation.index,
                )
            ),
            inplace=True,
        )

        # DIANN report.pg_matrix.tsv does not have a "Combined Total
        # Peptides" column, so we need to calculate it ourselves.
        tot_peptide_counts = (
            self.combined_peptide.reset_index()
            .groupby("Protein ID")["Peptide Sequence"]
            .nunique()
        )
        tot_peptide_counts.name = "Total Peptides"

        # Merge the peptide counts into the protein DataFrame
        combined_protein = combined_protein.merge(
            tot_peptide_counts, left_index=True, right_index=True
        )

        # DEBUG print removed proteins to file
        if self.debug:
            removed_proteins = combined_protein[
                combined_protein["Total Peptides"] < self.min_peptide_count
            ]
            if not removed_proteins.empty:
                self.debug_file.write(
                    f"Removed {len(removed_proteins)} proteins with less than "
                    f"{self.min_peptide_count} peptides.\n"
                )
                self.debug_file.write(
                    ", ".join(removed_proteins.index.tolist()) + "\n"
                )
        combined_protein = combined_protein[
            combined_protein["Total Peptides"] >= self.min_peptide_count
        ]
        combined_protein.drop("Total Peptides", axis=1, inplace=True)
        # DEBUG print removed proteins
        if self.debug:
            removed_proteins = combined_protein[
                combined_protein.transpose().max()
                <= combined_protein.quantile(self.quantile_threshold).median()
            ]
            if not removed_proteins.empty:
                self.debug_file.write(
                    f"Removed {len(removed_proteins)} proteins with "
                    f"max abundance value less than the median of "
                    f"quantile {self.quantile_threshold}.\n"
                )
                self.debug_file.write(
                    ", ".join(removed_proteins.index.tolist()) + "\n"
                )
        combined_protein = combined_protein[
            combined_protein.transpose().max()
            > combined_protein.quantile(self.quantile_threshold).median()
        ]
        combined_protein.replace(0, np.nan, inplace=True)
        combined_protein.dropna(inplace=True, how="all", axis=0)
        if self.log_transform_abundance:
            combined_protein = np.log10(combined_protein)
        return combined_protein

    def get_combined_peptide_loader(self):
        """Returns the correct combined peptide loader function.

        Returns:
        load_combined_peptide (function): Function to load the combined
            peptide file.
        """
        if self.workflow_type == "iq_dda":
            if self.keep_peptidoforms:
                self.combined_peptide_filename = (
                    self.input_folder + "/combined_modified_peptide.tsv"
                )
            else:
                self.combined_peptide_filename = (
                    self.input_folder + "/combined_peptide.tsv"
                )
            if not os.path.isfile(self.combined_peptide_filename):
                raise FileNotFoundError(
                    f"File not found: {self.combined_peptide_filename}"
                )
            return self.load_combined_peptide_iq_dda
        elif self.workflow_type == "diann_dia":
            # Older versions used to save under diann-output folder
            # Newer under dia-quant-output
            # Check which one exists
            if os.path.isdir(self.input_folder + "/dia-quant-output"):
                self.combined_peptide_filename = (
                    self.input_folder + "/dia-quant-output/report.pr_matrix.tsv"
                )
            else:
                self.combined_peptide_filename = (
                    self.input_folder + "/diann-output/report.pr_matrix.tsv"
                )
            if not os.path.isfile(self.combined_peptide_filename):
                raise FileNotFoundError(
                    f"File not found: {self.combined_peptide_filename}"
                )
            return self.load_combined_peptide_diann_dia
        else:
            raise ValueError(f"Unknown workflow_type: {self.workflow_type}")

    def load_combined_peptide(self):
        """Load FragPipe experiment annotation file."""
        combined_peptide_loader = self.get_combined_peptide_loader()
        return combined_peptide_loader()

    def load_combined_peptide_iq_dda(self):
        """Load FragPipe combined peptide file.

        Loads the content of the combined peptide file as a pd.DataFrame and
        performs the following pre-processing:
        - Only the requested abundance type is loaded.
        - Non-proteotypic peptides are removed.
        - Peptides with max abundance value less than the median of
          self.quantile_threshold abundance across all samples are removed.
          In other words, peptides are retained if their intensity in
          at least one sample exceeds the median intensity of the
          quantile specified in self.quantile_threshold of all
          peptides across all samples.
        - 0 values are replaced with NaN.
        - Peptides with only NaN values are removed.
        - Abundance values are log10 transformed according to
          self.log_transform_abundance.

        Returns:
            pd.DataFrame: The combined peptide file as a pd.DataFrame.
                 Index: "Modified Sequence", "Peptide Sequence"
                 Columns: [sample_abundance_type_1, sample_abundance_type_2,
                           ...]
            NOTE: if keep_peptidoforms is False, "Modified Sequence" is
                  identical by "Peptide Sequence".
        """
        intensity_columns = [
            sample + " " + self.abundance_type
            for sample in self.experiment_annotation["sample_name"]
        ]
        combined_peptide_columns = []
        if self.keep_peptidoforms:
            combined_peptide_columns = combined_peptide_columns + [
                "Modified Sequence"
            ]
        combined_peptide_columns = (
            combined_peptide_columns
            + [
                "Peptide Sequence",
                "Protein ID",
                "Mapped Genes",
            ]
            + intensity_columns
        )
        combined_peptide = pd.read_csv(
            self.combined_peptide_filename,
            sep="\t",
            usecols=combined_peptide_columns,
        )
        if not self.keep_peptidoforms:
            combined_peptide["Modified Sequence"] = combined_peptide[
                "Peptide Sequence"
            ]
        combined_peptide.set_index(
            ["Protein ID", "Modified Sequence", "Peptide Sequence"],
            inplace=True,
        )
        # Remove non-proteotypic peptides
        combined_peptide = combined_peptide[
            combined_peptide["Mapped Genes"].isna()
        ]
        combined_peptide.drop("Mapped Genes", axis=1, inplace=True)
        combined_peptide = combined_peptide[
            combined_peptide.transpose().max()
            > combined_peptide.quantile(self.quantile_threshold).median()
        ]
        combined_peptide.replace(0, np.nan, inplace=True)
        combined_peptide.dropna(inplace=True, how="all", axis=0)
        if self.log_transform_abundance:
            combined_peptide = np.log10(combined_peptide)
        return combined_peptide

    def load_combined_peptide_diann_dia(self):
        """Load FragPipe DIANN precursor file and convert to peptide.

        Loads the contenct of report.pr_matrix.tsv as a pd.DataFrame and
        performs the following pre-processing:
        - Peptides with max abundance value less than the median of
          self.quantile_threshold abundance across all samples are removed.
        - 0 values are replaced with NaN.
        - Peptides with only NaN values are removed.
        - Abundance values are log10 transformed according to
          self.log_transform_abundance.
        """
        combined_peptide_columns = [
            "Modified.Sequence",
            "Stripped.Sequence",
            "Protein.Ids",
            "Proteotypic",
        ] + [ms_file for ms_file in self.experiment_annotation["file"]]

        combined_peptide = pd.read_csv(
            self.combined_peptide_filename,
            sep="\t",
            usecols=combined_peptide_columns,
        )

        # Remove non-proteotypic peptides by dropping rows with Proteotypic=0
        combined_peptide.drop(
            combined_peptide[combined_peptide["Proteotypic"] == 0].index,
            inplace=True,
        )
        combined_peptide.drop("Proteotypic", axis=1, inplace=True)

        # Rename columns
        combined_peptide.rename(
            columns={
                "Modified.Sequence": "Modified Sequence",
                "Stripped.Sequence": "Peptide Sequence",
                "Protein.Ids": "Protein ID",
            },
            inplace=True,
        )
        # Rename file names
        combined_peptide.rename(
            columns=dict(
                zip(
                    self.experiment_annotation["file"],
                    self.experiment_annotation.index,
                )
            ),
            inplace=True,
        )

        # Replace (UniMod:id) modifications with their monoisotopic_mass
        # rounded to 4 decimal places for consistency with iq_dda
        unimod = Unimod()
        combined_peptide["Modified Sequence"] = combined_peptide[
            "Modified Sequence"
        ].apply(
            lambda x: re.sub(
                r"\(UniMod:(\d+)\)",
                lambda match: "["
                + str(
                    round(unimod.get(int(match.group(1))).monoisotopic_mass, 4)
                )
                + "]",
                x,
            )
        )

        # Sum intensity of all charge states for a given precursor
        if self.keep_peptidoforms:
            combined_peptide = combined_peptide.drop(
                ["Peptide Sequence"], axis=1
            )
            combined_peptide = combined_peptide.groupby(
                ["Protein ID", "Modified Sequence"]
            ).sum()
            combined_peptide.reset_index(inplace=True)
            # Add back Peptide Sequence by stripping the modified sequence
            combined_peptide["Peptide Sequence"] = combined_peptide[
                "Modified Sequence"
            ].apply(lambda x: re.sub(r"\[.*?\]", "", x))
            combined_peptide.set_index(
                ["Protein ID", "Modified Sequence", "Peptide Sequence"],
                inplace=True,
            )
        else:
            combined_peptide = combined_peptide.drop(
                ["Modified Sequence"], axis=1
            )
            combined_peptide = combined_peptide.groupby(
                ["Protein ID", "Peptide Sequence"]
            ).sum()
            # Copy index level 'Peptide Sequence' to 'Modified Sequence' level
            combined_peptide.reset_index(inplace=True)
            combined_peptide["Modified Sequence"] = combined_peptide[
                "Peptide Sequence"
            ]
            combined_peptide.set_index(
                ["Protein ID", "Modified Sequence", "Peptide Sequence"],
                inplace=True,
            )
        combined_peptide = combined_peptide[
            combined_peptide.transpose().max()
            > combined_peptide.quantile(self.quantile_threshold).median()
        ]
        combined_peptide.replace(0, np.nan, inplace=True)
        combined_peptide.dropna(inplace=True, how="all", axis=0)
        if self.log_transform_abundance:
            combined_peptide = np.log10(combined_peptide)

        return combined_peptide

    def drop_sample(self, sample):
        """Remove a sample from the experiment.

        Removes the sample from the combined_protein and experiment_annotation.

        Args:
            sample (str): The sample name to remove.
        """
        self.combined_protein.drop(sample, axis=1, inplace=True)
        self.experiment_annotation.drop(sample, axis=0, inplace=True)

    @staticmethod
    def format_long_lines_for_hover(col, wrap_len=40, max_len=200):
        """Formats long text for hover visualization in plotly.

        - Introduces html line breaks every wrap_len characters.
        - Truncates at a maximum of max_len characters.

        Args:
            col (pd.Series): The column to format.
            wrap_len (int, optional): The number of characters to wrap at.
                Defaults to 40.
            max_len (int, optional): The maximum number of characters to
                display. Defaults to 200.

        Returns:
            pd.Series: The formatted column.
        """
        col_trim = col.str[:max_len]
        col_wrap = col_trim.str.wrap(wrap_len)
        return col_wrap.apply(
            lambda x: (
                x.replace("\n", "<br>&nbsp;&nbsp;")
                if x is not np.nan
                else "Unknown"
            )
        )

    def load_uniprot_annotation(self):
        """Loads uniprot annotation file.

        Expects a tab-separated file with the following columns:
        - Entry
        - Protein names
        - Function [CC]
        - Gene Names
        - Gene Ontology (cellular component)

        Returns:
            pd.DataFrame: The uniprot annotation file as a pd.DataFrame.
                Index: #
                Columns: Entry, Protein names, Function [CC], Gene Names,
                         Gene Ontology (cellular component), is_uniprot_membrane
        """
        uniprot_annotation = pd.read_csv(
            self.uniprot_annotation_filename, sep="\t"
        )
        uniprot_annotation["Protein names"] = self.format_long_lines_for_hover(
            uniprot_annotation["Protein names"]
        )
        uniprot_annotation["Function [CC]"] = self.format_long_lines_for_hover(
            uniprot_annotation["Function [CC]"]
        )
        uniprot_annotation["Gene Ontology (cellular component)"] = (
            self.format_long_lines_for_hover(
                uniprot_annotation["Gene Ontology (cellular component)"]
            )
        )
        uniprot_annotation["is_uniprot_membrane"] = uniprot_annotation[
            "Gene Ontology (cellular component)"
        ].apply(lambda x: True if "plasma membrane" in x else False)
        return uniprot_annotation

    def load_cspa(self):
        """Load CSPA file.

        Returns:
            set: The CSPA file as a set of protein IDs.
        """
        # Load surfy protein annotations
        cspa = pd.read_csv(self.cspa_filename)
        return set(cspa["ID_link"])

    def load_surfy(self):
        """Load surfy file.

        Returns:
            set: The surfy uniprot IDS as a set.
        """
        # Load surfy protein annotations
        surfy = pd.read_csv(self.surfy_filename, header=None)
        return set(protein.split("_")[0] for protein in surfy[0])

    def plot_proteins_per_sample(self):
        """Plot the number of proteins per sample.

        Barplot visualization of the number of protein identifications
        per sample.
        """
        # Set width to 1/4 * number of samples
        width = 0.25 * len(self.experiment_annotation["sample_name"])
        plt.figure(figsize=(width, 5))
        X, y = self.get_protein_meta_dfs(fillna=False)
        X_meta = pd.DataFrame(X.T.count(), columns=["count"]).join(y)
        ax = sns.barplot(
            data=X_meta,
            x=X_meta.index,
            y="count",
            hue="class",
            dodge=False,
        )
        ax.set(title="Protein IDs per sample", ylabel="Protein #")
        labels = ax.get_xticklabels()
        ticks = range(len(labels))

        ax.set_xticks(ticks)
        ax.set_xticklabels(labels, rotation=90)
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)

    def plot_intensity_distributions_across_samples(self):
        """Visualize intensity distributions across samples as boxplots.

        Boxplot visualization of the intensity distributions across
        samples.
        """
        X, y = self.get_protein_meta_dfs(fillna=False)
        feature_visualization.visualize_intensity_distributions_across_samples(
            X.T, y, ylabel=self.intensity_label
        )

    def get_protein_meta_dfs(self, fillna=True, fillna_value=0.0001):
        """Get protein meta dataframes.

        Transposes the combined_protein dataframe and joins the class
        annotation. Optionally fills NaN values with a specified value.
        Finally splits the dataframe into X (abundances) and y (classes)
        that share a common index.

        Args:
            fillna (bool, optional): Whether to fill NaN values with
                fillna_value. Defaults to True.
            fillna_value (float, optional): The value to fill NaN values
                with. Defaults to 0.0001.

        Returns:
            tuple: (X, y) where X is the protein dataframe and y is the
                class dataframe.
                Note that X is transposed compared to the combined_protein
                dataframe (i.e. (samples, proteins))
        """
        X = self.combined_protein.transpose().copy()
        if fillna:
            X.fillna(fillna_value, inplace=True)
        X_meta = X.join(self.experiment_annotation["class"])
        # Sort by class so that samples from the same class will be
        # next to each other in plots.
        if self.reduce_to_labels:
            # If reduced to labels make sure class_label1 comes first
            # and class_label2 after
            order = [self.class_label1, self.class_label2]
            X_meta = X_meta.sort_values(
                "class",
                key=lambda x: x.map(
                    lambda y: order.index(y) if y in order else len(order)
                ),
            )
        else:
            X_meta = X_meta.sort_values("class")
        # Split into X and y
        y = pd.DataFrame(X_meta["class"])
        X = X_meta.drop("class", axis=1)
        return X, y

    def plot_corr_clustermap(self, figsize=None):
        """Plot clustermap of the correlation matrix.

        Calculates the correlation matrix of the protein dataframe and
        plots it as a clustermap with class membership as a leaf.

        Args:
            figsize (tuple, optional): The figure size. Defaults to None.
        """
        X, y = self.get_protein_meta_dfs()
        X = X.transpose()
        lut = {key: self.classes_palette[key] for key in y["class"].unique()}
        feature_visualization.samples_clustermap_plot(
            X, y, figsize=figsize, lut=lut
        )

    def plot_abundance_clustermap(self):
        """Plot clustermap of samples vs. proteins.

        Plots a clustermap of the protein dataframe with class
        membership as a leaf.
        """
        X, y = self.get_protein_meta_dfs()
        lut = {key: self.classes_palette[key] for key in y["class"].unique()}
        feature_visualization.clustermap_plot(
            X, y, title=self.intensity_label, lut=lut
        )

    def plot_pca(self):
        """PCA plot.

        Plots a PCA of the protein dataframe color coded by class.
        """
        X, y = self.get_protein_meta_dfs()
        feature_visualization.pca_batch_plots(X, y, plot_stripped=False)

    def normalize_protein_abundance(self):
        """Median normalize protein abundance.

        The abundance values are normalized by the median abundance value
        across all loaded samples. CAVE AT: if reduce_to_labels is True, the
        median is calculated only across the selected samples.

        CAVE AT: this function modifies self.combined_protein inplace.
        """
        preprocessing_pipe = Pipeline(
            [
                (
                    "median_normalize",
                    feature_preprocessing.MedianNormalizeIntensityMatrix(),
                ),
            ]
        )
        self.combined_protein = preprocessing_pipe.fit_transform(
            self.combined_protein
        )

    def normalize_peptide_abundance(self):
        """Median normalize peptide abundance.

        The abundance values are normalized by the median abundance value
        across all loaded samples. CAVE AT: if reduce_to_labels is True, the
        median is calculated only across the selected samples.

        CAVE AT: this function modifies self.combined_peptide inplace.
        """
        preprocessing_pipe = Pipeline(
            [
                (
                    "median_normalize",
                    feature_preprocessing.MedianNormalizeIntensityMatrix(),
                ),
            ]
        )
        self.combined_peptide = preprocessing_pipe.fit_transform(
            self.combined_peptide
        )

    def normalize_protein_abundance_global(self):
        """Global median normalize protein abundance.

        The abundance values are normalized by the median abundance value
        across all samples in the original experiment annotation file,
        regardless of reduce_to_labels setting, but taking into account the
        content of drop_samples.

        This function calculates the normalization offset for each
        sample and applies it to the current combined_protein
        dataframe. I.e. if reduce_to_labels is True, the normalization
        offsets are still calculated based on all samples, but only
        the selected samples are normalized. In this case peptide
        filtering based on min_peptide_count and quantile_threshold is
        still based on the reduced set of samples.  Normalization will
        be applied after those filters, but those filters will not
        affect the normalization offsets.

        Note that if reduce_to_labels is False this function is equivalent, but
        less efficient than normalize_protein_abundance().

        CAVE AT: this function modifies self.combined_protein inplace.
        """
        # Store original value of reduce_to_labels
        original_reduce_to_labels = self.reduce_to_labels
        # Temporarily set reduce_to_labels to False to load full experiment
        self.reduce_to_labels = False

        full_experiment_annotation = self.load_experiment_annotation()

        # Temporarily set experiment_annotation to full_experiment_annotation
        original_experiment_annotation = self.experiment_annotation
        self.experiment_annotation = full_experiment_annotation

        # Store original value of min_peptide_count and quantile_threshold
        original_min_peptide_count = self.min_peptide_count
        original_quantile_threshold = self.quantile_threshold
        # Temporarily set min_peptide_count and quantile_threshold to 0
        self.min_peptide_count = 0
        self.quantile_threshold = 0.0
        # Load full combined_protein
        full_combined_protein = self.load_combined_protein()

        # Perform median normalization on full combined_protein
        preprocessing_pipe = Pipeline(
            [
                (
                    "median_normalize",
                    feature_preprocessing.MedianNormalizeIntensityMatrix(),
                ),
            ]
        )
        full_combined_protein_median = preprocessing_pipe.fit_transform(
            full_combined_protein
        )

        # Calculate offsets
        offsets = full_combined_protein.subtract(full_combined_protein_median)

        # Apply offsets to current combined_protein
        relevant_offsets = offsets[self.combined_protein.columns]
        self.combined_protein = self.combined_protein - relevant_offsets

        # Restore original values
        self.reduce_to_labels = original_reduce_to_labels
        self.min_peptide_count = original_min_peptide_count
        self.quantile_threshold = original_quantile_threshold
        self.experiment_annotation = original_experiment_annotation

    def normalize_peptide_abundance_global(self):
        """Global median normalize peptide abundance.

        The abundance values are normalized by the median abundance value
        across all samples in the original experiment annotation file,
        regardless of reduce_to_labels setting, but taking into account the
        content of drop_samples.

        This function calculates the normalization offset for each
        sample and applies it to the current combined_peptide
        dataframe. I.e. if reduce_to_labels is True, the normalization
        offsets are still calculated based on all samples, but only
        the selected samples are normalized. In this case peptide
        filtering based on min_peptide_count and quantile_threshold is
        still based on the reduced set of samples.  Normalization will
        be applied after those filters, but those filters will not
        affect the normalization offsets.

        Note that if reduce_to_labels is False this function is equivalent, but
        less efficient than normalize_peptide_abundance().

        CAVE AT: this function modifies self.combined_peptide inplace.
        """
        # Store original value of reduce_to_labels
        original_reduce_to_labels = self.reduce_to_labels
        # Temporarily set reduce_to_labels to False to load full experiment
        self.reduce_to_labels = False

        full_experiment_annotation = self.load_experiment_annotation()

        # Temporarily set experiment_annotation to full_experiment_annotation
        original_experiment_annotation = self.experiment_annotation
        self.experiment_annotation = full_experiment_annotation

        # Store original value of quantile_threshold
        original_quantile_threshold = self.quantile_threshold
        # Temporarily set quantile_threshold to 0
        self.quantile_threshold = 0.0
        # Load full combined_peptide
        full_combined_peptide = self.load_combined_peptide()

        # Perform median normalization on full combined_peptide
        preprocessing_pipe = Pipeline(
            [
                (
                    "median_normalize",
                    feature_preprocessing.MedianNormalizeIntensityMatrix(),
                ),
            ]
        )
        full_combined_peptide_median = preprocessing_pipe.fit_transform(
            full_combined_peptide
        )

        # Calculate offsets
        offsets = full_combined_peptide.subtract(full_combined_peptide_median)

        # Apply offsets to current combined_peptide
        relevant_offsets = offsets[self.combined_peptide.columns]
        self.combined_peptide = self.combined_peptide - relevant_offsets

        # Restore original values
        self.reduce_to_labels = original_reduce_to_labels
        self.quantile_threshold = original_quantile_threshold
        self.experiment_annotation = original_experiment_annotation

    def impute_protein_abundance(self):
        """Simple min imputation.

        Missing values are filled with the minimum intensity measured in the
        corresponding sample minus a random percentage (between 1 and 10%) of
        said value.

        CAVE AT: this function modifies self.combined_protein inplace.
        """

        feature_visualization.visualize_missingness(
            feature_preprocessing.calculate_missingness(self.combined_protein),
            title="Missingness at the sample level",
        )

        feature_visualization.visualize_missingness(
            feature_preprocessing.calculate_missingness(
                self.combined_protein.transpose()
            ),
            title="Missingness at the peptide level",
        )

        impute_pipe = Pipeline(
            [
                (
                    "impute",
                    feature_preprocessing.FillNanWithMin(randomize=True),
                ),
            ]
        )
        self.combined_protein = impute_pipe.fit_transform(self.combined_protein)

    def limma_ttest(
        self, class_label1, class_label2, class_labels=None, debug=False
    ):
        """Differential abundance significance testing.

        Performs a differential abundance test using limma's bayes
        moderated t-test. Briefly, the following workflow is applied in R:
        - Fit a linear model to the abundance of each protein using limma's
          lmFit.
        - Fit a contrast matrix to calculate the difference between the
          parameter estimates of class_label1 - class_label2.
        - Computes Bayes moderated stats on the fitted contrast via limma's
          eBayes.

        Args:
            class_label1 (str): The first class label.
            class_label2 (str): The second class label.
            class_labels (list, optional): The list of class labels to
                include in the test. Defaults to only using class_label1 and
                class_label2.

        Sets:
            self.top_table: See return value.
            self.singularities_class1: The proteins that are present
                in each sample of class_label1, but absent from all
                samples in class_label2
            self.singularities_class2: The proteins that are present
                in each sample of class_label2, but absent from all
                samples in class_label1


        Returns:
            pd.DataFrame: A dataframe with the following columns:
                - Entry: The protein name.
                - mean_log2_fc: The log2 fold change of class_label1 over
                    class_label2.
                - ave_expr: The average log2 abundance of the protein.
                - t: The moderated t-statistic.
                - p_val: raw p-value.
                - adj_p: p-value adjusted for multiple testing by BH correction.
                - B: log-odds that the protein is differentially expressed.
                - -log10(adj_p): -log10 of the adjusted p-value.
                - Protein names: Additional protein names from UniProt
                - Function [CC]: Protein functions from UniProt
                - Gene Names: Gene names from UniProt
                - Gene Ontology (cellular component): GO cellular component
                    annotations from UniProt
                - is_uniprot_membrane: Whether the protein is annotated as
                    membrane in UniProt.
                - is_surfy: Whether the protein is annotated as membrane in
                    surfy.

        Dependencies:
            - R
            - limma
            - utils

        Refs:
            https://bioconductor.org/packages/release/workflows/vignettes/RNAseq123/inst/doc/designmatrices.html
        """  # noqa E501
        X = self.combined_protein.transpose().copy()
        X_meta = X.join(self.experiment_annotation["class"])
        # Filter out samples that are not in the list of desired classes
        if class_labels is None:
            class_labels = [class_label1, class_label2]
        X_meta = X_meta[X_meta["class"].isin(class_labels)]

        y = [cls for cls in X_meta["class"]]

        X = X_meta.drop("class", axis=1)
        if self.log_transform_abundance:
            X = 10**X
        XR = np.log2(X)
        XR = XR.transpose()

        # We rely on R and limma for bayes moderated t-test
        pandas2ri.activate()
        r_XR = pandas2ri.py2rpy(XR)  # (log2(protein abundances), samples)
        r_y = robjects.vectors.StrVector(y)
        print(r_y)
        r_class_label1 = robjects.vectors.StrVector([class_label1])
        r_class_label2 = robjects.vectors.StrVector([class_label2])
        importr("limma")
        importr("utils")
        robjects.r(
            """
         getTopTable <- function(XR, y, class_label1, class_label2, debug){
            # Convert to factor and set control as reference label
            factors = factor(y)
            # NOTE: since our variable is a factor, there is no difference
            # between including or not an intercept term in our design matrix
            design <- model.matrix(~0+factors)
            if (debug) {
            print(factors)
            print(design)
            print("Model matrix:")
            print(as.data.frame(design))
            }
            fit <- lmFit(XR, design)
            ctrst <- paste("factors", paste(class_label1, collapse=''),
                           "-factors", paste(class_label2, collapse=''), sep='')
            contrast.matrix <- makeContrasts(contrasts=ctrst, levels=design)
            if (debug) {
            print("Contrast matrix:")
            print(contrast.matrix)
            }
            fit2 <- contrasts.fit(fit, contrast.matrix)
            fit2 <- eBayes(fit2)
            bayes_fit <- topTable(fit2, coef=1, number=dim(XR)[1], adjust='BH')
         }
         """
        )
        r_get_top_table = robjects.globalenv["getTopTable"]
        topTable = r_get_top_table(
            r_XR, r_y, r_class_label1, r_class_label2, debug=debug
        )
        top_table = pandas2ri.rpy2py(topTable)
        top_table["-log10(adj_p)"] = -np.log10(top_table["adj.P.Val"])
        top_table = top_table.rename(
            {
                "logFC": "mean_log2_fc",
                "AveExpr": "ave_expr",
                "P.Val": "p_val",
                "adj.P.Val": "adj_p",
            },
            axis=1,
        )
        self.top_table = top_table
        self.top_table.reset_index(inplace=True)
        self.top_table.rename(columns={"index": "Entry"}, inplace=True)
        # Add UniProt metadata
        self.top_table = self.top_table.merge(
            self.uniprot_annotation, left_on="Entry", right_on="Entry"
        )
        # Add Surfy membrane localization
        self.top_table["is_surfy"] = False
        self.top_table.loc[
            self.top_table["Entry"].isin(self.surfy_proteins), "is_surfy"
        ] = True
        # Get list of proteins that were only present in one class
        singularities = self.top_table.loc[
            self.top_table["mean_log2_fc"].isnull(), "Entry"
        ]
        singularities_abundance = self.combined_protein.loc[
            singularities
        ].transpose()
        singularities_abundance_meta = singularities_abundance.join(
            self.experiment_annotation["class"]
        )
        self.singularities_class1 = singularities_abundance_meta.loc[
            singularities_abundance_meta["class"] == class_label1
        ]
        self.singularities_class1 = self.singularities_class1.drop(
            "class", axis=1
        )
        num_class1_samples = self.singularities_class1.shape[0]
        self.singularities_class1 = self.singularities_class1.dropna(
            thresh=num_class1_samples, axis=1
        )
        self.singularities_class2 = singularities_abundance_meta.loc[
            singularities_abundance_meta["class"] == class_label2
        ]
        self.singularities_class2 = self.singularities_class2.drop(
            "class", axis=1
        )
        num_class2_samples = self.singularities_class2.shape[0]
        self.singularities_class2 = self.singularities_class2.dropna(
            thresh=num_class2_samples, axis=1
        )
        return top_table

    def plot_volcano(self, class_label1, class_label2):
        """Plot volcano plot.

        Visualize the results of the differential expression analysis as
        an interactive volcano plot. The x-axis is the log2 fold change
        and the y-axis is the -log10 adjusted p-value.
        """
        feature_visualization.interactive_volcano_plot(
            self.top_table,
            hover_name_col="Entry",
            hover_data_cols=[
                "Gene Names",
                "Protein names",
                "Gene Ontology (cellular component)",
                "Function [CC]",
            ],
            title="Volcano plot {} vs. {}".format(class_label1, class_label2),
            fig_name=None,
        )

    def plot_singularities(self, class_label1, class_label2):
        """Plot singularity plot.

        Visualize the abundance of proteins that were only present in
        one class as a barplot.
        """
        colors = sns.color_palette()
        plt.rcParams["figure.autolayout"] = True
        f, axes = plt.subplots(1, 2)
        f.set_figwidth(15)
        if self.singularities_class1.shape[1] > 0:
            ax1 = sns.barplot(
                self.singularities_class1[
                    self.singularities_class1.mean()
                    .sort_values(ascending=False)
                    .index
                ],
                color=colors[1],
                ax=axes[0],
            )
            _ = ax1.set(
                title="Intensity of {} unique proteins".format(class_label2),
            )
            _ = ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)
        if self.singularities_class2.shape[1] > 0:
            ax2 = sns.barplot(
                self.singularities_class2[
                    self.singularities_class2.mean()
                    .sort_values(ascending=False)
                    .index
                ],
                color=colors[0],
                ax=axes[1],
            )
            _ = ax2.set(
                title="Intensity of {} unique proteins".format(class_label1),
            )
            _ = ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
        plt.suptitle(
            "Proteins unique to {} or {}".format(class_label1, class_label2)
        )

    def plot_interactive_singularities(self, class_label1, class_label2):
        """Plot singularity plot.

        Visualize the abundance of proteins that were only present in
        one class as a barplot.

        This version of the method uses plotly instead of matplotlib to
        create an interactive plot.
        """
        fig = make_subplots(rows=1, cols=2)
        fig.update_layout(
            template="plotly_white", yaxis_title=self.intensity_label
        )

        if self.singularities_class1.shape[1] > 0:
            # Calculate mean and std for each feature and store in
            # a dataframe sorted by mean
            df_mean_std = (
                self.singularities_class1.describe()
                .loc[["mean", "std"], :]
                .T.reset_index()
            )
            df_mean_std.columns = ["feature", "mean", "std"]
            df_mean_std = df_mean_std.sort_values(by="mean", ascending=False)
            # Add uniprot annotation
            df_mean_std = df_mean_std.merge(
                self.uniprot_annotation,
                left_on="feature",
                right_on="Entry",
                how="left",
            )
            # Plotly go bar plot
            fig.add_trace(
                go.Bar(
                    x=df_mean_std["feature"],
                    y=df_mean_std["mean"],
                    error_y=dict(type="data", array=df_mean_std["std"]),
                    name=class_label1,
                    marker_color=self.classes_palette[class_label1],
                    customdata=df_mean_std[
                        [
                            "feature",
                            "Protein names",
                            "Gene Names",
                            "Function [CC]",
                            "Gene Ontology (cellular component)",
                        ]
                    ].to_numpy(),
                    hovertemplate="Entry: %{customdata[0]}<br>"
                    + "Protein name: %{customdata[1]}<br>"
                    + "Gene name: %{customdata[2]}<br>"
                    + "Function: %{customdata[3]}<br>"
                    + "GO CC: %{customdata[4]}<br>",
                ),
                row=1,
                col=1,
            )

        if self.singularities_class2.shape[1] > 0:
            # Calculate mean and std for each feature and store in
            # a dataframe sorted by mean
            df_mean_std = (
                self.singularities_class2.describe()
                .loc[["mean", "std"], :]
                .T.reset_index()
            )
            df_mean_std.columns = ["feature", "mean", "std"]
            df_mean_std = df_mean_std.sort_values(by="mean", ascending=False)
            # Add uniprot annotation
            df_mean_std = df_mean_std.merge(
                self.uniprot_annotation,
                left_on="feature",
                right_on="Entry",
                how="left",
            )
            # Plotly go bar plot
            fig.add_trace(
                go.Bar(
                    x=df_mean_std["feature"],
                    y=df_mean_std["mean"],
                    error_y=dict(type="data", array=df_mean_std["std"]),
                    name=class_label2,
                    marker_color=self.classes_palette[class_label2],
                    customdata=df_mean_std[
                        [
                            "feature",
                            "Protein names",
                            "Gene Names",
                            "Function [CC]",
                            "Gene Ontology (cellular component)",
                        ]
                    ].to_numpy(),
                    hovertemplate="Entry: %{customdata[0]}<br>"
                    + "Protein name: %{customdata[1]}<br>"
                    + "Gene name: %{customdata[2]}<br>"
                    + "Function: %{customdata[3]}<br>"
                    + "GO CC: %{customdata[4]}<br>",
                ),
                row=1,
                col=2,
            )
        fig.show()

    def plot_intensity_of_significantly_changed_proteins(
        self, side=1, p_cutoff=0.01, fc_cutoff=0
    ):
        """Plot intensity of significantly changed proteins.

        Overlays the intensity of significantly changed proteins
        on top of the distribution of all proteins.

        Args:
            side (int): 1 for upregulated, -1 for downregulated, 0 for both
            p_cutoff (float): adjusted p-value cutoff. Default 0.01
            fc_cutoff (float): fold change cutoff. Default 0
        """
        # Filter combined_protein to proteins present in top_table
        tested_combined_protein = self.combined_protein.loc[
            self.top_table["Entry"]
        ]
        significant_proteins = tested_combined_protein.loc[
            self.get_top_table_selection(
                side=side, p_cutoff=p_cutoff, fc_cutoff=fc_cutoff
            )["Entry"]
        ]
        ax = sns.boxplot(tested_combined_protein, color="white")
        if not significant_proteins.empty:
            sns.lineplot(significant_proteins.transpose(), ax=ax)
            plt.legend(
                bbox_to_anchor=(1.02, 1),
                loc="upper left",
                borderaxespad=0,
                ncol=significant_proteins.shape[0] / 10,
            )
        _ = ax.set(
            title="Abundance distribution of significantly changing proteins"
        )
        _ = ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

    def plot_interactive_intensity_of_significantly_changed_proteins(
        self, side=1, p_cutoff=0.01, fc_cutoff=0
    ):
        """Plot intensity of significantly changed proteins.

        Overlays the intensity of significantly changed proteins
        on top of the distribution of all proteins.
        This version of the method uses plotly instead of matplotlib to
        create an interactive plot.

        Args:
            side (int): 1 for upregulated, -1 for downregulated, 0 for both
            p_cutoff (float): adjusted p-value cutoff. Default 0.01
            fc_cutoff (float): fold change cutoff. Default 0
        """
        # Filter combined_protein to proteins present in top_table
        tested_combined_protein = self.combined_protein.loc[
            self.top_table["Entry"]
        ]
        significant_proteins = tested_combined_protein.loc[
            self.get_top_table_selection(
                side=side, p_cutoff=p_cutoff, fc_cutoff=fc_cutoff
            )["Entry"]
        ]
        significant_proteins.fillna(0, inplace=True)

        if significant_proteins.empty:
            print("No significant proteins found.")
            return None
        # Prepare palette to colorize boxplots by class
        groups = tested_combined_protein.T.merge(
            self.experiment_annotation, left_index=True, right_index=True
        )["class"].T
        colors = [self.classes_palette[lbl] for lbl in groups]
        # Set width to 200 + 30 * number of samples
        width = 200 + 30 * tested_combined_protein.shape[1]

        # Setup for overlapping plots
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.update_layout(
            height=800,
            width=width,
            template="plotly_white",
            yaxis_title=self.intensity_label,
        )

        # Add traces for boxplots
        for idx, col in enumerate(tested_combined_protein.columns):
            fig.add_trace(
                go.Box(
                    y=tested_combined_protein[col],
                    notched=True,
                    name=col,
                    marker_color=colors[idx],
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

        # Add traces for protein abundances
        for index, row in significant_proteins.iterrows():
            entry = row.name
            protein_name = self.uniprot_annotation.loc[
                self.uniprot_annotation["Entry"] == row.name, "Protein names"
            ].iloc[0]
            gene_name = self.uniprot_annotation.loc[
                self.uniprot_annotation["Entry"] == row.name, "Gene Names"
            ].iloc[0]
            function = self.uniprot_annotation.loc[
                self.uniprot_annotation["Entry"] == row.name, "Function [CC]"
            ].iloc[0]
            go_cc = self.uniprot_annotation.loc[
                self.uniprot_annotation["Entry"] == row.name,
                "Gene Ontology (cellular component)",
            ].iloc[0]
            fig.add_trace(
                go.Scatter(
                    x=row.index,
                    y=row,
                    name=row.name,
                    customdata=[
                        [entry, protein_name, gene_name, function, go_cc]
                    ]
                    * row.shape[0],
                    hovertemplate="Entry: %{customdata[0]}<br>"
                    + "Protein name: %{customdata[1]}<br>"
                    + "Gene name: %{customdata[2]}<br>"
                    + "Function: %{customdata[3]}<br>"
                    + "GO CC: %{customdata[4]}<br>",
                )
            )

        fig.show()

    def plot_clustermap_of_significantly_changed_proteins(
        self, side=1, p_cutoff=0.01, fc_cutoff=0
    ):
        """Plot heatmap of significantly changed proteins.

        Args:
            side (int): 1 for upregulated, -1 for downregulated, 0 for both
            p_cutoff (float): adjusted p-value cutoff. Default 0.01
            fc_cutoff (float): fold change cutoff. Default 0
        """
        # Filter combined_protein to proteins present in top_table
        significant_proteins = self.get_top_table_selection(
            side=side, p_cutoff=p_cutoff, fc_cutoff=fc_cutoff
        )["Entry"]
        if len(significant_proteins) < 2:
            print("Insufficient number of significant IDs")
            return None
        df = self.combined_protein.loc[significant_proteins]
        vmin = df.min().min()
        df.fillna(0, inplace=True)
        rdgn = sns.diverging_palette(
            h_neg=230,
            h_pos=10,
            s=99,
            l=55,
            sep=3,
            as_cmap=True,
        )
        rdgn = sns.cubehelix_palette(as_cmap=True)
        ax = sns.clustermap(df, cmap=rdgn, vmin=vmin, col_cluster=False)
        _ = ax.fig.suptitle(
            "Abundance heatmap of significantly changing proteins"
        )
        plt.title(self.intensity_label)

    def plot_upset_proteins(self, min_subset_size=1):
        """Upset plot of protein identifications.

        Visualizes the distribution of protein identifications
        across samples.

        Args:
            min_subset_size (int): minimum size of a subset to be included in
                the plot. Default 1.
        """
        plot(
            from_indicators(indicators=pd.notna, data=self.combined_protein),
            min_subset_size=min_subset_size,
            orientation="vertical",
            show_counts=True,
        )
        plt.suptitle("Distribution of protein IDs across samples")

    def calculate_cv(self, cls):
        """Calculates coefficient of variation for each protein in class cls.

        Args:
            cls (str): Class to calculate coefficient of variation for.

        Returns:
            pd.Series: Coefficient of variation for each protein in class
            float: Median coefficient of variation for class
        """
        X_meta = self.combined_protein.T.merge(
            self.experiment_annotation.loc[
                self.experiment_annotation["class"] == cls, "class"
            ],
            left_index=True,
            right_index=True,
        )
        X = X_meta.drop("class", axis=1)
        if self.log_transform_abundance:
            X = 10**X
        # We set ddof=1 to ensure that the sample standard deviation is
        # computed as the square root of the unbiased sample variance.
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.variation.html
        cv = X.apply(lambda x: np.std(x, ddof=1) / np.mean(x) * 100, axis=0)
        median_cv = pd.Series(cv).dropna().median()
        return cv, median_cv

    def plot_cv(self):
        """Plots coefficient of variation.

        Plots histograms of coefficient of variation for each class.
        """
        classes = self.experiment_annotation["class"].unique()
        for cls in classes:
            cv, median_cv = self.calculate_cv(cls)
            sns.histplot(cv, bins=100, kde=True)
            plt.axvline(x=median_cv, color="red", linestyle="--")
            plt.text(
                median_cv,
                0,
                "Median CV: {:.2f}%".format(median_cv),
                rotation=90,
                verticalalignment="top",
            )
            plt.title("Coefficient of variation for {}".format(cls))
            plt.show()

    def filter_by_cv(self, cv_cutoff=20):
        """Filter proteins by coefficient of variation.

        Proteins with CV higher than cv_cutoff in all classes are removed.

        Args:
            cv_cutoff (int): Coefficient of variation cutoff.

        CAVE AT: this function modifies self.combined_protein inplace.
        """
        cv_df = pd.DataFrame(index=self.combined_protein.index)
        classes = self.experiment_annotation["class"].unique()
        for cls in classes:
            cv, _ = self.calculate_cv(cls)
            cv.name = cls
            cv_df = cv_df.merge(cv, left_index=True, right_index=True)
        keepers = pd.DataFrame(cv_df > cv_cutoff).apply(sum, axis=1) < len(
            classes
        )
        # If DEBUG is set save the removed proteins to the debug file
        if self.debug:
            removed_proteins = self.combined_protein[~keepers]
            if not removed_proteins.empty:
                self.debug_file.write(
                    f"Removed {len(removed_proteins)} proteins with CV higher "
                    f"than {cv_cutoff}.\n"
                )
                self.debug_file.write(
                    ", ".join(removed_proteins.index.tolist()) + "\n"
                )
        self.combined_protein = self.combined_protein.loc[keepers]

    def get_top_table_selection(self, side=0, p_cutoff=0.01, fc_cutoff=0):
        """Get top table selection.

        Filters top_table by p-value and fold change cutoffs.

        Args:
        - side: 0 for both, 1 for up, -1 for down
        - p_cutoff: p-value cutoff
        - fc_cutoff: fold change cutoff

        Returns:
            pd.DataFrame: top_table filtered by p-value and fold change cutoffs
        """
        match side:
            case -1:
                return self.top_table[
                    (self.top_table["adj_p"] < p_cutoff)
                    & (self.top_table["mean_log2_fc"] < -fc_cutoff)
                ]
            case 0:
                return self.top_table[
                    (self.top_table["adj_p"] < p_cutoff)
                    & (self.top_table["mean_log2_fc"].abs() > fc_cutoff)
                ]
            case 1:
                return self.top_table[
                    (self.top_table["adj_p"] < p_cutoff)
                    & (self.top_table["mean_log2_fc"] > fc_cutoff)
                ]
            case _:
                print("Invalid side value")
                return None

    def get_significant_peptides(self, side=0, p_cutoff=0.01, fc_cutoff=0):
        """Get peptides from significant proteins singularities.

        Filters top_table by p-value and fold change cutoffs,
        append singularities from class_label1,
        and returns a dataframe of corresponding peptides.

        Args:
            side (int): 0 for both, 1 for up, -1 for down
            p_cutoff (float): p-value cutoff
            fc_cutoff (float): fold change cutoff

        Returns:
            pd.DataFrame: Dataframe of significant peptides.
        """
        protein_list = []
        protein_list.append(
            self.get_top_table_selection(
                side=side, p_cutoff=p_cutoff, fc_cutoff=fc_cutoff
            )["Entry"]
        )
        match side:
            case -1:
                protein_list.append(
                    pd.Series(self.singularities_class2.columns)
                )
            case 0:
                protein_list.append(
                    pd.Series(self.singularities_class1.columns)
                )
                protein_list.append(
                    pd.Series(self.singularities_class2.columns)
                )
            case 1:
                protein_list.append(
                    pd.Series(self.singularities_class1.columns)
                )
        protein_series = pd.concat(protein_list).unique()
        return self.combined_peptide.loc[protein_series]

    @staticmethod
    def plot_membrane_enrichment(enrichment):
        """Plot membrane enrichment.

        Plots a barplot of membrane enrichment.

        Args:
            enrichment (pd.DataFrame): Membrane enrichment dataframe.
        """
        enrichment = enrichment.reset_index()

        colors = sns.color_palette("Greys")
        # Plot totals
        sns.barplot(data=enrichment, x="index", y="total", color=colors[1])
        # Plot enriched
        sns.barplot(data=enrichment, x="index", y="membrane", color=colors[0])
        plt.suptitle("Membrane enrichment estimations")
        # Add labels
        for i in enrichment.index:
            label = "{:.2f} enrichment".format(enrichment.loc[i, "enrichment"])
            y = enrichment.loc[i, "total"]
            plt.annotate(label, (i, y), ha="center", va="bottom")

            label = "{:.0f} total".format(enrichment.loc[i, "total"])
            y = enrichment.loc[i, "total"]
            plt.annotate(label, (i, y), ha="center", va="top")

            label = "{:.0f} membrane".format(enrichment.loc[i, "membrane"])
            y = enrichment.loc[i, "membrane"]
            plt.annotate(label, (i, y), ha="center", va="top")

        plt.xlabel("Metadata source")
        plt.ylabel("Number of proteins")
        plt.show()

    def get_membrane_enrichment(
        self, side=1, p_cutoff=0.01, fc_cutoff=0, plot=True
    ):
        """Get membrane enrichment.

        Calculates membrane enrichment for significant proteins and optionally
        plots it as a barplot.

        Args:
            side (int): 0 for both, 1 for up, -1 for down
            p_cutoff (float): p-value cutoff
            fc_cutoff (float): fold change cutoff
            plot (bool): whether to plot the results

        Returns:
            pd.DataFrame: Membrane enrichment dataframe.
                Index: uniprot, surfy
                Columns: membrane, total, enrichment
        """
        significant_proteins = self.get_top_table_selection(
            side=side, p_cutoff=p_cutoff, fc_cutoff=fc_cutoff
        )
        if significant_proteins.empty:
            print("No significant proteins found")
            return None

        num_membrane = significant_proteins["is_uniprot_membrane"].sum()
        total = significant_proteins.shape[0]
        enrichment = num_membrane / total
        uniprot_series = pd.Series(
            [num_membrane, total, enrichment],
            index=["membrane", "total", "enrichment"],
            name="uniprot",
        )
        num_membrane = significant_proteins["is_surfy"].sum()
        total = significant_proteins.shape[0]
        enrichment = num_membrane / total
        surfy_series = pd.Series(
            [num_membrane, total, enrichment],
            index=["membrane", "total", "enrichment"],
            name="surfy",
        )
        enrichment_df = pd.concat(
            [
                uniprot_series.to_frame().T,
                surfy_series.to_frame().T,
            ]
        )

        if plot:
            self.plot_membrane_enrichment(enrichment_df)

        return enrichment_df

    def get_membrane_enrichment_singularities(self, cls=1, plot=True):
        """Get membrane enrichment.

        Calculates membrane enrichment for proteins unique to a class.
        Optionally plots it as a barplot

        Args:
            cls (int): 1 or 2

        Returns:
            pd.DataFrame: Membrane enrichment dataframe.
                Index: uniprot, surfy
                Columns: membrane, total, enrichment
        """
        if cls == 1:
            proteins = list(self.singularities_class1.columns)
        elif cls == 2:
            proteins = list(self.singularities_class2.columns)
        else:
            print("Invalid class")
            return None

        singular_proteins = self.uniprot_annotation[
            self.uniprot_annotation["Entry"].isin(proteins)
        ].copy()
        if singular_proteins.empty:
            print("No singularity proteins found")
            return None
        singular_proteins["is_surfy"] = False
        singular_proteins.loc[
            singular_proteins["Entry"].isin(self.surfy_proteins), "is_surfy"
        ] = True

        num_membrane = singular_proteins["is_uniprot_membrane"].sum()
        total = singular_proteins.shape[0]
        enrichment = num_membrane / total
        uniprot_series = pd.Series(
            [num_membrane, total, enrichment],
            index=["membrane", "total", "enrichment"],
            name="uniprot",
        )
        num_membrane = singular_proteins["is_surfy"].sum()
        total = singular_proteins.shape[0]
        enrichment = num_membrane / total
        surfy_series = pd.Series(
            [num_membrane, total, enrichment],
            index=["membrane", "total", "enrichment"],
            name="surfy",
        )
        enrichment_df = pd.concat(
            [
                uniprot_series.to_frame().T,
                surfy_series.to_frame().T,
            ]
        )

        if plot:
            self.plot_membrane_enrichment(enrichment_df)

        return enrichment_df

    def peptides_barplot_html(self, protein_id):
        """Plot peptide quant as embedded barplot.

        All peptides for one protein are represented in stacked barplots.

        Args:
            protein_id (str): protein id

        Returns:
            str: HTML base64 encoded image (transparent png)
        """

        # Suppress seaborn warnings about tight_layout
        warnings.filterwarnings("ignore", module="seaborn\\..*axisgrid")
        # Get peptide quant values for proteins
        pep_df = self.combined_peptide.loc[protein_id]
        pep_df = pep_df.droplevel("Peptide Sequence")
        # Merge with experiment annotation to get class
        pep_df = (
            pep_df.transpose()
            .merge(
                self.experiment_annotation["class"],
                left_index=True,
                right_index=True,
            )
            .transpose()
        )
        pep_df.index.name = "Modified Sequence"
        pep_df.reset_index(inplace=True)
        pep_df_l = (
            pep_df.set_index("Modified Sequence")
            .transpose()
            .reset_index()
            .melt(id_vars=["index", "class"])
        )
        pep_df_l["value"] = pep_df_l["value"].astype(float).fillna(0)
        p = (
            so.Plot(pep_df_l, x="index", y="value", color="Modified Sequence")
            .facet(col="class")
            .share(x=False)
            .add(so.Bar(), so.Stack())
            .plot()
        )

        for ax in p._figure.axes:
            ax.xaxis.set_tick_params(rotation=90)

        # display(p)

        # Convert to base64 string for HTML embedding
        my_stringIObytes = BytesIO()
        p.save(
            my_stringIObytes,
            format="png",
            transparent=True,
            bbox_inches="tight",
        )
        my_stringIObytes.seek(0)
        my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
        embedded_img = '<img src="data:image/png;base64,{}">'.format(
            my_base64_jpgData
        )
        # Reset seaborn warnings
        warnings.filterwarnings("default", module="seaborn\\..*axisgrid")
        return embedded_img

    def peptides_lineplot_html(self, protein_id):
        # Get peptide quant values for proteins
        pep_df = self.combined_peptide.loc[protein_id]
        pep_df = pep_df.droplevel("Peptide Sequence")

        sorted_classes = pep_df.transpose().merge(
            self.experiment_annotation["class"],
            left_index=True,
            right_index=True,
            how="left",
        )

        if self.reduce_to_labels:
            # If reduced to labels make sure class_label1 comes first
            # and class_label2 after
            order = [self.class_label1, self.class_label2]
            sorted_classes = sorted_classes.sort_values(
                "class",
                key=lambda x: x.map(
                    lambda y: order.index(y) if y in order else len(order)
                ),
            )
        else:
            sorted_classes = sorted_classes.sort_values("class")

        sorted_pep_df = sorted_classes.drop("class", axis=1).transpose()

        # Plot peptide quant values
        fig, ax = plt.subplots(figsize=(3, 4))
        sns.lineplot(sorted_pep_df.transpose(), marker="o", ax=ax)
        if ax.get_legend() is not None:
            sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
        ax.set_ylim(0, sorted_pep_df.max().max() + 1)
        ax.tick_params(labelbottom=False)

        # Add class colored boxes at the bottom of the graph
        for count, cls in enumerate(sorted_classes["class"]):
            ax.axvspan(
                count - 0.5,
                count + 0.5,
                facecolor=self.classes_palette[cls],
                alpha=0.1,
                edgecolor="none",
            )

        # Convert to base64 string for HTML embedding
        my_stringIObytes = io.BytesIO()
        plt.savefig(
            my_stringIObytes,
            format="png",
            transparent=True,
            bbox_inches="tight",
        )
        my_stringIObytes.seek(0)
        my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
        embedded_img = '<img src="data:image/png;base64,{}">'.format(
            my_base64_jpgData
        )
        plt.close()

        return embedded_img

    # def peptides_lineplot_html(self, protein_id):
    #     # Get peptide quant values for proteins
    #     pep_df = self.combined_peptide.loc[protein_id]
    #     pep_df = pep_df.droplevel("Peptide Sequence")

    #     # Plot peptide quant values
    #     fig, ax = plt.subplots(figsize=(3, 4))
    #     sns.lineplot(pep_df.transpose(), marker="o", ax=ax)
    #     if ax.get_legend() is not None:
    #    	    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    #     ax.set_ylim(0, pep_df.max().max() + 1)
    #     ax.tick_params(labelbottom=False)

    #     # Add class colored boxes at the bottom of the graph
    #     sorted_classes = pep_df.transpose().merge(
    #         self.experiment_annotation,
    #         left_index=True,
    #         right_index=True,
    #         how="left",
    #     )
    #     for count, cls in enumerate(sorted_classes["class"]):
    #         ax.axvspan(
    #             count - 0.5,
    #             count + 0.5,
    #             facecolor=self.classes_palette[cls],
    #             alpha=0.1,
    #             edgecolor="none",
    #         )

    #     # Convert to base64 string for HTML embedding
    #     my_stringIObytes = io.BytesIO()
    #     plt.savefig(
    #         my_stringIObytes,
    #         format="png",
    #         transparent=True,
    #         bbox_inches="tight",
    #     )
    #     my_stringIObytes.seek(0)
    #     my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
    #     embedded_img = '<img src="data:image/png;base64,{}"'.format(
    #         my_base64_jpgData
    #     )
    #     plt.close()

    #     return embedded_img

    def protter_table(self, highlight_nxst=True):
        """Generate a summary table for significant proteins with protter
        links.

        An HTML table with significant/singularity proteins, proteotypic
        peptides, differential quant stats and their protter links is generated.
        Optionally, NxS/T sites are highlighted.

        Args:
            highlight_nxst (bool): whether to highlight NxS/T sites

        Returns:
            str: HTML table
        """
        protter_list = []
        nxst = re.compile(r"(N.[S,T])")
        # First add all significant IDs from top_table
        for _, row in self.get_top_table_selection().iterrows():
            protein_id = row["Entry"]
            protter_link = self.generate_protter_link(protein_id)
            if highlight_nxst:
                pep_list = [
                    nxst.sub(r'<font color="red"><b>\1</b></font>', pep)
                    for pep in self.combined_peptide.loc[
                        protein_id
                    ].index.get_level_values("Peptide Sequence")
                ]
            else:
                pep_list = self.combined_peptide.loc[protein_id].index
            protter_list.append(
                pd.DataFrame(
                    [
                        [
                            protein_id,
                            row["mean_log2_fc"],
                            row["adj_p"],
                            row["Gene Names"],
                            ",<br>".join(pep_list),
                            self.peptides_lineplot_html(protein_id),
                            '<a href="{}">protter</a>'.format(protter_link),
                        ]
                    ]
                )
            )
        # Then add all singularities
        for protein_id in self.singularities_class1.columns:
            protter_link = self.generate_protter_link(protein_id)
            if highlight_nxst:
                pep_list = [
                    nxst.sub(r'<font color="red"><b>\1</b></font>', pep)
                    for pep in self.combined_peptide.loc[
                        protein_id
                    ].index.get_level_values("Peptide Sequence")
                ]
            else:
                pep_list = self.combined_peptide.loc[protein_id].index
            protter_list.append(
                pd.DataFrame(
                    [
                        [
                            protein_id,
                            "inf",
                            "",
                            " ".join(
                                self.uniprot_annotation.loc[
                                    self.uniprot_annotation["Entry"]
                                    == protein_id,
                                    "Gene Names",
                                ]
                            ),
                            ",<br>".join(pep_list),
                            self.peptides_lineplot_html(protein_id),
                            '<a href="{}">protter</a>'.format(protter_link),
                        ]
                    ]
                )
            )
        for protein_id in self.singularities_class2.columns:
            protter_link = self.generate_protter_link(protein_id)
            if highlight_nxst:
                pep_list = [
                    nxst.sub(r'<font color="red"><b>\1</b></font>', pep)
                    for pep in self.combined_peptide.loc[
                        protein_id
                    ].index.get_level_values("Peptide Sequence")
                ]
            else:
                pep_list = self.combined_peptide.loc[protein_id].index
            protter_list.append(
                pd.DataFrame(
                    [
                        [
                            protein_id,
                            "-inf",
                            "",
                            " ".join(
                                self.uniprot_annotation.loc[
                                    self.uniprot_annotation["Entry"]
                                    == protein_id,
                                    "Gene Names",
                                ]
                            ),
                            ",<br>".join(pep_list),
                            self.peptides_lineplot_html(protein_id),
                            '<a href="{}">protter</a>'.format(protter_link),
                        ]
                    ]
                )
            )
        if not protter_list:
            return "No significant proteins found."
        protter_df = pd.concat(protter_list)
        protter_df.columns = [
            "Entry",
            "mean_log2_fc",
            "adj_p",
            "Gene Names",
            "Peptides",
            "Abundance",
            "Protter link",
        ]
        protter_df = protter_df.set_index("Entry")
        return protter_df.to_html(escape=False)

    def generate_protter_link(self, protein_id):
        """Generate a protter link for a given protein ID.

        Generates a link to protter for a given protein ID and all proteotypic
        peptides of that protein.

        Args:
            protein_id (str): The protein ID to generate the link for

        Returns:
            str: The link to protter for the given protein ID and all
                proteotypic peptides of that protein
        """
        # Get list of "Peptide Sequence" from index
        peptide_list = ",".join(
            self.combined_peptide.loc[protein_id].index.get_level_values(
                "Peptide Sequence"
            )
        )
        protter_link = (
            "https://wlab.ethz.ch/protter/#up={protein_id}&"
            "peptides={peptide_list}&"
            "tm=auto&"
            "mc=lightsalmon&"
            "lc=blue&"
            "tml=numcount&"
            "numbers&"
            "legend&"
            "tex=;&"
            "n:exp.peps,fc:darkblue=EX.PEPTIDES&"
            "n:signal%20peptide,fc:red,bc:red=UP.SIGNAL&"
            "n:disulfide%20bonds,s:box,fc:greenyellow,bc:greenyellow="
            "UP.DISULFID&"
            "n:variants,s:diamond,fc:orange,bc:orange=UP.VARIANT&"
            "n:PTMs,s:box,fc:forestgreen,bc:forestgreen=UP.CARBOHYD,UP.MOD_RES&"
            "n:exp.peps,cc:white,bc:blue=EX.PEPTIDES&"
            "format=svg".format(
                protein_id=protein_id, peptide_list=peptide_list
            )
        )
        return protter_link

    def plot_ma(self):
        """Plot an MA plot of the data in top_table."""

        # Make sure that top_table has been set
        if self.top_table is None:
            raise ValueError("top_table has not been set yet.")

        sns.scatterplot(
            self.top_table,
            x="ave_expr",
            y="mean_log2_fc",
            hue="-log10(adj_p)",
            alpha=0.7,
            s=10,
        )
        plt.title("MA plot")


class CorrelationMatrix:
    """Class for correlation matrix.

    Code from Max Ghenis stackoverflow
    """

    def __init__(self, df):
        self.df = df

    def cor_matrix(self):
        g = sns.PairGrid(self.df)
        # Use normal regplot as `lowess=True` doesn't provide CIs.
        g.map_upper(sns.regplot, scatter_kws={"s": 10})
        g.map_diag(
            sns.histplot,
            kde=True,
            kde_kws=dict(cut=3),
            alpha=0.4,
            edgecolor=(1, 1, 1, 0.4),
        )
        g.map_diag(self.annotate_colname)
        g.map_lower(sns.kdeplot, cmap="Blues_d")
        g.map_lower(self.corrfunc)
        # Remove axis labels, as they're in the diagonals.
        for ax in g.axes.flatten():
            ax.set_ylabel("")
            ax.set_xlabel("")
        return g

    @staticmethod
    def annotate_colname(x, **kws):
        ax = plt.gca()
        ax.annotate(
            x.name, xy=(0.05, 0.9), xycoords=ax.transAxes, fontweight="bold"
        )

    @staticmethod
    def corrfunc(x, y, **kws):
        r, p = stats.pearsonr(x, y)
        p_stars = ""
        if p <= 0.05:
            p_stars = "*"
        if p <= 0.01:
            p_stars = "**"
        if p <= 0.001:
            p_stars = "***"
        ax = plt.gca()
        ax.annotate(
            "r = {:.2f} ".format(r) + p_stars,
            xy=(0.05, 0.9),
            xycoords=ax.transAxes,
        )
