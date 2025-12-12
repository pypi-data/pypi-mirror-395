import logging
import os
import asyncio
from typing import List, Optional, Tuple

# from pdf2image import convert_from_path ELIMINADO
# pip uninstall pdf2image
# pip install PyMuPDF
import fitz  # <-- AÑADIDO (PyMuPDF)

from .image import save_image
from .text import format_markdown
from ..constants import PDFConversionDefaultOptions, Messages
from ..models import litellmmodel


def _convert_pdf_to_images_pymupdf(
    image_height: tuple[Optional[int], int],
    local_path: str,
    temp_dir: str,
    output_format: str = "png",
) -> List[str]:
    """
    Función síncrona que reemplaza a pdf2image.
    Convierte un PDF en imágenes usando PyMuPDF (fitz).

    Esta función NO depende de Poppler.
    """
    image_paths = []
    doc = None
    try:
        doc = fitz.open(local_path)

        if len(doc) == 0:
            logging.warning(f"El PDF está vacío (0 páginas): {local_path}")
            return []

        # Determinar la matriz de transformación (escalado)
        target_w, target_h = image_height

        # Usamos las dimensiones de la primera página para calcular el zoom
        page_for_dims = doc.load_page(0)
        rect = page_for_dims.rect

        if rect.width == 0 or rect.height == 0:
            logging.error(f"Dimensiones de página inválidas en el PDF: {local_path}")
            return []

        if target_w is None:  # Caso por defecto: (None, 2000) -> Escalar proporcionalmente a la altura
            zoom = target_h / rect.height
            matrix = fitz.Matrix(zoom, zoom)
        else:  # Si se especifican ambos (ej. (1000, 2000)) -> Estirar
            zoom_x = target_w / rect.width
            zoom_y = target_h / rect.height
            matrix = fitz.Matrix(zoom_x, zoom_y)

        # Preparar formato de salida
        output_format = output_format.lower().strip()
        if output_format not in ("png", "jpeg", "jpg"):
            output_format = "png"  # Usar PNG como fallback seguro

        total_pages = len(doc)
        num_digits = len(str(total_pages))  # Para rellenar con ceros (ej. 01, 02...)

        # Obtener el nombre base del archivo para nombrar las imágenes
        base_filename = os.path.basename(local_path)
        file_root, _ = os.path.splitext(base_filename)

        # Iterar sobre todas las páginas
        for page_num in range(total_pages):
            page = doc.load_page(page_num)

            # Renderizar la página usando la matriz calculada
            pix = page.get_pixmap(matrix=matrix, alpha=False)

            # Crear la ruta de salida (replicando el formato de pdf2image)
            page_str = str(page_num + 1).zfill(num_digits)
            image_name = f"{file_root}-{page_str}.{output_format}"
            image_path = os.path.join(temp_dir, image_name)

            # Guardar la imagen
            pix.save(image_path)
            image_paths.append(image_path)

        return image_paths

    except Exception as err:
        logging.error(f"Error convirtiendo PDF a imágenes con PyMuPDF: {err}")
        return []  # Devolver lista vacía en caso de fallo

    finally:
        if doc:
            doc.close()


async def convert_pdf_to_images(image_density: int, image_height: tuple[Optional[int], int], local_path: str,
                                temp_dir: str) -> List[str]:
    """
    Convierte un archivo PDF en una serie de imágenes en temp_dir.
    Devuelve una lista de rutas de imagen en orden de página.
    Esta versión usa PyMuPDF (fitz) y NO requiere Poppler.
    """

    # Nota: 'image_density' (DPI) no se usa si 'image_height' está presente,
    # para replicar el comportamiento de la librería original.

    try:
        # Ejecuta la función de conversión síncrona en un hilo separado
        image_paths = await asyncio.to_thread(
            _convert_pdf_to_images_pymupdf,
            image_height=image_height,
            local_path=local_path,
            temp_dir=temp_dir,
            output_format=PDFConversionDefaultOptions.FORMAT,
        )
        return image_paths
    except Exception as err:
        # El logging principal ocurre en la función síncrona, pero capturamos errores de asyncio
        logging.error(f"Error en asyncio.to_thread para la conversión de PDF: {err}")
        return []


async def process_page(
    image: str,
    model: litellmmodel,
    temp_directory: str = "",
    input_token_count: int = 0,
    output_token_count: int = 0,
    prior_page: str = "",
    semaphore: Optional[asyncio.Semaphore] = None,
) -> Tuple[str, int, int, str]:
    """Process a single page of a PDF"""

    # If semaphore is provided, acquire it before processing the page
    if semaphore:
        async with semaphore:
            # Re-llama a la función sin el semáforo para evitar recursión infinita
            return await process_page(
                image,
                model,
                temp_directory,
                input_token_count,
                output_token_count,
                prior_page,
                None,  # Pasa None para evitar el bucle
            )

    image_path = os.path.join(temp_directory, image)

    # Get the completion from LiteLLM
    try:
        completion = await model.completion(
            image_path=image_path,
            maintain_format=True,
            prior_page=prior_page,
        )

        formatted_markdown = format_markdown(completion.content)
        input_token_count += completion.input_tokens
        output_token_count += completion.output_tokens
        prior_page = formatted_markdown

        return formatted_markdown, input_token_count, output_token_count, prior_page

    except Exception as error:
        logging.error(f"{Messages.FAILED_T_PROCESS_IMAGE} Error:{error}")
        return "", input_token_count, output_token_count, ""


async def process_pages_in_batches(
    images: List[str],
    concurrency: int,
    model: litellmmodel,
    temp_directory: str = "",
    input_token_count: int = 0,
    output_token_count: int = 0,
    prior_page: str = "",
):
    # Create a semaphore to limit the number of concurrent tasks
    semaphore = asyncio.Semaphore(concurrency)

    # Process each page in parallel
    tasks = [
        process_page(
            image,
            model,
            temp_directory,
            input_token_count,
            output_token_count,
            prior_page,
            semaphore,
        )
        for image in images
    ]

    # Wait for all tasks to complete
    return await asyncio.gather(*tasks)
