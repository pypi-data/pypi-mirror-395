import numpy as np
from scipy.signal import hilbert
from .frequency_analysis import compute_amplitude_spectrum
from .preprocessing import filter_signal, apply_window

def compute_envelope_spectrum(signal, sampling_rate, lowcut, highcut,
                             window_type=None, frequency_resolution=None,
                             noise_window_hz=100):
    """
    Вычисляет спектр огибающей сигнала с возможностью управления частотным разрешением.

    :param signal: Входной сигнал.
    :param sampling_rate: Частота дискретизации (Гц).
    :param lowcut: Нижняя граница полосы фильтра (Гц).
    :param highcut: Верхняя граница полосы фильтра (Гц).
    :param window_type: Тип окна (None, 'hann', 'hamming', 'blackman').
    :param frequency_resolution: Желаемое частотное разрешение (Гц). Если None, используется длина сигнала.
    :param noise_window_hz: Размер окна для оценки уровня шума в герцах (по умолчанию 100 Гц).
    :return: Кортеж (frequencies, envelope_spectrum, phase_spectrum, noise_level), где:
             - frequencies: Массив частот (Гц).
             - envelope_spectrum: Спектр огибающей.
             - phase_spectrum: Фазовый спектр огибающей (в радианах).
             - noise_level: Оценка уровня шума в дБ (скользящее среднее спектра огибающей).
    """
    # Применяем полосовой фильтр
    filtered_signal = signal
    if lowcut is not None and highcut is not None:
        filter_type = 'bandpass'
        if lowcut == 0:
            filter_type = 'lowpass'
        filtered_signal = filter_signal(signal, (lowcut, highcut), sampling_rate, filter_type)

    # Накладываем окно (если указано)
    if window_type is not None:
        filtered_signal = apply_window(filtered_signal, window_type)

    # Вычисляем огибающую с помощью преобразования Гильберта
    analytic_signal = hilbert(filtered_signal)
    envelope = np.abs(analytic_signal)

    # Вычисляем спектр огибающей с заданным разрешением
    frequencies, spectrum, phase, noise_level = compute_amplitude_spectrum(
        envelope,
        sampling_rate,
        window_type=window_type,
        frequency_resolution=frequency_resolution,
        noise_window_hz=noise_window_hz
    )

    return frequencies, spectrum, phase, noise_level