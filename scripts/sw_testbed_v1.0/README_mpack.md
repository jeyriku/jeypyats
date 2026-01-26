---

### Structure des packages proposée
```
project_root/
├── tests/
│   ├── __init__.py
│   ├── connectivity_test.py    # Contient les tests liés à la connectivité
├── devices/
│   ├── __init__.py
│   ├── device.py               # Gestion des dispositifs
├── utils/
│   ├── __init__.py
│   ├── file_loader.py          # Chargement des fichiers YAML
├── main.py                     # Point d'entrée pour exécuter les tests
├── sw_tb_v1.0.yaml             # Fichier de testbed
└── requirements.txt            # Dépendances du projet
```

Voici le code refactorisé avec cette structure :

---

### `devices/device.py`
```python
import subprocess
import sys

class Device:
    def __init__(self, alias, ip):
        self.alias = alias
        self.ip = ip

    def ping(self, ip_address):
        print(f"\nPerforming real ping to {ip_address}...")
        try:
            param = "-n" if sys.platform.lower() == "win32" else "-c"
            command = ["ping", param, "4", ip_address]
            response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if response.returncode == 0:
                print(f"Ping to {ip_address} successful!")
                return True
            else:
                print(f"Ping to {ip_address} failed!")
                return False

        except Exception as e:
            print(f"An error occurred during the ping test: {e}")
            return False
```

---

### `utils/file_loader.py`
```python
import yaml

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
```

---

### `tests/connectivity_test.py`
```python
from pyats.aetest import Testcase, test
from devices.device import Device
from utils.file_loader import load_yaml

class ConnectivityTest(Testcase):
    def __init__(self, file_yaml):
        self.data = load_yaml(file_yaml)
        self.devices = []

    @test
    def check_connectivity(self):
        devices = self.data.get('devices', {})
        print("\nTestbed devices:", devices)

        for device_name, device_list in devices.items():
            try:
                device = self.create_device(device_list)
                print(f"\nChecking connectivity for device: {device_name} ({device.alias})")
                connected = device.ping(device_list.get('alias', ''))
                assert connected, f"Connection failed for device {device_name}"
                self.devices.append(device)

            except Exception as e:
                self.failed(f"Test failed for device {device_name} due to: {str(e)}")
                print(f"\nError for {device_name}: {str(e)}")

        print("\nSuccessfully connected devices:", [device.alias for device in self.devices])

    def create_device(self, device_list):
        return Device(device_list['alias'], device_list.get('ip', ''))
```

---

### `main.py`
```python
from tests.connectivity_test import ConnectivityTest

if __name__ == "__main__":
    file_yaml = "sw_tb_v1.0.yaml"
    test = ConnectivityTest(file_yaml)
    test.check_connectivity()
```

---

### Avantages de cette approche
1. **Modularité** : Chaque composant a un rôle bien défini (`Device`, `FileLoader`, `Test`).
2. **Réutilisabilité** : Les classes comme `Device` et `FileLoader` peuvent être utilisées dans d'autres projets.
3. **Lisibilité** : La structure permet de comprendre rapidement le rôle de chaque fichier.
4. **Évolutivité** : Facile à ajouter de nouvelles fonctionnalités ou types de tests.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------



-----------------------------------------------------------------------------------------------------------------------------------------------------------------

Les fichiers `__init__.py` vides ont une utilité spécifique dans Python. Voici leur rôle principal :

### 1. **Déclarer un package Python**  
Un fichier `__init__.py` est utilisé pour indiquer à Python qu'un répertoire doit être traité comme un **package**. Cela permet d'importer des modules ou sous-packages à partir de ce répertoire.

Par exemple :  
Si vous avez la structure suivante :
```
project_root/
├── utils/
│   ├── __init__.py
│   ├── file_loader.py
```

Avec un fichier `__init__.py` dans le répertoire `utils`, vous pouvez écrire :  
```python
from utils.file_loader import load_yaml
```

Sans le fichier `__init__.py`, Python ne considérait pas `utils` comme un package avant Python 3.3.

---

### 2. **Initialisation de package (optionnel)**  
Bien que les fichiers `__init__.py` soient souvent vides, ils peuvent aussi être utilisés pour **initialiser un package** ou **préconfigurer des imports communs**.

Par exemple :  
Si vous voulez que tout le contenu de `file_loader.py` soit accessible directement via `utils`, vous pouvez faire ceci dans `utils/__init__.py` :
```python
from .file_loader import load_yaml
```

Ainsi, vous pouvez importer directement la fonction avec :  
```python
from utils import load_yaml
```

---

### 3. **Compatibilité avec d'anciennes versions de Python**  
Dans les anciennes versions de Python (< 3.3), un répertoire sans `__init__.py` n'était pas reconnu comme un package. Même si ce n'est plus nécessaire à partir de Python 3.3, l'inclusion d'un fichier `__init__.py` reste une bonne pratique pour maintenir la compatibilité avec d'anciens projets.

---

### Quand le laisser vide ?  
- Si vous n'avez pas besoin d'une logique particulière pour initialiser le package.  
- Si le package ne contient que des modules sans configuration spécifique.

### Conclusion  
Les fichiers `__init__.py` servent principalement à structurer votre projet et à organiser les imports. Même vides, ils jouent un rôle essentiel dans la reconnaissance des packages Python et sont une bonne pratique pour garder votre code bien organisé.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------



-----------------------------------------------------------------------------------------------------------------------------------------------------------------

Créer une topologie automatiquement à partir de la liste des appareils (devices) dans un fichier YAML de testbed peut être utile pour structurer les connexions entre ces appareils. Je vais vous fournir un script Python qui lit votre fichier YAML de testbed et génère une topologie avec des connexions basées sur des règles simples (par exemple, chaque appareil est connecté à un ou plusieurs autres appareils).

### Plan du script

1. Lire les appareils à partir du fichier YAML de testbed.
2. Générer des connexions entre les appareils (avec des règles simples, comme des liens en étoile ou des paires).
3. Ajouter la topologie générée dans un fichier YAML de sortie.

Voici le script :

---

### Script : `generate_topology.py`

```python
import yaml

def load_testbed(file_path):
    """
    Charger le fichier YAML de testbed.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_topology(devices):
    """
    Générer une topologie simple basée sur la liste des appareils.
    Les connexions sont définies par des règles simples : chaque appareil est connecté à son voisin suivant.
    """
    topology = {}
    device_names = list(devices.keys())

    for i, device in enumerate(device_names):
        # Connect each device to the next one (circular connection)
        neighbors = []
        if i + 1 < len(device_names):
            neighbors.append(device_names[i + 1])
        if i - 1 >= 0:
            neighbors.append(device_names[i - 1])
        
        topology[device] = {
            "interfaces": [
                {
                    "connected_to": neighbor,
                    "interface": f"eth{i+1}"  # Example interface name
                }
                for neighbor in neighbors
            ]
        }
    return topology

def save_topology(testbed, topology, output_file):
    """
    Ajouter la topologie générée au testbed existant et sauvegarder dans un nouveau fichier.
    """
    testbed["topology"] = topology
    with open(output_file, 'w') as file:
        yaml.dump(testbed, file, default_flow_style=False)
    print(f"Topology saved to {output_file}")

if __name__ == "__main__":
    # Fichier d'entrée et de sortie
    input_yaml = "sw_tb_v1.0.yaml"  # Testbed YAML existant
    output_yaml = "sw_tb_with_topology.yaml"  # Fichier avec la topologie

    # Charger le testbed
    testbed = load_testbed(input_yaml)

    # Vérifier si des appareils existent
    devices = testbed.get("devices", {})
    if not devices:
        print("No devices found in the testbed file.")
    else:
        # Générer la topologie
        topology = generate_topology(devices)

        # Sauvegarder le testbed avec la topologie
        save_topology(testbed, topology, output_yaml)
```

---

### Structure d'entrée (`sw_tb_v1.0.yaml`)

Voici à quoi pourrait ressembler votre fichier de testbed sans la topologie : 

```yaml
devices:
  device1:
    alias: Router1
    ip: 192.168.1.1
  device2:
    alias: Router2
    ip: 192.168.1.2
  device3:
    alias: Switch1
    ip: 192.168.1.3
```

---

### Structure de sortie générée (`sw_tb_with_topology.yaml`)

Le script générera un fichier contenant une topologie comme ci-dessous (connexion en chaîne ou circulaire) :

```yaml
devices:
  device1:
    alias: Router1
    ip: 192.168.1.1
  device2:
    alias: Router2
    ip: 192.168.1.2
  device3:
    alias: Switch1
    ip: 192.168.1.3
topology:
  device1:
    interfaces:
      - connected_to: device2
        interface: eth1
  device2:
    interfaces:
      - connected_to: device3
        interface: eth2
      - connected_to: device1
        interface: eth1
  device3:
    interfaces:
      - connected_to: device2
        interface: eth3
```

---

### Explication des parties importantes

1. **Génération des connexions** : 
   Chaque appareil est connecté à ses voisins (avant et après dans la liste).
   
2. **Interfaces simulées** : 
   Les interfaces (par exemple `eth1`, `eth2`) sont générées dynamiquement en fonction de la position de l'appareil.

3. **Structure de topologie** : 
   La section `topology` dans le fichier YAML respecte une structure claire : chaque appareil a une liste d'interfaces et leurs connexions.

---

### Comment l'exécuter ?

1. Placez le fichier YAML existant (`sw_tb_v1.0.yaml`) dans le même répertoire que le script.
2. Exécutez le script avec Python :
   ```bash
   python3 generate_topology.py
   ```
3. Consultez le fichier généré `sw_tb_with_topology.yaml` pour voir la topologie enrichie.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------



-----------------------------------------------------------------------------------------------------------------------------------------------------------------

Pour construire une topologie réseau basée sur des protocoles comme **LLDP** (Link Layer Discovery Protocol) ou **CDP** (Cisco Discovery Protocol), nous devons utiliser ces protocoles pour découvrir les connexions entre les appareils. Ces protocoles permettent aux appareils d'annoncer leurs informations de voisinage, ce qui est idéal pour créer une carte réseau automatiquement.

### Plan du Script

1. **Exécuter une commande sur chaque appareil** pour collecter les données LLDP/CDP (par exemple : `show lldp neighbors` ou `show cdp neighbors`).
2. **Analyser la sortie des commandes** pour extraire les connexions entre appareils.
3. **Créer la topologie** à partir des données collectées.
4. **Sauvegarder la topologie** dans un fichier YAML.

Voici le script :

---

### Script : `generate_topology_from_protocol.py`

```python
import yaml
import subprocess


def load_testbed(file_path):
    """
    Charger le fichier YAML du testbed.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def fetch_neighbors_via_lldp_or_cdp(device):
    """
    Récupérer les voisins d'un appareil en utilisant LLDP/CDP.
    Cette fonction exécute une commande distante (simulée ici).
    """
    try:
        # Simulation : Remplacez cela par une vraie commande à envoyer à l'appareil
        # Exemples : "show lldp neighbors" ou "show cdp neighbors"
        output = subprocess.check_output(
            f"ssh {device['alias']} 'show lldp neighbors'",
            shell=True,
            text=True,
        )
        return output

    except Exception as e:
        print(f"Erreur lors de la collecte des voisins pour {device['alias']}: {e}")
        return None


def parse_neighbors(output):
    """
    Analyser la sortie LLDP/CDP pour obtenir les voisins.
    """
    neighbors = []

    if output:
        for line in output.splitlines():
            # Supposons que la sortie contient un tableau avec des colonnes Device-ID et Port-ID
            # Ex : "Switch1     Gi1/0/1"
            parts = line.split()
            if len(parts) >= 2:
                neighbors.append({"device": parts[0], "interface": parts[1]})

    return neighbors


def generate_topology(devices):
    """
    Générer une topologie à partir des données LLDP/CDP.
    """
    topology = {}

    for device_name, device in devices.items():
        # Collecter les voisins
        print(f"Collecte des voisins pour {device_name} ({device['alias']})...")
        output = fetch_neighbors_via_lldp_or_cdp(device)

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


def save_topology(testbed, topology, output_file):
    """
    Ajouter la topologie générée au testbed existant et sauvegarder dans un fichier.
    """
    testbed["topology"] = topology
    with open(output_file, 'w') as file:
        yaml.dump(testbed, file, default_flow_style=False)
    print(f"Topology saved to {output_file}")


if __name__ == "__main__":
    # Fichiers d'entrée et de sortie
    input_yaml = "sw_tb_v1.0.yaml"  # Testbed YAML existant
    output_yaml = "sw_tb_with_topology.yaml"  # Fichier avec la topologie

    # Charger le testbed
    testbed = load_testbed(input_yaml)

    # Vérifier si des appareils existent
    devices = testbed.get("devices", {})
    if not devices:
        print("Aucun appareil trouvé dans le fichier testbed.")
    else:
        # Générer la topologie basée sur LLDP/CDP
        topology = generate_topology(devices)

        # Sauvegarder le testbed avec la topologie
        save_topology(testbed, topology, output_yaml)
```

---

### Explications

#### 1. **Collecte des informations LLDP/CDP**  
La fonction `fetch_neighbors_via_lldp_or_cdp` exécute une commande distante (par exemple, via SSH) sur chaque appareil pour collecter les données LLDP ou CDP. La commande réelle dépend de votre appareil :
   - Pour LLDP : `show lldp neighbors`
   - Pour CDP : `show cdp neighbors`

Cela peut être simulé si vous ne pouvez pas exécuter les commandes directement (comme dans un environnement de test).

#### 2. **Analyse des données**  
La sortie des commandes est analysée pour extraire les connexions. Par exemple, la commande `show lldp neighbors` retourne généralement une table où chaque ligne décrit un voisin avec :
   - **Device ID** : Le nom du voisin.
   - **Port ID** : Le port de connexion.

Exemple de sortie simulée :
```
Device ID       Local Intf      Port ID
Switch1         Gi1/0/1         Gi1/0/2
Router1         Gi1/0/2         Gi0/1
```

#### 3. **Construction de la topologie**  
Une fois les voisins identifiés, une topologie est construite en associant chaque appareil à ses voisins via les interfaces.

#### 4. **Sauvegarde de la topologie**  
La topologie générée est ajoutée au testbed YAML sous une clé `topology`.

---

### Exemple de Testbed d'entrée (`sw_tb_v1.0.yaml`)

```yaml
devices:
  Router1:
    alias: router1
    ip: 192.168.1.1
  Switch1:
    alias: switch1
    ip: 192.168.1.2
  Router2:
    alias: router2
    ip: 192.168.1.3
```

---

### Exemple de Testbed avec Topologie (`sw_tb_with_topology.yaml`)

```yaml
devices:
  Router1:
    alias: router1
    ip: 192.168.1.1
  Switch1:
    alias: switch1
    ip: 192.168.1.2
  Router2:
    alias: router2
    ip: 192.168.1.3
topology:
  Router1:
    interfaces:
      - connected_to: Switch1
        interface: Gi1/0/1
  Switch1:
    interfaces:
      - connected_to: Router1
        interface: Gi1/0/2
      - connected_to: Router2
        interface: Gi1/0/3
  Router2:
    interfaces:
      - connected_to: Switch1
        interface: Gi1/0/3
```

---

### Prérequis

1. **Accès SSH** aux appareils pour exécuter les commandes LLDP/CDP.
2. **Protocoles activés** : LLDP ou CDP doit être activé sur tous les appareils.
3. **Simulation possible** : Si vous ne pouvez pas exécuter les commandes directement, vous pouvez fournir des exemples de sortie dans un fichier texte pour simuler les voisins.

---