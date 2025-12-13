import numpy as np
import pandas as pd
import scanpy as sc
from anndata import AnnData
from tqdm import tqdm

from revise.methods.base_method import BaseMethod
from revise.tools.coefficients import get_spatial_score
from revise.tools.coefficients import get_weighted_align_score
from revise.tools.topology import get_adjacency_graph


class GraphCluster(BaseMethod):
    """
    Graph-based clustering with spatial and alignment score evaluation.
    
    This class performs Leiden clustering at multiple resolutions and evaluates
    clustering quality using spatial coherence and alignment with cell type labels.
    """
    def __init__(self, config, logger):
        super().__init__(config, logger)

    def run(self, adata: AnnData, resolution, label):
        """
        Perform graph-based clustering and evaluate at multiple resolutions.
        
        Args:
            adata: AnnData object to cluster
            resolution: List of resolution values for Leiden clustering
            label: Column name in adata.obsm containing soft cell type labels
                (used for computing alignment scores)
                
        Returns:
            tuple: (adata, merge_df, best_res)
                - adata: AnnData with clustering results in obs
                - merge_df: DataFrame with metrics for each resolution
                - best_res: Best resolution based on alignment score
                
        For each resolution, computes:
        - Spatial score: Number of spatial neighbors with same cluster label
        - Alignment score: Agreement between clusters and cell type labels
        """
        adata = adata.copy()
        adata_raw = adata.copy()
        adjacency_graph = get_adjacency_graph(
            adata,
            "sp",
            self.config.rec_graph_method,
            self.config.rec_graph_alpha,
            self.config.rec_graph_exp_neighbor_num,
            self.config.rec_graph_spatial_neighbor_num
        )

        merge_df = pd.DataFrame()
        for res in tqdm(resolution, desc="leiden"):
            sc.tl.leiden(adata, adjacency=adjacency_graph, resolution=res, key_added=f"leiden_{res}")

            adata = get_spatial_score(adata, res=res)
            align_score = get_weighted_align_score(adata, res=res, label=label)
            mean_score = np.mean(adata.obs[f"spatial_score_{res}"])
            cluster_num = len(np.unique(adata.obs[f"leiden_{res}"]))
            df = pd.DataFrame({
                "resolution": res,
                "cluster_num": cluster_num,
                "mean_score": mean_score,
                "align_score": align_score,
            }, index=[0])

            self.logger.info(f"Resolution {res}: {cluster_num} clusters mean spatial score: {mean_score:.4f} {align_score}...")
            sc.pl.scatter(adata, x="x", y="y", color=f"leiden_{res}")
            sc.pl.scatter(adata, x="x", y="y", color=f"spatial_score_{res}")
            merge_df = pd.concat([merge_df, df], axis=0)
        best_res = merge_df[merge_df["align_score"] == merge_df["align_score"].max()]["resolution"].values[-1]
        self.logger.info(f"Best resolution: {best_res}")
        merge_df.reset_index(drop=True, inplace=True)
        adata_raw.obs = adata.obs.copy()
        return adata_raw, merge_df, best_res
