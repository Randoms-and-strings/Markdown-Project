from starlette.datastructures import FormData
from fastapi import HTTPException, UploadFile
import os
import uuid
import boto3

def parse_img_from_form(picture_object_key:str, form_object_iterable: FormData) -> tuple[str, int, UploadFile] | tuple[HTTPException, None, None]:
    element_type = picture_object_key.split(":")[0]
    element_position = int(picture_object_key.split(":")[1])
    raw_image_object: UploadFile = form_object_iterable.get(picture_object_key)

    if raw_image_object.filename.split(".")[-1] not in ["png", "jpg", "jpeg", "webp", "gif"]:
        return HTTPException(status_code=422, detail="Image type not supported"), None, None

    image_extension = raw_image_object.filename.split(".")[-1]
    new_filename = str(uuid.uuid4())
    raw_image_object.filename = f'{new_filename}.{image_extension}'
    # new_filename = raw_image_object.filename
    print(new_filename)

    image_max_size = 1024 * 1024 * 5  # 5mb max filesize upload
    if raw_image_object.size > image_max_size:
        return HTTPException(status_code=422, detail="Image item too large"), None, None

    return element_type, element_position, raw_image_object

def save_to_s3(cleaned_picture_object: UploadFile, element_name:str, element_position:int) -> dict[str, int]|HTTPException:
    obj = boto3.client("s3")
    try:
        with cleaned_picture_object.file as imageBytes:
            # contents:bytes =imageBytes.read()
            # print(contents, imageBytes)
            imageBytes.seek(0)
            obj.upload_fileobj(imageBytes,
                               os.getenv("AWS_BUCKET_NAME"),
                               f"{os.getenv("AWS_BUCKET_FOLDER")}/{cleaned_picture_object.filename}")
            print("done successfully")

    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong uploading your file")
    else:
        return {
            "type": element_name,
            "position": element_position,
            "content": cleaned_picture_object.filename
        }
