%{
#include <stdio.h>
#include <stdlib.h>

int yylex();
int yyerror(const char *s);
%}

%token A B

%%

S : A BPLUS '\n'   { printf("Valid string\n"); }
  ;

BPLUS : B
      | B BPLUS
      ;

%%

int yyerror(const char *s) {
    printf("Invalid string\n");
    return 0;
}

int main() {
    printf("Enter string: ");
    yyparse();
    return 0;
}
