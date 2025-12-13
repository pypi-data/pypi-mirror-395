%{
#include <stdio.h>
#include <ctype.h>

int wordCount = 0;
int charCount = 0;
int spaceCount = 0;
int lineCount = 0;
%}

%%

[ \t]     { spaceCount++; charCount++; }

\n        { lineCount++; charCount++; }

[a-zA-Z0-9_]+  { wordCount++; charCount += yyleng; }

.         { charCount++; }

%%

int yywrap() {
    return 1;
}

int main() {

    yyin = fopen("input.c", "r");

    if (!yyin) {
        printf("Cannot open input.c\n");
        return 0;
    }

    yylex();

    printf("Word Count: %d\n", wordCount);
    printf("Character Count: %d\n", charCount);
    printf("Blank Spaces: %d\n", spaceCount);
    printf("Line Count: %d\n", lineCount);

    fclose(yyin);

    return 0;
}
