import numpy as np
import cv2
import torch
import timm
from torchvision import transforms
from PIL import Image


class FeatureExtractor:
    def __init__(self, device=None):

        print("Loading feature extractor (prov-gigapath)...")

        # --- Device ---
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        # --- Model ---
        # Executing the first time creates a local cache of the model
        self.model = timm.create_model(
            model_name='hf_hub:prov-gigapath/prov-gigapath',
            pretrained=True,
        ).to(self.device).eval()

        self.num_features = self.model.num_features

        # --- Preprocessing pipeline ---
        self.preprocess = transforms.Compose([
            transforms.Resize(256, interpolation=transforms.InterpolationMode.BICUBIC),
            transforms.CenterCrop(224),
            transforms.ToTensor(),  # converts to [0,1] and CHW
            transforms.Normalize(
                mean=(0.485, 0.456, 0.406),
                std=(0.229, 0.224, 0.225),
            ),
        ])

        print("Finished loading feature extractor")

    def _sliding_window_sampling(self, batch, patch_size, stride):
        """
        For any tile, regardless of its size, sample multiple 256×256@20× patches using a sliding window with a chosen stride.

        - Every tile is consistently represented by one aggregated embedding, no matter its raw pixel dimensions.
        - The field-of-view is always 20× at 256 size, matching foundation model pretraining.
        - Context captured through multiple patches, even if tile is awkwardly sized.

        batch: (N, H, W, 3) BGR uint8 tiles.
        Returns:
            patches: (M, patch_size, patch_size, 3)
            tile_ids: (M,) array mapping each patch -> original tile index in [0, N-1]
        """

        if batch.ndim != 4 or batch.shape[-1] != 3:
            raise ValueError(f"Expected batch shape (N, H, W, 3), got {batch.shape}")

        all_patches = []
        tile_ids = []

        N = batch.shape[0]

        for i in range(N):
            img = batch[i]
            H, W = img.shape[:2]

            if H < patch_size or W < patch_size:
                raise ValueError(
                    f"Tile {i} is smaller than patch_size={patch_size}: got ({H}, {W})"
                )

            # starting positions for sliding window
            ys = list(range(0, H - patch_size + 1, stride))
            xs = list(range(0, W - patch_size + 1, stride))

            # ensure we cover the bottom/right borders
            if ys[-1] != H - patch_size:
                ys.append(H - patch_size)
            if xs[-1] != W - patch_size:
                xs.append(W - patch_size)

            for y in ys:
                for x in xs:
                    patch = img[y:y + patch_size, x:x + patch_size, :]
                    all_patches.append(patch)
                    tile_ids.append(i)

        patches = np.stack(all_patches, axis=0)  # (M, patch_size, patch_size, 3)
        tile_ids = np.array(tile_ids, dtype=np.int64)  # (M,)
        return patches, tile_ids

    def _grid_sampling(
            self,
            batch: np.ndarray,
            patch_size=256,
            num_patches=4,
            fast=False,
    ):
        """
        Adaptive grid sampling.

        - Every tile is consistently represented by one aggregated embedding, no matter its raw pixel dimensions.
        - The field-of-view is always 20× at 256 size, matching foundation model pretraining.
        - Context captured through multiple patches, even if tile is awkwardly sized.

        batch: (N, H, W, 3) BGR uint8 tiles.
        Returns:
            patches: (M, patch_size, patch_size, 3)
            tile_ids: (M,) mapping each patch -> original tile index

        Modes:
          - fast=True:
              Always take a single center crop (256x256) per tile.
          - fast=False:
              Use adaptive grid:
                * 1 center crop if tile is < 1.5 * patch_size in either dimension
                * otherwise 2x2 grid (up to num_patches crops)
        """
        if batch.ndim != 4 or batch.shape[-1] != 3:
            raise ValueError(f"Expected batch shape (N, H, W, 3), got {batch.shape}")

        all_patches = []
        tile_ids = []

        N = batch.shape[0]

        for i in range(N):
            img = batch[i]
            H, W = img.shape[:2]

            if H < patch_size or W < patch_size:
                # too small: just one center crop (same for fast / non-fast)
                y0 = max(0, (H - patch_size) // 2)
                x0 = max(0, (W - patch_size) // 2)
                # clamp just in case
                y0 = max(0, min(y0, H - patch_size))
                x0 = max(0, min(x0, W - patch_size))
                patch = img[y0:y0 + patch_size, x0:x0 + patch_size, :]
                all_patches.append(patch)
                tile_ids.append(i)
                continue

            # ---------- FAST MODE: single center crop ----------
            if fast:
                cy = H // 2
                cx = W // 2
                y0 = cy - patch_size // 2
                x0 = cx - patch_size // 2

                y0 = max(0, min(y0, H - patch_size))
                x0 = max(0, min(x0, W - patch_size))

                patch = img[y0:y0 + patch_size, x0:x0 + patch_size, :]
                all_patches.append(patch)
                tile_ids.append(i)
                continue

            # ---------- NORMAL MODE: adaptive grid ----------
            # decide how many patches for this tile
            if H < 1.5 * patch_size or W < 1.5 * patch_size:
                k = 1  # tile not much bigger than patch -> just 1 crop
                grid = [(0.5, 0.5)]  # center
            else:
                k = num_patches
                # assume num_patches == 4 → 2x2 grid
                # relative centers (row, col) in [0,1]
                grid = [
                           (0.25, 0.25),
                           (0.25, 0.75),
                           (0.75, 0.25),
                           (0.75, 0.75),
                       ][:k]

            for (ry, rx) in grid:
                cy = int(ry * H)
                cx = int(rx * W)

                y0 = cy - patch_size // 2
                x0 = cx - patch_size // 2

                # clamp so patch fits inside the tile
                y0 = max(0, min(y0, H - patch_size))
                x0 = max(0, min(x0, W - patch_size))

                patch = img[y0:y0 + patch_size, x0:x0 + patch_size, :]
                all_patches.append(patch)
                tile_ids.append(i)

        patches = np.stack(all_patches, axis=0)
        tile_ids = np.array(tile_ids, dtype=np.int64)
        return patches, tile_ids

    def _preprocess_batch(self, batch: np.ndarray) -> torch.Tensor:
        """
        batch: numpy array of shape (N, H, W, 3) from cv2.imread,
               i.e. BGR uint8 images.
        """
        # Ensure shape is (N, H, W, 3)
        if batch.ndim != 4 or batch.shape[-1] != 3:
            raise ValueError(f"Expected batch shape (N, H, W, 3), got {batch.shape}")

        tensors = []
        for img_bgr in batch:
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            tensors.append(self.preprocess(pil_img))

        return torch.stack(tensors, dim=0)

    def process(self, batch: np.ndarray, return_numpy=True, patch_size=256, num_patches=4):
        """
        batch: numpy array from cv2 (N, H, W, 3)
        returns: (N, D) feature matrix (numpy or torch tensor)
        """
        if batch is None or len(batch) == 0:
            # Return empty properly-shaped container if you want,
            # but empty list is also fine.
            return np.empty((0, 0), dtype=np.float32) if return_numpy else torch.empty(0, 0)

        if 0:
            # Not practical. Too slow
            patches, tile_ids = self._sliding_window_sampling(
                batch, patch_size=tile_size, stride=stride
            )
        else:
            patches, tile_ids = self._grid_sampling(
                batch,
                patch_size=patch_size,
                num_patches=num_patches
            )

        x = self._preprocess_batch(patches)

        x = x.to(self.device)
        with torch.no_grad():
            patch_feats = self.model(x)
        patch_feats = patch_feats.cpu()

        # Aggregate per original tile (mean pooling)
        M, D = patch_feats.shape
        N = batch.shape[0]

        tile_feats = torch.zeros((N, D), dtype=patch_feats.dtype)
        counts = torch.zeros(N, dtype=torch.long)

        for idx in range(M):
            t = tile_ids[idx]
            tile_feats[t] += patch_feats[idx]
            counts[t] += 1

        # avoid division by zero just in case
        counts = counts.clamp(min=1)
        tile_feats = tile_feats / counts.unsqueeze(1)

        if return_numpy:
            return tile_feats.numpy()
        else:
            return tile_feats
