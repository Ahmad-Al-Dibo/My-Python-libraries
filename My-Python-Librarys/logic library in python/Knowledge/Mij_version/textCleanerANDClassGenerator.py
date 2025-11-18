import re
from typing import Dict, List

class TextCleaner:
    """
    Cleans input text and extracts meaningful structures for class generation.
    """
    def clean_text(self, text: str) -> List[str]:
        """
        Cleans and splits text into meaningful components.

        Args:
            text (str): The raw input text.

        Returns:
            List[str]: A list of cleaned sentences or phrases.
        """
        # Lowercase and remove special characters except basic punctuation
        text = text.lower()
        text = re.sub(r'[^a-z0-9,.\n\s]', '', text)

        # Split text into sentences based on punctuation
        sentences = re.split(r'[.\n]', text)
        
        # Remove extra spaces and empty strings
        return [sentence.strip() for sentence in sentences if sentence.strip()]

class ClassGenerator:
    """
    Generates Python classes based on cleaned and structured text.
    """
    def __init__(self):
        self.classes: Dict[str, List[str]] = {}

    def _sanitize_name(self, name: str) -> str:
        """
        Sanitize a name to create a valid Python identifier.

        Args:
            name (str): The raw name.

        Returns:
            str: A sanitized name.
        """
        # Remove articles like 'a', 'an', 'the'
        name = re.sub(r'\b(a|an|the)\b', '', name).strip()
        # Replace spaces with underscores and ensure it's a valid identifier
        name = re.sub(r'\s+', '_', name)
        return name.capitalize()

    def analyze_text(self, sentences: List[str]):
        """
        Analyze sentences to extract class and attribute relationships.

        Args:
            sentences (List[str]): A list of cleaned sentences.
        """
        for sentence in sentences:
            # Basic pattern to find "class-like" structures: "X is a Y" or "X has Y"
            if "is a" in sentence:
                parts = sentence.split("is a")
                class_name = self._sanitize_name(parts[0].strip())
                parent_class = self._sanitize_name(parts[1].strip())

                # Create class and parent relationship
                self.classes[class_name] = self.classes.get(class_name, [])
                self.classes[class_name].append(f"Parent: {parent_class}")

            elif "has" in sentence:
                parts = sentence.split("has")
                class_name = self._sanitize_name(parts[0].strip())
                attributes = [self._sanitize_name(attr.strip()) for attr in re.split(r',|and', parts[1])]

                # Add attributes to the class
                self.classes[class_name] = self.classes.get(class_name, []) + attributes

    def generate_code(self) -> str:
        """
        Generate Python class definitions based on analyzed text.

        Returns:
            str: The generated Python code.
        """
        code = []

        for class_name, details in self.classes.items():
            code.append(f"class {class_name}:")
            code.append("    def __init__(self):")

            parents = [d.split(': ')[1] for d in details if d.startswith("Parent")]
            if parents:
                parent_str = ', '.join(parents)
                code[-2] = f"class {class_name}({parent_str}):"

            attributes = [d for d in details if not d.startswith("Parent")]
            if attributes:
                for attr in attributes:
                    code.append(f"        self.{attr} = None")
            else:
                code.append("        pass")

            code.append("")

        return "\n".join(code)

# Example Usage
if __name__ == "__main__":
    input_text = """
    A car is a vehicle. A car has wheels, an engine, and seats.
    A bike is a vehicle. A bike has wheels and a frame.
    """

    cleaner = TextCleaner()
    generator = ClassGenerator()

    cleaned_text = cleaner.clean_text(input_text)
    generator.analyze_text(cleaned_text)

    generated_code = generator.generate_code()
    print(generated_code)