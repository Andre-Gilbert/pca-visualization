"""Constants."""
from manim import *


class FontSize:
    HEADING1 = 38
    HEADING2 = 34
    HEADING3 = 30
    HEADING4 = 26
    TEXT = 24


class Formulas:
    CENTERED_MATRIX = MathTex(r"\textbf{B} = X - \bar{X}")
    COVARIANCE = MathTex(
        r"\operatorname{cov}[X_i, X_j] = \operatorname{E}[(X_i - \operatorname{E}[X_i])(X_j - \operatorname{E}[X_j])]"
    )
    COVARIANCE_SIMPLIFIED = MathTex(r"\operatorname{cov}[X_i, X_j] = \operatorname{E}[X_i \cdot X_j]")
    COVARIANCE_MATRIX = MathTex(r"Cov(X) = \frac{1}{i}(B^TB)")
    PRINCIPAL_COMPONENTS = MathTex(r"T = E_b \cdot B")
