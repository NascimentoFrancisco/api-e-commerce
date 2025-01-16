# E-commerce API

Projeto de uma API genérica, pois pode ser necessário incluir ou excluir funcionalidades e atributos, de um e-commerce.

# Configurações 

Para utilizar este projeto na versão com Firebase Storage, é necessário realizar algumas configurações prévias.

> Antes de qualquer coisa realize o clone do projeto e navegue para dentro do diretório do mesmo:
~~~ bash
git clone https://github.com/NascimentoFrancisco/api-e-commerce.git

cd api-e-commerce
~~~
> Crie um viryualenv e a ative:
~~~ bash
python3 -m venv .env
source .env/bin/activate
~~~

> Instale as dependências
~~~ bash
pip install -r requirements.txt
~~~

## Configuração de variáveis de ambiente

Para que o projeto funcione normalmente é necessário por informações sensíves em uma variável de ambiente. Copie a estrutura do arquivo `EXAMPLE_ENV` para um arquivo `.env` e insira as informações necessárias no mesmo.

Para que o Firebase Storage possa funcionar você precisa fazer as configurações de app e de autenticação na plataforma, no link abaixo você tem as informações de como fazer isso.

Documentação do firebase storage: https://firebase.google.com/docs/storage?hl=pt-br

Após configurar o aplicativo no Firebase e obter o arquivo `serviceAccountKey.json`, extraia as informações de autenticação e insira-as no arquivo `.env`, associando-as às chaves correspondentes.

## Configuraçoes finais

> Criar as tabelas no banco de dados, fazer os testes unitários para verificar se está tudo funcionando bem.
~~~ bash
python manage.py migrate

python manage.py test
~~~

> Executar testes de integração com Firebase Storage:
Para isso você deve ir em `api/services/firebase/tests/test_storage.py` e fazer as seguintes mudanças:
~~~ Python
""" Código omisso """

# Comente o decorador abaixo, antes de executar o teste
#@unittest.skip("Skip integration tests during standard tests")
class TestHandleFirebaseStorage(TestCase):
    def setUp(self):
        self.storage_handler = HandleFirebaseStorage()
        self.test_file = BytesIO(b"test data for integration")
        self.updated_file = BytesIO(b"updated image content")
        self.test_image_name = "test_image_integration"
        self.test_content_type = "image/jpeg"

""" Resto do código """
~~~

Por fim execute o teste:
~~~ bash
python manage.py test api.services.firebase.tests
~~~

Após o teste, se estiver tudo certo, recomendo você amanter o teste com o decorador `unittest.skip` para evitar de fazer requisições desnecessárias ao esxutar testes.

> Criar super usuário e executar a aplicação:
~~~ bash
python manage.py createsuperuser
python manage.py runserver
~~~

> Acessar a aplicação

Para acessar a aplicação como administrador no admin do Django abra a url `http://127.0.0.1:8000/admin` no navegador e faça o login com o super usuári que você criou anteriormente.

Para ver a forma de como usar a API, acesse a documentação da mesma nessa url: `http://127.0.0.1:8000`.

# Tecnologias usadas
> Framework Django com algumas bibliotecas amais:

* djangorestFramework https://www.django-rest-framework.org/
* Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/
* drf_yasg: https://drf-yasg.readthedocs.io/en/stable/
* corsheaders: https://pypi.org/project/django-cors-headers/
* firebase_admin: https://pypi.org/project/firebase-admin/

As demais ferraments de ambiente de desenvolvimento são destinadas a semântica e guias de estilo da aplicação seguindo a PEP8. Assim como lidar com o `pre_commit` para averiguar e ajustar as versões do código antes de fazer os commits.

Para entender usar e configurar o `pre_commit`acess essa url `https://pre-commit.com/`.

> Obrigado por ler até aqui, aproveite o projeto. 🤓