import ctypes
import os

class CImage(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.POINTER(ctypes.c_ubyte)),
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("channels", ctypes.c_int)
    ]

class CudaImageLib:
    def __init__(self):
        """
        Inicializa la librería compartida C/CUDA.
        :param lib_path: Ruta al archivo .so compilado.
        """
        lib_path = os.path.abspath('./bin/libfilterscuda.so')
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"Shared library was not found in {lib_path}")
        
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

        self.lib.Sobel.argtypes = [ctypes.POINTER(CImage)]
        self.lib.Sobel.restype = ctypes.POINTER(CImage)

    def __load_image(self, filename: str):
        """Carga una imagen y devuelve un puntero a CImage."""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Not found {filename} image.")
        return self.lib.image2arr(filename.encode('utf-8'))

    def __save_image(self, img_ptr, filename: str):
        """Guarda la imagen apuntada por img_ptr en el disco."""
        self.lib.saveImg(img_ptr, filename.encode('utf-8'))

    def __free_image(self, img_ptr):
        """Libera la memoria de la imagen."""
        if img_ptr:
            self.lib.freeImage(img_ptr)

    def rgb_to_gray(self, filename: str, output_file:str):
        """Aplica filtro RGB a Escala de Grises."""
        img_ptr = self.__load_image(filename)
        img_ptr = self.lib.rgb2gray(img_ptr)
        self.__save_image(img_ptr, output_file)
        self.__free_image(img_ptr)

    def gaussian_blur(self, filename:str, output_file:str, kernel_dim:int=7, stdev:float=2.0):
        """Aplica filtro Gaussian Blur."""
        img_ptr = self.__load_image(filename)
        img_ptr = self.lib.GaussianBlur(img_ptr, kernel_dim, stdev)
        self.__save_image(img_ptr, output_file)
        self.__free_image(img_ptr)

    def sobel(self, filename:str, output_file:str):
        """Aplica filtro de detección de bordes Sobel."""
        img_ptr = self.__load_image(filename)
        gray_ptr = self.lib.rgb2gray(img_ptr)
        img_ptr = self.lib.Sobel(gray_ptr)
        self.__save_image(img_ptr, output_file)
        self.__free_image(img_ptr)
        self.__free_image(gray_ptr)