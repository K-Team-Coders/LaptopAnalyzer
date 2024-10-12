# Импортируем нужный объект из библиотеки 
from pathlib import Path
import tempfile
import os

from loguru import logger
from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docx.shared import Mm
import cv2

class DocFormater():
    def __init__(self) -> None:
        self.work_dir = Path.cwd()
        self.template_path = self.work_dir.joinpath("services", "appeal_operations", "utils", "document_forming", "template.docx")
        self.doc_object = DocxTemplate(self.template_path)
        if self.doc_object:
            logger.success("Template loaded!")
        else: 
            logger.error("Template loading error!")
            return
    
    def _draw_rectangle(self, image, coords, name):
        image = cv2.rectangle(image, (coords[0], coords[1]), (coords[0] + coords[2],coords[1] + coords[3]), (36,255,12), 60)
        cv2.putText(image, name, (coords[0], coords[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 60)
        return image
    
    def _make_inline_image(self, path):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            cv2.imwrite(temp_file.name, path)
            temp_file_path = temp_file.name
        return InlineImage(self.doc_object, temp_file_path, height=Mm(25)), temp_file_path
    
    def make_and_save_document(self, template_data):
        temp_image_paths = [] 
        for item in template_data["content"]:
            image = cv2.imread(item["photo"])
            for defect in item["defects"]:
                item["photo"] = self._draw_rectangle(image, defect["coords"], defect["name"])
            inline_image, temp_image_path = self._make_inline_image(item["photo"])
            temp_image_paths.append(temp_image_path)  
            item["photo"] = inline_image
        
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
            'created_at': template_data["created_at"] ,
            'content': template_data["content"]
        }
        appeal_order = template_data["appeal_order"]
        created_at = template_data["created_at"]
        self.doc_object.render(context)
        save_path = self.work_dir.joinpath("services", "appeal_operations", "utils", "document_forming", f"№{appeal_order}_от_{created_at}.docx")
        self.doc_object.save(save_path)
        for path in temp_image_paths:
            os.remove(path)
        logger.success("Document has been created!")
        return save_path
    
    
if __name__ == '__main__':
    template_data = {
        'appeal_order': '000001',
    'executor_name': 'Иван Долбоеб',
    'executor_phone': '898222221',
    'executor_address': 'Плоховская 67Б',
    'customer_name': 'Богдан Горбунов',
    'customer_address': 'Самосир, Дворец Позднякова',
    'customer_phone': '898222221',
    'laptop_firm': 'Акваминерале',
    'laptop_model': 'Уставной',
    'laptop_serial_number': '82142141',
    'commission_date': '24.03.2024',
    'created_at': '24.03.2024' ,
    'content': 
         [
    {"photo": f"{Path.cwd().joinpath('img', '2023-12-26 15-38-08.jpg')}", 
     "defects": [
         {"name": "Scrath",
          "coords": [12, 13, 1000, 1000]}, 
         {"name": "Scrath",
          "coords": [12, 13, 1000, 1000]}]
     },
    {"photo": f"{Path.cwd().joinpath('img', '2024-01-15 14-38-21.jpg')}", 
     "defects": [
         {"name": "Scrath",
          "coords": [12, 13, 1000, 1000]}, 
         {"name": "Scrath",
          "coords": [12, 13, 250, 250]}]
     },
    {"photo": f"{Path.cwd().joinpath('img', '2024-01-15 16-28-22.jpg')}", 
     "defects": [
         {"name": "Scrath",
          "coords": [12, 13, 1000, 1000]}, 
        {"name": "Scrath",
          "coords": [12, 13, 1000, 1000]}]
     },
    ]
    }
    doc_formatter = DocFormater()
    doc_formatter.make_and_save_document(template_data)
    