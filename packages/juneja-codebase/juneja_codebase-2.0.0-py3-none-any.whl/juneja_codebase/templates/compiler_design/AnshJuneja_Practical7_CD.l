%{
#include <stdio.h>
#include <string.h>

void print_substrings(char *s);
%}

%%

"abcd" {
    /* yytext holds the matched string "abcd" */
    print_substrings(yytext);
}

.|\n { /* Ignore all other characters */ }

%%

void print_substrings(char *s) {
    int len = strlen(s);
    int i;

    for (i = len; i >= 1; i--) {
        printf("%.*s\n", i, s);
    }
}

int main(void) {
    printf("Please enter the string 'abcd': \n");
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}