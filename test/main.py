import unittest  # 1. Importa o módulo unittest

def add(a, b):    # 2. Função que queremos testar
    return a + b

class TestAddFunction(unittest.TestCase):  # 3. Cria uma classe de testes
    def test_addition(self):               # 4. Um método de teste (tem que começar com "test_")
        self.assertEqual(add(2, 3), 5)     # 5. Compara o resultado da função com o valor esperado

if __name__ == '__main__':                # 6. Garante que os testes só rodem se o arquivo for executado
    unittest.main()
