%{
#include<stdio.h>
#include<ctype.h>
int vowelcnt = 0;
int constcnt = 0;
%}

%%
[aeiouAEIOU] vowelcnt++;
[a-zA-Z] constcnt++;

%%
int yywrap() {
 return 1;
}

int main(){

yylex();

printf("vowel count : %d\n",vowelcnt);
printf("Consonant Count : %d\n", constcnt);


return 0;

}
