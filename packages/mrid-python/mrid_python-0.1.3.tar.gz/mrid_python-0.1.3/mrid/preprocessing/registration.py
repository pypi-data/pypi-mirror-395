from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any

import numpy as np
import SimpleITK as sitk

from ..loading.convert import tositk, ImageLike

def resample_to(input: ImageLike, to: ImageLike, interpolation=sitk.sitkNearestNeighbor) -> sitk.Image:
    """Resample ``input`` to ``reference``.

    Resampling uses spatial information embedded in the sitk.Image - size, origin, spacing and direction.

    Note that this information is only available when certain imaging formats are loaded, such as DICOM and NIfTI.

    ``input`` is transformed in such a way that those attributes will match ``reference``.
    """
    return sitk.Resample(tositk(input), tositk(to), sitk.Transform(), interpolation)


def _default_pmap():
    """Default parameter maps for registration"""
    euler = sitk.GetDefaultParameterMap('translation')
    euler['Transform'] = ['EulerTransform']
    pmap = sitk.VectorOfParameterMap()
    pmap.append(sitk.GetDefaultParameterMap("translation"))
    pmap.append(euler)
    pmap.append(sitk.GetDefaultParameterMap("rigid"))
    pmap.append(sitk.GetDefaultParameterMap("affine"))
    return pmap

class Registration:
    """Class for image registration.

    Args:
        pmap (Any, optional): parameter map, if None, uses default parameter map. Defaults to None.
        log_to_console (bool, optional): if False, disables SimpleElastix logging a lot of stuff to your console. Defaults to False.
    """
    def __init__(self, pmap: Any = None, log_to_console=False):
        if pmap is None: pmap = _default_pmap()
        self.pmap: sitk.VectorOfParameterMap = pmap
        self.log_to_console = log_to_console

        # create elastix filter
        self.elastix = sitk.ElastixImageFilter()
        if log_to_console: self.elastix.LogToConsoleOn()
        else: self.elastix.LogToConsoleOff()

        self.elastix.SetParameterMap(self.pmap)

        self._moving = None
        self._transformed = None
        self.inverse: "Registration | None" = None

    def find_transform(self, input: ImageLike, to: ImageLike) -> sitk.Image:
        """Find a transform that transforms ``input`` to ``to`` and save it to this ``Registration`` object.
        Returns ``input`` registered to ``to``.

        Args:
            input (ImageLike): Moving image.
            to (ImageLike): Fixed image.
        """
        if self._transformed is not None:
            raise RuntimeError("`find_transform` has already been called on this Registration object.")
        self._moving = tositk(input)
        to = tositk(to)

        self.elastix.SetFixedImage(to)
        self.elastix.SetMovingImage(self._moving)
        self.elastix.Execute()

        self._transformed = self.elastix.GetResultImage()
        return self.elastix.GetResultImage() # return copy

    def apply_transform(self, input: ImageLike, use_nearest_interpolation: bool = False) -> sitk.Image:
        """Applies transform stored in this ``Registration`` object to ``input``.

        You have to use ``find_transform`` method first to find the transform.

        Args:
            input (ImageLike): Moving image to apply transform to.
            use_nearest_interpolation (bool, optional):
                whether to use nearest interpolation, enable when transforming segmentations. Defaults to False.

        Returns:
            sitk.Image: transformed ``input``.
        """
        if self._transformed is None:
            raise RuntimeError("First find transform parameters using `find_transform` method.")

        transform = sitk.TransformixImageFilter()
        tmap = self.elastix.GetTransformParameterMap()
        if use_nearest_interpolation:
            for t in tmap:
                t["ResampleInterpolator"] = ["FinalNearestNeighborInterpolator"]

        transform.SetTransformParameterMap(tmap)
        transform.SetMovingImage(input)
        if not self.log_to_console: transform.LogToConsoleOff()

        return transform.Execute()

    def apply_inverse_transform(self, input: ImageLike, use_nearest_interpolation: bool = False) -> sitk.Image:
        """Applies inverse of the transform stored in this ``Registration`` object to ``input``.

        This is done by finding another transform that undoes the current one. Note that this may not be as robust as
        using other tools like freesurfer (because in SimpleElastix transform inverse is not implemented, and
        "DisplacementMagnitudePenalty" metric is not included in python build).

        Args:
            input (ImageLike): input image to apply inverse transform to.
            use_nearest_interpolation (bool, optional):
                whether to use nearest interpolation, enable when transforming segmentations. Defaults to False.
        """
        if self.inverse is None:
            if (self._transformed is None) or (self._moving is None):
                raise RuntimeError("First find transform parameters using `find_transform` method.")
            inverse_pmap = self.elastix.GetParameterMap() # this returns a copy
            # for p in inverse_pmap:
            #     p["Metric"] = "MeanSquaredDifference" # not implemented
            self.inverse = Registration(pmap=inverse_pmap, log_to_console=self.log_to_console)
            self.inverse.find_transform(
                input=self._transformed,
                to=self._moving
            )

        return self.inverse.apply_transform(input, use_nearest_interpolation=use_nearest_interpolation)


def register(input: ImageLike, to: ImageLike, pmap: Any = None, log_to_console=False):
    """Register ``input`` to ``reference``. Returns ``input`` with the same shape and spatial position as ``reference``

    Registering means finding a transform which alligns ``input`` to match with ``reference``,
    it will have the same size, orientation, etc. By default this used affine transform.

    This uses ``SimpleITK-SimpleElastix`` which is very robust.
    Note that if you don't have it installed, you need to uninstall normal SimpleITK
    and install https://pypi.org/project/SimpleITK-SimpleElastix/, don't worry, it's
    the same as SimpleITK but it additionally includes SimpleElastix.
    """
    reg = Registration(pmap=pmap, log_to_console=log_to_console)
    return reg.find_transform(input=input, to=to)


def register_D(
    images: Mapping[str, ImageLike],
    key: str,
    to: ImageLike,
    pmap: Any = None,
    log_to_console=False,
) -> dict[str, sitk.Image]:
    """Register ``images[key]`` to ``reference``, then use that transformation
    to transform other values in ``images`` that are assumed to be aligned with ``images[key]`` (e.g. segmentation).

    Make sure segmentation with hard edges is under a key that starts with ``"seg"``,
    it will use nearest neighbour interpolation, otherwise it will mess up the edges.
    """
    reg = Registration(pmap=pmap, log_to_console=log_to_console)
    registered = {key: reg.find_transform(images[key], to)}

    # process segs last because it sets resample interpolator to nearest
    for k,v in sorted(list(images.items()), key = lambda x: 1 if x[0].startswith('seg') else 0):
        if k != key:
            use_nearest_interpolation = k.startswith('seg')
            registered[k] = reg.apply_transform(v, use_nearest_interpolation=use_nearest_interpolation)

    return registered

def register_each(
    images: Mapping[str, ImageLike],
    key: str,
    to: ImageLike,
    pmap: Any = None,
    log_to_console=False,
) -> dict[str, sitk.Image]:
    """Register ``images[key]`` to ``reference``, then register all other values in ``images`` to registered ``images[key]``.

    Use this when you have multiple modalities that do not align."""
    images = {k: tositk(v) for k,v in images.items()}
    to = tositk(to)

    input = images[key]
    input_reg = register(input=input, to=to, pmap=pmap, log_to_console=log_to_console)

    registered = {key: input_reg}
    for k,v in images.items():
        if k != key:
            registered[k] = register(input=v, to=input_reg, pmap=pmap, log_to_console=log_to_console)

    return registered

def resize(img: ImageLike, new_size: Sequence[int], interpolator=sitk.sitkLinear) -> sitk.Image:
    """Resize ``sitk.Image`` to ``new_size``. Retains correct spatial information.
    source: https://gist.github.com/lixinqi98/1bbd3596492f20b776fed2778f7cd48c"""
    img = tositk(img)
    new_size = list(reversed(new_size))

    # img = sitk.ReadImage(img)
    dimension = img.GetDimension()

    # Physical image size corresponds to the largest physical size in the training set, or any other arbitrary size.
    reference_physical_size = np.zeros(dimension)

    reference_physical_size[:] = [(sz - 1) * spc if sz * spc > mx else mx for sz, spc, mx in
                                  zip(img.GetSize(), img.GetSpacing(), reference_physical_size)]

    # Create the reference image with a zero origin, identity direction cosine matrix and dimension
    reference_origin = np.zeros(dimension)
    reference_direction = np.identity(dimension).flatten()
    reference_size = new_size
    reference_spacing = [phys_sz / (sz - 1) for sz, phys_sz in zip(reference_size, reference_physical_size)]

    reference_image = sitk.Image(reference_size, img.GetPixelIDValue())
    reference_image.SetOrigin(reference_origin)
    reference_image.SetSpacing(reference_spacing)
    reference_image.SetDirection(reference_direction)

    # Always use the TransformContinuousIndexToPhysicalPoint to compute an indexed point's physical coordinates as
    # this takes into account size, spacing and direction cosines. For the vast majority of images the direction
    # cosines are the identity matrix, but when this isn't the case simply multiplying the central index by the
    # spacing will not yield the correct coordinates resulting in a long debugging session.
    reference_center = np.array(
        reference_image.TransformContinuousIndexToPhysicalPoint(np.array(reference_image.GetSize()) / 2.0))

    # Transform which maps from the reference_image to the current img with the translation mapping the image
    # origins to each other.
    transform = sitk.AffineTransform(dimension)
    transform.SetMatrix(img.GetDirection())
    transform.SetTranslation(np.array(img.GetOrigin()) - reference_origin)
    # Modify the transformation to align the centers of the original and reference image instead of their origins.
    centering_transform = sitk.TranslationTransform(dimension)
    img_center = np.array(img.TransformContinuousIndexToPhysicalPoint(np.array(img.GetSize()) / 2.0))
    centering_transform.SetOffset(np.array(transform.GetInverse().TransformPoint(img_center) - reference_center))

    # centered_transform = sitk.Transform(transform)
    # centered_transform.AddTransform(centering_transform)

    centered_transform = sitk.CompositeTransform([transform, centering_transform])

    # Using the linear interpolator as these are intensity images, if there is a need to resample a ground truth
    # segmentation then the segmentation image should be resampled using the NearestNeighbor interpolator so that
    # no new labels are introduced.

    return sitk.Resample(img, reference_image, centered_transform, interpolator, 0.0)

def downsample(image:ImageLike, factor:float, dims: Sequence[int] | None, interpolator=sitk.sitkLinear) -> sitk.Image:
    """factor = 2 for 2x downsampling"""
    image = tositk(image)
    size = sitk.GetArrayFromImage(image).shape
    size = [round(s/factor) if (dims is None or i in dims) else s for i,s in enumerate(size)]
    return resize(image, size, interpolator=interpolator)