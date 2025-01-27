from fastapi import FastAPI

from authentication import search_file
from download_files import download_folder
from duplicate_detector import remove_duplicates_local
from video_optimizer import compress_video
from image_optimizer import optimize_image




app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/services")
def read_root():
    service = search_file()
    return service


    
# @app.get("/test")
# def read_clear_drive():
#     service = authenticate()
#     if service:
#         download_files = download_folder(service, "videos")
#         compress_video(service, download_files[0], download_files[1])
#         return {"message":"success"}
#     else:
#         return {"error":"error al autenticar"}
        
# @app.get("/optimize_images")	
# def read_clear_drive():
#     service = authenticate()
#     if service:
#        dowloaded_files = download_folder(service, "images")
#        optimize_image(dowloaded_files[0], dowloaded_files[1])

#     else:
#         return {"error":"error al autenticar"}
       

# @app.get("/delete_duplicates")
# def read_clear_drive():
#     service = authenticate()
#     if service:
#         dowloaded_files = download_folder(service, "all")
#         remove_duplicates_local(service)
#     else:
#         return {"error":"error al autenticar"}
    
# @app.get("/orderer_files")
# def read_clear_drive():
#     service = authenticate()
#     if service:
#         dowloaded_files = download_folder(service, "all")
#     else:
#         return {"error":"error al autenticar"}
 
                