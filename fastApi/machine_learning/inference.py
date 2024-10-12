from ultralytics import YOLO
from pathlib import Path

model_path = Path().cwd().joinpath("epoch30.pt")


class KTeamYoloFinetune:

    def __init__(self, path: str, *args, **kwargs):
        self.model = YOLO(path)

    def __call__(self, image_path: str, *args, **kwargs):
        # Лист объектов-результатов
        results = self.model(image_path)[0]

        # Классы
        classes = [results.names[index.item()] for index in results.boxes.cls]

        # Квадраты
        tensored_boxes = [xyxy.cpu().numpy() for xyxy in results.boxes.xyxy]
        boxes = []
        for box in tensored_boxes:
            boxes.append([int(coordinate) for coordinate in box])

        # Вероятности
        confs = [conf.item() for conf in results.boxes.conf]

        return boxes, classes, confs

# USAGE
# model = KTeamYoloFinetune(model_path)
# boxes, classes, probs = model("3.jpg")
# boxes = [[123, 123, 123, 123]] - координаты Bounding box
# classes = [клавиатура]
# probs = [0,125]
# Если модель не определяет ничего - возврвщает [] во всех переменных
