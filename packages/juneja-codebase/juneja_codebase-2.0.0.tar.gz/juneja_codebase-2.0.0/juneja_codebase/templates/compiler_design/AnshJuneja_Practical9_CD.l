%{
#include "y.tab.h"
%}

%%

[0-9]+        { return NUM; }

[+\-*/()]     { return yytext[0]; }

[ \t]         { /* ignore spaces */ }

\n            { return '\n'; }

.             { return yytext[0]; }

%%

int yywrap() { return 1; }
