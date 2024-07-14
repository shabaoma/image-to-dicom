import os


def get_all_files_in_dir(input_dir: str,
                         include_extensions: list = None,
                         exclude_extensions: list = ['.DS_Store', '.gitkeep']) -> list[list[str], list[str]]:
    all_paths = []
    all_dirs = set()
    for root, _, files in os.walk(input_dir):
        for file in files:
            if exclude_extensions:
                if any(file.endswith(ext) for ext in exclude_extensions):
                    continue

            if include_extensions:
                if any(file.endswith(ext) for ext in include_extensions):
                    all_dirs.add(root)
                    file_path = os.path.join(root, file)
                    all_paths.append(file_path)
            else:
                all_dirs.add(root)
                file_path = os.path.join(root, file)
                all_paths.append(file_path)

    return [all_paths, list(all_dirs)]


def convert_to_output_path(input_dirs: list[str], input_root: str, output_root: str) -> list[str]:
    output_dirs = []
    for dir in input_dirs:
        output_dir = dir.replace(input_root, output_root)
        output_dirs.append(output_dir)
    return output_dirs


def create_output_dirs(dirs: list):
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
