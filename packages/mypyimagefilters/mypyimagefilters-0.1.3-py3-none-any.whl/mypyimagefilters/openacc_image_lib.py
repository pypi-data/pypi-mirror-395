import ctypes
import os

# Estructura CImage mapeada desde C
class CImage(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("channels", ctypes.c_int),
        ("data", ctypes.POINTER(ctypes.c_ubyte))
    ]

class OpenACCFilterLib:
    def __init__(self):
        """
        Inicializa la librería compartida compilada con OpenACC (nvc).
        """
        # Ruta al .so generado por el Makefile
        lib_path = os.path.join(os.path.dirname(__file__), 'bin', 'libfiltersacc.so')
        
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"Shared library was not found in: {lib_path}")
        
        try:
            self.lib = ctypes.CDLL(lib_path)
        except OSError as e:
            print("Error cargando la librería. Asegúrate de tener las librerías de NVIDIA en tu LD_LIBRARY_PATH.")
            raise e
        
        self._setup_signatures()

    def _setup_signatures(self):
        """Configura los tipos de argumentos y retorno para ctypes."""
        
        # Image *image2arr(const char *file)
        self.lib.image2arr.argtypes = [ctypes.c_char_p]
        self.lib.image2arr.restype = ctypes.POINTER(CImage)

        # void saveImg(Image *img, const char *filename)
        self.lib.saveImg.argtypes = [ctypes.POINTER(CImage), ctypes.c_char_p]
        self.lib.saveImg.restype = None

        # void freeImage(Image *img)
        self.lib.freeImage.argtypes = [ctypes.POINTER(CImage)]
        self.lib.freeImage.restype = None

        # Image *rgb2gray(Image *image)
        self.lib.rgb2gray.argtypes = [ctypes.POINTER(CImage)]
        self.lib.rgb2gray.restype = ctypes.POINTER(CImage)

        # Image *GaussianBlur(Image *image, int kdim, float stdev)
        # IMPORTANTE: stdev es float en C, usar c_float en Python
        self.lib.GaussianBlur.argtypes = [ctypes.POINTER(CImage), ctypes.c_int, ctypes.c_float]
        self.lib.GaussianBlur.restype = ctypes.POINTER(CImage)

        # Image *Sobel(Image *image)
        self.lib.Sobel.argtypes = [ctypes.POINTER(CImage)]
        self.lib.Sobel.restype = ctypes.POINTER(CImage)

    def __load_image(self, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Image not found: {filename}")
        return self.lib.image2arr(filename.encode('utf-8'))

    def __save_image(self, img_ptr, filename: str):
        self.lib.saveImg(img_ptr, filename.encode('utf-8'))

    def __free_image(self, img_ptr):
        if img_ptr:
            self.lib.freeImage(img_ptr)

    def rgb_to_gray(self, filename: str, output_file: str):
        """Ejecuta rgb2gray en GPU (OpenACC)."""
        img_ptr = self.__load_image(filename)
        
        # Llamada a C (Devuelve nueva imagen)
        gray_ptr = self.lib.rgb2gray(img_ptr)
        
        self.__save_image(gray_ptr, output_file)
        
        # Limpieza
        self.__free_image(img_ptr)
        self.__free_image(gray_ptr)

    def gaussian_blur(self, filename: str, output_file: str, kernel_dim: int = 5, stdev: float = 10.0):
        """Ejecuta GaussianBlur en GPU (OpenACC)."""
        img_ptr = self.__load_image(filename)
        
        # Llamada a C
        blurred_ptr = self.lib.GaussianBlur(img_ptr, kernel_dim, stdev)
        
        self.__save_image(blurred_ptr, output_file)
        
        # Limpieza
        self.__free_image(img_ptr)
        self.__free_image(blurred_ptr)

    def sobel(self, filename: str, output_file: str):
        """
        Ejecuta Sobel en GPU (OpenACC).
        Convierte a Gris primero, luego aplica Sobel.
        """
        img_ptr = self.__load_image(filename)
        
        # 1. Convertir a Gris (Sobel necesita 1 canal para tu implementación actual)
        gray_ptr = self.lib.rgb2gray(img_ptr)
        
        # 2. Aplicar Sobel
        sobel_ptr = self.lib.Sobel(gray_ptr)
        
        self.__save_image(sobel_ptr, output_file)
        
        # Limpieza en cadena
        self.__free_image(img_ptr)
        self.__free_image(gray_ptr)
        self.__free_image(sobel_ptr)