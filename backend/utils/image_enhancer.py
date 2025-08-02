"""
Mejorador de imágenes UNIFICADO - Lo mejor de ambos sistemas.
Usa solo OpenCV y PIL para garantizar compatibilidad.
"""
import cv2
import numpy as np
from PIL import Image
import io
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

class ImageEnhancer:
    """Mejorador unificado de imágenes para OCR."""
    
    def __init__(self):
        self.debug_enabled = True
        logger.info("ImageEnhancer inicializado")

    def enhance_scanned_document(self, image_data: bytes, strategy: str = "auto") -> np.ndarray:
        """
        Pipeline unificado de mejora de imagen.
        
        Args:
            image_data: Datos binarios de la imagen
            strategy: "auto", "aggressive", "conservative", "document"
        """
        try:
            # 1. Cargar y preparar imagen
            image = self._load_and_prepare_image(image_data)
            logger.info(f"Imagen cargada: {image.shape}")
            
            # 2. Análisis de calidad para estrategia automática
            if strategy == "auto":
                quality_metrics = self._analyze_image_quality(image)
                strategy = self._select_optimal_strategy(quality_metrics)
                logger.info(f"Estrategia seleccionada: {strategy} (calidad detectada)")
            
            # 3. Aplicar pipeline según estrategia
            enhanced = self._apply_enhancement_strategy(image, strategy)
            
            logger.info(f"Mejora completada con estrategia: {strategy}")
            return enhanced
            
        except Exception as e:
            logger.error(f"Error en mejora de imagen: {e}")
            return self._emergency_fallback(image_data)
    
    def _load_and_prepare_image(self, image_data: bytes) -> np.ndarray:
        """Cargar y preparar imagen de forma robusta."""
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("No se pudo decodificar la imagen")
        
        # Redimensionar si es necesario (usando el mejor método de ambos)
        height, width = image.shape[:2]
        if width < 2000:
            # Factor de escala inteligente
            scale_factor = max(2.0, 2000 / width)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
            logger.info(f"Imagen redimensionada: {width}x{height} → {new_width}x{new_height}")
        
        return image
    
    def _analyze_image_quality(self, image: np.ndarray) -> Dict[str, float]:
        """Análisis unificado de calidad de imagen."""
        # Convertir a escala de grises para análisis
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Métricas básicas
        contrast = np.std(gray)
        brightness = np.mean(gray)
        
        # Detección de ruido (Laplaciano)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Análisis de histograma
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_peaks = self._analyze_histogram_peaks(hist)
        
        # Detección de texto vs imagen
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        return {
            'contrast': contrast,
            'brightness': brightness,
            'noise_level': laplacian_var,
            'is_noisy': laplacian_var < 100,
            'is_dark': brightness < 100,
            'is_light': brightness > 180,
            'is_low_contrast': contrast < 30,
            'hist_peaks': hist_peaks,
            'edge_density': edge_density,
            'likely_text': edge_density > 0.1 and contrast > 20
        }
    
    def _select_optimal_strategy(self, quality: Dict[str, float]) -> str:
        """Seleccionar estrategia óptima - SIEMPRE agresiva para documentos escaneados."""
        # CAMBIO CRÍTICO: Para documentos escaneados, siempre usar estrategia agresiva
        logger.info(f"Calidad detectada: {quality}")
        
        # Para cualquier documento con problemas, usar agresivo
        if (quality['is_dark'] or quality['is_light'] or 
            quality['is_low_contrast'] or quality['is_noisy'] or
            quality['contrast'] < 50):
            strategy = "aggressive"
        else:
            # Incluso para documentos "buenos", usar agresivo si hay dudas
            strategy = "aggressive"
        
        logger.info(f"Estrategia seleccionada: {strategy}")
        return strategy

    def _apply_enhancement_strategy(self, image: np.ndarray, strategy: str) -> np.ndarray:
        """Aplicar estrategia de mejora específica."""
        # Convertir a escala de grises
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        if strategy == "aggressive":
            return self._apply_aggressive_enhancement(gray)
        elif strategy == "document":
            return self._document_enhancement(gray)
        elif strategy == "conservative":
            return self._conservative_enhancement(gray)
        else:
            return self._balanced_enhancement(gray)
    
    def _apply_aggressive_enhancement(self, image: np.ndarray) -> np.ndarray:
        """Mejora agresiva optimizada para documentos muy problemáticos."""
        try:
            logger.info("Aplicando mejora agresiva optimizada")
            
            # 1. Conversión a escala de grises si es necesario
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            # 2. Redimensionar si la imagen es muy grande (optimización)
            height, width = gray.shape
            if height > 2000 or width > 2000:
                scale = min(2000/height, 2000/width)
                new_height, new_width = int(height * scale), int(width * scale)
                gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
                logger.info(f"Imagen redimensionada de {width}x{height} a {new_width}x{new_height}")
            
            # 3. Eliminación de ruido MUY agresiva
            denoised = cv2.fastNlMeansDenoising(gray, None, 15, 7, 21)  # Parámetros más fuertes
            
            # 4. CLAHE muy agresivo
            clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(4,4))  # Más agresivo
            enhanced = clahe.apply(denoised)
            
            # 5. Corrección gamma adaptativa
            gamma = self._calculate_optimal_gamma(enhanced)
            gamma_corrected = self._apply_gamma_correction(enhanced, gamma)
            
            # 6. Sharpening muy fuerte
            kernel = np.array([[-1,-1,-1],
                              [-1, 12,-1],
                              [-1,-1,-1]])  # Kernel más agresivo
            sharpened = cv2.filter2D(gamma_corrected, -1, kernel)
            
            # 7. Binarización múltiple con votación
            # Otsu
            _, binary1 = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Adaptativa
            binary2 = cv2.adaptiveThreshold(sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                          cv2.THRESH_BINARY, 15, 8)
            
            # Media simple
            mean_val = np.mean(sharpened)
            _, binary3 = cv2.threshold(sharpened, mean_val, 255, cv2.THRESH_BINARY)
            
            # Votación: cada pixel se decide por mayoría
            vote = (binary1.astype(np.float32) + binary2.astype(np.float32) + binary3.astype(np.float32)) / 3
            final_binary = (vote > 127).astype(np.uint8) * 255
            
            # 8. Limpieza morfológica final
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
            cleaned = cv2.morphologyEx(final_binary, cv2.MORPH_CLOSE, kernel)
            cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
            
            logger.info("Mejora agresiva completada exitosamente")
            return cleaned
            
        except Exception as e:
            logger.error(f"Error en mejora agresiva: {e}")
            # Fallback: al menos binarización básica
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return binary

    def _calculate_optimal_gamma(self, image: np.ndarray) -> float:
        """Calcular gamma óptimo para la imagen."""
        # Calcular histograma
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        
        # Encontrar percentiles
        total_pixels = image.shape[0] * image.shape[1]
        cumsum = np.cumsum(hist)
        
        # Percentiles 25 y 75
        p25_idx = np.where(cumsum >= total_pixels * 0.25)[0][0]
        p75_idx = np.where(cumsum >= total_pixels * 0.75)[0][0]
        
        # Calcular gamma basado en la distribución
        if p25_idx < 85:  # Imagen muy oscura
            gamma = 0.7
        elif p75_idx > 170:  # Imagen muy clara
            gamma = 1.3
        else:
            # Gamma adaptativo
            gamma = 1.0 + (128 - np.mean(image)) / 256
        
        # Limitar gamma a rango razonable
        gamma = max(0.5, min(2.0, gamma))
        logger.debug(f"Gamma calculado: {gamma:.2f}")
        return gamma
    
    def _document_enhancement(self, gray: np.ndarray) -> np.ndarray:
        """Pipeline optimizado para documentos de texto."""
        logger.info("Aplicando mejora para documentos...")
        
        # 1. Corrección gamma moderada
        gamma_corrected = self._apply_gamma_correction(gray, 0.8)
        
        # 2. Eliminación de ruido preservando texto
        denoised = cv2.bilateralFilter(gamma_corrected, 9, 75, 75)
        
        # 3. CLAHE moderado
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        contrast_enhanced = clahe.apply(denoised)
        
        # 4. Corrección de inclinación precisa
        angle_corrected = self._correct_skew_robust(contrast_enhanced)
        
        # 5. Sharpening suave
        sharpened = self._apply_gentle_sharpening(angle_corrected)
        
        # 6. Binarización adaptativa
        binary = cv2.adaptiveThreshold(
            sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 15, 10
        )
        
        # 7. Limpieza morfológica suave
        final = self._morphological_cleanup_gentle(binary)
        
        return final
    
    def _conservative_enhancement(self, gray: np.ndarray) -> np.ndarray:
        """Pipeline conservador para imágenes de buena calidad."""
        logger.info("Aplicando mejora conservadora...")
        
        # 1. CLAHE suave
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # 2. Corrección de inclinación
        angle_corrected = self._correct_skew_robust(enhanced)
        
        # 3. Binarización Otsu simple
        _, binary = cv2.threshold(angle_corrected, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 4. Limpieza mínima
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        final = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return final
    
    def _balanced_enhancement(self, gray: np.ndarray) -> np.ndarray:
        """Pipeline balanceado (por defecto)."""
        logger.info("Aplicando mejora balanceada...")
        
        # Combinación de los mejores aspectos
        gamma_corrected = self._apply_gamma_correction(gray, 0.7)
        denoised = cv2.fastNlMeansDenoising(gamma_corrected, None, 20, 7, 21)
        
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(6,6))
        contrast_enhanced = clahe.apply(denoised)
        
        angle_corrected = self._correct_skew_robust(contrast_enhanced)
        sharpened = self._apply_gentle_sharpening(angle_corrected)
        binary = self._multi_method_binarization_standard(sharpened)
        final = self._morphological_cleanup_gentle(binary)
        
        return final
    
    # ========== MÉTODOS AUXILIARES UNIFICADOS ==========
    
    def _apply_gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        """Aplicar corrección gamma."""
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        corrected = cv2.LUT(image, table)
        logger.debug(f"Gamma {gamma:.2f} aplicado")
        return corrected
    
    def _correct_skew_robust(self, image: np.ndarray) -> np.ndarray:
        """Corrección robusta de inclinación (mejor método de ambos)."""
        try:
            # Método Hough Lines (más preciso)
            edges = cv2.Canny(image, 50, 150, apertureSize=3)
            lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
            
            if lines is not None and len(lines) > 5:
                angles = []
                for line in lines[:20]:
                    rho, theta = line[0]
                    angle = theta * 180 / np.pi - 90
                    if -15 < angle < 15:
                        angles.append(angle)
                
                if angles:
                    median_angle = np.median(angles)
                    if abs(median_angle) > 0.3:
                        return self._rotate_image(image, median_angle)
            
        except Exception as e:
            logger.debug(f"Error en corrección Hough: {e}")
        
        return image
    
    def _rotate_image(self, image: np.ndarray, angle: float) -> np.ndarray:
        """Rotar imagen de forma robusta."""
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        rotated = cv2.warpAffine(
            image, rotation_matrix, (w, h),
            flags=cv2.INTER_CUBIC, 
            borderMode=cv2.BORDER_REPLICATE
        )
        
        logger.info(f"Imagen rotada {angle:.2f} grados")
        return rotated
    
    def _apply_aggressive_sharpening(self, image: np.ndarray) -> np.ndarray:
        """Sharpening agresivo."""
        # Kernel agresivo
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpened = cv2.filter2D(image, -1, kernel)
        
        # Unsharp mask adicional
        gaussian = cv2.GaussianBlur(image, (5, 5), 0)
        unsharp_mask = cv2.addWeighted(image, 1.8, gaussian, -0.8, 0)
        
        # Combinar
        final = cv2.addWeighted(sharpened, 0.7, unsharp_mask, 0.3, 0)
        return final
    
    def _apply_gentle_sharpening(self, image: np.ndarray) -> np.ndarray:
        """Sharpening suave."""
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        return cv2.filter2D(image, -1, kernel)
    
    def _multi_method_binarization_extended(self, image: np.ndarray) -> np.ndarray:
        """Binarización con 5 métodos (versión extendida)."""
        methods = []
        
        # Método 1: Otsu
        _, otsu = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        methods.append(otsu // 255)
        
        # Método 2: Adaptativo Gaussiano
        adaptive_gauss = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 8
        )
        methods.append(adaptive_gauss // 255)
        
        # Método 3: Adaptativo Media
        adaptive_mean = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 8
        )
        methods.append(adaptive_mean // 255)
        
        # Método 4: Histograma
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        threshold = self._find_optimal_threshold(hist)
        _, manual = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        methods.append(manual // 255)
        
        # Método 5: Triangle
        _, triangle = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
        methods.append(triangle // 255)
        
        # Votación por mayoría (3 de 5)
        votes = np.sum(methods, axis=0)
        combined = np.zeros_like(otsu)
        combined[votes >= 3] = 255
        
        return combined
    
    def _multi_method_binarization_standard(self, image: np.ndarray) -> np.ndarray:
        """Binarización estándar con 3 métodos."""
        # Otsu
        _, otsu = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Adaptativo
        adaptive = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 10
        )
        
        # Combinar (mayoría de 2)
        combined = np.zeros_like(otsu)
        votes = (otsu // 255) + (adaptive // 255)
        combined[votes >= 1] = 255  # Más permisivo
        
        return combined
    
    def _morphological_cleanup_aggressive(self, binary: np.ndarray) -> np.ndarray:
        """Limpieza morfológica agresiva."""
        # Eliminar ruido
        kernel_noise = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_noise)
        
        # Cerrar gaps
        kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close)
        
        # Engrosar caracteres
        kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilated = cv2.dilate(closed, kernel_dilate, iterations=1)
        
        return dilated
    
    def _morphological_cleanup_gentle(self, binary: np.ndarray) -> np.ndarray:
        """Limpieza morfológica suave."""
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel_open)
        
        return opened
    
    def _find_optimal_threshold(self, histogram: np.ndarray) -> int:
        """Encontrar umbral óptimo."""
        hist_smooth = cv2.GaussianBlur(histogram.astype(np.float32), (5, 1), 0)
        
        min_val = float('inf')
        min_idx = 128
        
        for i in range(50, 200):
            if hist_smooth[i][0] < min_val:
                min_val = hist_smooth[i][0]
                min_idx = i
        
        return min_idx
    
    def _analyze_histogram_peaks(self, histogram: np.ndarray) -> Dict[str, Any]:
        """Analizar picos del histograma."""
        hist_flat = histogram.flatten()
        peaks = []
        
        for i in range(1, len(hist_flat) - 1):
            if hist_flat[i] > hist_flat[i-1] and hist_flat[i] > hist_flat[i+1]:
                if hist_flat[i] > np.max(hist_flat) * 0.1:  # Solo picos significativos
                    peaks.append(i)
        
        return {
            'num_peaks': len(peaks),
            'peaks': peaks[:5],  # Solo primeros 5
            'is_bimodal': len(peaks) == 2,
            'is_multimodal': len(peaks) > 2
        }
    
    def _emergency_fallback(self, image_data: bytes) -> np.ndarray:
        """Fallback de emergencia ultrarrápido."""
        try:
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
            
            if image is None:
                return np.ones((100, 100), dtype=np.uint8) * 255
            
            # Solo CLAHE + Otsu
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(image)
            _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            logger.warning("Usando fallback de emergencia")
            return binary
            
        except Exception as e:
            logger.error(f"Error en fallback de emergencia: {e}")
            return np.ones((100, 100), dtype=np.uint8) * 255

# Instancia global
image_enhancer = ImageEnhancer()
# Auto-generated comment - 20:13:37
