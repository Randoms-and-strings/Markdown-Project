from starlette.datastructures import FormData
from fastapi import HTTPException, UploadFile
import os
import uuid
import boto3
import aioboto3
import asyncio
from dotenv import load_dotenv
load_dotenv()

# obj = boto3.client("s3")
s3_session = aioboto3.Session()
S3_BUCKET_URL = (f"https://{os.getenv("S3_MARKDOWNAPP_BUCKETNAME")}.s3."
                 f"{os.getenv("S3_MARKDOWNAPP_REGION")}.amazonaws.com/"
                 f"{os.getenv("S3_MARKDOWNAPP_FOLDER")}")

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

# def send_to_s3(cleaned_pic_obj):
#     with cleaned_pic_obj.file as imageBytes:
#         # contents:bytes =imageBytes.read()
#         # print(contents, imageBytes)
#         imageBytes.seek(0)
#         obj.upload_fileobj(imageBytes,
#                            os.getenv("AWS_BUCKET_NAME"),
#                            f"{os.getenv("AWS_BUCKET_FOLDER")}/{cleaned_pic_obj.filename}")
#
# async def save_to_s3(cleaned_picture_object: UploadFile, element_name:str, element_position:int) -> dict[str, int]|HTTPException:
#     # obj = boto3.client("s3")
#     loop = asyncio.get_running_loop()
#     try:
#         # with cleaned_picture_object.file as imageBytes:
#         #     # contents:bytes =imageBytes.read()
#         #     # print(contents, imageBytes)
#         #     imageBytes.seek(0)
#         #     obj.upload_fileobj(imageBytes,
#         #                        os.getenv("AWS_BUCKET_NAME"),
#         #                        f"{os.getenv("AWS_BUCKET_FOLDER")}/{cleaned_picture_object.filename}")
#         result = await loop.run_in_executor(None, send_to_s3, cleaned_picture_object)
#         print(f"done successfully: {result}")
#
#     except Exception as e:
#         print(e)
#         return HTTPException(status_code=500, detail="something went wrong uploading your file")
#     else:
#         return {
#             "type": element_name,
#             "position": element_position,
#             "content": cleaned_picture_object.filename
#         }

async def save_to_s3(cleaned_picture_object: UploadFile, element_name:str, element_position:int) -> dict[str, int]|HTTPException:

    try:
        async with s3_session.client("s3") as obj:
            with cleaned_picture_object.file as imageBytes:
                # contents:bytes =imageBytes.read()
                # print(contents, imageBytes)
                imageBytes.seek(0)

                await obj.upload_fileobj(imageBytes,
                                   os.getenv("AWS_BUCKET_NAME"),
                                   f"{os.getenv("AWS_BUCKET_FOLDER")}/{cleaned_picture_object.filename}")

            print(f"done successfully")

    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong uploading your file")
    else:
        return {
            "type": element_name,
            "position": element_position,
            "content": cleaned_picture_object.filename
        }

def get_img_s3(img_name:str) -> str:
    return f"{S3_BUCKET_URL}/{img_name}"

async def delete_from_s3(filename) -> bool:
    async with s3_session.resource("s3") as s3:
        try:
            bucket = await s3.Bucket(os.getenv("S3_MARKDOWNAPP_BUCKETNAME"))
            result = await bucket.objects.filter(Prefix=f'{os.getenv("S3_MARKDOWNAPP_FOLDER")}/{filename}').delete()
            print("done", result)
        except Exception as s3_delete_error:
            print(s3_delete_error)
            return False
            # return HTTPException(status_code=500, detail="failed to delete your file")
        else:
            return True

# asyncio.run(delete_from_s3("a0a08203-dbc4-48e6-82ae-ff8712e74e64.jpg"))
