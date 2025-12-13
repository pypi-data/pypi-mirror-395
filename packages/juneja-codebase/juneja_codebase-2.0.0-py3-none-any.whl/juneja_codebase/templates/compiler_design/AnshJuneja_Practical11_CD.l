%{
#include "y.tab.h"
%}

%%

[0-9]+     { yylval = atoi(yytext); return NUM; }
[+\-*/]    { return yytext[0]; }
\n         { return '\n'; }
[ \t]      { /* ignore */ }
.          { /* invalid */ }

%%

int yywrap() { return 1; }
