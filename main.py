from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
import io
from skimage import measure
import numpy as np
import cv2
from modules import dbconnection


app = FastAPI(title="Image Processing API", version="1.0")

@app.post("/procesar-imagen")
async def procesar_imagen(id: int = Form(...), file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        print("El archivo debe ser una imagen")
        print(file.content_type)
        print(file.filename)
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
        
    # Leer el contenido del archivo
    imagen_bytes = await file.read()

    try:
        # Abrir imagen desde los bytes
        pil_img = Image.open(io.BytesIO(imagen_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al abrir la imagen: {e}")

    # Procesar imagen: convertir a escala de grises
    # imagen_gris = imagen.convert("L")
#---------------------------

    img_bgr=cv2.cvtColor(np.array(pil_img),cv2.COLOR_RGB2BGR)
    # image = cv2.imread('../imagenes/Habitacion2.jpg')

    gray_image= cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)
    _,binarizada=cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY_INV)
    labels = measure.label(binarizada ,connectivity=1)
    borders = np.max(labels)

    border_muestra = 1618

    if borders >= border_muestra-5 and borders <= border_muestra+5 :
        print(f"La imagen tiene {borders} bordes, lo cual significa que la habitacion esta limpia")
    else:
        print(f"La imagen tiene {borders} bordes, lo cual significa que la habitacion esta desordenada")
        try:
            conn = await dbconnection.get_db_connection()
            await conn.execute("""
                UPDATE "habitacion"
                SET idEstado = 2
                WHERE id = $1
            """
            , id)  
            await conn.close()
        except Exception as e:
            print(f"Error al actualizar la base de datos: {e}")


    # Guardar la imagen procesada en un buffer
    buffer = io.BytesIO()
    Image.fromarray(gray_image).save(buffer, format="PNG")
    buffer.seek(0)

    # return StreamingResponse(buffer, media_type="image/png")

@app.get("/ping")
def ping():
    return {"mensaje": "Servidor activo"}
