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
    # print(new_filename)

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

# async def save_to_s3(cleaned_picture_object: UploadFile, element_name:str, element_position:int) -> dict[str, int]|HTTPException:
async def save_to_s3(picture_data:tuple[UploadFile, str, int]) -> dict[str, int] | HTTPException:
    cleaned_picture_object = picture_data[0]
    element_name = picture_data[1]
    element_position = picture_data[2]
    try:
        async with s3_session.client("s3") as obj:
            with cleaned_picture_object.file as imageBytes:
                # contents:bytes =imageBytes.read()
                # print(contents, imageBytes)
                imageBytes.seek(0)

                await obj.upload_fileobj(imageBytes,
                                   os.getenv("AWS_BUCKET_NAME"),
                                   f"{os.getenv("AWS_BUCKET_FOLDER")}/{cleaned_picture_object.filename}")

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
        delete_result:list = await asyncio.gather(*[delete_from_s3(name) for name in all_img_names], return_exceptions=True)
        # print(delete_result)
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

            bucket = await s3.Bucket(os.getenv("S3_MARKDOWNAPP_BUCKETNAME"))
            # asyncio.gather(*[for name in items_to_delete])

            for name in items_to_delete:
                result = await bucket.objects.filter(Prefix=f'{os.getenv("S3_MARKDOWNAPP_FOLDER")}/{name}').delete()
            #     await s3_object.delete()
            #     [{'ResponseMetadata': {'RequestId': 'NT5TG5PP31CHRY31',
            #                            'HostId': '6/qf/dR07E7TGkZiUgKuRHI2/nQmCBvd91YncGGVU1kwNwIHxTu3anYnUK0QvoGUH7wecucyxao=',
            #                            'HTTPStatusCode': 200, 'HTTPHeaders': {
            #             'x-amz-id-2': '6/qf/dR07E7TGkZiUgKuRHI2/nQmCBvd91YncGGVU1kwNwIHxTu3anYnUK0QvoGUH7wecucyxao=',
            #             'x-amz-request-id': 'NT5TG5PP31CHRY31', 'date': 'Wed, 15 Jul 2026 15:41:50 GMT',
            #             'connection': 'close', 'content-type': 'application/xml', 'transfer-encoding': 'chunked',
            #             'server': 'AmazonS3'}, 'RetryAttempts': 0},
            #       'Deleted': [{'Key': 'markdown_app/a932ea42-99d5-4f9a-9349-3bf4abd80632.jpg'}]}]

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
    async with s3_session.resource("s3") as s3:
        try:
            bucket = await s3.Bucket(os.getenv("S3_MARKDOWNAPP_BUCKETNAME"))
            result = await bucket.objects.filter(Prefix=f'{os.getenv("S3_MARKDOWNAPP_FOLDER")}/{filename}').delete()
            # print("done", result)
        except Exception as s3_delete_error:
            print(s3_delete_error)
            # return False
            return HTTPException(status_code=500, detail="failed to delete your file")
        else:
            return True

# asyncio.run(remove_image_from_post(["03603388-b370-4cb8-876f-998243d90384.jpg",
#                                     "0c1de524-91f9-4709-aec0-44dcb7be2e49.jpg",
#                                     "20c4c798-3548-492f-93af-c38156130f41.jpg",
#                                     "2fbe284a-cab9-4230-9920-055ffcd26c09.jpg",
#                                     "41671833-9ca3-4af0-aded-1f46f551a8a1.jpg"]))
