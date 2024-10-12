from pathlib import Path
import cv2
import os
from docxtpl import InlineImage, DocxTemplate
from docx.shared import Mm
import tempfile
from loguru import logger


class DocFormater():
    def __init__(self) -> None:
        self.work_dir = Path.cwd()
        self.template_path = self.work_dir.joinpath("fastApi", "auxilary_function", "document_forming",
                                                    "template.docx")
        self.doc_object = DocxTemplate(self.template_path)
        if self.doc_object:
            logger.success("Template loaded!")
        else:
            logger.error("Template loading error!")
            return

    def _draw_rectangle(self, image, coords, name):
        image = cv2.rectangle(image, (coords[0], coords[1]), (coords[0] + coords[2], coords[1] + coords[3]),
                              (36, 255, 12), 60)
        cv2.putText(image, name, (coords[0], coords[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 60)
        return image

    def _make_inline_image(self, image):
        """Save the image temporarily and return the inline image for docx."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            cv2.imwrite(temp_file.name, image)
            temp_file_path = temp_file.name
        return InlineImage(self.doc_object, temp_file_path, height=Mm(25)), temp_file_path

    def make_and_save_document(self, template_data):
        temp_image_paths = []  # Track temporary files to clean up
        for item in template_data["content"]:
            # Получаем путь к фото и проверяем его
            photo_path = item.get("photo", "")

            # Проверяем, существует ли файл и является ли это файлом (а не директорией)
            if photo_path and Path(photo_path).is_file():
                # Загружаем изображение
                image = cv2.imread(photo_path)
                if image is None:
                    logger.error(f"Не удалось загрузить изображение: {photo_path}")
                    item["photo"] = "Фото не удалось загрузить"
                    continue
                # Наносим дефекты на изображение
                for defect in item["defects"]:
                    image = self._draw_rectangle(image, defect["coords"], defect["name"])
                # Создаем изображение для вставки в документ
                inline_image, temp_image_path = self._make_inline_image(image)
                temp_image_paths.append(temp_image_path)
                item["photo"] = inline_image  # Заменяем путь на InlineImage для вставки в документ
            else:
                item["photo"] = "Фото не предоставлено"  # Если фото нет или путь некорректен

        # Рендерим документ с контекстом
        context = {
            'appeal_order': template_data["appeal_order"],
            'executor_name': template_data["executor_name"],
            'executor_phone': template_data["executor_phone"],
            'executor_address': template_data["executor_address"],
            'customer_name': template_data["customer_name"],
            'customer_address': template_data["customer_address"],
            'customer_phone': template_data["customer_phone"],
            'laptop_firm': template_data["laptop_firm"],
            'laptop_model': template_data["laptop_model"],
            'laptop_serial_number': template_data["laptop_serial_number"],
            'commission_date': template_data["commission_date"],
            'created_at': template_data["created_at"],
            'content': template_data["content"]
        }

        # Сохранение документа
        appeal_order = template_data["appeal_order"]
        created_at = template_data["created_at"]
        self.doc_object.render(context)
        save_path = self.work_dir.joinpath("fastApi", "auxilary_function", "document_forming",
                                           f"№{appeal_order}_от_{created_at}.docx")
        self.doc_object.save(save_path)

        # Очистка временных изображений
        for path in temp_image_paths:
            os.remove(path)

        logger.success("Документ создан успешно!")
        return save_path

