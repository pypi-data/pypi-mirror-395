import os
import pickle
import shutil
import tempfile
import warnings
from collections import UserDict
from collections.abc import Callable, Mapping, Sequence
from functools import partial
from typing import TYPE_CHECKING, Any, Literal, overload

import numpy as np
import SimpleITK as sitk

from . import preprocessing
from .loading.convert import ImageLike, tonumpy, tositk, totensor
from .utils.torch_utils import CUDA_IF_AVAILABLE

if TYPE_CHECKING:
    import torch

def _identity(x): return x

class Study(UserDict[str, sitk.Image | Any]):
    @overload
    def __init__(self, /, **kwargs): ...
    @overload
    def __init__(self, dict, /): ...
    def __init__(self, dict=None, /, **kwargs):
        if dict is None: dict = kwargs

        proc = {}
        for k,v in dict.items():
            if k.startswith("info"):
                proc[k] = v
            else:
                proc[k] = tositk(v)

        super().__init__(proc)

    def __setitem__(self, key: str, item: "ImageLike | Any") -> None:
        if not key.startswith("info"): item = tositk(item)
        return super().__setitem__(key, item)

    def add(self, key: str, item: "ImageLike | Any", reference_key: str | None = None):
        """Returns a new study with an extra item inserted under ``key``.

        Args:
            key (str): Key to insert new item under.
            item (ImageLike | Any): Item to insert.
            reference_key (str | None, optional):
                if specified, ``item`` will have SimpleITK attributes copied from ``self[reference_key]``. Defaults to None.
        """
        study = self.copy()
        if key.startswith('info'):
            if reference_key: raise RuntimeError(f"Can't copy sitk attributes for an non-image item {key}")
            study[key] = item
            return study

        item = tositk(item)
        if reference_key is not None: item.CopyInformation(study[reference_key])
        study[key] = item
        return study

    def get_scans(self):
        """Returns a new ``Study`` with segmentations and info removed."""
        return self.__class__({k:v for k,v in self.items() if not k.startswith(("seg", "info"))})

    def get_images(self):
        """Returns a new ``Study`` with info removed."""
        return self.__class__({k:v for k,v in self.items() if not k.startswith("info")})

    def get_segmentations(self):
        """Returns a new ``Study`` with scans and info removed."""
        return self.__class__({k:v for k,v in self.items() if k.startswith("seg")})

    def get_info(self):
        """Returns a new ``Study`` with scans and segmentations removed."""
        return self.__class__({k:v for k,v in self.items() if k.startswith("info")})

    def apply(self, fn:Callable[[sitk.Image], sitk.Image] | None, seg_fn: Callable[[sitk.Image], sitk.Image] | None,) -> "Study":
        """Returns a new ``Study`` with ``fn`` applied to scans and ``seg_fn`` applied to segmentations.

        Args:
            fn: Function to apply to scan images. Must take and return ``sitk.Image``.
                If None, identity function is used.
            seg_fn: Function to apply to segmentation images. Must take and return ``sitk.Image``.
                If None, identity function is used.
        """
        if fn is None: fn = _identity
        if seg_fn is None: seg_fn = _identity

        scans = {k: fn(v) for k,v in self.get_scans().items()}
        seg = {k: seg_fn(v) for k,v in self.get_segmentations().items()}

        return Study(**scans, **seg, **self.get_info())

    def cast(self, dtype) -> "Study":
        """Returns a new study with all scans cast to the specified SimpleITK dtype.

        Note:
            This operation does not affect segmentations.
        """
        return self.apply(partial(sitk.Cast, pixelID=dtype), seg_fn=None)

    def cast_float64(self) -> "Study":
        """Returns a new study with all scans cast to float64.

        Note:
            This operation does not affect segmentations.
        """
        return self.cast(sitk.sitkFloat64)

    def cast_float32(self) -> "Study":
        """Returns a new study with all scans cast to float32.

        Note:
            This operation does not affect segmentations.
        """
        return self.cast(sitk.sitkFloat32)

    def normalize(self) -> "Study":
        """Return a new study where all scans are separately z-normalized to 0 mean and 1 variance.

        Note:
            This operation does not affect segmentations.
        """
        return self.apply(sitk.Normalize, seg_fn=None)

    def rescale_intensity(self, min: float, max: float) -> "Study":
        """Return a new study where all scans are separately rescaled to the specified intensity range.

        Args:
            min: Minimum value for the output intensity range.
            max: Maximum value for the output intensity range.
        """
        return self.apply(partial(sitk.RescaleIntensity, outputMinimum = min, outputMaximum = max), seg_fn=None) # type:ignore

    def crop_bg(self, key: str) -> "Study":
        """Return a new study with cropped black background. Finds the foreground bounding box of ``study[key]``,
        and uses that bounding box to crop all other images, including segmentations.

        Args:
            key: The key of the image to use for finding the foreground bounding box.
        """
        d = preprocessing.cropping.crop_bg_D(self.get_images(), key)
        return Study(**d, **self.get_info())

    def skullstrip(
        self,
        key: str,
        register_to_mni152: Literal["T1", "T2"] | None = None,
        device: Literal["cpu", "cuda", "mps"] = CUDA_IF_AVAILABLE,
        disable_tta: bool = False,
        verbose: bool = False,
    ) -> "Study":
        """Predicts brain mask of ``study[key]``, then uses this mask to skull strip all scans. Doesn't affect segmentations.

        Args:
            key: Key of the image to pass to HD-BET for brain mask prediction.
            register_to_mni152: Should be ``"T1"``, ``"T2"`` or ``None``.
                If specified, ``input`` will be registered to specified MNI152 template,
                and brain mask registered back to original ``input``.
                Note that HD-BET expects images to be in MNI152 space. Defaults to None.
            device: Used to set on which device the prediction will run. Can be 'cuda' (=GPU), 'cpu' or 'mps'.
                Defaults to CUDA_IF_AVAILABLE.
            disable_tta: Set this flag to disable test time augmentation. This will make prediction faster
                at a slight decrease in prediction quality. Recommended for device cpu. Defaults to False.
            verbose: Enable verbose output during processing. Defaults to False.
        """
        d = preprocessing.skullstripping.skullstrip_D(
            images=self.get_scans(),
            key=key,
            register_to_mni152=register_to_mni152,
            device=device,
            disable_tta=disable_tta,
            verbose=verbose,
        )
        return Study(**d, **self.get_segmentations(), **self.get_info())

    def resize(self, size: Sequence[int], interpolator=sitk.sitkLinear):
        """Resize all images to ``size``.

        Args:
            size: Target size as a sequence of integers (e.g., [height, width, depth]).
            interpolator: Interpolation method for regular images (segmentations always use nearest neighbor).
        """
        return self.apply(
            partial(preprocessing.registration.resize, new_size=size, interpolator=interpolator,),
            partial(preprocessing.registration.resize, new_size=size, interpolator=sitk.sitkNearestNeighbor,),
        )

    def downsample(self, factor: float, dims = None, interpolator=sitk.sitkLinear):
        """Downsample all images. Factor = 2 for 2x downsampling. Dims ``None`` for all dims.

        Args:
            factor: Downsampling factor (e.g., 2 for 2x downsampling).
            dims: Specific dimensions to downsample, or None for all dimensions.
            interpolator: Interpolation method for regular images (segmentations always use nearest neighbor).
        """
        return self.apply(
            partial(preprocessing.registration.downsample, factor=factor, dims=dims, interpolator=interpolator,),
            partial(preprocessing.registration.downsample, factor=factor, dims=dims, interpolator=sitk.sitkNearestNeighbor,),
        )

    def register(self, key: str, to: ImageLike, pmap=None, log_to_console=False) -> "Study":
        """Returns a new Study, registers ``study[key]`` to ``to``,
        and use transformation parameters to register all other images including segmentation.
        This assumes that all images are in the same space, if they are not, use ``register_many`` method.

        Args:
            key: The key of the image to use as reference for registration.
            to: Target image or path to register to.
            pmap: Parameter map for registration. If None, uses default parameters.
            log_to_console: Whether to log registration progress to console.
        """
        d = preprocessing.registration.register_D(
            images=self.get_images(),
            key=key,
            to=to,
            pmap=pmap,
            log_to_console=log_to_console,
        )
        return Study(**d, **self.get_info())

    def register_each(self, key: str, to: "ImageLike | None" = None, pmap=None, log_to_console=False) -> "Study":
        """Returns a new study. Registers all other images to ``study[key]``.
        If ``to`` is specified, register ``study[key]`` to ``to`` beforehand.

        Args:
            key: The key of the image to use as reference for registration.
            to: Target image or path to register the reference image to. If None, uses key as reference.
            pmap: Parameter map for registration. If None, uses default parameters.
            log_to_console: Whether to log registration progress to console.

        Note:
            If called on a study with segmentations, they will be removed from the returned study.
        """
        if len(self.get_segmentations()) > 0:
            keys = ', '.join(self.get_segmentations().keys())
            warnings.warn(f"`register_many` was called on a study with segmentations ({keys}), "
                          "they will be removed from the returned study", stacklevel=3)

        d = self.get_scans()
        if to is not None:
            d[key] = preprocessing.registration.register(d[key], to=to, pmap=pmap, log_to_console=log_to_console)

        for k in d:
            if k != key:
                d[k] = preprocessing.registration.register(d[k], to=d[key], pmap=pmap, log_to_console=log_to_console)

        return Study(**d, **self.get_info())

    def resample_to(self, to: "np.ndarray | sitk.Image | torch.Tensor | str", interpolation=sitk.sitkLinear) -> "Study":
        """Returns a new study, resamples all images including segmentation to `to`.
        Segmentation always uses nearest interpolation"""
        to = tositk(to)

        return self.apply(
            partial(preprocessing.registration.resample_to, to=to, interpolation=interpolation),
            partial(preprocessing.registration.resample_to, to=to, interpolation=sitk.sitkNearestNeighbor),
        )

    def n4_bias_field_correction(self, key: str, shrink: int = 4) -> "Study":
        """Returns a new study with corrected bias field of the image under ``key``. Doesn't affect other images.

        Args:
            key: The key of the image for which to correct the bias field.
            shrink: By how many times to shrink the size of input image for calculating the bias field.
                The bias field is then applied to original size (unshrunk) image.
                Setting shrink to 1 disables it, but n4 algorithm may take several minutes.
                Setting it to ~4 is good enough in most cases and will be significantly faster (usually few seconds).
        """
        new = self.copy()
        new[key] = preprocessing.bias_field_correction.n4_bias_field_correction(new[key], shrink=shrink)
        return new

    def numpy(self, key: str):
        """returns ``study[key]`` converted to a numpy array."""
        return tonumpy(self[key])

    def tensor(self, key: str):
        """returns ``study[key]`` converted to a tensor."""
        return totensor(self[key])

    def _get_sorted_items(self, scans: bool, seg: bool, order: Sequence[str] | None = None) -> list[tuple[str, sitk.Image]]:
        if not (scans or seg): raise ValueError("At least one of `scans` or `seg` must be True")

        if order is not None:
            return [(k, self[k]) for k in order]

        # make sure items are always sorted in the same order
        items = []
        if scans: items = sorted(self.get_scans().items(), key = lambda x: x[0])
        if seg: items.extend(sorted(self.get_segmentations().items(), key = lambda x: x[0]))
        return items


    def stack_numpy(self, scans:bool = True, seg: bool = False, dtype=None, order: Sequence[str] | None = None) -> np.ndarray:
        """Stack images into a numpy array, returns an array of shape ``(n_images, *dims)``.

        Args:
            scans: Whether to include scan images in the stack.
            seg: Whether to include segmentation images in the stack.
            dtype: Data type for the output array. If None, uses the default type.
            order:
                Specific order for the images in the stack. If specified, ignores ``scans`` and ``seg`` options.
                If None, uses alphabetic sorting.
        """
        items = self._get_sorted_items(scans=scans, seg=seg, order=order)

        stacked = np.array([sitk.GetArrayFromImage(v) for k, v in items])
        if dtype is not None: stacked = stacked.astype(dtype, copy=False)
        return stacked

    def stack_tensor(self, scans:bool = True, seg: bool = False, device=None, dtype=None, order: Sequence[str] | None = None) -> "torch.Tensor":
        """Stack images into a torch tensor, returns an tensor of shape ``(n_images, *dims)``.

        Args:
            scans: Whether to include scan images in the stack.
            seg: Whether to include segmentation images in the stack.
            device: Device for the output tensor. If None, uses the default device.
            dtype: Data type for the output tensor. If None, uses the default type.
            order:
                Specific order for the images in the stack. If specified, ignores ``scans`` and ``seg`` options.
                If None, uses alphabetic sorting.
        """
        import torch
        items = self._get_sorted_items(scans=scans, seg=seg, order=order)
        stacked = torch.stack([torch.from_numpy(sitk.GetArrayFromImage(v)) for _,v in items])
        return stacked.to(device=device, dtype=dtype, memory_format=torch.contiguous_format)

    def numpy_dict(self) -> dict[str, np.ndarray | Any]:
        """Returns a dictionary with all images converted to numpy arrays, info is included as is."""
        return {k: (sitk.GetArrayFromImage(v) if isinstance(v, sitk.Image) else v) for k, v in self.items()}

    def tensor_dict(self) -> "dict[str, torch.Tensor | Any]":
        """Returns a dictionary with all images converted to tensors, info is included as is."""
        import torch
        return {k: (torch.from_numpy(v) if isinstance(v, np.ndarray) else v) for k,v in self.numpy_dict()}

    def plot(self):
        from .utils.plotting import visualize_3d_arrays
        visualize_3d_arrays(self.get_images().numpy_dict())

    def save(
        self,
        dir: str | os.PathLike,
        prefix: str = "",
        suffix: str = "",
        ext: str = "nii.gz",
        mkdir=True,
        use_compression=True,
        pickle_module = pickle,
    ):
        """Writes this study to a directory, with filenames being ``{path}/{prefix}{key}{suffix}.{ext}``

        Args:
            dir: Directory to save the study to.
            prefix: Prefix to add to all filenames.
            suffix: Suffix to add to all filenames (before extension).
            ext: File extension for image files. Default is 'nii.gz'.
            mkdir: Whether to create the directory if it doesn't exist. Default is True.
            use_compression: Whether to use compression for image files. Default is True.
            pickle_module: Module to use for pickling info objects. Default is pickle.
        """
        if ext.startswith('.'): ext = ext[1:]

        # make directory
        if not os.path.exists(dir):
            if mkdir: os.mkdir(dir)
            else: raise FileNotFoundError(f"Directory {dir} doesn't exist and {mkdir = }")

        # save
        for k,v in self.items():

            # save infos
            if k.startswith('info'):
                try:
                    with open(os.path.join(dir, f"{prefix}{k}{suffix}.pkl"), "wb") as file:
                        pickle_module.dump(v, file)

                except Exception as e:
                    print(f"Couldn't save {k}:\n{e!r}")

            # save images
            else:
                # this handles non ascii chars
                with tempfile.TemporaryDirectory() as temp_path:
                    sitk.WriteImage(v, os.path.join(temp_path, f"{prefix}{k}{suffix}.{ext}"), useCompression=use_compression)
                    shutil.move(os.path.join(temp_path, f"{prefix}{k}{suffix}.{ext}"), dir)

    def load(self, dir: str | os.PathLike, prefix: str = '', suffix: str = '', ext: str = 'nii.gz', pickle_module = pickle):
        """Returns a new study, updated by data loaded from ``dir``, which can be created by calling ``study.save(dir)``.

        Args:
            dir: Directory to load the study from.
            prefix: Expected prefix of filenames.
            suffix: Expected suffix of filenames.
            ext: Expected file extension for image files. Default is 'nii.gz'.
            pickle_module: Module used for unpickling info objects. Default is pickle.
        """
        study = self.copy()

        files = os.listdir(dir)

        for f in files:
            full = os.path.join(dir, f)
            name:str = f

            # check prefix
            if prefix == '' or name.startswith(prefix):
                name = name[len(prefix):]

                # load images
                if name.endswith(f'{suffix}.{ext}'):
                    name = name[:-len(f'{suffix}.{ext}')]
                    study[name] = tositk(full)

                # load infos
                elif name.endswith(f'{suffix}.pkl'):
                    name = name[:-len(f'{suffix}.pkl')]

                    try:
                        with open(full, 'rb') as file:
                            study[name] = pickle_module.load(file)
                    except Exception as e:
                        print(f"Couldn't load {full}:\n{e!r}")

        return study

    @classmethod
    def from_dir(cls, dir: str | os.PathLike, prefix: str = '', suffix: str = '', ext: str = 'nii.gz', pickle_module = pickle):
        """Load a study from a directory.

        Args:
            dir: Directory to load the study from.
            prefix: Expected prefix of filenames.
            suffix: Expected suffix of filenames.
            ext: Expected file extension for image files. Default is 'nii.gz'.
            pickle_module: Module used for unpickling info objects. Default is pickle.
        """
        return cls().load(dir=dir, prefix=prefix, suffix=suffix, ext=ext, pickle_module=pickle_module)