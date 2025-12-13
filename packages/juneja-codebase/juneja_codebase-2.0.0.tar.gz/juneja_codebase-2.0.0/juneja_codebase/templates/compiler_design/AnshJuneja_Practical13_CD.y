%{
#include <stdio.h>
#include <stdlib.h>

int yylex();
int yyerror(const char *s);
int count = 0;
%}

%token A B

%%

S : ALIST B '\n'
    {
        if (count >= 1)
            printf("Valid string\n");
        else
            printf("Invalid string\n");
    }
  ;

ALIST : A            { count++; }
      | ALIST A      { count++; }
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
