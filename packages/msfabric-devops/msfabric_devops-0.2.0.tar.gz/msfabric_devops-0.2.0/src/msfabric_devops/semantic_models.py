import os
import json
import re
from . import config

def set_semantic_model_parameters(path, parameters, fail_if_not_found=False):
    model_path = os.path.join(path, "definition")

    is_tmsl = False

    if not os.path.exists(model_path):
        model_path = os.path.join(path, "model.bim")
        is_tmsl = True

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Cannot find semantic model definition: '{model_path}'")

    changed = False

    # ----- Load model -----
    # tmdl
    if not(is_tmsl):
        file_path = os.path.join(model_path, "expressions.tmdl")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"expressions.tmdl not found at: {file_path}")

        # Read file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original = content
        missing_keys = []

        # Apply replacements
        for key, value in parameters.items():
            pattern = rf"{re.escape(key)}\s*=\s*\".*?\""
            # Check if key exists
            if not re.search(pattern, content):
                missing_keys.append(key)
                continue  # skip replacement

            # Replace
            replacement = f'{key} = "{value}"'
            content = re.sub(pattern, replacement, content)

        # Raise error if any key is missing
        if missing_keys and fail_if_not_found:
            raise ValueError(f"The following parameters were not found in the file: {missing_keys}")
        elif missing_keys:
            config.print_color("Parameter(s) not found: " + ", ".join(missing_keys), "yellow")

        # Save only if modified
        if content != original:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            config.print_color("expressions.tmdl updated ✅", "green")
        else:
            config.print_color("No changes needed", "yellow")
        return

    # model.bim
    else:
        with open(model_path, "r", encoding="utf-8") as f:
            model_text = f.read()
        model = json.loads(model_text)

        # ----- Update expression parameters -----
        expressions = model.get("model", {}).get("expressions", [])

        for name, value in parameters.items():
            match = next((expr for expr in expressions if expr.get("name") == name), None)

            if not match:
                if fail_if_not_found:
                    raise ValueError(f"Cannot find parameter with name '{name}'")
                else:
                    config.print_color(f"Cannot find parameter with name '{name}'","yellow")
                    continue

            expr_text = match.get("expression")

            # Equivalent of: -replace """?(.*)""? meta", """$parameterValue"" meta"
            expr_text = re.sub(r'\"?.*\"?\s+meta', f'"{value}" meta', expr_text)

            match["expression"] = expr_text
            changed = True

        # ----- Save if changed -----
        if changed:
            with open(model_path, "w", encoding="utf-8") as f:
                json.dump(model, f, indent=2)
        else:
            config.print_color("No changes applied","yellow")

def main():
    set_semantic_model_parameters(
        "../output",
        {
            "Param_Brand": "X",
            "Param_Billing": "dev",
            "Param_Source": "prod"
        },
        fail_if_not_found=False
    )
    config.print_color("Parameters changed successfully.","green")


if __name__ == "__main__":
    main()
