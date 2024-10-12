from pathlib import Path

from fastApi.services.appeal_operations.models import Appeal, Result


def format_appeal_response(appeal: Appeal, result: Result):
    response = {
        'appeal_order': str(appeal.uuid).replace("-", "")[:6],  # Taking first 6 characters of the UUID
        'executor_name': appeal.executor.name,
        'executor_phone': appeal.executor.phone_number,
        'executor_address': appeal.executor.address,
        'customer_name': appeal.customer.name,
        'customer_address': appeal.customer.address,
        'customer_phone': appeal.customer.phone_number,
        'laptop_firm': appeal.laptop_firm,
        'laptop_model': appeal.laptop_model,
        'laptop_serial_number': appeal.laptop_serial_number,
        'commission_date': appeal.commission_date.strftime('%d.%m.%Y'),
        'created_at': appeal.created_at.strftime('%d.%m.%Y'),
        'content': []
    }

    # Creating the defects content
    for index, file_path in enumerate(result.defect_photo_path):
        defects = []
        for defect_class, coords in zip(result.defect_class[index], result.defect_coords[index]):
            defects.append({
                "name": defect_class,  # Class or name of the defect
                "coords": coords  # Coordinates of the defect
            })

        content_entry = {
            "defect_photo_path": str(Path.cwd().joinpath('fastApi/uploads', Path(file_path).name)),
            "defects": defects
        }
        response['content'].append(content_entry)

    return response
