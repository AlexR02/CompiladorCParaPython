# "Compilador" C para Python

## Compilação

Para compilar o programa é necessário utilizar o python3 e basta utilizar o seguinte comando no terminal:

``python3 compilador.py`` 

O retorno da execução será um print contendo todos os tokens encontrados e sua devida descrição. E, caso seja possível converter o código em C, uma mensagem de sucesso será apresentada. Você também deve utilizar os arquivos em C contidos na pasta 'CodigosTesteC' já que eles estão um formato no qual o compilador consegue interpretar, para ficar mais fácil, todos os arquivos já estão no compilador, basta tirar o comentário do bloco que você deseja executar.

## Características do Compilador

O compilador foi desenvolvido dentro das etapas de análise anteriores, acreditei que seria mais prático assim, já que todas as analises são feitas em cada linha de uma vez, já é garantido que em cada linha verificada já seja possível realizar as conversões. Principalmente por motivo de tempo, algumas verificações e foram ignoradas no processo de "compilação", como casts e ifs por exemplo. Fora isso creio que todas as outras características dos códigos enviados como exeplo pelo professor foram convertidas de C para Python.
