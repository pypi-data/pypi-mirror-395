%{
#include <stdio.h>
#include <stdlib.h>

int yylex();
int yyerror(const char *s);
%}

%token LETTER DIGIT

%%

S : LETTER DIGIT '\n'   { printf("Valid variable\n"); }
  ;

%%

int yyerror(const char *s) {
    printf("Invalid variable\n");
    return 0;
}

int main() {
    printf("Enter variable: ");
    yyparse();
    return 0;
}
