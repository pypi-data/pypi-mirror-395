%{
#include <stdio.h>
#include <ctype.h>

char shift_char(char c) {
    if (c >= 'a' && c <= 'z') {
        return 'a' + ( (c - 'a' + 3) % 26 );
    }
    else if (c >= 'A' && c <= 'Z') {
        return 'A' + ( (c - 'A' + 3) % 26 );
    }
    else {
        return c;
    }
}
%}

%%
[a-zA-Z] {
    char c = yytext[0];
    c = shift_char(c);
    printf("%c", c);
}

.|\n {
    printf("%s", yytext);
}
%%

int yywrap() {
    return 1;
}

int main() {

    yylex();

    return 0;
}
