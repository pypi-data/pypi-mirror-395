%{
#include <stdio.h>
#include <stdlib.h>

int yylex();
int yyerror(const char *s);
%}

%token NUM

%%

S : E '\n'         { printf("Valid expression\n"); }
  ;

E : E '+' E
  | E '-' E
  | E '*' E
  | E '/' E
  | '(' E ')'
  | NUM
  ;

%%

int yyerror(const char *s)
{
    printf("Invalid expression\n");
    return 0;
}

int main() {
    printf("Enter expression:\n");
    yyparse();
    return 0;
}
