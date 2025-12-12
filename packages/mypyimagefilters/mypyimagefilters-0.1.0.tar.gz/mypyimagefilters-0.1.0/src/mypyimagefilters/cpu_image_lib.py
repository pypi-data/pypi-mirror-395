import ctypes
import os

class CImage(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("channels", ctypes.c_int),
        ("data", ctypes.POINTER(ctypes.c_ubyte))
    ]

class CPUFilterLib:
    def __init__(self):
        """
        Inicializa la librería compartida de Filtros CPU.
        """
        lib_path = os.path.abspath('./bin/libfiltersseq.so')
        
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"Shared library was not found in: {lib_path}")
        
        # Cargar la librería
        self.lib = ctypes.CDLL(lib_path)
        
        # Configurar firmas de funciones
        self._setup_signatures()

    def _setup_signatures(self):
        """Configura los tipos de argumentos y retorno para ctypes."""
        
        self.lib.image2arr.argtypes = [ctypes.c_char_p]
        self.lib.image2arr.restype = ctypes.POINTER(CImage)

        self.lib.saveImg.argtypes = [ctypes.POINTER(CImage), ctypes.c_char_p]
        self.lib.saveImg.restype = None

        self.lib.freeImage.argtypes = [ctypes.POINTER(CImage)]
        self.lib.freeImage.restype = None

        self.lib.rgb2gray.argtypes = [ctypes.POINTER(CImage)]
        self.lib.rgb2gray.restype = ctypes.POINTER(CImage)

        self.lib.GaussianBlur.argtypes = [ctypes.POINTER(CImage), ctypes.c_int, ctypes.c_float]
        self.lib.GaussianBlur.restype = ctypes.POINTER(CImage)

        # Image *Sobel(Image *image)
        self.lib.Sobel.argtypes = [ctypes.POINTER(CImage)]
        self.lib.Sobel.restype = ctypes.POINTER(CImage)

    def __load_image(self, filename: str):
        """Carga una imagen y devuelve un puntero a CImage."""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Image not found: {filename}")
        return self.lib.image2arr(filename.encode('utf-8'))

    def __save_image(self, img_ptr, filename: str):
        """Guarda la imagen apuntada por img_ptr en el disco."""
        self.lib.saveImg(img_ptr, filename.encode('utf-8'))

    def __free_image(self, img_ptr):
        """Libera la memoria de la imagen."""
        if img_ptr:
            self.lib.freeImage(img_ptr)
            # Nota: En tu código C, freeImage solo hace free(img->data).
            # Si createImg hizo malloc del struct Image, técnicamente 
            # también deberías liberar el puntero struct aquí o en C.

    def rgb_to_gray(self, filename: str, output_file: str):
        """Aplica filtro RGB a Escala de Grises."""
        img_ptr = self.__load_image(filename)
        gray_ptr = self.lib.rgb2gray(img_ptr)
        self.__save_image(gray_ptr, output_file)
        self.__free_image(img_ptr)
        self.__free_image(gray_ptr)

    def gaussian_blur(self, filename: str, output_file: str, kernel_dim: int = 5, stdev: float = 10.0):
        """Aplica filtro Gaussian Blur."""
        img_ptr = self.__load_image(filename)
        blurred_ptr = self.lib.GaussianBlur(img_ptr, kernel_dim, stdev)
        self.__save_image(blurred_ptr, output_file)
        self.__free_image(img_ptr)
        self.__free_image(blurred_ptr)

    def sobel(self, filename: str, output_file: str):
        """
        Aplica filtro de detección de bordes Sobel.
        Nota: Sobel generalmente requiere una imagen en escala de grises.
        """
        img_ptr = self.__load_image(filename)
        gray_ptr = self.lib.rgb2gray(img_ptr)
        sobel_ptr = self.lib.Sobel(gray_ptr)
        self.__save_image(sobel_ptr, output_file)
        self.__free_image(img_ptr)
        self.__free_image(gray_ptr)
        self.__free_image(sobel_ptr)