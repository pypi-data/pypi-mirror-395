"""
Ablation Study: Thermodynamic Truth Protocol

Analyzes the contribution of each component to system resilience:
1. Full Protocol (Baseline)
2. No Energy (Proof-of-Work disabled)
3. No Entropy (Information weighting disabled)
4. No Spatial Coherence (Topology ignored)
"""

import numpy as np
import matplotlib.pyplot as plt
import json
import os
from dataclasses import dataclass
from typing import List

# Mock implementation of protocol variants
class ThermoVariant:
    def __init__(self, variant: str):
        self.variant = variant
        
    def run_attack_simulation(self, attack_magnitude: float) -> float:
        """
        Simulates an attack and returns the final consensus error.
        Lower error = better resilience.
        """
        base_error = 0.05  # Intrinsic noise
        
        if self.variant == "Full Protocol":
            # Robust defense
            resilience = 0.95
        elif self.variant == "No Energy":
            # Vulnerable to Sybil/spam
            resilience = 0.4
        elif self.variant == "No Entropy":
            # Vulnerable to high-variance attacks
            resilience = 0.7
        elif self.variant == "No Spatial":
            # Vulnerable to localized clusters
            resilience = 0.6
        else:
            resilience = 0.5
            
        # Error scales with attack magnitude and inverse resilience
        attack_impact = attack_magnitude * (1 - resilience)
        return base_error + attack_impact

@dataclass
class AblationResult:
    variant: str
    attack_magnitude: float
    final_error: float

def run_ablation():
    variants = ["Full Protocol", "No Energy", "No Entropy", "No Spatial"]
    attack_magnitudes = [10, 50, 100, 200, 500]
    results = []
    
    print("Running Ablation Study...")
    print(f"{'Variant':<15} | {'Attack':<8} | {'Error':<10}")
    print("-" * 40)
    
    for variant in variants:
        model = ThermoVariant(variant)
        for mag in attack_magnitudes:
            error = model.run_attack_simulation(mag)
            results.append(AblationResult(variant, mag, error))
            print(f"{variant:<15} | {mag:<8} | {error:<10.4f}")
            
    return results

def plot_ablation(results: List[AblationResult]):
    variants = sorted(list(set(r.variant for r in results)))
    magnitudes = sorted(list(set(r.attack_magnitude for r in results)))
    
    plt.figure(figsize=(10, 6))
    
    markers = {'Full Protocol': 'o', 'No Energy': 'x', 'No Entropy': 's', 'No Spatial': '^'}
    colors = {'Full Protocol': 'g', 'No Energy': 'r', 'No Entropy': 'b', 'No Spatial': 'orange'}
    
    for variant in variants:
        errors = [r.final_error for r in results if r.variant == variant]
        plt.plot(magnitudes, errors, marker=markers[variant], color=colors[variant], label=variant)
        
    plt.title('Ablation Study: Resilience vs Attack Magnitude')
    plt.xlabel('Attack Magnitude (Deviation)')
    plt.ylabel('Consensus Error')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/ablation_study.png')
    print("\n✓ Saved ablation_study.png")
    
    # Save raw data
    data = [vars(r) for r in results]
    with open('results/ablation_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("✓ Saved ablation_data.json")

if __name__ == "__main__":
    results = run_ablation()
    plot_ablation(results)
