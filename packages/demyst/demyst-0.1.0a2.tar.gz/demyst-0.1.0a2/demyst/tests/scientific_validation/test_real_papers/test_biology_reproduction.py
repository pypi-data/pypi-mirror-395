"""
Real Paper Reproduction Tests: Biology

Reproducing code snippets from Genomics, Bioinformatics, and Systems Biology.
"""

import textwrap

import pytest

from demyst.guards.hypothesis_guard import HypothesisGuard
from demyst.guards.leakage_hunter import LeakageHunter


class TestENCODEProject:
    """
    Based on large-scale genomic studies like ENCODE.
    Focus: Multiple hypothesis testing on gene expression.
    """

    def test_gene_expression_significance(self):
        """
        Testing thousands of genes for differential expression.
        """
        code = textwrap.dedent(
            """
            from scipy.stats import ttest_ind
            
            def identify_differentially_expressed_genes(expression_matrix, conditions):
                # expression_matrix: [n_genes, n_samples]
                significant_genes = []
                
                n_genes = expression_matrix.shape[0]
                
                for i in range(n_genes):
                    gene_data = expression_matrix[i]
                    group1 = gene_data[conditions == 0]
                    group2 = gene_data[conditions == 1]
                    
                    # Statistical Test per gene
                    stat, p_val = ttest_ind(group1, group2)
                    
                    # Flaw: No FDR correction (Benjamini-Hochberg) inside the loop
                    if p_val < 0.05:
                        significant_genes.append(i)
                        
                return significant_genes
        """
        )

        guard = HypothesisGuard()
        result = guard.analyze_code(code)

        # Should flag uncorrected multiple tests or conditional reporting
        violations = [
            v
            for v in result["violations"]
            if v["type"] in ["uncorrected_multiple_tests", "conditional_reporting"]
        ]
        assert len(violations) > 0


class TestGWASStudies:
    """
    Based on Genome-Wide Association Studies (GWAS).
    Focus: Leakage or Confounding (Population Stratification).
    """

    def test_feature_selection_on_all_snps(self):
        """
        Selecting 'top SNPs' before cross-validation (Leakage).
        """
        code = textwrap.dedent(
            """
            from sklearn.feature_selection import SelectKBest, f_classif
            from sklearn.model_selection import cross_val_score
            from sklearn.linear_model import LogisticRegression
            
            def predict_trait(snps, trait):
                # Flaw: Selecting top 100 SNPs using ALL data (including CV holdouts)
                selector = SelectKBest(f_classif, k=100)
                snps_selected = selector.fit_transform(snps, trait)
                
                # Then running CV
                model = LogisticRegression()
                scores = cross_val_score(model, snps_selected, trait, cv=5)
                return scores
        """
        )

        # LeakageHunter should catch fit_transform before cross_val_score
        hunter = LeakageHunter()
        result = hunter.analyze(code)

        violations = [v for v in result["violations"] if v["type"] == "preprocessing_leakage"]
        assert len(violations) > 0


class TestSingleCellRNASeq:
    """
    Based on scRNA-seq analysis pipelines (e.g., Seurat, Scanpy).
    Focus: Statistical validity in clustering/marker identification.
    """

    def test_marker_identification_p_hacking(self):
        """
        Adjusting clusters until markers are significant (a form of p-hacking/HARKing).
        Hard to detect 'adjusting clusters' statically, but we can detect 'optional stopping'
        style loops if they exist, or just simple multiple testing on markers.
        """
        code = textwrap.dedent(
            """
            from scipy.stats import ranksums
            
            def find_markers(clusters, expression):
                markers = {}
                for cluster_id in unique_clusters:
                    # Test every gene for this cluster vs others
                    for gene_id in all_genes:
                        p_val = ranksums(expr_in, expr_out).pvalue
                        
                        # Flaw: P-value thresholding without correction for (n_clusters * n_genes) tests
                        if p_val < 0.01:
                            markers.setdefault(cluster_id, []).append(gene_id)
                return markers
        """
        )

        guard = HypothesisGuard()
        result = guard.analyze_code(code)

        # Should flag multiple tests
        violations = [v for v in result["violations"] if v["type"] == "uncorrected_multiple_tests"]
        assert len(violations) > 0
