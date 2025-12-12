import re
import tomli
from pathlib import Path
from typing import Optional, Dict, Any


class TOMLValidator:
    """Validateur TOML avec messages d'erreur détaillés et localisés."""

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.content = ""
        self.lines = []

    def validate(self) -> tuple[bool, Optional[str], Optional[Dict[Any, Any]]]:
        """
        Valide un fichier TOML.

        Returns:
            tuple: (succès: bool, message_erreur: str|None, données: dict|None)
        """
        # Vérifier l'existence du fichier
        if not self.filepath.exists():
            return False, f"❌ Fichier introuvable : {self.filepath}", None

        # Lire le contenu
        try:
            self.content = self.filepath.read_text(encoding='utf-8')
            self.lines = self.content.splitlines()
        except UnicodeDecodeError as e:
            return False, f"❌ Erreur d'encodage : {e}", None
        except Exception as e:
            return False, f"❌ Impossible de lire le fichier : {e}", None

        # Vérifier les doublons de clés avant le parsing
        duplicate_check = self._check_duplicate_keys()
        if duplicate_check:
            return False, duplicate_check, None

        # Parser avec tomli
        try:
            with open(self.filepath, 'rb') as f:
                data = tomli.load(f)
            return True, "✅ Fichier TOML valide", data

        except tomli.TOMLDecodeError as e:
            error_msg = self._format_toml_error(e)
            return False, error_msg, None

        except Exception as e:
            return False, f"❌ Erreur inattendue : {e}", None

    def _check_duplicate_keys(self) -> Optional[str]:
        """Détecte les clés dupliquées dans chaque section."""
        current_section = "root"
        section_keys: Dict[str, set] = {"root": set()}
        section_line_numbers: Dict[str, Dict[str, int]] = {"root": {}}
        table_array_depth = 0  # Track depth of table arrays

        for line_num, line in enumerate(self.lines, 1):
            stripped = line.strip()

            # Ignorer commentaires et lignes vides
            if not stripped or stripped.startswith('#'):
                continue

            # Détecter nouvelle section
            if stripped.startswith('['):
                # Reset section tracking for array of tables
                if stripped.startswith('[[') and stripped.endswith(']]'):
                    # This is an array of tables, create a new context
                    table_array_depth += 1
                    current_section = f"{stripped[2:-2]}_{table_array_depth}"
                else:
                    # Regular section
                    current_section = stripped[1:-1]

                if current_section not in section_keys:
                    section_keys[current_section] = set()
                    section_line_numbers[current_section] = {}
                continue

            # Détecter clé = valeur
            if '=' in stripped:
                key = stripped.split('=')[0].strip()

                if key in section_keys[current_section]:
                    first_occurrence = section_line_numbers[current_section][key]
                    context = self._get_context(line_num, first_occurrence)

                    return (
                        f"❌ CLÉS DUPLIQUÉES\n\n"
                        f"Section : [{current_section}]\n"
                        f"Clé dupliquée : '{key}'\n\n"
                        f"Première occurrence : ligne {first_occurrence}\n"
                        f"Duplication trouvée : ligne {line_num}\n\n"
                        f"{context}\n\n"
                        f"💡 Solution : TODO Supprimez l'une des deux déclarations de '{key}'"
                    )

                section_keys[current_section].add(key)
                section_line_numbers[current_section][key] = line_num

        return None

    def _format_toml_error(self, error: tomli.TOMLDecodeError) -> str:
        """Formate une erreur tomli de manière lisible."""
        error_str = str(error)

        # Extraire numéro de ligne et colonne
        line_match = re.search(r'line (\d+)', error_str)
        col_match = re.search(r'column (\d+)', error_str)

        line_num = int(line_match.group(1)) if line_match else None
        col_num = int(col_match.group(1)) if col_match else None

        # Message principal
        if "Cannot overwrite a value" in error_str:
            msg_type = "CLÉS DUPLIQUÉES"
            explanation = "Une même clé a été définie plusieurs fois dans la même section."
        elif "Invalid" in error_str:
            msg_type = "SYNTAXE INVALIDE"
            explanation = "Le format TOML n'est pas respecté."
        elif "Expected" in error_str:
            msg_type = "VALEUR ATTENDUE"
            explanation = "Une valeur est manquante ou mal formatée."
        else:
            msg_type = "ERREUR DE PARSING"
            explanation = error_str

        # Contexte
        context = ""
        if line_num:
            context = self._get_context(line_num)

        return (
            f"❌ {msg_type}\n\n"
            f"{explanation}\n\n"
            f"Position : ligne {line_num}, colonne {col_num}\n\n"
            f"{context}\n\n"
            f"Erreur brute : {error_str}"
        )

    def _get_context(self, line_num: int, compare_line: Optional[int] = None) -> str:
        """Affiche le contexte autour d'une ligne avec numéros."""
        context_range = 3
        start = max(0, line_num - context_range - 1)
        end = min(len(self.lines), line_num + context_range)

        context_lines = []
        for i in range(start, end):
            line_number = i + 1
            line_content = self.lines[i]

            if line_number == line_num:
                marker = ">>> "
            elif compare_line and line_number == compare_line:
                marker = "!!! "
            else:
                marker = "    "

            context_lines.append(f"{marker}{line_number:4d} | {line_content}")

        return "\n".join(context_lines)


# Fonction utilitaire
def validate_toml_file(filepath: str) -> tuple[bool, str, Optional[Dict]]:
    """
    Valide un fichier TOML et retourne un résultat détaillé.

    Args:
        filepath: Chemin vers le fichier TOML

    Returns:
        tuple: (succès, message, données)
    """
    validator = TOMLValidator(filepath)
    return validator.validate()


# Exemple d'utilisation
if __name__ == "__main__":
    # Test avec votre fichier
    success, message, data = validate_toml_file("rooms.toml")

    print(message)
    print("\n" + "=" * 60 + "\n")

    if success:
        print("Données chargées avec succès :")
        print(f"Nombre de rooms : {len(data.get('rooms', []))}")
    else:
        # TODO Introduire la localisation
        print("Le fichier contient des erreurs et doit être corrigé.")
