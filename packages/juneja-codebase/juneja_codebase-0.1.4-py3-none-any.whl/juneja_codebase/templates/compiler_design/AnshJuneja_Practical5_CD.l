%{
#include <stdio.h>
#include <ctype.h>
#include <string.h>

%}

/* List of some common C keywords */
KEYWORD    "int"|"float"|"char"|"double"|"if"|"else"|"for"|"while"|"return"

IDENT      [a-zA-Z_][a-zA-Z0-9_]*
INT        [0-9]+
FLOAT      [0-9]+"."[0-9]+

OP         [+\-*/=<>]

COMMENT1   "//".*
COMMENT2   "/\*([^*]|\*+[^*/])*\*/"

%%

{KEYWORD}      { printf("Keyword: %s\n", yytext); }

{FLOAT}        { printf("Float: %s\n", yytext); }

{INT}          { printf("Integer: %s\n", yytext); }

{IDENT}        { printf("Identifier: %s\n", yytext); }

{OP}           { printf("Operator: %s\n", yytext); }

{COMMENT1}     { printf("Comment: %s\n", yytext); }

{COMMENT2}     { printf("Comment: %s\n", yytext); }

[ \t\n]+       { /* ignore whitespace */ }

.              { printf("Other: %s\n", yytext); }

%%

int yywrap() {
    return 1;
}

int main() {

    yylex();

    return 0;
}
