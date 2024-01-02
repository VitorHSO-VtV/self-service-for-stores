def txt_to_py(file_path):
    array = []
    try:
        with open(file_path, 'r') as arquivo:
            text = arquivo.readlines()
        for linha in text:
            array.append(linha.strip())
        return array
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return []


def clear_file(file_path):
    with open(file_path, 'w') as arquivo:
        arquivo.write('')


def file_append(file_path, text):
    try:
        with open(file_path, 'a') as arquivo:
            arquivo.write(str(text) + '\n')
        print(f"Linha adicionada com sucesso em {file_path}")
        print_file_content(file_path)
    except Exception as e:
        print(f"Erro ao adicionar linha em {file_path}: {e}")


def remove_line_from_file(file_path, line_to_remove):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        if line_to_remove in lines:
            lines.remove(line_to_remove)
            with open(file_path, 'w') as file:
                file.writelines(lines)
            print(f'Linha removida do arquivo {file_path}:\n{line_to_remove}')
            print_file_content(file_path)
        else:
            print(f'Linha não encontrada no arquivo {file_path}:\n{line_to_remove}')

    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
    except Exception as e:
        print(f'Erro ao remover a linha: {e}')


def print_file_content(file_path):
    try:
        with open(file_path, 'r') as arquivo:
            conteudo = arquivo.read()
        print(f"Conteúdo do arquivo {file_path}:\n{conteudo}")
    except Exception as e:
        print(f"Erro ao ler conteúdo de {file_path}: {e}")
