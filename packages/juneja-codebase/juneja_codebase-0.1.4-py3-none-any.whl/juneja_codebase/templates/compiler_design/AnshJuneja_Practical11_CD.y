%{
#include <stdio.h>
#include <stdlib.h>

int yylex();
int yyerror(const char *s);
%}

%token NUM
%left '+' '-'
%left '*' '/'

%%

S : E '\n'   { printf("Result = %d\n", $1); }
  ;

E : E '+' E  { $$ = $1 + $3; }
  | E '-' E  { $$ = $1 - $3; }
  | E '*' E  { $$ = $1 * $3; }
  | E '/' E  { $$ = $1 / $3; }
  | NUM      { $$ = $1; }
  ;

%%

int yyerror(const char *s) {
    printf("Invalid expression\n");
    return 0;
}

int main() {
    printf("Enter expression:\n");
    yyparse();
    return 0;
}
