---

### Objectif général :
Ce script semble être destiné à tester la connectivité réseau d'une liste de périphériques décrits dans un fichier **YAML**. Il utilise **pyATS** pour la gestion des tests et **subprocess** pour effectuer un test de ping réel vers ces périphériques.


### Imports :

```python
from pyats.aetest import Testcase, test
import subprocess
import sys
import yaml
```

- **pyATS (Testcase, test)** : Permet de créer et d'exécuter des tests automatisés. `Testcase` est la classe de base pour un test, et `test` est un décorateur qui marque une méthode comme un test.
  
- **subprocess** : Utilisé pour exécuter des commandes systèmes, ici pour effectuer un **ping** vers un périphérique en utilisant la commande `ping` de ton système d'exploitation.
  
- **sys** : Permet d'interagir avec le système d'exploitation, ici pour vérifier la plateforme afin de choisir le bon argument pour `ping` (`-n` pour Windows et `-c` pour Unix/Linux).
  
- **yaml** : Permet de charger des données à partir d'un fichier **YAML** qui décrit ton réseau et les périphériques à tester.

---

### Classe **ConnectivityTest** :

```python
class ConnectivityTest(Testcase):
    def __init__(self, file_yaml):
        with open(file_yaml, 'r') as file:
            self.data = yaml.safe_load(file)
        self.devices = []
```

- **`ConnectivityTest`** hérite de `Testcase` (de pyATS), donc c'est un test dans pyATS.
  
- **`__init__`** : Le constructeur charge les données depuis un fichier YAML (indiqué par `file_yaml`). Ces données sont stockées dans **`self.data`** sous forme de dictionnaire Python après conversion du fichier YAML.

---

### Méthode **check_connectivity** :

```python
@test
def check_connectivity(self):
    devices = self.data.get('devices', {})
    print("Testbed devices is :", devices)
```

- Le décorateur **`@test`** indique que la méthode **`check_connectivity`** est un test dans pyATS.
  
- Cette méthode commence par récupérer la liste des périphériques depuis les données chargées dans `self.data` à partir du fichier YAML. Elle affiche ensuite cette liste de périphériques.

---

### Boucle pour vérifier la connectivité de chaque périphérique :

```python
for device_name, device_list in devices.items():
    try:
        device = self.create_device(device_list) 
        print(f"Checking connectivity for device: {device_name} ({device.alias})")
        connected = device.ping(device_list.get('alias', ''))
        assert connected, f"Connection failed for device {device_name}"
        
        self.devices.append(device)
        print("Device list members are :", {device_name})
    except Exception as e:
        self.failed(f"Test failed for device {device_name} due to: {str(e)}")
        print(f"Error for {device_name}: {str(e)}")
```

- **Boucle `for`** : Chaque périphérique dans le fichier YAML est récupéré. Pour chaque périphérique, il tente de :
    - Créer une instance de périphérique avec **`self.create_device()`**.
    - Vérifier la connectivité avec la méthode **`ping()`**.
    - Si le périphérique répond au ping, il est ajouté à une liste **`self.devices`**.
    - Si le périphérique ne répond pas, une exception est levée et le test échoue pour ce périphérique.

---

### Affichage des résultats :

```python
print("Successfully connected devices:", [device.alias for device in self.devices])
```

- Après avoir vérifié la connectivité pour tous les périphériques, il affiche la liste des périphériques pour lesquels la connectivité a réussi.

---

### Méthode **create_device** :

```python
def create_device(self, device_list):
    class Device:
        def __init__(self, alias, ip):
            self.alias = alias
            self.ip = ip

        def ping(self, ip_address):
            print(f"Performing real ping to {ip_address}...")
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
    return Device(device_list['alias'], device_list.get('alias', ''))
```

- **`create_device()`** : Cette méthode crée une instance de la classe `Device` (une classe interne définie à l'intérieur de `create_device`). Elle prend les informations du périphérique et crée un objet `Device` avec un alias et une adresse IP.
  
- **`ping()`** : La méthode `ping` utilise la bibliothèque **`subprocess`** pour envoyer un véritable ping vers une adresse IP.
    - Selon le système d'exploitation (Windows ou Unix), elle adapte l'argument de la commande `ping` (`-n` pour Windows et `-c` pour Unix).
    - Elle exécute la commande `ping` en utilisant **`subprocess.run()`**.
    - Si le ping réussit (code de retour `0`), elle retourne `True`, sinon `False`.
    - Si une erreur se produit, elle affiche l'erreur et retourne `False`.

---

### Exemple d'appel de la méthode :

```python
file_yaml = "sw_tb_v1.0.yaml"
device_list = ConnectivityTest(file_yaml)
device_list.check_connectivity()
```

- Ce code initialise un objet de test **`ConnectivityTest`** avec un fichier YAML (qui contient la configuration du réseau) et appelle **`check_connectivity()`** pour vérifier la connectivité de chaque périphérique défini dans ce fichier.

---

### Résumé de l'ensemble du code :
1. **Chargement du fichier YAML** : Le fichier YAML spécifie une liste de périphériques à tester.
2. **Création d'instances de périphériques** : Pour chaque périphérique, une instance de la classe `Device` est créée.
3. **Ping** : Un vrai test de ping est effectué à l'aide de `subprocess` pour chaque périphérique vers l'adresse IP donnée.
4. **Gestion des erreurs** : Si un périphérique échoue au test de ping ou si une erreur se produit, un message d'erreur est affiché.
5. **Affichage des résultats** : Les périphériques pour lesquels la connectivité a réussi sont affichés à la fin.

Ce script est conçu pour tester la connectivité réseau des périphériques de manière automatisée, tout en offrant un bon mécanisme de gestion des erreurs.

### Conclusion :
Le code réalise un test de connectivité via un vrai test de ping pour chaque périphérique défini dans le fichier YAML. Si un périphérique répond au ping, il est ajouté à une liste des périphériques "connectés". Sinon, un message d'erreur est affiché et le test pour ce périphérique échoue.

---