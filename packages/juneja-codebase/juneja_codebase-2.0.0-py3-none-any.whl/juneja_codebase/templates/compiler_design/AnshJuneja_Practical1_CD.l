%{
#include <stdio.h>
#include <ctype.h>
int charCount = 0;
int lineCount = 1;
int numCount = 0;
int special = 0;
%}

%%
[\n] lineCount++; printf("%c" , yytext[0]);
[a-zA-Z] charCount++; printf("%c", yytext[0]);
[0-9] numCount++; printf("%c" , yytext[0]);
[@#$%*<:>;&^!()_+=|\~`{}] special = 1; printf("%c" , yytext[0]);

%%
int yywrap(){
return 1;
}

int main(int argc, char* argv[]){

yyin = fopen("input.txt", "r");
yyout = fopen("output.txt", "w");

yylex();

fprintf(yyout,"Line Count %d\n ", lineCount);
fprintf(yyout,"Character Count %d\n ", charCount);
fprintf(yyout,"Number Count %d\n ", numCount);
if (special==1)fprintf(yyout,"Special: True\n");
else fprintf(yyout,"Special: False\n");

fclose(yyin);
fclose(yyout);

return 0;
}
