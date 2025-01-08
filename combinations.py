import numpy as np
from scipy.optimize import linprog
from itertools import combinations

# Referenzmuster (WHO-Empfehlung in mg)
reference = np.array([
    10,  # Histidin (H)
    20,  # Isoleucin (I)
    39   # Leucin (L)
])

# Nährwerte der Lebensmittel (mg pro kg)
foods = {
    'Apfel':  np.array([6, 3, 11]),   # H, I, L
    'Birne':  np.array([1, 4, 1]),    # H, I, L
    'Tomate': np.array([3, 5, 2])     # H, I, L
}

def optimize_combination(food1_name, food2_name):
    """
    Optimiert die Kombination zweier Lebensmittel, um das Referenzmuster bestmöglich zu erreichen.
    """
    food1 = foods[food1_name]
    food2 = foods[food2_name]

    # Erstelle die Koeffizientenmatrix A und den Zielvektor b
    A = np.vstack([food1, food2]).T
    b = reference

    # Zielfunktion: Minimiere die Summe der absoluten Abweichungen
    # Wir fügen Hilfsvariablen hinzu, um absolute Abweichungen zu modellieren
    # [x1, x2, u1, u2, u3, v1, v2, v3]
    # Dabei sind:
    # x1, x2: Mengen der Lebensmittel
    # ui, vi: positive und negative Abweichungen für jede Aminosäure
    c = np.array([0, 0, 1, 1, 1, 1, 1, 1])

    # Erweiterte Koeffizientenmatrix für die Abweichungsvariablen
    A_eq = np.hstack([
        A,
        np.eye(3),    # ui (positive Abweichungen)
        -np.eye(3)    # vi (negative Abweichungen)
    ])

    # Nichtnegativitätsbedingungen für alle Variablen
    bounds = [(0, None) for _ in range(8)]

    # Löse das Optimierungsproblem
    result = linprog(
        c,
        A_eq=A_eq,
        b_eq=b,
        bounds=bounds,
        method='highs'
    )

    if result.success:
        food1_amount = result.x[0]
        food2_amount = result.x[1]
        achieved_values = food1_amount * food1 + food2_amount * food2
        total_deviation = sum(abs(achieved_values - reference))

        return {
            'success': True,
            'food1': (food1_name, food1_amount),
            'food2': (food2_name, food2_amount),
            'achieved_values': achieved_values,
            'deviation': total_deviation
        }
    else:
        return {'success': False}

def find_best_combination():
    """
    Findet die beste Kombination aus allen möglichen Lebensmittelpaaren.
    """
    best_result = None
    min_deviation = float('inf')

    for food1, food2 in combinations(foods.keys(), 2):
        result = optimize_combination(food1, food2)
        if result['success'] and result['deviation'] < min_deviation:
            min_deviation = result['deviation']
            best_result = result

    return best_result

# Hauptprogramm
if __name__ == "__main__":
    best_combination = find_best_combination()

    if best_combination:
        print("Beste gefundene Kombination:")
        food1_name, food1_amount = best_combination['food1']
        food2_name, food2_amount = best_combination['food2']

        print(f"\n{food1_name}: {food1_amount:.2f} kg")
        print(f"{food2_name}: {food2_amount:.2f} kg")

        print("\nErreichte Werte (mg):")
        print(f"Histidin:  {best_combination['achieved_values'][0]:.2f} (Ziel: {reference[0]})")
        print(f"Isoleucin: {best_combination['achieved_values'][1]:.2f} (Ziel: {reference[1]})")
        print(f"Leucin:    {best_combination['achieved_values'][2]:.2f} (Ziel: {reference[2]})")
        print(f"\nGesamtabweichung: {best_combination['deviation']:.2f} mg")
    else:
        print("Keine gültige Lösung gefunden.")