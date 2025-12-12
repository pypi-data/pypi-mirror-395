# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defining enums for dataset and model formats and types"""

import enum


class DatasetType(str, enum.Enum):
    """Class defining dataset types in enum"""

    maxine_eye_contact = "maxine_eye_contact"
    object_detection = "object_detection"
    segmentation = "segmentation"
    image_classification = "image_classification"
    character_recognition = "character_recognition"
    action_recognition = "action_recognition"
    bevfusion = "bevfusion"
    pointpillars = "pointpillars"
    pose_classification = "pose_classification"
    ml_recog = "ml_recog"
    ocdnet = "ocdnet"
    ocrnet = "ocrnet"
    optical_inspection = "optical_inspection"
    re_identification = "re_identification"
    stylegan_xl = "stylegan_xl"
    sparse4d = "sparse4d"
    visual_changenet_segment = "visual_changenet_segment"
    visual_changenet_classify = "visual_changenet_classify"
    centerpose = "centerpose"
    not_restricted = "not_restricted"
    user_custom = "user_custom"


class DatasetFormat(str, enum.Enum):
    """Class defining dataset formats in enum"""

    kitti = "kitti"
    pascal_voc = "pascal_voc"
    raw = "raw"
    coco_raw = "coco_raw"
    coco_panoptic = "coco_panoptic"
    ovpkl = "ovpkl"
    unet = "unet"
    coco = "coco"
    odvg = "odvg"
    lprnet = "lprnet"
    train = "train"
    test = "test"
    default = "default"
    custom = "custom"
    classification_pyt = "classification_pyt"
    visual_changenet_segment = "visual_changenet_segment"
    visual_changenet_classify = "visual_changenet_classify"
    monai = "monai"


class ExperimentNetworkArch(str, enum.Enum):
    """Class defining network types in enum - matches V2_API_SPECS.json exactly"""

    # Official v2 API network architectures (from V2_API_SPECS.json ExperimentJobReq.network_arch)
    action_recognition = "action_recognition"
    analytics = "analytics"
    annotations = "annotations"
    augmentation = "augmentation"
    auto_label = "auto_label"
    bevfusion = "bevfusion"
    centerpose = "centerpose"
    classification_pyt = "classification_pyt"
    cosmos_rl = "cosmos-rl"
    deformable_detr = "deformable_detr"
    depth_net_mono = "depth_net_mono"
    depth_net_stereo = "depth_net_stereo"
    dino = "dino"
    grounding_dino = "grounding_dino"
    image = "image"
    mae = "mae"
    mal = "mal"
    mask2former = "mask2former"
    mask_grounding_dino = "mask_grounding_dino"
    maxine_eye_contact = "maxine_eye_contact"
    ml_recog = "ml_recog"
    nvdinov2 = "nvdinov2"
    ocdnet = "ocdnet"
    ocrnet = "ocrnet"
    oneformer = "oneformer"
    optical_inspection = "optical_inspection"
    pointpillars = "pointpillars"
    pose_classification = "pose_classification"
    re_identification = "re_identification"
    rtdetr = "rtdetr"
    segformer = "segformer"
    sparse4d = "sparse4d"
    stylegan_xl = "stylegan_xl"
    vila = "vila"
    visual_changenet_classify = "visual_changenet_classify"
    visual_changenet_segment = "visual_changenet_segment"


class Metrics(str, enum.Enum):
    """Class defining metric types in enum"""

    three_d_mAP = "3d mAP"
    AP = "AP"
    AP11 = "AP11"
    AP40 = "AP40"
    AP50 = "AP50"
    AP75 = "AP75"
    APl = "APl"
    APm = "APm"
    APs = "APs"
    ARl = "ARl"
    ARm = "ARm"
    ARmax1 = "ARmax1"
    ARmax10 = "ARmax10"
    ARmax100 = "ARmax100"
    ARs = "ARs"
    bbox_val_mAP = "bbox_val_mAP"
    bbox_val_mAP50 = "bbox_val_mAP50"
    bbox_test_mAP = "bbox_test_mAP"
    bbox_test_mAP50 = "bbox_test_mAP50"
    Hmean = "Hmean"
    Mean_IOU = "Mean IOU"
    Precision = "Precision"
    ema_precision = "ema_precision"
    Recall = "Recall"
    ema_recall = "ema_recall"
    Thresh = "Thresh"
    ACC_all = "ACC_all"
    accuracy = "accuracy"
    m_accuracy = "m_accuracy"
    avg_accuracy = "avg_accuracy"
    accuracy_top_1 = "accuracy_top-1"
    bev_mAP = "bev mAP"
    cmc_rank_1 = "cmc_rank_1"
    cmc_rank_10 = "cmc_rank_10"
    cmc_rank_5 = "cmc_rank_5"
    defect_acc = "defect_acc"
    embedder_base_lr = "embedder_base_lr"
    hmean = "hmean"
    ema_hmean = "ema_hmean"
    learning_rate = "learning_rate"
    loss = "loss"
    lr = "lr"
    matched_ious = "matched_ious"
    mAP = "mAP"
    mAcc = "mAcc"
    mIoU = "mIoU"
    mIoU_large = "mIoU_large"
    mIoU_medium = "mIoU_medium"
    mIoU_small = "mIoU_small"
    param_count = "param_count"
    precision = "precision"
    pruning_ratio = "pruning_ratio"
    recall = "recall"
    recall_rcnn_0_3 = "recall/rcnn_0.3"
    recall_rcnn_0_5 = "recall/rcnn_0.5"
    recall_rcnn_0_7 = "recall/rcnn_0.7"
    recall_roi_0_3 = "recall/roi_0.3"
    recall_roi_0_5 = "recall/roi_0.5"
    recall_roi_0_7 = "recall/roi_0.7"
    size = "size"
    segm_val_mAP = "segm_val_mAP"
    segm_val_mAP50 = "segm_val_mAP50"
    segm_test_mAP = "segm_test_mAP"
    segm_test_mAP50 = "segm_test_mAP50"
    test_Mean_Average_Precision = "test Mean Average Precision"
    test_Mean_Reciprocal_Rank = "test Mean Reciprocal Rank"
    test_Precision_at_Rank_1 = "test Precision at Rank 1"
    test_r_Precision = "test r-Precision"
    fid50k_full = "fid50k_full"
    test_AMI = "test_AMI"
    test_NMI = "test_NMI"
    test_acc = "test_acc"
    test_fnr = "test_fnr"
    test_fpr = "test_fpr"
    test_mAP = "test_mAP"
    test_mAP50 = "test_mAP50"
    test_mf1 = "test_mf1"
    test_miou = "test_miou"
    test_mprecision = "test_mprecision"
    test_mrecall = "test_mrecall"
    top_k = "top_k"
    train_acc = "train_acc"
    train_accuracy = "train_accuracy"
    train_fpr = "train_fpr"
    train_loss = "train_loss"
    trunk_base_lr = "trunk_base_lr"
    val_Mean_Average_Precision = "val Mean Average Precision"
    val_Mean_Reciprocal_Rank = "val Mean Reciprocal Rank"
    val_Precision_at_Rank_1 = "val Precision at Rank 1"
    val_r_Precision = "val r-Precision"
    val_2DMPE = "val_2DMPE"
    val_3DIoU = "val_3DIoU"
    test_2DMPE = "test_2DMPE"
    test_3DIoU = "test_3DIoU"
    val_AMI = "val_AMI"
    val_NMI = "val_NMI"
    val_acc = "val_acc"
    val_accuracy = "val_accuracy"
    val_fpr = "val_fpr"
    val_loss = "val_loss"
    val_mAP = "val_mAP"
    val_mAP50 = "val_mAP50"
    val_mf1 = "val_mf1"
    val_miou = "val_miou"
    val_mprecision = "val_mprecision"
    val_mrecall = "val_mrecall"

    # Data Service Analytics KPI metrics
    num_objects = "num_objects"
    object_count_index = "object_count_index"
    object_count_num = "object_count_num"
    object_count_percent = "object_count_percent"
    bbox_area_type = "bbox_area_type"
    bbox_area_mean = "bbox_area_mean"


class BaseExperimentTask(enum.Enum):
    """Class defining base experiment metadata task field"""

    unknown = None
    object_detection = "object detection"
    image_classification = "image classification"
    segmentation = "segmentation"
    re_identification = "re identification"
    pose_classification = "pose classification"
    action_recognition = "action recognition"
    optical_character_recognition = "optical character recognition"
    visual_changenet_segmentation = "visual changenet segmentation"
    visual_changenet_classification = "visual changenet classification"


class BaseExperimentDomain(enum.Enum):
    """Class defining base experiment metadata license field"""

    unknown = None
    general = "general"
    purpose_built = "purpose built"


class BaseExperimentBackboneType(enum.Enum):
    """Class defining base experiment metadata license field"""

    unknown = None
    cnn = "cnn"
    transformer = "transformer"


class BaseExperimentBackboneClass(enum.Enum):
    """Class defining base experiment metadata license field"""

    unknown = None
    swin = "swin"
    fan = "fan"
    vit = "vit"
    gcvit = "gcvit"
    fastervit = "fastervit"
    efficientnet = "efficientnet"
    resnet = "resnet"
    stgcn = "st gcn"


class BaseExperimentLicense(enum.Enum):
    """Class defining base experiment metadata license field"""

    unknown = None
    nvaie_eula = "nvaie eula"
    nvidia_model_eula = "nvidia model eula"
    cc_by_nc_sa_4 = "cc by nc sa 4.0"
