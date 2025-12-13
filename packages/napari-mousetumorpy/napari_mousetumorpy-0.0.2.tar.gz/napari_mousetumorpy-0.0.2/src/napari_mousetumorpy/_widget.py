from mousetumorpy import (
    LungsPredictor,
    TumorPredictor,
    NNUNET_MODELS,
    YOLO_MODELS,
    run_tracking,
    generate_tracked_tumors,
)

import imaging_server_kit as sk
import numpy as np


@sk.algorithm(
    name="Tumor tracking",
    parameters={
        "tumor_series": sk.Mask(name="Tumor series"),
        "lungs_series": sk.Mask(name="Lungs series"),
        "image_series": sk.Image(name="Image series", required=False),
        "max_dist_px": sk.Integer(
            name="Max dist.",
            description="Distance cutoff (in pixels) for object tracking between consecutive frames",
            min=0,
            default=30,
        ),
        "memory": sk.Integer(
            name="Memory",
            description="Maximum number of frames skipped during tracking.",
            default=0,
            min=0,
        ),
        "dist_weight_ratio": sk.Float(
            name="Dist/Vol weighing",
            description="Relative importance given to preserving object positions or their volume for linking between consecutive frames.",
            min=0,
            max=1,
            step=0.05,
            default=0.9,
        ),
        "max_volume_diff_rel": sk.Float(
            name="Max vol. diff.",
            description="Maximum allowed relative volume difference between tracked objects in consecutive frames. 1.0 means objects can double in size between two frames (100% volume increase/decrease)",
            default=1.0,
            min=0.0,
        ),
    },
    tileable=False,
)
def sk_tracking(
    tumor_series,
    lungs_series,
    image_series,
    max_dist_px,
    memory,
    dist_weight_ratio,
    max_volume_diff_rel,
):
    linkage_df = run_tracking(
        tumor_timeseries=tumor_series,
        lungs_timeseries=lungs_series,
        image_timeseries=image_series,
        method="laptrack",
        max_dist_px=max_dist_px,
        with_lungs_registration=True,
        memory=memory,
        dist_weight_ratio=dist_weight_ratio,
        max_volume_diff_rel=max_volume_diff_rel,
        skip_level=8,
        remove_partially_tracked=False,
    )

    tracked_labels_timeseries = generate_tracked_tumors(tumor_series, linkage_df)

    n_tracked_tumors = len(linkage_df["tumor"].unique().tolist())

    if n_tracked_tumors == 0:
        return sk.Notification("No tumors tracked")
    elif tracked_labels_timeseries is None:
        return sk.Notification("Tracked tumors are None", meta={"level": "warning"})

    return (
        sk.Mask(tracked_labels_timeseries, name="Tracked tumors"),
        f"{n_tracked_tumors} tumors tracked",
    )


@sk.algorithm(
    name="Lungs segmentation",
    parameters={
        "image": sk.Image(
            name="Image", description="Raw CT scan image (3D).", dimensionality=[3]
        ),
        "model": sk.Choice(name="Model", items=list(YOLO_MODELS.keys())),
    },
    tileable=False,
)
def sk_lungs_seg(image, model):
    predictor = LungsPredictor(model)
    roi, mask = predictor.compute_3d_roi(image)
    return sk.Image(roi, name="Image (ROI)"), sk.Mask(mask, name="Lungs (ROI)")


@sk.algorithm(
    name="Tumor segmentation",
    parameters={
        "image": sk.Image(
            name="Image",
            description="CT scan ROI image (3D) or series (3D+t).",
            dimensionality=[3, 4],
        ),
        "model": sk.Choice(name="Model", items=list(NNUNET_MODELS.keys())),
    },
    tileable=False,
)
def sk_tumor_seg(image, model):
    predictor = TumorPredictor(model)
    if image.ndim == 3:
        mask = predictor.predict(image)
        return sk.Mask(mask)
    elif image.ndim == 4:
        mask = np.zeros(image.shape, dtype=np.uint16)
        for k, scan in enumerate(image):  # Assuming the first dimension is T
            mask[k] = predictor.predict(scan)
            yield sk.Mask(mask)  # Progressively output the segmentation masks
    else:
        return sk.Notification(
            f"Images of dimensionality {image.ndim} are not supported.",
            meta={"level": "warning"},
        )
