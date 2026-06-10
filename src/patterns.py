from scipy.signal import find_peaks
import numpy as np


def detect_double_bottom(close):

    prices = np.array(close).flatten()

    valleys, _ = find_peaks(-prices, distance=20)

    if len(valleys) < 2:
        return False

    v1 = prices[valleys[-2]]
    v2 = prices[valleys[-1]]

    diff = abs(v1 - v2) / max(v1, v2)

    return diff < 0.03


def detect_inverse_head_shoulders(close):

    prices = np.array(close).flatten()

    valleys, _ = find_peaks(-prices, distance=15)

    if len(valleys) < 3:
        return False

    a = prices[valleys[-3]]
    b = prices[valleys[-2]]
    c = prices[valleys[-1]]

    return b < a and b < c


def detect_ascending_triangle(close):

    prices = np.array(close).flatten()[-60:]

    if len(prices) < 60:
        return False

    resistance = np.max(prices)

    highs = prices[prices > resistance * 0.98]

    if len(highs) < 3:
        return False

    lows = []

    for i in range(1, len(prices) - 1):
        if prices[i] < prices[i - 1] and prices[i] < prices[i + 1]:
            lows.append(prices[i])

    if len(lows) < 3:
        return False

    return lows[-1] > lows[0]
