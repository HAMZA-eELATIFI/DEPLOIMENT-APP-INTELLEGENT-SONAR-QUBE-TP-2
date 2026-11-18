from credit import calculate_risk


# ---------- Partie A : cas normaux ----------

def test_high_risk():
    result = calculate_risk(1000, 700)
    assert result == "HIGH"


def test_medium_risk():
    result = calculate_risk(1000, 400)
    assert result == "MEDIUM"


def test_low_risk():
    result = calculate_risk(1000, 100)
    assert result == "LOW"


# ---------- Partie B : cas limites ----------

def test_income_zero():
    assert calculate_risk(0, 500) == -1


def test_income_negative():
    assert calculate_risk(-1000, 500) == -1


def test_debt_zero():
    assert calculate_risk(1000, 0) == "LOW"


def test_ratio_exactly_0_3():
    # 300 / 1000 = 0.3 -> pas strictement > 0.3 -> LOW
    assert calculate_risk(1000, 300) == "LOW"


def test_ratio_exactly_0_6():
    # 600 / 1000 = 0.6 -> pas strictement > 0.6 -> MEDIUM
    assert calculate_risk(1000, 600) == "MEDIUM"
