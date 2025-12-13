%{
#include <stdio.h>
#include <ctype.h>
#include <string.h>
char longestWord[1000];
%}

%%
[A-Za-z]+ {
if (strlen(yytext) > strlen(longestWord)){
strcpy(longestWord, yytext);
}

}


%%

int yywrap(){
return 1;
}

int main(){
yylex();
if(strlen(longestWord) > 0)
printf("Longest word: %s\n", longestWord);
else
printf("No words found \n");

return 0;

}
