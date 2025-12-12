import os
import shutil
from dataclasses import dataclass, field
import cv2
import ast
import pathlib
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import pandas as pd

from havoc_clustering_v2.general_utility.ai.tileextractor import TileExtractor
from havoc_clustering_v2 import correlation_of_dlfv_groups
from havoc_clustering_v2.general_utility import unique_colors
from havoc_clustering_v2.feature_extractor import FeatureExtractor


# from general_utility.ai.tileextractor import TileExtractor
# import correlation_of_dlfv_groups
# from general_utility import unique_colors
# from feature_extractor import FeatureExtractor


@dataclass(slots=True)
class DeveloperOptions:
    save_and_keep_tmp_tiles: bool = False
    save_parquet: bool = False
    map_scale_fac: int = 16


@dataclass(slots=True)
class HAVOCConfig:
    out_dir: str = './'
    k_vals: list[int] = field(default_factory=lambda: [7, 8, 9])  # if empty [], only performs feature extraction
    save_tiles_k_vals: list[int] = field(default_factory=list)

    tile_size: int = 512

    min_tissue_amt: float = 0.2

    extra_metrics: list[str] = field(default_factory=lambda: ['tsne', 'dendrogram', 'corr_clustmap'])

    # Developer-only section
    dev: DeveloperOptions = field(default_factory=DeveloperOptions, repr=False)

    def __post_init__(self):
        if not set(self.save_tiles_k_vals).issubset(self.k_vals):
            raise ValueError("save_tiles_k_vals must be a subset of k_vals")

        if self.tile_size < 256:
            raise ValueError("tile_size must be at least 256")

        if not (0.0 <= self.min_tissue_amt <= 1.0):
            raise ValueError("min_tissue_amt must be between 0 and 1")

        if not set(self.extra_metrics).issubset(['tsne', 'dendrogram', 'corr_clustmap']):
            raise ValueError("invalid extra_metrics")


class HAVOC:

    def __init__(self, havoc_config: HAVOCConfig):
        self.config = havoc_config
        self.feature_extractor = FeatureExtractor()
        self.save_tiles = bool(havoc_config.save_tiles_k_vals) or havoc_config.dev.save_and_keep_tmp_tiles

        pathlib.Path(havoc_config.out_dir).mkdir(parents=True, exist_ok=True)

    def run(self, slide):

        curr_out_dir = os.path.join(self.config.out_dir, slide.name)
        pathlib.Path(curr_out_dir).mkdir(parents=True, exist_ok=True)

        if 1:
            df, thumbnail = self.process_dlfvs(slide, curr_out_dir=curr_out_dir)
        else:
            df = pd.read_csv('')
            thumbnail = TileExtractor(slide, self.config.tile_size,
                                      map_scale_fac=self.config.dev.map_scale_fac).extraction_map
            thumbnail.image = cv2.imread('')

        df['Coor'] = df['Coor'].apply(ast.literal_eval)

        if len(self.config.k_vals) > 0:
            cluster_info_df = self.create_cluster_info_df(
                df[[str(x) for x in range(1, self.feature_extractor.num_features + 1)]], linkage_method='ward')
            df = pd.concat([cluster_info_df, df], axis=1)

        df.to_csv(os.path.join(curr_out_dir, 'cluster_info_df.csv'), index=False)
        if self.config.dev.save_parquet:
            df.to_parquet(os.path.join(curr_out_dir, 'cluster_info_df.parquet'), engine='pyarrow', compression="zstd",
                          index=False)

        for k in self.config.k_vals:
            self.create_colortiled_slide(df, thumbnail, target_k=k, curr_out_dir=curr_out_dir)

            if 'dendrogram' in self.config.extra_metrics:
                self.make_dendrogram(df, target_k=k, curr_out_dir=curr_out_dir)
            if 'tsne' in self.config.extra_metrics:
                self.make_tsne(df, target_k=k, curr_out_dir=curr_out_dir)
            if 'corr_clustmap' in self.config.extra_metrics:
                correlation_of_dlfv_groups.create_correlation_clustermap_single_slide(curr_out_dir, target_k=k)

        if self.save_tiles and not self.config.dev.save_and_keep_tmp_tiles:
            # done copying to k color folders
            shutil.rmtree(os.path.join(curr_out_dir, 'tiles', 'tmp'))

    def process_dlfvs(self, slide, curr_out_dir):

        if self.save_tiles:
            # we save all the tiles to a tmp folder and then copy the tiles into color folders when we do colortiling
            pathlib.Path(os.path.join(curr_out_dir, 'tiles', 'tmp')).mkdir(parents=True, exist_ok=True)

        print(f'Processing {slide.name}...')

        te = TileExtractor(slide, self.config.tile_size, map_scale_fac=self.config.dev.map_scale_fac)
        gen = te.iterate_tiles2(min_tissue_amt=self.config.min_tissue_amt, batch_size=4)

        coors = []
        coors_raw = []
        dlfvs = []
        amt_tissues = []
        for res in gen:
            tiles, currcoors, currcoors_raw, amt_tissue = res['tiles'], res['coordinates'], res['coordinates_raw'], res[
                'amt_tissue']

            currdlfvs = self.feature_extractor.process(tiles)
            # currdlfvs = np.zeros((tiles.shape[0],1536))

            coors.append(currcoors)
            coors_raw.append(currcoors_raw)
            dlfvs.append(currdlfvs)
            amt_tissues.append(amt_tissue)

            if self.save_tiles:
                # each iteration contains a batch of tiles
                for pos in range(len(tiles)):
                    curr_sp = os.path.join(curr_out_dir, 'tiles', 'tmp', str(tuple(currcoors[pos].tolist())) + '.jpg')
                    cv2.imwrite(curr_sp, tiles[pos])

        # we go through the whole slide so the extraction map is slide's thumbnail
        cv2.imwrite(os.path.join(curr_out_dir, 'thumbnail.jpg'), te.extraction_map.image)

        dlfvs = np.concatenate(dlfvs)
        coors = np.concatenate(coors)
        coors_raw = np.concatenate(coors_raw)
        amt_tissues = np.concatenate(amt_tissues)

        df = pd.DataFrame(dlfvs, columns=[str(x) for x in range(1, self.feature_extractor.num_features + 1)])
        df['Slide'] = [slide.name] * len(df)
        df['Coor'] = [str(x) for x in coors.tolist()]
        df['Coor_Raw'] = [str(x) for x in coors_raw.tolist()]
        df['AmtTissue'] = [round(x, 4) for x in amt_tissues]

        return df, te.extraction_map

    # cluster the data into k groups and assign each a (stable, incremental) color
    def create_cluster_info_df(self, X, linkage_method="ward"):

        k_vals = sorted(self.config.k_vals)
        k_min = k_vals[0]
        k_max = k_vals[-1]

        # 1) Build full hierarchy once
        Z = linkage(X, method=linkage_method)  # full tree

        # 2) Get labels for all k in one shot
        labels_per_k: dict[int, np.ndarray] = {}
        for k in k_vals:
            # fcluster returns labels 1..k; convert to 0..k-1
            labels = fcluster(Z, t=k, criterion="maxclust") - 1
            labels_per_k[k] = labels

        n_samples = X.shape[0]

        # 3) Global color generator (from your RGB_COLORS list)
        color_gen = unique_colors.next_color_generator(
            scaled=False,
            mode="rgb",
            shuffle=False,
        )

        # (k, cluster_id) -> {'name': ..., 'val': (r,g,b)}
        cluster_color: dict[tuple[int, int], dict] = {}

        # 4) Initialize colors at the smallest k (e.g., k=2)
        k_prev = k_min
        labels_prev = labels_per_k[k_prev]

        # sort clusters at k_min by size (largest first)
        counts_prev = np.bincount(labels_prev, minlength=k_prev)
        cluster_ids_sorted = np.argsort(counts_prev)[::-1]

        for cid in cluster_ids_sorted:
            color_info = next(color_gen)
            cluster_color[(k_prev, cid)] = color_info

        # 5) For each larger k, propagate and introduce new colors on splits
        for k in k_vals[1:]:
            labels_curr = labels_per_k[k]
            counts_curr = np.bincount(labels_curr, minlength=k)

            # Map each current cluster -> its parent cluster at k_prev
            parent_for_child: dict[int, int] = {}
            for c in range(k):
                mask = (labels_curr == c)
                # Because of hierarchy, this should be exactly one parent
                parent_ids = np.unique(labels_prev[mask])
                if parent_ids.size != 1:
                    # Safety check; in theory this shouldn't happen
                    raise RuntimeError(
                        f"Cluster {c} at k={k} has multiple parents at k={k_prev}: {parent_ids}"
                    )
                parent_for_child[c] = int(parent_ids[0])

            # Group children by parent
            parent_to_children: dict[int, list[int]] = {}
            for c, p in parent_for_child.items():
                parent_to_children.setdefault(p, []).append(c)

            # Assign colors for this k
            for p, children in parent_to_children.items():
                parent_color = cluster_color[(k_prev, p)]

                if len(children) == 1:
                    # No split: child keeps parent's color
                    c = children[0]
                    cluster_color[(k, c)] = parent_color
                else:
                    # Parent split into multiple children:
                    # - largest child keeps parent's color
                    # - others get new colors from palette
                    children_sorted = sorted(
                        children,
                        key=lambda c: counts_curr[c],
                        reverse=True
                    )

                    # Largest child inherits the parent's color
                    first = True
                    for c in children_sorted:
                        if first:
                            cluster_color[(k, c)] = parent_color
                            first = False
                        else:
                            cluster_color[(k, c)] = next(color_gen)

            # Move to next k
            k_prev = k
            labels_prev = labels_curr

        # 6) Build DataFrame with Cluster_k and color columns for all k
        dfs = []
        for k in k_vals:
            labels_k = labels_per_k[k]
            temp_df = pd.DataFrame({f"Cluster_{k}": labels_k})

            color_name_col = []
            color_rgb_col = []
            for lbl in labels_k:
                color_info = cluster_color[(k, lbl)]
                color_name_col.append(color_info["name"])
                color_rgb_col.append(color_info["val"])

            temp_df[f"Cluster_color_name_{k}"] = color_name_col
            temp_df[f"Cluster_color_rgb_{k}"] = color_rgb_col

            dfs.append(temp_df)

        # 7) Concatenate all k-level cluster columns side-by-side
        cluster_info_df = pd.concat(dfs, axis=1)

        return cluster_info_df

    def create_colortiled_slide(self, cluster_info_df, thumbnail, target_k, curr_out_dir):
        '''
        Using a dict mapping cluster to coordinates, creates bordered boxes all throughout the image.
        Optionally, save the tiles belonging to each color cluster
        '''

        # make the color folders for saving the actual tiles
        if target_k in self.config.save_tiles_k_vals:
            for c in cluster_info_df[f'Cluster_color_name_{target_k}'].unique():
                pathlib.Path(os.path.join(curr_out_dir, 'tiles', str(target_k), c)).mkdir(parents=True, exist_ok=True)

                coords = cluster_info_df['Coor'][cluster_info_df[f'Cluster_color_name_{target_k}'] == c]
                for _, coord in coords.items():
                    fname = str(tuple(coord)) + '.jpg'
                    try:
                        shutil.copy2(os.path.join(curr_out_dir, 'tiles', 'tmp', fname),
                                     os.path.join(curr_out_dir, 'tiles', str(target_k), c, fname))
                    except FileNotFoundError:
                        print(f'Tile for coordinate {coord} not found')

        # group on cluster color and get all the associated coordinates
        for color, coors in cluster_info_df.groupby(f'Cluster_color_rgb_{target_k}')['Coor'].apply(
                list).to_dict().items():
            # change rgb to bgr
            thumbnail.add_borders(coors, color=color[::-1], border_thickness=0.1)

        cv2.imwrite(
            os.path.join(curr_out_dir, 'k{}_colortiled.jpg'.format(target_k)),
            thumbnail.image
        )

    def make_tsne(self, cluster_info_df, target_k, curr_out_dir):
        print('Generating TSNE')

        res = TSNE(2).fit_transform(
            cluster_info_df[[str(x) for x in range(1, self.feature_extractor.num_features + 1)]])

        tsne_df = pd.DataFrame({'TSNE_X': res[:, 0], 'TSNE_Y': res[:, 1]})

        tsne_df['Cluster_color_hex'] = cluster_info_df[f'Cluster_color_rgb_{target_k}'].apply(
            lambda rgb_tuple: mpl.colors.rgb2hex([x / 255. for x in rgb_tuple]))

        # go through each cluster and get the data belonging to it. plot it with its corresponding color
        plt.close('all')
        for hex, rows in tsne_df.groupby('Cluster_color_hex'):
            plt.scatter(
                rows['TSNE_X'],
                rows['TSNE_Y'],
                s=20,
                c=[hex] * len(rows)
            )

        sp = os.path.join(curr_out_dir, 'k{}_tsne.jpg'.format(target_k))
        plt.savefig(sp, dpi=200, bbox_inches='tight')

    def make_dendrogram(self, cluster_info_df, target_k, curr_out_dir):
        print('Generating dendrogram')

        cluster_color_hex = cluster_info_df[f'Cluster_color_rgb_{target_k}'].apply(
            lambda rgb_tuple: mpl.colors.rgb2hex([x / 255. for x in rgb_tuple]))
        Z = linkage(cluster_info_df[[str(x) for x in range(1, self.feature_extractor.num_features + 1)]], 'ward')

        # NOTE: THIS IS FOR MAKING DENDROGRAM COLORS MATCH THE COLORTILE SLIDE
        link_cols = {}
        for i, i12 in enumerate(Z[:, :2].astype(int)):
            c1, c2 = (link_cols[x] if x > len(Z) else cluster_color_hex.loc[x]
                      for x in i12)
            link_cols[i + 1 + len(Z)] = c1 if c1 == c2 else '#0000FF'

        plt.close('all')
        plt.title('Hierarchical Clustering Dendrogram')
        plt.ylabel('distance')

        dendrogram(
            Z,
            no_labels=True,
            color_threshold=None,
            link_color_func=lambda x: link_cols[x]
        )

        sp = os.path.join(curr_out_dir, 'k{}_dendrogram.jpg'.format(target_k))
        plt.savefig(sp, dpi=200, bbox_inches='tight')






if __name__ == '__main__':
    import time

    start = time.time()

    # Default config values
    config = HAVOCConfig(
        # out_dir=r'C:\Users\Shadow\Desktop\new_havoc_testing\jaja2',
        # out_dir=r'C:\Users\Shadow\Desktop\new_havoc_testing\2',
        out_dir=r'C:\Users\Shadow\Desktop\new_havoc_testing\small_ki67_svs',
        k_vals=[7, 8, 9],
        # k_vals=[],
        save_tiles_k_vals=[],

        tile_size=512,

        min_tissue_amt=0.2,

        extra_metrics=[],#'tsne', 'dendrogram', 'corr_clustmap']

        dev=DeveloperOptions(save_and_keep_tmp_tiles=False, save_parquet=True, map_scale_fac=32)
    )

    from general_utility.slide import Slide
    from huggingface_hub import login

    login(token='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')

    s = Slide(r'C:\Users\Shadow\Desktop\new_havoc_testing\small_ki67_svs\SmallTestSVS.svs')
    # s = Slide(r'C:\Users\Shadow\Desktop\new_havoc_testing\2\2019VAL380.svs')

    havoc = HAVOC(config)
    havoc.run(s)
    #
    #
    # import glob
    # for fp in glob.glob(os.path.join(r'C:\Users\Shadow\Desktop\new_havoc_testing\jaja2\*')):
    #     s = Slide(fp)
    #     havoc.run(s)
