"""
Расчёт падения напряжения в кабелях питания трансмиттеров
DEEPAK K1 — GP Plant, India
Схема 421457.103E1

Цепь питания:
  SCADA Ekor Box (24VDC) ──Cable 9 (250m)──> Connection Box
                                                  ├── Cable 3 (15m) ──> Трансмиттер №1
                                                  └── Cable 4 (15m) ──> Трансмиттер №2

ВАЖНО: Cable 9 несёт суммарный ток ОБОИХ трансмиттеров!
"""

# ── Физические константы ──────────────────────────────────────────
rho_20 = 0.0175      # Удельное сопротивление меди при 20°C, Ом·мм²/м
alpha_cu = 0.00393    # Температурный коэффициент меди, 1/°C

# ── Параметры кабелей ─────────────────────────────────────────────
cables = {
    'Cable 9': {'length_m': 250, 'section_mm2': 1.5, 'description': 'SCADA Box → Connection Box'},
    'Cable 3': {'length_m': 15,  'section_mm2': 1.5, 'description': 'Connection Box → Transmitter №1'},
    'Cable 4': {'length_m': 15,  'section_mm2': 1.5, 'description': 'Connection Box → Transmitter №2'},
}

# ── Параметры системы ─────────────────────────────────────────────
V_source = 24.0       # Напряжение источника питания, В

# Потребление трансмиттера Ekor (из документации K1):
#   "Power consumption of the transmitter: 8 W (0.35A)"
#   I = P / U = 8 Вт / 24 В = 0.333 А ≈ 0.35 А (паспортное)
#
# Сценарии нагрузки:
I_transmitter_scenarios = {
    'Минимальный (пуск, прогрев)':           0.200,     # 200 мА
    'Номинальный (выходы ~12мА)':            0.300,     # 300 мА
    'Паспортный (8 Вт / 24 В = 0.35 А)':    0.350,     # 350 мА — из документации
    'Максимальный (с запасом 10%)':          0.385,     # 385 мА
}

# Температурные сценарии (Индия, GP Plant)
temperatures = [20, 35, 50, 65]  # °C


def calc_resistance(length_m, section_mm2, temp_c):
    """Сопротивление одного проводника с учётом температуры"""
    rho_t = rho_20 * (1 + alpha_cu * (temp_c - 20))
    return rho_t * length_m / section_mm2


def calc_voltage_drop(r_loop, current_a):
    """Падение напряжения в петле (туда + обратно)"""
    return 2 * r_loop * current_a


# ═══════════════════════════════════════════════════════════════════
# РАСЧЁТ
# ═══════════════════════════════════════════════════════════════════
print("=" * 90)
print("  РАСЧЁТ ПАДЕНИЯ НАПРЯЖЕНИЯ В КАБЕЛЯХ ПИТАНИЯ ТРАНСМИТТЕРОВ")
print("  DEEPAK K1 — GP Plant  |  421457.103E1")
print("=" * 90)

# 1. Сопротивления кабелей
print("\n" + "─" * 90)
print("  1. СОПРОТИВЛЕНИЕ КАБЕЛЕЙ (одна жила, Ом)")
print("─" * 90)
print(f"  {'Кабель':<12} {'Длина, м':>10} {'Сечение':>10}", end="")
for t in temperatures:
    print(f" {'R@'+str(t)+'°C':>10}", end="")
print(f" {'R петли@50°C':>14}")
print("  " + "-" * 78)

for name, params in cables.items():
    L = params['length_m']
    S = params['section_mm2']
    print(f"  {name:<12} {L:>10} {str(S)+' мм²':>10}", end="")
    for t in temperatures:
        r = calc_resistance(L, S, t)
        print(f" {r:>10.3f}", end="")
    r_loop = 2 * calc_resistance(L, S, 50)
    print(f" {r_loop:>14.3f}")

# 2. Падение напряжения по сценариям
print("\n" + "─" * 90)
print("  2. ПАДЕНИЕ НАПРЯЖЕНИЯ И НАПРЯЖЕНИЕ НА ТРАНСМИТТЕРАХ")
print("─" * 90)

for temp in [20, 50, 65]:
    print(f"\n  ╔══ Температура кабеля: {temp}°C {'(лето, Индия, кабель на солнце)' if temp >= 50 else ''}")

    R9 = calc_resistance(250, 1.5, temp)
    R3 = calc_resistance(15, 1.5, temp)
    R4 = calc_resistance(15, 1.5, temp)

    print(f"  ║  R(Cable 9) одна жила = {R9:.3f} Ом, петля = {2*R9:.3f} Ом")
    print(f"  ║  R(Cable 3) одна жила = {R3:.3f} Ом, петля = {2*R3:.3f} Ом")
    print(f"  ║  R(Cable 4) одна жила = {R4:.3f} Ом, петля = {2*R4:.3f} Ом")
    print(f"  ║")

    for scenario, I_tx in I_transmitter_scenarios.items():
        I_total_cab9 = 2 * I_tx  # Cable 9 несёт ток ОБОИХ трансмиттеров

        dU_cab9 = calc_voltage_drop(R9, I_total_cab9)
        dU_cab3 = calc_voltage_drop(R3, I_tx)
        dU_cab4 = calc_voltage_drop(R4, I_tx)

        V_conn_box = V_source - dU_cab9
        V_T1 = V_source - dU_cab9 - dU_cab3
        V_T2 = V_source - dU_cab9 - dU_cab4

        dU_total_T1 = dU_cab9 + dU_cab3
        dU_total_T2 = dU_cab9 + dU_cab4
        pct_T1 = (dU_total_T1 / V_source) * 100
        P_cable9 = dU_cab9 * I_total_cab9
        P_cable3 = dU_cab3 * I_tx
        P_total = P_cable9 + P_cable3

        status_T1 = ""
        if V_T1 < 18.0:
            status_T1 = "⛔ НИЖЕ МИНИМУМА 18В!"
        elif V_T1 < 19.0:
            status_T1 = "⚠️  КРИТИЧНО НИЗКОЕ!"
        elif V_T1 < 20.0:
            status_T1 = "⚠️  Пониженное"
        else:
            status_T1 = "✅ Норма"

        print(f"  ║  ┌─ {scenario}")
        print(f"  ║  │  I трансмиттера = {I_tx*1000:.0f} мА, "
              f"I суммарный в Cable 9 = {I_total_cab9*1000:.0f} мА")
        print(f"  ║  │")
        print(f"  ║  │  Cable 9 (250м): ΔU = {dU_cab9:.2f} В  "
              f"(P = {P_cable9:.2f} Вт)")
        print(f"  ║  │  Cable 3 (15м):  ΔU = {dU_cab3:.2f} В  "
              f"(P = {P_cable3:.3f} Вт)")
        print(f"  ║  │")
        print(f"  ║  │  V на Connection Box = {V_conn_box:.2f} В")
        print(f"  ║  │  V на Трансмиттере 1 = {V_T1:.2f} В  "
              f"(потеряно {dU_total_T1:.2f} В = {pct_T1:.1f}%)  {status_T1}")
        print(f"  ║  │  V на Трансмиттере 2 = {V_T2:.2f} В")
        print(f"  ║  │  Суммарная мощность потерь = {P_total:.2f} Вт")
        print(f"  ║  └─")

    print(f"  ╚══")

# 3. Сводная таблица
print("\n" + "─" * 90)
print("  3. СВОДНАЯ ТАБЛИЦА: НАПРЯЖЕНИЕ НА КЛЕММАХ ТРАНСМИТТЕРА")
print("─" * 90)
print(f"  {'Сценарий':<42} {'20°C':>8} {'35°C':>8} {'50°C':>8} {'65°C':>8}")
print("  " + "-" * 78)

for scenario, I_tx in I_transmitter_scenarios.items():
    I_total = 2 * I_tx
    short_name = scenario.split('(')[0].strip()
    print(f"  {short_name + ' (' + str(int(I_tx*1000)) + ' мА)':<42}", end="")
    for temp in temperatures:
        R9 = calc_resistance(250, 1.5, temp)
        R3 = calc_resistance(15, 1.5, temp)
        dU = calc_voltage_drop(R9, I_total) + calc_voltage_drop(R3, I_tx)
        V = V_source - dU
        mark = " !" if V < 19.0 else ""
        print(f" {V:>7.2f}{mark}", end="")
    print()

print(f"\n  Допустимый диапазон питания трансмиттера: 18...30 В (типовой)")
print(f"  Рекомендуемый минимум: 20 В (с запасом на пульсации)")

# 4. Рекомендации
print("\n" + "═" * 90)
print("  4. ВЫВОДЫ И РЕКОМЕНДАЦИИ")
print("═" * 90)

# Worst case
R9_65 = calc_resistance(250, 1.5, 65)
R3_65 = calc_resistance(15, 1.5, 65)
I_worst = 0.350  # паспортное: 8 Вт / 24 В = 0.35 А
I_total_worst = 2 * I_worst
dU_worst = calc_voltage_drop(R9_65, I_total_worst) + calc_voltage_drop(R3_65, I_worst)
V_worst = V_source - dU_worst

print(f"""
  НАИХУДШИЙ СЛУЧАЙ (350 мА на трансмиттер = 8 Вт паспортн., 65°C):
  ─────────────────────────────────────────────
  Падение в Cable 9 (250м, 2×{I_total_worst*1000:.0f} мА): {calc_voltage_drop(R9_65, I_total_worst):.2f} В
  Падение в Cable 3/4 (15м):                   {calc_voltage_drop(R3_65, I_worst):.2f} В
  ИТОГО падение:                                {dU_worst:.2f} В ({dU_worst/24*100:.1f}%)
  НАПРЯЖЕНИЕ НА ТРАНСМИТТЕРЕ:                   {V_worst:.2f} В
""")

if V_worst < 18.0:
    print("  ⛔ КРИТИЧЕСКАЯ ПРОБЛЕМА: Напряжение ниже минимума 18В!")
    print("     Трансмиттеры могут не запуститься или работать нестабильно.")
elif V_worst < 20.0:
    print("  ⚠️  ПРОБЛЕМА: Напряжение ниже рекомендуемого минимума 20В.")
    print("     Возможна нестабильная работа при максимальной нагрузке.")

print(f"""
  РЕКОМЕНДАЦИИ:
  ─────────────
  1. УВЕЛИЧИТЬ сечение Cable 9 с 1.5 мм² до 2.5 мм²:""")

R9_25 = 0.0175 * (1 + alpha_cu * (65 - 20)) * 250 / 2.5
dU_25 = calc_voltage_drop(R9_25, I_total_worst) + calc_voltage_drop(R3_65, I_worst)
V_25 = V_source - dU_25
print(f"     → V на трансмиттере (65°C, 350мА) = {V_25:.2f} В  ✅")

print(f"""
  2. Или ПОВЫСИТЬ напряжение источника до 27В (если блок питания позволяет):
     → V на трансмиттере (65°C, 350мА) = {V_worst + 3:.2f} В  ✅

  3. Или СОКРАТИТЬ длину Cable 9 (перенести SCADA box ближе):
     При 100м вместо 250м:""")

R9_100 = 0.0175 * (1 + alpha_cu * (65 - 20)) * 100 / 1.5
dU_100 = calc_voltage_drop(R9_100, I_total_worst) + calc_voltage_drop(R3_65, I_worst)
V_100 = V_source - dU_100
print(f"     → V на трансмиттере (65°C, 350мА) = {V_100:.2f} В  ✅")

print(f"""
  4. МИНИМАЛЬНОЕ решение — установить ОТДЕЛЬНЫЙ блок питания 24VDC
     вблизи Connection Box (питание по Cable 10 → 230VAC → DC/DC).
     Это полностью исключит падение на 250м Cable 9.""")

print("\n" + "=" * 90)
