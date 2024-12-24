import requests
import pygame
import random
import json
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
import io
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chemical Compound Game")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 102, 204)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
HEADER_FONT = pygame.font.Font(None, 48)
FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 28)

def get_compound_properties_by_name(name):
    """Fetch compound properties from PubChem."""
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/property/IUPACName,MolecularFormula,MolecularWeight/JSON"
    cid_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/cids/JSON"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        properties = data["PropertyTable"]["Properties"][0]

        cid_response = requests.get(cid_url)
        cid_response.raise_for_status()
        cid_data = cid_response.json()
        cid = cid_data["IdentifierList"]["CID"][0] if "IdentifierList" in cid_data else "N/A"

        return (
            properties.get("IUPACName", None),
            properties.get("MolecularFormula", None),
            properties.get("MolecularWeight", None),
            cid
        )
    except (requests.exceptions.RequestException, KeyError):
        return None, None, None, None

def generate_3d_molecule(smiles):
    """Generate 3D molecular structure using RDKit."""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            mol = Chem.AddHs(mol)
            AllChem.EmbedMolecule(mol, AllChem.ETKDG())
            AllChem.MMFFOptimizeMolecule(mol)
            return mol
        else:
            return None
    except Exception:
        return None

def display_3d_molecule(mol):
    """Display 3D molecular structure."""
    if mol:
        img = Draw.MolToImage(mol, size=(500, 500))
        img.show()  # Show the image in the default image viewer
        print("3D model generated for the molecule.")
    else:
        print("Failed to generate 3D model.")

def load_chemical_equations(file_path):
    """Load chemical equations from JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: Chemical equations file not found!")
        return []

def stage1():
    running = True
    input_text = ""
    message = "Enter a compound name:"
    compound_name = None
    iupac_name = None
    molecular_formula = None
    cid = None

    while running:
        screen.fill(LIGHT_BLUE)
        header = HEADER_FONT.render("Stage 1: Compound Name Input", True, DARK_BLUE)
        screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 20))
        instruction = FONT.render(message, True, BLACK)
        screen.blit(instruction, (50, 100))
        pygame.draw.rect(screen, WHITE, (50, 150, 700, 40), border_radius=5)
        input_render = FONT.render(input_text, True, BLACK)
        screen.blit(input_render, (60, 160))

        if iupac_name or molecular_formula:
            y_offset = 220
            iupac_text = f"IUPAC Name: {iupac_name if iupac_name else 'N/A'}"
            formula_text = f"Molecular Formula: {molecular_formula if molecular_formula else 'N/A'}"
            cid_text = f"CID: {cid if cid else 'N/A'}"
            screen.blit(FONT.render(iupac_text, True, BLACK), (50, y_offset))
            screen.blit(FONT.render(formula_text, True, BLACK), (50, y_offset + 40))
            screen.blit(FONT.render(cid_text, True, BLACK), (50, y_offset + 80))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None, None, None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    compound_name = input_text.strip()
                    iupac_name, molecular_formula, _, cid = get_compound_properties_by_name(compound_name)
                    if iupac_name or molecular_formula:
                        message = "Compound found!"
                        pygame.time.delay(1000)
                        return True, compound_name, molecular_formula, cid
                    else:
                        message = "Compound not found. Try again."
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
    return True, None, None, None

def stage2(compound_name, molecular_formula):
    input_text = ""
    message = f"Enter the molecular weight of {compound_name}:"
    _, _, molecular_weight, _ = get_compound_properties_by_name(compound_name)
    if not molecular_weight:
        print("Error fetching molecular weight.")
        return False

    while True:
        screen.fill(LIGHT_BLUE)
        header = HEADER_FONT.render("Stage 2: Molecular Weight Guess", True, DARK_BLUE)
        screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 20))
        instruction = FONT.render(message, True, BLACK)
        screen.blit(instruction, (50, 100))
        pygame.draw.rect(screen, WHITE, (50, 150, 700, 40), border_radius=5)
        input_render = FONT.render(input_text, True, BLACK)
        screen.blit(input_render, (60, 160))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        user_guess = float(input_text.strip())
                        if abs(user_guess - float(molecular_weight)) <= 2:
                            smiles_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{compound_name}/property/CanonicalSMILES/JSON"
                            response = requests.get(smiles_url)
                            smiles = response.json()["PropertyTable"]["Properties"][0].get("CanonicalSMILES", None)
                            if smiles:
                                mol = generate_3d_molecule(smiles)
                                display_3d_molecule(mol)
                            print(f"Correct molecular weight entered for {compound_name}.")
                            return True
                        else:
                            message = "Incorrect. Try again."
                    except ValueError:
                        message = "Invalid input. Enter a number."
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode


def stage3():
    chemical_equations = load_chemical_equations("chemical_equations.json")
    current_equation = random.choice(chemical_equations)
    input_text = ""
    message = "Balance the equation:"

    while True:
        screen.fill(LIGHT_BLUE)
        header = HEADER_FONT.render("Stage 3: Balancing Equations", True, DARK_BLUE)
        screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 20))
        equation = " + ".join(current_equation["reactants"]) + " -> " + " + ".join(current_equation["products"])
        equation_render = FONT.render(equation, True, BLACK)
        screen.blit(equation_render, (50, 100))
        pygame.draw.rect(screen, WHITE, (50, 150, 700, 40), border_radius=5)
        input_render = FONT.render(input_text, True, BLACK)
        screen.blit(input_render, (60, 160))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip() == current_equation["balanced"]:
                        print("Correct! Proceeding to the next stage.")
                        return True
                    else:
                        message = "Incorrect balance. Try again."
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

def stage4():
    """Reaction Rate Constant Game."""
    def generate_reaction():
        """Generate random reaction coefficients and concentrations."""
        A = random.randint(1, 6)
        B = random.randint(1, 6)
        C = random.randint(1, 6)
        D = random.randint(1, 6)
        a_eq = round(random.uniform(0.001, 0.1), 3)
        b_eq = round(random.uniform(0.001, 0.1), 3)
        c_eq = round(random.uniform(0.001, 0.1), 3)
        d_eq = round(random.uniform(0.001, 0.1), 3)
        return A, B, C, D, a_eq, b_eq, c_eq, d_eq

    def calculate_rate_constant(A, B, C, D, a_eq, b_eq, c_eq, d_eq):
        """Calculate the rate constant k."""
        return (c_eq**C * d_eq**D) / (a_eq**A * b_eq**B)

    def plot_dynamic_concentration(A, B, C, D, a_eq, b_eq, c_eq, d_eq):
        """Plot dynamic concentration changes over time."""
        time = np.linspace(0, 50, 500)
        a_start, b_start, c_start, d_start = 0.1, 0.1, 0.0, 0.0

        a_conc = a_start + (a_eq - a_start) * (1 - np.exp(-0.1 * time))
        b_conc = b_start + (b_eq - b_start) * (1 - np.exp(-0.1 * time))
        c_conc = c_start + (c_eq - c_start) * (1 - np.exp(-0.1 * time))
        d_conc = d_start + (d_eq - d_start) * (1 - np.exp(-0.1 * time))

        fig, ax = plt.subplots()
        ax.set_xlim(0, 50)
        ax.set_ylim(0, 0.12)
        ax.set_title("Concentration Dynamics")
        ax.set_xlabel("Time")
        ax.set_ylabel("Concentration")

        line_a, = ax.plot([], [], label="Reactant A", color="blue")
        line_b, = ax.plot([], [], label="Reactant B", color="green")
        line_c, = ax.plot([], [], label="Product C", color="red")
        line_d, = ax.plot([], [], label="Product D", color="orange")

        ax.legend()

        def update(frame):
            line_a.set_data(time[:frame], a_conc[:frame])
            line_b.set_data(time[:frame], b_conc[:frame])
            line_c.set_data(time[:frame], c_conc[:frame])
            line_d.set_data(time[:frame], d_conc[:frame])
            return line_a, line_b, line_c, line_d

        ani = FuncAnimation(fig, update, frames=len(time), interval=50, blit=True)
        plt.show()

    input_text = ""
    message = "Enter the rate constant k (e.g., 4*10**-4):"
    A, B, C, D, a_eq, b_eq, c_eq, d_eq = generate_reaction()
    k_actual = calculate_rate_constant(A, B, C, D, a_eq, b_eq, c_eq, d_eq)

    while True:
        screen.fill(LIGHT_BLUE)
        header = HEADER_FONT.render("Stage 4: Reaction Rate Constant Game", True, DARK_BLUE)
        screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 20))
        reaction_text = f"Reaction: {A}A + {B}B -> {C}C + {D}D"
        screen.blit(FONT.render(reaction_text, True, BLACK), (50, 100))
        concentrations_text = f"Equilibrium concentrations (mol/L): A={a_eq}, B={b_eq}, C={c_eq}, D={d_eq}"
        screen.blit(FONT.render(concentrations_text, True, BLACK), (50, 150))
        instruction = FONT.render(message, True, BLACK)
        screen.blit(instruction, (50, 250))
        pygame.draw.rect(screen, WHITE, (50, 300, 900, 50))
        input_render = FONT.render(input_text, True, BLACK)
        screen.blit(input_render, (60, 310))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        k_user = eval(input_text.strip())
                        if abs(k_user - k_actual) < 0.1 * k_actual:
                            plot_dynamic_concentration(A, B, C, D, a_eq, b_eq, c_eq, d_eq)
                            return True
                        else:
                            message = "Incorrect. Try again."
                    except Exception:
                        message = "Invalid input. Use scientific notation like 4*10**-4."
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

# --- Main Function ---
def main():
    stages = [
        ("Stage 1: Compound Name Input", stage1),
        ("Stage 2: Molecular Weight Guess", stage2),
        ("Stage 3: Balancing Equations", stage3),
        ("Stage 4: Reaction Rate Constant", stage4),
    ]

    stage_index = 0
    while stage_index < len(stages):
        stage_name, stage_func = stages[stage_index]
        if stage_name == "Stage 2: Molecular Weight Guess":
            _, compound_name, molecular_formula, _ = stages[0][1]()  # Use Stage 1 result
            if not stage_func(compound_name, molecular_formula):
                print("Game over.")
                return
        else:
            if not stage_func():
                print("Game over.")
                return
        stage_index += 1

    # 游戏胜利画面
    screen.fill(LIGHT_BLUE)
    header = HEADER_FONT.render("Congratulations! You won!", True, BLACK)
    screen.blit(header, (WIDTH // 2 - header.get_width() // 2, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(5000)
    pygame.quit()


if __name__ == "__main__":
    main()
