# Organizador de Arquivos

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-v8.6-green.svg)](https://wiki.python.org/moin/TkInter)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Este é um aplicativo simples de organização de arquivos que utiliza Python, com a interface gráfica construída usando a biblioteca `tkinter`. O objetivo do programa é ajudar a organizar arquivos dentro de uma pasta selecionada, movendo-os para subpastas de acordo com suas extensões.

## Funcionalidade

1. **Seleção de Pasta**: O aplicativo solicita ao usuário que selecione uma pasta de destino onde os arquivos a serem organizados estão localizados.
2. **Organização por Extensão**: Para cada arquivo na pasta selecionada, o aplicativo verifica sua extensão e cria uma subpasta com o nome da extensão (por exemplo, arquivos `.jpg` serão movidos para uma pasta chamada `jpg`).
3. **Movimento dos Arquivos**: Após a criação das pastas para cada tipo de arquivo, o programa move os arquivos para as respectivas pastas.
4. **Notificação de Conclusão**: Ao final, o aplicativo exibe uma mensagem informando que os arquivos foram organizados com sucesso.

## Como Funciona

- O programa usa a biblioteca `tkinter` para criar uma interface gráfica simples com um botão que permite ao usuário selecionar a pasta onde os arquivos estão localizados.
- Em seguida, o script percorre todos os arquivos da pasta e os move para subpastas baseadas nas suas extensões. Caso a pasta de uma extensão não exista, ela será criada automaticamente.
- A interface gráfica exibe uma mensagem após a execução do processo, informando que os arquivos foram organizados com sucesso.

## Como Rodar o Código

Para rodar o programa, siga os seguintes passos:

1. **Instalar as dependências**: Certifique-se de ter o Python instalado em seu computador. O `tkinter` já vem instalado com o Python, mas caso tenha problemas, instale-o utilizando o comando:
    ```bash
    pip install tk
    ```

2. **Executar o Script**: Abra o terminal ou o prompt de comando e execute o arquivo Python com o seguinte comando:
    ```bash
    python nome_do_arquivo.py
    ```

3. **Usar o Programa**: Uma janela será aberta com um botão "Selecionar Pasta e Organizar". Clique no botão, escolha a pasta que deseja organizar e o programa fará o trabalho automaticamente!

## Automação

Esse programa automatiza o processo de organização de arquivos, evitando a necessidade de organizar manualmente cada tipo de arquivo em suas pastas. Isso é particularmente útil quando você tem uma grande quantidade de arquivos desorganizados e deseja organizá-los de forma eficiente e rápida.

## Objetivo

O objetivo principal desse projeto é facilitar a organização de arquivos no sistema de maneira simples e intuitiva, economizando tempo e esforço.

---

Se você tiver alguma dúvida ou sugestão de melhoria, sinta-se à vontade para contribuir!

## License

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).
