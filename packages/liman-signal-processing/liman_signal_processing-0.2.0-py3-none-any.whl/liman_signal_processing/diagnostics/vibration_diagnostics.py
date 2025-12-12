"""
Модуль для вибродиагностики - обнаружение дефектов в спектрах вибрации.

Использует RuleBasedDefectDetector для анализа дефектов на основе JSON-структуры правил.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Union
import numpy as np


@dataclass
class EquipmentFrequencies:
    """
    Базовые частоты оборудования для вычисления целевых частот правил.
    
    :param shaft: Частота вращения ротора/вала (Гц)
    :param network_frequency: Частота питающей сети (Гц)
    :param bpfo: Ball Pass Frequency Outer для подшипника (Гц)
    :param bpfi: Ball Pass Frequency Inner для подшипника (Гц)
    :param bsf: Ball Spin Frequency для подшипника (Гц)
    :param ftf: Fundamental Train Frequency для подшипника (Гц)
    :param belt_belt: Частота ремня (Гц)
    :param belt_driving: Частота ведущего шкива (Гц)
    :param belt_driven: Частота ведомого шкива (Гц)
    :param blades: Лопастная частота (Гц)
    """
    shaft: float
    network_frequency: float = None
    bpfo: Optional[float] = None
    bpfi: Optional[float] = None
    bsf: Optional[float] = None
    ftf: Optional[float] = None
    belt_belt: Optional[float] = None
    belt_driving: Optional[float] = None
    belt_driven: Optional[float] = None
    blades: Optional[float] = None
    
    def get_frequency(self, frequency_type: str) -> float:
        """
        Получает базовую частоту по типу.
        
        :param frequency_type: Тип частоты ('shaft', 'bpfo', 'custom', и т.д.)
        :return: Значение частоты в Гц
        :raises ValueError: Если тип частоты неизвестен или не задан
        """
        frequency_map = {
            'shaft': self.shaft,
            'network_frequency': self.network_frequency,
            'bpfo': self.bpfo,
            'bpfi': self.bpfi,
            'bsf': self.bsf,
            'ftf': self.ftf,
            'belt_belt': self.belt_belt,
            'belt_driving': self.belt_driving,
            'belt_driven': self.belt_driven,
            'blades': self.blades,
        }
        
        if frequency_type not in frequency_map:
            raise ValueError(f"Неизвестный тип частоты: {frequency_type}")
        
        frequency = frequency_map[frequency_type]
        if frequency is None:
            raise ValueError(f"Частота {frequency_type} не задана")
        
        return frequency


@dataclass
class RuleEvaluationResult:
    """
    Результат оценки одного правила.
    
    :param rule_id: ID правила
    :param passed: Правило выполнено или нет
    :param details: Детали оценки правила
    :param frequencies_found: Найденные частоты с амплитудами
    :param defect_strength_amplitude: Амплитуда для определения силы дефекта (если useForDefectStrength=True)
    """
    rule_id: str
    passed: bool
    details: Dict[str, Any]
    frequencies_found: List[Dict[str, Any]] = None
    defect_strength_amplitude: Optional[float] = None
    
    def __post_init__(self):
        if self.frequencies_found is None:
            self.frequencies_found = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует результат в JSON-сериализуемый словарь."""
        return {
            'rule_id': self.rule_id,
            'passed': bool(self.passed) if isinstance(self.passed, (np.bool_, bool)) else self.passed,
            'details': self._convert_to_native(self.details),
            'frequencies_found': [self._convert_to_native(f) for f in self.frequencies_found],
            'defect_strength_amplitude': float(self.defect_strength_amplitude) if self.defect_strength_amplitude is not None else None
        }
    
    @staticmethod
    def _convert_to_native(obj: Any) -> Any:
        """Преобразует numpy типы в нативные Python типы."""
        if isinstance(obj, (np.integer, np.floating)):
            return float(obj) if isinstance(obj, np.floating) else int(obj)
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, dict):
            return {k: RuleEvaluationResult._convert_to_native(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [RuleEvaluationResult._convert_to_native(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj


@dataclass
class GroupEvaluationResult:
    """
    Результат оценки группы правил.
    
    :param group_id: ID группы
    :param passed: Группа выполнена или нет
    :param operator: Оператор группы ('AND' или 'OR')
    :param element_results: Результаты элементов группы
    """
    group_id: str
    passed: bool
    operator: str
    element_results: List[Union['RuleEvaluationResult', 'GroupEvaluationResult']] = None
    
    def __post_init__(self):
        if self.element_results is None:
            self.element_results = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует результат в JSON-сериализуемый словарь."""
        return {
            'group_id': self.group_id,
            'passed': bool(self.passed) if isinstance(self.passed, (np.bool_, bool)) else self.passed,
            'operator': self.operator,
            'element_results': [elem.to_dict() for elem in self.element_results]
        }


@dataclass
class DefectEvaluationResult:
    """
    Результат полной оценки дефекта по правилам.
    
    :param detected: Дефект обнаружен
    :param defect_strength: Сила дефекта (на основе правил с useForDefectStrength)
    :param root_group_result: Результат оценки корневой группы
    :param all_frequencies_found: Все найденные частоты
    """
    detected: bool
    defect_strength: Optional[str] = None  # 'low', 'medium', 'high'
    root_group_result: Optional[GroupEvaluationResult] = None
    all_frequencies_found: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.all_frequencies_found is None:
            self.all_frequencies_found = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует результат в JSON-сериализуемый словарь."""
        result = {
            'detected': bool(self.detected) if isinstance(self.detected, (np.bool_, bool)) else self.detected,
            'defect_strength': self.defect_strength,
            'all_frequencies_found': [RuleEvaluationResult._convert_to_native(f) for f in self.all_frequencies_found]
        }
        if self.root_group_result is not None:
            result['root_group_result'] = self.root_group_result.to_dict()
        return result


@dataclass
class HarmonicInfo:
    """
    Информация о гармонике.
    
    :param frequency_type: Тип частоты (shaft, bpfo, custom и т.д.)
    :param multiplier: Кратность частоты
    :param expected_frequency: Ожидаемая частота (Гц)
    :param actual_frequency: Найденная частота (Гц) или None
    :param amplitude_db: Амплитуда в дБ или None
    :param delta_l: Высота пика над уровнем шума в дБ (amplitude_db - noise_level_db) или None
    :param modulation: Модуляция в % (только для огибающей) или None
    :param template_criterion_value: Значение критерия "Эталон" в дБ (текущая - эталонная амплитуда) или None
    :param sideband_criterion_value: Значение критерия "Основная/боковая" в дБ (основная - боковая амплитуда) или None (только для боковых полос)
    :param used_for_template_criterion: Сила дефекта, если эта гармоника использована для определения общего значения критерия "Эталон" (None если не использована)
    :param used_for_sideband_criterion: Сила дефекта, если эта гармоника использована для определения общего значения критерия "Основная/боковая" (None если не использована)
    :param used_for_modulation_criterion: Сила дефекта, если эта гармоника использована для определения общего значения критерия "Модуляция" (None если не использована)
    :param is_present: Должна ли частота присутствовать (True/False/None)
    :param passed: Правило выполнено
    :param use_for_defect_strength: Учитывается ли в силе дефекта
    :param offset: Смещение для боковых полос (если применимо)
    :param harmonic_type: Тип гармоники: 'main', 'comparison', 'sideband', 'sideband_comparison'
    :param main_expected_frequency: Ожидаемая частота основной гармоники (только для боковых полос)
    :param main_actual_frequency: Найденная частота основной гармоники (только для боковых полос)
    :param main_amplitude_db: Амплитуда основной гармоники в дБ (только для боковых полос)
    :param main_frequency_type: Тип частоты основной гармоники (только для боковых полос)
    :param main_multiplier: Множитель основной гармоники (только для боковых полос)
    """
    frequency_type: str
    multiplier: float
    expected_frequency: float
    actual_frequency: Optional[float] = None
    amplitude_db: Optional[float] = None
    delta_l: Optional[float] = None  # Высота пика над уровнем шума
    modulation: Optional[float] = None  # Модуляция в % (только для огибающей)
    template_criterion_value: Optional[float] = None  # Критерий "Эталон" в дБ (только для спектра)
    sideband_criterion_value: Optional[float] = None  # Критерий "Основная/боковая" в дБ (только для боковых полос)
    used_for_template_criterion: Optional[str] = None  # Сила дефекта, если использована для общего значения критерия "Эталон"
    used_for_sideband_criterion: Optional[str] = None  # Сила дефекта, если использована для общего значения критерия "Основная/боковая"
    used_for_modulation_criterion: Optional[str] = None  # Сила дефекта, если использована для общего значения критерия "Модуляция"
    is_present: Optional[bool] = None
    passed: bool = False
    use_for_defect_strength: bool = False
    offset: Optional[int] = None
    harmonic_type: str = 'main'
    main_expected_frequency: Optional[float] = None  # Ожидаемая частота основной гармоники (только для боковых полос)
    main_actual_frequency: Optional[float] = None  # Найденная частота основной гармоники (только для боковых полос)
    main_amplitude_db: Optional[float] = None  # Амплитуда основной гармоники в дБ (только для боковых полос)
    main_frequency_type: Optional[str] = None  # Тип частоты основной гармоники (только для боковых полос)
    main_multiplier: Optional[float] = None  # Множитель основной гармоники (только для боковых полос)
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует в словарь."""
        result = {
            'frequency_type': self.frequency_type,
            'multiplier': float(self.multiplier),
            'expected_frequency': float(self.expected_frequency),
            'actual_frequency': float(self.actual_frequency) if self.actual_frequency is not None else None,
            'amplitude_db': float(self.amplitude_db) if self.amplitude_db is not None else None,
            'delta_l': float(self.delta_l) if self.delta_l is not None else None,
            'modulation': float(self.modulation) if self.modulation is not None else None,
            'template_criterion_value': float(self.template_criterion_value) if self.template_criterion_value is not None else None,
            'sideband_criterion_value': float(self.sideband_criterion_value) if self.sideband_criterion_value is not None else None,
            'used_for_template_criterion': self.used_for_template_criterion,
            'used_for_sideband_criterion': self.used_for_sideband_criterion,
            'used_for_modulation_criterion': self.used_for_modulation_criterion,
            'is_present': self.is_present,
            'passed': bool(self.passed),
            'use_for_defect_strength': self.use_for_defect_strength,
            'offset': self.offset,
            'harmonic_type': self.harmonic_type
        }
        # Добавляем информацию об основной гармонике для боковых полос
        if self.harmonic_type in ('sideband', 'sideband_comparison'):
            result['main_expected_frequency'] = float(self.main_expected_frequency) if self.main_expected_frequency is not None else None
            result['main_actual_frequency'] = float(self.main_actual_frequency) if self.main_actual_frequency is not None else None
            result['main_amplitude_db'] = float(self.main_amplitude_db) if self.main_amplitude_db is not None else None
            result['main_frequency_type'] = self.main_frequency_type
            result['main_multiplier'] = float(self.main_multiplier) if self.main_multiplier is not None else None
        return result


@dataclass
class DefectDetectionReport:
    """
    Отчет о дефекте с полной информацией.
    
    :param defect_name: Название дефекта
    :param detected: Дефект обнаружен
    :param defect_strength: Сила дефекта ('weak', 'medium', 'strong' или None)
    :param spectrum_detected: Дефект обнаружен в спектре (только для объединенного отчета)
    :param envelope_detected: Дефект обнаружен в огибающей (только для объединенного отчета)
    :param spectrum_defect_strength: Сила дефекта в спектре (только для объединенного отчета)
    :param envelope_defect_strength: Сила дефекта в огибающей (только для объединенного отчета)
    :param sideband_thresholds: Пороговые значения критерия "Основная/боковая" (дБ) - только для спектра
    :param template_thresholds: Пороговые значения критерия "Эталон" (дБ) - только для спектра с эталоном
    :param modulation_thresholds: Пороговые значения критерия "Модуляция" (%) - только для огибающей
    :param modulation: Вычисленное значение модуляции (%) - только для огибающей
    :param sideband_criterion_value: Общее значение критерия "Основная/боковая" (дБ) - минимальное из прошедших правил
    :param template_criterion_value: Общее значение критерия "Эталон" (дБ) - максимальное из всех гармоник
    :param recommendation: Рекомендация
    :param harmonics: Плоский список гармоник с информацией (для обратной совместимости)
    :param spectrum_harmonics: Гармоники из спектра
    :param envelope_harmonics: Гармоники из спектра огибающей
    """
    defect_name: str
    detected: bool
    defect_strength: Optional[str] = None
    spectrum_detected: Optional[bool] = None  # Только для объединенного отчета
    envelope_detected: Optional[bool] = None  # Только для объединенного отчета
    spectrum_defect_strength: Optional[str] = None  # Только для объединенного отчета
    envelope_defect_strength: Optional[str] = None  # Только для объединенного отчета
    sideband_thresholds: Optional[Dict[str, Any]] = None
    template_thresholds: Optional[Dict[str, Any]] = None
    modulation_thresholds: Optional[Dict[str, Any]] = None
    modulation: Optional[float] = None
    sideband_criterion_value: Optional[float] = None  # Минимальное из прошедших правил
    template_criterion_value: Optional[float] = None  # Максимальное из всех гармоник
    recommendation: Optional[str] = None
    harmonics: List[HarmonicInfo] = None
    spectrum_harmonics: List[HarmonicInfo] = None
    envelope_harmonics: List[HarmonicInfo] = None
    
    def __post_init__(self):
        if self.harmonics is None:
            self.harmonics = []
        if self.spectrum_harmonics is None:
            self.spectrum_harmonics = []
        if self.envelope_harmonics is None:
            self.envelope_harmonics = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует отчет в JSON-сериализуемый словарь."""
        result = {
            'defect': self.defect_name,
            'detected': bool(self.detected) if isinstance(self.detected, (np.bool_, bool)) else self.detected,
            'defect_strength': self.defect_strength,
            'spectrum_detected': bool(self.spectrum_detected) if self.spectrum_detected is not None and isinstance(self.spectrum_detected, (np.bool_, bool)) else self.spectrum_detected,
            'envelope_detected': bool(self.envelope_detected) if self.envelope_detected is not None and isinstance(self.envelope_detected, (np.bool_, bool)) else self.envelope_detected,
            'spectrum_defect_strength': self.spectrum_defect_strength,
            'envelope_defect_strength': self.envelope_defect_strength,
            'recommendation': self.recommendation
        }
        
        # Добавляем гармоники по типам спектров
        if self.spectrum_harmonics:
            result['spectrum_harmonics'] = [h.to_dict() for h in self.spectrum_harmonics]
        if self.envelope_harmonics:
            result['envelope_harmonics'] = [h.to_dict() for h in self.envelope_harmonics]
        
        # Для обратной совместимости добавляем общий список гармоник, если есть только один тип
        if not self.spectrum_harmonics and not self.envelope_harmonics and self.harmonics:
            result['harmonics'] = [h.to_dict() for h in self.harmonics]
        
        # Добавляем только непустые границы по критериям
        if self.sideband_thresholds:
            result['sideband_thresholds'] = RuleEvaluationResult._convert_to_native(self.sideband_thresholds)
        if self.template_thresholds:
            result['template_thresholds'] = RuleEvaluationResult._convert_to_native(self.template_thresholds)
        if self.modulation_thresholds:
            result['modulation_thresholds'] = RuleEvaluationResult._convert_to_native(self.modulation_thresholds)
        # Всегда включаем значения критериев, даже если они None
        result['modulation'] = float(self.modulation) if self.modulation is not None else None
        result['sideband_criterion_value'] = float(self.sideband_criterion_value) if self.sideband_criterion_value is not None else None
        result['template_criterion_value'] = float(self.template_criterion_value) if self.template_criterion_value is not None else None
        
        return result


class RuleBasedDefectDetector:
    """
    Класс для обнаружения дефектов на основе JSON-структуры правил.
    
    Поддерживает:
    - Простые правила спектра (присутствие/отсутствие частоты)
    - Правила с пользовательскими частотами
    - Правила с сравнением частот
    - Правила с боковыми полосами
    - Группы правил с операторами AND/OR
    - Определение силы дефекта
    
    Пример использования:
        >>> detector = RuleBasedDefectDetector()
        >>> 
        >>> # Базовые частоты оборудования
        >>> equipment_freqs = EquipmentFrequencies(
        ...     shaft=25.0,
        ...     bpfo=125.0
        ... )
        >>> 
        >>> # Правила в формате JSON
        >>> rules_json = {
        ...     "rootGroup": {
        ...         "type": "group",
        ...         "id": "root",
        ...         "operator": "AND",
        ...         "elements": [...]
        ...     }
        ... }
        >>> 
        >>> # Оценка правил
        >>> result = detector.evaluate_rules(
        ...     rules=rules_json,
        ...     frequencies=spectrum_frequencies,
        ...     spectrum_db=spectrum_db,
        ...     equipment_frequencies=equipment_freqs,
        ...     noise_threshold_db=30.0
        ... )
    """
    
    def __init__(self, frequency_tolerance_hz: float = 0.5):
        """
        Инициализация детектора.
        
        :param frequency_tolerance_hz: Допустимое отклонение частоты при поиске (Гц)
        """
        self.frequency_tolerance_hz = frequency_tolerance_hz
    
    def evaluate_rules(
        self,
        rules: Dict[str, Any],
        frequencies: np.ndarray,
        spectrum_db: np.ndarray,
        equipment_frequencies: EquipmentFrequencies,
        noise_threshold_db: float = 10.0,
        reference_spectrum_db: Optional[np.ndarray] = None,
        frequency_resolution: Optional[float] = None,
        filter_bandwidth: Optional[float] = None,
        spectrum_type: str = 'spectrum'  # 'spectrum' или 'envelope'
    ) -> DefectEvaluationResult:
        """
        Оценивает правила дефекта на основе спектральных данных.
        
        :param rules: JSON-структура правил с корневой группой
        :param frequencies: Массив частот спектра (Гц)
        :param spectrum_db: Массив значений спектра в децибелах
        :param equipment_frequencies: Базовые частоты оборудования
        :param noise_threshold_db: Порог превышения над уровнем шума в дБ (по умолчанию 10 дБ)
        :param reference_spectrum_db: Эталонный спектр в дБ (для критерия "эталон")
        :param frequency_resolution: Разрешение по частоте Δf_a (Гц) для критерия "модуляция"
        :param filter_bandwidth: Ширина полосы фильтра Δf_w (Гц) для критерия "модуляция"
        :param spectrum_type: Тип спектра ('spectrum' или 'envelope')
        :return: Результат оценки дефекта
        """
        if 'rootGroup' not in rules:
            raise ValueError("Правила должны содержать 'rootGroup'")
        
        # Вычисляем полином для уровня шума спектра
        noise_poly = self._calculate_noise_level(frequencies, spectrum_db)
        
        root_group = rules['rootGroup']
        root_result = self._evaluate_group(
            root_group,
            frequencies,
            spectrum_db,
            equipment_frequencies,
            noise_threshold_db,
            noise_poly
        )
        
        # Собираем все найденные частоты
        all_frequencies = self._collect_all_frequencies(root_result)
        
        # Определяем, обнаружен ли дефект на основе правил с useForDefectStrength=True
        # Дефект считается обнаруженным только если:
        # 1. Выполнено хотя бы одно правило с useForDefectStrength=True
        # 2. И есть хотя бы один применимый критерий для определения силы дефекта
        rules_passed = self._check_defect_detected_by_strength_rules(root_result, rules)
        has_applicable_criteria = self._has_applicable_criteria(
            rules, spectrum_type=spectrum_type,
            reference_spectrum_db=reference_spectrum_db,
            frequency_resolution=frequency_resolution,
            filter_bandwidth=filter_bandwidth
        )
        detected = rules_passed and has_applicable_criteria
        
        return DefectEvaluationResult(
            detected=detected,
            defect_strength=None,  # Будет вычислено позже
            root_group_result=root_result,
            all_frequencies_found=all_frequencies
        )
    
    def _evaluate_group(
        self,
        group: Dict[str, Any],
        frequencies: np.ndarray,
        spectrum_db: np.ndarray,
        equipment_frequencies: EquipmentFrequencies,
        noise_threshold_db: float,
        noise_poly: np.poly1d
    ) -> GroupEvaluationResult:
        """Оценивает группу правил."""
        if group.get('type') != 'group':
            raise ValueError("Ожидается группа правил")
        
        group_id = group.get('id', 'unknown')
        operator = group.get('operator', 'AND')
        elements = group.get('elements', [])
        
        if not elements:
            # Пустая группа считается невыполненной
            return GroupEvaluationResult(
                group_id=group_id,
                passed=False,
                operator=operator,
                element_results=[]
            )
        
        element_results = []
        for element in elements:
            if element.get('type') == 'group':
                result = self._evaluate_group(
                    element, frequencies, spectrum_db,
                    equipment_frequencies, noise_threshold_db, noise_poly
                )
            elif element.get('type') == 'rule':
                if element.get('ruleType') == 'spectrum':
                    result = self._evaluate_spectrum_rule(
                        element, frequencies, spectrum_db,
                        equipment_frequencies, noise_threshold_db, noise_poly
                    )
                elif element.get('ruleType') == 'trend':
                    # Трендовые правила пока не реализованы
                    result = RuleEvaluationResult(
                        rule_id=element.get('id', 'unknown'),
                        passed=False,
                        details={'error': 'Trend rules not implemented yet'}
                    )
                else:
                    result = RuleEvaluationResult(
                        rule_id=element.get('id', 'unknown'),
                        passed=False,
                        details={'error': f"Unknown rule type: {element.get('ruleType')}"}
                    )
            else:
                result = RuleEvaluationResult(
                    rule_id='unknown',
                    passed=False,
                    details={'error': f"Unknown element type: {element.get('type')}"}
                )
            
            element_results.append(result)
        
        # Применяем оператор группы
        if operator == 'AND':
            passed = all(r.passed for r in element_results)
        elif operator == 'OR':
            passed = any(r.passed for r in element_results)
        else:
            raise ValueError(f"Неизвестный оператор: {operator}")
        
        return GroupEvaluationResult(
            group_id=group_id,
            passed=passed,
            operator=operator,
            element_results=element_results
        )
    
    def _evaluate_spectrum_rule(
        self,
        rule: Dict[str, Any],
        frequencies: np.ndarray,
        spectrum_db: np.ndarray,
        equipment_frequencies: EquipmentFrequencies,
        noise_threshold_db: float,
        noise_poly: np.poly1d
    ) -> RuleEvaluationResult:
        """Оценивает правило спектра."""
        rule_id = rule.get('id', 'unknown')
        frequency_type = rule.get('frequencyType')
        multiplier = rule.get('multiplier', 1)
        custom_frequency = rule.get('customFrequency')
        is_present = rule.get('isPresent', True)
        has_comparison = rule.get('hasComparison', False)
        comparison_multiplier = rule.get('comparisonMultiplier')
        has_sidebands = rule.get('hasSidebands', False)
        sidebands = rule.get('sidebands')
        use_for_defect_strength = rule.get('useForDefectStrength', False)
        
        # Вычисляем основную частоту
        if frequency_type == 'custom':
            if custom_frequency is None:
                return RuleEvaluationResult(
                    rule_id=rule_id,
                    passed=False,
                    details={'error': 'customFrequency required for custom frequency type'}
                )
            main_frequency = custom_frequency
        else:
            base_freq = equipment_frequencies.get_frequency(frequency_type)
            main_frequency = base_freq * multiplier
        
        # Проверяем основную частоту
        main_freq_result = self._check_frequency(
            main_frequency, frequencies, spectrum_db, noise_threshold_db, noise_poly
        )
        
        # Обрабатываем isPresent:
        # - null: условие не проверяется (всегда выполнено)
        # - true: амплитуда должна превышать уровень шума на noise_threshold_db
        # - false: амплитуда должна быть ниже уровня шума
        if is_present is None:
            main_passed = True  # Условие не проверяется
        elif is_present is True:
            # Частота должна присутствовать (превышать уровень шума на noise_threshold_db)
            main_passed = main_freq_result['present']
        else:  # is_present is False
            # Частота должна отсутствовать (быть ниже уровня шума)
            if main_freq_result['amplitude_db'] is not None:
                noise_level_at_freq = self._get_noise_level_at_frequency(
                    main_frequency, frequencies, noise_poly
                )
                main_passed = main_freq_result['amplitude_db'] < noise_level_at_freq
            else:
                # Если частота не найдена, считаем что она отсутствует (правило выполнено)
                main_passed = True
        
        frequencies_found = []
        defect_strength_amplitude = None
        
        # Всегда добавляем частоту в результаты, если она найдена в спектре
        # (независимо от того, проходит ли она проверку present)
        if main_freq_result.get('amplitude_db') is not None:
            frequencies_found.append({
                'frequency': main_freq_result['frequency'],
                'amplitude_db': main_freq_result['amplitude_db'],
                'type': 'main',
                'expected_frequency': main_frequency
            })
            # Для определения силы дефекта используем только частоты, которые прошли проверку
            if use_for_defect_strength and main_freq_result['present']:
                defect_strength_amplitude = main_freq_result['amplitude_db']
        
        # Проверяем сравнение с другой частотой
        comparison_passed = True
        if has_comparison and comparison_multiplier is not None:
            if frequency_type == 'custom':
                comparison_frequency = custom_frequency * comparison_multiplier
            else:
                base_freq = equipment_frequencies.get_frequency(frequency_type)
                comparison_frequency = base_freq * comparison_multiplier
            
            comparison_result = self._check_frequency(
                comparison_frequency, frequencies, spectrum_db, noise_threshold_db, noise_poly
            )
            
            # Сравнение: основная частота должна быть больше частоты сравнения
            if (main_freq_result.get('amplitude_db') is not None and 
                comparison_result.get('amplitude_db') is not None):
                comparison_passed = (main_freq_result['amplitude_db'] > comparison_result['amplitude_db'])
            else:
                comparison_passed = False
            
            # Всегда добавляем частоту сравнения в результаты, если она найдена в спектре
            if comparison_result.get('amplitude_db') is not None:
                frequencies_found.append({
                    'frequency': comparison_result['frequency'],
                    'amplitude_db': comparison_result['amplitude_db'],
                    'type': 'comparison',
                    'expected_frequency': comparison_frequency
                })
        
        # Проверяем боковые полосы
        sidebands_passed = True
        if has_sidebands and sidebands:
            modulating_freq_type = sidebands.get('modulatingFrequencyType')
            sideband_items = sidebands.get('items', [])
            sideband_operator = sidebands.get('operator', 'AND')  # По умолчанию AND
            
            if modulating_freq_type:
                modulating_freq = equipment_frequencies.get_frequency(modulating_freq_type)
                
                # Разделяем боковые полосы на левые (offset < 0) и правые (offset > 0)
                left_sidebands = [item for item in sideband_items if item.get('offset', 0) < 0]
                right_sidebands = [item for item in sideband_items if item.get('offset', 0) > 0]
                
                # Словарь для отслеживания прохождения каждой боковой полосы
                sideband_passed_map = {}  # {offset: passed}
                
                # Вспомогательная функция для проверки группы боковых полос
                def check_sideband_group(group_items):
                    """Проверяет группу боковых полос (все должны пройти через AND)"""
                    nonlocal defect_strength_amplitude, frequencies_found, sideband_passed_map
                    group_passed = True
                    for sideband_item in group_items:
                        sideband_id = sideband_item.get('id', 'unknown')
                        offset = sideband_item.get('offset', 0)
                        sideband_is_present = sideband_item.get('isPresent', True)
                        sideband_has_comparison = sideband_item.get('hasComparison', False)
                        comparison_offset = sideband_item.get('comparisonOffset')
                        sideband_use_for_strength = sideband_item.get('useForDefectStrength', False)
                        
                        # Вычисляем частоту боковой полосы
                        sideband_frequency = main_frequency + (offset * modulating_freq)
                        
                        sideband_result = self._check_frequency(
                            sideband_frequency, frequencies, spectrum_db, noise_threshold_db, noise_poly
                        )
                        
                        # Обрабатываем isPresent:
                        # - null: условие не проверяется (всегда выполнено)
                        # - true: амплитуда должна превышать уровень шума на noise_threshold_db
                        # - false: амплитуда должна быть ниже уровня шума
                        if sideband_is_present is None:
                            sideband_passed_item = True  # Условие не проверяется
                        elif sideband_is_present is True:
                            # Боковая полоса должна присутствовать
                            sideband_passed_item = sideband_result['present']
                        else:  # sideband_is_present is False
                            # Боковая полоса должна отсутствовать (быть ниже уровня шума)
                            if sideband_result['amplitude_db'] is not None:
                                noise_level_at_freq = self._get_noise_level_at_frequency(
                                    sideband_frequency, frequencies, noise_poly
                                )
                                sideband_passed_item = sideband_result['amplitude_db'] < noise_level_at_freq
                            else:
                                # Если частота не найдена, считаем что она отсутствует (правило выполнено)
                                sideband_passed_item = True
                        group_passed = group_passed and sideband_passed_item
                        
                        # Сохраняем результат проверки для этой боковой полосы
                        sideband_passed_map[offset] = sideband_passed_item
                        
                        # Всегда добавляем боковую полосу в результаты, если она найдена в спектре
                        if sideband_result.get('amplitude_db') is not None:
                            frequencies_found.append({
                                'frequency': sideband_result['frequency'],
                                'amplitude_db': sideband_result['amplitude_db'],
                                'type': 'sideband',
                                'id': sideband_id,
                                'offset': offset,
                                'expected_frequency': sideband_frequency
                            })
                            # Для определения силы дефекта используем только боковые полосы, которые прошли проверку
                            if sideband_use_for_strength and sideband_result['present']:
                                if defect_strength_amplitude is None or sideband_result['amplitude_db'] > defect_strength_amplitude:
                                    defect_strength_amplitude = sideband_result['amplitude_db']
                        
                        # Проверяем сравнение боковых полос
                        if sideband_has_comparison and comparison_offset is not None:
                            comparison_sideband_freq = main_frequency + (comparison_offset * modulating_freq)
                            comparison_sideband_result = self._check_frequency(
                                comparison_sideband_freq, frequencies, spectrum_db, noise_threshold_db, noise_poly
                            )
                            
                            # Сравнение боковых полос: одна должна быть больше другой
                            if (sideband_result.get('amplitude_db') is not None and 
                                comparison_sideband_result.get('amplitude_db') is not None):
                                sideband_comparison_passed = (
                                    sideband_result['amplitude_db'] > comparison_sideband_result['amplitude_db']
                                )
                                # Обновляем результат проверки для этой боковой полосы с учетом сравнения
                                # Боковая полоса прошла, если она прошла свою проверку И прошла сравнение
                                sideband_passed_map[offset] = sideband_passed_map.get(offset, True) and sideband_comparison_passed
                                group_passed = group_passed and sideband_comparison_passed
                            
                            # Всегда добавляем боковую полосу сравнения в результаты, если она найдена в спектре
                            if comparison_sideband_result.get('amplitude_db') is not None:
                                frequencies_found.append({
                                    'frequency': comparison_sideband_result['frequency'],
                                    'amplitude_db': comparison_sideband_result['amplitude_db'],
                                    'type': 'sideband_comparison',
                                    'id': sideband_id,
                                    'offset': comparison_offset,
                                    'expected_frequency': comparison_sideband_freq
                                })
                    
                    return group_passed
                
                # Проверяем левые и правые боковые полосы
                left_passed = check_sideband_group(left_sidebands) if left_sidebands else True
                right_passed = check_sideband_group(right_sidebands) if right_sidebands else True
                
                # Применяем оператор между группами
                # Согласно документации:
                # - AND: основная частота И все левые И все правые
                # - OR: (основная частота И все левые) ИЛИ (основная частота И все правые)
                if sideband_operator == 'OR':
                    # OR: (основная частота И все левые) ИЛИ (основная частота И все правые)
                    sidebands_passed = (main_passed and left_passed) or (main_passed and right_passed)
                else:  # AND (по умолчанию)
                    # AND: основная частота И все левые И все правые
                    sidebands_passed = main_passed and left_passed and right_passed
        
        # Правило выполнено, если все проверки пройдены
        rule_passed = main_passed and comparison_passed and sidebands_passed
        
        # Сохраняем информацию о прохождении боковых полос в details
        details_dict = {
            'main_frequency': main_frequency,
            'main_passed': main_passed,
            'comparison_passed': comparison_passed,
            'sidebands_passed': sidebands_passed
        }
        if has_sidebands and sidebands and modulating_freq_type:
            # Сохраняем информацию о том, какие боковые полосы прошли проверку
            details_dict['sideband_passed_map'] = sideband_passed_map
            details_dict['sideband_operator'] = sidebands.get('operator', 'AND')
            # Сохраняем информацию о том, какая группа прошла (для OR)
            # left_passed и right_passed уже вычислены выше в том же блоке
            if sidebands.get('operator') == 'OR':
                details_dict['left_sidebands_passed'] = left_passed
                details_dict['right_sidebands_passed'] = right_passed
        
        return RuleEvaluationResult(
            rule_id=rule_id,
            passed=rule_passed,
            details=details_dict,
            frequencies_found=frequencies_found,
            defect_strength_amplitude=defect_strength_amplitude
        )
    
    def _calculate_noise_level(
        self, 
        frequencies: np.ndarray, 
        spectrum_db: np.ndarray
    ) -> np.poly1d:
        """
        Вычисляет уровень шума спектра через полиномиальную аппроксимацию 8-й степени.
        
        Аппроксимирует спектр полиномом 8-й степени, который используется для оценки
        уровня шума на любой частоте. Полином сглаживает пики гармоник и дает оценку
        фонового уровня шума.
        
        :param frequencies: Массив частот спектра (Гц)
        :param spectrum_db: Массив значений спектра в децибелах
        :return: Полином 8-й степени для вычисления уровня шума
        """
        if len(spectrum_db) == 0 or len(frequencies) == 0:
            # Возвращаем полином, который всегда возвращает -inf
            return np.poly1d([-np.inf])
        
        if len(spectrum_db) < 9:
            # Если точек меньше, чем нужно для полинома 8-й степени, используем среднее
            return np.poly1d([np.mean(spectrum_db)])
        
        # Нормализуем частоты для численной устойчивости
        # Используем нормализованные частоты от 0 до 1
        freq_min = frequencies.min()
        freq_max = frequencies.max()
        if freq_max == freq_min:
            # Если все частоты одинаковы, возвращаем среднее значение
            return np.poly1d([np.mean(spectrum_db)])
        
        freq_normalized = frequencies #(frequencies - freq_min) / (freq_max - freq_min)
        
        # Аппроксимируем спектр полиномом 8-й степени
        # Используем numpy.polyfit для аппроксимации
        try:
            poly_coeffs = np.polyfit(freq_normalized, spectrum_db, deg=8)
            noise_poly = np.poly1d(poly_coeffs)
        except (np.linalg.LinAlgError, ValueError):
            # Если не удалось вычислить полином, используем медиану
            median_value = np.median(spectrum_db)
            return np.poly1d([median_value])
        
        return noise_poly
    
    def _get_noise_level_at_frequency(
        self,
        frequency: float,
        frequencies: np.ndarray,
        noise_poly: np.poly1d
    ) -> float:
        """
        Вычисляет уровень шума на конкретной частоте используя полином.
        
        :param frequency: Частота, для которой вычисляется уровень шума (Гц)
        :param frequencies: Массив всех частот спектра (Гц) для нормализации
        :param noise_poly: Полином для вычисления уровня шума
        :return: Уровень шума на заданной частоте в дБ
        """
        if len(frequencies) == 0:
            return -np.inf
        
        freq_min = frequencies.min()
        freq_max = frequencies.max()
        
        if freq_max == freq_min:
            # Если все частоты одинаковы, возвращаем значение полинома в точке 0
            return float(noise_poly(0.0))
        
        # Нормализуем частоту
        freq_normalized = (frequency - freq_min) / (freq_max - freq_min)
        
        # Вычисляем значение полинома на нормализованной частоте
        noise_level = noise_poly(freq_normalized)
        
        return float(noise_level)
    
    def _check_frequency(
        self,
        target_frequency: float,
        frequencies: np.ndarray,
        spectrum_db: np.ndarray,
        noise_threshold_db: float,
        noise_poly: np.poly1d
    ) -> Dict[str, Any]:
        """
        Проверяет наличие частоты в спектре.
        
        Частота считается присутствующей, если её амплитуда превышает
        уровень шума на значение noise_threshold_db децибел.
        Уровень шума вычисляется для конкретной частоты через полином 8-й степени.
        
        :param target_frequency: Целевая частота (Гц)
        :param frequencies: Массив частот спектра (Гц)
        :param spectrum_db: Массив значений спектра в децибелах
        :param noise_threshold_db: Порог превышения над уровнем шума в дБ
        :param noise_poly: Полином 8-й степени для вычисления уровня шума
        :return: Словарь с результатами проверки
        """
        # Вычисляем уровень шума на целевой частоте через полином
        noise_level_db = self._get_noise_level_at_frequency(target_frequency, frequencies, noise_poly)
        
        # Находим ближайшую частоту в спектре
        freq_min = target_frequency - self.frequency_tolerance_hz
        freq_max = target_frequency + self.frequency_tolerance_hz
        
        mask = (frequencies >= freq_min) & (frequencies <= freq_max)
        
        if not np.any(mask):
            return {
                'present': False,
                'frequency': target_frequency,
                'amplitude_db': None,
                'noise_level_db': noise_level_db
            }
        
        # Находим максимальную амплитуду в диапазоне
        amplitudes_in_range = spectrum_db[mask]
        max_amplitude_idx = np.argmax(amplitudes_in_range)
        actual_freq_idx = np.where(mask)[0][max_amplitude_idx]
        actual_freq = frequencies[actual_freq_idx]
        amplitude = spectrum_db[actual_freq_idx]
        
        # Частота присутствует, если амплитуда превышает уровень шума на noise_threshold_db
        threshold = noise_level_db + noise_threshold_db
        present = amplitude >= threshold
        
        return {
            'present': present,
            'frequency': actual_freq,
            'amplitude_db': amplitude,
            'expected_frequency': target_frequency,
            'noise_level_db': noise_level_db,
            'threshold_db': threshold
        }
    
    def _collect_all_frequencies(
        self,
        result: Union[RuleEvaluationResult, GroupEvaluationResult]
    ) -> List[Dict[str, Any]]:
        """Собирает все найденные частоты из результатов."""
        frequencies = []
        
        if isinstance(result, RuleEvaluationResult):
            frequencies.extend(result.frequencies_found)
        elif isinstance(result, GroupEvaluationResult):
            for element_result in result.element_results:
                frequencies.extend(self._collect_all_frequencies(element_result))
        
        return frequencies
    
    def _collect_defect_strength_amplitudes(
        self,
        result: Union[RuleEvaluationResult, GroupEvaluationResult]
    ) -> List[float]:
        """Собирает все амплитуды из правил с useForDefectStrength=True."""
        amplitudes = []
        
        if isinstance(result, RuleEvaluationResult):
            if result.defect_strength_amplitude is not None:
                amplitudes.append(result.defect_strength_amplitude)
        elif isinstance(result, GroupEvaluationResult):
            for element_result in result.element_results:
                amplitudes.extend(self._collect_defect_strength_amplitudes(element_result))
        
        return amplitudes
    
    def _check_defect_detected_by_strength_rules(
        self,
        result: Union[RuleEvaluationResult, GroupEvaluationResult],
        rules: Dict[str, Any]
    ) -> bool:
        """
        Проверяет, обнаружен ли дефект на основе правил с useForDefectStrength=True.
        
        Дефект считается обнаруженным только если выполнено хотя бы одно правило
        с useForDefectStrength=True.
        
        :param result: Результат оценки правил
        :param rules: JSON-структура правил (для определения useForDefectStrength)
        :return: True если дефект обнаружен, False иначе
        """
        # Извлекаем все правила с их useForDefectStrength флагами
        all_rules = self._extract_all_rules(rules.get('rootGroup', {}))
        rule_use_strength_map = {rule.get('id'): rule.get('useForDefectStrength', False) 
                                 for rule in all_rules if rule.get('ruleType') == 'spectrum'}
        
        # Проверяем результаты правил с useForDefectStrength=True
        if isinstance(result, RuleEvaluationResult):
            use_for_strength = rule_use_strength_map.get(result.rule_id, False)
            return use_for_strength and result.passed
        elif isinstance(result, GroupEvaluationResult):
            operator = result.operator
            element_results = result.element_results
            
            if not element_results:
                return False
            
            # Для оператора AND: все правила с useForDefectStrength=True должны быть выполнены
            # Для оператора OR: хотя бы одно правило с useForDefectStrength=True должно быть выполнено
            strength_rule_results = []
            for element_result in element_results:
                if isinstance(element_result, RuleEvaluationResult):
                    use_for_strength = rule_use_strength_map.get(element_result.rule_id, False)
                    if use_for_strength:
                        strength_rule_results.append(element_result.passed)
                elif isinstance(element_result, GroupEvaluationResult):
                    # Рекурсивно проверяем вложенные группы
                    # Проверяем, есть ли в группе правила с useForDefectStrength=True
                    nested_has_strength_rules = self._has_strength_rules_in_group(element_result, rules)
                    if nested_has_strength_rules:
                        nested_detected = self._check_defect_detected_by_strength_rules(element_result, rules)
                        strength_rule_results.append(nested_detected)
            
            # Если нет правил с useForDefectStrength=True, дефект не обнаружен
            if not strength_rule_results:
                return False
            
            # Применяем оператор группы
            if operator == 'AND':
                return all(strength_rule_results)
            elif operator == 'OR':
                return any(strength_rule_results)
            else:
                return False
        
        return False
    
    def _has_strength_rules_in_group(
        self,
        result: Union[RuleEvaluationResult, GroupEvaluationResult],
        rules: Dict[str, Any]
    ) -> bool:
        """
        Проверяет, есть ли в группе правила с useForDefectStrength=True.
        
        :param result: Результат оценки правил
        :param rules: JSON-структура правил
        :return: True если есть правила с useForDefectStrength=True
        """
        all_rules = self._extract_all_rules(rules.get('rootGroup', {}))
        rule_use_strength_map = {rule.get('id'): rule.get('useForDefectStrength', False) 
                                 for rule in all_rules if rule.get('ruleType') == 'spectrum'}
        
        if isinstance(result, RuleEvaluationResult):
            return rule_use_strength_map.get(result.rule_id, False)
        elif isinstance(result, GroupEvaluationResult):
            for element_result in result.element_results:
                if isinstance(element_result, RuleEvaluationResult):
                    if rule_use_strength_map.get(element_result.rule_id, False):
                        return True
                elif isinstance(element_result, GroupEvaluationResult):
                    if self._has_strength_rules_in_group(element_result, rules):
                        return True
            return False
        
        return False
    
    def _has_applicable_criteria(
        self,
        rules: Dict[str, Any],
        spectrum_type: str,
        reference_spectrum_db: Optional[np.ndarray] = None,
        frequency_resolution: Optional[float] = None,
        filter_bandwidth: Optional[float] = None
    ) -> bool:
        """
        Проверяет, есть ли применимые критерии для определения силы дефекта.
        
        Для спектра: нужны боковые полосы или эталонный спектр
        Для огибающей: нужны параметры фильтра (frequency_resolution и filter_bandwidth)
        
        :param rules: JSON-структура правил
        :param spectrum_type: Тип спектра ('spectrum' или 'envelope')
        :param reference_spectrum_db: Эталонный спектр (для критерия "Эталон")
        :param frequency_resolution: Разрешение по частоте (для критерия "Модуляция")
        :param filter_bandwidth: Ширина полосы фильтра (для критерия "Модуляция")
        :return: True если есть применимые критерии, False иначе
        """
        if spectrum_type == 'spectrum':
            # Для спектра нужны либо боковые полосы, либо эталонный спектр
            all_rules = self._extract_all_rules(rules.get('rootGroup', {}))
            
            # Проверяем наличие боковых полос
            has_sidebands = any(
                rule.get('hasSidebands', False) and rule.get('useForDefectStrength', False)
                for rule in all_rules
                if rule.get('ruleType') == 'spectrum'
            )
            
            # Проверяем наличие эталонного спектра
            has_template = reference_spectrum_db is not None
            
            return has_sidebands or has_template
        
        elif spectrum_type == 'envelope':
            # Для огибающей нужны параметры фильтра
            return frequency_resolution is not None and filter_bandwidth is not None
        
        return False
    
    def _calculate_defect_strength_by_criteria(
        self,
        evaluation_result: DefectEvaluationResult,
        rules: Dict[str, Any],
        frequencies: np.ndarray,
        spectrum_db: np.ndarray,
        equipment_frequencies: EquipmentFrequencies,
        defect_metadata: Dict[str, Any],
        spectrum_type: str,
        reference_spectrum_db: Optional[np.ndarray] = None,
        frequency_resolution: Optional[float] = None,
        filter_bandwidth: Optional[float] = None,
        spectrum_weak: Optional[float] = None,
        spectrum_medium: Optional[float] = None,
        spectrum_strong: Optional[float] = None,
        spectrum_template_weak: Optional[float] = None,
        spectrum_template_medium: Optional[float] = None,
        spectrum_template_strong: Optional[float] = None,
        envelope_weak: Optional[float] = None,
        envelope_medium: Optional[float] = None,
        envelope_strong: Optional[float] = None
    ) -> Optional[str]:
        """
        Вычисляет силу дефекта по трем критериям:
        1. Основная/боковая (только для спектра, только для боковых полос)
        2. Эталон (только для спектра, для всех правил)
        3. Модуляция (только для спектра огибающей)
        
        :param evaluation_result: Результат оценки правил
        :param rules: JSON-структура правил
        :param frequencies: Массив частот спектра (Гц)
        :param spectrum_db: Массив значений спектра в дБ
        :param equipment_frequencies: Базовые частоты оборудования
        :param defect_metadata: Метаданные о дефекте с пороговыми значениями
        :param spectrum_type: Тип спектра ('spectrum' или 'envelope')
        :param reference_spectrum_db: Эталонный спектр в дБ
        :param frequency_resolution: Разрешение по частоте Δf_a (Гц)
        :param filter_bandwidth: Ширина полосы фильтра Δf_w (Гц)
        :return: Кортеж (максимальная сила дефекта, словарь с силами по каждому критерию)
        """
        strengths = []
        sideband_strength = None
        template_strength = None
        modulation_strength = None
        
        # Критерий 1: Основная/боковая (только для спектра, только для боковых полос)
        if spectrum_type == 'spectrum':
            sideband_strength = self._calculate_sideband_criterion(
                evaluation_result, rules, frequencies, spectrum_db, 
                equipment_frequencies, defect_metadata,
                spectrum_weak, spectrum_medium, spectrum_strong
            )
            if sideband_strength:
                strengths.append(sideband_strength)
            
            # Критерий 2: Эталон (только для спектра, для всех правил)
            if reference_spectrum_db is not None:
                template_strength = self._calculate_template_criterion(
                    evaluation_result, rules, frequencies, spectrum_db,
                    reference_spectrum_db, equipment_frequencies, defect_metadata,
                    spectrum_template_weak, spectrum_template_medium, spectrum_template_strong
                )
                if template_strength:
                    strengths.append(template_strength)
        
        # Критерий 3: Модуляция (только для спектра огибающей)
        elif spectrum_type == 'envelope':
            if frequency_resolution is not None and filter_bandwidth is not None:
                modulation_strength, modulation_value = self._calculate_modulation_criterion(
                    evaluation_result, rules, frequencies, spectrum_db,
                    equipment_frequencies, defect_metadata,
                    frequency_resolution, filter_bandwidth,
                    envelope_weak=envelope_weak,
                    envelope_medium=envelope_medium,
                    envelope_strong=envelope_strong
                )
                if modulation_strength:
                    strengths.append(modulation_strength)
                # Сохраняем значение модуляции в evaluation_result
                if modulation_value is not None:
                    evaluation_result.modulation_value = modulation_value
        
        # Возвращаем максимальную силу из всех критериев
        if not strengths:
            return None, {}
        
        # Преобразуем в числовые значения для сравнения
        strength_map = {'weak': 1, 'medium': 2, 'strong': 3}
        max_strength_value = max(strength_map.get(s, 0) for s in strengths)
        
        # Обратное преобразование
        max_strength = None
        for strength, value in strength_map.items():
            if value == max_strength_value:
                max_strength = strength
                break
        
        # Формируем словарь с силами по каждому критерию
        criterion_strengths = {}
        if spectrum_type == 'spectrum':
            if sideband_strength:
                criterion_strengths['sideband'] = sideband_strength
            if template_strength:
                criterion_strengths['template'] = template_strength
        elif spectrum_type == 'envelope':
            if modulation_strength:
                criterion_strengths['modulation'] = modulation_strength
        
        return max_strength, criterion_strengths
    
    def _calculate_sideband_criterion(
        self,
        evaluation_result: DefectEvaluationResult,
        rules: Dict[str, Any],
        frequencies: np.ndarray,
        spectrum_db: np.ndarray,
        equipment_frequencies: EquipmentFrequencies,
        defect_metadata: Dict[str, Any],
        spectrum_weak: Optional[float] = None,
        spectrum_medium: Optional[float] = None,
        spectrum_strong: Optional[float] = None
    ) -> Optional[str]:
        """
        Вычисляет силу дефекта по критерию "Основная/боковая".
        Разница амплитуды боковой частоты в сравнении с основной (дБ).
        """
        all_rules = self._extract_all_rules(rules.get('rootGroup', {}))
        found_frequencies_map = {f.get('expected_frequency'): f for f in evaluation_result.all_frequencies_found}
        
        max_diff = None
        
        for rule in all_rules:
            if rule.get('ruleType') != 'spectrum' or not rule.get('hasSidebands'):
                continue
            
            # Учитываем только правила с useForDefectStrength=True
            if not rule.get('useForDefectStrength', False):
                continue
            
            # Проверяем, выполнено ли правило
            rule_id = rule.get('id')
            rule_result = self._find_rule_result(evaluation_result.root_group_result, rule_id)
            if rule_result is None or not rule_result.passed:
                # Пропускаем правила, которые не выполнены
                continue
            
            frequency_type = rule.get('frequencyType')
            multiplier = rule.get('multiplier', 1)
            custom_frequency = rule.get('customFrequency')
            sidebands = rule.get('sidebands')
            
            # Вычисляем основную частоту
            if frequency_type == 'custom':
                if custom_frequency is None:
                    continue
                main_frequency = custom_frequency
            else:
                try:
                    base_freq = equipment_frequencies.get_frequency(frequency_type)
                    main_frequency = base_freq * multiplier
                except ValueError:
                    continue
            
            # Получаем амплитуду основной частоты
            main_freq_info = found_frequencies_map.get(main_frequency)
            if main_freq_info is None or main_freq_info.get('amplitude_db') is None:
                continue
            
            main_amplitude = main_freq_info.get('amplitude_db')
            
            # Проверяем боковые полосы
            if sidebands:
                modulating_freq_type = sidebands.get('modulatingFrequencyType')
                sideband_items = sidebands.get('items', [])
                
                if modulating_freq_type:
                    try:
                        modulating_freq = equipment_frequencies.get_frequency(modulating_freq_type)
                        
                        for sideband_item in sideband_items:
                            if not sideband_item.get('useForDefectStrength', False):
                                continue
                            
                            offset = sideband_item.get('offset', 0)
                            sideband_frequency = main_frequency + (offset * modulating_freq)
                            
                            # Ищем боковую полосу в найденных частотах
                            sideband_freq_info = None
                            for expected_freq, info in found_frequencies_map.items():
                                if abs(expected_freq - sideband_frequency) < self.frequency_tolerance_hz * 2:
                                    sideband_freq_info = info
                                    break
                            
                            if sideband_freq_info and sideband_freq_info.get('amplitude_db') is not None:
                                sideband_amplitude = sideband_freq_info.get('amplitude_db')
                                # Разница: основная минус боковая (в дБ)
                                diff = main_amplitude - sideband_amplitude
                                # Для sideband критерия: чем меньше разница, тем сильнее дефект
                                # Поэтому ищем минимальную разницу (max_diff будет минимальным значением)
                                if max_diff is None or diff < max_diff:
                                    max_diff = diff
                    except ValueError:
                        continue
        
        if max_diff is None:
            return None
        
        # Определяем силу по порогам
        # ВАЖНО: Для критерия "Основная/боковая" логика обратная:
        # чем МЕНЬШЕ разница, тем СИЛЬНЕЕ дефект
        weak_threshold = spectrum_weak if spectrum_weak is not None else defect_metadata.get('default_spectrum_weak', 0)
        medium_threshold = spectrum_medium if spectrum_medium is not None else defect_metadata.get('default_spectrum_medium', 0)
        strong_threshold = spectrum_strong if spectrum_strong is not None else defect_metadata.get('default_spectrum_strong', 0)
        
        # Обратная логика: меньше разница = сильнее дефект
        if max_diff <= strong_threshold:
            return 'strong'
        elif max_diff <= medium_threshold:
            return 'medium'
        elif max_diff <= weak_threshold:
            return 'weak'
        
        return None
    
    def _calculate_template_criterion(
        self,
        evaluation_result: DefectEvaluationResult,
        rules: Dict[str, Any],
        frequencies: np.ndarray,
        spectrum_db: np.ndarray,
        reference_spectrum_db: np.ndarray,
        equipment_frequencies: EquipmentFrequencies,
        defect_metadata: Dict[str, Any],
        spectrum_template_weak: Optional[float] = None,
        spectrum_template_medium: Optional[float] = None,
        spectrum_template_strong: Optional[float] = None
    ) -> Optional[str]:
        """
        Вычисляет силу дефекта по критерию "эталон".
        Разница амплитуды в сравнении с эталоном (дБ).
        """
        all_rules = self._extract_all_rules(rules.get('rootGroup', {}))
        found_frequencies_map = {f.get('expected_frequency'): f for f in evaluation_result.all_frequencies_found}
        
        max_diff = None
        
        for rule in all_rules:
            if rule.get('ruleType') != 'spectrum' or not rule.get('useForDefectStrength', False):
                continue
            
            # Проверяем, выполнено ли правило
            rule_id = rule.get('id')
            rule_result = self._find_rule_result(evaluation_result.root_group_result, rule_id)
            if rule_result is None or not rule_result.passed:
                # Пропускаем правила, которые не выполнены
                continue
            
            frequency_type = rule.get('frequencyType')
            multiplier = rule.get('multiplier', 1)
            custom_frequency = rule.get('customFrequency')
            
            # Вычисляем частоту
            if frequency_type == 'custom':
                if custom_frequency is None:
                    continue
                target_frequency = custom_frequency
            else:
                try:
                    base_freq = equipment_frequencies.get_frequency(frequency_type)
                    target_frequency = base_freq * multiplier
                except ValueError:
                    continue
            
            # Получаем амплитуду текущего спектра
            freq_info = found_frequencies_map.get(target_frequency)
            if freq_info is None or freq_info.get('amplitude_db') is None:
                continue
            
            current_amplitude = freq_info.get('amplitude_db')
            
            # Находим амплитуду в эталонном спектре
            freq_min = target_frequency - self.frequency_tolerance_hz
            freq_max = target_frequency + self.frequency_tolerance_hz
            mask = (frequencies >= freq_min) & (frequencies <= freq_max)
            
            if not np.any(mask):
                continue
            
            # Берем максимальную амплитуду в диапазоне из эталона
            reference_amplitudes = reference_spectrum_db[mask]
            reference_amplitude = np.max(reference_amplitudes)
            
            # Разница: текущий минус эталон (в дБ)
            diff = current_amplitude - reference_amplitude
            if max_diff is None or diff > max_diff:
                max_diff = diff
        
        if max_diff is None:
            return None
        
        # Определяем силу по порогам
        weak_threshold = spectrum_template_weak if spectrum_template_weak is not None else defect_metadata.get('default_spectrum_template_weak', 0)
        medium_threshold = spectrum_template_medium if spectrum_template_medium is not None else defect_metadata.get('default_spectrum_template_medium', 0)
        strong_threshold = spectrum_template_strong if spectrum_template_strong is not None else defect_metadata.get('default_spectrum_template_strong', 0)
        
        if max_diff >= strong_threshold:
            return 'strong'
        elif max_diff >= medium_threshold:
            return 'medium'
        elif max_diff >= weak_threshold:
            return 'weak'
        
        return None
    
    def _calculate_modulation_criterion(
        self,
        evaluation_result: DefectEvaluationResult,
        rules: Dict[str, Any],
        frequencies: np.ndarray,
        spectrum_db: np.ndarray,
        equipment_frequencies: EquipmentFrequencies,
        defect_metadata: Dict[str, Any],
        frequency_resolution: float,
        filter_bandwidth: float,
        envelope_weak: Optional[float] = None,
        envelope_medium: Optional[float] = None,
        envelope_strong: Optional[float] = None
    ) -> Optional[str]:
        """
        Вычисляет силу дефекта по критерию "модуляция".
        Формула: m = sqrt((10^(ΔL/10) - 1) * (Δf_a / Δf_w)) * 100%
        где ΔL - разница в дБ, Δf_a - разрешение по частоте, Δf_w - ширина полосы фильтра.
        """
        all_rules = self._extract_all_rules(rules.get('rootGroup', {}))
        found_frequencies_map = {f.get('expected_frequency'): f for f in evaluation_result.all_frequencies_found}
        
        # Вычисляем полином для уровня шума один раз
        noise_poly = self._calculate_noise_level(frequencies, spectrum_db)
        
        max_modulation = None
        
        for rule in all_rules:
            if rule.get('ruleType') != 'spectrum' or not rule.get('useForDefectStrength', False):
                continue
            
            # Проверяем, выполнено ли правило
            rule_id = rule.get('id')
            rule_result = self._find_rule_result(evaluation_result.root_group_result, rule_id)
            if rule_result is None or not rule_result.passed:
                # Пропускаем правила, которые не выполнены
                continue
            
            frequency_type = rule.get('frequencyType')
            multiplier = rule.get('multiplier', 1)
            custom_frequency = rule.get('customFrequency')
            has_sidebands = rule.get('hasSidebands', False)
            sidebands = rule.get('sidebands')
            
            # Вычисляем основную частоту
            if frequency_type == 'custom':
                if custom_frequency is None:
                    continue
                main_frequency = custom_frequency
            else:
                try:
                    base_freq = equipment_frequencies.get_frequency(frequency_type)
                    main_frequency = base_freq * multiplier
                except ValueError:
                    continue
            
            # Вычисляем модуляцию для основной гармоники
            main_freq_info = found_frequencies_map.get(main_frequency)
            if main_freq_info and main_freq_info.get('amplitude_db') is not None:
                main_amplitude = main_freq_info.get('amplitude_db')
                noise_level = self._get_noise_level_at_frequency(main_frequency, frequencies, noise_poly)
                delta_l = main_amplitude - noise_level
                
                # Если delta_l отрицательная, устанавливаем в 0
                if delta_l < 0:
                    delta_l = 0.0
                
                # Вычисляем модуляцию по формуле
                # m = sqrt((10^(ΔL/10) - 1) * (Δf_a / Δf_w)) * 100%
                try:
                    # Проверяем, что выражение под корнем не отрицательное
                    expression_under_sqrt = (10 ** (delta_l / 10) - 1) * (frequency_resolution / filter_bandwidth)
                    print(f"expression_under_sqrt: delta_l = {delta_l}, frequency_resolution = {frequency_resolution}, filter_bandwidth = {filter_bandwidth}, expression_under_sqrt = {expression_under_sqrt}")
                    if expression_under_sqrt < 0: 
                        modulation = 0.0
                    else:
                        modulation = np.sqrt(expression_under_sqrt) * 100
                    
                    if max_modulation is None or modulation > max_modulation:
                        max_modulation = modulation
                except (ValueError, OverflowError):
                    # Если вычисление невозможно, модуляция = 0
                    pass
            
            # Вычисляем модуляцию для боковых полос (если есть)
            if has_sidebands and sidebands:
                modulating_freq_type = sidebands.get('modulatingFrequencyType')
                sideband_items = sidebands.get('items', [])
                
                if modulating_freq_type:
                    try:
                        modulating_freq = equipment_frequencies.get_frequency(modulating_freq_type)
                        
                        for sideband_item in sideband_items:
                            if not sideband_item.get('useForDefectStrength', False):
                                continue
                            
                            offset = sideband_item.get('offset', 0)
                            sideband_frequency = main_frequency + (offset * modulating_freq)
                            
                            # Ищем боковую полосу
                            sideband_freq_info = None
                            for expected_freq, info in found_frequencies_map.items():
                                if abs(expected_freq - sideband_frequency) < self.frequency_tolerance_hz * 2:
                                    sideband_freq_info = info
                                    break
                            
                            if sideband_freq_info and sideband_freq_info.get('amplitude_db') is not None:
                                sideband_amplitude = sideband_freq_info.get('amplitude_db')
                                noise_level_sideband = self._get_noise_level_at_frequency(sideband_frequency, frequencies, noise_poly)
                                
                                # ΔL - высота пика над уровнем шума (для боковой полосы)
                                delta_l = sideband_amplitude - noise_level_sideband
                                
                                # Если delta_l отрицательная, устанавливаем в 0
                                if delta_l < 0:
                                    delta_l = 0.0
                                
                                # Вычисляем модуляцию по формуле
                                # m = sqrt((10^(ΔL/10) - 1) * (Δf_a / Δf_w)) * 100%
                                try:
                                    # Проверяем, что выражение под корнем не отрицательное
                                    expression_under_sqrt = (10 ** (delta_l / 10) - 1) * (frequency_resolution / filter_bandwidth)
                                    if expression_under_sqrt < 0:
                                        modulation = 0.0
                                    else:
                                        modulation = np.sqrt(expression_under_sqrt) * 100
                                    
                                    if max_modulation is None or modulation > max_modulation:
                                        max_modulation = modulation
                                except (ValueError, OverflowError):
                                    # Если вычисление невозможно, модуляция = 0
                                    pass
                    except ValueError:
                        pass
        
        if max_modulation is None:
            return None, None
        
        # Определяем силу по порогам (в процентах)
        weak_threshold = envelope_weak if envelope_weak is not None else defect_metadata.get('default_envelope_weak', 0)
        medium_threshold = envelope_medium if envelope_medium is not None else defect_metadata.get('default_envelope_medium', 0)
        strong_threshold = envelope_strong if envelope_strong is not None else defect_metadata.get('default_envelope_strong', 0)
        
        strength = None
        if max_modulation >= strong_threshold:
            strength = 'strong'
        elif max_modulation >= medium_threshold:
            strength = 'medium'
        elif max_modulation >= weak_threshold:
            strength = 'weak'
        
        return strength, max_modulation
    
    def create_detection_report(
        self,
        evaluation_result: DefectEvaluationResult,
        rules: Dict[str, Any],
        frequencies: np.ndarray,
        spectrum_db: np.ndarray,
        equipment_frequencies: EquipmentFrequencies,
        defect_metadata: Dict[str, Any],
        spectrum_type: str = 'spectrum',  # 'spectrum' или 'envelope'
        reference_spectrum_db: Optional[np.ndarray] = None,
        frequency_resolution: Optional[float] = None,
        filter_bandwidth: Optional[float] = None,
        spectrum_weak: Optional[float] = None,
        spectrum_medium: Optional[float] = None,
        spectrum_strong: Optional[float] = None,
        spectrum_template_weak: Optional[float] = None,
        spectrum_template_medium: Optional[float] = None,
        spectrum_template_strong: Optional[float] = None,
        envelope_weak: Optional[float] = None,
        envelope_medium: Optional[float] = None,
        envelope_strong: Optional[float] = None
    ) -> DefectDetectionReport:
        """
        Создает отчет о дефекте с полной информацией.
        
        :param evaluation_result: Результат оценки правил
        :param rules: JSON-структура правил
        :param frequencies: Массив частот спектра (Гц)
        :param spectrum_db: Массив значений спектра в децибелах
        :param equipment_frequencies: Базовые частоты оборудования
        :param defect_metadata: Метаданные о дефекте (название, пороги, рекомендации)
        :param spectrum_type: Тип спектра ('spectrum' или 'envelope')
        :param reference_spectrum_db: Эталонный спектр в дБ (для критерия "эталон")
        :param frequency_resolution: Разрешение по частоте Δf_a (Гц) для критерия "модуляция"
        :param filter_bandwidth: Ширина полосы фильтра Δf_w (Гц) для критерия "модуляция"
        :param spectrum_weak: Порог для слабого дефекта критерия "Основная/боковая" (дБ)
        :param spectrum_medium: Порог для среднего дефекта критерия "Основная/боковая" (дБ)
        :param spectrum_strong: Порог для сильного дефекта критерия "Основная/боковая" (дБ)
        :param spectrum_template_weak: Порог для слабого дефекта критерия "Эталон" (дБ)
        :param spectrum_template_medium: Порог для среднего дефекта критерия "Эталон" (дБ)
        :param spectrum_template_strong: Порог для сильного дефекта критерия "Эталон" (дБ)
        :param envelope_weak: Порог для слабого дефекта критерия "Модуляция" (%)
        :param envelope_medium: Порог для среднего дефекта критерия "Модуляция" (%)
        :param envelope_strong: Порог для сильного дефекта критерия "Модуляция" (%)
        :return: Отчет о дефекте
        """
        # Вычисляем полином для уровня шума (для вычисления delta_l и модуляции)
        noise_poly = self._calculate_noise_level(frequencies, spectrum_db)
        defect_name = defect_metadata.get('name', 'Неизвестный дефект')
        
        # Вычисляем модуляцию для каждой гармоники (только для огибающей)
        compute_modulation = (spectrum_type == 'envelope' and 
                             frequency_resolution is not None and 
                             filter_bandwidth is not None)
        
        # Вычисляем силу дефекта по трем критериям
        defect_strength, criterion_strengths = self._calculate_defect_strength_by_criteria(
            evaluation_result=evaluation_result,
            rules=rules,
            frequencies=frequencies,
            spectrum_db=spectrum_db,
            equipment_frequencies=equipment_frequencies,
            defect_metadata=defect_metadata,
            spectrum_type=spectrum_type,
            reference_spectrum_db=reference_spectrum_db,
            frequency_resolution=frequency_resolution,
            filter_bandwidth=filter_bandwidth,
            spectrum_weak=spectrum_weak,
            spectrum_medium=spectrum_medium,
            spectrum_strong=spectrum_strong,
            spectrum_template_weak=spectrum_template_weak,
            spectrum_template_medium=spectrum_template_medium,
            spectrum_template_strong=spectrum_template_strong,
            envelope_weak=envelope_weak,
            envelope_medium=envelope_medium,
            envelope_strong=envelope_strong
        )
        
        # Обновляем силу дефекта в результате
        evaluation_result.defect_strength = defect_strength
        
        # Дефект считается обнаруженным только если определена степень развития (weak, medium, strong)
        # Если defect_strength = null, то дефект не обнаружен
        if defect_strength is None:
            evaluation_result.detected = False
        else:
            # Если степень развития определена, дефект обнаружен
            evaluation_result.detected = True
        
        # Формируем пороговые значения только для применимых критериев
        sideband_thresholds = None
        template_thresholds = None
        modulation_thresholds = None
        
        if spectrum_type == 'spectrum':
            # Пороги критерия "Основная/боковая" (для спектра)
            sideband_thresholds = {
                'weak': spectrum_weak if spectrum_weak is not None else defect_metadata.get('default_spectrum_weak'),
                'medium': spectrum_medium if spectrum_medium is not None else defect_metadata.get('default_spectrum_medium'),
                'strong': spectrum_strong if spectrum_strong is not None else defect_metadata.get('default_spectrum_strong')
            }
            # Пороги критерия "Эталон" (только если есть эталонный спектр)
            if reference_spectrum_db is not None:
                template_thresholds = {
                    'weak': spectrum_template_weak if spectrum_template_weak is not None else defect_metadata.get('default_spectrum_template_weak'),
                    'medium': spectrum_template_medium if spectrum_template_medium is not None else defect_metadata.get('default_spectrum_template_medium'),
                    'strong': spectrum_template_strong if spectrum_template_strong is not None else defect_metadata.get('default_spectrum_template_strong')
                }
        else:  # envelope
            # Пороги критерия "Модуляция" (для огибающей)
            if frequency_resolution is not None and filter_bandwidth is not None:
                modulation_thresholds = {
                    'weak': envelope_weak if envelope_weak is not None else defect_metadata.get('default_envelope_weak'),
                    'medium': envelope_medium if envelope_medium is not None else defect_metadata.get('default_envelope_medium'),
                    'strong': envelope_strong if envelope_strong is not None else defect_metadata.get('default_envelope_strong')
                }
        
        # Определяем рекомендацию на основе силы дефекта
        recommendation = None
        if defect_strength == 'strong':
            recommendation = defect_metadata.get('recommendations_strong')
        elif defect_strength == 'medium':
            recommendation = defect_metadata.get('recommendations_average') or defect_metadata.get('recommendations_medium')
        elif defect_strength == 'weak':
            recommendation = defect_metadata.get('recommendations_weak')
        
        # Извлекаем все правила из структуры
        all_rules = self._extract_all_rules(rules.get('rootGroup', {}))
        
        # Формируем плоский список гармоник
        harmonics = []
        # Создаем словарь для быстрого поиска найденных частот по expected_frequency
        found_frequencies_map = {}
        for f in evaluation_result.all_frequencies_found:
            expected_freq = f.get('expected_frequency')
            if expected_freq is not None:
                found_frequencies_map[expected_freq] = f
        
        for rule in all_rules:
            if rule.get('ruleType') != 'spectrum':
                continue
            
            rule_id = rule.get('id', 'unknown')
            frequency_type = rule.get('frequencyType')
            multiplier = rule.get('multiplier', 1)
            custom_frequency = rule.get('customFrequency')
            is_present = rule.get('isPresent', True)
            use_for_defect_strength = rule.get('useForDefectStrength', False)
            has_comparison = rule.get('hasComparison', False)
            comparison_multiplier = rule.get('comparisonMultiplier')
            has_sidebands = rule.get('hasSidebands', False)
            sidebands = rule.get('sidebands')
            
            # Вычисляем основную частоту
            base_freq = None
            if frequency_type == 'custom':
                if custom_frequency is None:
                    continue
                main_frequency = custom_frequency
            else:
                try:
                    base_freq = equipment_frequencies.get_frequency(frequency_type)
                    main_frequency = base_freq * multiplier
                except ValueError:
                    continue
            
            # Получаем информацию о правиле из результатов
            rule_result = self._find_rule_result(evaluation_result.root_group_result, rule_id)
            rule_passed = rule_result.passed if rule_result else False
            
            # Основная частота - ищем в найденных частотах
            main_freq_info = found_frequencies_map.get(main_frequency)
            if main_freq_info is None:
                # Ищем близкую частоту по expected_frequency
                for expected_freq, info in found_frequencies_map.items():
                    if abs(expected_freq - main_frequency) < self.frequency_tolerance_hz * 2:
                        main_freq_info = info
                        break
                # Если не нашли по expected_frequency, ищем по actual frequency
                if main_freq_info is None:
                    for info in evaluation_result.all_frequencies_found:
                        actual_freq = info.get('frequency')
                        if actual_freq is not None and abs(actual_freq - main_frequency) < self.frequency_tolerance_hz * 2:
                            main_freq_info = info
                            break
            
            # Вычисляем delta_l (высота пика над уровнем шума)
            # Вычисляем уровень шума на ожидаемой частоте
            noise_level = self._get_noise_level_at_frequency(main_frequency, frequencies, noise_poly)
            delta_l = None
            if main_freq_info and main_freq_info.get('amplitude_db') is not None:
                # Если частота найдена, вычисляем delta_l как разницу амплитуды и уровня шума
                amplitude = main_freq_info.get('amplitude_db')
                delta_l = amplitude - noise_level
            else:
                # Если частота не найдена, delta_l будет отрицательным или None
                # Можно показать, что пик отсутствует (ниже уровня шума)
                # Для этого нужно найти амплитуду на ожидаемой частоте в спектре
                freq_min = main_frequency - self.frequency_tolerance_hz
                freq_max = main_frequency + self.frequency_tolerance_hz
                mask = (frequencies >= freq_min) & (frequencies <= freq_max)
                if np.any(mask):
                    # Находим максимальную амплитуду в диапазоне
                    amplitudes_in_range = spectrum_db[mask]
                    max_amplitude = np.max(amplitudes_in_range)
                    delta_l = max_amplitude - noise_level
                # Если частота вообще не найдена в спектре, delta_l остается None
            
            # Если delta_l отрицательная, устанавливаем в 0
            if delta_l is not None and delta_l < 0:
                delta_l = 0.0
            
            # Вычисляем модуляцию для основной гармоники (только для огибающей)
            modulation = None
            if compute_modulation and delta_l is not None and delta_l >= 0:
                try:
                    # m = sqrt(10^(ΔL/10) - 1) * (Δf_a / Δf_w) * 100%
                    # Если delta_l = 0, то модуляция = 0
                    if delta_l == 0:
                        modulation = 0.0
                    else:
                        # Проверяем, что выражение под корнем не отрицательное
                        # m = sqrt((10^(ΔL/10) - 1) * (Δf_a / Δf_w)) * 100%
                        expression_under_sqrt = (10 ** (delta_l / 10) - 1) * (frequency_resolution / filter_bandwidth)
                        if expression_under_sqrt < 0:
                            modulation = 0.0
                        else:
                            modulation = np.sqrt(expression_under_sqrt) * 100
                except (ValueError, OverflowError):
                    modulation = 0.0
            
            # Вычисляем критерий "Эталон" для основной гармоники (только для спектра с эталоном)
            template_criterion_value = None
            if spectrum_type == 'spectrum' and reference_spectrum_db is not None:
                current_amplitude = main_freq_info.get('amplitude_db') if main_freq_info else None
                if current_amplitude is None:
                    # Ищем амплитуду в спектре
                    freq_min = main_frequency - self.frequency_tolerance_hz
                    freq_max = main_frequency + self.frequency_tolerance_hz
                    mask = (frequencies >= freq_min) & (frequencies <= freq_max)
                    if np.any(mask):
                        amplitudes_in_range = spectrum_db[mask]
                        current_amplitude = np.max(amplitudes_in_range)
                
                if current_amplitude is not None:
                    # Находим амплитуду в эталонном спектре
                    freq_min = main_frequency - self.frequency_tolerance_hz
                    freq_max = main_frequency + self.frequency_tolerance_hz
                    mask = (frequencies >= freq_min) & (frequencies <= freq_max)
                    if np.any(mask):
                        reference_amplitudes = reference_spectrum_db[mask]
                        reference_amplitude = np.max(reference_amplitudes)
                        # Разница: текущий минус эталон (в дБ)
                        template_criterion_value = current_amplitude - reference_amplitude
            
            # Определяем, прошла ли основная частота свою проверку
            main_passed_item = rule_passed  # По умолчанию используем общий результат
            if rule_result and rule_result.details:
                # Используем результат проверки основной частоты из details
                main_passed_item = rule_result.details.get('main_passed', rule_passed)
            
            harmonics.append(HarmonicInfo(
                frequency_type=frequency_type,
                multiplier=multiplier,
                expected_frequency=main_frequency,
                actual_frequency=main_freq_info.get('frequency') if main_freq_info else None,
                amplitude_db=main_freq_info.get('amplitude_db') if main_freq_info else None,
                delta_l=delta_l,
                modulation=modulation,
                template_criterion_value=template_criterion_value,
                sideband_criterion_value=None,  # Для основной гармоники не применимо
                is_present=is_present,
                passed=main_passed_item,
                use_for_defect_strength=use_for_defect_strength,
                harmonic_type='main'
            ))
            
            # Частота сравнения
            if has_comparison and comparison_multiplier is not None:
                if frequency_type == 'custom':
                    comparison_frequency = custom_frequency * comparison_multiplier
                else:
                    comparison_frequency = base_freq * comparison_multiplier
                
                comparison_freq_info = found_frequencies_map.get(comparison_frequency)
                if comparison_freq_info is None:
                    # Ищем близкую частоту по expected_frequency
                    for expected_freq, info in found_frequencies_map.items():
                        if abs(expected_freq - comparison_frequency) < self.frequency_tolerance_hz * 2:
                            comparison_freq_info = info
                            break
                    # Если не нашли, ищем по actual frequency
                    if comparison_freq_info is None:
                        for info in evaluation_result.all_frequencies_found:
                            actual_freq = info.get('frequency')
                            if actual_freq is not None and abs(actual_freq - comparison_frequency) < self.frequency_tolerance_hz * 2:
                                comparison_freq_info = info
                                break
                
                # Вычисляем delta_l для частоты сравнения
                noise_level = self._get_noise_level_at_frequency(comparison_frequency, frequencies, noise_poly)
                delta_l = None
                if comparison_freq_info and comparison_freq_info.get('amplitude_db') is not None:
                    amplitude = comparison_freq_info.get('amplitude_db')
                    delta_l = amplitude - noise_level
                else:
                    # Если частота не найдена, ищем амплитуду в спектре
                    freq_min = comparison_frequency - self.frequency_tolerance_hz
                    freq_max = comparison_frequency + self.frequency_tolerance_hz
                    mask = (frequencies >= freq_min) & (frequencies <= freq_max)
                    if np.any(mask):
                        amplitudes_in_range = spectrum_db[mask]
                        max_amplitude = np.max(amplitudes_in_range)
                        delta_l = max_amplitude - noise_level
                
                # Если delta_l отрицательная, устанавливаем в 0
                if delta_l is not None and delta_l < 0:
                    delta_l = 0.0
                
                # Вычисляем модуляцию для частоты сравнения (только для огибающей)
                modulation = None
                if compute_modulation and delta_l is not None and delta_l >= 0:
                    try:
                        # Если delta_l = 0, то модуляция = 0
                        if delta_l == 0:
                            modulation = 0.0
                        else:
                            # Проверяем, что выражение под корнем не отрицательное
                            # m = sqrt((10^(ΔL/10) - 1) * (Δf_a / Δf_w)) * 100%
                            expression_under_sqrt = (10 ** (delta_l / 10) - 1) * (frequency_resolution / filter_bandwidth)
                            if expression_under_sqrt < 0:
                                modulation = 0.0
                            else:
                                modulation = np.sqrt(expression_under_sqrt) * 100
                    except (ValueError, OverflowError):
                        modulation = 0.0
                
                # Вычисляем критерий "Эталон" для частоты сравнения (только для спектра с эталоном)
                template_criterion_value = None
                if spectrum_type == 'spectrum' and reference_spectrum_db is not None:
                    current_amplitude = comparison_freq_info.get('amplitude_db') if comparison_freq_info else None
                    if current_amplitude is None:
                        # Ищем амплитуду в спектре
                        freq_min = comparison_frequency - self.frequency_tolerance_hz
                        freq_max = comparison_frequency + self.frequency_tolerance_hz
                        mask = (frequencies >= freq_min) & (frequencies <= freq_max)
                        if np.any(mask):
                            amplitudes_in_range = spectrum_db[mask]
                            current_amplitude = np.max(amplitudes_in_range)
                    
                    if current_amplitude is not None:
                        # Находим амплитуду в эталонном спектре
                        freq_min = comparison_frequency - self.frequency_tolerance_hz
                        freq_max = comparison_frequency + self.frequency_tolerance_hz
                        mask = (frequencies >= freq_min) & (frequencies <= freq_max)
                        if np.any(mask):
                            reference_amplitudes = reference_spectrum_db[mask]
                            reference_amplitude = np.max(reference_amplitudes)
                            # Разница: текущий минус эталон (в дБ)
                            template_criterion_value = current_amplitude - reference_amplitude
                
                # Определяем, прошла ли частота сравнения свою проверку
                comparison_passed_item = rule_passed  # По умолчанию используем общий результат
                if rule_result and rule_result.details:
                    # Используем результат проверки частоты сравнения из details
                    comparison_passed_item = rule_result.details.get('comparison_passed', rule_passed)
                
                harmonics.append(HarmonicInfo(
                    frequency_type=frequency_type,
                    multiplier=comparison_multiplier,
                    expected_frequency=comparison_frequency,
                    actual_frequency=comparison_freq_info.get('frequency') if comparison_freq_info else None,
                    amplitude_db=comparison_freq_info.get('amplitude_db') if comparison_freq_info else None,
                    delta_l=delta_l,
                    modulation=modulation,
                    template_criterion_value=template_criterion_value,
                    sideband_criterion_value=None,  # Для частоты сравнения не применимо
                    is_present=None,  # Для сравнения не проверяется присутствие
                    passed=comparison_passed_item,
                    use_for_defect_strength=False,
                    harmonic_type='comparison'
                ))
            
            # Боковые полосы
            if has_sidebands and sidebands:
                modulating_freq_type = sidebands.get('modulatingFrequencyType')
                sideband_items = sidebands.get('items', [])
                
                if modulating_freq_type:
                    try:
                        modulating_freq = equipment_frequencies.get_frequency(modulating_freq_type)
                        
                        for sideband_item in sideband_items:
                            offset = sideband_item.get('offset', 0)
                            sideband_is_present = sideband_item.get('isPresent', True)
                            sideband_use_for_strength = sideband_item.get('useForDefectStrength', False)
                            sideband_id = sideband_item.get('id', 'unknown')
                            
                            sideband_frequency = main_frequency + (offset * modulating_freq)
                            
                            sideband_freq_info = found_frequencies_map.get(sideband_frequency)
                            if sideband_freq_info is None:
                                # Ищем близкую частоту по expected_frequency
                                for expected_freq, info in found_frequencies_map.items():
                                    if abs(expected_freq - sideband_frequency) < self.frequency_tolerance_hz * 2:
                                        sideband_freq_info = info
                                        break
                                # Если не нашли, ищем по actual frequency
                                if sideband_freq_info is None:
                                    for info in evaluation_result.all_frequencies_found:
                                        actual_freq = info.get('frequency')
                                        if actual_freq is not None and abs(actual_freq - sideband_frequency) < self.frequency_tolerance_hz * 2:
                                            sideband_freq_info = info
                                            break
                            
                            # Определяем тип боковой полосы
                            harmonic_type = 'sideband'
                            if sideband_item.get('hasComparison', False):
                                harmonic_type = 'sideband_comparison'
                            
                            # Вычисляем delta_l для боковой полосы
                            noise_level = self._get_noise_level_at_frequency(sideband_frequency, frequencies, noise_poly)
                            delta_l = None
                            if sideband_freq_info and sideband_freq_info.get('amplitude_db') is not None:
                                amplitude = sideband_freq_info.get('amplitude_db')
                                delta_l = amplitude - noise_level
                            else:
                                # Если частота не найдена, ищем амплитуду в спектре
                                freq_min = sideband_frequency - self.frequency_tolerance_hz
                                freq_max = sideband_frequency + self.frequency_tolerance_hz
                                mask = (frequencies >= freq_min) & (frequencies <= freq_max)
                                if np.any(mask):
                                    amplitudes_in_range = spectrum_db[mask]
                                    max_amplitude = np.max(amplitudes_in_range)
                                    delta_l = max_amplitude - noise_level
                            
                            # Если delta_l отрицательная, устанавливаем в 0
                            if delta_l is not None and delta_l < 0:
                                delta_l = 0.0
                            
                            # Вычисляем модуляцию для боковой полосы (только для огибающей)
                            modulation = None
                            if compute_modulation and delta_l is not None and delta_l >= 0:
                                try:
                                    # Если delta_l = 0, то модуляция = 0
                                    if delta_l == 0:
                                        modulation = 0.0
                                    else:
                                        # Проверяем, что выражение под корнем не отрицательное
                                        # m = sqrt((10^(ΔL/10) - 1) * (Δf_a / Δf_w)) * 100%
                                        expression_under_sqrt = (10 ** (delta_l / 10) - 1) * (frequency_resolution / filter_bandwidth)
                                        if expression_under_sqrt < 0:
                                            modulation = 0.0
                                        else:
                                            modulation = np.sqrt(expression_under_sqrt) * 100
                                except (ValueError, OverflowError):
                                    modulation = 0.0
                            
                            # Вычисляем критерий "Эталон" для боковой полосы (только для спектра с эталоном)
                            template_criterion_value = None
                            if spectrum_type == 'spectrum' and reference_spectrum_db is not None:
                                sideband_amplitude = sideband_freq_info.get('amplitude_db') if sideband_freq_info else None
                                if sideband_amplitude is None:
                                    # Ищем амплитуду в спектре
                                    freq_min = sideband_frequency - self.frequency_tolerance_hz
                                    freq_max = sideband_frequency + self.frequency_tolerance_hz
                                    mask = (frequencies >= freq_min) & (frequencies <= freq_max)
                                    if np.any(mask):
                                        amplitudes_in_range = spectrum_db[mask]
                                        sideband_amplitude = np.max(amplitudes_in_range)
                                
                                if sideband_amplitude is not None:
                                    # Находим амплитуду в эталонном спектре
                                    freq_min = sideband_frequency - self.frequency_tolerance_hz
                                    freq_max = sideband_frequency + self.frequency_tolerance_hz
                                    mask = (frequencies >= freq_min) & (frequencies <= freq_max)
                                    if np.any(mask):
                                        reference_amplitudes = reference_spectrum_db[mask]
                                        reference_amplitude = np.max(reference_amplitudes)
                                        # Разница: текущий минус эталон (в дБ)
                                        template_criterion_value = sideband_amplitude - reference_amplitude
                            
                            # Получаем информацию об основной гармонике для боковой полосы
                            # Вычисляем амплитуду основной частоты
                            main_amplitude = main_freq_info.get('amplitude_db') if main_freq_info else None
                            if main_amplitude is None:
                                # Ищем амплитуду основной частоты в спектре
                                freq_min = main_frequency - self.frequency_tolerance_hz
                                freq_max = main_frequency + self.frequency_tolerance_hz
                                mask = (frequencies >= freq_min) & (frequencies <= freq_max)
                                if np.any(mask):
                                    amplitudes_in_range = spectrum_db[mask]
                                    main_amplitude = np.max(amplitudes_in_range)
                            
                            # Получаем фактическую частоту основной гармоники
                            main_actual_freq = main_freq_info.get('frequency') if main_freq_info else None
                            if main_actual_freq is None:
                                # Если не нашли в main_freq_info, ищем в спектре
                                freq_min = main_frequency - self.frequency_tolerance_hz
                                freq_max = main_frequency + self.frequency_tolerance_hz
                                mask = (frequencies >= freq_min) & (frequencies <= freq_max)
                                if np.any(mask):
                                    # Берем частоту с максимальной амплитудой
                                    freq_indices = np.where(mask)[0]
                                    max_amp_idx = np.argmax(spectrum_db[mask])
                                    main_actual_freq = frequencies[freq_indices[max_amp_idx]]
                            
                            # Вычисляем критерий "Основная/боковая" для боковой полосы (только для спектра)
                            sideband_criterion_value = None
                            if spectrum_type == 'spectrum':
                                sideband_amplitude = sideband_freq_info.get('amplitude_db') if sideband_freq_info else None
                                if sideband_amplitude is None:
                                    # Ищем амплитуду в спектре
                                    freq_min = sideband_frequency - self.frequency_tolerance_hz
                                    freq_max = sideband_frequency + self.frequency_tolerance_hz
                                    mask = (frequencies >= freq_min) & (frequencies <= freq_max)
                                    if np.any(mask):
                                        amplitudes_in_range = spectrum_db[mask]
                                        sideband_amplitude = np.max(amplitudes_in_range)
                                
                                if sideband_amplitude is not None and main_amplitude is not None:
                                    # Разница: основная минус боковая (в дБ)
                                    sideband_criterion_value = main_amplitude - sideband_amplitude
                            
                            # Определяем, прошла ли эта боковая полоса проверку
                            # Используем информацию из rule_result.details
                            sideband_passed = False  # По умолчанию false
                            if rule_result and rule_result.details:
                                sideband_passed_map = rule_result.details.get('sideband_passed_map', {})
                                
                                # Проверяем, прошла ли эта конкретная боковая полоса свою проверку
                                # Это зависит только от её собственной проверки, не от общего результата правила
                                sideband_passed = sideband_passed_map.get(offset, False)
                            else:
                                # Если нет информации, используем общий результат как fallback
                                sideband_passed = rule_passed
                            
                            harmonics.append(HarmonicInfo(
                                frequency_type=modulating_freq_type,
                                multiplier=offset,
                                expected_frequency=sideband_frequency,
                                actual_frequency=sideband_freq_info.get('frequency') if sideband_freq_info else None,
                                amplitude_db=sideband_freq_info.get('amplitude_db') if sideband_freq_info else None,
                                delta_l=delta_l,
                                modulation=modulation,
                                template_criterion_value=template_criterion_value,
                                sideband_criterion_value=sideband_criterion_value,
                                is_present=sideband_is_present,
                                passed=sideband_passed,
                                use_for_defect_strength=sideband_use_for_strength,
                                offset=offset,
                                harmonic_type=harmonic_type,
                                main_expected_frequency=main_frequency,
                                main_actual_frequency=main_actual_freq,
                                main_amplitude_db=main_amplitude,
                                main_frequency_type=frequency_type,
                                main_multiplier=multiplier
                            ))
                    except ValueError:
                        pass
        
        # Вычисляем общие значения критериев
        # 1. Критерий "Основная/боковая": минимальное значение из прошедших правил (только для боковых полос)
        sideband_criterion_value = None
        if spectrum_type == 'spectrum':
            sideband_values = []
            candidate_harmonics = []
            for harmonic in harmonics:
                # Учитываем только боковые полосы с прошедшими правилами и use_for_defect_strength=True
                if (harmonic.harmonic_type in ('sideband', 'sideband_comparison') and 
                    harmonic.passed and 
                    harmonic.use_for_defect_strength and
                    harmonic.sideband_criterion_value is not None):
                    sideband_values.append(harmonic.sideband_criterion_value)
                    candidate_harmonics.append(harmonic)
            if sideband_values:
                sideband_criterion_value = min(sideband_values)
                # Помечаем только одну гармонику с минимальным значением (определяющую общее значение)
                for harmonic in candidate_harmonics:
                    if harmonic.sideband_criterion_value == sideband_criterion_value:
                        harmonic.used_for_sideband_criterion = criterion_strengths.get('sideband')
                        break  # Устанавливаем только для одной гармоники, остальные остаются с None
        
        # 2. Критерий "Эталон": максимальное значение из прошедших правил
        template_criterion_value = None
        if spectrum_type == 'spectrum' and reference_spectrum_db is not None:
            template_values = []
            candidate_harmonics = []
            for harmonic in harmonics:
                # Учитываем только гармоники с прошедшими правилами и use_for_defect_strength=True
                if (harmonic.passed and 
                    harmonic.use_for_defect_strength and
                    harmonic.template_criterion_value is not None):
                    template_values.append(harmonic.template_criterion_value)
                    candidate_harmonics.append(harmonic)
            if template_values:
                template_criterion_value = max(template_values)
                # Помечаем только одну гармонику с максимальным значением (определяющую общее значение)
                for harmonic in candidate_harmonics:
                    if harmonic.template_criterion_value == template_criterion_value:
                        harmonic.used_for_template_criterion = criterion_strengths.get('template')
                        break  # Устанавливаем только для одной гармоники, остальные остаются с None
        
        # 3. Критерий "Модуляция": максимальное значение из прошедших правил (только для огибающей)
        modulation_value = getattr(evaluation_result, 'modulation_value', None)
        if spectrum_type == 'envelope' and modulation_value is not None:
            # Находим гармонику с максимальной модуляцией среди прошедших правил
            max_modulation = None
            candidate_harmonic = None
            for harmonic in harmonics:
                if (harmonic.passed and 
                    harmonic.use_for_defect_strength and
                    harmonic.modulation is not None):
                    if max_modulation is None or harmonic.modulation > max_modulation:
                        max_modulation = harmonic.modulation
                        candidate_harmonic = harmonic
            # Помечаем только одну гармонику с максимальной модуляцией (определяющую общее значение)
            if candidate_harmonic is not None and abs(candidate_harmonic.modulation - modulation_value) < 1e-10:
                candidate_harmonic.used_for_modulation_criterion = criterion_strengths.get('modulation')
                # Остальные гармоники остаются с None (по умолчанию)
        
        # Разделяем гармоники по типу спектра (после вычисления всех флагов)
        spectrum_harmonics = harmonics if spectrum_type == 'spectrum' else []
        envelope_harmonics = harmonics if spectrum_type == 'envelope' else []
        
        return DefectDetectionReport(
            defect_name=defect_name,
            detected=evaluation_result.detected,
            defect_strength=evaluation_result.defect_strength,
            sideband_thresholds=sideband_thresholds,
            template_thresholds=template_thresholds,
            modulation_thresholds=modulation_thresholds,
            modulation=getattr(evaluation_result, 'modulation_value', None),
            sideband_criterion_value=sideband_criterion_value,
            template_criterion_value=template_criterion_value,
            recommendation=recommendation,
            harmonics=harmonics,  # Для обратной совместимости
            spectrum_harmonics=spectrum_harmonics,
            envelope_harmonics=envelope_harmonics
        )
    
    def create_combined_detection_report(
        self,
        spectrum_evaluation_result: DefectEvaluationResult,
        envelope_evaluation_result: DefectEvaluationResult,
        spectrum_rules: Dict[str, Any],
        envelope_rules: Dict[str, Any],
        spectrum_frequencies: np.ndarray,
        spectrum_db: np.ndarray,
        envelope_frequencies: np.ndarray,
        envelope_db: np.ndarray,
        equipment_frequencies: EquipmentFrequencies,
        defect_metadata: Dict[str, Any],
        reference_spectrum_db: Optional[np.ndarray] = None,
        frequency_resolution: Optional[float] = None,
        filter_bandwidth: Optional[float] = None,
        spectrum_weak: Optional[float] = None,
        spectrum_medium: Optional[float] = None,
        spectrum_strong: Optional[float] = None,
        spectrum_template_weak: Optional[float] = None,
        spectrum_template_medium: Optional[float] = None,
        spectrum_template_strong: Optional[float] = None,
        envelope_weak: Optional[float] = None,
        envelope_medium: Optional[float] = None,
        envelope_strong: Optional[float] = None
    ) -> DefectDetectionReport:
        """
        Создает объединенный отчет о дефекте из результатов оценки спектра и огибающей.
        
        :param spectrum_evaluation_result: Результат оценки правил для спектра
        :param envelope_evaluation_result: Результат оценки правил для огибающей
        :param spectrum_rules: JSON-структура правил для спектра
        :param envelope_rules: JSON-структура правил для огибающей
        :param spectrum_frequencies: Массив частот спектра (Гц)
        :param spectrum_db: Массив значений спектра в децибелах
        :param envelope_frequencies: Массив частот спектра огибающей (Гц)
        :param envelope_db: Массив значений спектра огибающей в децибелах
        :param equipment_frequencies: Базовые частоты оборудования
        :param defect_metadata: Метаданные о дефекте (название, пороги, рекомендации)
        :param reference_spectrum_db: Эталонный спектр в дБ (для критерия "эталон")
        :param frequency_resolution: Разрешение по частоте Δf_a (Гц) для критерия "модуляция"
        :param filter_bandwidth: Ширина полосы фильтра Δf_w (Гц) для критерия "модуляция"
        :param spectrum_weak: Порог для слабого дефекта критерия "Основная/боковая" (дБ)
        :param spectrum_medium: Порог для среднего дефекта критерия "Основная/боковая" (дБ)
        :param spectrum_strong: Порог для сильного дефекта критерия "Основная/боковая" (дБ)
        :param spectrum_template_weak: Порог для слабого дефекта критерия "Эталон" (дБ)
        :param spectrum_template_medium: Порог для среднего дефекта критерия "Эталон" (дБ)
        :param spectrum_template_strong: Порог для сильного дефекта критерия "Эталон" (дБ)
        :param envelope_weak: Порог для слабого дефекта критерия "Модуляция" (%)
        :param envelope_medium: Порог для среднего дефекта критерия "Модуляция" (%)
        :param envelope_strong: Порог для сильного дефекта критерия "Модуляция" (%)
        :return: Объединенный отчет о дефекте
        """
        # Создаем отдельные отчеты
        spectrum_report = self.create_detection_report(
            evaluation_result=spectrum_evaluation_result,
            rules=spectrum_rules,
            frequencies=spectrum_frequencies,
            spectrum_db=spectrum_db,
            equipment_frequencies=equipment_frequencies,
            defect_metadata=defect_metadata,
            spectrum_type='spectrum',
            reference_spectrum_db=reference_spectrum_db,
            spectrum_weak=spectrum_weak,
            spectrum_medium=spectrum_medium,
            spectrum_strong=spectrum_strong,
            spectrum_template_weak=spectrum_template_weak,
            spectrum_template_medium=spectrum_template_medium,
            spectrum_template_strong=spectrum_template_strong
        )
        
        envelope_report = self.create_detection_report(
            evaluation_result=envelope_evaluation_result,
            rules=envelope_rules,
            frequencies=envelope_frequencies,
            spectrum_db=envelope_db,
            equipment_frequencies=equipment_frequencies,
            defect_metadata=defect_metadata,
            spectrum_type='envelope',
            frequency_resolution=frequency_resolution,
            filter_bandwidth=filter_bandwidth,
            envelope_weak=envelope_weak,
            envelope_medium=envelope_medium,
            envelope_strong=envelope_strong
        )
        
        # Объединяем отчеты
        return self.create_combined_report(spectrum_report, envelope_report)
    
    def create_combined_report(
        self,
        spectrum_report: DefectDetectionReport,
        envelope_report: DefectDetectionReport
    ) -> DefectDetectionReport:
        """
        Объединяет отчеты по спектру и огибающей в один общий отчет.
        
        :param spectrum_report: Отчет по амплитудному спектру
        :param envelope_report: Отчет по спектру огибающей
        :return: Объединенный отчет
        """
        # Сила дефекта - максимальная из двух отчетов
        strength_map = {'weak': 1, 'medium': 2, 'strong': 3}
        spectrum_strength_value = strength_map.get(spectrum_report.defect_strength, 0)
        envelope_strength_value = strength_map.get(envelope_report.defect_strength, 0)
        max_strength_value = max(spectrum_strength_value, envelope_strength_value)
        
        defect_strength = None
        if max_strength_value > 0:
            for strength, value in strength_map.items():
                if value == max_strength_value:
                    defect_strength = strength
                    break
        
        # Дефект считается обнаруженным, если:
        # 1. Обнаружен хотя бы в одном из спектров, ИЛИ
        # 2. Определена степень развития (defect_strength не None)
        detected = spectrum_report.detected or envelope_report.detected or (defect_strength is not None)
        
        # Рекомендация - берем из того отчета, где дефект сильнее, или из спектра
        recommendation = None
        if envelope_strength_value > spectrum_strength_value:
            recommendation = envelope_report.recommendation
        else:
            recommendation = spectrum_report.recommendation
        
        # Объединяем все гармоники
        all_harmonics = spectrum_report.harmonics + envelope_report.harmonics
        
        # Берем значения критериев из спектра (для sideband и template) и из огибающей (для modulation)
        sideband_criterion_value = spectrum_report.sideband_criterion_value
        template_criterion_value = spectrum_report.template_criterion_value
        
        return DefectDetectionReport(
            defect_name=spectrum_report.defect_name,  # Название одинаковое
            detected=detected,
            defect_strength=defect_strength,
            spectrum_detected=spectrum_report.detected,
            envelope_detected=envelope_report.detected,
            spectrum_defect_strength=spectrum_report.defect_strength,
            envelope_defect_strength=envelope_report.defect_strength,
            sideband_thresholds=spectrum_report.sideband_thresholds,
            template_thresholds=spectrum_report.template_thresholds,
            modulation_thresholds=envelope_report.modulation_thresholds,
            modulation=envelope_report.modulation,
            sideband_criterion_value=sideband_criterion_value,
            template_criterion_value=template_criterion_value,
            recommendation=recommendation,
            harmonics=all_harmonics,  # Для обратной совместимости
            spectrum_harmonics=spectrum_report.harmonics,
            envelope_harmonics=envelope_report.harmonics
        )
    
    def _extract_all_rules(self, group: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Извлекает все правила из группы (рекурсивно)."""
        rules = []
        
        if group.get('type') == 'group':
            elements = group.get('elements', [])
            for element in elements:
                if element.get('type') == 'rule':
                    rules.append(element)
                elif element.get('type') == 'group':
                    rules.extend(self._extract_all_rules(element))
        
        return rules
    
    def _find_rule_result(
        self,
        result: Union[RuleEvaluationResult, GroupEvaluationResult],
        rule_id: str
    ) -> Optional[RuleEvaluationResult]:
        """Находит результат правила по ID."""
        if isinstance(result, RuleEvaluationResult):
            if result.rule_id == rule_id:
                return result
        elif isinstance(result, GroupEvaluationResult):
            for element_result in result.element_results:
                found = self._find_rule_result(element_result, rule_id)
                if found:
                    return found
        return None
    
    def _get_frequency_type_label(self, frequency_type: str) -> str:
        """Возвращает человекочитаемое название типа частоты."""
        labels = {
            'shaft': 'Частота вращения вала',
            'network_frequency': 'Частота сети',
            'bpfo': 'BPFO (частота прохождения шариков по наружному кольцу)',
            'bpfi': 'BPFI (частота прохождения шариков по внутреннему кольцу)',
            'bsf': 'BSF (частота вращения шариков)',
            'ftf': 'FTF (частота сепаратора)',
            'belt_belt': 'Частота ремня',
            'belt_driving': 'Частота ведущего шкива',
            'belt_driven': 'Частота ведомого шкива',
            'blades': 'Лопастная частота',
            'custom': 'Пользовательская частота'
        }
        return labels.get(frequency_type, frequency_type)

