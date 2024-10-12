from fastApi.machine_learning.inference import KTeamYoloFinetune


def model_usage(img_path: str):
    model = KTeamYoloFinetune(path="C://Users//Boba//Documents//GitHub//LaptopAnalyzer//fastApi//machine_learning//epoch30.pt")
    boxes, classes, _ = model(img_path)
    return boxes, classes
