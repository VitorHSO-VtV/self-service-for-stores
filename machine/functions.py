from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def txt_to_py(file_path):
    array = []
    try:
        with open(file_path, 'r') as arquivo:
            text = arquivo.readlines()
        for linha in text:
            array.append(linha.strip())
        return array
    except FileNotFoundError:
        print(f'Erro: O arquivo {file_path} não foi encontrado.')
        return []


def file_append(file_path, text):
    try:
        with open(file_path, 'a') as arquivo:
            arquivo.write(str(text) + '\n')
        print(f'Linha adicionada com sucesso em {file_path}')
        print_file_content(file_path)
    except Exception as e:
        print(f'Erro ao adicionar linha em {file_path}: {e}')


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
        print(f'Erro: O arquivo {file_path} não foi encontrado.')
    except Exception as e:
        print(f'Erro ao remover a linha: {e}')


def print_file_content(file_path):
    try:
        with open(file_path, 'r') as arquivo:
            conteudo = arquivo.read()
        print(f'Conteúdo do arquivo {file_path}:\n{conteudo}')
    except Exception as e:
        print(f'Erro ao ler conteúdo de {file_path}: {e}')


def generate_to_pdf(layout, output_file_path):
    pdf_canvas = canvas.Canvas(f'{output_file_path}.pdf')
    width, height = layout.size
    layout.export_to_png(f'{output_file_path}.png')
    pdf_canvas.drawInlineImage(f'{output_file_path}.png', 0, 0, width, height)
    pdf_canvas.save()


def text_to_pdf(input_file, output_file, width=400, font_size=21):
    with open(input_file, 'r', encoding='utf-8') as text_file:
        lines = text_file.readlines()

    height = len(lines) * font_size * 1.2

    pdf = canvas.Canvas(output_file, pagesize=(width, height))

    y_pos = height - font_size
    for line in lines:
        pdf.setFont("Helvetica", font_size)
        pdf.drawString(10, y_pos, line.strip())
        y_pos -= font_size * 1.2

    pdf.save()


def replace_line(file_path, target_line, new_content):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    found = False
    for i, line in enumerate(lines):
        if target_line in line:
            lines[i] = new_content
            found = True
            break

    if found:
        with open(file_path, 'w') as file:
            file.writelines(lines)
        print(f'A linha contendo {target_line} foi substituída por {new_content} em {file_path}.')
    else:
        print(f'A linha contendo {target_line} não foi encontrada em {file_path}.')


def clear_file(file_path):
    try:
        with open(file_path, 'w') as arquivo:
            pass
        print(f'Arquivo {file_path} apagado com sucesso.')
    except Exception as e:
        print(f'Erro ao apagar o arquivo: {e}')