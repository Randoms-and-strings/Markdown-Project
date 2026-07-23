import time
from starlette.datastructures import FormData
from fastapi import HTTPException, UploadFile
import os
import uuid
import boto3
import aioboto3
import asyncio
from dotenv import load_dotenv
load_dotenv()


s3_session = aioboto3.Session()
S3_FOLDER_NAME = os.getenv("S3_MARKDOWNAPP_FOLDER")
S3_BUCKETNAME = os.getenv("S3_MARKDOWNAPP_BUCKETNAME")
S3_REGION = os.getenv("S3_MARKDOWNAPP_REGION")
S3_BUCKET_URL = (f"https://{S3_BUCKETNAME}.s3."
                 f"{S3_REGION}.amazonaws.com/"
                 f"{S3_FOLDER_NAME}")



def parse_img_from_form(picture_object_key:str, form_object_iterable: FormData) -> tuple[str, int, UploadFile] | tuple[HTTPException, None, None]:
    element_type = picture_object_key.split(":")[0]
    element_position = int(picture_object_key.split(":")[1])
    raw_image_object: UploadFile = form_object_iterable.get(picture_object_key)

    if raw_image_object.filename.split(".")[-1] not in ["png", "jpg", "jpeg", "webp", "gif"]:
        return HTTPException(status_code=422, detail="Image type not supported"), None, None

    image_extension = raw_image_object.filename.split(".")[-1]
    new_filename = str(uuid.uuid4())
    raw_image_object.filename = f'{new_filename}.{image_extension}'

    image_max_size = 1024 * 1024 * 5  # 5mb max filesize upload
    if raw_image_object.size > image_max_size:
        return HTTPException(status_code=422, detail="Image item too large"), None, None

    return element_type, element_position, raw_image_object

# async def save_to_s3(cleaned_picture_object: UploadFile, element_name:str, element_position:int) -> dict[str, int]|HTTPException:
async def save_to_s3(picture_data:tuple[UploadFile, str, int]) -> dict[str, int] | HTTPException:
    cleaned_picture_object = picture_data[0]
    element_name = picture_data[1]
    element_position = picture_data[2]
    try:
        start_opening_file = time.time()
        async with s3_session.client("s3") as obj:
            with cleaned_picture_object.file as imageBytes:
                imageBytes.seek(0)
                print(f"time taken to open one file is {time.time() - start_opening_file}")

                send_start_time = time.time()
                await obj.upload_fileobj(imageBytes,
                                   S3_BUCKETNAME,
                                   f"{S3_FOLDER_NAME}/{cleaned_picture_object.filename}")
                print(f"time taken to send one file is {time.time() - send_start_time}")

            # print(f"done successfully")

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

async def remove_image_from_post(post_content:list):
    if post_content is None:
        return True
    all_img_names:list[str] = []
    for items in post_content:
        # print(items)
        post_content_type:str = items.get("type")
        if post_content_type.lower() == "img":
            all_img_names.append(items.get("content"))

    # todo:there shuld be a more eff way to batch delete, thats why i left this, else i'd have used 1func to handle all
    #
    no_of_images_in_post:int = len(all_img_names)
    if no_of_images_in_post > 1:
        batch_delete_time = time.time()
        delete_result:list = await asyncio.gather(*[delete_from_s3(name) for name in all_img_names], return_exceptions=True)
        # print(delete_result)
        print(f"time taken to batch delete file is {time.time() - batch_delete_time}")
        for result in delete_result:
            if isinstance(result, HTTPException):
                return result
        # result = await batch_delete_from_s3(all_img_names)
        # if not result:
        #     # todo:should return failed img names list
        #     return False
        return True

    # print(all_img_names)
    single_delete:bool = await delete_from_s3(all_img_names[0])
    if not single_delete:
        return HTTPException(status_code=500, detail="failed to delete an unused img from s3")
    return True



async def batch_delete_from_s3(items_to_delete:list[str]):
    async with s3_session.resource("s3") as s3:
        try:

            bucket = await s3.Bucket(S3_BUCKETNAME)
            # asyncio.gather(*[for name in items_to_delete])

            for name in items_to_delete:
                result = await bucket.objects.filter(Prefix=f'{S3_FOLDER_NAME}/{name}').delete()

                # print("done", result) #result is an empty list if the file doesnt exist, or above if success

        except Exception as s3_delete_error:
            print(s3_delete_error)
            # todo:should return name that failed to delete from s3, for later processing
            return False
            # return HTTPException(status_code=500, detail="failed to delete your file")
        else:
            # if result[0]["ResponseMetadata"]["HTTPStatusCode"] != 200:
            #     return False
            return True
    return

async def delete_from_s3(filename:str) -> bool|HTTPException:
    start_delete_time = time.time()
    async with s3_session.resource("s3") as s3:
        try:
            bucket = await s3.Bucket(S3_BUCKETNAME)
            result = await bucket.objects.filter(Prefix=f'{S3_FOLDER_NAME}/{filename}').delete()
            # print("done", result)
            print(f"time taken to delete one file is {time.time() - start_delete_time}")
        except Exception as s3_delete_error:
            print(s3_delete_error)
            # return False
            return HTTPException(status_code=500, detail="failed to delete your file")
        else:
            return True

