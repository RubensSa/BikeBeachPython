# Relatório de Segurança - Trabalho 2

## RS01 - Configuração Segura
- ✔ O que foi verificado: configuração de DEBUG, SECRET_KEY, ALLOWED_HOSTS, cookies seguros e headers de segurança.
- ✔ O que foi corrigido: leitura de variáveis de ambiente para DEBUG e SECRET_KEY, definição de ALLOWED_HOSTS e habilitação de opções de segurança com comentários para produção.
- ✔ Como foi implementado: ajuste em settings.py com helpers para leitura de variáveis e configuração de cookies/headers.

## RS02 - Autorização em Nível de Objeto (IDOR)
- ✔ O que foi verificado: acesso direto a bicicletas por identificador.
- ✔ O que foi corrigido: restrição de visualização/edição/exclusão para objetos pertencentes ao usuário autenticado.
- ✔ Como foi implementado: substituição de buscas abertas por get_object_or_404 com filtro pelo dono do objeto nas views de detalhes, edição e exclusão.

## RS03 - Política de Senhas
- ✔ O que foi verificado: validadores de senha configurados no projeto.
- ✔ O que foi corrigido: ajuste do MinimumLengthValidator para mínimo de 10 caracteres e manutenção do CommonPasswordValidator.
- ✔ Como foi implementado: atualização de AUTH_PASSWORD_VALIDATORS em settings.py.

## RS04 - CSRF
- ✔ O que foi verificado: templates com formulários POST.
- ✔ O que foi corrigido: confirmação de uso de csrf_token nos formulários POST existentes.
- ✔ Como foi implementado: revisão dos templates e preservação do token nos formulários.

## RS05 - XSS
- ✔ O que foi verificado: uso de safe/mark_safe nos templates e views.
- ✔ O que foi corrigido: nenhuma ocorrência problemática foi encontrada no projeto atual.
- ✔ Como foi implementado: manutenção do render padrão do Django sem uso de safe/mark_safe.

## RS06 - Logging
- ✔ O que foi verificado: necessidade de registrar eventos sensíveis.
- ✔ O que foi corrigido: configuração de logging simples e registro de exclusão de registro em view sensível.
- ✔ Como foi implementado: criação de logger no módulo rentals.views e configuração em settings.py.

Risco remanescente:
- O projeto ainda depende de um ambiente de produção bem configurado para HTTPS e de variáveis de ambiente corretamente definidas.

Integrantes:
- Rubens Santana Santos e equipe
