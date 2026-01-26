---

### Fichier `README.md`

```markdown
# Generate Topology from LLDP/CDP

Ce projet permet de générer automatiquement une topologie réseau basée sur les protocoles LLDP (Link Layer Discovery Protocol) ou CDP (Cisco Discovery Protocol). Le script collecte des informations de voisinage à partir d'appareils réseau définis dans un fichier **pyATS Testbed YAML**, puis génère une topologie et l'ajoute au fichier Testbed.

## Structure du Projet

```
generate_topology/
├── __init__.py
├── main.py                # Script principal
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

## Fonctionnalités

1. **Chargement du Testbed YAML** :
   - Lecture des appareils définis dans un fichier Testbed YAML.
2. **Collecte des voisins via LLDP/CDP** :
   - Utilisation de commandes telles que `show lldp neighbors` ou `show cdp neighbors` pour découvrir les connexions réseau.
3. **Analyse des données LLDP/CDP** :
   - Extraction des relations entre appareils et interfaces.
4. **Construction de la topologie** :
   - Génération d'une structure définissant les connexions entre les appareils.
5. **Sauvegarde de la topologie** :
   - Ajout de la topologie générée au fichier Testbed YAML.

---

## Prérequis

1. Python 3.8 ou plus récent.
2. Accès SSH configuré pour les appareils réseau.
3. Protocoles **LLDP** ou **CDP** activés sur tous les appareils.

---

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-repo/generate_topology.git
   cd generate_topology
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

---

## Utilisation

1. Placez votre fichier Testbed YAML (exemple : `sw_tb_v1.0.yaml`) dans le répertoire du projet.

2. Lancez le script principal :
   ```bash
   python main.py
   ```

3. Une fois terminé, le script génère un fichier de sortie (par défaut : `sw_tb_with_topology.yaml`) contenant la topologie réseau.

---

## Exemple de Testbed YAML

### Entrée : `sw_tb_v1.0.yaml`

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

### Sortie : `sw_tb_with_topology.yaml`

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

## Tests Unitaires

Le projet inclut des tests unitaires pour garantir la fiabilité du code.

1. Lancer tous les tests :
   ```bash
   pytest tests/
   ```

2. Exemple de test pour le module `parser` :
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

## Contributions

Les contributions sont les bienvenues ! Veuillez ouvrir une pull request ou soumettre un ticket pour signaler des bugs ou demander de nouvelles fonctionnalités.

---

## Auteurs

- **Jeremie Rouzet** - Créateur principal du projet.

---

## Licence

Ce projet est sous licence **MIT**. Consultez le fichier `LICENSE` pour plus d'informations.
```

---

### Fichier `requirements.txt`

```plaintext
# Modules nécessaires pour le projet
PyYAML==6.0          # Pour gérer les fichiers YAML
pytest==7.4.0        # Pour les tests unitaires
paramiko==3.2.0      # Pour exécuter les commandes SSH
```

---

### Instructions pour compléter

1. **Ajoutez votre dépôt GitHub** dans le champ `git clone` du fichier `README.md` si applicable.
2. **Ajoutez d'autres dépendances** dans `requirements.txt` si vous utilisez des modules supplémentaires, comme un framework spécifique.
3. **Vérifiez que `paramiko` est bien fonctionnel** pour gérer les connexions SSH.