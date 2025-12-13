%{
#include <stdio.h>

int valid = 1;
%}

%%

[0-9]+              { /* valid number */ }

[+\-*/]             { /* operator */ }

[() ]               { /* parentheses or space */ }

\n                  { return 0; }

.                   { valid = 0; }

%%

int yywrap() { return 1; }

int main() {
    printf("Enter expression: ");
    yylex();

    if (valid)
        printf("Valid expression\n");
    else
        printf("Invalid expression\n");

    return 0;
}
