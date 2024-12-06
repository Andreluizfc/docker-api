#### **1. Introdução ao Docker**  
- **O que é o Docker?**  
  - Conceito de containers versus máquinas virtuais.  
  - Benefícios do Docker no desenvolvimento e produção.  

- **Instalação e Configuração Básica:**  
  - Instalação do Docker no sistema operacional.  
  - Configuração inicial e verificação com `docker --version`.  

- **Terminologia Essencial:**  
  - Imagens, containers, volumes e redes.  

- **Primeiros Comandos:**  
  - `docker run`, `docker ps`, `docker stop`, `docker rm`.  
  - Executando a imagem do *hello-world*.  

---

#### **2. Trabalhando com Imagens Docker**  
- **Dockerfile: A Base de uma Imagem**  
  - Estrutura básica do Dockerfile.  
  - Instruções principais:  
    - `FROM`, `RUN`, `COPY`, `CMD`.  
  - Construção de uma imagem simples usando `docker build`.  

- **Executando Containers Baseados em Imagens**  
  - Comandos úteis:  
    - `docker logs`, `docker exec -it <mycontainer> sh`.
  - Persistência de dados com volumes (`-v` e `--mount`).  

- **Publicação e Reutilização de Imagens**  
  - *Docker Hub*

---

#### **3. Docker Compose: Orquestrando Serviços**  
- **O que é o Docker Compose?**  
  - Diferença entre `docker-compose` e `docker run`.  

- **Criando o Arquivo `docker-compose.yml`:**  
  - Estrutura básica:  
    - Definição de serviços.  
    - Mapeamento de portas (`ports`).  
    - Configuração de volumes e redes.  
  - Exemplo prático:  
    - Aplicação com Python e PostgreSQL.  

- **Comandos Essenciais:**  
  - `docker-compose up`, `docker-compose down`, `docker-compose logs`.  

---

#### **4. Dicas e Boas Práticas para Otimização (15 minutos)**  
- **Reduzindo o Tamanho da Imagem:**  
  - Uso de imagens *base* leves, como `alpine`.  
  - Minimizando camadas no Dockerfile.  
  - Limpeza de arquivos temporários durante a construção (`rm`).  

- **Melhores Práticas no Dockerfile:**  
  - Ordenação lógica das instruções.  
  - Uso do `.dockerignore` para excluir arquivos desnecessários.  
  - Separação de etapas de desenvolvimento e produção (multistage builds).  

- **Melhorias no Tempo de Build e Execução:**  
  - Cache inteligente com camadas estáveis.  
  - Evitar instalação de dependências desnecessárias.  

- **Ferramentas e Debugging:**  
  - Comandos úteis: `docker stats`, `docker system prune`.  
  - Inspeção com `docker inspect` e `docker logs`.  

--- 