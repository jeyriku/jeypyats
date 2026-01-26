---

### Structure du projet

```
generate_topology/
├── __init__.py
├── main.py                # Script principal pour exécuter le processus
├── utils/
│   ├── __init__.py
│   ├── file_manager.py    # Gestion des fichiers YAML
│   ├── command_runner.py  # Exécution des commandes LLDP/CDP
│   ├── parser.py          # Analyse des données LLDP/CDP
├── topology/
│   ├── __init__.py
│   ├── builder.py         # Construction de la topologie
│   ├── saver.py           # Sauvegarde de la topologie
├── tests/
│   ├── __init__.py
│   ├── test_parser.py     # Tests unitaires pour le module parser
│   ├── test_builder.py    # Tests pour la génération de topologie
├── requirements.txt       # Dépendances Python
└── README.md              # Documentation du projet
```

---

### 1. **Module : `file_manager.py`**

Ce module gère la lecture et l'écriture des fichiers YAML.

```python
import yaml

def load_yaml(file_path):
    """
    Charger un fichier YAML.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def save_yaml(data, file_path):
    """
    Sauvegarder un fichier YAML.
    """
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
```

---

### 2. **Module : `command_runner.py`**

Ce module exécute les commandes LLDP/CDP sur les appareils via SSH.

```python
import subprocess

def run_command_on_device(alias, command):
    """
    Exécuter une commande distante sur un appareil.
    """
    try:
        output = subprocess.check_output(
            f"ssh {alias} '{command}'",
            shell=True,
            text=True,
        )
        return output
    except subprocess.CalledProcessError as e:
        print(f"Erreur d'exécution de la commande sur {alias}: {e}")
        return None
```

---

### 3. **Module : `parser.py`**

Ce module analyse les données collectées à partir de LLDP/CDP.

```python
def parse_neighbors(output):
    """
    Analyser la sortie LLDP/CDP pour extraire les voisins.
    """
    neighbors = []

    if output:
        for line in output.splitlines():
            # Supposons que la sortie contienne des colonnes Device-ID et Port-ID
            parts = line.split()
            if len(parts) >= 2:
                neighbors.append({"device": parts[0], "interface": parts[1]})

    return neighbors
```

---

### 4. **Module : `builder.py`**

Ce module construit la topologie à partir des informations collectées.

```python
from utils.command_runner import run_command_on_device
from utils.parser import parse_neighbors

def generate_topology(devices):
    """
    Générer une topologie à partir des données LLDP/CDP.
    """
    topology = {}

    for device_name, device in devices.items():
        print(f"Collecte des voisins pour {device_name} ({device['alias']})...")

        # Exécuter une commande pour récupérer les voisins
        output = run_command_on_device(device["alias"], "show lldp neighbors")

        # Analyser les voisins
        neighbors = parse_neighbors(output)

        # Construire les connexions
        topology[device_name] = {
            "interfaces": [
                {"connected_to": neighbor["device"], "interface": neighbor["interface"]}
                for neighbor in neighbors
            ]
        }

    return topology
```

---

### 5. **Module : `saver.py`**

Ce module gère la sauvegarde de la topologie dans le fichier testbed YAML.

```python
from utils.file_manager import save_yaml

def save_topology(testbed, topology, output_file):
    """
    Ajouter la topologie générée au testbed et sauvegarder dans un fichier.
    """
    testbed["topology"] = topology
    save_yaml(testbed, output_file)
    print(f"Topology saved to {output_file}")
```

---

### 6. **Script principal : `main.py`**

Le script principal utilise tous les modules pour exécuter le processus complet.

```python
from utils.file_manager import load_yaml
from topology.builder import generate_topology
from topology.saver import save_topology

def main():
    # Fichiers d'entrée et de sortie
    input_yaml = "sw_tb_v1.0.yaml"
    output_yaml = "sw_tb_with_topology.yaml"

    # Charger le testbed
    testbed = load_yaml(input_yaml)

    # Vérifier si des appareils existent
    devices = testbed.get("devices", {})
    if not devices:
        print("Aucun appareil trouvé dans le fichier testbed.")
        return

    # Générer la topologie basée sur LLDP/CDP
    topology = generate_topology(devices)

    # Sauvegarder le testbed avec la topologie
    save_topology(testbed, topology, output_yaml)

if __name__ == "__main__":
    main()
```

---

### 7. **Tests unitaires (exemple)**

Pour tester chaque module, vous pouvez créer des fichiers comme `test_parser.py` :

```python
from utils.parser import parse_neighbors

def test_parse_neighbors():
    output = """
    Device ID       Local Intf      Port ID
    Switch1         Gi1/0/1         Gi1/0/2
    Router1         Gi1/0/2         Gi0/1
    """
    expected = [
        {"device": "Switch1", "interface": "Gi1/0/1"},
        {"device": "Router1", "interface": "Gi1/0/2"},
    ]
    assert parse_neighbors(output) == expected
```

---

### Avantages de cette architecture

1. **Lisibilité** : Chaque module a une responsabilité spécifique.
2. **Réutilisabilité** : Les fonctions dans des modules comme `file_manager.py` peuvent être réutilisées dans d'autres projets.
3. **Testabilité** : Chaque module peut être testé individuellement avec des tests unitaires.
4. **Évolutivité** : Vous pouvez facilement ajouter d'autres protocoles ou fonctionnalités (comme SNMP ou Netconf) en créant de nouveaux modules.

---