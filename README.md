
# Guide complet : JeyPyats (pyats-jeyws01)

Ce dossier regroupe un environnement de test automatisé basé sur pyATS pour l’audit et la validation d’équipements réseau via NETCONF. Il est conçu pour faciliter le développement, l’exécution et l’extension de jobs de test personnalisés.

## Version
1.0.0 - Dernière mise à jour : 26 janvier 2026

## Objectif
Automatiser la collecte et l’analyse d’informations réseau (statut des interfaces, configuration, etc.) sur des équipements compatibles NETCONF, en utilisant des parsers spécialisés et des utilitaires avancés.

## Prérequis
- Python 3.8 ou supérieur
- Accès au dépôt de code
- Connexion réseau vers les équipements à tester
- Accès internet pour installer les dépendances

## Structure détaillée du dossier
- **bin/** : exécutables Python de l'environnement virtuel
- **include/** : fichiers d'en-tête pour les paquets Python
- **lib/** : bibliothèques Python installées
- **parsers/** : scripts de parsing des résultats ou logs :
	- `xrd_interface_parser.py` :
		- Fonction principale : `get_interface_status(self)`
		- Récupère le statut des interfaces via NETCONF (OpenConfig), construit et envoie la requête, parse la réponse XML et retourne le statut des interfaces.
		- Exemple d’utilisation :
			```python
			status = obj.get_interface_status()
			print(status)
			```
		- Dépendances : xmltodict, lxml, genie.utils.Dq
	- `xrd_interface_parser_oc.py` :
		- Fonction principale : `get_interface_status_oc(self)`
		- Variante parser pour OpenConfig, loggue et parse la réponse NETCONF, retourne le statut des interfaces réseau.
		- Ajoute des logs détaillés et utilise pprint pour l’affichage des résultats.
	- `xrd_interface_parser_xr.py` :
		- Fonction principale : `get_interface_status_xr(self)`
		- Parser pour Cisco XR, construit la requête NETCONF spécifique, parse la réponse et extrait le nom et l'état des interfaces XR.
		- Permet d’auditer des équipements Cisco IOS XR.
- **pyvenv.cfg** : configuration de l'environnement virtuel
- **scripts/** : scripts d'automatisation ou de test (à personnaliser selon vos besoins)
- **utils/** : utilitaires pour les jobs/tests :
	- `netconf_connector.py` :
		- Fonction : `connect_netconf(host, port, username, password, device_params=None)`
		- Établit une connexion NETCONF avec un équipement réseau via ncclient.
		- Gère les erreurs de connexion et retourne l’objet manager ou None.
	- `rpc_msgs.py` :
		- Définit des messages XML NETCONF standards (`RPC_OK_MSG`, `RPC_EMPTY_MSG`, `BASE_RPC`) utilisés pour les échanges RPC.
		- Permet de générer des requêtes et de valider les réponses attendues.
	- `utils.py` :
		- Fonctions utilitaires avancées :
			- Application dynamique de mixins (ajout de méthodes à des objets selon leur type et version)
			- Manipulation XML (insertion, nettoyage, intersection de dictionnaires)
			- Gestion de versions et logs
		- Exemple :
			```python
			from utils import sanitize_xml
			xml_clean = sanitize_xml(xml_string)
			```
- **README.md** : ce guide détaillé

## Configuration et utilisation

### 1. Cloner le dépôt
```bash
git clone <url-du-depot>
```

### 2. Accéder au dossier
```bash
cd pyats-jeyws01
```

### 3. Créer un environnement virtuel
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Installer les dépendances
```bash
pip install -r ../requirements.txt
```

### 5. Configurer le testbed
- Placez votre fichier de testbed dans le dossier `testbed/`.
- Modifiez le fichier selon votre environnement réseau (voir [documentation pyATS](https://developer.cisco.com/docs/pyats/)).

### 6. Lancer un test exemple
```bash
pyats run job <nom_du_job>.py --testbed-file testbed/<votre_testbed>.yaml
```

## Personnalisation et extension
- Ajoutez vos propres scripts dans `scripts/` pour automatiser des séquences de test spécifiques.
- Modifiez ou enrichissez les parsers pour supporter de nouveaux modèles d’équipements ou de nouveaux types de données.
- Utilisez les utilitaires pour manipuler les données XML, gérer les logs ou appliquer des mixins selon vos besoins.

## Dépannage
- Vérifiez la version de Python et l’activation de l’environnement virtuel.
- Consultez les logs générés par les parsers pour diagnostiquer les erreurs de connexion ou de parsing.
- Utilisez les messages d’erreur détaillés des scripts utils pour identifier les problèmes de configuration ou de dépendances.

## Ressources complémentaires
- [Documentation officielle pyATS](https://developer.cisco.com/docs/pyats/)
- [ncclient (NETCONF Python client)](https://ncclient.readthedocs.io/en/latest/)
- [lxml (traitement XML)](https://lxml.de/)

---
Pour toute question ou demande d’assistance, contactez le responsable technique ou consultez la documentation officielle.
