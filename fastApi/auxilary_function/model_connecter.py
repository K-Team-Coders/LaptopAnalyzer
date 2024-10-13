from fastApi.machine_learning.inference import KTeamYoloFinetune
from pathlib import Path

actual_path_support = Path(__file__).parent.parent.joinpath("machine_learning").joinpath("support_025_012.pt").__str__()
actual_path_phusical = Path(__file__).parent.parent.joinpath("machine_learning").joinpath("phusical_medium_020_010.pt").__str__()

def model_usage(img_path: str):

    support_model = KTeamYoloFinetune(path=actual_path_support)
    support_boxes, support_classes, _ = support_model(img_path)

    phusical_model = KTeamYoloFinetune(path=actual_path_phusical)
    phusical_boxes, phusical_classes, _ = phusical_model(img_path)

    boxes = []
    boxes.extend(support_boxes)
    boxes.extend(phusical_boxes)

    classes = []
    classes.extend(support_classes)
    classes.extend(phusical_classes)

    return boxes, classes
